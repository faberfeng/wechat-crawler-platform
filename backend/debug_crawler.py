#!/usr/bin/env python3
"""
微信爬虫诊断脚本
测试访问微信公众号时是否需要登录态
"""
import asyncio
from playwright.async_api import async_playwright
import sys


async def test_page():
    """测试访问页面"""
    async with async_playwright() as p:
        # 启动浏览器（非无头模式，便于观察）
        browser = await p.chromium.launch(
            headless=False,
            args=['--disable-blink-features=AutomationControlled']
        )

        context = await browser.new_context(
            user_agent='Mozilla/5.0 (iPhone; CPU iPhone OS 16_0 like Mac OS X) AppleWebKit/605.1.15 (KHTML, like Gecko) Mobile/15E148 MicroMessenger/8.0.32',
            viewport={'width': 375, 'height': 812},
            is_mobile=True,
            locale='zh-CN',
            timezone_id='Asia/Shanghai'
        )

        page = await context.new_page()

        # 测试 URL
        biz = "MjM5NjE2ODAyMA=="
        url = f"https://mp.weixin.qq.com/mp/profile_ext?action=home&__biz={biz}&scene=124&devicetype=android&version=28000337&lang=zh_CN&nettype=WIFI&a8scene=3&fontScale=100"

        print(f"正在访问: {url}")
        print("=" * 80)

        try:
            await page.goto(url, wait_until="networkidle", timeout=30000)
            await asyncio.sleep(3)

            # 截图
            screenshot_path = "./debug_screenshot.png"
            await page.screenshot(path=screenshot_path)
            print(f"✅ 截图已保存: {screenshot_path}")

            # 获取页面标题
            title = await page.title()
            print(f"页面标题: {title}")

            # 检查页面内容
            body_text = await page.inner_text("body")
            print(f"页面内容长度: {len(body_text)}")

            # 检查是否有"访问过于频繁"提示
            if "访问过于频繁" in body_text:
                print("❌ 被限流！需要登录态或降低访问频率")
            elif "请在微信客户端打开" in body_text:
                print("❌ 页面要求在微信客户端打开")
            elif "验证" in body_text:
                print("❌ 页面要求验证")
            else:
                print("✅ 页面看起来正常，检查文章元素...")

                # 尝试查找文章元素
                articles = await page.query_selector_all('[data-id]')
                print(f"找到 {len(articles)} 个 [data-id] 元素")

                if len(articles) == 0:
                    # 打印 HTML 结构供调试
                    html = await page.content()
                    print("\n页面 HTML 片段（前500字符）:")
                    print(html[:500])
                else:
                    print("✅ 找到文章元素！")
                    for i, article in enumerate(articles[:3]):
                        title = await article.inner_text()
                        print(f"  文章 {i+1}: {title[:100]}...")

            # 保持浏览器打开 10 秒供人工观察
            print("\n浏览器将保持打开 10 秒供观察...")
            await asyncio.sleep(10)

        except Exception as e:
            print(f"❌ 访问失败: {e}", file=sys.stderr)
        finally:
            await browser.close()


async def test_with_login():
    """测试带登录态的访问（如果有保存的 session）"""
    import os

    session_path = "./data/auth_sessions/"
    if os.path.exists(session_path):
        session_files = [f for f in os.listdir(session_path) if f.endswith('.json')]
        if session_files:
            print(f"\n发现 {len(session_files)} 个登录态文件")
            print("可以尝试加载登录态后测试")


if __name__ == "__main__":
    print("微信爬虫诊断工具")
    print("=" * 80)
    asyncio.run(test_page())
    asyncio.run(test_with_login())
