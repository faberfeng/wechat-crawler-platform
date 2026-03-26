#!/usr/bin/env python3
"""
微信公众号历史文章抓取功能 v2
改进版本，支持更多页面结构和调试功能
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
from playwright.sync_api import sync_playwright, TimeoutError as PlaywrightTimeoutError

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
    获取公众号历史文章列表（改进版）

    Args:
        account_biz: 公众号的 biz 参数
        account_name: 公众号名称（用于日志）

    Returns:
        文章列表
    """

    logger.info(f"开始抓取公众号历史文章: {account_name} (biz: {account_biz})")

    articles = []
    page_source = None

    with sync_playwright() as p:
        # 启动浏览器（非无头模式，便于调试）
        headless = False  # 改为 True 用于生产环境
        logger.info(f"正在启动浏览器 (headless={headless})...")

        browser = p.chromium.launch(headless=headless, slow_mo=100)
        context = browser.new_context(
            user_agent='Mozilla/5.0 (iPhone; CPU iPhone OS 16_6 like Mac OS X) AppleWebKit/605.1.15 (KHTML, like Gecko) Version/16.6 Mobile/15E148 Safari/604.1',
            viewport={'width': 375, 'height': 667}
        )

        page = context.new_page()

        try:
            # 构造公众号主页URL（使用公众号历史页）
            profile_url = f"https://mp.weixin.qq.com/mp/profile_ext?action=home&__biz={account_biz}&scene=124"

            logger.info(f"正在访问: {profile_url}")

            # 访问公众号主页
            page.goto(profile_url, timeout=60000)

            # 等待页面加载
            logger.info("等待页面加载...")
            page.wait_for_timeout(5000)

            # 保存页面截图用于调试
            screenshot_path = f"/tmp/wechat_crawl_screenshot_{account_biz[:10]}.png"
            page.screenshot(path=screenshot_path)
            logger.info(f"页面截图已保存: {screenshot_path}")

            # 获取当前URL
            current_url = page.url
            logger.info(f"当前页面URL: {current_url}")

            # 获取页面标题
            page_title = page.title()
            logger.info(f"页面标题: {page_title}")

            # 保存页面源码
            page_source = page.content()
            source_file = f"/tmp/wechat_page_source_{account_biz[:10]}.html"
            with open(source_file, 'w', encoding='utf-8') as f:
                f.write(page_source)
            logger.info(f"页面源码已保存: {source_file}")

            # 尝试多种选择器，看能否找到文章
            selectors_to_try = [
                ('文章列表', '.weui_media_bd'),
                ('文章链接', 'a[href*="mp.weixin.qq.cn/s"]'),
                ('消息列表', '.weui_msg_card'),
                ('所有链接', 'a'),
                ('appmsg', '.appmsg'),
                ('appmsg_item', 'li.appmsg'),
            ]

            all_href = []

            for selector_name, selector in selectors_to_try:
                try:
                    elements = page.query_selector_all(selector)
                    logger.info(f"选择器 '{selector_name}' ({selector}): 找到 {len(elements)} 个元素")

                    if elements and len(elements) < 100:
                        for i, elem in enumerate(elements[:5]):
                            logger.info(f"  示例 {i+1}: {elem.text_content()[:100] if elem.text_content() else '(空文本)'}")
                            href = elem.get_attribute('href')
                            if href:
                                all_href.append(href)

                    if len(elements) > 0:
                        # 查找文章链接
                        for element in elements:
                            try:
                                # 查找链接
                                link_elem = element.query_selector('a')
                                if link_elem:
                                    url = link_elem.get_attribute('href')
                                    if url and 'mp.weixin.qq.com/s' in url:
                                        # 尝试提取标题
                                        title = element.text_content()[:200] if element.text_content() else ""
                                        title = ' '.join(title.split())

                                        if url not in [a['url'] for a in articles]:
                                            articles.append({
                                                'url': url,
                                                'title': title,
                                                'publish_time': '',
                                                'source_selector': selector_name
                                            })
                                            logger.debug(f"找到文章: {title[:50]}...")

                            except Exception as e:
                                continue

                        if articles:
                            logger.info(f"从 '{selector_name}' 成功提取 {len(articles)} 篇文章")
                            break

                except Exception as e:
                    logger.warning(f"尝试选择器 '{selector_name}' 时出错: {e}")
                    continue

            logger.info(f"总共提取到 {len(articles)} 篇文章")

            # 如果没有找到，打印所有链接
            if not articles and all_href:
                logger.info("未找到文章链接，但发现了其他链接:")
                for i, href in enumerate(set(all_href[:20])):  # 去重并显示前20个
                    logger.info(f"  {i+1}. {href[:100]}")

        except PlaywrightTimeoutError:
            logger.error("页面加载超时")
        except Exception as e:
            logger.error(f"抓取过程出错: {e}", exc_info=True)
            return []

        finally:
            # 等待一下，人工查看
            logger.info("等待 5 秒后关闭浏览器（便于人工查看）...")
            page.wait_for_timeout(5000)
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

        # 保存到文件
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
                    # f.write(f"# {article['title']}\n"

            logger.info(f"文章链接已保存到: {output_file}")

            # 更新配置文件（最多保存50篇，避免超过环境变量限制）
            max_urls = 50
            urls_to_save = [article['url'] for article in articles[:max_urls]]

            config_file = "config/article_urls.txt"
            with open(config_file, 'w', encoding='utf-8') as f:
                f.write(f"{account_id}={','.join(urls_to_save)}\n")

            logger.info(f"配置文件已更新: {config_file}")
            logger.info(f"保存了 {len(urls_to_save)} 个URL（最多 {max_urls} 个）")

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

    parser = argparse.ArgumentParser(description='微信公众号历史文章抓取 v2')

    parser.add_argument('--account-id', type=int, required=True,
                       help='公众号 ID')

    parser.add_argument('--no-save', action='store_true',
                       help='不保存到文件')

    parser.add_argument('--debug', action='store_true',
                       help='调试模式（显示浏览器窗口）')

    args = parser.parse_args()

    if args.debug:
        import importlib
        import sys
        sys.path.append(os.path.dirname(__file__))
        importlib.import_module('crawl_history')

        # 修改 headless 设置
        headless = False

    logger.info("=" * 60)
    logger.info("微信公众号历史文章抓取 v2")
    logger.info("=" * 60)

    result = crawl_account_history(args.account_id, save_to_file=not args.no_save)

    logger.info("=" * 60)
    logger.info("抓取完成")
    logger.info("=" * 60)

    if result.get('success'):
        logger.info(f"✓ 成功抓取 {result['total']} 篇文章")

        if result['total'] > 0:
            logger.info("\n前5篇文章:")
            for i, article in enumerate(result['articles'][:5], 1):
                logger.info(f"\n{i}. {article['title'][:60]}...")
                logger.info(f"   URL: {article['url'][:80]}...")
                if 'source_selector' in article:
                    logger.info(f"   来源: {article['source_selector']}")

        if result.get('config_updated'):
            logger.info("\n✓ 配置文件已更新")
            logger.info("  配置文件: config/article_urls.txt")
            logger.info("  下次定时任务将抓取这些文章")

        return 0
    else:
        logger.error(f"✗ 抓取失败: {result.get('error', 'Unknown error')}")
        return 1


if __name__ == "__main__":
    sys.exit(main())
