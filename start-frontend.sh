#!/bin/bash

# 简化版启动脚本（仅启动前端）

echo "========================================"
echo "  微信公众号抓取平台 - 前端"
echo "========================================"

PROJECT_DIR="$(cd "$(dirname "$0")" && pwd)"
cd "$PROJECT_DIR/frontend"

# 检查 Node.js
if ! command -v node &> /dev/null; then
    echo "❌ 需要 Node.js 16+"
    exit 1
fi

echo "📦 安装依赖..."
npm install

echo "🚀 启动前端服务..."
npm run dev
