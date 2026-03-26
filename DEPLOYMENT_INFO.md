# 微信爬虫平台 - 公网访问信息

## ✅ 部署完成！

微信爬虫平台已经成功部署并通过公网可访问。

---

## 🌐 访问地址

### 前端界面
```
https://wechat-crawler-fwb.loca.lt
```

### 后端 API
```
https://wechat-crawler-api-fwb.loca.lt
```

### API 文档（Swagger）
```
http://localhost:8000/docs
```

---

## 🏠 本地访问地址

### 前端
```
http://localhost:5174
```

### 后端
```
http://localhost:8000
```

---

## 🚀 服务状态

### ✅ 后端服务（FastAPI）
- 状态：运行中
- 端口：8000
- 进程 ID：19334
- 数据库：已初始化
- 浏览器池：3 个实例已加载
- 定时任务：已启动（每 6 小时扫描一次）
- 当前抓取：正在抓取"活力大宁"公众号

### ✅ 前端服务（Vue 3 + Vite）
- 状态：运行中
- 端口：5174
- 访问：http://localhost:5174

### ✅ 内网穿透服务（localtunnel）
- 前端隧道：https://wechat-crawler-fwb.loca.lt
- API 隧道：https://wechat-crawler-api-fwb.loca.lt

---

## 📊 数据统计

### 当前数据
- 活跃公众号：1 个（活力大宁）
- 数据库：/Users/fengweibo/Desktop/wechat-crawler-platform/backend/data/wechat.db
- 登录态：已启用（3 个浏览器实例）
- 日志位置：
  - 后端：/tmp/wechat-backend.log
  - 前端：/tmp/wechat-frontend.log
  - 隧道：/tmp/lt.log (前端), /tmp/lt-api.log (API)

---

## 🔧 管理命令

### 查看后端日志
```bash
tail -f /tmp/wechat-backend.log
```

### 查看前端日志
```bash
tail -f /tmp/wechat-frontend.log
```

### 查看隧道日志
```bash
tail -f /tmp/lt.log        # 前端隧道
tail -f /tmp/lt-api.log    # API 隧道
```

### 重启后端服务
```bash
pkill -f "uvicorn app.main:app"
cd /Users/fengweibo/Desktop/wechat-crawler-platform/backend
nohup python3 -m uvicorn app.main:app --host 0.0.0.0 --port 8000 > /tmp/wechat-backend.log 2>&1 &
```

### 重启前端服务
```bash
cd /Users/fengweibo/Desktop/wechat-crawler-platform/frontend
nohup npm run dev > /tmp/wechat-frontend.log 2>&1 &
```

### 重启隧道服务
```bash
pkill -f "lt --port"
lt --port 5174 --subdomain wechat-crawler-fwb > /tmp/lt.log 2>&1 &
lt --port 8000 --subdirectory api --subdomain wechat-crawler-api-fwb > /tmp/lt-api.log 2>&1 &
```

### 停止所有服务
```bash
pkill -f "uvicorn app.main:app"   # 后端
pkill -f "vite"                   # 前端
pkill -f "lt --port"              # 隧道
```

---

## ⚠️ 注意事项

### 1. 隧道服务
- 隧道服务依赖你的机器保持在线
- 如果你的机器关机或断网，公网链接将无法访问
- 建议保持机器一直开机或在需要时手动启动

### 2. localtunnel 特性
- localtunnel 是免费的，可能有流量限制
- 链接稳定性取决于网络状况
- 首次访问时可能需要输入验证码

### 3. 安全性
- 当前配置不包含访问限制，任何人都可以访问
- 如果需要安全性，可以：
  - 配置 Cloudflare Tunnel（支持自定义域名和访问控制）
  - 添加 API 认证
  - 使用 VPN

---

## 📈 下一步优化建议

### 1. 固定域名
考虑使用 Cloudflare Tunnel 获取固定的自定义域名。

### 2. 访问控制
添加用户认证或 IP 白名单限制访问。

### 3. 监控告警
配置服务监控，异常时自动通知。

### 4. 数据备份
定期备份数据库，防止数据丢失。

---

## 📞 故障排查

### 无法访问公网链接
1. 检查隧道服务是否运行：`ps aux | grep lt`
2. 查看隧道日志：`tail -f /tmp/lt.log`
3. 重启隧道服务：见上方管理命令

### 前端无法连接后端
1. 检查后端是否运行：`ps aux | grep uvicorn`
2. 查看后端日志：`tail -f /tmp/wechat-backend.log`
3. 确认后端端口：`netstat -an | grep 8000`

### 抓取失败
1. 检查微信登录态是否过期
2. 查看详细日志：`tail -f /tmp/wechat-backend.log`
3. 重新登录微信：见项目文档 LOGIN_GUIDE.md

---

**部署时间：** 2026-03-26 10:01
**部署人：** AI 助手
**项目位置：** /Users/fengweibo/Desktop/wechat-crawler-platform

🎉 享受你的云访问吧！
