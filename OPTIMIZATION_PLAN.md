# 微信爬虫平台 - 综合优化计划

## 📋 项目概述

**当前项目位置：** `/Users/fengweibo/Desktop/wechat-crawler-platform`

**目标：** 将单用户爬虫改造为多用户 SaaS 平台，并优化 UI 和功能。

---

## 🎯 优化目标

### 1️⃣ 前端 UI 风格升级
- 采用现代化 SaaS 产品设计风格
- 改善配色方案和布局
- 优化交互体验
- 保持 Vue 3 + Element Plus 技术栈

### 2️⃣ 用户登录和权限系统（SaaS化）
- 多用户数据隔离
- JWT 认证
- 超级管理员功能
- 用户管理接口

### 3️⃣ 文章存储功能
- 按规则保存 MD 文件
- 文件夹按公众号分类
- 前端支持查看和下载

### 4️⃣ 自测爬虫功能
- 验证爬虫逻辑
- 测试完整流程
- 输出测试报告

---

## 📊 当前项目分析

### 技术栈
- **后端：** FastAPI + Playwright + SQLite
- **前端：** Vue 3 + Vite + Element Plus
- **数据库：** SQLite
- **认证：** 无（单用户）

### 数据库表结构
```sql
-- 当前表
accounts        -- 公众号列表
articles        -- 文章列表
tasks           -- 任务列表
```

### 功能模块
1. 公众号管理
2. 文章列表
3. 定时抓取
4. Playwright 浏览器池

---

## 🚀 详细实施方案

## 任务 1：前端 UI 风格升级

### 1.1 设计风格参考

**参考产品：**
- Linear (linear.app) - 极简、高效
- Notion (notion.so) - 清晰、专业
- Vercel (vercel.com) - 现代、科技感

**设计原则：**
- ✅ 简洁干净的界面
- ✅ 柔和的配色（蓝灰、白色主色调）
- ✅ 清晰的信息层级
- ✅ 流畅的交互动画
- ✅ 响应式设计

### 1.2 配色方案

```css
/* 主色调 */
--primary-color: #3B82F6;       /* 蓝色 */
--primary-light: #60A5FA;       /* 浅蓝 */
--primary-dark: #2563EB;        /* 深蓝 */

/* 中性色 */
--bg-primary: #FFFFFF;          /* 背景白 */
--bg-secondary: #F8FAFC;        /* 浅灰背景 */
--bg-tertiary: #F1F5F9;         /* 更浅灰 */
--border-color: #E2E8F0;        /* 边框色 */

/* 文字颜色 */
--text-primary: #1E293B;        /* 主文字 */
--text-secondary: #64748B;      /* 次要文字 */
--text-tertiary: #94A3B8;       /* 辅助文字 */

/* 功能色 */
--success: #10B981;             /* 成功绿 */
--warning: #F59E0B;             /* 警告黄 */
--danger: #EF4444;              /* 危险红 */
```

### 1.3 需要修改的文件

#### 1. 添加全局样式变量
```javascript
// frontend/src/styles/variables.scss
:root {
  --primary-color: #3B82F6;
  // ... 其他变量
}
```

#### 2. 更新 Element Plus 主题
```javascript
// frontend/src/styles/element-theme.scss
@use "element-plus/theme-chalk/src/index.scss" as *;

$--color-primary: var(--primary-color);
// ... 其他主题变量
```

#### 3. 优化各页面样式
- `Dashboard.vue` - 概览页优化
- `AccountManage.vue` - 公众号管理页
- `ArticleList.vue` - 文章列表页

### 1.4 布局改进

**改进点：**
1. 添加侧边导航栏
2. 顶部导航栏优化
3. 添加页面加载状态
4. 添加空状态提示
5. 添加骨架屏

---

## 任务 2：用户登录和权限系统

### 2.1 数据库设计

