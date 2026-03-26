"""
获取微信公众号 biz 参数的脚本
"""
import sys
sys.path.append('/Users/fengweibo/Desktop/wechat-crawler-platform/backend')

from playwright.sync_api import sync_playwright
import re
from urllib.parse import urlparse, parse_qs

def get_biz_from_url(url):
    """从 URL 中提取 biz 参数"""
    # 尝试从 URL 参数中提取
    if '__biz=' in url:
        biz_start = url.find('__biz=')
        biz_end = url.find('&', biz_start)
        if biz_end == -1:
            biz_end = len(url.url)
        biz = url[biz_start + 6:biz_end]
        return biz

    # 尝试从 parse_qs 中提取
    parsed = urlparse(url)
    params = parse_qs(parsed.query)
    if '__biz' in params:
        return params['__biz'][0]

    return None

def get_biz_from_page(url):
    """通过访问页面获取 biz 参数"""
    with sync_playwright() as p:
        # 启动浏览器
        browser = p.chromium.launch(headless=True)
        page = browser.new_page(user_agent='Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36')

        try:
            print(f"正在访问: {url}")
            page.goto(url, timeout=30000)

            # 等待页面加载
            page.wait_for_timeout(3000)

            # 从 URL 获取 biz
            current_url = page.url
            print(f"当前 URL: {current_url}")

            biz = get_biz_from_url(current_url)
            if biz:
                print(f"找到 biz: {biz}")
                return biz

            # 尝试从页面内容中提取
            page_content = page.content()

            # 尝试匹配 biz 格式
            biz_pattern = r'"biz"\s*:\s*"([A-Za-z0-9+=/]+)"'
            match = re.search(biz_pattern, page_content)
            if match:
                biz = match.group(1)
                print(f"从页面找到 biz: {biz}")
                return biz

            # 尝试从 meta 标签提取
            meta_pattern = r'<meta property="og:title" content="([^"]*)"'
            title_match = re.search(meta_pattern, page_content)
            if title_match:
                print(f"文章标题: {title_match.group(1)}")

            print("未找到 biz 参数")
            return None

        except Exception as e:
            print(f"访问页面出错: {e}")
            return None
        finally:
            browser.close()

if __name__ == "__main__":
    # 上海静安公众号文章
    url = "https://mp.weixin.qq.com/s/ZKXjKURWMMStlij6OhUbiA"

    print("=" * 60)
    print("获取公众号 biz 参数")
    print("=" * 60)

    # 访问公众号资料页（如果有）
    # 公众号资料页通常格式：https://mp.weixin.qq.com/mp/profile_ext?action=home&__biz=...
    # 我们需要先找到 biz，然后才能访问资料页

    biz = get_biz_from_page(url)

    if biz:
        print(f"\n✅ 成功获取 biz 参数: {biz}")
        print(f"\n可以使用以下 API 添加公众号:")
        print(f'curl -X POST http://localhost:8002/api/v1/accounts \\')
        print(f'  -H "Content-Type: application/json" \\')
        print(f"  -H \"Authorization: Bearer YOUR_TOKEN\" \\")
        print(f'  -d \'{{"biz":"{biz}","name":"上海静安","is_active":true}}\'')
    else:
        print("\n❌ 未能获取 biz 参数")
        print("可能需要手动检查或使用其他方法")
