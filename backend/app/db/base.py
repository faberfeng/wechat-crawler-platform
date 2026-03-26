from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker, declarative_base
from pathlib import Path
from app.core.config import settings
from app.core.logger import logger

# 确保数据目录存在
data_dir = Path("data")
data_dir.mkdir(parents=True, exist_ok=True)

# 创建 SQLite 引擎
DATABASE_URL = settings.DATABASE_URL
engine = create_engine(
    DATABASE_URL,
    connect_args={"check_same_thread": False} if "sqlite" in DATABASE_URL else {},
    echo=False  # 设置为True可以看到SQL语句
)

# 创建会话工厂
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

# 基类
Base = declarative_base()


def get_db():
    """获取数据库会话"""
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


def init_db():
    """初始化数据库表"""
    from app.models.account import Base

    logger.info(f"正在初始化数据库: {DATABASE_URL}")
    Base.metadata.create_all(bind=engine)
    logger.info("数据库表创建成功")


def drop_db():
    """删除所有表（慎用！）"""
    from app.models.account import Base

    logger.warning("正在删除所有数据库表...")
    Base.metadata.drop_all(bind=engine)
    logger.info("数据库表已删除")
