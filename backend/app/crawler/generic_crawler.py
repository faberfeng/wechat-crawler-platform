"""
通用网页爬虫
支持抓取任意 URL 的文章内容
"""

import os
import requests
from datetime import datetime
from sqlalchemy.orm import Session

from app.crawler.extractor import ArticleExtractor
from app.models.article import Article
from app.models.user import User
from app.core.config import settings


class GenericCrawler:
    """通用网页爬虫"""

    def __init__(self, db: Session):
        self.db = db
        self.session = requests.Session()
        self.session.headers.update({
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36'
        })

    def crawl_url(self, url: str, user_id: int = None) -> dict:
        """
        抓取指定 URL 的文章内容

        Args:
            url: 文章 URL
            user_id: 用户 ID

        Returns:
            dict: {
                'success': bool,
                'article': dict or None,
                'message': str
            }
        """
        try:
            # 检查 URL 是否已存在
            existing_article = self.db.query(Article).filter(Article.url == url).first()
            if existing_article:
                return {
                    'success': True,
                    'article': self._article_to_dict(existing_article),
                    'message': '文章已存在',
                    'exists': True
                }

            # 1. 获取网页内容
            print(f"[GenericCrawler] 正在抓取: {url}")
            response = self.session.get(url, timeout=30)
            response.raise_for_status()
            print(f"[GenericCrawler] 网页获取成功，大小: {len(response.content)} bytes")

            # 2. 提取文章内容
            extractor = ArticleExtractor(url, response.text)
            article_data = extractor.extract()
            print(f"[GenericCrawler] 文章标题: {article_data['title']}")
            print(f"[GenericCrawler] 作者: {article_data['author']}")

            # 3. 生成 Markdown 文件路径
            timestamp = datetime.now().strftime('%Y%m%d_%H%M%S')
            safe_title = self._sanitize_filename(article_data['title'][:100])
            markdown_filename = f"{timestamp}_{safe_title}.md"
            markdown_path = os.path.join(
                settings.MARKDOWN_STORAGE_PATH,
                markdown_filename
            )

            # 4. 保存 Markdown 文件
            os.makedirs(settings.MARKDOWN_STORAGE_PATH, exist_ok=True)
            with open(markdown_path, 'w', encoding='utf-8') as f:
                f.write(article_data['content'])
            print(f"[GenericCrawler] Markdown 文件已保存: {markdown_path}")

            # 5. 解析发布时间
            publish_time = None
            if article_data['publish_time']:
                try:
                    publish_time = datetime.fromisoformat(article_data['publish_time'].replace('Z', '+00:00'))
                except:
                    pass

            # 6. 保存到数据库
            article = Article(
                account_id=None,  # 通用抓取不关联公众号
                user_id=user_id or 1,
                title=article_data['title'],
                url=url,
                author=article_data['author'],
                cover_img=article_data['cover_img'],
                markdown_path=markdown_path,
                publish_time=publish_time,
                read_count=0,
                like_count=0
            )

            self.db.add(article)
            self.db.commit()
            self.db.refresh(article)
            print(f"[GenericCrawler] 文章已保存到数据库，ID: {article.id}")

            return {
                'success': True,
                'article': self._article_to_dict(article),
                'message': '文章抓取成功',
                'exists': False
            }

        except requests.exceptions.RequestException as e:
            print(f"[GenericCrawler] 请求错误: {e}")
            return {
                'success': False,
                'article': None,
                'message': f'请求失败: {str(e)}'
            }
        except Exception as e:
            print(f"[GenericCrawler] 错误: {e}")
            self.db.rollback()
            return {
                'success': False,
                'article': None,
                'message': f'抓取失败: {str(e)}'
            }

    def crawl_urls(self, urls: list, user_id: int = None) -> dict:
        """
        批量抓取多个 URL

        Args:
            urls: URL 列表
            user_id: 用户 ID

        Returns:
            dict: {
                'total': int,
                'success': int,
                'failed': int,
                'results': list
            }
        """
        results = []
        success_count = 0
        failed_count = 0

        for url in urls:
            result = self.crawl_url(url, user_id)
            results.append(result)

            if result['success']:
                success_count += 1
            else:
                failed_count += 1

        return {
            'total': len(urls),
            'success': success_count,
            'failed': failed_count,
            'results': results
        }

    def get_markdown_content(self, article_id: int) -> str:
        """
        获取文章的 Markdown 内容

        Args:
            article_id: 文章 ID

        Returns:
            str: Markdown 内容
        """
        article = self.db.query(Article).filter(Article.id == article_id).first()
        if not article or not article.markdown_path:
            return None

        try:
            with open(article.markdown_path, 'r', encoding='utf-8') as f:
                return f.read()
        except Exception as e:
            print(f"[GenericCrawler] 读取 Markdown 文件失败: {e}")
            return None

    def _sanitize_filename(self, filename: str) -> str:
        """清理文件名"""
        # 移除非法字符
        illegal_chars = ['/', '\\', ':', '*', '?', '"', '<', '>', '|']
        for char in illegal_chars:
            filename = filename.replace(char, '_')

        # 移除空格
        filename = filename.replace(' ', '_')

        # 限制长度
        return filename[:200]

    def _article_to_dict(self, article: Article) -> dict:
        """将文章对象转换为字典"""
        # 安全地转换datetime为ISO字符串
        def safe_isoformat(dt):
            if dt is None:
                return None
            if isinstance(dt, datetime):
                return dt.isoformat()
            return str(dt)

        return {
            'id': article.id,
            'title': article.title,
            'url': article.url,
            'author': article.author,
            'cover_img': article.cover_img,
            'publish_time': safe_isoformat(article.publish_time),
            'created_at': safe_isoformat(article.created_at),
            'read_count': article.read_count,
            'like_count': article.like_count,
            'has_markdown': article.markdown_path is not None
        }
