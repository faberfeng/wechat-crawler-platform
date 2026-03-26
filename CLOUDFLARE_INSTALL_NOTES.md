# Cloudflare Tunnel 安装说明

## ⚠️ 当前问题

由于 GitHub 无法访问，无法自动下载 cloudflared 工具。

---

## 🎯 解决方案

### 方案 1：使用国内镜像下载（推荐）

```bash
# 方法 1: 使用 ghproxy 镜像
curl -L https://ghproxy.com/https://github.com/cloudflare/cloudflared/releases/latest/download/cloudflared-darwin-amd64.tar.gz -o /tmp/cloudflared.tar.gz

# 方法 2: 使用 jsDelivr CDN
curl -L https://cdn.jsdelivr.net/gh/cloudflare/cloudflared@latest/cloudflared-darwin-amd64.tar.gz -o /tmp/cloudflared.tar.gz

# 解压
cd /tmp
tar xzf cloudflared.tar.gz

# 复制到系统目录
sudo mv cloudflared /usr/local/bin/
chmod +x /usr/local/bin/cloudflared

# 验证安装
cloudflared --version
```

---

### 方案 2：手动下载

1. 访问官方发布页：
   ```
   https://github.com/cloudflare/cloudflared/releases
   ```

2. 下载 macOS 版本：
   ```
   cloudflared-darwin-amd64.tar.gz
   ```

3. 解压并安装：
   ```bash
   cd ~/Downloads
   tar xzf cloudflared-darwin-amd64.tar.gz
   sudo mv cloudflared /usr/local/bin/
   chmod +x /usr/local/bin/cloudflared
   cloudflared --version
   ```

---

### 方案 3：使用 Homebrew（需要代理）

如果你有稳定的网络环境：

```bash
brew install cloudflare/cloudflare/cloudflared
```

---

## 🚀 安装完成后

运行自动化脚本：

```bash
cd /Users/fengweibo/Desktop/wechat-crawler-platform
./setup-cloudflare-tunnel.sh
```

**脚本会自动完成以下步骤：**

1. 检查 cloudflared 安装
2. 登录 Cloudflare（需浏览器授权）
3. 创建隧道
4. 生成配置文件
5. 提示你添加 DNS 记录
6. 启动隧道

---

## 🌐 关于域名

你说没有自己的域名，有以下几个选择：

### 选项 1：注册一个免费域名

**推荐免费域名注册商：**

- Freenom (freenom.com) - `.tk`, `.ml`, `.ga` 等免费域名
- EU.org - 免费 `.eu.org` 域名
- DuckDNS - 免费 `xxx.duckdns.org` 域名

### 选项 2：使用 Cloudflare 免费域名

Cloudflare 为 tunnels 提供临时域名，格式：
```
xxxxxx.channels.cloudflare.net
```

这个域名是固定的，可以长期使用。

### 选项 3：使用 trycloudflare.com 临时域名

这个不需要 cloudflared，直接使用：

```bash
cloudflared tunnel --url http://localhost:5174
```

会输出类似：
```
https://abcd-efgh.trycloudflare.com
```

这是一个临时域名，会变化。

---

## 💡 我的建议

**如果你现在就想要永久稳定的公网访问：**

1. **暂时使用 localtunnel**（当前已经配置好）
   - 前端：https://wechat-crawler-fwb.loca.lt
   - API：https://wechat-crawler-api-fwb.loca.lt

2. **然后你注册一个免费域名**（比如 `fengweibo.tk`）

3. **回来继续配置 Cloudflare Tunnel**：

   ```bash
   # 等网络恢复后，运行
   cd /Users/fengweibo/Desktop/wechat-crawler-platform
   ./setup-cloudflare-tunnel.sh
   ```

---

## 📋 使用自动化脚本的好处

我为你创建了完整的自动化脚本：
```
/Users/fengweibo/Desktop/wechat-crawler-platform/setup-cloudflare-tunnel.sh
```

**脚本特点：**
- ✅ 步骤化引导
- ✅ 自动检查安装
- ✅ 自动创建配置
- ✅ 自动启动服务
- ✅ 显示访问地址

---

## 🎉 你现在有两个选择

### 选项 A：立即使用（推荐）

**继续使用当前的 localtunnel：**
```
前端: https://wechat-crawler-fwb.loca.lt
API:  https://wechat-crawler-api-fwb.loca.lt
```

这个已经可以正常使用了，而且是免费的。

### 选项 B：配置 Cloudflare Tunnel

**步骤：**
1. 手动下载并安装 cloudflared（参考方案 1/2/3）
2. 注册一个免费域名（可选，或使用 Cloudflare 免费域名）
3. 运行自动化脚本：
   ```bash
   ./setup-cloudflare-tunnel.sh
   ```

---

## ❓ 推荐方案

**短期使用（测试、临时）：**
- ✅ 使用当前的 localtunnel

**长期使用（生产、稳定）：**
- ✅ 注册一个免费域名
- ✅ 配置 Cloudflare Tunnel

---

## 📞 需要帮助吗？

告诉我想选哪个方案，我可以：
- 帮你手动配置 Cloudflare Tunnel 的每个步骤
- 或者优化当前的 localtunnel 配置
- 或者介绍其他内网穿透方案

---

**准备好继续了吗？告诉我你的选择！** 🚀
