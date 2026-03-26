#!/usr/bin/env python3
"""
微信公众号历史文章抓取功能
使用浏览器自动化获取公众号所有历史文章链接
"""

import sys
import os
from datetime import datetime
from typing import List, Optional

# 确保 backend 在 Python 路径中
SCRIPT_DIR = os.path.dirname(os.path.abspath(__file__))
BACKEND_DIR = os.path.join(SCRIPT_DIR, 'backend')
sys.path.insert(0, BACKEND_DIR)
os.chdir(BACKEND_DIR)

import logging
from playwright.sync_api import sync_playwright

from app.db.base import SessionLocal
from app.models.account import Account

# 配置日志
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s | %(levelname)s | %(message)s',
    handlers=[
        logging.FileHandler('/tmp/wechat_history_crawl.log'),
        logging.StreamHandler(sys.stdout)
    ]
)

logger = logging.getLogger(__name__)


def get_public_account_articles(account_biz: str, account_name: str = "未知") -> List[dict]:
    """
    获取公众号历史文章列表

    Args:
        account_biz: 公众号的 biz 参数
        account_name: 公众号名称（用于日志）

    Returns:
        文章列表，每个元素包含 url, title, publish_time 等信息
    """

    logger.info(f"开始抓取公众号历史文章: {account_name} (biz: {account_biz})")

    articles = []

    with sync_playwright() as p:
        # 启动浏览器
        logger.info("正在启动浏览器...")
        browser = p.chromium.launch(headless=True)
        context = browser.new_context(
            user_agent='Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36'
        )

        page = context.new_page()

        try:
            # 构造公众号主页URL
            profile_url = f"https://mp.weixin.qq.com/mp/profile_ext?action=home&__biz={account_biz}&scene=124#wechat_redirect"

            logger.info(f"正在访问: {profile_url}")

            # 访问公众号主页
            page.goto(profile_url, timeout=30000, wait_until='networkidle')
            page.wait_for_timeout(3000)

            # 获取当前URL，可能被重定向
            current_url = page.url
            logger.info(f"当前页面URL: {current_url}")

            # 等待页面加载完成
            page.wait_for_timeout(2000)

            # 滚动加载所有文章
            logger.info("正在滚动加载所有文章...")

            last_height = 0
            scroll_count = 0
            max_scrolls = 50  # 最多滚动50次

            while scroll_count < max_scrolls:
                # 滚动到底部
                page.evaluate('window.scrollTo(0, document.body.scrollHeight)')
                page.wait_for_timeout(2000)

                # 获取当前滚动高度
                new_height = page.evaluate('document.body.scrollHeight')

                # 如果没有新内容，停止滚动
                if new_height == last_height:
                    logger.info(f"已加载全部文章，共滚动 {scroll_count} 次")
                    break

                last_height = new_height
                scroll_count += 1

                if scroll_count % 10 == 0:
                    logger.info(f"已滚动 {scroll_count} 次，当前高度: {new_height}")

            logger.info(f"滚动完成，开始提取文章信息...")

            # 提取文章信息
            # 微信公众号历史页面的文章在 appmsg 元素中
            article_elements = page.query_selector_all('.weui_media_bd')

            logger.info(f"找到 {len(article_elements)} 篇文章")

            for idx, element in enumerate(article_elements):
                try:
                    # 提取文章链接
                    link_element = element.query_selector('a')
                    if not link_element:
                        continue

                    url = link_element.get_attribute('href')

                    # 提取标题
                    title_element = element.query_selector('h4.weui_media_title')
                    title = title_element.text_content().strip() if title_element else f"文章 {idx + 1}"

                    # 提取发布时间
                    time_element = element.query_selector('p.weui_media_extra_info')
                    publish_time = time_element.text_content().strip() if time_element else ""

                    # 清理标题（移除多余空格）
                    title = ' '.join(title.split())

                    if url and title:
                        articles.append({
                            'url': url,
                            'title': title,
                            'publish_time': publish_time,
                            'idx': idx + 1
                        })

                except Exception as e:
                    logger.warning(f"提取第 {idx + 1} 篇文章时出错: {e}")
                    continue

            logger.info(f"成功提取 {len(articles)} 篇文章")

            # 打印前5篇文章作为示例
            if articles:
                logger.info("\n前5篇文章示例:")
                for i, article in enumerate(articles[:5], 1):
                    logger.info(f"  {i}. {article['title']}")
                    logger.info(f"     URL: {article['url'][:60]}...")
                    if article['publish_time']:
                        logger.info(f"     时间: {article['publish_time']}")
                    logger.info("")

        except Exception as e:
            logger.error(f"抓取过程出错: {e}", exc_info=True)
            return []

        finally:
            browser.close()

    return articles


