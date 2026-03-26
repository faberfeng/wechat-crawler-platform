#!/bin/bash

echo "=========================================="
echo "  停止部署服务"
echo "=========================================="

# 停止前端服务器
if [ -f "logs/frontend-server.pid" ]; then
    FRONTEND_PID=$(cat logs/frontend-server.pid)
    if kill -0 $FRONTEND_PID 2>/dev/null; then
        kill $FRONTEND_PID
        echo "✓ 前端服务器已停止 (PID: $FRONTEND_PID)"
    fi
    rm -f logs/frontend-server.pid
fi

# 停止前端隧道
if [ -f "logs/frontend-tunnel.pid" ]; then
    FRONTEND_TUNNEL_PID=$(cat logs/frontend-tunnel.pid)
    if kill -0 $FRONTEND_TUNNEL_PID 2>/dev/null; then
        kill $FRONTEND_TUNNEL_PID
        echo "✓ 前端 LocalTunnel 已停止 (PID: $FRONTEND_TUNNEL_PID)"
    fi
    rm -f logs/frontend-tunnel.pid
fi

# 停止后端隧道
if [ -f "logs/backend-tunnel.pid" ]; then
    BACKEND_TUNNEL_PID=$(cat logs/backend-tunnel.pid)
    if kill -0 $BACKEND_TUNNEL_PID 2>/dev/null; then
        kill $BACKEND_TUNNEL_PID
        echo "✓ 后端 LocalTunnel 已停止 (PID: $BACKEND_TUNNEL_PID)"
    fi
    rm -f logs/backend-tunnel.pid
fi

echo ""
echo "=========================================="
echo "  所有服务已停止"
echo "=========================================="
