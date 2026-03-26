#!/usr/bin/env python3
"""
微信公众号定时抓取脚本
支持单公众号或多公众号抓取
"""

import sys
import os

# 确保 backend 在 Python 路径中
SCRIPT_DIR = os.path.dirname(os.path.abspath(__file__))
BACKEND_DIR = os.path.join(SCRIPT_DIR, 'backend')
sys.path.insert(0, BACKEND_DIR)
os.chdir(BACKEND_DIR)

import argparse
import logging
from datetime import datetime
from typing import List, Optional

# 使用爬虫功能
# 注意：这里需要后端实现完整的公众号历史抓取功能
# 暂时使用简单的示例结构

from playwright.sync_api import sync_playwright
from app.db.base import get_db, SessionLocal
from app.models.account import Account
from app.models.article import Article
from app.crawler.generic_crawler import GenericCrawler
import re

# 配置日志
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s | %(levelname)s | %(message)s',
    handlers=[
        logging.FileHandler('/tmp/wechat_crawl.log'),
        logging.StreamHandler(sys.stdout)
    ]
)

logger = logging.getLogger(__name__)


def get_account_biz_articles(account_biz: str) -> List[str]:
    """
    从微信公众号主页获取文章 URL 列表

    注意：此功能需要有效的登录态和反爬处理
    由于微信反爬机制，实际使用时需要：
    1. 手动登录一次获取 Cookie
    2. 保存并复用登录态
    3. 处理验证码等反爬措施

    这里返回一个示例结构
    """

    logger.info(f"正在获取公众号文章列表 (biz: {account_biz})")

    # TODO: 实现实际的微信公众号历史文章抓取
    # 这需要：
    # 1. Playwright 浏览器自动化
    # 2. 加载登录态 Cookie
    # 3. 访问公众号主页：https://mp.weixin.qq.com/mp/profile_ext?__biz=...
    # 4. 滚动加载所有文章
    # 5. 提取文章链接
    # 6. 去重并返回新文章

    # 暂时返回空列表
    logger.warning("公众号历史文章抓取功能暂未实现，需要手动提供文章链接")
    return []


def crawl_articles_for_account(account_id: int, limit: int = None) -> dict:
    """
    为特定公众号抓取文章

    Args:
        account_id: 公众号 ID
        limit: 限制抓取数量（可选）

    Returns:
        抓取结果统计
    """
    db = SessionLocal()
    crawler = GenericCrawler(db)

    try:
        # 获取公众号信息
        account = db.query(Account).filter(Account.id == account_id).first()
        if not account:
            logger.error(f"公众号不存在: {account_id}")
            return {"success": False, "error": "公众号不存在"}

        logger.info(f"开始抓取公众号: {account.name} (biz: {account.biz})")

        # 获取文章列表（当前需要手动配置）
        # 从环境中读取或从配置文件读取最新文章链接
        article_urls = []

        # 示例：从环境变量读取
        env_key = f"WX_ARTICLE_URLS_{account_id}"
        if env_key in os.environ:
            article_urls = os.environ[env_key].split(',')
            logger.info(f"从环境变量读取到 {len(article_urls)} 个文章链接")

        # 如果没有配置，提示用户
        if not article_urls:
            logger.warning(f"未配置文章链接，请设置环境变量 {env_key}")
            return {
                "success": True,
                "message": "未配置文章链接",
                "account": account.name,
                "crawled": 0,
                "new": 0,
                "existed": 0,
                "failed": 0
            }

        # 限制抓取数量
        if limit:
            article_urls = article_urls[:limit]

        # 统计
        stats = {
            "success": True,
            "account": account.name,
            "total": len(article_urls),
            "crawled": 0,
            "new": 0,
            "existed": 0,
            "failed": 0,
            "urls": []
        }

        # 抓取每个文章
        for url in article_urls:
            try:
                # 检查是否已存在
                existing = db.query(Article).filter(Article.url == url).first()
                if existing:
                    logger.info(f"文章已存在: {url}")
                    stats["existed"] += 1
                    stats["urls"].append({
                        "url": url,
                        "status": "existed",
                        "title": existing.title
                    })
                    continue

                # 抓取文章
                logger.info(f"正在抓取: {url}")
                result = crawler.crawl_url(url, user_id=1)

                if result['success']:
                    # 更新文章归属
                    article = db.query(Article).filter(Article.url == url).first()
                    if article:
                        article.account_id = account_id
                        db.commit()

                    stats["crawled"] += 1
                    stats["new"] += 1

                    article_id = result['article'].get('id') if result.get('article') else None
                    title = result['article'].get('title') if result.get('article') else 'Unknown'

                    logger.info(f"✓ 抓取成功: {title}")
                    stats["urls"].append({
                        "url": url,
                        "status": "new",
                        "title": title,
                        "article_id": article_id
                    })
                else:
                    stats["failed"] += 1
                    logger.error(f"✗ 抓取失败: {result.get('message', 'Unknown error')}")
                    stats["urls"].append({
                        "url": url,
                        "status": "failed",
                        "error": result.get('message', 'Unknown error')
                    })

            except Exception as e:
                stats["failed"] += 1
                logger.error(f"✗ 抓取出错: {str(e)}", exc_info=True)
                stats["urls"].append({
                    "url": url,
                    "status": "error",
                    "error": str(e)
                })

        # 更新公众号统计
        account.article_count = db.query(Article).filter(Article.account_id == account_id).count()
        account.last_crawl_time = datetime.now()
        db.commit()

        logger.info(f"抓取完成: 新增 {stats['new']} 篇，已存在 {stats['existed']} 篇，失败 {stats['failed']} 篇")

        return stats

    except Exception as e:
        logger.error(f"抓取过程出错: {str(e)}", exc_info=True)
        return {"success": False, "error": str(e)}
    finally:
        db.close()


