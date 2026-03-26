#!/bin/bash
# Cloudflare Tunnel 安装助手脚本
# 注意：需要在浏览器中完成授权

set -e

echo "========================================="
echo "   Cloudflare Tunnel 安装助手"
echo "========================================="
echo ""

# 检查是否安装了 cloudflared
if command -v cloudflared &> /dev/null; then
    echo "✅ cloudflared 已经安装"
    cloudflared --version
else
    echo "❌ cloudflared 未安装"
    echo ""
    echo "请手动安装 cloudflared："
    echo ""
    echo "方法 1: 使用 Homebrew（推荐，需要网络访问 GitHub）"
    echo "  brew install cloudflare/cloudflare/cloudflared"
    echo ""
    echo "方法 2: 手动下载"
    echo "  1. 访问: https://github.com/cloudflare/cloudflared/releases"
    echo "  2. 下载: cloudflared-darwin-amd64.tar.gz"
    echo "  3. 解压到: /usr/local/bin/cloudflared"
    echo ""
    echo "方法 3: 使用国内镜像"
    echo "  curl -L https://ghproxy.com/https://github.com/cloudflare/cloudflared/releases/latest/download/cloudflared-darwin-amd64.tar.gz -o cloudflared.tar.gz"
    echo "  tar xzf cloudflared.tar.gz"
    echo "  sudo mv cloudflared /usr/local/bin/"
    echo "  chmod +x /usr/local/bin/cloudflared"
    echo ""
    read -p "安装完成后按回车继续..."
fi

echo ""
echo "========================================="
echo "   第一步：登录 Cloudflare"
echo "========================================="
echo ""
echo "即将执行: cloudflared tunnel login"
echo ""
echo "这将："
echo "  1. 打开默认浏览器"
echo "  2. 需要你登录 Cloudflare"
echo "  3. 选择授权的域名（如果你有域名）"
echo "  4. 点击 Authorize 授权"
echo ""
read -p "准备好了吗？按回车继续..."

echo ""
echo "正在登录..."
if cloudflared tunnel login 2>&1 | tee /tmp/cloudflared-login.log; then
    echo ""
    echo "✅ 登录成功！"
else
    echo ""
    echo "❌ 登录失败，请查看日志: /tmp/cloudflared-login.log"
    exit 1
fi

echo ""
echo "========================================="
echo "   第二步：创建隧道"
echo "========================================="
echo ""

TUNNEL_NAME="${1:-wechat-crawler}"
echo "隧道名称: $TUNNEL_NAME"
echo ""

echo "正在创建隧道..."
TUNNEL_OUTPUT=$(cloudflared tunnel create "$TUNNEL_NAME" 2>&1 | tee /tmp/cloudflared-create.log)

echo "$TUNNEL_OUTPUT"

# 提取 Tunnel ID
TUNNEL_ID=$(echo "$TUNNEL_OUTPUT" | grep -oE '[a-f0-9]{8}-[a-f0-9]{4}-[a-f0-9]{4}-[a-f0-9]{4}-[a-f0-9]{12}' | head -1)

if [ -z "$TUNNEL_ID" ]; then
    echo "❌ 无法提取 Tunnel ID"
    exit 1
fi

echo ""
echo "✅ 隧道创建成功！"
echo ""
echo "Tunnel ID: $TUNNEL_ID"
echo ""

# 检查证书文件
CERT_FILE="$HOME/.cloudflared/${TUNNEL_ID}.json"
if [ ! -f "$CERT_FILE" ]; then
    echo "❌ 证书文件不存在: $CERT_FILE"
    exit 1
fi

echo ""
echo "========================================="
echo "   第三步：配置服务映射"
echo "========================================="
echo ""

CONFIG_FILE="$HOME/.cloudflared/config.yml"

echo "正在创建配置文件: $CONFIG_FILE"
echo ""

cat > "$CONFIG_FILE" << EOF
tunnel: $TUNNEL_ID
credentials-file: $CERT_FILE

ingress:
  # 前端服务
  - hostname: \${FRONTEND_HOSTNAME}
    service: http://localhost:5174

  # 后端 API
  - hostname: \${API_HOSTNAME}
    service: http://localhost:8000

  # 默认路由（放在最后）
  - service: http_status:404
EOF

echo "✅ 配置文件创建成功"
echo ""
echo "配置文件内容:"
cat "$CONFIG_FILE"
echo ""

