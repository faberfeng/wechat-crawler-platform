#!/bin/bash

# 文件管理功能测试脚本

API_BASE="http://localhost:8000"
ENDPOINT="$API_BASE/api/v1/files"

# 测试账号
EMAIL="admin@example.com"
PASSWORD="admin123"

echo "==========================================
文件管理功能测试
=========================================="

# 1. 登录获取 Token
echo ""
echo "[1/6] 登录获取 Token..."
LOGIN_RESPONSE=$(curl -s -X POST "$API_BASE/api/v1/auth/login" \
  -H "Content-Type: application/x-www-form-urlencoded" \
  -d "username=$EMAIL&password=$PASSWORD")

TOKEN=$(echo $LOGIN_RESPONSE | jq -r '.access_token')

if [ -z "$TOKEN" ] || [ "$TOKEN" == "null" ]; then
  echo "❌ 登录失败"
  exit 1
fi

echo "✅ 登录成功"
echo "Token: ${TOKEN:0:50}..."

# 2. 测试上传文件（创建一个测试文件）
echo ""
echo "[2/6] 测试上传文件..."

# 创建一个测试文件
TEST_FILE="/tmp/test_upload_$(date +%s).txt"
echo "This is a test file uploaded at $(date)" > $TEST_FILE

UPLOAD_RESPONSE=$(curl -s -X POST "$ENDPOINT/upload" \
  -H "Authorization: Bearer $TOKEN" \
  -F "file=@$TEST_FILE")

FILE_ID=$(echo $UPLOAD_RESPONSE | jq -r '.id')

if [ -z "$FILE_ID" ] || [ "$FILE_ID" == "null" ]; then
  echo "❌ 文件上传失败"
  echo "响应: $UPLOAD_RESPONSE"
  exit 1
fi

echo "✅ 文件上传成功"
echo "文件 ID: $FILE_ID"
echo "文件名: $(echo $UPLOAD_RESPONSE | jq -r '.filename')"
echo "文件大小: $(echo $UPLOAD_RESPONSE | jq -r '.file_size_formatted')"

# 3. 测试获取文件列表
echo ""
echo "[3/6] 测试获取文件列表..."

LIST_RESPONSE=$(curl -s -X GET "$ENDPOINT/" \
  -H "Authorization: Bearer $TOKEN")

FILE_COUNT=$(echo $LIST_RESPONSE | jq 'length')

echo "✅ 获取文件列表成功"
echo "文件总数: $FILE_COUNT"

if [ "$FILE_COUNT" -gt 0 ]; then
  echo "最新文件:"
  echo $LIST_RESPONSE | jq -r '.[0] | "  - ID: \(.id), 文件名: \(.original_filename), 大小: \(.file_size)"'
fi

# 4. 测试获取文件信息
echo ""
echo "[4/6] 测试获取文件信息..."

INFO_RESPONSE=$(curl -s -X GET "$ENDPOINT/$FILE_ID" \
  -H "Authorization: Bearer $TOKEN")

INFO_FILENAME=$(echo $INFO_RESPONSE | jq -r '.original_filename')

if [ -z "$INFO_FILENAME" ] || [ "$INFO_FILENAME" == "null" ]; then
  echo "❌ 获取文件信息失败"
  exit 1
fi

echo "✅ 获取文件信息成功"
echo "文件名: $INFO_FILENAME"
echo "MIME 类型: $(echo $INFO_RESPONSE | jq -r '.mime_type')"
echo "上传时间: $(echo $INFO_RESPONSE | jq -r '.uploaded_at')"

# 5. 测试获取文件统计信息
echo ""
echo "[5/6] 测试获取文件统计信息..."

STATS_RESPONSE=$(curl -s -X GET "$ENDPOINT/stats/summary" \
  -H "Authorization: Bearer $TOKEN")

TOTAL_COUNT=$(echo $STATS_RESPONSE | jq -r '.total_count')
TOTAL_SIZE=$(echo $STATS_RESPONSE | jq -r '.total_size_formatted')

if [ -z "$TOTAL_COUNT" ] || [ "$TOTAL_COUNT" == "null" ]; then
  echo "❌ 获取统计信息失败"
  exit 1
fi

echo "✅ 获取统计信息成功"
echo "总文件数: $TOTAL_COUNT"
echo "总大小: $TOTAL_SIZE"

# 6. 测试删除文件
echo ""
echo "[6/6] 测试删除文件..."

DELETE_RESPONSE=$(curl -s -X DELETE "$ENDPOINT/$FILE_ID" \
  -H "Authorization: Bearer $TOKEN")

DELETE_MESSAGE=$(echo $DELETE_RESPONSE | jq -r '.message')

if [ "$DELETE_MESSAGE" != "文件删除成功" ]; then
  echo "❌ 文件删除失败"
  echo "响应: $DELETE_RESPONSE"
  exit 1
fi

echo "✅ 文件删除成功"

# 清理测试文件
rm -f $TEST_FILE

echo ""
echo "==========================================
✅ 所有测试通过！
=========================================="
echo ""
echo "文件管理功能已就绪"
echo "API 文档: http://localhost:8000/docs"
