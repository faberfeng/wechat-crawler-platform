"""
获取微信公众号 biz 参数的脚本 - 方法2：访问公众号资料页
"""
import sys
sys.path.append('/Users/fengweibo/Desktop/wechat-crawler-platform/backend')

from playwright.sync_api import sync_playwright
import re
from urllib.parse import urlparse, parse_qs

def get_biz_from_search(search_url):
    """通过搜索获取 biz 参数"""
    with sync_playwright() as p:
        browser = p.chromium.launch(headless=True)
        page = browser.new_page(
            user_agent='Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36'
        )

        try:
            print(f"正在访问搜索页面: {search_url}")
            page.goto(search_url, timeout=30000)

            # 等待页面加载
            page.wait_for_timeout(5000)

            # 获取页面内容
            page_content = page.content()

            # 尝试从搜索结果中提取 biz
            biz_pattern = r'"biz"\s*:\s*"([A-Za-z0-9+=/]+)"'
            matches = re.findall(biz_pattern, page_content)

            if matches:
                print(f"\n找到 {len(matches)} 个 biz 参数:")
                for i, biz in enumerate(matches, 1):
                    print(f"{i}. {biz}")
                return matches[0]  # 返回第一个

            print("未从搜索结果找到 biz 参数")
            return None

        except Exception as e:
            print(f"访问搜索页面出错: {e}")
            return None
        finally:
            browser.close()

def get_biz_from_profile(account_name):
    """
    通过公众号搜索获取 biz 参数
    微信公众平台搜索：http://weixin.sogou.com/
    """
    # 使用搜狗微信搜索
    search_url = f"http://weixin.sogou.com/weixin?type=1&query={account_name}&ie=utf8"

    with sync_playwright() as p:
        browser = p.chromium.launch(headless=True)
        page = browser.new_page(
            user_agent='Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36'
        )

        try:
            print(f"正在搜索公众号: {account_name}")
            print(f"搜索 URL: {search_url}")
            page.goto(search_url, timeout=30000)

            # 等待页面加载
            page.wait_for_timeout(5000)

            # 查找第一个公众号链接
            account_links = page.query_selector_all('a[href*="mp.weixin.qq.com"]')

            for link in account_links[:3]:  # 检查前3个链接
                href = link.get_attribute('href')
                print(f"\n找到链接: {href[:100]}...")

                # 从链接中提取 biz
                if '__biz=' in href:
                    biz_start = href.find('__biz=')
                    biz_end = href.find('&', biz_start)
                    if biz_end == -1:
                        biz_end = len(href)
                    biz = href[biz_start + 6:biz_end]
                    print(f"✅ 找到 biz: {biz}")
                    return biz

            print("未从搜索结果找到 biz 参数")
            return None

        except Exception as e:
            print(f"搜索公众号出错: {e}")
            return None
        finally:
            browser.close()

if __name__ == "__main__":
    account_name = "上海静安"

    print("=" * 60)
    print(f"搜索公众号: {account_name}")
    print("=" * 60)

    biz = get_biz_from_profile(account_name)

    if biz:
        print(f"\n✅ 成功获取 biz 参数: {biz}")
        print(f"\n可以使用以下命令添加公众号:")
        print(f'curl -X POST http://localhost:8002/api/v1/accounts \\')
        print(f'  -H "Content-Type: application/json" \\')
        print(f"  -H \"Authorization: Bearer YOUR_TOKEN\" \\")
        print(f'  -d \'{{"biz":"{biz}","name":"上海静安","is_active":true}}\'')
    else:
        print("\n❌ 未能获取 biz 参数")
        print("请手动检查或使用公众号文章链接")
