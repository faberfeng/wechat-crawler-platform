"""
抓取相关 API 路由
提供通用 URL 抓取和微信公众号抓取功能
"""

from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from pydantic import BaseModel, HttpUrl
from typing import List, Optional

from app.db.base import get_db
from app.crawler.generic_crawler import GenericCrawler
# WeChatCrawler 暂时注释，需要安装 pyppeteer
# from app.crawler.wechat_crawler import WeChatCrawler


router = APIRouter()


# Pydantic 模型
class CrawlURLRequest(BaseModel):
    """抓取单个 URL 请求"""
    url: str
    user_id: Optional[int] = None


class BatchCrawlURLsRequest(BaseModel):
    """批量抓取 URL 请求"""
    urls: List[str]
    user_id: Optional[int] = None


class WeChatArticleRequest(BaseModel):
    """微信文章抓取请求"""
    url: str
    account_id: Optional[int] = None
    user_id: Optional[int] = None


class WeChatAccountCrawlRequest(BaseModel):
    """微信公众号抓取请求"""
    account_id: int
    limit: Optional[int] = 10


# API 端点
@router.post("/crawl/url")
async def crawl_single_url(
    request: CrawlURLRequest,
    db: Session = Depends(get_db)
):
    """
    抓取单个 URL 的文章内容

    支持任意网页 URL，自动提取文章标题、作者、正文等内容，
    并保存为 Markdown 文件到文件系统。
    """
    try:
        crawler = GenericCrawler(db)
        result = crawler.crawl_url(request.url, request.user_id)

        if result['success']:
            return {
                "success": True,
                "message": result['message'],
                "article": result['article'],
                "exists": result.get('exists', False)
            }
        else:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail=result['message']
            )

    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"抓取失败: {str(e)}"
        )


@router.post("/crawl/batch")
async def crawl_urls_batch(
    request: BatchCrawlURLsRequest,
    db: Session = Depends(get_db)
):
    """
    批量抓取多个 URL 的文章内容
    """
    try:
        crawler = GenericCrawler(db)
        result = crawler.crawl_urls(request.urls, request.user_id)

        return {
            "success": True,
            "message": f"批量抓取完成",
            "summary": {
                "total": result['total'],
                "success": result['success'],
                "failed": result['failed']
            },
            "results": result['results']
        }

    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"批量抓取失败: {str(e)}"
        )


@router.post("/crawl/wechat")
async def crawl_wechat_article(
    request: WeChatArticleRequest,
    db: Session = Depends(get_db)
):
    """
    抓取微信公众号文章内容（使用通用爬虫）

    与通用抓取类似，但针对微信公众号文章进行了优化。
    可以选择关联到指定的公众号。
    """
    try:
        # 使用通用爬虫抓取微信文章
        crawler = GenericCrawler(db)
        result = crawler.crawl_url(request.url, request.user_id)

        # 如果成功且提供了 account_id，更新账号信息
        if result['success'] and request.account_id:
            from app.models.article import Article
            article = db.query(Article).filter(Article.url == request.url).first()
            if article:
                article.account_id = request.account_id
                db.commit()

        if result['success']:
            return {
                "success": True,
                "message": result['message'],
                "article": result['article']
            }
        else:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail=result['message']
            )

    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"微信文章抓取失败: {str(e)}"
        )


@router.post("/crawl/wechat/account")
async def crawl_wechat_account_articles(
    request: WeChatAccountCrawlRequest,
    db: Session = Depends(get_db)
):
    """
    自动抓取指定公众号的文章列表

    使用浏览器自动化技术，自动访问微信公众号页面，
    获取最新文章列表并逐个抓取。

    **注意：** 此功能需要安装 pyppeteer，暂时禁用。
    """
    raise HTTPException(
        status_code=status.HTTP_501_NOT_IMPLEMENTED,
        detail="公众号自动抓取功能需要安装 pyppeteer，暂时不可用。请使用单个文章抓取功能。"
    )


@router.get("/articles/{article_id}/markdown")
async def get_article_markdown(
    article_id: int,
    db: Session = Depends(get_db)
):
    """
    获取文章的 Markdown 内容
    """
    try:
        crawler = GenericCrawler(db)
        content = crawler.get_markdown_content(article_id)

        if content is not None:
            return {
                "success": True,
                "article_id": article_id,
                "content": content
            }
        else:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="文章不存在或未生成 Markdown 文件"
            )

    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"获取 Markdown 内容失败: {str(e)}"
        )
