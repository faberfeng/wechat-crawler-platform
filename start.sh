#!/bin/bash

# 微信公众号抓取平台启动脚本

echo "========================================"
echo "  微信公众号抓取平台"
echo "========================================"
echo ""

PROJECT_DIR="$(cd "$(dirname "$0")" && pwd)"
cd "$PROJECT_DIR"

# 检查 Python
if ! command -v python3 &> /dev/null; then
    echo "❌ 错误: 未找到 Python 3"
    echo "请先安装 Python 3.9 或更高版本"
    exit 1
fi

# 检查 Node.js
if ! command -v node &> /dev/null; then
    echo "❌ 错误: 未找到 Node.js"
    echo "请先安装 Node.js 16 或更高版本"
    exit 1
fi

echo "📍 项目目录: $PROJECT_DIR"
echo ""

# 安装后端依赖
echo "📦 安装后端依赖..."
cd backend
pip3 install -r requirements.txt
cd ..

# 安装前端依赖
echo "📦 安装前端依赖..."
cd frontend
npm install
cd ..

# 启动后端
echo ""
echo "🚀 启动后端服务..."
cd backend
uvicorn app.main:app --host 0.0.0.0 --port 8000 --reload &
BACKEND_PID=$!
cd ..

echo "✅ 后端已启动 (PID: $BACKEND_PID)"
echo "   API 地址: http://localhost:8000"
echo "   API 文档: http://localhost:8000/docs"
echo ""

# 等待后端启动
sleep 3

# 启动前端
echo "🚀 启动前端服务..."
cd frontend
npm run dev &
FRONTEND_PID=$!
cd ..

echo "✅ 前端已启动 (PID: $FRONTEND_PID)"
echo "   访问地址: http://localhost:5173"
echo ""

echo "========================================"
echo "🎉 服务已全部启动！"
echo "========================================"
echo ""
echo "📝 使用说明:"
echo "  1. 打开浏览器访问: http://localhost:5173"
echo "  2. 添加公众号（输入文章链接）"
echo "  3. 系统自动抓取文章"
echo "  4. 查看和管理文章"
echo ""
echo "按 Ctrl+C 停止服务"
echo ""

# 等待信号
trap "echo ''; echo '🛑 正在停止服务...'; kill $BACKEND_PID $FRONTEND_PID; echo '✅ 服务已停止'; exit 0" INT TERM

wait
