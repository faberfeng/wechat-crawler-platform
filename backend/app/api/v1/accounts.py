from fastapi import APIRouter, Depends, HTTPException, Query
from sqlalchemy.orm import Session
from typing import List
from datetime import datetime

from app.db.base import get_db
from app.models.account import Account
from app.schemas.account import AccountCreate, AccountUpdate, AccountResponse
from app.services.crawler.wechat_crawler import WeChatCrawler
from app.services.scheduler import task_scheduler
from app.core.logger import logger

router = APIRouter(prefix="/accounts", tags=["公众号管理"])


@router.post("", response_model=AccountResponse, summary="添加公众号")
async def create_account(
    account: AccountCreate,
    db: Session = Depends(get_db)
):
    """
    添加公众号

    - **url**: 公众号任意文章链接
    - **name**: 公众号名称（可选，会自动从文章页提取）
    """
    # 从 URL 提取 biz
    biz = WeChatCrawler.extract_biz_from_url(account.url)
    if not biz:
        raise HTTPException(status_code=400, detail="无法从 URL 提取 biz 参数")

    # 检查是否已存在
    existing = db.query(Account).filter(Account.biz == biz).first()
    if existing:
        raise HTTPException(status_code=400, detail="该公众号已存在")

    # 创建公众号记录
    db_account = Account(
        biz=biz,
        name=account.name or "未命名公众号",
        avatar_url=account.avatar_url,
        is_active=account.is_active
    )

    db.add(db_account)
    db.commit()
    db.refresh(db_account)

    logger.info(f"添加公众号: {db_account.name} (biz={biz})")

    return db_account


@router.get("", response_model=List[AccountResponse], summary="获取公众号列表")
async def get_accounts(
    skip: int = Query(0, description="跳过数量"),
    limit: int = Query(100, description="返回数量"),
    active_only: bool = Query(False, description="仅返回活跃的公众号"),
    db: Session = Depends(get_db)
):
    """
    获取公众号列表

    - **skip**: 跳过前 N 条记录
    - **limit**: 返回记录数
    - **active_only**: 是否仅返回活跃的公众号
    """
    query = db.query(Account)

    if active_only:
        query = query.filter(Account.is_active == True)

    accounts = query.order_by(Account.created_at.desc()).offset(skip).limit(limit).all()

    return accounts


@router.get("/{account_id}", response_model=AccountResponse, summary="获取公众号详情")
async def get_account(
    account_id: int,
    db: Session = Depends(get_db)
):
    """获取指定公众号的详细信息"""
    account = db.query(Account).get(account_id)
    if not account:
        raise HTTPException(status_code=404, detail="公众号不存在")

    return account


@router.put("/{account_id}", response_model=AccountResponse, summary="更新公众号")
async def update_account(
    account_id: int,
    account_update: AccountUpdate,
    db: Session = Depends(get_db)
):
    """更新公众号信息"""
    account = db.query(Account).get(account_id)
    if not account:
        raise HTTPException(status_code=404, detail="公众号不存在")

    # 更新字段
    update_data = account_update.dict(exclude_unset=True)
    for field, value in update_data.items():
        setattr(account, field, value)

    account.updated_at = datetime.utcnow()

    db.commit()
    db.refresh(account)

    logger.info(f"更新公众号: {account.name}")

    return account


@router.delete("/{account_id}", summary="删除公众号")
async def delete_account(
    account_id: int,
    db: Session = Depends(get_db)
):
    """
    删除公众号

    注意：删除公众号会同时删除其所有关联的文章记录
    """
    account = db.query(Account).get(account_id)
    if not account:
        raise HTTPException(status_code=404, detail="公众号不存在")

    # 统计文章数
    article_count = db.query(Article).filter(Article.account_id == account_id).count()

    db.delete(account)
    db.commit()

    logger.info(f"删除公众号: {account.name} (删除 {article_count} 篇文章)")

    return {"message": f"公众号已删除，同时删除了 {article_count} 篇文章"}


@router.post("/{account_id}/crawl", summary="立即抓取公众号")
async def trigger_crawl(
    account_id: int,
    db: Session = Depends(get_db)
):
    """
    立即触发指定公众号的抓取任务

    该操作是异步的，会立即返回任务已触发
    """
    account = db.query(Account).get(account_id)
    if not account:
        raise HTTPException(status_code=404, detail="公众号不存在")

    if not account.is_active:
        raise HTTPException(status_code=400, detail="公众号未启用")

    # 异步触发抓取
    asyncio.create_task(task_scheduler.manual_crawl_account(account_id))

    logger.info(f"手动触发抓取: {account.name}")

    return {"message": f"抓取任务已触发: {account.name}"}


@router.put("/{account_id}/toggle", response_model=AccountResponse, summary="切换公众号启用状态")
async def toggle_account(
    account_id: int,
    db: Session = Depends(get_db)
):
    """切换公众号的启用/禁用状态"""
    account = db.query(Account).get(account_id)
    if not account:
        raise HTTPException(status_code=404, detail="公众号不存在")

    account.is_active = not account.is_active
    account.updated_at = datetime.utcnow()

    db.commit()
    db.refresh(account)

    status = "启用" if account.is_active else "禁用"
    logger.info(f"{status}公众号: {account.name}")

    return account
