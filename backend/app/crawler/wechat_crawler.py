"""
微信公众号文章爬虫
自动抓取指定公众号的文章
"""

import asyncio
import os
from datetime import datetime
from typing import List, Optional
from sqlalchemy.orm import Session
from pyppeteer import launch

from app.crawler.generic_crawler import GenericCrawler
from app.models.article import Article
from app.models.account import Account
from app.core.config import settings


class WeChatCrawler:
    """微信公众号爬虫"""

    def __init__(self, db: Session):
        self.db = db
        self.generic_crawler = GenericCrawler(db)
        self.base_url = "https://mp.weixin.qq.com"

    async def crawl_account_articles(self, account_id: int, limit: int = 10) -> dict:
        """
        抓取指定公众号的文章列表

        Args:
            account_id: 公众号 ID
            limit: 最大抓取数量

        Returns:
            dict: {
                'success': bool,
                'total': int,
                'crawled': int,
                'articles': list,
                'message': str
            }
        """
        try:
            # 获取公众号信息
            account = self.db.query(Account).filter(Account.id == account_id).first()
            if not account:
                return {
                    'success': False,
                    'total': 0,
                    'crawled': 0,
                    'articles': [],
                    'message': f'公众号 ID {account_id} 不存在'
                }

            if not account.is_active:
                return {
                    'success': False,
                    'total': 0,
                    'crawled': 0,
                    'articles': [],
                    'message': '公众号未启用'
                }

            print(f"[WeChatCrawler] 开始抓取公众号: {account.name} ({account.account_id})")

            # 启动浏览器
            browser = await launch(headless=True, args=['--no-sandbox'])
            page = await browser.newPage()

            # 构造搜索页面 URL
            search_url = f"{self.base_url}/cgi-bin/searchapp"
            await page.goto(search_url)

            # 输入公众号名称
            search_input = await page.querySelector('#__next > div > div.pages-home-index__container___2_7L8 > div.pages-home-index__content___3oFwE > div > div.pages-home-index__result-wrapper___2Ow1o > div.pages-home-index__search-wrapper___2J8i6 > div.pages-home-index__search-box___2iOeF > input')
            if search_input:
                await search_input.type(account.name)
                await asyncio.sleep(1)

                # 搜索
                search_button = await page.querySelector('.pages-home-index__search-btn___2JbJd')
                if search_button:
                    await search_button.click()
                    await asyncio.sleep(2)

            # 找到公众号并进入
            # 这里需要根据实际的微信搜一搜页面结构来调整
            # 由于反爬虫限制，这里提供基本框架

            # 获取文章列表
            # ...

            await browser.close()

            print(f"[WeChatCrawler] 抓取完成")

            # 返回结果
            # 这里先用通用爬虫抓取单个 URL 作为示例
            return {
                'success': True,
                'total': 0,
                'crawled': 0,
                'articles': [],
                'message': f'微信公众号抓取功能需要进一步完善反爬虫处理'
            }

        except Exception as e:
            print(f"[WeChatCrawler] 错误: {e}")
            return {
                'success': False,
                'total': 0,
                'crawled': 0,
                'articles': [],
                'message': f'抓取失败: {str(e)}'
            }

    async def crawl_wechat_article(self, article_url: str, account_id: int = None, user_id: int = None) -> dict:
        """
        抓取微信文章内容

        Args:
            article_url: 微信文章 URL
            account_id: 公众号 ID（可选）
            user_id: 用户 ID

        Returns:
            dict: {
                'success': bool,
                'article': dict or None,
                'message': str
            }
        """
        try:
            # 检查是否为微信文章 URL
            if 'mp.weixin.qq.com' not in article_url:
                return {
                    'success': False,
                    'article': None,
                    'message': '不是微信公众号文章 URL'
                }

            # 使用通用爬虫抓取
            result = self.generic_crawler.crawl_url(article_url, user_id)

            # 如果成功，更新账号信息
            if result['success'] and account_id:
                article = self.db.query(Article).filter(Article.url == article_url).first()
                if article:
                    article.account_id = account_id
                    self.db.commit()

            return result

        except Exception as e:
            print(f"[WeChatCrawler] 错误: {e}")
            return {
                'success': False,
                'article': None,
                'message': f'抓取失败: {str(e)}'
            }

    def crawl_wechat_articles_sync(self, article_urls: List[str], account_id: int = None, user_id: int = None) -> dict:
        """
        同步方式抓取多个微信文章

        Args:
            article_urls: 文章 URL 列表
            account_id: 公众号 ID（可选）
            user_id: 用户 ID

        Returns:
            dict: {
                'total': int,
                'success': int,
                'failed': int,
                'results': list
            }
        """
        # 启动事件循环
        loop = asyncio.new_event_loop()
        asyncio.set_event_loop(loop)

        try:
            results = []
            for url in article_urls:
                result = loop.run_until_complete(
                    self.crawl_wechat_article(url, account_id, user_id)
                )
                results.append(result)

            success_count = sum(1 for r in results if r['success'])
            failed_count = len(results) - success_count

            return {
                'total': len(article_urls),
                'success': success_count,
                'failed': failed_count,
                'results': results
            }
        finally:
            loop.close()
