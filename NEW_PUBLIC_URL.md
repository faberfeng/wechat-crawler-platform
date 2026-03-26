# 🎉 腾道已更新！公网访问地址

## ✅ 新的访问地址

### 📱 前端界面
```
https://wechat-fwb.loca.lt
```

### 🔌 后端 API
```
https://wechat-crawler-api-fwb.loca.lt
```

---

## 🔄 更新说明

由于之前的子域名可能被占用，已重新创建隧道：

**旧地址（已失效）：**
- ❌ https://wechat-crawler-fwb.loca.lt

**新地址（当前可用）：**
- ✅ https://wechat-fwb.loca.lt
- ✅ https://wechat-crawler-api-fwb.loca.lt

---

## 🌐 第一次访问如何通过验证

当你第一次访问 `https://wechat-fwb.loca.lt` 时：

### 可能遇到的情况：

#### 情况 1：显示 Cloudflare 验证页面

**你会看到：**
- "Checking your browser before accessing..."
- 或者 "Just a moment..."
- 可能需要验证码

**解决方法：**
1. 等待几秒钟
2. 如果有验证码，勾选"我不是机器人"
3. 点击验证
4. 验证通过后自动跳转

**只需验证一次！** 后续访问就不会有了。

---

#### 情况 2：显示 403 Forbidden

**如果你在 curl 或工具中看到：**
```
HTTP/1.1 403 Forbidden
```

**这是正常的！** Cloudflare 对非浏览器请求会返回 403。

**解决方法：**
- **必须使用浏览器访问**
- 手机浏览器也可以（Safari, Chrome 等）
- 完成验证后就可以正常使用

---

#### 情况 3：连接超时

**如果页面无法打开：**

**解决方法：**
1. 刷新浏览器：`Cmd+Shift+R` (Mac) 或 `Ctrl+F5` (Windows)
2. 换个浏览器试试（Chrome, Edge, Firefox）
3. 等 5-10 分钟再试
4. 检查网络连接

---

## 🎯 验证成功后

验证通过后，你会看到：

**微信公众号抓取平台** 界面，包括：
- 📱 公众号管理
- 📝 文章列表
- 🔍 搜索功能
- ⚙️ 设置

---

## 📊 当前服务状态

| 服务 | 状态 | 地址 | 说明 |
|------|------|------|------|
| 前端服务 | ✅ 运行中 | http://localhost:5174 | 本地访问 |
| 前端隧道 | ✅ 运行中 | https://wechat-fwb.loca.lt | **新地址** |
| 后端服务 | ✅ 运行中 | http://localhost:8000 | 本地访问 |
| API 隧道 | ✅ 运行中 | https://wechat-crawler-api-fwb.loca.lt | API 地址 |

---

## 💡 重要提示

### 关于首次访问

1. **必须用浏览器访问**（不能用 curl、wget 等工具）
2. **完成 Cloudflare 验证**（验证码或等待）
3. **仅需验证一次**（Cloudflare 会记住你的浏览器）
4. **验证后可正常使用**

### 关于连接稳定性

- ✅ Loc altunnel 使用 Cloudflare，稳定性很好
- ✅ 支持持续连接
- ✅ 无需额外配置

### 如果验证失败

1. 检查网络是否正常
2. 尝试其他浏览器
3. 等几分钟后重试
4. 使用手机浏览器试试

---

## 🔧 管理命令

### 重启隧道

```bash
# 停止所有隧道
pkill -f "lt --port"

# 启动前端隧道
lt --port 5174 --subdomain wechat-fwb

# 启动 API 隧道（新终端）
lt --port 8000 --subdomain wechat-crawler-api-fwb
```

### 查看隧道状态

```bash
ps aux | grep "lt --port" | grep -v grep
```

---

## 🚀 现在试试吧！

**在浏览器中访问：**
```
https://wechat-fwb.loca.lt
```

**步骤：**
1. 打开浏览器
2. 输入地址
3. 等待验证页面
4. 完成验证（如有）
5. 开始使用！

---

## 📞 遇到问题？

**如果还是进不去：**

1. **告诉我具体看到了什么**（页面提示或错误信息）
2. **确认你的公网 IP：** `58.247.19.62`
3. **我们帮你排查**

---

**✨ 试试看，应该可以正常访问了！**

---

更新时间：2026-03-26 10:53
当前 IP：58.247.19.62
前端隧道：wechat-fwb
API 隧道：wechat-crawler-api-fwb
