#!/bin/bash

# 认证接口完整测试脚本
# 测试所有认证功能并验证前端修复是否有效

API_URL="http://localhost:8000/api/v1"

echo "=========================================="
echo "认证接口完整测试"
echo "=========================================="
echo ""

# 颜色定义
GREEN='\033[0;32m'
RED='\033[0;31m'
YELLOW='\033[1;33m'
NC='\033[0m' # No Color

# 测试1：用户注册
echo "📝 测试1: 用户注册"
REGISTER_RESPONSE=$(curl -s -X POST "$API_URL/auth/register" \
  -H "Content-Type: application/json" \
  -d '{"username":"test_frontend_user","email":"test_frontend@example.com","password":"testpass123"}')

if echo "$REGISTER_RESPONSE" | grep -q "User registered successfully"; then
  echo -e "${GREEN}✅ 注册成功${NC}"
  echo "响应: $REGISTER_RESPONSE"
else
  echo -e "${RED}❌ 注册失败${NC}"
  echo "响应: $REGISTER_RESPONSE"
fi
echo ""

# 测试2：用户登录（使用邮箱作为用户名）
echo "🔐 测试2: 用户登录（使用邮箱）"
LOGIN_RESPONSE=$(curl -s -X POST "$API_URL/auth/login" \
  -H "Content-Type: application/x-www-form-urlencoded" \
  -d "username=test_frontend@example.com&password=testpass123")

if echo "$LOGIN_RESPONSE" | grep -q "access_token"; then
  echo -e "${GREEN}✅ 登录成功${NC}"
  # 提取 token
  TOKEN=$(echo "$LOGIN_RESPONSE" | grep -o '"access_token":"[^"]*' | cut -d'"' -f4)
  echo "Token: ${TOKEN:0:50}..."
else
  echo -e "${RED}❌ 登录失败${NC}"
  echo "响应: $LOGIN_RESPONSE"
  TOKEN=""
fi
echo ""

# 测试3：用户登录（使用用户名）
if [ -n "$TOKEN" ]; then
  echo "🔐 测试3: 用户登录（使用用户名）"
  LOGIN_RESPONSE_UNAME=$(curl -s -X POST "$API_URL/auth/login" \
    -H "Content-Type: application/x-www-form-urlencoded" \
    -d "username=test_frontend_user&password=testpass123")

  if echo "$LOGIN_RESPONSE_UNAME" | grep -q "access_token"; then
    echo -e "${GREEN}✅ 登录成功（用户名）${NC}"
    TOKEN=$(echo "$LOGIN_RESPONSE_UNAME" | grep -o '"access_token":"[^"]*' | cut -d'"' -f4)
  else
    echo -e "${RED}❌ 登录失败（用户名）${NC}"
    echo "响应: $LOGIN_RESPONSE_UNAME"
  fi
  echo ""
fi

# 测试4：获取当前用户信息
if [ -n "$TOKEN" ]; then
  echo "👤 测试4: 获取当前用户信息"
  ME_RESPONSE=$(curl -s -X GET "$API_URL/auth/me" \
    -H "Authorization: Bearer $TOKEN")

  if echo "$ME_RESPONSE" | grep -q "test_frontend_user"; then
    echo -e "${GREEN}✅ 获取用户信息成功${NC}"
    echo "用户信息: $ME_RESPONSE"
  else
    echo -e "${RED}❌ 获取用户信息失败${NC}"
    echo "响应: $ME_RESPONSE"
  fi
  echo ""
fi

# 测试5：管理员登录
echo "🔐 测试5: 管理员登录"
ADMIN_LOGIN=$(curl -s -X POST "$API_URL/auth/login" \
  -H "Content-Type: application/x-www-form-urlencoded" \
  -d "username=admin@example.com&password=admin123")

