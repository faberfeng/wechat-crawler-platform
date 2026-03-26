from fastapi import APIRouter, Depends, HTTPException, Query
from sqlalchemy.orm import Session

from app.db.base import get_db
from app.models.account import CrawlTask, Account
from app.schemas.task import TaskResponse, TaskListResponse
from app.core.logger import logger

router = APIRouter(prefix="/tasks", tags=["任务管理"])


@router.get("", response_model=TaskListResponse, summary="获取任务列表")
async def get_tasks(
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
    for task in tasks:
        account = db.query(Account).get(task.account_id)
        if account:
            task.account_name = account.name

    return TaskListResponse(
        items=tasks,
        total=total,
        page=page,
        page_size=page_size
    )


@router.get("/{task_id}", response_model=TaskResponse, summary="获取任务详情")
async def get_task(
    task_id: int,
    db: Session = Depends(get_db)
):
    """获取指定任务的详细信息"""
    task = db.query(CrawlTask).get(task_id)
    if not task:
        raise HTTPException(status_code=404, detail="任务不存在")

    # 填充公众号名称
    account = db.query(Account).get(task.account_id)
    if account:
        task.account_name = account.name

    return task
