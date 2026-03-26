import asyncio
import html2text
import random
import json
from pathlib import Path
from datetime import datetime
from typing import List, Dict, Optional
from playwright.async_api import async_playwright, Browser, BrowserContext, Page
from app.core.config import settings
from app.core.logger import logger


class BrowserPool:
    """浏览器实例池 - 支持登录态管理"""

    def __init__(self, max_instances: int = None):
        self.max_instances = max_instances or settings.MAX_BROWSERS
        self.browsers: List[Browser] = []
        self.contexts: List[BrowserContext] = []
        self.playwright = None
        self.auth_session_dir = Path(settings.AUTH_SESSIONS_DIR)

    async def init(self):
        """初始化浏览器池，自动加载可用的登录态"""
        logger.info(f"正在初始化浏览器池（{self.max_instances} 个实例）...")

        # 确保登录态目录存在
        self.auth_session_dir.mkdir(parents=True, exist_ok=True)

        self.playwright = await async_playwright().start()

        # 获取可用的登录态文件
        session_files = list(self.auth_session_dir.glob("*.json"))
        has_auth = len(session_files) > 0

        for i in range(self.max_instances):
            browser = await self.playwright.chromium.launch(
                headless=settings.HEADLESS_BROWSER,
                args=[
                    '--disable-blink-features=AutomationControlled',
                    '--no-sandbox',
                    '--disable-dev-shm-usage',
                    '--disable-web-security',
                    '--disable-features=IsolateOrigins,site-per-process',
                    '--disable-infobars',
                ]
            )

            # 创建上下文选项
            context_options = {
                'user_agent': self._get_random_ua(),
                'viewport': {'width': 375, 'height': 812},
                'device_scale_factor': 2,
                'is_mobile': True,
                'has_touch': True,
                'locale': 'zh-CN',
                'timezone_id': 'Asia/Shanghai'
            }

            # 加载登录态（如果有）
            if has_auth and session_files:
                session_file = session_files[i % len(session_files)]
                try:
                    with open(session_file, 'r', encoding='utf-8') as f:
                        storage_state = json.load(f)
                    context_options['storage_state'] = storage_state
                    logger.info(f"✅ 浏览器实例 {i} 加载登录态: {session_file.name}")
                except Exception as e:
                    logger.warning(f"⚠️ 浏览器实例 {i} 加载登录态失败: {e}")

            context = await browser.new_context(**context_options)

            self.browsers.append(browser)
            self.contexts.append(context)
            logger.debug(f"浏览器实例 {i} 已创建")

        logger.info(f"浏览器池初始化完成，共 {self.max_instances} 个实例（登录态: {'已启用' if has_auth else '未配置'}）")

    def _get_random_ua(self) -> str:
        """获取随机微信 UA"""
        uas = [
            "Mozilla/5.0 (Linux; Android 12; SM-G996B) AppleWebKit/537.36 (KHTML, like Gecko) Version/4.0 Chrome/108.0.5359.128 Mobile Safari/537.36 MicroMessenger/8.0.32",
            "Mozilla/5.0 (Linux; Android 13; Pixel 7) AppleWebKit/537.36 (KHTML, like Gecko) Version/4.0 Chrome/116.0.0.0 Mobile Safari/537.36 MicroMessenger/8.0.40",
            "Mozilla/5.0 (iPhone; CPU iPhone OS 16_0 like Mac OS X) AppleWebKit/605.1.15 (KHTML, like Gecko) Mobile/15E148 MicroMessenger/8.0.32",
            "Mozilla/5.0 (Linux; Android 11; vivo V2134A) AppleWebKit/537.36 (KHTML, like Gecko) Version/4.0 Chrome/108.0.5359.128 Mobile Safari/537.36 MicroMessenger/8.0.33",
        ]
        return random.choice(uas)

    async def get_context(self, index: int = 0) -> BrowserContext:
        """获取浏览器上下文"""
        if not self.contexts:
            await self.init()
        return self.contexts[index % len(self.contexts)]

    async def close_all(self):
        """关闭所有浏览器"""
        for context in self.contexts:
            await context.close()
        for browser in self.browsers:
            await browser.close()
        if self.playwright:
            await self.playwright.stop()
        logger.info("浏览器池已关闭")

    async def __aenter__(self):
        await self.init()
        return self

    async def __aexit__(self, exc_type, exc_val, exc_tb):
        await self.close_all()

    async def login_and_save_session(self, account_name: str = "default") -> str:
        """
        扫码登录并保存 session

        Args:
            account_name: 账号名称（用户自定义）

        Returns:
            session 文件路径
        """
        logger.info(f"开始为账号 '{account_name}' 扫码登录...")

        # 创建一个非无头模式的浏览器
        browser = await self.playwright.chromium.launch(
            headless=False,  # 显示浏览器窗口
            args=['--disable-blink-features=AutomationControlled']
        )

        context = await browser.new_context(
            user_agent=self._get_random_ua(),
            viewport={'width': 375, 'height': 812},
            device_scale_factor=2,
            is_mobile=True,
            has_touch=True,
            locale='zh-CN',
            timezone_id='Asia/Shanghai'
        )

        page = await context.new_page()

        try:
            # 访问微信登录页
            logger.info("正在打开微信扫码登录页...")
            await page.goto("https://mp.weixin.qq.com/", wait_until="networkidle")

            # 等待用户扫码登录
            logger.info("📱 请使用微信扫描二维码登录...")
            logger.info("登录成功后按 Ctrl+C 继续，或等待 5 分钟自动超时")

            # 等待跳转到登录后的页面
            try:
                await page.wait_for_url(
                    lambda url: "mp.weixin.qq.com" in url and "login" not in url,
                    timeout=300000  # 5 分钟超时
                )
                logger.info("✅ 登录成功！")
            except:
                logger.warning("⚠️ 等待超时，假设已登录")

            # 保存 session
            session_file = self.auth_session_dir / f"{account_name}_{datetime.now().strftime('%Y%m%d_%H%M%S')}.json"
            storage_state = await context.storage_state(path=str(session_file))

            logger.info(f"✅ 登录态已保存: {session_file}")

            # 更新所有上下文使用新的登录态
            await self._reload_sessions()

            return str(session_file)

        except Exception as e:
            logger.error(f"❌ 登录失败: {e}", exc_info=True)
            raise
        finally:
            await page.close()
            await context.close()
            await browser.close()

    async def _reload_sessions(self):
        """重新加载所有登录态"""
        session_files = list(self.auth_session_dir.glob("*.json"))
        if not session_files:
            return

        logger.info(f"重新加载 {len(session_files)} 个登录态...")

        for i, context in enumerate(self.contexts):
            session_file = session_files[i % len(session_files)]
            try:
                with open(session_file, 'r', encoding='utf-8') as f:
                    storage_state = json.load(f)

                # 清空并重新添加 cookies
                await context.clear_cookies()
                await context.add_cookies(storage_state.get('cookies', []))

                logger.debug(f"浏览器实例 {i} 重新加载登录态: {session_file.name}")
            except Exception as e:
                logger.warning(f"⚠️ 浏览器实例 {i} 重新加载登录态失败: {e}")
