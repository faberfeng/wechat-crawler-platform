#!/bin/bash

# 测试认证 API

echo "=========================================="
echo "   测试认证 API"
echo "=========================================="
echo

BASE_URL="http://localhost:8000/api/v1"

# 1. 测试注册新用户
echo "1. 测试注册新用户..."
REGISTER_RESPONSE=$(curl -s -X POST "$BASE_URL/auth/register" \
  -H "Content-Type: application/json" \
  -d '{
    "username": "testuser123",
    "email": "testuser123@example.com",
    "password": "password123"
  }')

echo "$REGISTER_RESPONSE" | python3 -m json.tool 2>/dev/null || echo "$REGISTER_RESPONSE"
echo

# 2. 测试登录
echo "2. 测试登录..."
echo "   使用测试账号登录：testuser123@example.com / password123"

LOGIN_RESPONSE=$(curl -s -X POST "$BASE_URL/auth/login" \
  -H "Content-Type: application/x-www-form-urlencoded" \
  -d "username=testuser123@example.com&password=password123")

TOKEN=$(echo "$LOGIN_RESPONSE" | python3 -c "import sys, json; print(json.load(sys.stdin)['access_token'])" 2>/dev/null)

echo "$LOGIN_RESPONSE" | python3 -m json.tool 2>/dev/null || echo "$LOGIN_RESPONSE"
echo

if [ -z "$TOKEN" ]; then
  echo "❌ 登录失败，无法获取 token"
  exit 1
fi

echo "✅ 登录成功！"
echo "   Token: ${TOKEN:0:50}..."
echo

# 3. 测试获取当前用户信息
echo "3. 测试获取当前用户信息..."
USER_RESPONSE=$(curl -s -X GET "$BASE_URL/auth/me" \
  -H "Authorization: Bearer $TOKEN")

echo "$USER_RESPONSE" | python3 -m json.tool 2>/dev/null || echo "$USER_RESPONSE"
echo

# 4. 测试管理员账号登录
echo "4. 测试管理员账号登录：admin / admin@example.com / admin123"
echo

ADMIN_LOGIN_RESPONSE=$(curl -s -X POST "$BASE_URL/auth/login" \
  -H "Content-Type: application/x-www-form-urlencoded" \
  -d "username=admin@example.com&password=admin123")

ADMIN_TOKEN=$(echo "$ADMIN_LOGIN_RESPONSE" | python3 -c "import sys, json; print(json.load(sys.stdin)['access_token'])" 2>/dev/null)

echo "$ADMIN_LOGIN_RESPONSE" | python3 -m json.tool 2>/dev/null || echo "$ADMIN_LOGIN_RESPONSE"
echo

if [ -z "$ADMIN_TOKEN" ]; then
  echo "⚠️ 管理员登录失败（可能是密码哈希未正确配置）"
else
  echo "✅ 管理员登录成功！"
  echo "   Token: ${ADMIN_TOKEN:0:50}..."
fi
echo

# 5. 测试用户列表（需要管理员权限）
if [ -n "$ADMIN_TOKEN" ]; then
  echo "5. 测试获取用户列表（管理员功能）..."
  USERS_RESPONSE=$(curl -s -X GET "$BASE_URL/users" \
    -H "Authorization: Bearer $ADMIN_TOKEN")

  echo "$USERS_RESPONSE" | python3 -m json.tool 2>/dev/null || echo "$USERS_RESPONSE"
  echo
else
  echo "5. 跳过用户列表测试（管理员未登录）"
fi

echo "=========================================="
echo "   测试完成"
echo "=========================================="