def crawl_account_history(account_id: int, save_to_file: bool = True) -> dict:
    """
    为指定公众号抓取历史文章

    Args:
        account_id: 公众号 ID
        save_to_file: 是否保存到文件

    Returns:
        抓取结果统计
    """
    db = SessionLocal()

    try:
        # 获取公众号信息
        account = db.query(Account).filter(Account.id == account_id).first()
        if not account:
            logger.error(f"公众号不存在: {account_id}")
            return {"success": False, "error": "公众号不存在"}

        logger.info(f"正在抓取公众号历史: {account.name} (biz: {account.biz})")

        # 抓取历史文章
        articles = get_public_account_articles(account.biz, account.name)

        if not articles:
            logger.warning("未抓取到任何文章")
            return {
                "success": True,
                "account": account.name,
                "total": 0,
                "articles": []
            }

        # 保存到文件（可选）
        if save_to_file:
            output_file = f"config/article_urls_{account_id}_{datetime.now().strftime('%Y%m%d_%H%M%S')}.txt"

            with open(output_file, 'w', encoding='utf-8') as f:
                f.write(f"# {account.name} 公众号文章链接\n")
                f.write(f"# 抓取时间: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}\n")
                f.write(f"# 公众号 ID: {account_id}\n")
                f.write(f"# Biz: {account.biz}\n")
                f.write(f"# 共 {len(articles)} 篇文章\n\n")

                for article in articles:
                    f.write(f"{article['url']}\n")
                    # f.write(f"# {article['title']}\n")

            logger.info(f"文章链接已保存到: {output_file}")

            # 同时更新配置文件
            config_file = "config/article_urls.txt"
            with open(config_file, 'w', encoding='utf-8') as f:
                # 将所有 URL 合并成一行，用逗号分隔
                urls = [article['url'] for article in articles]
                f.write(f"{account_id}={','.join(urls)}\n")

            logger.info(f"配置文件已更新: {config_file}")

        return {
            "success": True,
            "account": account.name,
            "total": len(articles),
            "articles": articles,
            "config_updated": save_to_file
        }

    except Exception as e:
        logger.error(f"抓取历史文章出错: {e}", exc_info=True)
        return {"success": False, "error": str(e)}
    finally:
        db.close()


def main():
    import argparse

    parser = argparse.ArgumentParser(description='微信公众号历史文章抓取')

    parser.add_argument('--account-id', type=int, required=True,
                       help='公众号 ID')

    parser.add_argument('--no-save', action='store_true',
                       help='不保存到文件')

    args = parser.parse_args()

    logger.info("=" * 60)
    logger.info("微信公众号历史文章抓取")
    logger.info("=" * 60)

    result = crawl_account_history(args.account_id, save_to_file=not args.no_save)

    logger.info("=" * 60)
    logger.info("抓取完成")
    logger.info("=" * 60)

    if result.get('success'):
        logger.info(f"✓ 成功抓取 {result['total']} 篇文章")
        if result.get('config_updated'):
            logger.info("✓ 配置文件已更新")
            logger.info("  配置文件: config/article_urls.txt")
            logger.info("  下次定时任务将抓取这些文章")
        return 0
    else:
        logger.error(f"✗ 抓取失败: {result.get('error', 'Unknown error')}")
        return 1


if __name__ == "__main__":
    sys.exit(main())
