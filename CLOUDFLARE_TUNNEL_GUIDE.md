# Cloudflare Tunnel 部署指南

## 🎯 方案优势

相比 localtunnel，Cloudflare Tunnel 的优势：

- ✅ **永久免费** - 无流量限制，无需担心超额
- ✅ **固定域名** - 使用你自己的域名，或者 Cloudflare 提供的域名
- ✅ **全球加速** - Cloudflare CDN 加速，访问速度快
- ✅ **SSL/TLS 支持** - 自动配置 HTTPS 证书
- ✅ **访问控制** - 可配置访问权限（可选）
- ✅ **稳定性高** - Cloudflare 免费提供的基础设施
- ✅ **日志监控** - 免贵的流量和访问日志

---

## 📋 部署步骤总览

### 第一阶段：账号准备（需要你手动操作）
1. 注册 Cloudflare 账号
2. 添加并验证域名，或使用 Cloudflare 免费域名

### 第二阶段：安装配置（我可以自动完成）
3. 安装 cloudflared 工具
4. 创建隧道
5. 配置服务映射
6. 启动隧道

### 第三阶段：验证使用（测试）
7. 验证公网访问
8. 配置前端和后端

---

## 🚀 详细步骤

### 第一阶段：账号准备

#### 1. 注册 Cloudflare 账号

**注册地址**：https://dash.cloudflare.com/sign-up

**步骤**：
1. 使用邮箱注册（推荐使用 Gmail/Outlook 等）
2. 进入邮箱验证
3. 登录 Cloudflare Dashboard

#### 2. 域名配置

**方案 A：使用你自己的域名（推荐）**

如果你有域名（如 `example.com`）：

1. 在 Cloudflare Dashboard 点击 **"Add a site"**
2. 输入你的域名（如 `faberfeng.com`）
3. 选择 **Free** 免费计划
4. Cloudflare 会提供两个 nameserver（如 `nina.ns.cloudflare.com`）
5. 到你的域名注册商（阿里云/腾讯云/GoDaddy 等）修改 nameserver
6. 等待 DNS 生效（通常 10-60 分钟）

**方案 B：使用 Cloudflare 免费域名**

如果你没有域名：

1. 访问 https://dash.cloudflare.com/sign-up
2. 注册时会自动分配一个 Cloudflare 免费域名
3. 或者使用 `*.trycloudflare.com` 临时域名（无需注册）

---

### 第二阶段：安装配置

#### 3. 安装 cloudflared（我可以帮你完成）

**系统命令**：
```bash
# macOS 安装
brew install cloudflare/cloudflare/cloudflared

# 或者直接下载二进制文件
curl -L https://github.com/cloudflare/cloudflared/releases/latest/download/cloudflared-darwin-amd64.tar.gz | tar xz
sudo mv cloudflared /usr/local/bin/
```

#### 4. 登录 Cloudflare（需要你授权）

**系统命令**：
```bash
cloudflared tunnel login
```

**操作步骤**：
1. 执行命令后，会自动打开浏览器
2. 选择你要授权的域名（如 `faberfeng.com`）
3. 点击 **Authorize** 授权
4. 授权成功后会创建 `~/.cloudflared/cert.pem` 文件

---

#### 5. 创建隧道（我可以帮你完成）

**创建隧道**：
```bash
# 创建名为 wechat-crawler 的隧道
cloudflared tunnel create wechat-crawler
```

**输出示例**：
```
Tunnel credentials written to /Users/fengweibo/.cloudflared/xxxxxxxx-cert.pem
Tunnel ID: xxxxxxxx-xxxx-xxxx-xxxx-xxxxxxxxxxxx
```

**保存隧道 ID**：记录下 `Tunnel ID`，后续配置需要用到。

---

#### 6. 配置服务映射（我可以帮你完成）

**创建配置文件**：`~/.cloudflared/config.yml`

