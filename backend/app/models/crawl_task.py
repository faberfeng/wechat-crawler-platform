"""
抓取任务模型
"""
from datetime import datetime
from sqlalchemy import Column, Integer, String, DateTime, Text
from sqlalchemy.orm import relationship

from app.db.base import Base


class CrawlTask(Base):
    """抓取任务表模型"""
    __tablename__ = "crawl_tasks"

    id = Column(Integer, primary_key=True, index=True, autoincrement=True)
    account_id = Column(Integer, nullable=True, index=True)
    status = Column(String(20), nullable=False, default='pending')  # pending, running, success, failed
    article_count = Column(Integer, default=0)
    error_message = Column(Text, nullable=True)
    started_at = Column(DateTime(timezone=True), nullable=True)
    finished_at = Column(DateTime(timezone=True), nullable=True)
    created_at = Column(DateTime(timezone=True), server_default='CURRENT_TIMESTAMP', index=True)