echo ""
echo "========================================="
echo "   第四步：添加 DNS 记录"
echo "========================================="
echo ""
echo "请手动在 Cloudflare Dashboard 添加 DNS 记录："
echo ""
echo "1. 访问: https://dash.cloudflare.com"
echo "2. 选择你的域名"
echo "3. 进入 DNS → Records"
echo "4. 点击 Add record"
echo ""
echo "=== 前端 DNS 记录 ==="
echo "  Type: CNAME"
echo "  Name: [填写你的前端子域名，如: wechat]"
echo "  Target: [填写 Tunnel 显示的域名]"
echo "  Proxy: Proxied (橙色云朵)"
echo ""
echo "=== API DNS 记录 ==="
echo "  Type: CNAME"
echo "  Name: [填写你的 API 子域名，如: api]"
echo "  Target: [填写 Tunnel 显示的域名]"
echo "  Proxy: Proxied (橙色云朵)"
echo ""

# 显示 Tunnel 信息
echo ""
echo "========================================="
echo "   隧道信息"
echo "========================================="
echo ""
cloudflared tunnel info "$TUNNEL_NAME" | tee /tmp/cloudflared-info.log

# 提取 Tunnle 域名
TUNNEL_DOMAIN=$(grep -oE '[a-z0-9]+\.channels\.cloudflare\.net' /tmp/cloudflared-info.log | head -1)

if [ -n "$TUNNEL_DOMAIN" ]; then
    echo ""
    echo "Tunnel 域名: $TUNNEL_DOMAIN"
    echo ""
    echo "请使用以下信息配置 DNS："
    echo ""
    echo "=== 前端 DNS ==="
    echo "  Name: your-frontend-name"
    echo "  Target: $TUNNEL_DOMAIN"
    echo ""
    echo "=== API DNS ==="
    echo "  Name: your-api-name"
    echo "  Target: $TUNNEL_DOMAIN"
    echo ""
fi

echo ""
read -p "DNS 记录添加完成后，按回车继续..."

echo ""
echo "========================================="
echo "   第五步：更新配置文件"
echo "========================================="
echo ""

read -p "请输入前端域名（如: wechat.yourdomain.com）: " FRONTEND_HOSTNAME
read -p "请输入 API 域名（如: api.yourdomain.com）: " API_HOSTNAME

# 更新配置文件
cat > "$CONFIG_FILE" << EOF
tunnel: $TUNNEL_ID
credentials-file: $CERT_FILE

ingress:
  # 前端服务
  - hostname: $FRONTEND_HOSTNAME
    service: http://localhost:5174

  # 后端 API
  - hostname: $API_HOSTNAME
    service: http://localhost:8000

  # 默认路由
  - service: http_status:404
EOF

echo ""
echo "✅ 配置文件已更新"
echo ""
echo "配置文件内容:"
cat "$CONFIG_FILE"
echo ""

echo ""
echo "========================================="
echo "   第六步：启动隧道"
echo "========================================="
echo ""

read -p "准备好启动隧道了吗？按回车继续..."

echo ""
echo "正在启动隧道..."
nohup cloudflared tunnel --config "$CONFIG_FILE" run "$TUNNEL_NAME" > /tmp/cloudflared.log 2>&1 &
TUNNEL_PID=$!

sleep 3

if ps -p $TUNNEL_PID > /dev/null; then
    echo ""
    echo "✅ 隧道启动成功！"
    echo ""
    echo "进程 ID: $TUNNEL_PID"
    echo "日志文件: /tmp/cloudflared.log"
    echo ""

    # 检查日志
    if grep -q "ip update successful" /tmp/cloudflared.log 2>/dev/null || grep -q "Connected" /tmp/cloudflared.log 2>/dev/null; then
        echo "========================================="
        echo "   🎉 部署完成！"
        echo "========================================="
        echo ""
        echo "前端访问地址:"
        echo "  https://$FRONTEND_HOSTNAME"
        echo ""
        echo "API 访问地址:"
        echo "  https://$API_HOSTNAME/api/v1"
        echo ""
        echo "查看日志:"
        echo "  tail -f /tmp/cloudflared.log"
        echo ""
    else
        echo "⚠️隧道可能未完全启动，请查看日志:"
        echo "  tail -f /tmp/cloudflared.log"
    fi
else
    echo ""
    echo "❌ 隧道启动失败，请查看日志: /tmp/cloudflared.log"
    exit 1
fi

echo ""
echo "========================================="
echo "   后续步骤"
echo "========================================="
echo ""
echo "1. 更新前端 API 配置 (frontend/src/api/index.js):"
echo "   baseURL: 'https://$API_HOSTNAME/api/v1'"
echo ""
echo "2. 更新后端 CORS 配置 (backend/app/core/config.py):"
echo "   CORS_ORIGINS: str = 'https://$FRONTEND_HOSTNAME,https://$API_HOSTNAME'"
echo ""
echo "3. 重启后端服务"
echo ""
echo "========================================="
