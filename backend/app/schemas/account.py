from pydantic import BaseModel, Field
from typing import Optional
from datetime import datetime


class AccountBase(BaseModel):
    """公众号基础模型"""
    name: str = Field(..., min_length=1, max_length=200)
    biz: Optional[str] = None  # 添加公众号时可以不提供，从 URL 提取
    avatar_url: Optional[str] = None
    is_active: bool = True


class AccountCreate(AccountBase):
    """创建公众号"""
    url: Optional[str] = Field(None, description="公众号任意文章链接（可选，如果提供了 biz 则不需要）")



class AccountUpdate(BaseModel):
    """更新公众号"""
    name: Optional[str] = None
    avatar_url: Optional[str] = None
    is_active: Optional[bool] = None


class AccountResponse(BaseModel):
    """公众号响应"""
    id: int
    biz: str
    name: str
    avatar_url: Optional[str]
    is_active: bool
    last_crawl_time: Optional[datetime]
    article_count: int
    created_at: datetime
    updated_at: datetime

    class Config:
        from_attributes = True
