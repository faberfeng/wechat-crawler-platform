from pydantic import BaseModel, Field
from typing import Optional
from datetime import datetime


class ArticleBase(BaseModel):
    """文章基础模型"""
    account_id: int
    title: str
    url: str
    publish_time: datetime


class ArticleResponse(BaseModel):
    """文章响应"""
    id: int
    account_id: int
    account_name: Optional[str] = None  # 关联查询时填充
    title: str
    url: str
    publish_time: datetime
    markdown_path: Optional[str]
    read_count: int
    like_count: int
    cover_img: Optional[str]
    author: Optional[str]
    created_at: datetime

    class Config:
        from_attributes = True


class ArticleListResponse(BaseModel):
    """文章列表响应"""
    items: list[ArticleResponse]
    total: int
    page: int
    page_size: int


class ArticleDetailResponse(ArticleResponse):
    """文章详情响应（包含 Markdown）"""
    markdown_content: Optional[str] = None
