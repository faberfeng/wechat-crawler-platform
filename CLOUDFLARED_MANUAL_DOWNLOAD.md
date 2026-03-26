# cloudflared 手动下载指南

## ❌ 网络问题

尝试了多个国内镜像，都无法成功下载 cloudflared：
- ghproxy.com ❌ 超时
- moeyy.cn ❌ 返回错误内容
- gh.api.99988866.xyz ❌ SSL 错误
- gitclone.com ❌ 连接失败

---

## 🎯 解决方案

### 方案 1：浏览器手动下载（推荐）

**步骤：**

1. **在浏览器中打开以下网址（如果可以访问）：**

   - 官方地址：
     ```
     https://github.com/cloudflare/cloudflared/releases/download/2024.3.1/cloudflared-darwin-amd64.tar.gz
     ```

   - 或访问发布页选择最新版本：
     ```
     https://github.com/cloudflare/cloudflared/releases
     ```

2. **下载 `cloudflared-darwin-amd64.tar.gz`** 文件

3. **保存到下载文件夹**（`~/Downloads/`）

4. **执行以下命令完成安装**：

   ```bash
   # 进入下载目录
   cd ~/Downloads

   # 解压
   tar xzf cloudflared-darwin-amd64.tar.gz

   # 移动到系统目录
   sudo mv cloudflared /usr/local/bin/

   # 添加执行权限
   chmod +x /usr/local/bin/cloudflared

   # 验证安装
   cloudflared --version
   ```

5. **如果看到版本信息，说明安装成功！**

---

### 方案 2：使用代理下载

如果你有代理：

```bash
# 使用代理下载
export https_proxy=http://127.0.0.1:7890  # 改成你的代理端口
curl -L https://github.com/cloudflare/cloudflared/releases/download/2024.3.1/cloudflared-darwin-amd64.tar.gz -o /tmp/cloudflared.tar.gz

# 解压并安装
cd /tmp && tar xzf cloudflared.tar.gz
sudo mv cloudflared /usr/local/bin/
chmod +x /usr/local/bin/cloudflared
```

---

### 方案 3：从其他设备下载

如果你有其他设备可以访问 GitHub：

1. 在其他设备下载 `cloudflared-darwin-amd64.tar.gz`
2. 通过网盘、邮件、AirDrop 等方式传到你的 Mac
3. 执行：
   ```bash
   cd ~/Downloads
   tar xzf cloudflared-darwin-amd64.tar.gz
   sudo mv cloudflared /usr/local/bin/
   chmod +x /usr/local/bin/cloudflared
   ```

---

### 方案 4：继续使用 localtunnel（立即可用）

如果上面所有方法都行不通，你可以继续使用已经配置好的 localtunnel：

**地址：**
- 前端：https://wechat-crawler-fwb.loca.lt
- API：https://wechat-crawler-api-fwb.loca.lt

**这个方案已经可以正常使用，满足你的访问需求！**

---

## ✅ 安装完成后

安装成功后，告诉我，我会继续帮你配置 Cloudflare Tunnel：

```bash
# 验证安装
cloudflared --version

# 登录 Cloudflare
cloudflared tunnel login

# 运行配置脚本
cd /Users/fengweibo/Desktop/wechat-crawler-platform
./setup-cloudflare-tunnel.sh
```

---

## 📞 告诉我你的选择

请告诉我：

1. 你是否可以通过浏览器手动下载并安装？
   - 如果是，安装完成后告诉我

2. 或者继续使用 localtunnel？
   - 这是当前已经配置好并可用的方案

3. 或者有其他方式可以访问 GitHub？
   - 比如有代理、VPN、其他设备等

---

**等你回复后，我会继续下一步！** 🚀
