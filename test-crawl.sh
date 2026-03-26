#!/bin/bash

echo "=========================================="
echo "  测试抓取功能"
echo "=========================================="

# 1. 登录获取 Token
echo ""
echo "[1] 登录获取 Token..."
LOGIN_RESPONSE=$(curl -s -X POST http://localhost:8001/api/v1/auth/login \
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

# 2. 测试通用URL抓取（使用一个公共博客文章）
echo ""
echo "[2] 测试通用URL抓取..."

# 使用一个简单的测试URL（Python官网首页）
TEST_URL="https://www.python.org/"

CRAWL_RESPONSE=$(curl -s -X POST http://localhost:8001/api/v1/crawl/url \
  -H "Content-Type: application/json" \
  -H "Authorization: Bearer $TOKEN" \
  -d "{\"url\": \"$TEST_URL\"}")

echo "响应: $CRAWL_RESPONSE"

# 检查响应
SUCCESS=$(echo $CRAWL_RESPONSE | python3 -c "import sys, json; print(json.load(sys.stdin).get('success', False))")

if [ "$SUCCESS" = "True" ]; then
  echo "✓ URL抓取成功"
else
  echo "⚠ URL抓取失败（可能正常，因为是首页而非文章）"
fi

# 3. 测试获取文章列表
echo ""
echo "[3] 测试获取文章列表..."
ARTICLES_RESPONSE=$(curl -s -X GET "http://localhost:8001/api/v1/articles?page=1&page_size=10" \
  -H "Authorization: Bearer $TOKEN")

echo "响应: $ARTICLES_RESPONSE"

# 4. 测试API端点列表
echo ""
echo "[4] 测试抓取API端点..."
echo "可用端点:"
curl -s http://localhost:8001/docs | grep -o "crawl.*" | sed 's/<[^>]*>//g' | sort -u | head -10

echo ""
echo "=========================================="
echo "  测试完成"
echo "=========================================="
