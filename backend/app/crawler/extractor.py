"""
文章内容提取器
支持从各种网页中提取文章内容
"""

import re
from bs4 import BeautifulSoup
from urllib.parse import urljoin, urlparse


class ArticleExtractor:
    """文章内容提取器"""

    def __init__(self, url, html_content):
        self.url = url
        self.html = html_content
        self.soup = BeautifulSoup(html_content, 'html.parser')

    def extract(self):
        """
        提取文章内容
        返回: {
            'title': str,
            'author': str,
            'content': str,
            'publish_time': str,
            'cover_img': str
        }
        """
        result = {
            'title': self.extract_title(),
            'author': self.extract_author(),
            'content': self.extract_content(),
            'publish_time': self.extract_publish_time(),
            'cover_img': self.extract_cover_img()
        }

        return result

    def extract_title(self):
        """提取文章标题"""
        # 方法 1: 从 meta ogs:title
        title_meta = self.soup.find('meta', property='og:title')
        if title_meta and title_meta.get('content'):
            return title_meta['content'].strip()

        # 方法 2: 从 meta name="title"
        title_meta = self.soup.find('meta', attrs={'name': 'title'})
        if title_meta and title_meta.get('content'):
            return title_meta['content'].strip()

        # 方法 3: 从 title 标签
        if self.soup.title and self.soup.title.string:
            return self.soup.title.string.strip()

        # 方法 4: 从微信文章标题
        wechat_title = self.soup.find('h1', class_='rich_media_title')
        if wechat_title:
            return wechat_title.get_text().strip()

        return "未命名文章"

    def extract_author(self):
        """提取作者信息"""
        # 方法 1: 从 meta author
        author_meta = self.soup.find('meta', attrs={'name': 'author'})
        if author_meta and author_meta.get('content'):
            return author_meta['content'].strip()

        # 方法 2: 从微信文章作者
        wechat_author = self.soup.find('a', class_='rich_media_meta_link')
        if wechat_author:
            return wechat_author.get_text().strip()

        # 方法 3: 从 meta article:author
        article_author = self.soup.find('meta', property='article:author')
        if article_author and article_author.get('content'):
            return article_author['content'].strip()

        return None

    def extract_content(self):
        """提取文章正文内容"""
        content = None

        # 方法 1: 微信公众号文章
        wechat_content = self.soup.find('div', class_='rich_media_content')
        if wechat_content:
            content = wechat_content

        # 方法 2: 知乎文章
        elif self.soup.find('div', class_='Post-RichTextContainer'):
            content = self.soup.find('div', class_='Post-RichTextContainer')

        # 方法 3: 掘金文章
        elif self.soup.find('div', class_='markdown-body'):
            content = self.soup.find('div', class_='markdown-body')

        # 方法 4: 使用Readability算法（简化版）
        if not content:
            # 查找包含最多文本的 div
            divs = self.soup.find_all('div')
            if divs:
                content = max(divs, key=lambda d: len(d.get_text()))

        if not content:
            return "无法提取文章内容"

        # 清理内容
        content_str = self._clean_content(content)
        return content_str

    def _clean_content(self, element):
        """清理和格式化内容"""
        # 移除不需要的标签
        for tag in element.find_all(['script', 'style', 'nav', 'footer', 'aside']):
            tag.decompose()

        # 移除类名和 id
        for tag in element.find_all(True):
            del tag['class']
            del tag['id']

        # 转换为 Markdown 格式
        markdown = self._html_to_markdown(element)
        return markdown

    def _html_to_markdown(self, element):
        """将 HTML 转换为 Markdown（简化版）"""
        result = []

        for child in element.children:
            if child.name is None:
                # 文本节点
                text = str(child).strip()
                if text:
                    result.append(text)
                    result.append('\n\n')

            elif child.name in ['h1', 'h2', 'h3', 'h4', 'h5', 'h6']:
                level = int(child.name[1])
                prefix = '#' * level + ' '
                result.append(prefix)
                result.append(child.get_text().strip())
                result.append('\n\n')

            elif child.name == 'p':
                result.append(child.get_text().strip())
                result.append('\n\n')

            elif child.name == 'strong' or child.name == 'b':
                result.append('**')
                result.append(child.get_text().strip())
                result.append('**')

            elif child.name == 'em' or child.name == 'i':
                result.append('*')
                result.append(child.get_text().strip())
                result.append('*')

            elif child.name == 'a':
                text = child.get_text().strip()
                href = child.get('href', '')
                if href:
                    result.append(f'[{text}]({href})')
                else:
                    result.append(text)

            elif child.name == 'img':
                src = child.get('src', '')
                alt = child.get('alt', '')
                if src:
                    # 转换为绝对 URL
                    src = urljoin(self.url, src)
                    result.append(f'![{alt}]({src})')
                    result.append('\n\n')

            elif child.name == 'br':
                result.append('\n')

            elif child.name in ['ul', 'ol']:
                for li in child.find_all('li', recursive=False):
                    text = li.get_text().strip()
                    if child.name == 'ul':
                        result.append(f'- {text}')
                    else:
                        result.append(f'1. {text}')
                    result.append('\n')
                result.append('\n')

            elif child.name == 'blockquote':
                text = child.get_text().strip()
                result.append('> ')
                result.append(text)
                result.append('\n\n')

            elif child.name == 'code':
                text = child.get_text().strip()
                result.append('`')
                result.append(text)
                result.append('`')

            elif child.name == 'pre':
                text = child.get_text().strip()
                result.append('```\n')
                result.append(text)
                result.append('\n```')
                result.append('\n\n')

            elif child.name == 'hr':
                result.append('---\n\n')

            # 递归处理其他标签
            elif child.name:
                result.append(self._html_to_markdown(child))

        return ''.join(result)

    def extract_publish_time(self):
        """提取发布时间"""
        # 方法 1: 从 meta article:published_time
        publish_meta = self.soup.find('meta', property='article:published_time')
        if publish_meta and publish_meta.get('content'):
            return publish_meta['content'].strip()

        # 方法 2: 从 meta pubdate
        pubdate_meta = self.soup.find('meta', attrs={'name': 'pubdate'})
        if pubdate_meta and pubdate_meta.get('content'):
            return pubdate_meta['content'].strip()

        # 方法 3: 从微信文章时间
        wechat_time = self.soup.find('em', id='publish_time')
        if wechat_time:
            return wechat_time.get_text().strip()

        # 方法 4: 从 datetime 属性
        time_tag = self.soup.find('time', attrs={'datetime': True})
        if time_tag and time_tag.get('datetime'):
            return time_tag['datetime']

        return None

    def extract_cover_img(self):
        """提取封面图片"""
        # 方法 1: 从 meta og:image
        img_meta = self.soup.find('meta', property='og:image')
        if img_meta and img_meta.get('content'):
            return img_meta['content'].strip()

        # 方法 2: 从微信文章封面
        wechat_cover = self.soup.find('img', id='js_cover')
        if wechat_cover and wechat_cover.get('data-src'):
            return wechat_cover['data-src']

        # 方法 3: 从第一张图片
        first_img = self.soup.find('img')
        if first_img and first_img.get('src'):
            return first_img['src']

        return None