**完整配置示例**：
```yaml
tunnel: xxxxxxxx-xxxx-xxxx-xxxx-xxxxxxxxxxxx  # 替换为你的 Tunnel ID
credentials-file: /Users/fengweibo/.cloudflared/xxxxxxxx-cert.pem

ingress:
  # 前端服务
  - hostname: wechat.faberfeng.com              # 你的域名
    service: http://localhost:5174              # 前端服务端口

  # 后端 API
  - hostname: api.wechat.faberfeng.com         # API 子域名
    service: http://localhost:8000              # 后端服务端口

  # API 文档
  - hostname: docs.wechat.faberfeng.com        # 文档子域名
    service: http://localhost:8000              # 后端服务端口

  # 默认路由（放在最后）
  - service: http_status:404
```

**如果你使用 Cloudflare 免费域名**：
```yaml
tunnel: xxxxxxxx-xxxx-xxxx-xxxx-xxxxxxxxxxxx
credentials-file: /Users/fengweibo/.cloudflared/xxxxxxxx-cert.pem

ingress:
  - hostname: xxxxx.channels.cloudflare.net     # Cloudflare 提供的域名
    service: http://localhost:5174
  - service: http_status:404
```

---

#### 7. 添加 DNS 记录（需要你在 Cloudflare Dashboard 操作）

**方法 A：使用命令行（推荐）**

```bash
# 为前端添加 DNS 记录
cloudflared tunnel route dns wechat-crawler wechat.faberfeng.com

# 为 API 添加 DNS 记录
cloudflared tunnel route dns wechat-crawler api.wechat.faberfeng.com

# 为文档添加 DNS 记录
cloudflared tunnel route dns wechat-crawler docs.wechat.faberfeng.com
```

**方法 B：在 Cloudflare Dashboard 配置**

1. 登录 https://dash.cloudflare.com
2. 选择你的域名
3. 进入 **DNS → Records**
4. 点击 **Add record**
5. 配置：
   - **Type**: CNAME
   - **Name**: `wechat`
   - **Target**: `xxxxxx.channels.cloudflare.net`（创建隧道时显示）
   - **Proxy status**: Proxied（橙色云朵）
6. 点击 **Save**

---

#### 8. 启动隧道（我可以帮你完成）

**启动命令**：
```bash
# 测试运行
cloudflared tunnel run

# or 指定配置文件
cloudflared tunnel --config ~/.cloudflared/config.yml run
```

**后台运行**：
```bash
nohup cloudflared tunnel --config ~/.cloudflared/config.yml run > /tmp/cloudflared.log 2>&1 &
```

---

### 第三阶段：验证使用

#### 9. 验证公网访问

**测试前端**：
```bash
curl https://wechat.faberfeng.com
```

**测试后端 API**：
```bash
curl https://api.wechat.faberfeng.com/health
```

#### 10. 更新前端和后端配置

**后端 CORS 配置**：`backend/app/core/config.py`

```python
CORS_ORIGINS: str = "https://wechat.faberfeng.com,https://api.wechat.faberfeng.com,http://localhost:5173,http://localhost:5174"
```

**前端 API 配置**：`frontend/src/api/index.js`

```javascript
const api = axios.create({
  baseURL: 'https://api.wechat.faberfeng.com/api/v1',  // 改为 Cloudflare 域名
  timeout: 30000
})
```

---

## 🔧 管理命令

### 查看 tunnel 信息
```bash
cloudflared tunnel list
```

### 查看隧道日志
```bash
cloudflared tunnel info wechat-crawler
tail -f /tmp/cloudflared.log
```

### 停止隧道
```bash
pkill -f cloudflared
```

### 重启隧道
```bash
pkill -f cloudflared
nohup cloudflared tunnel --config ~/.cloudflared/config.yml run > /tmp/cloudflared.log 2>&1 &
```

---

## 🛠️ 完整自动化脚本示例

**创建启动脚本**：`start-cloudflare-tunnel.sh`

