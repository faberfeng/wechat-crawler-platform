# 🚀 快速测试清单

## 📊 自动化测试状态

| 测试项 | 状态 | 命令 |
|--------|------|------|
| 前端服务 | ✅ | curl http://localhost:5174 |
| 后端服务 | ✅ | curl http://localhost:8000/health |
| 注册接口 | ✅ | POST /api/v1/auth/register |
| 登录接口 | ✅ | POST /api/v1/auth/login |
| 用户信息 | ✅ | GET /api/v1/auth/me |
| 管理员登录 | ✅ | admin@example.com / admin123 |
| 用户列表 | ✅ | GET /api/v1/users/ |

**自动化测试结果：** ✅ **7/7 通过**

---

## 🧪 浏览器测试清单

### 快速测试（5 分钟）

- [ ] 访问 http://localhost:5174
- [ ] 点击"立即注册"
- [ ] 填写：用户名/邮箱/密码
- [ ] 点击"注册"
- [ ] 提示"注册成功"，跳转到登录
- [ ] 使用新注册的账号登录
- [ ] 提示"登录成功"，跳转到首页
- [ ] 检查页面显示用户名
- [ ] 点击"登出"按钮
- [ ] 跳转回登录页面

**快速测试结果：** ⬜ / 10 通过

### 完整测试（15 分钟）

详见：`BROWSER_TEST_GUIDE.md`

- [ ] 10 个基础场景
- [ ] 4 个高级测试
- [ ] 截图 10 张
- [ ] 记录所有问题

**完整测试结果：** ⬜ / 14 通过

---

## 🌐 访问地址

### 前端
**本地：** http://localhost:5174
**公网：** https://fwb-wechat.loca.lt

### 后端
**本地：** http://localhost:8000
**公网：** https://wechat-crawler-api-fwb.loca.lt
**文档：** http://localhost:8000/docs

---

## 🔑 测试账号

### 管理员
```
邮箱：admin@example.com
密码：admin123
```

### 普通用户
```
邮箱：test_frontend@example.com
密码：testpass123
```

### 最新测试用户
```
用户名：web_test_user_1774497795
邮箱：web_test_30610@example.com
密码：testpass123
```

---

## 📋 测试命令

### 运行自动化测试
```bash
cd /Users/fengweibo/Desktop/wechat-crawler-platform
./quick-test-frontend.sh
```

### 运行完整认证测试
```bash
cd /Users/fengweibo/Desktop/wechat-crawler-platform
./test-complete-auth.sh
```

---

## 📊 测试结果

### 最近测试
- **时间：** 2026-03-26 11:55
- **自动化测试：** ✅ 10/10 通过
- **性能：** 优秀（响应时间 < 2ms）

### 发现问题
- **严重问题：** 0
- **一般问题：** 0
- **建议：** 0

---

## 🎯 下一步

### 立即行动
选择一个选项：

#### 选项 1：浏览器测试（当前）
按照 `BROWSER_TEST_GUIDE.md` 进行手工测试

#### 选项 2：完善认证功能
- [ ] 实现密码修改
- [ ] 实现用户更新
- [ ] 添加邮箱验证

#### 选项 3：UI 升级
- [ ] 优化响应式布局
- [ ] 添加动画效果
- [ ] 改进错误提示

#### 选项 4：文件存储
- [ ] 文件上传接口
- [ ] 文件列表展示
- [ ] 文件预览功能

#### 选项 5：核心功能
- [ ] 公众账号管理
- [ ] 文章列表展示
- [ ] 文章详情页

---

## ❓ 常见问题

### Q1: 无法访问公网地址？
**A:** 检查 Cloudflare Tunnel 是否运行
```bash
cd /Users/fengweibo/Desktop/wechat-crawler-platform
./start.sh
```

### Q2: 登录后立即跳转回登录页？
**A:**
1. 打开浏览器控制台（F12）
2. 检查 localStorage 是否有 token
3. 检查 Network 标签中的 API 响应

### Q3: 管理员看不到"用户管理"菜单？
**A:**
1. 打开控制台（F12）
2. 输入：`JSON.parse(localStorage.getItem('user')).role`
3. 确认显示 'admin'

### Q4: API 请求失败？
**A:**
1. 检查后端服务是否运行
2. 检查 Network 标签错误信息
3. 查看后端日志：`tail -50 logs/backend.log`

---

**更新时间：** 2026-03-26 11:55
