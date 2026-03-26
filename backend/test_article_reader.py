#!/usr/bin/env python3
"""
使用 wechat-mp-reader skill 获取微信公众号文章
"""
import sys
sys.path.insert(0, '/Users/fengweibo/.openclaw/workspace/skills/wechat-mp-reader')

from app.services.crawler.browser_pool import BrowserPool
from playwright.async_api import async_playwright
import asyncio


async def main():
    """主函数"""
    # 示例：提取 "活力大宁" 的其他文章

    # 从已知文章 URL 提取 biz
    sample_url = "https://mp.weixin.qq.com/s/1v_icW5yqVErsIZQIXHGnQ"

    async with async_playwright() as p:
        browser = await p.chromium.launch(
            headless=False,
            args=['--disable-blink-features=AutomationControlled']
        )

        context = await browser.new_context(
            user_agent='Mozilla/5.0 (iPhone; CPU iPhone OS 16_0 like Mac OS X) AppleWebKit/605.1.15 (KHTML, like Gecko) Mobile/15E148 MicroMessenger/8.0.32',
            viewport={'width': 375, 'height': 812},
            is_mobile=True,
            locale='zh-CN'
        )

        page = await context.new_page()

        try:
            # 访问文章页
            print(f"正在访问: {sample_url}")
            await page.goto(f"{sample_url}?scene=1", wait_until="networkidle", timeout=30000)
            await asyncio.sleep(2)

            # 提取公众号名称
            account_name_elem = await page.query_selector('#js_name')
            account_name = await account_name_elem.text_content() if account_name_elem else "未知"

            print(f"\n公众号: {account_name}\n")

            # 提取文章内容
            article_content = await page.query_selector('.rich_media_content')
            if article_content:
                content_html = await article_content.inner_text()
                print(f"文章内容长度: {len(content_html)} 字符")
                print(f"文章内容预览（前200字）:\n{content_html[:200]}...")
            else:
                print("未找到文章内容")

            # 尝试查找"查看历史消息"链接
            history_links = await page.query_selector_all('a')
            history_url = None

            for link in history_links:
                text = await link.text_content()
                if text and ("历史消息" in text or "文章" in text):
                    href = await link.get_attribute('href')
                    if href and "__biz" in href:
                        history_url = href
                        break

            if history_url:
                print(f"\n找到历史消息链接: {history_url}")
                print("\n提示: 可以访问这个链接查看公众号的所有文章")
            else:
                print("\n未找到历史消息链接（通常在页面底部，需要滚动）")
                print("可以手动在浏览器中打开查看")

        except Exception as e:
            print(f"错误: {e}", file=sys.stderr)
        finally:
            await asyncio.sleep(5)  # 保持 5 秒供观察
            await browser.close()


if __name__ == "__main__":
    asyncio.run(main())
