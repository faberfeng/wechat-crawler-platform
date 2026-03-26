from pydantic_settings import BaseSettings
from typing import Optional


class Settings(BaseSettings):
    # API 配置
    API_HOST: str = "0.0.0.0"
    API_PORT: int = 8000

    # 数据库配置
    DATABASE_URL: str = "sqlite:///./data/wechat.db"

    # 调度配置
    CRAWL_INTERVAL_HOURS: int = 6
    CLEANUP_DAYS: int = 30

    # 浏览器配置
    HEADLESS_BROWSER: bool = True
    MAX_BROWSERS: int = 3
    SCROLL_DELAY_MS: int = 2000
    MAX_PAGES_PER_CRAWL: int = 10

    # 日志配置
    LOG_LEVEL: str = "INFO"
    LOG_DIR: str = "./logs"

    # 文件存储
    MARKDOWN_DIR: str = "./data/markdown"
    MARKDOWN_STORAGE_PATH: str = "./data/markdown"
    AUTH_SESSIONS_DIR: str = "./data/auth_sessions"

    # CORS
    CORS_ORIGINS: str = "http://localhost:5173,http://localhost:5174,https://wechat-crawler-fwb.loca.lt,https://wechat-crawler-api-fwb.loca.lt,https://wechat-fwb.loca.lt,https://fwb-wechat.loca.lt"

    # JWT 认证
    SECRET_KEY: str = "your-secret-key-change-this-in-production-please"
    ALGORITHM: str = "HS256"
    ACCESS_TOKEN_EXPIRE_MINUTES: int = 60 * 24 * 7  # 7 天

    class Config:
        env_file = ".env"


settings = Settings()
