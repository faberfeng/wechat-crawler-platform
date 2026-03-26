#!/bin/bash

# 测试认证功能脚本

BASE_URL="http://localhost:8001"
API_URL="$BASE_URL/api/v1"

echo "========================================="
echo "  测试认证功能"
echo "========================================="
echo ""

# 测试 1: 使用 admin 账户登录
echo "[1] 测试 Admin 账户登录"
echo "账户: admin / admin123"

LOGIN_DATA="username=admin&password=admin123"

LOGIN_RESPONSE=$(curl -s -X POST \
  -H "Content-Type: application/x-www-form-urlencoded" \
  -d "$LOGIN_DATA" \
  "$API_URL/auth/login")

echo "登录响应: $LOGIN_RESPONSE"

if echo "$LOGIN_RESPONSE" | grep -q "access_token"; then
    echo "✓ Admin 登录成功!"
    TOKEN=$(echo "$LOGIN_RESPONSE" | python3 -c "import sys, json; print(json.load(sys.stdin).get('access_token', ''))" 2>/dev/null)
    echo "Token: ${TOKEN:0:50}..."
else
    echo "✗ Admin 登录失败"
fi
echo ""

# 测试 2: 使用 testuser 账户登录
echo "[2] 测试 Test User 账户登录"
echo "账户: testuser / Test123456"

LOGIN_DATA2="username=testuser&password=Test123456"

LOGIN_RESPONSE2=$(curl -s -X POST \
  -H "Content-Type: application/x-www-form-urlencoded" \
  -d "$LOGIN_DATA2" \
  "$API_URL/auth/login")

echo "登录响应: $LOGIN_RESPONSE2"

if echo "$LOGIN_RESPONSE2" | grep -q "access_token"; then
    echo "✓ Test User 登录成功!"
else
    echo "✗ Test User 登录失败"
fi
echo ""

# 测试 3: 使用 demo 账户登录
echo "[3] 测试 Demo 账户登录"
echo "账户: demo / Demo123456"

LOGIN_DATA3="username=demo&password=Demo123456"

LOGIN_RESPONSE3=$(curl -s -X POST \
  -H "Content-Type: application/x-www-form-urlencoded" \
  -d "$LOGIN_DATA3" \
  "$API_URL/auth/login")

echo "登录响应: $LOGIN_RESPONSE3"

if echo "$LOGIN_RESPONSE3" | grep -q "access_token"; then
    echo "✓ Demo 登录成功!"
else
    echo "✗ Demo 登录失败"
fi
echo ""

# 测试 4: 使用错误的密码登录
echo "[4] 测试错误密码登录"
echo "账户: admin / wrong_password"

LOGIN_DATA4="username=admin&password=wrong_password"

LOGIN_RESPONSE4=$(curl -s -X POST \
  -H "Content-Type: application/x-www-form-urlencoded" \
  -d "$LOGIN_DATA4" \
  "$API_URL/auth/login")

echo "登录响应: $LOGIN_RESPONSE4"

if echo "$LOGIN_RESPONSE4" | grep -q "Incorrect username or password\|error"; then
    echo "✓ 错误密码被正确拒绝"
else
    echo "⚠ 错误密码未被正确拒绝"
fi
echo ""

# 测试 5: 测试获取当前用户信息（需要 Token）
if [ -n "$TOKEN" ]; then
    echo "[5] 测试获取当前用户信息"
    ME_RESPONSE=$(curl -s -X GET \
      -H "Authorization: Bearer $TOKEN" \
      "$API_URL/auth/me")

    if echo "$ME_RESPONSE" | grep -q "username"; then
        echo "✓ 获取用户信息成功"
        echo "用户数据: $(echo $ME_RESPONSE | python3 -c "import sys, json; d=json.load(sys.stdin); print(f\"用户名: {d.get('username')}, 邮箱: {d.get('email')}, 角色: {d.get('role')}\")" 2>/dev/null)"
    else
        echo "✗ 获取用户信息失败"
    fi
else
    echo "[5] 跳过（无 Token）"
fi

echo ""
echo "========================================="
echo "  测试总结"
echo "========================================="
echo ""
echo "可用账户："
echo "  管理员: admin / admin123"
echo "  测试用户: testuser / Test123456"
echo "  演示用户: demo / Demo123456"
echo ""