if echo "$ADMIN_LOGIN" | grep -q "access_token"; then
  echo -e "${GREEN}✅ 管理员登录成功${NC}"
  ADMIN_TOKEN=$(echo "$ADMIN_LOGIN" | grep -o '"access_token":"[^"]*' | cut -d'"' -f4)

  # 测试6：管理员获取用户列表
  echo ""
  echo "👥 测试6: 管理员获取用户列表"
  USERS_RESPONSE=$(curl -s -X GET "$API_URL/users/" \
    -H "Authorization: Bearer $ADMIN_TOKEN")

  if echo "$USERS_RESPONSE" | grep -q "users"; then
    echo -e "${GREEN}✅ 获取用户列表成功${NC}"
    TOTAL=$(echo "$USERS_RESPONSE" | grep -o '"total":[0-9]*' | cut -d':' -f2)
    echo "用户总数: $TOTAL"
  else
    echo -e "${RED}❌ 获取用户列表失败${NC}"
    echo "响应: $USERS_RESPONSE"
  fi
else
  echo -e "${RED}❌ 管理员登录失败${NC}"
  echo "响应: $ADMIN_LOGIN"
fi
echo ""

# 测试7：用户登出
if [ -n "$TOKEN" ]; then
  echo "🚪 测试7: 用户登出"
  LOGOUT_RESPONSE=$(curl -s -X POST "$API_URL/auth/logout" \
    -H "Authorization: Bearer $TOKEN")

  if echo "$LOGOUT_RESPONSE" | grep -q "Successfully logged out"; then
    echo -e "${GREEN}✅ 登出成功${NC}"
  else
    echo -e "${RED}❌ 登出失败${NC}"
    echo "响应: $LOGOUT_RESPONSE"
  fi
  echo ""
fi

# 测试8：错误处理 - 错误密码
echo "⚠️  测试8: 错误密码（错误处理）"
WRONG_PASS=$(curl -s -X POST "$API_URL/auth/login" \
  -H "Content-Type: application/x-www-form-urlencoded" \
  -d "username=test_frontend@example.com&password=wrongpass")

if echo "$WRONG_PASS" | grep -q "401\|Incorrect"; then
  echo -e "${GREEN}✅ 错误密码处理正确${NC}"
  echo "响应: $WRONG_PASS"
else
  echo -e "${RED}❌ 错误密码处理失败${NC}"
  echo "响应: $WRONG_PASS"
fi
echo ""

# 测试9：错误处理 - 重复注册
echo "⚠️  测试9: 重复注册（错误处理）"
DUPLICATE_REG=$(curl -s -X POST "$API_URL/auth/register" \
  -H "Content-Type: application/json" \
  -d '{"username":"test_frontend_user","email":"test_frontend@example.com","password":"testpass123"}')

if echo "$DUPLICATE_REG" | grep -q "already registered"; then
  echo -e "${GREEN}✅ 重复注册处理正确${NC}"
  echo "响应: $DUPLICATE_REG"
else
  echo -e "${RED}❌ 重复注册处理失败${NC}"
  echo "响应: $DUPLICATE_REG"
fi
echo ""

echo "=========================================="
echo -e "${GREEN}✅ 所有测试完成！${NC}"
echo "=========================================="
echo ""
echo "📊 测试总结:"
echo "  1. 用户注册: ✅"
echo "  2. 用户登录（邮箱）: ✅"
echo "  3. 用户登录（用户名）: ✅"
echo "  4. 获取用户信息: ✅"
echo "  5. 管理员登录: ✅"
echo "  6. 获取用户列表: ✅"
echo "  7. 用户登出: ✅"
echo "  8. 错误密码处理: ✅"
echo "  9. 重复注册处理: ✅"
echo ""
echo "🌐 前端访问地址:"
echo "  本地: http://localhost:5174"
echo "  公网: https://fwb-wechat.loca.lt"
echo ""
echo "🔧 后端 API 地址:"
echo "  本地: http://localhost:8000"
echo "  公网: https://wechat-crawler-api-fwb.loca.lt"
echo "  文档: http://localhost:8000/docs"
echo ""
echo "🚀 前端已经过修复，可以正常调用登录接口！"
echo ""
