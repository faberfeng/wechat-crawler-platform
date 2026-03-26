# WeChat Crawler Platform

微信公众号文章自动化抓取平台

## 技术栈

- **后端**: FastAPI + Playwright + SQLite
- **前端**: Vue 3 + Element Plus
- **数据库**: SQLite
- **调度**: APScheduler

## 功能特性

- 📱 批量抓取公众号文章
- 📅 定时自动更新
- 📄 Markdown 格式导出
- 🔍 文章搜索和过滤
- 📊 抓取任务监控

## 快速开始

### 后端启动

```bash
cd backend
pip install -r requirements.txt
uvicorn app.main:app --reload
```

### 前端启动

```bash
cd frontend
npm install
npm run dev
```

### 首次运行

1. 启动后端服务
2. 访问 http://localhost:8000/docs 查看 API 文档
3. 访问 http://localhost:5173 查看前端界面

## 项目结构

```
wechat-crawler-platform/
├── backend/          # FastAPI 后端
├── frontend/         # Vue 3 前端
├── data/            # 数据存储
│   ├── wechat.db    # SQLite 数据库
│   ├── markdown/    # Markdown 文件
│   └── auth_sessions/  # 登录态
└── logs/            # 日志文件
```

## 数据库初始化

首次运行时会自动创建 SQLite 数据库和表结构。

## 配置说明

复制 `.env.example` 为 `.env` 并修改配置：

```env
# 数据库
DATABASE_URL=sqlite:///./data/wechat.db

# API 配置
API_HOST=0.0.0.0
API_PORT=8000

# 抓取配置
CRAWL_INTERVAL_HOURS=6
MAX_BROWSERS=3
HEADLESS_BROWSER=true
```
