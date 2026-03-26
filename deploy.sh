#!/bin/bash

echo "=========================================="
echo "  微信公众号抓取平台 - 部署脚本"
echo "=========================================="

# 检查是否安装了 localtunnel
if ! command -v npx &> /dev/null; then
    echo "❌ 未检测到 Node.js/npm，无法使用 LocalTunnel"
    exit 1
fi

echo ""
echo "[1] 检查服务状态..."

# 检查后端服务
if curl -s http://localhost:8002/health > /dev/null 2>&1; then
    echo "✓ 后端服务运行正常 (端口 8002)"
else
    echo "⚠ 后端服务未运行，请先启动后端服务"
    echo "   cd /Users/fengweibo/Desktop/wechat-crawler-platform/backend && python3 -m uvicorn app.main:app --host 0.0.0.0 --port 8002 --reload"
    exit 1
fi

# 检查前端文件
if [ -d "frontend/dist" ]; then
    echo "✓ 前端构建文件已存在"
else
    echo "⚠ 前端未构建，正在构建..."
    cd frontend && npm run build && cd ..
    echo "✓ 前端构建完成"
fi

echo ""
echo "[2] 启动 LocalTunnel..."

# 提示用户
echo ""
echo "=========================================="
echo " LocalTunnel 部署说明"
echo "=========================================="
echo ""
echo "将启动以下服务："
echo "  - 前端: 通过 LocalTunnel 暴露"
echo "  - 后端: 通过 LocalTunnel 暴露"
echo ""
echo "启动后将提供公网访问链接，请复制保存。"
echo ""
read -p "按回车键继续..."

# 创建临时目录
mkdir -p logs

# 启动前端代理（使用 Python 简单 HTTP 服务器）
echo ""
echo "正在启动前端服务器（端口 5173）..."
cd frontend/dist
python3 -m http.server 5173 > ../../logs/frontend-server.log 2>&1 &
FRONTEND_PID=$!
cd ../..

echo "✓ 前端服务器已启动 (PID: $FRONTEND_PID, 端口 5173)"

# 等待前端服务器启动
sleep 2

# 启动 LocalTunnel - 前端
echo ""
echo "正在创建前端 LocalTunnel..."
npx localtunnel --port 5173 --subdomain wechat-crawler-fwb > logs/frontend-tunnel.log 2>&1 &
FRONTEND_TUNNEL_PID=$!

# 等待隧道创建
sleep 5

# 获取前端 URL
FRONTEND_URL=$(grep -o "https://.*\.loca\.lt" logs/frontend-tunnel.log | head -1)

if [ -z "$FRONTEND_URL" ]; then
    FRONTEND_URL="https://wechat-crawler-fwb.loca.lt"
fi

echo "✓ 前端 LocalTunnel 已启动"
echo "  URL: $FRONTEND_URL"
echo "  PID: $FRONTEND_TUNNEL_PID"
echo ""

# 启动 LocalTunnel - 后端
echo "正在创建后端 LocalTunnel..."
npx localtunnel --port 8002 --subdomain wechat-crawler-api-fwb > logs/backend-tunnel.log 2>&1 &
BACKEND_TUNNEL_PID=$!

# 等待隧道创建
sleep 5

# 获取后端 URL
BACKEND_URL=$(grep -o "https://.*\.loca\.lt" logs/backend-tunnel.log | head -1)

if [ -z "$BACKEND_URL" ]; then
    BACKEND_URL="https://wechat-crawler-api-fwb.loca.lt"
fi

echo "✓ 后端 LocalTunnel 已启动"
echo "  URL: $BACKEND_URL"
echo "  PID: $BACKEND_TUNNEL_PID"
echo ""

# 保存 PID
echo "$FRONTEND_PID" > logs/frontend-server.pid
echo "$FRONTEND_TUNNEL_PID" > logs/frontend-tunnel.pid
echo "$BACKEND_TUNNEL_PID" > logs/backend-tunnel.pid

echo "=========================================="
echo "  部署完成！"
echo "=========================================="
echo ""
echo "📱 访问链接："
echo ""
echo "前端应用："
echo "  $FRONTEND_URL"
echo ""
echo "后端 API："
echo "  $BACKEND_URL"
echo ""
echo "API 文档："
echo "  $BACKEND_URL/docs"
echo ""
echo "健康检查："
echo "  $BACKEND_URL/health"
echo ""
echo "=========================================="
echo "  使用说明"
echo "=========================================="
echo ""
echo "1. 上面的链接可以在任何网络环境中访问"
echo "2. 使用账户 admin / admin123 登录"
echo "3. LocalTunnel 地址可能会变化，请保存当前链接"
echo "4. 如需停止服务，运行: ./stop-deploy.sh"
echo ""
echo "=========================================="
echo "  进程信息"
echo "=========================================="
echo ""
echo "前端服务器 PID: $FRONTEND_PID"
echo "前端隧道 PID: $FRONTEND_TUNNEL_PID"
echo "后端隧道 PID: $BACKEND_TUNNEL_PID"
echo ""
echo "日志文件："
echo "  logs/frontend-server.log"
echo "  logs/frontend-tunnel.log"
echo "  logs/backend-tunnel.log"
echo ""
