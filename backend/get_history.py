#!/usr/bin/env python3
"""
获取"活力大宁"历史文章列表
尝试从文章页面提取历史消息链接
"""
import asyncio
import re
from playwright.async_api import async_playwright


async def main():
    """主函数"""
    article_url = "https://mp.weixin.qq.com/s/1v_icW5yqVErsIZQIXHGnQ?scene=1"

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
            print(f"正在访问文章页，查找历史消息链接...")

            await page.goto(article_url, wait_until="networkidle", timeout=30000)
            await asyncio.sleep(3)

            # 提取 biz（通过多种方式）
            biz = None

            # 方法1: 从页面 HTML 中提取
            html = await page.content()
            pattern = r'__biz=([A-Za-z0-9=]+)'
            match = re.search(pattern, html)
            if match:
                biz = match.group(1)

            # 方法2: 从 JS 变量中提取
            if not biz:
                js_result = await page.evaluate("() => window.__biz || window.missionBiz || window.missionNo")
                if js_result:
                    biz = js_result

            # 方法3: 从 meta 标签提取
            if not biz:
                meta_biz = await page.evaluate("""
                    () => {
                        const meta = document.querySelector('meta[name*="biz"]');
                        return meta ? meta.content : null;
                    }
                """)
                if meta_biz:
                    biz = meta_biz

            if biz:
                print(f"✅ 找到公众号 ID: {biz}")

                # 构造历史消息链接
                history_url = f"https://mp.weixin.qq.com/mp/profile_ext?action=home&__biz={biz}&scene=124&devicetype=android&version=28000337&lang=zh_CN&nettype=WIFI&a8scene=3&fontScale=100"

                print(f"\n📚 历史消息链接:")
                print(f"{history_url}")

                print("\n选项:")
                print("1. 在浏览器中打开此链接查看所有文章")
                print("2. 运行扫码登录后让爬虫自动抓取所有文章")
                print("\n如果选项1失败（需要登录），请使用选项2：")
                print("  cd ~/Desktop/wechat-crawler-platform/backend")
                print("  python3 login_wechat.py")

                # 尝试自动打开历史消息页
                print("\n正在尝试打开历史消息页...")
                await page.goto(history_url, wait_until="domcontentloaded", timeout=30000)
                await asyncio.sleep(5)

                # 尝试提取文章
                articles = await page.query_selector_all('[data-id]')
                print(f"\n当前页面找到 {len(articles)} 个文章")

                if len(articles) > 0:
                    print("\n✅ 成功！这里显示的是历史文章列表")
                    print("你可以手动复制感兴趣的文章链接")
                else:
                    print("\n⚠️ 页面可能需要登录才能显示完整内容")
                    print("建议使用扫码登录方式")

            else:
                print("❌ 无法找到公众号 ID")

                # 尝试查找历史消息按钮
                print("\n尝试查找历史消息按钮...")
                history_buttons = await page.query_selector_all('a')
                for btn in history_buttons[:20]:  # 只检查前20个
                    text = await btn.text_content()
                    if text and ('历史' in text or '消息' in text or '文章' in text):
                        href = await btn.get_attribute('href')
                        print(f"  找到: {text[:50]}")
                        if href and '__biz' in href:
                            print(f"  链接: {href[:100]}...")

            # 保持浏览器打开
            print("\n浏览器将保持打开 60 秒供观察...")
            await asyncio.sleep(60)

        except Exception as e:
            print(f"❌ 错误: {e}")
            import traceback
            traceback.print_exc()
        finally:
            await browser.close()


if __name__ == "__main__":
    asyncio.run(main())
