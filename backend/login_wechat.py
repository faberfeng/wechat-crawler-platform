#!/usr/bin/env python3
"""
微信扫码登录工具
用于保存微信登录态，供爬虫使用
"""
import asyncio
import sys
import argparse
from pathlib import Path

# 添加项目根目录到 Python 路径
sys.path.insert(0, str(Path(__file__).parent))


async def main():
    """主函数"""
    parser = argparse.ArgumentParser(description='微信扫码登录工具')
    parser.add_argument('--account', '-a', default='default', help='账号名称（默认: default）')
    args = parser.parse_args()

    account_name = args.account

    print(f"""
╔══════════════════════════════════════════════════════════════════╗
║                                                                  ║
║              微信公众号爬虫 - 扫码登录工具                        ║
║                                                                  ║
║  此工具将打开一个浏览器窗口，显示微信扫码登录页面。               ║
║  请使用微信扫描二维码登录，登录成功后系统将自动保存登录态。       ║
║                                                                  ║
║  账号名称: {account_name:<50} ║
║                                                                  ║
╚══════════════════════════════════════════════════════════════════╝

    """)

    from app.services.crawler.browser_pool import BrowserPool
    from app.core.logger import logger

    # 创建浏览器池实例
    browser_pool = BrowserPool()

    try:
        # 初始化 playwright
        from playwright.async_api import async_playwright
        browser_pool.playwright = await async_playwright().start()

        # 开始扫码登录
        session_file = await browser_pool.login_and_save_session(account_name)

        print("\n" + "=" * 80)
        print(f"✅ 登录态已保存: {session_file}")
        print("=" * 80)
        print("\n现在可以启动爬虫服务了，将自动使用这个登录态")
        print("\n🚀 启动爬虫服务:")
        print("  cd ~/Desktop/wechat-crawler-platform/backend")
        print("  python3 -m uvicorn app.main:app --host 127.0.0.1 --port 8000 --reload")

    except KeyboardInterrupt:
        print("\n\n⚠️ 用户中断")
    except Exception as e:
        print(f"\n❌ 发生错误: {e}", file=sys.stderr)
        import traceback
        traceback.print_exc()
    finally:
        await browser_pool.close_all()


if __name__ == "__main__":
    asyncio.run(main())
