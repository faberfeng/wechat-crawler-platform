#!/bin/bash

# 微信爬虫平台 - 重启服务测试脚本

echo "=========================================="
echo "   微信爬虫平台 - 服务重启测试"
echo "=========================================="
echo

# 1. 停止旧服务
echo "1. 停止旧服务..."
pkill -f "python3 -m uvicorn" 2>/dev/null
pkill -f "python3 -m http.server" 2>/dev/null
pkill -f "node.*lt.*--port" 2>/dev/null

sleep 2

# 2. 启动后端服务
echo "2. 启动后端服务..."
cd /Users/fengweibo/Desktop/wechat-crawler-platform/backend
nohup python3 -m uvicorn app.main:app --host 0.0.0.0 --port 8000 > ../logs/backend-restart.log 2>&1 &
BACKEND_PID=$!
echo "   后端 PID: $BACKEND_PID"

sleep 3

# 检查后端服务
if curl -s http://localhost:8000/health > /dev/null; then
  echo "   ✅ 后端服务启动成功"
else
  echo "   ❌ 后端服务启动失败"
  cat ../logs/backend-restart.log
  exit 1
fi

# 3. 重建前端
echo "3. 重建前端..."
cd ../frontend
npm run build

if [ $? -eq 0 ]; then
  echo "   ✅ 前端构建成功"
else
  echo "   ❌ 前端构建失败"
  exit 1
fi

# 4. 启动前端服务
echo "4. 启动前端服务..."
cd dist
nohup python3 -m http.server 5174 > ../../logs/frontend-restart.log 2>&1 &
FRONTEND_PID=$!
echo "   前端 PID: $FRONTEND_PID"

sleep 2

if curl -s http://localhost:5174 > /dev/null; then
  echo "   ✅ 前端服务启动成功"
else
  echo "   ❌ 前端服务启动失败"
  cat ../../logs/frontend-restart.log
  exit 1
fi

# 5. 显示服务状态
echo
echo "=========================================="
echo "   服务启动完成"
echo "=========================================="
echo
echo "后端 API:"
echo "  本地: http://localhost:8000"
echo "  公网: https://wechat-crawler-api-fwb.loca.lt"
echo "  文档: http://localhost:8000/docs"
echo
echo "前端界面:"
echo "  本地: http://localhost:5174"
echo "  公网: https://fwb-wechat.loca.lt"
echo
echo "测试账号:"
echo "  管理员：admin"
echo "  邮箱：admin@example.com"
echo "  密码：admin123"
echo
echo "=========================================="

# 检查隧道进程
if pgrep -f "lt.*--port 5174" > /dev/null; then
  echo "✅ 前端隧道运行中"
else
  echo "⚠️ 前端隧道未运行，请手动启动："
  echo "   lt --port 5174 --subdomain wechat-fwb"
fi

if pgrep -f "lt.*--port 8000" > /dev/null; then
  echo "✅ API 隧道运行中"
else
  echo "⚠️ API 隧道未运行，请手动启动："
  echo "   lt --port 8000 --subdomain wechat-api"
fi

echo
echo "✅ 所有服务就绪！"
echo
