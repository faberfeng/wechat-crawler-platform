#!/usr/bin/env python3
"""
快速获取微信公众号文章链接
使用浏览器访问并提取公众号信息
"""
import asyncio
from playwright.async_api import async_playwright
import re


async def main():
    """从文章链接获取公众号信息"""

    # 示例文章链接
    sample_url = "https://mp.weixin.qq.com/s/1v_icW5yqVErsIZQIXHGnQ"

    async with async_playwright() as p:
        browser = await p.chromium.launch(
            headless=False,
            args=['--disable-blink-features=AutomationControlled']
        )

        context = await browser.new_context(
            user_agent='Mozilla/5.0 (Linux; Android 12; SM-G996B) AppleWebKit/537.36 (KHTML, like Gecko) Version/4.0 Chrome/108.0.5359.128 Mobile Safari/537.36 MicroMessenger/8.0.32',
            viewport={'width': 375, 'height': 812},
            is_mobile=True,
            locale='zh-CN'
        )

        page = await context.new_page()

        try:
            print(f"正在访问文章: {sample_url}")
            await page.goto(f"{sample_url}?scene=1", wait_until="networkidle", timeout=30000)
            await asyncio.sleep(3)

            # 提取公众号名称
            account_name = "未找到"
            try:
                account_name_elem = await page.query_selector('#js_name')
                if account_name_elem:
                    account_name = await account_name_elem.text_content()
                    print(f"\n✅ 公众号名称: {account_name}\n")
            except:
                pass

            # 提取文章标题
            title = "未找到"
            try:
                title_elem = await page.query_selector('#activity-name')
                if title_elem:
                    title = await title_elem.text_content()
                    print(f"📄 文章标题: {title}")
            except:
                pass

            # 提取 biz 参数
            biz = None
            page_html = await page.content()
            pattern = r'__biz=([A-Za-z0-9=]+)'
            match = re.search(pattern, page_html)
            if match:
                biz = match.group(1)
                print(f"🔑 公众号 ID (biz): {biz}\n")

            # 截图保存
            await page.screenshot(path="./article_sample.png")
            print("✅ 截图已保存: ./article_sample.png\n")

            # 构造历史消息链接
            if biz:
                history_url = f"https://mp.weixin.qq.com/mp/profile_ext?action=home&__biz={biz}&scene=124&devicetype=android&version=28000337&lang=zh_CN&nettype=WIFI&a8scene=3&fontScale=100"
                print(f"📚 历史消息链接:")
                print(f"   {history_url}")
                print("\n提示: 可以在浏览器中打开此链接查看所有文章")

            # 提取文章正文（前500字）
            try:
                content_elem = await page.query_selector('.rich_media_content')
                if content_elem:
                    content_text = await content_elem.inner_text()
                    print(f"\n📝 文章内容预览（前500字）:")
                    print("=" * 80)
                    print(content_text[:500])
                    print("=" * 80)
                    print(f"\n（完整内容共 {len(content_text)} 字）")
            except Exception as e:
                print(f"提取正文失败: {e}")

            print("\n💡 使用方法:")
            print("1. 在浏览器中打开历史消息链接")
            print("2. 手动复制感兴趣的文章链接")
            print("3. 使用此脚本访问并提取文章内容")
            print("\n或者运行下面命令启动扫码登录，让爬虫自动抓取所有文章:")
            print("  cd ~/Desktop/wechat-crawler-platform/backend")
            print("  python3 login_wechat.py")

            # 保持浏览器打开
            print("\n浏览器将保持打开 30 秒供观察...")
            await asyncio.sleep(30)

        except Exception as e:
            print(f"❌ 错误: {e}", file=sys.stderr)
            import traceback
            traceback.print_exc()
        finally:
            await browser.close()


if __name__ == "__main__":
    import sys
    print("""
╔══════════════════════════════════════════════════════════════════╗
║          微信公众号文章快速提取工具                              ║
╚══════════════════════════════════════════════════════════════════╝
""")
    asyncio.run(main())
