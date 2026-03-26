#!/bin/bash

# 获取 token
echo "正在获取登录 token..."
TOKEN=$(curl -s -X POST http://localhost:8002/api/v1/auth/login \
  -H "Content-Type: application/x-www-form-urlencoded" \
  -d "username=admin&password=admin123" | python3 -c "import sys, json; print(json.load(sys.stdin)['access_token'])")

echo "Token: ${TOKEN:0:20}..."

# 添加公众号 - 使用包含 biz 的 URL
echo ""
echo "正在添加公众号（上海静安）..."
echo "Biz: MzA5MzI3NjkyNA=="

# 构造一个包含 biz 的 URL（微信文章链接格式）
URL="https://mp.weixin.qq.com/s/ZKXjKURWMMStlij6OhUbiA?__biz=MzA5MzI3NjkyNA=="

RESPONSE=$(curl -s -X POST http://localhost:8002/api/v1/accounts \
  -H "Content-Type: application/json" \
  -H "Authorization: Bearer $TOKEN" \
  -d "{
    \"url\": \"$URL\",
    \"name\": \"上海静安\",
    \"is_active\": true
  }")

echo ""
echo "响应:"
echo "$RESPONSE" | python3 -m json.tool

