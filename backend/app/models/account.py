"""
公众号模型
"""
from datetime import datetime, timezone
from sqlalchemy import Column, Integer, String, Boolean, DateTime, Text
from sqlalchemy.orm import relationship

from app.db.base import Base


def get_now():
    """获取当前时间（带时区）"""
    return datetime.now(timezone.utc)


class Account(Base):
    """公众号表模型"""
    __tablename__ = "accounts"

    id = Column(Integer, primary_key=True, index=True, autoincrement=True)
    biz = Column(String(100), unique=True, nullable=False, index=True)
    name = Column(String(200), nullable=False)
    avatar_url = Column(Text, nullable=True)
    is_active = Column(Boolean, default=True, nullable=False)
    last_crawl_time = Column(DateTime(timezone=True), nullable=True)
    article_count = Column(Integer, default=0)
    created_at = Column(DateTime(timezone=True), default=get_now, nullable=False)
    updated_at = Column(DateTime(timezone=True), default=get_now, onupdate=get_now, nullable=False)

    # 关系
    articles = relationship("Article", back_populates="account")
