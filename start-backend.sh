#!/bin/bash

# 简化版启动脚本（仅启动后端）

echo "========================================"
echo "  微信公众号抓取平台 - 后端"
echo "========================================"

PROJECT_DIR="$(cd "$(dirname "$0")" && pwd)"
cd "$PROJECT_DIR/backend"

# 检查 Python
if ! command -v python3 &> /dev/null; then
    echo "❌ 需要 Python 3.9+"
    exit 1
fi

echo "📦 安装依赖..."
pip3 install -q -r requirements.txt

echo "🚀 启动后端服务..."
uvicorn app.main:app --host 0.0.0.0 --port 8000 --reload
