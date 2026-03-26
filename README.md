# WeChat Crawler Platform

> 微信公众号文章自动化抓取与管理平台

[![Python](https://img.shields.io/badge/Python-3.9%2B-blue)](https://www.python.org/)
[![FastAPI](https://img.shields.io/badge/FastAPI-0.100%2B-green)](https://fastapi.tiangolo.com/)
[![Vue 3](https://img.shields.io/badge/Vue-3.0%2B-42b883)](https://vuejs.org/)
[![License](https://img.shields.io/badge/License-MIT-yellow)](LICENSE)

## ✨ 功能特性

### 📱 核心功能
- **批量抓取**: 支持批量添加多个公众号，自动抓取最新文章
- **智能调度**: 内置定时任务，每 6 小时自动扫描并抓取新文章
- **增量更新**: 只抓取新发布的文章，避免重复
- **Markdown 导出**: 一键导出文章为 Markdown 格式
- **文章搜索**: 支持按公众号、关键词、时间筛选文章

### 🎨 界面特性
- **现代化 UI**: 基于 Vue 3 + Element Plus 的响应式界面
- **实时监控**: 抓取任务状态实时更新
- **数据可视化**: 直观的统计数据展示
- **Markdown 预览**: 支持文章内容在线预览
- **深色模式**: 支持深色/浅色主题切换
- **响应式设计**: 完美适配桌面端和移动端

### 🔐 安全特性
- **用户认证**: 基于 JWT 的用户认证系统
- **角色权限**: 支持管理员和普通用户角色
- **会话管理**: 安全的会话存储和验证
- **文件上传**: 支持安全的文件上传和管理

### 🛠️ 技术特性
- **浏览器模拟**: 基于 Playwright 的真实浏览器环境
- **并发抓取**: 支持多浏览器实例并发抓取
- **登录态保持**: 自动保存和恢复微信登录状态
- **错误重试**: 自动重试失败的抓取任务
- **日志记录**: 完整的日志系统，便于调试
- **环境适配**: 自动识别本地/公网环境并切换 API

---

## 🎬 功能展示

### 仪表盘
![仪表盘](screenshots/dashboard.png)

> 实时展示系统运行状态，包括公众号数量、文章总数、最新抓取进度等

### 公众号管理
![公众号管理](screenshots/accounts.png)

> 添加、编辑、删除公众号，查看公众号详细信息

### 文章列表
![文章列表](screenshots/articles.png)

> 浏览所有抓取的文章，支持搜索、筛选、导出

### 用户管理
![用户管理](screenshots/users.png)

> 管理系统用户，设置管理员权限

### 文件管理
![文件管理](screenshots/files.png)

> 上传和管理文件，支持文件分类和下载

---

## 📖 使用示例

### 示例 1: 添加公众号并抓取文章

### 示例 2: 查询文章列表

```javascript
// 获取所有文章
const articles = await fetch('https://wechat-crawler-api.loca.lt/api/v1/articles', {
  headers: {
    'Authorization': 'Bearer YOUR_TOKEN'
  }
}).then(res => res.json());

console.log(`共 ${articles.length} 篇文章`);

// 按关键词搜索
const searchResults = await fetch(
  'https://wechat-crawler-api.loca.lt/api/v1/articles?keyword=社区',
  {
    headers: {
      'Authorization': 'Bearer YOUR_TOKEN'
    }
  }
).then(res => res.json());
```

## 🏗️ 技术栈

### 后端
- **FastAPI**: 高性能 Python Web 框架
- **Playwright**: 浏览器自动化工具
- **SQLite**: 轻量级数据库
- **APScheduler**: 定时任务调度
- **SQLAlchemy**: ORM 框架
- **Pydantic**: 数据验证

### 前端
- **Vue 3**: 渐进式 JavaScript 框架
- **Vite**: 下一代前端构建工具
- **Element Plus**: Vue 3 UI 组件库
- **Axios**: HTTP 客户端

## 📦 快速开始

### 前置要求

- Python 3.9+
- Node.js 16+
- macOS / Linux / Windows

### 一键启动（推荐）

```bash
# 克隆项目
git clone git@github.com:faberfeng/wechat-crawler-platform.git
cd wechat-crawler-platform

# 一键启动
./start.sh
```

等待依赖安装完成后，访问 http://localhost:5173

### 分别启动后端和前端

#### 1. 启动后端

```bash
cd wechat-crawler-platform
./start-backend.sh
```

后端运行在 http://localhost:8000

#### 2. 启动前端（新终端）

```bash
cd wechat-crawler-platform
./start-frontend.sh
```

前端运行在 http://localhost:5173

## 📖 使用说明

### 1. 添加公众号

1. 访问 http://localhost:5173
2. 点击「公众号管理」
3. 点击「添加公众号」
4. 输入公众号任意文章链接
5. 点击「添加并开始抓取」

**示例链接格式**：
```
https://mp.weixin.qq.com/s/xxxxxx
```

### 2. 查看文章

1. 点击「文章列表」
2. 支持按公众号、关键词筛选
3. 点击文章标题查看详情
4. 支持导出 Markdown

### 3. 定时抓取

- 系统默认每 6 小时自动扫描所有活跃公众号
- 只抓取新发布的文章（增量更新）
- 可以在「任务管理」中手动触发立即抓取

### 4. 首次微信登录

首次运行时需要扫码登录微信：

```bash
cd backend
python3 login_wechat.py
```

扫码后在浏览器中会自动保存登录态，后续无需重复登录。

## 🗂️ 项目结构

```
wechat-crawler-platform/
├── backend/                    # 后端 (FastAPI)
│   ├── app/
│   │   ├── api/v1/            # API 路由
│   │   │   ├── accounts.py    # 公众号管理
│   │   │   ├── articles.py    # 文章管理
│   │   │   └── tasks.py       # 任务管理
│   │   ├── core/              # 核心配置
│   │   │   ├── config.py      # 配置管理
│   │   │   └── logger.py      # 日志配置
│   │   ├── db/                # 数据库
│   │   │   └── base.py        # 数据库连接
│   │   ├── models/            # SQLAlchemy 模型
│   │   │   ├── account.py     # 公众号模型
│   │   │   └── article.py     # 文章模型
│   │   ├── schemas/           # Pydantic 模型
│   │   ├── services/          # 业务逻辑
│   │   │   ├── crawler/       # 爬虫模块
│   │   │   │   ├── browser_pool.py    # 浏览器池
│   │   │   │   └── wechat_crawler.py  # 微信爬虫
│   │   │   └── scheduler.py   # 定时任务
│   │   └── main.py            # FastAPI 应用入口
│   ├── requirements.txt       # Python 依赖
│   └── data/
│       └── wechat.db          # SQLite 数据库
├── frontend/                   # 前端 (Vue 3)
│   ├── src/
│   │   ├── api/               # API 调用
│   │   │   ├── accounts.js    # 公众号 API
│   │   │   ├── articles.js    # 文章 API
│   │   │   ├── tasks.js       # 任务 API
│   │   │   └── index.js       # API 配置
│   │   ├── views/             # 页面组件
│   │   │   ├── Dashboard.vue  # 仪表盘
│   │   │   ├── AccountManage.vue  # 公众号管理
│   │   │   └── ArticleList.vue    # 文章列表
│   │   ├── components/        # 通用组件
│   │   │   └── MarkdownViewer.vue # Markdown 预览
│   │   ├── App.vue            # 主应用
│   │   └── main.js            # 入口文件
│   ├── package.json           # Node 依赖
│   └── vite.config.js         # Vite 配置
├── data/                       # 数据目录
│   ├── markdown/              # Markdown 文件
│   └── auth_sessions/         # 登录态
├── logs/                       # 日志文件
├── .env.example                # 环境变量示例
├── start.sh                    # 一键启动脚本
├── start-backend.sh            # 后端启动脚本
├── start-frontend.sh           # 前端启动脚本
└── README.md                   # 项目文档
```

## ⚙️ 配置说明

复制 `.env.example` 为 `.env` 并修改配置：

```env
# 数据库
DATABASE_URL=sqlite:///./backend/data/wechat.db

# API 配置
API_HOST=0.0.0.0
API_PORT=8000

# 浏览器配置
HEADLESS_BROWSER=true   # 是否无头模式（调试时改为 false）
MAX_BROWSERS=3          # 浏览器实例数量

# 调度配置
CRAWL_INTERVAL_HOURS=6  # 抓取间隔（小时）

# 日志配置
LOG_LEVEL=INFO          # 日志级别（DEBUG/INFO/WARNING/ERROR）
```

## 🔧 开发指南

### 安装 Playwright 浏览器

```bash
cd backend
python3 -m playwright install chromium
```

### 启动开发环境

**后端（开发模式）**：
```bash
cd backend
pip install -r requirements.txt
uvicorn app.main:app --reload
```

**前端（开发模式）**：
```bash
cd frontend
npm install
npm run dev
```

### API 文档

访问 http://localhost:8000/docs 查看 Swagger API 文档

## 🐛 常见问题

### Q1: 抓取失败？

**解决方案**：
- 检查网络是否正常
- 确认公众号链接是否正确
- 查看日志文件 `logs/app_*.log`
- 检查 Playwright 浏览器是否安装

### Q2: 浏览器启动失败？

**解决方案**：
```bash
cd backend
python3 -m playwright install chromium
```

### Q3: 前端无法连接后端？

**解决方案**：
- 确认后端已启动在 http://localhost:8000
- 检查防火墙设置
- 查看浏览器控制台错误信息

### Q4: 如何查看抓取进度？

**解决方案**：
- 查看日志文件 `logs/app_*.log`
- 访问 http://localhost:8000/docs 查看 API 文档
- 在前端「任务管理」页面查看任务状态

### Q5: 微信登录态过期怎么办？

**解决方案**：
```bash
cd backend
python3 login_wechat.py
```

重新扫码登录即可，系统会自动更新登录态。

## ⚠️ 注意事项

### 合规使用

1. 本项目仅供个人学习研究使用
2. 不要频繁抓取，避免对服务器造成压力
3. 抓取的文章仅供个人查看，禁止商用
4. 尊原作者版权，不要转载获利

### 数据安全

1. 文章保存在本地 SQLite 数据库
2. 不会上传任何数据到外部服务器
3. 登录态保存在本地，请注意保密

### 反爬策略

1. 已配置随机延迟，避免请求过快
2. 使用真实浏览器环境模拟
3. 建议设置合理的抓取间隔（默认 6 小时）

## 📄 License

[MIT License](LICENSE)

---

## 🐛 已知问题 & 待办事项

查看 [ISSUES_TODO.md](ISSUES_TODO.md) 了解当前已知的问题和已规划的待办事项。

欢迎提交 Issue 来报告新问题或提出功能建议！

---

## 🚀 部署 & CI/CD

项目已配置 GitHub Actions 自动化流程：

- **CI**: 自动运行测试和代码检查
- **Deploy**: 自动部署到服务器

详见：
- [.github/workflows/ci.yml](.github/workflows/ci.yml) - 持续集成配置
- [.github/workflows/deploy.yml](.github/workflows/deploy.yml) - 自动部署配置

---

## 🤝 贡献

欢迎提交 Issue 和 Pull Request！

## 📮 联系方式

- 作者: faberfeng
- GitHub: [@faberfeng](https://github.com/faberfeng)

## 🙏 致谢

- [FastAPI](https://fastapi.tiangolo.com/) - 现代化的 Python Web 框架
- [Playwright](https://playwright.dev/) - 现代化的浏览器自动化工具
- [Vue 3](https://vuejs.org/) - 渐进式 JavaScript 框架
- [Element Plus](https://element-plus.org/) - Vue 3 UI 组件库

---

**项目创建时间**: 2026-03-25

⭐ 如果这个项目对你有帮助，请给个 Star！
