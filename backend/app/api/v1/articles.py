from fastapi import APIRouter, Depends, HTTPException, Query
from sqlalchemy.orm import Session
from typing import Optional
from pathlib import Path

from app.db.base import get_db
from app.models.account import Account
from app.models.article import Article
from app.models.crawl_task import CrawlTask
from app.core.logger import logger

router = APIRouter(prefix="/articles", tags=["文章管理"])


@router.get("", summary="获取文章列表")
def get_articles(
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
        try:
            query = query.filter(Article.publish_time >= start_date)
        except:
            pass

    if end_date:
        try:
            query = query.filter(Article.publish_time <= end_date)
        except:
            pass

    # 总数
    total = query.count()

    # 分页
    articles = query.order_by(Article.publish_time.desc()).offset(
        (page - 1) * page_size
    ).limit(page_size).all()

    # 填充公众号名称
    result = []
    for article in articles:
        account = db.query(Account).filter(Account.id == article.account_id).first()
        article_dict = {
            "id": article.id,
            "account_id": article.account_id,
            "account_name": account.name if account else "",
            "title": article.title,
            "url": article.url,
            "publish_time": article.publish_time.isoformat() if article.publish_time else None,
            "read_count": article.read_count,
            "like_count": article.like_count,
            "cover_img": article.cover_img,
            "author": article.author,
            "created_at": article.created_at.isoformat() if article.created_at else None
        }
        result.append(article_dict)

    return {
        "items": result,
        "total": total,
        "page": page,
        "page_size": page_size
    }


@router.get("/{article_id}", summary="获取文章详情")
def get_article(
    article_id: int,
    db: Session = Depends(get_db)
):
    """获取文章详情"""
    article = db.query(Article).filter(Article.id == article_id).first()
    if not article:
        raise HTTPException(status_code=404, detail="文章不存在")

    # 填充公众号名称
    account = db.query(Account).filter(Account.id == article.account_id).first()

    article_dict = {
        "id": article.id,
        "account_id": article.account_id,
        "account_name": account.name if account else "",
        "title": article.title,
        "url": article.url,
        "publish_time": article.publish_time.isoformat() if article.publish_time else None,
        "read_count": article.read_count,
        "like_count": article.like_count,
        "cover_img": article.cover_img,
        "author": article.author,
        "created_at": article.created_at.isoformat() if article.created_at else None,
        "markdown_content": ""
    }

    # 读取 Markdown 内容
    if article.markdown_path:
        try:
            markdown_file = Path(article.markdown_path)
            if markdown_file.exists():
                with open(markdown_file, 'r', encoding='utf-8') as f:
                    article_dict["markdown_content"] = f.read()
        except Exception as e:
            logger.warning(f"读取 Markdown 文件失败: {e}")

    return article_dict


@router.get("/{article_id}/markdown", summary="获取原始 Markdown 内容")
def get_article_markdown(
    article_id: int,
    db: Session = Depends(get_db)
):
    """
    获取文章的原始 Markdown 内容（纯文本）

    如果 Markdown 文件不存在或读取失败，返回空字符串
    """
    article = db.query(Article).filter(Article.id == article_id).first()
    if not article:
        raise HTTPException(status_code=404, detail="文章不存在")

    if not article.markdown_path:
        return {"markdown_content": ""}

    try:
        markdown_file = Path(article.markdown_path)
        if markdown_file.exists():
            with open(markdown_file, 'r', encoding='utf-8') as f:
                markdown_content = f.read()
            return {"markdown_content": markdown_content}
    except Exception as e:
        logger.warning(f"读取 Markdown 文件失败: {e}")

    return {"markdown_content": ""}


@router.delete("/{article_id}", summary="删除文章")
def delete_article(
    article_id: int,
    db: Session = Depends(get_db)
):
    """删除指定文章"""
    article = db.query(Article).filter(Article.id == article_id).first()
    if not article:
        raise HTTPException(status_code=404, detail="文章不存在")

    article_title = article.title
    db.delete(article)
    db.commit()

    logger.info(f"删除文章: {article_title}")

    return {"message": f"文章已删除: {article_title}"}


@router.get("/stats/summary", summary="获取统计数据")
def get_stats(
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

    latest_crawl_time = latest_task.finished_at.isoformat() if latest_task and latest_task.finished_at else None

    return {
        "total_accounts": total_accounts,
        "active_accounts": active_accounts,
        "total_articles": total_articles,
        "latest_crawl_time": latest_crawl_time
    }
