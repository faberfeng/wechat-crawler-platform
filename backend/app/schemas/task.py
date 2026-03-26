from pydantic import BaseModel
from typing import Optional
from datetime import datetime


class TaskBase(BaseModel):
    """任务基础模型"""
    account_id: int
    status: str


class TaskResponse(BaseModel):
    """任务响应"""
    id: int
    account_id: int
    account_name: Optional[str] = None  # 关联查询时填充
    status: str
    article_count: int
    error_message: Optional[str]
    started_at: Optional[datetime]
    finished_at: Optional[datetime]
    created_at: datetime

    class Config:
        from_attributes = True


class TaskListResponse(BaseModel):
    """任务列表响应"""
    items: list[TaskResponse]
    total: int
    page: int
    page_size: int
