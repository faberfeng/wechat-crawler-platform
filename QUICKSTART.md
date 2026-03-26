# 快速启动指南

## 🚀 快速开始

### 方式一：一键启动（推荐）

```bash
cd ~/Desktop/wechat-crawler-platform
./start.sh
```

等待依赖安装完成后，访问 http://localhost:5173

### 方式二：分别启动后端和前端

#### 1. 启动后端

打开终端（Terminal 1）：

```bash
cd ~/Desktop/wechat-crawler-platform
./start-backend.sh
```

等待看到 "服务启动完成"，后端运行在 http://localhost:8000

#### 2. 启动前端

打开新终端（Terminal 2）：

```bash
cd ~/Desktop/wechat-crawler-platform
./start-frontend.sh
```

前端运行在 http://localhost:5173

---

## 📖 使用说明

### 1. 添加公众号

1. 访问 http://localhost:5173
2. 点击"公众号管理"
3. 点击"添加公众号"
4. 输入公众号任意文章链接
5. 点击"添加并开始抓取"

**示例链接**：
```
https://mp.weixin.qq.com/s/xxxxxx
```

### 2. 查看文章

1. 点击"文章列表"
2. 支持按公众号、关键词筛选
3. 点击文章标题查看详情
4. 支持导出 Markdown

### 3. 定时抓取

- 系统每 6 小时自动扫描所有活跃公众号
- 只抓取新发布的文章（增量更新）
- 可以手动触发立即抓取

---

## 🔧 配置

编辑 `.env` 文件：

```env
# 浏览器配置
HEADLESS_BROWSER=true   # 是否无头模式（调试时改为 false）
MAX_BROWSERS=3          # 浏览器实例数量

# 调度配置
CRAWL_INTERVAL_HOURS=6  # 抓取间隔（小时）

# 日志配置
LOG_LEVEL=INFO          # 日志级别
```

---

## 📂 项目结构

```
wechat-crawler-platform/
├── backend/                    # 后端 (FastAPI)
│   ├── app/
│   │   ├── api/v1/            # API 路由
│   │   ├── core/              # 核心配置
│   │   ├── models/            # 数据库模型
│   │   ├── schemas/           # Pydantic 模型
│   │   └── services/          # 业务逻辑
│   │       ├── crawler/       # 爬虫（Playwright）
│   │       └── scheduler.py   # 定时任务
│   └── requirements.txt
├── frontend/                   # 前端 (Vue 3)
│   ├── src/
│   │   ├── api/               # API 调用
│   │   ├── views/             # 页面组件
│   │   └── components/        # 通用组件
│   └── package.json
├── data/                       # 数据目录
│   ├── wechat.db              # SQLite 数据库
│   ├── markdown/              # Markdown 文件
│   └── auth_sessions/         # 登录态
├── logs/                       # 日志文件
├── .env                        # 环境变量
├── start.sh                    # 一键启动脚本
├── start-backend.sh            # 后端启动脚本
└── start-frontend.sh           # 前端启动脚本
```

---

## 🐛 常见问题

### Q1: 抓取失败？
**A**: 检查以下几点：
- 网络是否正常
- 公众号链接是否正确
- 查看日志 `logs/app_*.log`

### Q2: 浏览器启动失败？
**A**: 安装 Playwright 浏览器：

```bash
cd backend
python3 -m playwright install chromium
```

### Q3: 前端无法连接后端？
**A**: 确认后端已启动在 http://localhost:8000

### Q4: 如何查看抓取进度？
**A**: 查看日志或访问 http://localhost:8000/docs 查看 API 文档

---

## 📦 依赖要求

- Python 3.9+
- Node.js 16+
- 系统需要联网（首次安装依赖）

---

## 🔒 注意事项

1. **合规使用**: 仅用于个人学习研究，不要频繁抓取
2. **数据安全**: 文章保存在本地数据库，不会上传到外部
3. **反爬策略**: 已配置随机延迟和浏览器模拟
4. **版权**: 抓取的文章仅供个人查看，禁止商用

---

## 📚 API 文档

访问 http://localhost:8000/docs 查看 Swagger API 文档

---

**项目创建时间**: 2026-03-25
**技术栈**: FastAPI + Vue 3 + SQLite + Playwright