#### 新增表：users
```sql
CREATE TABLE users (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    username VARCHAR(50) UNIQUE NOT NULL,
    email VARCHAR(100) UNIQUE NOT NULL,
    password_hash VARCHAR(255) NOT NULL,
    role VARCHAR(20) DEFAULT 'user',  -- 'admin' or 'user'
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);
```

#### 修改表：accounts
```sql
ALTER TABLE accounts ADD COLUMN user_id INTEGER NOT NULL DEFAULT 1;
CREATE INDEX idx_accounts_user_id ON accounts(user_id);
```

#### 修改表：articles
```sql
ALTER TABLE articles ADD COLUMN user_id INTEGER NOT NULL DEFAULT 1;
CREATE INDEX idx_articles_user_id ON articles(user_id);
```

#### 修改表：tasks
```sql
ALTER TABLE tasks ADD COLUMN user_id INTEGER NOT NULL DEFAULT 1;
CREATE INDEX idx_tasks_user_id ON tasks(user_id);
```

### 2.2 后端实现

#### 文件结构
```
backend/
├── app/
│   ├── api/
│   │   ├── v1/
│   │   │   ├── auth.py          # 认证接口（新建）
│   │   │   └── users.py         # 用户管理接口（新建）
│   ├── core/
│   │   ├── security.py          # 安全相关（新建）
│   │   └── dependencies.py      # 依赖注入（新建）
│   └── models/
│       └── user.py              # 用户模型（新建）
```

#### 认证接口设计

**注册接口：**
```python
POST /api/v1/auth/register
{
    "username": "string",
    "email": "string",
    "password": "string"
}
Response: 201 Created
{
    "id": 1,
    "username": "string",
    "email": "string",
    "role": "user"
}
```

**登录接口：**
```python
POST /api/v1/auth/login
{
    "email": "string",
    "password": "string"
}
Response: 200 OK
{
    "access_token": "string",
    "token_type": "bearer",
    "user": { ... }
}
```

**获取当前用户：**
```python
GET /api/v1/auth/me
Headers: Authorization: Bearer {token}
Response: 200 OK
{
    "id": 1,
    "username": "string",
    "email": "string",
    "role": "user"
}
```

#### 用户管理接口（仅管理员）

**获取用户列表：**
```python
GET /api/v1/users
Headers: Authorization: Bearer {admin_token}
Response: 200 OK
{
    "users": [...],
    "total": 10
}
```

**创建用户：**
```python
POST /api/v1/users
{
    "username": "string",
    "email": "string",
    "password": "string",
    "role": "user"
}
```

**删除用户：**
```python
DELETE /api/v1/users/{user_id}
```

**修改用户角色：**
```python
PATCH /api/v1/users/{user_id}
{
    "role": "admin"
}
```

#### 依赖注入（认证中间件）

```python
# app/core/dependencies.py
from fastapi import Depends, HTTPException, status
from fastapi.security import HTTPBearer, HTTPAuthorizationCredentials
from jose import JWTError, jwt

security = HTTPBearer()

async def get_current_user(
    credentials: HTTPAuthorizationCredentials = Depends(security)
):
    """获取当前登录用户"""
    token = credentials.credentials
    try:
        payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
        user_id = payload.get("sub")
        if user_id is None:
            raise HTTPException(status_code=401, detail="Invalid token")
    except JWTError:
        raise HTTPException(status_code=401, detail="Invalid token")

    # 从数据库查询用户
    user = await get_user_by_id(user_id)
    if user is None:
        raise HTTPException(status_code=401, detail="User not found")

    return user

async def get_admin_user(current_user = Depends(get_current_user)):
    """获取管理员用户"""
    if current_user.role != "admin":
        raise HTTPException(status_code=403, detail="Not authorized")
    return current_user
```

#### 修改现有接口（添加数据隔离）

