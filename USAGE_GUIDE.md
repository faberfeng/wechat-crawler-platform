# 微信公众号抓取平台 - 使用指南

**版本：** 1.0.0
**更新时间：** 2026-03-26
**状态：** ✅ 可用

---

## 🚀 快速开始

### 前提条件
- Node.js v24.14.0+
- Python 3.9+
- 现代浏览器（Chrome/Safari/Firefox）

### 启动步骤

#### 1. 启动后端服务
```bash
cd /Users/fengweibo/Desktop/wechat-crawler-platform/backend
python3 -m uvicorn app.main:app --host 0.0.0.0 --port 8001 --reload
```

#### 2. 启动前端服务
```bash
cd /Users/fengweibo/Desktop/wechat-crawler-platform/frontend
npm run dev
```

#### 3. 访问应用
打开浏览器访问：http://localhost:5176

---

## 🔐 默认账户

### 管理员账户
- **用户名：** admin
- **密码：** admin123
- **权限：** 完整访问权限

### 测试账户
- **用户名：** testuser
- **密码：** Test123456
- **权限：** 标准用户权限

### 演示账户
- **用户名：** demo
- **密码：** Demo123456
- **权限：** 标准用户权限

---

## 📱 功能概览

### 已实现功能

#### 1. 用户认证 ✅
- 用户注册
- 用户登录
- JWT Token 认证
- 角色权限管理（admin/user）
- 密码哈希（pbkdf2_sha256）

#### 2. 公众号管理 ✅
- 添加公众号
- 查看公众号列表
- 启用/禁用公众号
- 手动触发抓取（框架已完成）

#### 3. 文章管理 ✅
- 查看文章列表
- 文章搜索和筛选
- 文章统计
- 文章详情查看（框架已完成）

#### 4. 文件管理 ⚠️
- 基础框架已完成
- 文件上传/下载功能需要完善

#### 5. 用户管理 ✅
- 查看用户列表（管理员专享）
- 更新用户角色（管理员专享）
- 删除用户（管理员专享）

---

## 🌐 访问地址

### 前端页面
- **主页：** http://localhost:5176/
- **登录：** http://localhost:5176/login
- **注册：** http://localhost:5176/register
- **仪表盘：** http://localhost:5176/dashboard
- **公众号管理：** http://localhost:5176/accounts
- **文章列表：** http://localhost:5176/articles
- **文件管理：** http://localhost:5176/files
- **用户管理：** http://localhost:5176/users (仅管理员)
- **个人信息：** http://localhost:5176/profile

### 后端 API
- **API Base URL：** http://localhost:8001/api/v1
- **Swagger 文档：** http://localhost:8001/docs
- **OpenAPI JSON：** http://localhost:8001/openapi.json

---

## 📚 API 端点

### 认证 API
```
POST /api/v1/auth/register  # 用户注册
POST /api/v1/auth/login     # 用户登录
POST /api/v1/auth/logout    # 用户登出
GET  /api/v1/auth/me       # 获取当前用户
```

### 公众号管理 API
```
GET    /api/v1/accounts              # 获取公众号列表
POST   /api/v1/accounts              # 创建公众号
GET    /api/v1/accounts/{id}         # 获取公众号详情
PUT    /api/v1/accounts/{id}         # 更新公众号
DELETE /api/v1/accounts/{id}         # 删除公众号
PUT    /api/v1/accounts/{id}/toggle  # 启用/禁用公众号
POST   /api/v1/accounts/{id}/crawl   # 触发抓取
```

### 文章管理 API
```
GET    /api/v1/articles              # 获取文章列表
GET    /api/v1/articles/{id}         # 获取文章详情
GET    /api/v1/articles/{id}/markdown # 获取文章 Markdown
GET    /api/v1/articles/stats/summary # 获取统计
```

### 文件管理 API
```
GET    /api/v1/files/              # 获取文件列表
POST   /api/v1/files/upload        # 上传文件
GET    /api/v1/files/{id}          # 获取文件详情
DELETE /api/v1/files/{id}          # 删除文件
GET    /api/v1/files/{id}/download  # 下载文件
GET    /api/v1/files/{id}/preview  # 预览文件
GET    /api/v1/files/stats/summary # 获取统计
```

### 用户管理 API
```
GET    /api/v1/users          # 获取用户列表（仅管理员）
GET    /api/v1/users/{id}     # 获取用户详情（仅管理员）
PUT    /api/v1/users/{id}     # 更新用户（仅管理员）
DELETE /api/v1/users/{id}     # 删除用户（仅管理员）
POST   /api/v1/auth/me/password # 修改密码
```