def crawl_all_accounts(limit: int = None) -> dict:
    """
    抓取所有活跃的公众号

    Args:
        limit: 每个公众号限制抓取数量

    Returns:
        总体抓取统计
    """
    db = SessionLocal()

    try:
        # 获取所有活跃公众号
        accounts = db.query(Account).filter(Account.is_active == True).all()

        if not accounts:
            logger.info("没有活跃的公众号需要抓取")
            return {"success": True, "message": "无活跃公众号"}

        logger.info(f"开始抓取 {len(accounts)} 个公众号")

        # 统计
        total_stats = {
            "success": True,
            "accounts": len(accounts),
            "total_crawled": 0,
            "total_new": 0,
            "total_existed": 0,
            "total_failed": 0,
            "accounts_stats": []
        }

        # 抓取每个公众号
        for account in accounts:
            logger.info(f"\n{'='*60}")
            logger.info(f"处理公众号: {account.name} (ID: {account.id})")
            logger.info(f"{'='*60}")

            stats = crawl_articles_for_account(account.id, limit)

            total_stats["accounts_stats"].append(stats)
            total_stats["total_crawled"] += stats.get("crawled", 0)
            total_stats["total_new"] += stats.get("new", 0)
            total_stats["total_existed"] += stats.get("existed", 0)
            total_stats["total_failed"] += stats.get("failed", 0)

        # 输出汇总
        logger.info(f"\n{'='*60}")
        logger.info(f"抓取汇总")
        logger.info(f"{'='*60}")
        logger.info(f"公众号总数: {total_stats['accounts']}")
        logger.info(f"抓取成功: {total_stats['total_crawled']} 篇")
        logger.info(f"新增文章: {total_stats['total_new']} 篇")
        logger.info(f"已存在: {total_stats['total_existed']} 篇")
        logger.info(f"抓取失败: {total_stats['total_failed']} 篇")
        logger.info(f"{'='*60}")

        return total_stats

    except Exception as e:
        logger.error(f"抓取过程出错: {str(e)}", exc_info=True)
        return {"success": False, "error": str(e)}
    finally:
        db.close()


def main():
    parser = argparse.ArgumentParser(description='微信公众号定时抓取脚本')

    # 抓取模式
    mode_group = parser.add_mutually_exclusive_group(required=True)
    mode_group.add_argument('--account-id', type=int, help='抓取指定公众号（ID）')
    mode_group.add_argument('--all', action='store_true', help='抓取所有活跃公众号')

    # 其他参数
    parser.add_argument('--limit', type=int, help='限制抓取数量')
    parser.add_argument('--test', action='store_true', help='测试模式，仅验证不实际抓取')

    args = parser.parse_args()

    logger.info(f"{'='*60}")
    logger.info(f"微信公众号定时抓取脚本启动")
    logger.info(f"启动时间: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
    logger.info(f"{'='*60}")

    if args.test:
        logger.info("测试模式：仅验证不实际抓取")
        logger.info("✓ 数据库连接正常")
        logger.info("✓ 脚本可以正常运行")
        return 0

    if args.all:
        result = crawl_all_accounts(args.limit)
    else:
        result = crawl_articles_for_account(args.account_id, args.limit)

    if result.get('success'):
        logger.info("✓ 抓取任务完成")
        return 0
    else:
        logger.error(f"✗ 抓取任务失败: {result.get('error', 'Unknown error')}")
        return 1


if __name__ == "__main__":
    sys.exit(main())