```python
# app/api/v1/accounts.py
from app.core.dependencies import get_current_user

@router.get("/")
async def get_accounts(
    current_user = Depends(get_current_user)
):
    """获取当前用户的公众号列表"""
    # 只查询当前用户的数据
    return await get_accounts_by_user_id(current_user.id)
```

### 2.3 前端实现

#### 文件结构
```
frontend/src/
├── views/
│   ├── Login.vue          # 登录页（新建）
│   ├── Register.vue       # 注册页（新建）
│   └── UserManage.vue     # 用户管理页（仅管理员，新建）
├── stores/
│   └── auth.ts            # 认证状态管理（新建）
├── router/
│   └── index.js           # 路由配置（修改）
└── api/
    └── auth.js            # 认证 API（新建）
```

#### Pinia Store（auth.ts）

```javascript
// frontend/src/stores/auth.ts
import { defineStore } from 'pinia'
import { login, register, logout, getCurrentUser } from '@/api/auth'

export const useAuthStore = defineStore('auth', {
  state: () => ({
    user: null,
    token: localStorage.getItem('token') || null,
    isAuthenticated: !!localStorage.getItem('token')
  }),

  actions: {
    async login(email, password) {
      const response = await login(email, password)
      this.token = response.access_token
      this.user = response.user
      this.isAuthenticated = true
      localStorage.setItem('token', response.access_token)
    },

    async register(username, email, password) {
      const response = await register(username, email, password)
      return response
    },

    async logout() {
      await logout()
      this.token = null
      this.user = null
      this.isAuthenticated = false
      localStorage.removeItem('token')
    },

    async fetchCurrentUser() {
      const user = await getCurrentUser()
      this.user = user
      return user
    }
  }
})
```

#### 路由拦截

```javascript
// frontend/src/router/index.js
(router.beforeEach((to, from, next) => {
  const authStore = useAuthStore()

  // 如果访问的是公开路由（登录/注册），直接放行
  if (to.meta.public) {
    return next()
  }

  // 如果未登录，跳转到登录页
  if (!authStore.isAuthenticated) {
    return next('/login')
  }

  // 如果已登录，访问登录页则跳转到首页
  if (to.path === '/login' && authStore.isAuthenticated) {
    return next('/')
  }

  next()
}))
```

#### Axios 拦截器

```javascript
// frontend/src/api/index.js
api.interceptors.request.use(
  config => {
    const authStore = useAuthStore()
    if (authStore.token) {
      config.headers.Authorization = `Bearer ${authStore.token}`
    }
    return config
  }
)
```

### 2.4 默认超级管理员

初始化脚本创建管理员账号：

```python
# backend/scripts/init_admin.py
import asyncio
from app.db.base import get_db
from app.core.security import get_password_hash
from sqlalchemy import insert
from app.models.user import User

async def create_admin():
    async with get_db() as db:
        # 检查管理员是否存在
        existing = await db.execute(
            select(User).where(User.email == "admin@example.com")
        )
        if existing.first():
            print("Admin already exists")
            return

        # 创建管理员
        admin = User(
            username="admin",
            email="admin@example.com",
            password_hash=get_password_hash("admin123"),
            role="admin"
        )
        db.add(admin)
        await db.commit()
        print("Admin created successfully")

if __name__ == "__main__":
    asyncio.run(create_admin())
```

---

## 任务 3：文章存储功能

### 3.1 存储路径配置

**配置文件修改：**

```python
# backend/app/core/config.py
MARKDOWN_DIR: str = "/Volumes/KINGSTON/faber_mac/wechat_articles"
```

### 3.2 存储规则

#### 文件夹结构
```
/Volumes/KINGSTON/faber_mac/wechat_articles/
├── {biz_1}/
│   ├── 公众号名称_2026-03-26_文章标题1.md
│   ├── 公众号名称_2026-03-26_文章标题2.md
│   └── ...
├── {biz_2}/
│   └── ...
```

#### 文件名规则
```
{公众号名称}_{publish_date}_{文章标题}.md
```

