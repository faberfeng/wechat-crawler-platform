from fastapi import APIRouter, Depends, HTTPException, Query
from sqlalchemy.orm import Session
from datetime import datetime

from app.db.base import get_db
from app.models.account import Account
from app.models.crawl_task import CrawlTask
from app.core.logger import logger

router = APIRouter(prefix="/tasks", tags=["任务管理"])


@router.get("", summary="获取任务列表")
def get_tasks(
    account_id: int = Query(None, description="公众号 ID"),
    status: str = Query(None, description="任务状态"),
    page: int = Query(1, ge=1, description="页码"),
    page_size: int = Query(20, ge=1, le=100, description="每页数量"),
    db: Session = Depends(get_db)
):
    """
    获取抓取任务列表（支持分页、筛选）

    - **account_id**: 指定公众号 ID
    - **status**: 任务状态 (pending, running, success, failed)
    - **page**: 页码（从1开始）
    - **page_size**: 每页数量（1-100）
    """
    query = db.query(CrawlTask)

    # 筛选条件
    if account_id:
        query = query.filter(CrawlTask.account_id == account_id)

    if status:
        query = query.filter(CrawlTask.status == status)

    # 总数
    total = query.count()

    # 分页
    tasks = query.order_by(CrawlTask.created_at.desc()).offset(
        (page - 1) * page_size
    ).limit(page_size).all()

    # 填充公众号名称
    result = []
    for task in tasks:
        account = db.query(Account).filter(Account.id == task.account_id).first()
        task_dict = {
            "id": task.id,
            "account_id": task.account_id,
            "account_name": account.name if account else "",
            "status": task.status,
            "article_count": task.article_count,
            "error_message": task.error_message,
            "started_at": task.started_at.isoformat() if task.started_at else None,
            "finished_at": task.finished_at.isoformat() if task.finished_at else None,
            "created_at": task.created_at.isoformat() if task.created_at else None
        }
        result.append(task_dict)

    return {
        "items": result,
        "total": total,
        "page": page,
        "page_size": page_size
    }


@router.get("/{task_id}", summary="获取任务详情")
def get_task(
    task_id: int,
    db: Session = Depends(get_db)
):
    """获取指定任务的详细信息"""
    task = db.query(CrawlTask).filter(CrawlTask.id == task_id).first()
    if not task:
        raise HTTPException(status_code=404, detail="任务不存在")

    # 填充公众号名称
    account = db.query(Account).filter(Account.id == task.account_id).first()

    task_dict = {
        "id": task.id,
        "account_id": task.account_id,
        "account_name": account.name if account else "",
        "status": task.status,
        "article_count": task.article_count,
        "error_message": task.error_message,
        "started_at": task.started_at.isoformat() if task.started_at else None,
        "finished_at": task.finished_at.isoformat() if task.finished_at else None,
        "created_at": task.created_at.isoformat() if task.created_at else None
    }

    return task_dict


@router.post("/health-check", summary="执行健康检查")
def health_check(
    account_id: int = Query(..., description="公众号 ID"),
    db: Session = Depends(get_db)
):
    """
    执行公众号健康检查

    检查公众号是否可以访问
    """
    account = db.query(Account).filter(Account.id == account_id).first()
    if not account:
        raise HTTPException(status_code=404, detail="公众号不存在")

    # TODO: 实现实际的健康检查
    # 这里可以调用微信访问检查服务

    logger.info(f"健康检查: {account.name}")

    return {
        "account_id": account_id,
        "account_name": account.name,
        "status": "healthy",
        "checked_at": datetime.utcnow().isoformat()
    }
