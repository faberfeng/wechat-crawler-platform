"""
爬虫模块
提供微信公众号文章抓取和通用网页文章抓取功能
"""

from .generic_crawler import GenericCrawler
from .extractor import ArticleExtractor

# WeChatCrawler 暂时注释，需要安装 pyppeteer
# from .wechat_crawler import WeChatCrawler

__all__ = ['GenericCrawler', 'ArticleExtractor']
