import asyncio
from datetime import datetime
from typing import Optional
from apscheduler.schedulers.asyncio import AsyncIOScheduler
from sqlalchemy.orm import Session

from app.services.crawler.wechat_crawler import WeChatCrawler
from app.services.crawler.browser_pool import BrowserPool
from app.models.account import Account
from app.models.article import Article
from app.models.crawl_task import CrawlTask
from app.db.base import SessionLocal
from app.core.config import settings
from app.core.logger import logger


class TaskScheduler:
    """定时任务调度器"""

    def __init__(self):
        self.scheduler = AsyncIOScheduler()
        self.browser_pool: Optional[BrowserPool] = None
        self.crawler: Optional[WeChatCrawler] = None

    async def init(self):
        """初始化调度器"""
        logger.info("正在初始化调度器...")

        # 初始化浏览器池
        self.browser_pool = BrowserPool()
        await self.browser_pool.init()

        # 初始化爬虫
        self.crawler = WeChatCrawler(self.browser_pool)

        # 添加定时任务
        self.scheduler.add_job(
            self.scheduled_crawl_all_accounts,
            'interval',
            hours=settings.CRAWL_INTERVAL_HOURS,
            id='crawl_all_accounts',
            replace_existing=True
        )

        logger.info(f"定时任务已配置：每 {settings.CRAWL_INTERVAL_HOURS} 小时扫描一次")

    async def start(self):
        """启动调度器"""
        await self.init()

        # 启动时立即执行一次
        logger.info("启动时执行一次全局抓取...")
        await self.scheduled_crawl_all_accounts()

        # 启动调度器
        self.scheduler.start()
        logger.info("调度器已启动")

    async def stop(self):
        """停止调度器"""
        self.scheduler.shutdown()
        if self.browser_pool:
            await self.browser_pool.close_all()
        logger.info("调度器已停止")

    async def scheduled_crawl_all_accounts(self):
        """定时扫描所有活跃公众号并抓取"""
        db = SessionLocal()
        try:
            # 获取所有启用的公众号
            active_accounts = db.query(Account).filter(Account.is_active == True).all()

            if not active_accounts:
                logger.info("没有启用的公众号")
                return

            logger.info(f"开始扫描 {len(active_accounts)} 个活跃公众号...")

            for account in active_accounts:
                try:
                    await self.crawl_account(db, account.id)
                except Exception as e:
                    logger.error(f"抓取公众号 {account.name} 失败: {e}", exc_info=True)

        finally:
            db.close()

    async def manual_crawl_account(self, account_id: int):
        """手动触发抓取指定公众号"""
        db = SessionLocal()
        try:
            return await self.crawl_account(db, account_id, manual=True)
        finally:
            db.close()

    async def crawl_account(self, db: Session, account_id: int, manual: bool = False):
        """
        抓取单个公众号的最新文章

        Args:
            db: 数据库会话
            account_id: 公众号 ID
            manual: 是否为手动触发
        """
        account = db.query(Account).get(account_id)
        if not account:
            logger.error(f"公众号 {account_id} 不存在")
            raise ValueError("公众号不存在")

        # 创建任务记录
        task = CrawlTask(
            account_id=account_id,
            status="running",
            started_at=datetime.utcnow()
        )
        db.add(task)
        db.commit()
        db.refresh(task)

        logger.info(f"开始抓取公众号: {account.name} (biz={account.biz})")

        try:
            # 1. 抓取文章列表
            articles_list = await self.crawler.crawl_article_list(account.biz)

            if not articles_list:
                logger.warning(f"公众号 {account.name} 没有抓取到文章")
                task.status = "success"
                task.finished_at = datetime.utcnow()
                db.commit()
                return

            # 2. 获取该公众号已抓取的最新文章时间（增量抓取）
            latest_article = db.query(Article).filter(
                Article.account_id == account_id
            ).order_by(Article.publish_time.desc()).first()

            latest_time = latest_article.publish_time if latest_article else datetime.min

            # 3. 筛选新文章
            if not manual:
                # 自动模式下，只抓取比上次更新的新文章
                new_articles = [a for a in articles_list if a['publish_time'] > latest_time]
                if not new_articles:
                    logger.info(f"公众号 {account.name} 没有新文章")
                    task.status = "success"
                    task.finished_at = datetime.utcnow()
                    db.commit()
                    return
            else:
                # 手动模式下，抓取所有文章
                new_articles = articles_list

            logger.info(f"公众号 {account.name}: 发现 {len(new_articles)} 篇新文章待抓取")

            # 4. 逐个抓取内容
            for article_info in new_articles:
                try:
                    # 检查是否已存在
                    existing = db.query(Article).filter(
                        Article.url == article_info['url']
                    ).first()

                    if existing:
                        continue

                    # 抓取文章内容
                    content = await self.crawler.crawl_article_content(article_info['url'])

                    # 保存 Markdown 文件
                    try:
                        markdown_path = self.crawler.save_markdown(
                            account.biz,
                            content['publish_time'],
                            content['title'],
                            content['markdown']
                        )
                    except Exception as e:
                        logger.error(f"保存 Markdown 失败: {e}")
                        markdown_path = None

                    # 创建文章记录
                    article = Article(
                        account_id=account_id,
                        title=content['title'],
                        url=content['url'],
                        publish_time=content['publish_time'],
                        markdown_path=markdown_path,
                        read_count=content['read_count'],
                        like_count=content['like_count'],
                        author=content.get('author') or article_info.get('author'),
                        cover_img=article_info.get('cover_img')
                    )
                    db.add(article)

                    logger.info(f"保存文章: {content['title'][:50]}...")

                    # 延迟避免请求过快
                    await asyncio.sleep(1)

                except Exception as e:
                    logger.error(f"抓取单篇文章失败: {e}", exc_info=True)
                    continue

            # 5. 更新公众号信息
            account.last_crawl_time = datetime.utcnow()
            account.article_count = db.query(Article).filter(
                Article.account_id == account_id
            ).count()
            account.updated_at = datetime.utcnow()

            # 6. 更新任务状态
            task.status = "success"
            task.finished_at = datetime.utcnow()
            task.article_count = len(new_articles)

            db.commit()

            logger.info(f"公众号 {account.name} 抓取完成，共 {len(new_articles)} 篇文章")

        except Exception as e:
            logger.error(f"抓取公众号 {account.name} 失败: {e}", exc_info=True)
            task.status = "failed"
            task.error_message = str(e)
            task.finished_at = datetime.utcnow()
            db.commit()
            raise


# 全局调度器实例
task_scheduler = TaskScheduler()
