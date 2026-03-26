import asyncio
from datetime import datetime
from pathlib import Path
from typing import List, Dict, Optional
from urllib.parse import urlparse, parse_qs
import re
import html2text

from app.services.crawler.browser_pool import BrowserPool
from app.core.config import settings
from app.core.logger import logger


class WeChatCrawler:
    """微信文章爬虫"""

    def __init__(self, browser_pool: BrowserPool):
        self.browser_pool = browser_pool
        self.h2t = html2text.HTML2Text()
        self.h2t.ignore_links = False
        self.h2t.body_width = 0
        self.h2t.ignore_images = False
        self.h2t.unicode_snob = True

    @staticmethod
    def extract_biz_from_url(url: str) -> Optional[str]:
        """从 URL 提取 biz 参数"""
        try:
            # 从 URL 中提取 __biz 参数
            pattern = r'__biz=([^&]+)'
            match = re.search(pattern, url)
            if match:
                return match.group(1)
        except Exception as e:
            logger.error(f"提取 biz 失败: {e}")
        return None

    async def crawl_article_list(self, biz: str) -> List[Dict]:
        """
        抓取公众号历史文章列表

        Args:
            biz: 公众号 biz 标识

        Returns:
            文章列表: [{title, url, publish_time, cover_img, author}, ...]
        """
        context = await self.browser_pool.get_context()
        page = await context.new_page()

        articles = []

        try:
            # 构造历史消息页 URL
            history_url = (
                f"https://mp.weixin.qq.com/mp/profile_ext"
                f"?action=home&__biz={biz}"
                f"&scene=124&devicetype=android"
                f"&version=28000337&lang=zh_CN"
                f"&nettype=WIFI&a8scene=3&fontScale=100"
            )

            logger.info(f"正在访问历史消息页: {history_url[:100]}...")

            await page.goto(history_url, wait_until="domcontentloaded", timeout=30000)
            await page.wait_for_timeout(3000)

            max_pages = settings.MAX_PAGES_PER_CRAWL
            for page_num in range(max_pages):
                # 滚动到底部触发加载
                await page.evaluate("window.scrollTo(0, document.body.scrollHeight)")
                await page.wait_for_timeout(settings.SCROLL_DELAY_MS)

                # 提取当前页面的文章
                new_articles = await self._extract_articles_from_page(page)

                # 去重
                for art in new_articles:
                    if not any(a['url'] == art['url'] for a in articles):
                        articles.append(art)

                logger.debug(f"第 {page_num + 1} 页: 提取到 {len(new_articles)} 篇文章，累计 {len(articles)} 篇")

                # 检查是否还有更多
                has_more = await page.query_selector('.weui-btn_loading')
                no_more = await page.query_selector('text=没有更多')

                if not has_more or no_more:
                    logger.info("已加载所有文章")
                    break

                await page.wait_for_timeout(1000)

            logger.info(f"共提取到 {len(articles)} 篇文章")
            return articles

        except Exception as e:
            logger.error(f"抓取文章列表失败: {e}", exc_info=True)
            raise
        finally:
            await page.close()

    async def _extract_articles_from_page(self, page) -> List[Dict]:
        """从页面提取文章列表"""
        articles = []

        try:
            # 尝试多种选择器提取文章
            article_elements = await page.query_selector_all('[data-id]')
            logger.debug(f"找到 {len(article_elements)} 个文章元素")

            for elem in article_elements:
                try:
                    # 提取标题和链接
                    title_elem = await elem.query_selector('h3')
                    if not title_elem:
                        continue

                    url_elem = await elem.query_selector('a')
                    if not url_elem:
                        continue

                    title = await title_elem.text_content()
                    url = await url_elem.get_attribute('href')

                    if not title or not url:
                        continue

                    # 提取封面图
                    cover_img_elem = await elem.query_selector('img')
                    cover_img = await cover_img_elem.get_attribute('data-src') if cover_img_elem else None

                    # 提取发布时间
                    time_elem = await elem.query_selector('.js_time')
                    publish_time_str = await time_elem.get_attribute('data-time') if time_elem else None

                    publish_time = None
                    if publish_time_str:
                        try:
                            publish_time = datetime.fromtimestamp(int(publish_time_str))
                        except:
                            pass

                    # 提取公众号名称
                    author_elem = await elem.query_selector('.js_name')
                    author = await author_elem.text_content() if author_elem else None

                    articles.append({
                        'title': title.strip(),
                        'url': url.strip(),
                        'publish_time': publish_time or datetime.now(),
                        'cover_img': cover_img,
                        'author': author.strip() if author else None
                    })

                except Exception as e:
                    logger.debug(f"提取单篇文章失败: {e}")
                    continue

        except Exception as e:
            logger.error(f"_extract_articles_from_page 失败: {e}", exc_info=True)

        # 如果 DOM 提取失败，尝试拦截 XHR
        if not articles:
            articles = await self._extract_from_xhr(page)

        return articles

    async def _extract_from_xhr(self, page) -> List[Dict]:
        """通过拦截 XHR 请求提取文章"""
        logger.info("尝试通过 XHR 拦截提取文章")
        articles = []
        captured_data = []

        def handle_response(response):
            if "getmsg" in response.url:
                async def process():
                    try:
                        data = await response.json()
                        if "msgList" in data:
                            msg_list = data["msgList"]
                            for msg in msg_list:
                                if msg.get("type") == 49:  # 图文消息
                                    content = msg.get("content", {})
                                    articles.append({
                                        'title': content.get("title", ""),
                                        'url': f"https://mp.weixin.qq.com/s/{content.get('link', '')}",
                                        'publish_time': datetime.fromtimestamp(msg.get("comm_msg_info", {}).get("datetime", 0)),
                                        'cover_img': content.get("cover", ""),
                                        'author': msg.get("app_msg_ext_info", {}).get("digest", "")
                                    })
                    except:
                        pass
                asyncio.create_task(process())

        page.on("response", handle_response)

        # 滚动触发加载
        await page.evaluate("window.scrollTo(0, document.body.scrollHeight)")
        await page.wait_for_timeout(3000)

        return articles

    async def crawl_article_content(self, url: str) -> Dict:
        """
        抓取单篇文章内容

        Returns:
            文章内容: {title, author, publish_time, content_html, markdown, read_count, like_count, url}
        """
        context = await self.browser_pool.get_context()
        page = await context.new_page()

        try:
            logger.info(f"正在抓取文章: {url[:100]}...")

            await page.goto(url, wait_until="networkidle", timeout=30000)
            await page.wait_for_timeout(2000)

            # 提取标题
            title_elem = await page.query_selector('#activity-name')
            title = await title_elem.text_content() if title_elem else "未知标题"

            # 提取作者
            author_elem = await page.query_selector('#js_name')
            author = await author_elem.text_content() if author_elem else None

            # 提取发布时间
            publish_time = datetime.now()
            time_elem = await page.query_selector('#publish_time')
            if time_elem:
                time_str = await time_elem.get_attribute('data-time')
                if time_str:
                    try:
                        publish_time = datetime.fromtimestamp(int(time_str))
                    except:
                        pass

            # 提取正文 HTML
            content_div = await page.query_selector('.rich_media_content')
            content_html = await content_div.inner_html() if content_div else ""

            # 转为 Markdown
            markdown = self.h2t.handle(content_html)

            # 尝试获取阅读数（可能无法实时获取）
            read_count, like_count = await self._get_stats(page)

            logger.info(f"文章抓取成功: {title[:50]}...")

            return {
                'title': title.strip(),
                'author': author.strip() if author else None,
                'publish_time': publish_time,
                'content_html': content_html,
                'markdown': markdown,
                'read_count': read_count,
                'like_count': like_count,
                'url': url
            }

        except Exception as e:
            logger.error(f"抓取文章内容失败: {e}", exc_info=True)
            raise
        finally:
            await page.close()

    async def _get_stats(self, page) -> tuple[int, int]:
        """获取阅读数和点赞数"""
        read_count = 0
        like_count = 0

        try:
            # 阅读数
            read_elem = await page.query_selector('.read_num')
            if read_elem:
                read_text = await read_elem.text_content()
                read_count = int(re.search(r'\d+', read_text).group()) if read_text else 0

            # 点赞数
            like_elem = await page.query_selector('.like_num')
            if like_elem:
                like_text = await like_elem.text_content()
                like_count = int(re.search(r'\d+', like_text).group()) if like_text else 0
        except:
            pass

        return read_count, like_count

    def save_markdown(self, biz: str, publish_time: datetime, title: str, markdown: str) -> str:
        """保存 Markdown 文件"""
        markdown_dir = Path(settings.MARKDOWN_DIR) / biz
        markdown_dir.mkdir(parents=True, exist_ok=True)

        # 清理文件名
        safe_title = re.sub(r'[<>:"/\\|?*]', '_', title)[:100]
        filename = f"{publish_time.strftime('%Y%m%d_%H%M%S')}_{safe_title}.md"
        filepath = markdown_dir / filename

        with open(filepath, 'w', encoding='utf-8') as f:
            f.write(markdown)

        return str(filepath.relative_to(Path(settings.MARKDOWN_DIR).parent))
