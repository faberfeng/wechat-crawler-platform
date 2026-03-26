#!/bin/bash

echo "=========================================="
echo "  快速部署 - 使用 LocalTunnel"
echo "=========================================="

# 检查后端服务
if ! curl -s http://localhost:8002/health > /dev/null 2>&1; then
    echo "❌ 后端服务未运行"
    echo "请先启动后端："
    echo "  cd backend && python3 -m uvicorn app.main:app --host 0.0.0.0 --port 8002 --reload"
    exit 1
fi

echo "✓ 后端服务运行正常"

# 检查前端构建
if [ ! -d "frontend/dist" ]; then
    echo "❌ 前端未构建"
    echo "正在构建前端..."
    cd frontend && npm run build && cd ..
fi

echo "✓ 前端已构建"

# 创建日志目录
mkdir -p logs

# 启动前端服务器（后台）
echo ""
echo "正在启动前端服务器..."
cd frontend/dist
python3 -m http.server 5173 > ../../logs/frontend.log 2>&1 &
FRONTEND_PID=$!
cd ../..

sleep 2
echo "✓ 前端服务器已启动 (PID: $FRONTEND_PID)"

# 获取后端隧道 URL
echo ""
echo "正在启动后端 LocalTunnel..."
npx localtunnel --port 8002 --subdomain wechat-crawler-api-fwb > logs/backend-tunnel.log 2>&1 &
BACKEND_TUNNEL_PID=$!

sleep 5
BACKEND_URL=$(grep -o "https://.*\.loca\.lt" logs/backend-tunnel.log | head -1)
[ -z "$BACKEND_URL" ] && BACKEND_URL="https://wechat-crawler-api-fwb.loca.lt"

echo "✓ 后端 LocalTunnel: $BACKEND_URL"

# 获取前端隧道 URL
echo ""
echo "正在启动前端 LocalTunnel..."
npx localtunnel --port 5173 --subdomain wechat-crawler-fwb > logs/frontend-tunnel.log 2>&1 &
FRONTEND_TUNNEL_PID=$!

sleep 5
FRONTEND_URL=$(grep -o "https://.*\.loca\.lt" logs/frontend-tunnel.log | head -1)
[ -z "$FRONTEND_URL" ] && FRONTEND_URL="https://wechat-crawler-fwb.loca.lt"

echo "✓ 前端 LocalTunnel: $FRONTEND_URL"

# 保存 PID
echo "$FRONTEND_PID" > logs/pids.txt
echo "$FRONTEND_TUNNEL_PID" >> logs/pids.txt
echo "$BACKEND_TUNNEL_PID" >> logs/pids.txt

echo ""
echo "=========================================="
echo "  部署完成！"
echo "=========================================="
echo ""
echo "🎉 公网访问链接："
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
echo ""
echo "🔑 登录信息："
echo "  用户名: admin"
echo "  密码: admin123"
echo ""
echo ""
echo "⚠️  注意事项："
echo "  1. 链接可能在 LocalTunnel 重启后变化"
echo "  2. 建议保存当前链接"
echo "  3. 停止服务: kill \$(cat logs/pids.txt)"
echo ""
