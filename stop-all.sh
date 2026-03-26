#!/bin/bash

echo "=========================================="
echo "  停止部署服务"
echo "=========================================="

# 杀死所有相关进程
if [ -f "logs/pids.txt" ]; then
    PIDS=$(cat logs/pids.txt)
    for PID in $PIDS; do
        if kill -0 $PID 2>/dev/null; then
            echo "✓ 停止进程 $PID"
            kill $PID
        fi
    done
    rm -f logs/pids.txt
fi

# 额外清理：杀死可能残留的进程
pkill -f "python3 -m http.server" 2>/dev/null
pkill -f "localtunnel" 2>/dev/null

echo ""
echo "✓ 所有服务已停止"
