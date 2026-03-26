# 微信公众号爬虫平台 - 使用指南

## 问题诊断

### 当前状态
✅ 后端启动成功
✅ 浏览器池初始化成功
❌ 爬取文章失败（提取到 0 篇）

### 根本原因
微信公众号历史文章页面需要**登录态**才能访问。当没有登录态时，微信会显示"验证"页面，拒绝爬虫访问。

## 解决方案

### 方法一：扫码登录（推荐）

步骤：
1. 运行扫码登录工具（需要手动操作）
2. 使用微信扫描二维码登录
3. 自动保存登录态到 `data/auth_sessions/`
4. 重启后端服务，自动使用登录态

**执行命令：**
```bash
cd ~/Desktop/wechat-crawler-platform/backend

# 扫码登录（会打开浏览器窗口）
python3 login_wechat.py --account my_wechat

# 等待扫码完成后，启动后端
python3 -m uvicorn app.main:app --host 127.0.0.1 --port 8000 --reload
```

### 方法二：使用已有登录态文件

如果你已经有微信登录态文件（Chrome cookies 等），可以手动转换格式并放到 `data/auth_sessions/` 目录。

**登录态文件格式：** JSON 格式，包含 cookies 和 localStorage
```json
{
  "cookies": [
    {
      "name": "xxx",
      "value": "xxx",
      "domain": ".mp.weixin.qq.com",
      "path": "/",
      "expires": 1234567890,
      "httpOnly": true,
      "secure": true,
      "sameSite": "None"
    }
  ],
  "origins": []
}
```

### 方法三：使用第三方 API（备选）

如果不想扫码登录，可以使用以下替代方案：
- **wechat-crawler** (GitHub 开源项目)
- **BrowserAct (API)** (本项目已集成的技能)
- 其他微信公众号爬虫工具

## 测试爬虫功能

### 1. 手动测试

启动后端后，访问 API：
```bash
curl http://127.0.0.1:8000/api/v1/accounts
curl http://127.0.0.1:8000/api/v1/articles
```

### 2. 查看 API 文档
```bash
# 在浏览器中打开
http://127.0.0.1:8000/docs
```

### 3. 查看日志
```bash
cd ~/Desktop/wechat-crawler-platform/backend
tail -f logs/app.log
```

## 常见问题

### Q: 找不到登录态文件？
A: 确保已运行 `login_wechat.py` 并成功扫码登录。文件会保存在 `data/auth_sessions/` 目录。

### Q: 登录态过期了怎么办？
A: 重新运行 `login_wechat.py` 扫码登录，会生成新的登录态文件。

### Q: 浏览器窗口打开太快看不到二维码？
A: 可以修改 `login_wechat.py` 中的超时时间，或者在浏览器窗口打开后人工等待。

### Q: 能否自动化登录？
A: 微信登录态有有效期限制，目前只能通过扫码登录获取。可以设置定时任务自动重新登录。

## 当前修复内容

### 已修复问题
1. ✅ 浏览器池支持加载/保存登录态
2. ✅ 提供扫码登录工具
3. ✅ 诊断脚本识别根本原因

### 待实现功能
1. ⏳ 登录态自动刷新机制
2. ⏳ 多账号管理
3. ⏳ 前端界面集成登录功能

## 下一步

1. **立即执行：** 运行 `python3 login_wechat.py` 扫码登录
2. **启动服务：** 登录完成后启动后端服务
3. **测试功能：** 访问 `http://127.0.0.1:8000/docs` 查看 API
4. **抓取文章：** 调用 `/api/v1/crawl` 接口开始抓取

---

## 技术说明

### 登录态工作原理
- 微信公众号使用 cookies 验证登录状态
- Playwright 通过 `storage_state` 保存并加载 cookies
- 登录态有效期通常为 1-3 天，需定期刷新

### 爬虫选择器说明
项目使用两种方式提取文章：
1. **DOM 提取**：直接解析 HTML（快速但不可靠）
2. **XHR 拦截**：拦截 API 请求（可靠但复杂）

目前两种方式都已实现，会根据实际情况自动选择。