---

## 🧪 测试工具

### 1. 认证测试工具
- **文件：** `auth-test.html`
- **用途：** 测试登录和注册功能
- **使用：** 在浏览器中打开文件

### 2. API 测试工具
- **文件：** `test.html`
- **用途：** 测试所有 API 端点
- **使用：** 在浏览器中打开文件

### 3. 命令行测试脚本
```bash
# 测试认证功能
./test-auth.sh

# 测试注册功能
./test-register.sh

# 完整测试
./test-full.sh
```

### 4. 数据库初始化脚本
```bash
cd backend
python3 init_db.py
```

---

## 🔧 维护和故障排除

### 重启服务

#### 重启后端
```bash
pkill -f "uvicorn.*main:app"
cd backend
python3 -m uvicorn app.main:app --host 0.0.0.0 --port 8001 --reload
```

#### 重启前端
```bash
pkill -f "vite.*5176"
cd frontend
npm run dev
```

### 重置数据库
```bash
cd backend
rm data/wechat.db
python3 -m uvicorn app.main:app --host 0.0.0.0 --port 8001 --reload
python3 init_db.py
```

### 查看日志

#### 后端日志
```bash
tail -f logs/backend.log
# 或
tail -f /tmp/backend-new.log
```

#### 前端日志
```bash
tail -f /tmp/frontend.log
```

---

## 📋 项目结构

```
wechat-crawler-platform/
├── backend/                 # 后端服务
│   ├── app/
│   │   ├── api/            # API 路由
│   │   ├── core/           # 核心配置
│   │   ├── db/             # 数据库
│   │   ├── models/         # 数据模型
│   │   ├── schemas/        # Pydantic schemas
│   │   └── main.py         # FastAPI 主应用
│   ├── data/               # 数据文件
│   │   └── wechat.db       # SQLite 数据库
│   ├── init_db.py          # 数据库初始化脚本
│   └── requirements.txt    # Python 依赖
├── frontend/               # 前端服务
│   ├── src/
│   │   ├── api/           # API 封装
│   │   ├── assets/        # 静态资源
│   │   ├── components/    # Vue 组件
│   │   ├── stores/        # 状态管理
│   │   ├── styles/        # 样式文件
│   │   ├── views/         # 页面视图
│   │   ├── App.vue        # 根组件
│   │   └── main.js        # 入口文件
│   └── package.json       # Node 依赖
├── test-*.sh              # 测试脚本
├── *-report.md            # 测试报告
└── *.html                 # 测试工具
```

---

## 🎯 后续开发计划

### 高优先级
1. **完善文件管理功能**
   - 实现文件上传 UI
   - 实现文件下载功能
   - 添加文件预览

2. **实现微信爬虫**
   - 开发爬虫逻辑
   - 测试抓取功能
   - 优化数据存储

### 中优先级
3. **增强用户体验**
   - 添加加载状态
   - 优化错误提示
   - 改进响应式设计

4. **添加高级功能**
   - 批量操作
   - 数据导出
   - 搜索优化

### 低优先级
5. **性能优化**
   - 前端代码分割
   - API 响应缓存
   - 数据库索引优化

---

## 💡 常见问题

### Q: 忘记管理员密码怎么办？
**A:** 运行数据库初始化脚本：
```bash
cd backend
python3 init_db.py
```
这会重置 admin 密码为 admin123

### Q: 前端无法连接后端？
**A:** 检查以下事项：
1. 后端服务是否运行（端口 8001）
2. 前端 API 配置是否正确（`frontend/src/api/index.js`）
3. 浏览器控制台是否有错误信息

### Q: 如何添加新的 API 端点？
**A:** 在 `backend/app/api/v1/` 下创建新的路由文件，然后在 `backend/app/main.py` 中注册路由

### Q: 如何修改前端样式？
**A:** 在 `frontend/src/styles/` 下修改样式文件，或在 Vue 组件中使用 scoped 样式

---

## 📞 技术支持

### 联系方式
- **项目文档：** 查看项目根目录下的各种 *.md 报告文件
- **API 文档：** http://localhost:8001/docs
- **测试工具：** 使用提供的测试脚本和 HTML 工具

### 常用命令
```bash
# 查看后端状态
ps aux | grep uvicorn

# 查看前端状态
ps aux | grep vite

# 查看端口占用
lsof -i :8001
lsof -i :5176

# 测试 API 连接
curl http://localhost:8001/docs
```

---

## 📄 许可证

本项目仅供学习和研究使用。

---

**最后更新：** 2026-03-26
**版本：** 1.0.0
**状态：** ✅ 可用
