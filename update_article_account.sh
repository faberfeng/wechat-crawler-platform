#!/bin/bash

# 获取 token
echo "正在获取登录 token..."
TOKEN=$(curl -s -X POST http://localhost:8002/api/v1/auth/login \
  -H "Content-Type: application/x-www-form-urlencoded" \
  -d "username=admin&password=admin123" | python3 -c "import sys, json; print(json.load(sys.stdin)['access_token'])")

echo "Token: ${TOKEN:0:20}..."

# 将文章关联到公众号
echo ""
echo "正在将文章关联到公众号..."
echo "文章 ID: 4"
echo "公众号 ID: 1"

RESPONSE=$(curl -s -X PATCH http://localhost:8002/api/v1/articles/4 \
  -H "Content-Type: application/json" \
  -H "Authorization: Bearer $TOKEN" \
  -d '{
    "account_id": 1
  }')

echo ""
echo "响应:"
echo "$RESPONSE" | python3 -m json.tool

