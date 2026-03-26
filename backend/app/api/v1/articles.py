from fastapi import APIRouter, Depends, HTTPException, Query
from sqlalchemy.orm import Session
from typing import Optional
from pathlib import Path

from app.db.base import get_db
from app.models.account import Account, Article, CrawlTask
from app.schemas.article import ArticleResponse, ArticleListResponse, ArticleDetailResponse
from app.core.config import settings
from app.core.logger import logger

router = APIRouter(prefix="/articles", tags=["文章管理"])


@router.get("", response_model=ArticleListResponse, summary="获取文章列表")
async def get_articles(
    account_id: Optional[int] = Query(None, description="公众号 ID"),
    keyword: Optional[str] = Query(None, description="关键词搜索"),
    start_date: Optional[str] = Query(None, description="开始日期 (YYYY-MM-DD)"),
    end_date: Optional[str] = Query(None, description="结束日期 (YYYY-MM-DD)"),
    page: int = Query(1, ge=1, description="页码"),
    page_size: int = Query(20, ge=1, le=100, description="每页数量"),
    db: Session = Depends(get_db)
):
    """
    获取文章列表（支持分页、搜索、筛选）

    - **account_id**: 指定公众号 ID
    - **keyword**: 搜索标题
    - **start_date**: 开始日期
    - **end_date**: 结束日期
    - **page**: 页码（从1开始）
    - **page_size**: 每页数量（1-100）
    """
    query = db.query(Article)

    # 筛选条件
    if account_id:
        query = query.filter(Article.account_id == account_id)

    if keyword:
        query = query.filter(Article.title.contains(keyword))

    if start_date:
        query = query.filter(Article.publish_time >= start_date)

    if end_date:
        query = query.filter(Article.publish_time <= end_date)

    # 总数
    total = query.count()

    # 分页
    articles = query.order_by(Article.publish_time.desc()).offset(
        (page - 1) * page_size
    ).limit(page_size).all()

    # 填充公众号名称
    for article in articles:
        account = db.query(Account).get(article.account_id)
        if account:
            article.account_name = account.name

    return ArticleListResponse(
        items=articles,
        total=total,
        page=page,
        page_size=page_size
    )


@router.get("/{article_id}", response_model=ArticleDetailResponse, summary="获取文章详情")
async def get_article(
    article_id: int,
    db: Session = Depends(get_db)
):
    """获取文章详情（包含 Markdown 内容）"""
    article = db.query(Article).get(article_id)
    if not article:
        raise HTTPException(status_code=404, detail="文章不存在")

    # 填充公众号名称
    account = db.query(Account).get(article.account_id)
    if account:
        article.account_name = account.name

    # 读取 Markdown 内容
    markdown_content = None
    if article.markdown_path:
        try:
            markdown_file = Path(settings.MARKDOWN_DIR) / article.markdown_path.replace(f"{settings.MARKDOWN_DIR}/", "")
            if markdown_file.exists():
                with open(markdown_file, 'r', encoding='utf-8') as f:
                    markdown_content = f.read()
        except Exception as e:
            logger.warning(f"读取 Markdown 文件失败: {e}")

    return ArticleDetailResponse(
        **{
            **article.__dict__,
            'markdown_content': markdown_content
        }
    )


@router.get("/{article_id}/markdown", summary="获取原始 Markdown 内容")
async def get_article_markdown(
    article_id: int,
    db: Session = Depends(get_db)
):
    """
    获取文章的原始 Markdown 内容（纯文本）

    如果 Markdown 文件不存在或读取失败，返回空字符串
    """
    article = db.query(Article).get(article_id)
    if not article:
        raise HTTPException(status_code=404, detail="文章不存在")

    if not article.markdown_path:
        return {"markdown_content": ""}

    try:
        markdown_file = Path(settings.MARKDOWN_DIR) / article.markdown_path.replace(f"{settings.MARKDOWN_DIR}/", "")
        if markdown_file.exists():
            with open(markdown_file, 'r', encoding='utf-8') as f:
                markdown_content = f.read()
            return {"markdown_content": markdown_content}
    except Exception as e:
        logger.warning(f"读取 Markdown 文件失败: {e}")

    return {"markdown_content": ""}


@router.delete("/{article_id}", summary="删除文章")
async def delete_article(
    article_id: int,
    db: Session = Depends(get_db)
):
    """删除指定文章"""
    article = db.query(Article).get(article_id)
    if not article:
        raise HTTPException(status_code=404, detail="文章不存在")

    article_title = article.title
    db.delete(article)
    db.commit()

    logger.info(f"删除文章: {article_title}")

    return {"message": f"文章已删除: {article_title}"}


@router.get("/stats/summary", summary="获取统计数据")
async def get_stats(
    db: Session = Depends(get_db)
):
    """
    获取平台统计数据

    - 总公众号数
    - 活跃公众号数
    - 总文章数
    - 最近一次抓取时间
    """
    # 公众号统计
    total_accounts = db.query(Account).count()
    active_accounts = db.query(Account).filter(Account.is_active == True).count()

    # 文章统计
    total_articles = db.query(Article).count()

    # 最近一次抓取
    latest_task = db.query(CrawlTask).filter(
        CrawlTask.status == "success"
    ).order_by(CrawlTask.finished_at.desc()).first()

    latest_crawl_time = latest_task.finished_at if latest_task else None

    return {
        "total_accounts": total_accounts,
        "active_accounts": active_accounts,
        "total_articles": total_articles,
        "latest_crawl_time": latest_crawl_time
    }
