from contextlib import asynccontextmanager
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from pathlib import Path

from app.core.config import settings
from app.core.logger import logger
from app.db.base import init_db
# from app.services.scheduler import task_scheduler  # 暂时注释，测试
from app.api.v1 import auth, users, files, accounts, articles, tasks, crawler  # 全部启用


# 确保必要目录存在
Path(settings.LOG_DIR).mkdir(parents=True, exist_ok=True)
Path(settings.MARKDOWN_DIR).mkdir(parents=True, exist_ok=True)
Path(settings.AUTH_SESSIONS_DIR).mkdir(parents=True, exist_ok=True)


@asynccontextmanager
async def lifespan(app: FastAPI):
    """应用生命周期管理"""
    # 启动时
    logger.info("=" * 50)
    logger.info("微信公众号抓取平台启动中...")
    logger.info("=" * 50)

    # 初始化数据库
    init_db()

    # 启动调度器
    # await task_scheduler.start()  # 暂时注释，测试

    logger.info("服务启动完成")
    logger.info(f"API 地址: http://{settings.API_HOST}:{settings.API_PORT}")
    logger.info(f"API 文档: http://{settings.API_HOST}:{settings.API_PORT}/docs")

    yield

    # 关闭时
    logger.info("正在关闭服务...")
    # await task_scheduler.stop()  # 暂时注释，测试
    logger.info("服务已关闭")


# 创建 FastAPI 应用
app = FastAPI(
    title="微信公众号抓取平台",
    description="自动化抓取、管理、搜索微信公众号文章",
    version="1.0.0",
    lifespan=lifespan
)

# 配置 CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=settings.CORS_ORIGINS.split(","),
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# 注册路由
app.include_router(auth.router, prefix="/api/v1/auth", tags=["认证"])
app.include_router(users.router, prefix="/api/v1/users", tags=["用户管理"])
app.include_router(accounts.router, prefix="/api/v1", tags=["公众号"])
app.include_router(articles.router, prefix="/api/v1", tags=["文章"])
app.include_router(tasks.router, prefix="/api/v1", tags=["任务"])
app.include_router(files.router, prefix="/api/v1/files", tags=["文件管理"])
app.include_router(crawler.router, prefix="/api/v1", tags=["抓取功能"])


@app.get("/", tags=["根路径"])
async def root():
    """根路径"""
    return {
        "message": "微信公众号抓取平台",
        "version": "1.0.0",
        "docs": "/docs",
        "api": "/api/v1"
    }


@app.get("/health", tags=["健康检查"])
async def health():
    """健康检查接口"""
    return {
        "status": "ok",
        "service": "wechat-crawler"
    }


if __name__ == "__main__":
    import uvicorn

    uvicorn.run(
        "app.main:app",
        host=settings.API_HOST,
        port=settings.API_PORT,
        reload=True
    )
