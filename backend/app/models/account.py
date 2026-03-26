from sqlalchemy import Column, Integer, String, Boolean, DateTime, Text, ForeignKey
from sqlalchemy.ext.declarative import declarative_base
from datetime import datetime

Base = declarative_base()


class Account(Base):
    """公众号表"""
    __tablename__ = "accounts"

    id = Column(Integer, primary_key=True, autoincrement=True)
    biz = Column(String(100), unique=True, nullable=False, index=True)
    name = Column(String(200), nullable=False)
    avatar_url = Column(Text)
    is_active = Column(Boolean, default=True, nullable=False)
    last_crawl_time = Column(DateTime)
    article_count = Column(Integer, default=0)
    created_at = Column(DateTime, default=datetime.utcnow)
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)


class Article(Base):
    """文章表"""
    __tablename__ = "articles"

    id = Column(Integer, primary_key=True, autoincrement=True)
    account_id = Column(Integer, ForeignKey("accounts.id", ondelete="CASCADE"), nullable=False)
    title = Column(String(500), nullable=False, index=True)
    url = Column(String(500), unique=True, nullable=False)
    publish_time = Column(DateTime, nullable=False, index=True)
    markdown_path = Column(String(500))
    read_count = Column(Integer, default=0)
    like_count = Column(Integer, default=0)
    cover_img = Column(Text)
    author = Column(String(200))
    created_at = Column(DateTime, default=datetime.utcnow, index=True)


class CrawlTask(Base):
    """抓取任务表"""
    __tablename__ = "crawl_tasks"

    id = Column(Integer, primary_key=True, autoincrement=True)
    account_id = Column(Integer, ForeignKey("accounts.id"))
    status = Column(String(20), nullable=False)  # pending, running, success, failed
    article_count = Column(Integer, default=0)
    error_message = Column(Text)
    started_at = Column(DateTime)
    finished_at = Column(DateTime)
    created_at = Column(DateTime, default=datetime.utcnow, index=True)