**示例：**
```
活力大宁_2026-03-26_文章标题.md
```

### 3.3 后端实现

#### 文件存储服务

```python
# backend/app/services/storage.py
import os
from pathlib import Path
from datetime import datetime
from app.core.config import settings

class MarkdownStorageService:
    def __init__(self):
        self.base_dir = Path(settings.MARKDOWN_DIR)
        self.base_dir.mkdir(parents=True, exist_ok=True)

    def get_account_dir(self, biz: str) -> Path:
        """获取公众号存储目录"""
        account_dir = self.base_dir / biz
        account_dir.mkdir(parents=True, exist_ok=True)
        return account_dir

    def generate_filename(self, account_name: str, publish_date: str, title: str) -> str:
        """生成文件名"""
        # 清理文件名中的非法字符
        safe_title = self.sanitize_filename(title)
        safe_account_name = self.sanitize_filename(account_name)

        # 截断长标题
        if len(safe_title) > 50:
            safe_title = safe_title[:50]

        return f"{safe_account_name}_{publish_date}_{safe_title}.md"

    def sanitize_filename(self, filename: str) -> str:
        """清理文件名"""
        # 移除不允许的字符
        invalid_chars = ['/', '\\', ':', '*', '?', '"', '<', '>', '|', '\n', '\r']
        for char in invalid_chars:
            filename = filename.replace(char, '_')

        # 移除前后空格
        filename = filename.strip()

        return filename if filename else 'untitled'

    def save_markdown(self, biz: str, account_name: str, publish_date: str,
                     article_id: str, title: str, content: str) -> str:
        """保存 Markdown 文件"""
        account_dir = self.get_account_dir(biz)
        filename = self.generate_filename(account_name, publish_date, title)
        filepath = account_dir / filename

        # 写入文件
        with open(filepath, 'w', encoding='utf-8') as f:
            f.write(content)

        return str(filepath)

storage_service = MarkdownStorageService()
```

#### 修改爬虫逻辑

```python
# backend/app/services/crawler/wechat_crawler.py
from app.services.storage import storage_service

async def crawl_article_detail(self, article_url: str, article_id: str, biz: str, account_name: str):
    """抓取文章详情并保存 MD"""

    # ... 原有抓取逻辑 ...

    # 保存 Markdown 文件
    try:
        md_content = await self.extract_markdown_content(page)
        filepath = storage_service.save_markdown(
            biz=biz,
            account_name=account_name,
            publish_date=publish_date,
            article_id=article_id,
            title=title,
            content=md_content
        )

        # 更新数据库中的文件路径
        await update_article_markdown_path(article_id, filepath)
    except Exception as e:
        logger.error(f"保存 Markdown 文件失败: {e}")
```

#### 数据库字段

为 articles 表添加字段：
```sql
ALTER TABLE articles ADD COLUMN markdown_path TEXT;
ALTER TABLE articles ADD COLUMN file_saved BOOLEAN DEFAULT FALSE;
```

### 3.4 新增接口

#### 获取 MD 文件
```python
@router.get("/articles/{article_id}/markdown")
async def get_article_markdown(
    article_id: int,
    current_user = Depends(get_current_user)
):
    """获取文章 Markdown 内容"""
    article = await get_article_by_id(article_id)
    if not article or article.user_id != current_user.id:
        raise HTTPException(status_code=404, detail="Article not found")

    if not article.file_saved or not article.markdown_path:
        raise HTTPException(status_code=404, detail="Markdown file not found")

    # 读取文件
    with open(article.markdown_path, 'r', encoding='utf-8') as f:
        content = f.read()

    return {"content": content}
```

