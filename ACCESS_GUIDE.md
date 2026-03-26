# 微信公众号抓取平台 - 访问指南

**服务启动时间：** 2026-03-26 13:36

---

## 🌐 访问链接

### 前端应用
- **本地访问：** http://localhost:5173
- **登录页面：** http://localhost:5173/login
- **抓取页面：** http://localhost:5173/crawl
- **仪表盘：** http://localhost:5173/dashboard
- **文章列表：** http://localhost:5173/articles

### 后端 API
- **API 根地址：** http://localhost:8002/api/v1
- **API 文档：** http://localhost:8002/docs
- **健康检查：** http://localhost:8002/health

### 网络访问（局域网）
如需在局域网内访问，可使用以下地址：
- **前端：** http://[你的IP地址]:5173
- **后端 API：** http://[你的IP地址]:8002/api/v1

---

## 🔑 登录信息

### 管理员账户
- **用户名：** `admin`
- **密码：** `admin123`

### 测试账户
- **用户名：** `testuser`
- **密码：** `Test123456`

---

## 📱 所有可用页面

| 页面名称 | 路由 | 访问链接 |
|---------|------|---------|
| 首页 | / | http://localhost:5173/ |
| 登录 | /login | http://localhost:5173/login |
| 注册 | /register | http://localhost:5173/register |
| 仪表盘 | /dashboard | http://localhost:5173/dashboard |
| 公众号管理 | /accounts | http://localhost:5173/accounts |
| 文章列表 | /articles | http://localhost:5173/articles |
| **文章抓取** | /crawl | http://localhost:5173/crawl |
| 文件管理 | /files | http://localhost:5173/files |
| 个人信息 | /profile | http://localhost:5173/profile |

---

## 🚀 快速开始

### 1. 打开浏览器
访问：http://localhost:5173

### 2. 登录系统
- 用户名：`admin`
- 密码：`admin123`

### 3. 测试抓取功能
访问：http://localhost:5173/crawl

输入任意 URL 进行抓取，例如：
- https://www.python.org/
- https://docs.python.org/3/

---

## 🛠️ 服务状态

### 前端服务
- **状态：** ✅ 运行中
- **端口：** 5173
- **进程ID：** 38080
- **框架：** Vite + Vue 3

### 后端服务
- **状态：** ✅ 运行中
- **端口：** 8002
- **进程ID：** 37603
- **框架：** FastAPI + Uvicorn

### 数据库
- **路径：** backend/data/wechat.db
- **状态：** ✅ 正常
- **用户数：** 3
- **文章数：** 2

### 文件存储
- **Markdown 路径：** backend/data/markdown/
- **文件数：** 7
- **状态：** ✅ 正常

---

## 📊 API 端点

### 抓取相关
- `POST /api/v1/crawl/url` - 单个 URL 抓取
- `POST /api/v1/crawl/batch` - 批量 URL 抓取
- `POST /api/v1/crawl/wechat` - 微信文章抓取

### 其他
- `POST /api/v1/auth/login` - 用户登录
- `GET /api/v1/articles` - 文章列表
- `GET /api/v1/articles/{id}/markdown` - Markdown 内容

完整 API 文档：http://localhost:8002/docs

---

## 🎯 推荐测试流程

### 1. 登录
访问：http://localhost:5173/login

### 2. 查看仪表盘
登录后会自动跳转到仪表盘，查看统计数据

### 3. 测试抓取功能
访问：http://localhost:5173/crawl

选择"单个 URL"模式，输入：
```
https://www.python.org/
```

点击"开始抓取"，等待几秒后查看结果

### 4. 查看文章列表
访问：http://localhost:5173/articles

查看所有已抓取的文章

---

## 📝 常见问题

### Q: 前端无法连接后端？
A: 确保后端服务运行在 8002 端口，查看：
```bash
curl http://localhost:8002/health
```

### Q: 抓取失败？
A: 检查 URL 是否正确，如果是微信文章，需要完整的 mp.weixin.qq.com 链接

### Q: 如何查看 Markdown 文件？
A: 在文章列表中点击文章，或使用抓取结果中的"查看 Markdown"按钮

### Q: 如何重启服务？
**重启后端：**
```bash
cd /Users/fengweibo/Desktop/wechat-crawler-platform/backend
python3 -m uvicorn app.main:app --host 0.0.0.0 --port 8002 --reload
```

**重启前端：**
```bash
cd /Users/fengweibo/Desktop/wechat-crawler-platform/frontend
npm run dev
```

---

## 📱 移动端访问

### 外网访问（如需要）
可以使用 LocalTunnel 等工具暴露本地服务：

```bash
# 暴露前端
npx localtunnel --port 5173

# 暴露后端
npx localtunnel --port 8002
```

---

## 🎉 快速访问按钮

直接点击以下链接开始使用：

- **🏠 首页：** http://localhost:5173
- **📝 登录：** http://localhost:5173/login
- **📊 仪表盘：** http://localhost:5173/dashboard
- **🔍 文章列表：** http://localhost:5173/articles
- **🔗 文章抓取：** http://localhost:5173/crawl
- **📖 API 文档：** http://localhost:8002/docs

---

**文档生成时间：** 2026-03-26 13:36
**服务状态：** 🟢 全部正常运行
