"""
从微信公众号历史页获取 biz 参数
"""
import sys
sys.path.append('/Users/fengweibo/Desktop/wechat-crawler-platform/backend')

from playwright.sync_api import sync_playwright
import re

from playwright.sync_api import sync_playwright
import re

def get_biz_from_history(article_url):
    """
    从文章页面跳转到历史记录获取 biz
    """
    with sync_playwright() as p:
        browser = p.chromium.launch(headless=False)  # 使用非无头模式，可以看到操作
        page = browser.new_page(
            user_agent='Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36'
        )

        try:
            print(f"正在访问文章: {article_url}")
            page.goto(article_url, timeout=30000)

            # 等待页面加载
            page.wait_for_timeout(5000)

            print("页面已加载，正在查找公众号名称链接...")

            # 查找公众号名称链接
            account_name_elements = page.query_selector_all('a')

            for element in account_name_elements:
                text = element.text_content()
                href = element.get_attribute('href')

                if '上海静安' in text:
                    print(f"找到链接: {href}")
                    print(f"链接文本: {text}")

                    if href and 'mp.weixin.qq.com' in href:
                        # 尝试从链接中提取 biz
                        if '__biz=' in href:
                            biz_start = href.find('__biz=')
                            biz_end = href.find('&', biz_start)
                            if biz_end == -1:
                                biz_end = len(href)
                            biz = href[biz_start + 6:biz_end]
                            print(f"✅ 找到 biz: {biz}")
                            return biz

                        # 点击链接，进入公众号主页
                        print("点击公众号名称...")
                        element.click()
                        page.wait_for_timeout(3000)

                        # 获取当前 URL
                        current_url = page.url
                        print(f"当前 URL: {current_url}")

                        if '__biz=' in current_url:
                            biz_start = current_url.find('__biz=')
                            biz_end = current_url.find('&', biz_start)
                            if biz_end == -1:
                                biz_end = len(current_url)
                            biz = current_url[biz_start + 6:biz_end]
                            print(f"✅ 从主页 URL 找到 biz: {biz}")
                            return biz

            print("未能找到公众号名称链接")
            return None

        except Exception as e:
            print(f"操作出错: {e}")
            import traceback
            traceback.print_exc()
            return None
        finally:
            print("\n浏览器将在 5 秒后关闭...")
            page.wait_for_timeout(5000)
            browser.close()

if __name__ == "__main__":
    article_url = "https://mp.weixin.qq.com/s/ZKXjKURWMMStlij6OhUbiA"

    print("=" * 60)
    print("从文章页面获取公众号 biz 参数")
    print("=" * 60)

    biz = get_biz_from_history(article_url)

    if biz:
        print(f"\n✅ 成功获取 biz 参数: {biz}")
        print(f"\n可以使用以下命令添加公众号:")
        print(f'curl -X POST http://localhost:8002/api/v1/accounts \\')
        print(f'  -H "Content-Type: application/json" \\')
        print(f"  -H \"Authorization: Bearer YOUR_TOKEN\" \\")
        print(f'  -d \'{{"biz":"{biz}","name":"上海静安","is_active":true}}\'')
    else:
        print("\n❌ 未能获取 biz 参数")