#### 下载 MD 文件
```python
@router.get("/articles/{article_id}/download")
async def download_article_markdown(
    article_id: int,
    current_user = Depends(get_current_user)
):
    """下载文章 Markdown 文件"""
    article = await get_article_by_id(article_id)
    if not article or article.user_id != current_user.id:
        raise HTTPException(status_code=404, detail="Article not found")

    if not article.file_saved or not article.markdown_path:
        raise HTTPException(status_code=404, detail="Markdown file not found")

    # 返回文件
    from fastapi.responses import FileResponse
    filename = os.path.basename(article.markdown_path)
    return FileResponse(
        path=article.markdown_path,
        filename=filename,
        media_type='text/markdown'
    )
```

### 3.5 前端实现

#### 文章列表页显示文件状态

```vue
<!-- frontend/src/views/ArticleList.vue -->
<el-table-column label="文件状态" width="120">
  <template #default="{ row }">
    <el-tag :type="row.file_saved ? 'success' : 'info'" size="small">
      {{ row.file_saved ? '已保存' : '未保存' }}
    </el-tag>
  </template>
</el-table-column>

<el-table-column label="操作" width="200">
  <template #default="{ row }">
    <el-button
      v-if="row.file_saved"
      size="small"
      @click="viewMarkdown(row)"
    >
      查看 MD
    </el-button>
    <el-button
      v-if="row.file_saved"
      size="small"
      type="primary"
      @click="downloadMarkdown(row)"
    >
      下载
    </el-button>
  </template>
</el-table-column>
```

#### Markdown 预览

```vue
<!-- Markdown 预览对话框 -->
<el-dialog v-model="markdownVisible" title="文章预览" width="80%">
  <div class="markdown-preview">
    <pre>{{ markdownContent }}</pre>
  </div>
</el-dialog>
```

```javascript
// JavaScript
const viewMarkdown = async (article) => {
  try {
    const res = await getArticleMarkdown(article.id)
    markdownContent.value = res.content
    markdownVisible.value = true
  } catch (error) {
    ElMessage.error('获取文章失败')
  }
}

const downloadMarkdown = async (article) => {
  try {
    const url = `/api/v1/articles/${article.id}/download`
    window.open(url, '_blank')
  } catch (error) {
    ElMessage.error('下载失败')
  }
}
```

---

## 任务 4：自测爬虫功能

### 4.1 测试计划

#### 1. 环境检查
```bash
# 检查 Python 依赖
pip list | grep -E "fastapi|playwright|apscheduler"

# 检查 Playwright 浏览器
playwright install chromium

# 检查数据库
ls -lh backend/data/wechat.db

# 检查存储目录
ls -lh /Volumes/KINGSTON/faber_mac/wechat_articles/ 2>/dev/null || echo "目录不存在"
```

#### 2. 功能测试

**测试 1：后端服务启动**
```bash
cd backend
python3 -m uvicorn app.main:app --host 0.0.0.0 --port 8000
```

**测试 2：添加公众号**
```bash
curl -X POST http://localhost:8000/api/v1/accounts \
  -H "Content-Type: application/json" \
  -d '{
    "name": "测试号",
    "biz": "MjM5NjE2ODAyMA==",
    "article_url": "https://mp.weixin.qq.com/s/xxxxx"
  }'
```

**测试 3：手动触发抓取**
```bash
curl -X POST http://localhost:8000/api/v1/accounts/1/crawl
```

**测试 4：查看文章列表**
```bash
curl http://localhost:8000/api/v1/articles
```

**测试 5：检查 MD 文件**
```bash
# 查看数据库中的文件路径
sqlite3 backend/data/wechat.db "SELECT id, title, markdown_path, file_saved FROM articles LIMIT 5;"

# 查看实际文件
ls -lh /Volumes/KINGSTON/faber_mac/wechat_articles/*/
```

#### 3. 完整流程测试

**测试场景：**
1. 添加公众号
2. 触发抓取
3. 查看抓取进度
4. 验证文章数据
5. 验证 Markdown 文件
6. 前端显示
7. 下载 Markdown