```bash
#!/bin/bash
# Cloudflare Tunnel 启动脚本

TUNNEL_NAME="wechat-crawler"
CONFIG_FILE="$HOME/.cloudflared/config.yml"
LOG_FILE="/tmp/cloudflared.log"

# 停止旧进程
echo "停止旧的 tunnel 进程..."
pkill -f cloudflared

# 等待进程完全停止
sleep 2

# 启动 tunnel
echo "启动 Cloudflare Tunnel: $TUNNEL_NAME"
nohup cloudflared tunnel --config "$CONFIG_FILE" run "$TUNNEL_NAME" > "$LOG_FILE" 2>&1 &

# 等待启动
sleep 3

# 检查状态
if pgrep cloudflared > /dev/null; then
    echo "✅ Cloudflare Tunnel 启动成功"
    echo "📝 日志文件: $LOG_FILE"
    echo "🔗 前端地址: https://wechat.faberfeng.com"
    echo "🔗 API 地址: https://api.wechat.faberfeng.com"
else
    echo "❌ Cloudflare Tunnel 启动失败"
    echo "📝 查看日志: tail -f $LOG_FILE"
    exit 1
fi
```

**添加执行权限**：
```bash
chmod +x start-cloudflare-tunnel.sh
```

**使用**：
```bash
./start-cloudflare-tunnel.sh
```

---

## 📊 对比：Cloudflare Tunnel vs Localtunnel

| 特性 | Cloudflare Tunnel | Localtunnel |
|------|-------------------|-------------|
| **费用** | 完全免费 | 免费但有流量限制 |
| **域名** | 自定义域名或固定域名 | 随机子域名 |
| **稳定性** | 极高（Cloudflare 基础设施） | 中等 |
| **HTTPS** | 自动配置 | 自动配置 |
| **访问控制** | 支持 | 不支持 |
| **流量统计** | 详细的访问日志 | 基本日志 |
| **长期使用** | 推荐长期使用 | 临时测试 |

---

## ⚡ 快速启动（如果已有 Cloudflare 账号）

如果你已经注册了 Cloudflare 账号并添加了域名，只需要：

1. **登录授权**（手动）：
   ```bash
   cloudflared tunnel login
   ```

2. **创建隧道**（我可以帮你）：
   ```bash
   cloudflared tunnel create wechat-crawler
   ```

3. **配置路由**（我可以帮你）：
   ```bash
   cloudflared tunnel route dns wechat-crawler wechat.faberfeng.com
   ```

4. **启动隧道**（我可以帮你）：
   ```bash
   cloudflared tunnel run
   ```

---

## ❓ 常见问题

### Q1: 没有 Cloudflare 账号怎么办？
**A**: 注册一个免费账号即可，https://dash.cloudflare.com/sign-up

### Q2: 没有自己的域名怎么办？
**A**: 可以使用 Cloudflare 免费域名或 `*.trycloudflare.com` 临时域名

### Q3: 多久能生效？
**A**:
- 如果有自己的域名：DNS 生效需要 10-60 分钟
- 如果用 Cloudflare 免费域名：立即生效

### Q4: 能同时运行 localtunnel 和 Cloudflare Tunnel 吗？
**A**: 可以，但建议只用一个，避免冲突

### Q5: 可以重启机器后自动启动吗？
**A**: 可以，使用开机自启动脚本或 systemd 服务

---

## 🎉 完成后的访问地址

**Cloudflare Tunnel 部署完成后，你将获得固定域名**：

### 前端界面
```
https://wechat.faberfeng.com           # 你的自定义域名
```

### 后端 API
```
https://api.wechat.faberfeng.com/api/v1
```

### API 文档
```
https://docs.wechat.faberfeng.com/docs
```

---

## 📞 下一步

**准备好后，告诉我**：

1. ✅ 你是否已经有 Cloudflare 账号？
2. ✅ 你是否有自己的域名？
3. ✅ 你的 Cloudflare 域名是什么？

**我可以帮你**：
- 安装 cloudflared 工具
- 创建隧道并配置
- 生成配置文件
- 自动启动服务
- 更新前端和后端配置

---

**准备开始了吗？告诉我你的情况！** 🚀
