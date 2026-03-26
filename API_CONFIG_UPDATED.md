# 前端 API 配置更新完成

## ✅ 更新内容

已修改前端 API 配置，实现根据访问环境自动选择后端 API 地址：

### 本地访问
- 前端地址：`http://localhost:8080`
- 后端 API：`http://localhost:8002/api/v1`

### 公网访问（LocalTunnel）
- 前端地址：`https://wechat-crawler-fwb.loca.lt`
- 后端 API：`https://wechat-crawler-api.loca.lt/api/v1`

---

## 📝 修改文件

`frontend/src/api/index.js`

新增了 `getApiBaseURL()` 函数，根据 `window.location.hostname` 自动判断环境：

```javascript
const getApiBaseURL = () => {
  const hostname = window.location.hostname

  // 公网环境 - LocalTunnel
  if (hostname === 'wechat-crawler-fwb.loca.lt') {
    return 'https://wechat-crawler-api.loca.lt/api/v1'
  }

  // 本地开发环境
  if (hostname === 'localhost' || hostname === '127.0.0.1') {
    return 'http://localhost:8002/api/v1'
  }

  // 其他环境默认使用本地
  return 'http://localhost:8002/api/v1'
}
```

---

## 🔄 部署状态

- [x] 前端已重新构建
- [x] 前端服务已重启
- [x] 公网隧道正常

---

## 🌐 访问链接

**本地访问：**
- 前端：http://localhost:8080
- 后端：http://localhost:8002

**公网访问：**
- 前端：https://wechat-crawler-fwb.loca.lt
- 后端：https://wechat-crawler-api.loca.lt
- API 文档：https://wechat-crawler-api.loca.lt/docs

---

## 👤 登录信息

- 用户名：admin
- 密码：admin123

---