### 4.2 测试报告模板

```markdown
# 微信爬虫测试报告

## 测试环境
- 测试时间：2026-03-26
- 操作系统：macOS
- Python 版本：3.9+
- Node.js 版本：v24.14.0

## 测试项目

### 1. 环境测试
- [ ] Python 依赖完整
- [ ] Playwright 浏览器安装
- [ ] 数据库初始化
- [ ] 存储目录创建

### 2. 功能测试
- [ ] 后端服务启动
- [ ] 添加公众号
- [ ] 手动抓取触发
- [ ] 文章列表查询
- [ ] 定时任务运行

### 3. 数据测试
- [ ] 公众号数据保存
- [ ] 文章数据保存
- [ ] Markdown 文件生成
- [ ] 文件路径记录

### 4. 前端测试
- [ ] 公众号管理页面
- [ ] 文章列表页面
- [ ] Markdown 预览
- [ ] 文件下载

### 5. 集成测试
- [ ] 完整抓取流程
- [ ] 多公众号抓取
- [ ] 错误处理

## 测试结果
- 通过：X 项
- 失败：Y 项
- 待测试：Z 项

## 问题列表
1. ...
2. ...

## 结论
...
```

---

## 任务 5：环境配置

### 5.1 Python 依赖

检查并安装：
```bash
cd backend
pip install -r requirements.txt

# 如果缺少依赖，手动安装
pip install fastapi uvicorn sqlalchemy playwright apscheduler passlib[bcrypt] python-jose[cryptography]
```

### 5.2 Playwright 浏览器

```bash
playwright install chromium
```

### 5.3 前端依赖

```bash
cd frontend
npm install
```

### 5.4 启动脚本

创建完整的启动脚本：
```bash
# start-all.sh
#!/bin/bash

# 1. 启动后端
cd backend
nohup python3 -m uvicorn app.main:app --host 0.0.0.0 --port 8000 > ../logs/backend.log 2>&1 &

# 2. 构建前端
cd ../frontend
npm run build

# 3. 启动前端静态服务
cd dist
nohup python3 -m http.server 5174 > ../../logs/frontend.log 2>&1 &

# 4. 启动隧道
cd ../..
lt --port 5174 --subdomain wechat-crawler > logs/lt-frontend.log 2>&1 &
lt --port 8000 --subdomain wechat-api > logs/lt-api.log 2>&1 &

echo "服务已启动"
```

---

## 📅 实施计划

### 阶段一：用户系统（2-3天）
1. 数据库表设计和迁移
2. 后端认证接口
3. 前端登录注册页面
4. 路由拦截和状态管理

### 阶段二：UI 升级（1-2天）
1. 全局样式变量
2. Element Plus 主题配置
3. 页面样式优化
4. 布局改进

### 阶段三：文件存储（1-2天）
1. 文件存储服务
2. 修改爬虫逻辑
3. 新增接口
4. 前端查看下载功能

### 阶段四：测试和优化（1天）
1. 功能测试
2. 修复问题
3. 性能优化
4. 文档完善

**总计：5-8 天**

---

## 🎯 交付清单

### 代码
- [ ] 完整的后端代码
- [ ] 完整的前端代码
- [ ] 数据库迁移脚本
- [ ] 配置文件

### 文档
- [ ] 技术文档
- [ ] API 文档
- [ ] 部署文档
- [ ] 测试报告

### 其他
- [ ] 启动脚本
- [ ] 环境说明
- [ ] 使用指南

---

## ⚠️ 注意事项

1. **数据备份：** 改造前备份现有数据库
2. **向后兼容：** 不破坏现有数据
3. **权限控制：** 严格执行数据隔离
4. **错误处理：** 完善的错误处理和日志
5. **测试充分：** 每个功能都要充分测试

---

**创建时间：** 2026-03-26
**预计完成时间：** 5-8 天
**负责人：** AI 助手（Claude Code）
