"""
文章模型
"""
from datetime import datetime
from sqlalchemy import Column, Integer, String, DateTime, Text, ForeignKey, text
from sqlalchemy.orm import relationship

from app.db.base import Base


class Article(Base):
    """文章表模型"""
    __tablename__ = "articles"

    id = Column(Integer, primary_key=True, index=True, autoincrement=True)
    account_id = Column(Integer, ForeignKey("accounts.id"), index=True, nullable=True)  # 通用抓取可以为null
    user_id = Column(Integer, ForeignKey("users.id"), index=True, nullable=False)  # 必须关联一个用户

    # 文章基本信息
    title = Column(String(500), nullable=False, index=True)
    url = Column(String(500), nullable=False, unique=True, index=True)
    author = Column(String(200), nullable=True)
    cover_img = Column(Text, nullable=True)  # 封面图片 URL

    # 统计数据
    read_count = Column(Integer, default=0)
    like_count = Column(Integer, default=0)

    # 时间信息
    publish_time = Column(DateTime, nullable=True)
    created_at = Column(DateTime, default=datetime.utcnow, nullable=False)

    # 文件存储路径
    markdown_path = Column(String(500), nullable=True)

    # 关系
    account = relationship("Account", back_populates="articles")
    user = relationship("User")
