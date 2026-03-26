#!/usr/bin/env python3
"""
微信公众号文章提取器
基于 wechat-mp-reader skill 的逻辑
"""
import asyncio
import sys
import re
from playwright.async_api import async_playwright
from urllib.parse import urlparse, parse_qs


def normalize_url(url):
    """标准化 URL，确保带有 ?scene=1"""
    if not url.startswith('https://mp.weixin.qq.com/'):
        raise ValueError("不是微信公众号文章链接")

    # 检查是否已有 scene=1
    if '?scene=1' in url:
        return url

    # 如果没有 query params，直接追加
    if '?' not in url:
        return url + '?scene=1'

    # 如果有其他 params，需要重新构造
    parsed = urlparse(url)
    params = parse_qs(parsed.query)
    params['scene'] = ['1']

    # 重新构造 query string
    new_query = '&'.join([f"{k}={v[0]}" for k, v in params.items()])
    return f"{parsed.scheme}://{parsed.netloc}{parsed.path}?{new_query}"


async def extract_article(url):
    """提取文章内容"""
    normalized_url = normalize_url(url)

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
            print(f"📖 正在访问: {normalized_url}")
            await page.goto(normalized_url, wait_until="networkidle", timeout=30000)

            # 等待内容加载
            try:
                await page.wait_for_selector('.rich_media_content', timeout=10000)
            except:
                print("⚠️ 等待内容超时，尝试直接提取")

            await asyncio.sleep(2)

            # 提取标题
            title = "未知标题"
            title_elem = await page.query_selector('#activity-name')
            if title_elem:
                title = await title_elem.text_content()

            # 提取公众号
            account = "未知公众号"
            account_elem = await page.query_selector('#js_name')
            if account_elem:
                account = await account_elem.text_content()

            # 提取发布时间
            publish_time = "未知时间"
            time_elem = await page.query_selector('#publish_time')
            if time_elem:
                publish_time = await time_elem.text_content()

            # 提取正文
            content = ""
            content_elem = await page.query_selector('.rich_media_content')
            if content_elem:
                content = await content_elem.inner_text()

            # 提取 biz 参数
            biz = None
            page_html = await page.content()
            match = re.search(r'__biz=([A-Za-z0-9=]+)', page_html)
            if match:
                biz = match.group(1)

            print("\n" + "=" * 80)
            print(f"📰 公众号: {account}")
            print(f"📝 标题: {title}")
            print(f"🕐 发布时间: {publish_time}")
            print(f"🔑 公众号 ID: {biz or '未找到'}")
            print("=" * 80)

            print(f"\n📄 正文内容（共 {len(content)} 字）:\n")
            print(content)

            # 截图
            await page.screenshot(path="./article_extracted.png")
            print(f"\n✅ 截图已保存: ./article_extracted.png")

            return {
                'title': title,
                'account': account,
                'publish_time': publish_time,
                'biz': biz,
                'content': content,
                'content_length': len(content)
            }

        except Exception as e:
            print(f"❌ 提取失败: {e}", file=sys.stderr)
            raise
        finally:
            await asyncio.sleep(2)  # 保持 2 秒供观察
            await browser.close()


if __name__ == "__main__":
    if len(sys.argv) < 2:
        print("用法: python3 extract_article.py <微信文章链接>")
        print("\n示例:")
        print("  python3 extract_article.py https://mp.weixin.qq.com/s/xxx")
        sys.exit(1)

    url = sys.argv[1]

    print("""
╔══════════════════════════════════════════════════════════════════╗
║              微信公众号文章提取器                                ║
╚══════════════════════════════════════════════════════════════════╝
""")

    asyncio.run(extract_article(url))
