#!/bin/bash

echo "=========================================="
echo "  简化部署 - 自动分配隧道"
echo "=========================================="

# 检查后端
if ! curl -s http://localhost:8002/health > /dev/null 2>&1; then
    echo "❌ 后端服务未运行"
    exit 1
fi

echo "✓ 后端服务运行正常"

# 检查构建
if [ ! -d "frontend/dist" ]; then
    echo "正在构建前端..."
    cd frontend && npm run build && cd ..
fi

echo "✓ 前端已构建"

mkdir -p logs

# 停止旧服务
bash stop-all.sh >/dev/null 2>&1
sleep 2

# 启动前端服务器（使用 8080 端口避免冲突）
echo ""
echo "正在启动前端服务器（端口 8080）..."
cd frontend/dist
python3 -m http.server 8080 > ../../logs/frontend.log 2>&1 &
FRONTEND_PID=$!
cd ../..

sleep 2

if ! kill -0 $FRONTEND_PID 2>/dev/null; then
    echo "❌ 前端服务器启动失败"
    exit 1
fi

echo "✓ 前端服务器已启动 (PID: $FRONTEND_PID)"

# 启动后端隧道（不指定子域名）
echo ""
echo "正在启动后端 LocalTunnel..."
npx localtunnel --port 8002 > logs/backend-tunnel.log 2>&1 &
BACKEND_TUNNEL_PID=$!

sleep 8
BACKEND_URL=$(grep -o "https://.*\.loca\.lt" logs/backend-tunnel.log | head -1)

if [ -z "$BACKEND_URL" ]; then
    echo "❌ 后端隧道创建失败"
    tail -20 logs/backend-tunnel.log
    exit 1
fi

echo "✓ 后端 LocalTunnel: $BACKEND_URL"

# 启动前端隧道（不指定子域名）
echo ""
echo "正在启动前端 LocalTunnel..."
npx localtunnel --port 8080 > logs/frontend-tunnel.log 2>&1 &
FRONTEND_TUNNEL_PID=$!

sleep 8
FRONTEND_URL=$(grep -o "https://.*\.loca\.lt" logs/frontend-tunnel.log | head -1)

if [ -z "$FRONTEND_URL" ]; then
    echo "❌ 前端隧道创建失败"
    tail -20 logs/frontend-tunnel.log
    exit 1
fi

echo "✓ 前端 LocalTunnel: $FRONTEND_URL"

# 保存 PID
echo "$FRONTEND_PID" > logs/pids.txt
echo "$FRONTEND_TUNNEL_PID" >> logs/pids.txt
echo "$BACKEND_TUNNEL_PID" >> logs/pids.txt

# 创建访问信息文件
cat > DEPLOY_INFO.md << EOF
# 部署信息

**部署时间：** $(date)

## 🌐 公网访问链接

### 前端应用
**链接：** $FRONTEND_URL

### 后端 API
**链接：** $BACKEND_URL
**API 文档：** $BACKEND_URL/docs
**健康检查：** $BACKEND_URL/health

### 本地访问
- **后端：** http://localhost:8002
- **前端：** http://localhost:8080

## 🔑 登录信息

- **用户名：** admin
- **密码：** admin123

## ⚠️ 注意事项

1. 铂接只在当前终端会话有效，关闭会话后失效
2. 需要保持终端运行状态
3. 停止服务：bash stop-all.sh

## 📊 服务状态

- 前端服务器：PID $FRONTEND_PID，端口 8080
- 前端隧道：PID $FRONTEND_TUNNEL_PID
- 后端隧道：PID $BACKEND_TUNNEL_PID

---

生成时间：$(date)
EOF

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
echo "✓ 详细信息已保存到：DEPLOY_INFO.md"
echo ""
