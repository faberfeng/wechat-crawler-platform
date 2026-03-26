#!/bin/bash

# 获取 token
echo "正在获取登录 token..."
TOKEN=$(curl -s -X POST http://localhost:8002/api/v1/auth/login \
  -H "Content-Type: application/x-www-form-urlencoded" \
  -d "username=admin&password=admin123" | python3 -c "import sys, json; print(json.load(sys.stdin)['access_token'])")

echo "Token: ${TOKEN:0:20}..."

# 添加公众号
echo ""
echo "正在添加公众号..."
RESPONSE=$(curl -s -X POST http://localhost:8002/api/v1/accounts \
  -H "Content-Type: application/json" \
  -H "Authorization: Bearer $TOKEN" \
  -d '{
    "biz": "MzA5MzI3NjkyNA==",
    "name": "上海静安",
    "avatar_url": "https://mmbiz.qpic.cn/mmbiz_jpg/iabkFej6iaWfyyia1Wqwiad25u479nWXvnBFowgN9TBZUE7cgFBictzheBHnD7ASicPloWyZibKcq6Jp2FPFH4T0dMQPcLRZBAqbehrjqJoSmFKM20/0?wx_fmt=jpeg",
    "is_active": true
  }')

echo ""
echo "响应:"
echo "$RESPONSE" | python3 -m json.tool

