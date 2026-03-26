#!/bin/bash

# 端口配置
API_PORT=8002
API_BASE="http://localhost:${API_PORT}/api/v1"

echo "=========================================="
echo "  测试抓取功能 (端口: $API_PORT)"
echo "=========================================="

# 1. 登录获取 Token
echo ""
echo "[1] 登录获取 Token..."
LOGIN_RESPONSE=$(curl -s -X POST ${API_BASE}/auth/login \
  -H "Content-Type: application/x-www-form-urlencoded" \
  -d "username=admin&password=admin123")

TOKEN=$(echo $LOGIN_RESPONSE | python3 -c "import sys, json; print(json.load(sys.stdin).get('access_token', ''))")

if [ -z "$TOKEN" ]; then
  echo "❌ 登录失败"
  echo "响应: $LOGIN_RESPONSE"
  exit 1
fi

echo "✓ 登录成功"
echo "Token: ${TOKEN:0:50}..."

# 2. 测试通用URL抓取
echo ""
echo "[2] 测试通用URL抓取..."
TEST_URL="https://www.python.org/"

CRAWL_RESPONSE=$(curl -s -X POST ${API_BASE}/crawl/url \
  -H "Content-Type: application/json" \
  -H "Authorization: Bearer $TOKEN" \
  -d "{\"url\": \"$TEST_URL\"}")

echo "响应: $CRAWL_RESPONSE" | python3 -m json.tool

SUCCESS=$(echo $CRAWL_RESPONSE | python3 -c "import sys, json; print(json.load(sys.stdin).get('success', False))")

if [ "$SUCCESS" = "True" ]; then
  echo "✓ URL抓取成功"
else
  echo "⚠ URL抓取失败"
fi

# 3. 测试获取文章列表
echo ""
echo "[3] 测试获取文章列表..."
ARTICLES_RESPONSE=$(curl -s -X GET "${API_BASE}/articles?page=1&page_size=10" \
  -H "Authorization: Bearer $TOKEN")

echo "文章列表: $ARTICLES_RESPONSE" | python3 -m json.tool

# 4. 测试批量抓取
echo ""
echo "[4] 测试批量抓取..."
BATCH_RESPONSE=$(curl -s -X POST ${API_BASE}/crawl/batch \
  -H "Content-Type: application/json" \
  -H "Authorization: Bearer $TOKEN" \
  -d "{\"urls\": [\"https://docs.python.org/3/\"]}")

echo "批量抓取响应: $BATCH_RESPONSE" | python3 -m json.tool

echo ""
echo "=========================================="
echo "  测试完成"
echo "=========================================="
echo ""
echo "后端API地址: http://localhost:${API_PORT}"
echo "API文档地址: http://localhost:${API_PORT}/docs"
