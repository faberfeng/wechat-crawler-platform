#!/bin/bash

# 端口配置
API_PORT=8002
API_BASE="http://localhost:${API_PORT}/api/v1"

echo "=========================================="
echo "  全面测试抓取功能"
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
  exit 1
fi

echo "✓ 登录成功"

# 2. 测试单个URL抓取
echo ""
echo "[2] 测试单个URL抓取..."
TEST_URL="https://docs.python.org/3/"

CRAWL_RESPONSE=$(curl -s -X POST ${API_BASE}/crawl/url \
  -H "Content-Type: application/json" \
  -H "Authorization: Bearer $TOKEN" \
  -d "{\"url\": \"$TEST_URL\"}")

SUCCESS=$(echo $CRAWL_RESPONSE | python3 -c "import sys, json; print(json.load(sys.stdin).get('success', False))")
ARTICLE_ID=$(echo $CRAWL_RESPONSE | python3 -c "import sys, json; print(json.load(sys.stdin).get('article', {}).get('id', 0))")

if [ "$SUCCESS" = "True" ]; then
  echo "✓ URL抓取成功，文章ID: $ARTICLE_ID"
  TITLE=$(echo $CRAWL_RESPONSE | python3 -c "import sys, json; print(json.load(sys.stdin).get('article', {}).get('title', ''))")
  echo "  标题: $TITLE"
  HAS_MARKDOWN=$(echo $CRAWL_RESPONSE | python3 -c "import sys, json; print(json.load(sys.stdin).get('article', {}).get('has_markdown', False))")
  echo "  Markdown: $HAS_MARKDOWN"
else
  echo "⚠ URL抓取失败"
  echo $CRAWL_RESPONSE
fi

# 3. 测试批量抓取
echo ""
echo "[3] 测试批量抓取..."

BATCH_RESPONSE=$(curl -s -X POST ${API_BASE}/crawl/batch \
  -H "Content-Type: application/json" \
  -H "Authorization: Bearer $TOKEN" \
  -d "{\"urls\": [\"https://community.python.org/\"]}")

BATCH_SUCCESS=$(echo $BATCH_RESPONSE | python3 -c "import sys, json; print(json.load(sys.stdin).get('success', False))")
TOTAL=$(echo $BATCH_RESPONSE | python3 -c "import sys, json; print(json.load(sys.stdin).get('summary', {}).get('total', 0))")

if [ "$BATCH_SUCCESS" = "True" ]; then
  echo "✓ 批量抓取完成，总URL数: $TOTAL"
else
  echo "⚠ 批量抓取失败"
  echo $BATCH_RESPONSE
fi

# 4. 测试获取文章列表
echo ""
echo "[4] 测试获取文章列表..."
sleep 1  # 等待一下让数据库更新

ARTICLES_RESPONSE=$(curl -s -X GET "${API_BASE}/articles?page=1&page_size=10" \
  -H "Authorization: Bearer $TOKEN")

TOTAL_ARTICLES=$(echo $ARTICLES_RESPONSE | python3 -c "import sys, json; print(json.load(sys.stdin).get('total', 0))")

if [ "$TOTAL_ARTICLES" -gt 0 ]; then
  echo "✓ 文章列表获取成功，总文章数: $TOTAL_ARTICLES"
else
  echo "⚠ 文章列表为空"
fi

# 5. 测试获取文章Markdown内容
if [ "$ARTICLE_ID" != "0" ]; then
  echo ""
  echo "[5] 测试获取文章Markdown内容..."

  MARKDOWN_RESPONSE=$(curl -s -X GET "${API_BASE}/articles/${ARTICLE_ID}/markdown" \
    -H "Authorization: Bearer $TOKEN")

  MARKDOWN_SUCCESS=$(echo $MARKDOWN_RESPONSE | python3 -c "import sys, json; print(json.load(sys.stdin).get('success', False))")

  if [ "$MARKDOWN_SUCCESS" = "True" ]; then
    CONTENT_LENGTH=$(echo $MARKDOWN_RESPONSE | python3 -c "import sys, json; print(len(json.load(sys.stdin).get('content', '')))")
    echo "✓ Markdown内容获取成功，内容长度: $CONTENT_LENGTH 字符"
  else
    echo "⚠ Markdown内容获取失败"
  fi
fi

# 6. 测试获取统计数据
echo ""
echo "[6] 测试获取统计数据..."

STATS_RESPONSE=$(curl -s -X GET "${API_BASE}/articles/stats/summary" \
  -H "Authorization: Bearer $TOKEN")

echo $STATS_RESPONSE | python3 -m json.tool

# 总结
echo ""
echo "=========================================="
echo "  测试完成"
echo "=========================================="
echo ""
echo "后端API地址: http://localhost:${API_PORT}"
echo "API文档地址: http://localhost:${API_PORT}/docs"
echo ""
echo "可用功能："
echo "  ✓ 单个URL抓取"
echo "  ✓ 批量URL抓取"
echo "  ✓ 文章列表查询"
echo "  ✓ 文章Markdown内容获取"
echo "  ✓ 统计数据"
