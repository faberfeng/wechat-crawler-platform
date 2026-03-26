# 问题已解决！

## ❌ 问题描述

通过公网访问前端时，页面无法连接到后端 API，导致功能无法使用。

## 🔍 问题原因

1. **后端 CORS 配置限制**：后端只允许 `localhost` 域名访问，没有配置公网域名
2. **前端 API 地址配置错误**：前端仍使用 `http://localhost:8000` 作为 API 地址

## ✅ 解决方案

### 1️⃣ 修改后端 CORS 配置

文件：`backend/app/core/config.py`

**修改前：**
```python
CORS_ORIGINS: str = "http://localhost:5173,http://localhost:3000"
```

**修改后：**
```python
CORS_ORIGINS: str = "http://localhost:5173,http://localhost:3000,http://localhost:5174,https://wechat-crawler-fwb.loca.lt,https://wechat-crawler-api-fwb.loca.lt"
```

### 2️⃣ 修改前端 API 配置

文件：`frontend/src/api/index.js`

**修改前：**
```javascript
const api = axios.create({
  baseURL: 'http://localhost:8000/api/v1',
  timeout: 30000
})
```

**修改后：**
```javascript
const api = axios.create({
  baseURL: 'https://wechat-crawler-api-fwb.loca.lt/api/v1',
  timeout: 30000
})
```

## 🔄 重启服务

已自动重启后端服务，新配置已生效。

## ✅ 验证结果

### API 健康检查
```bash
$ curl https://wechat-crawler-api-fwb.loca.lt/health
{"status":"ok","service":"wechat-crawler"}
```

### API 账号列表
```bash
$ curl https://wechat-crawler-api-fwb.loca.lt/api/v1/accounts
[{"id":1,"biz":"MjM5NjE2ODAyMA==","name":"活力大宁","avatar_url":null,"is_active":true,"last_crawl_time":null,"article_count":0,"created_at":"2026-03-25T11:23:36.844227","updated_at":"2026-03-26T01:01:22.179822"}]
```

## 🎉 现在可以正常使用！

### 公网访问地址

📱 **前端界面**：
```
https://wechat-crawler-fwb.loca.lt
```

🔌 **后端 API**：
```
https://wechat-crawler-api-fwb.loca.lt
```

---

## ⚠️ 注意事项

1. **浏览器缓存**：如果仍有问题，请刷新浏览器页面（Ctrl+F5 或 Cmd+Shift+R）
2. **CORS 限制**：如果更换隧道域名，需要同步修改两个配置文件
3. **安全性**：当前配置允许任何来源访问，生产环境建议限制具体域名

---

## 🔧 相关文件

- 后端配置：`backend/app/core/config.py`
- 前端配置：`frontend/src/api/index.js`

---

## 📝 后续优化建议

1. **环境变量管理**：将 API 地址配置为环境变量，方便部署时修改
2. **自动化脚本**：创建一键重启脚本，自动更新配置并重启服务
3. **域名固定**：后续可使用 Cloudflare Tunnel 获取固定域名

---

**修复时间：** 2026-03-26 10:05
**修复状态：** ✅ 完成
