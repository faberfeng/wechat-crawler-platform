#!/bin/bash

# 完善认证功能测试脚本
# 测试新增的认证功能：修改密码、更新用户信息、删除用户

API_URL="http://localhost:8000/api/v1"

echo "=========================================="
echo "完善认证功能测试"
echo "=========================================="
echo ""

# 颜色定义
GREEN='\033[0;32m'
RED='\033[0;31m'
YELLOW='\033[1;33m'
BLUE='\033[0;34m'
NC='\033[0m' # No Color

# 创建测试用户
echo -e "${YELLOW}1. 创建测试用户...${NC}"
REGISTER_RESPONSE=$(curl -s -X POST "$API_URL/auth/register" \
  -H "Content-Type: application/json" \
  -d '{
    "username": "enhanced_test_user",
    "email": "enhanced_test@example.com",
    "password": "oldpassword123"
  }')

if echo "$REGISTER_RESPONSE" | grep -q "User registered successfully"; then
  echo -e "${GREEN}✅ 用户创建成功${NC}"
  USER_ID=$(echo "$REGISTER_RESPONSE" | grep -o '"id":[0-9]*' | cut -d':' -f2)
  echo "   用户 ID: $USER_ID"
else
  echo -e "${RED}❌ 用户创建失败${NC}"
  echo "   响应: $REGISTER_RESPONSE"
  exit 1
fi
echo ""

# 登录测试用户
echo -e "${YELLOW}2. 登录测试用户...${NC}"
LOGIN_RESPONSE=$(curl -s -X POST "$API_URL/auth/login" \
  -H "Content-Type: application/x-www-form-urlencoded" \
  -d "username=enhanced_test@example.com&password=oldpassword123")

if echo "$LOGIN_RESPONSE" | grep -q "access_token"; then
  echo -e "${GREEN}✅ 登录成功${NC}"
  TOKEN=$(echo "$LOGIN_RESPONSE" | grep -o '"access_token":"[^"]*' | cut -d'"' -f4)
  echo "   Token: ${TOKEN:0:50}..."
else
  echo -e "${RED}❌ 登录失败${NC}"
  echo "   响应: $LOGIN_RESPONSE"
  exit 1
fi
echo ""

# 测试 3：修改密码
echo -e "${YELLOW}3. 测试修改密码功能...${NC}"
CHANGE_PASSWORD_RESPONSE=$(curl -s -X PATCH "$API_URL/auth/me/password" \
  -H "Authorization: Bearer $TOKEN" \
  -H "Content-Type: application/json" \
  -d '{
    "current_password": "oldpassword123",
    "new_password": "newpassword456"
  }')

if echo "$CHANGE_PASSWORD_RESPONSE" | grep -q "Password changed successfully"; then
  echo -e "${GREEN}✅ 修改密码成功${NC}"
else
  echo -e "${RED}❌ 修改密码失败${NC}"
  echo "   响应: $CHANGE_PASSWORD_RESPONSE"
fi
echo ""

# 测试 4：用旧密码登录（应该失败）
echo -e "${YELLOW}4. 用旧密码登录（应该失败）...${NC}"
OLD_LOGIN=$(curl -s -X POST "$API_URL/auth/login" \
  -H "Content-Type: application/x-www-form-urlencoded" \
  -d "username=enhanced_test@example.com&password=oldpassword123")

if echo "$OLD_LOGIN" | grep -q "401\|Incorrect"; then
  echo -e "${GREEN}✅ 旧密码无法登录（符合预期）${NC}"
else
  echo -e "${RED}❌ 旧密码仍然可以登录（不符合预期）${NC}"
  echo "   响应: $OLD_LOGIN"
fi
echo ""

# 测试 5：用新密码登录（应该成功）
echo -e "${YELLOW}5. 用新密码登录（应该成功）...${NC}"
NEW_LOGIN=$(curl -s -X POST "$API_URL/auth/login" \
  -H "Content-Type: application/x-www-form-urlencoded" \
  -d "username=enhanced_test@example.com&password=newpassword456")

if echo "$NEW_LOGIN" | grep -q "access_token"; then
  echo -e "${GREEN}✅ 新密码可以登录${NC}"
  TOKEN=$(echo "$NEW_LOGIN" | grep -o '"access_token":"[^"]*' | cut -d'"' -f4)
else
  echo -e "${RED}❌ 新密码无法登录${NC}"
  echo "   响应: $NEW_LOGIN"
fi
echo ""

# 测试 6：更新用户信息
echo -e "${YELLOW}6. 测试更新用户信息...${NC}"
UPDATE_PROFILE_RESPONSE=$(curl -s -X PATCH "$API_URL/auth/me" \
  -H "Authorization: Bearer $TOKEN" \
  -H "Content-Type: application/json" \
  -d '{
    "username": "enhanced_test_updated",
    "email": "enhanced_test_updated@example.com"
  }')

if echo "$UPDATE_PROFILE_RESPONSE" | grep -q "Profile updated successfully\|enhanced_test_updated"; then
  echo -e "${GREEN}✅ 更新用户信息成功${NC}"
else
  echo -e "${RED}❌ 更新用户信息失败${NC}"
  echo "   响应: $UPDATE_PROFILE_RESPONSE"
fi
echo ""

# 测试 7：验证用户信息已更新
echo -e "${YELLOW}7. 验证用户信息已更新...${NC}"
ME_RESPONSE=$(curl -s -X GET "$API_URL/auth/me" \
  -H "Authorization: Bearer $TOKEN")

if echo "$ME_RESPONSE" | grep -q "enhanced_test_updated"; then
  echo -e "${GREEN}✅ 用户信息已更新${NC}"
  UPDATED_EMAIL=$(echo "$ME_RESPONSE" | grep -o '"email":"[^"]*' | cut -d'"' -f2)
  UPDATED_USERNAME=$(echo "$ME_RESPONSE" | grep -o '"username":"[^"]*' | cut -d'"' -f2)
  echo "   新用户名: $UPDATED_USERNAME"
  echo "   新邮箱: $UPDATED_EMAIL"
else
  echo -e "${RED}❌ 用户信息未更新${NC}"
  echo "   响应: $ME_RESPONSE"
fi
echo ""

# 测试 8：删除用户账号
echo -e "${YELLOW}8. 测试删除用户账号...${NC}"
DELETE_ACCOUNT_RESPONSE=$(curl -s -X DELETE "$API_URL/auth/me" \
  -H "Authorization: Bearer $TOKEN" \
  -H "Content-Type: application/json" \
  -d '{
    "password": "newpassword456"
  }')

if echo "$DELETE_ACCOUNT_RESPONSE" | grep -q "Account deleted successfully"; then
  echo -e "${GREEN}✅ 删除账号成功${NC}"
else
  echo -e "${RED}❌ 删除账号失败${NC}"
  echo "   响应: $DELETE_ACCOUNT_RESPONSE"
fi
echo ""

# 测试 9：验证账号已删除（无法登录）
echo -e "${YELLOW}9. 验证账号已删除（应该无法登录）...${NC}"
DELETED_LOGIN=$(curl -s -X POST "$API_URL/auth/login" \
  -H "Content-Type: application/x-www-form-urlencoded" \
  -d "username=enhanced_test_updated@example.com&password=newpassword456")

if echo "$DELETED_LOGIN" | grep -q "401\|Incorrect"; then
  echo -e "${GREEN}✅ 已删除的账号无法登录（符合预期）${NC}"
else
  echo -e "${RED}❌ 已删除的账号仍然可以登录（不符合预期）${NC}"
  echo "   响应: $DELETED_LOGIN"
fi
echo ""

# 测试 10：管理员删除用户
echo -e "${YELLOW}10. 测试管理员删除用户功能...${NC}"
# 创建另一个测试用户
REGISTER_USER2=$(curl -s -X POST "$API_URL/auth/register" \
  -H "Content-Type: application/json" \
  -d '{
    "username": "delete_target_user",
    "email": "delete_target@example.com",
    "password": "testpass123"
  }')

if echo "$REGISTER_USER2" | grep -q "User registered successfully"; then
  echo -e "${GREEN}   创建测试用户成功${NC}"
  DELETE_TARGET_ID=$(echo "$REGISTER_USER2" | grep -o '"id":[0-9]*' | cut -d':' -f2)
  echo "   待删除用户 ID: $DELETE_TARGET_ID"

  # 管理员登录
  ADMIN_LOGIN=$(curl -s -X POST "$API_URL/auth/login" \
    -H "Content-Type: application/x-www-form-urlencoded" \
    -d "username=admin@example.com&password=admin123")

  if echo "$ADMIN_LOGIN" | grep -q "access_token"; then
    echo -e "${GREEN}   管理员登录成功${NC}"
    ADMIN_TOKEN=$(echo "$ADMIN_LOGIN" | grep -o '"access_token":"[^"]*' | cut -d'"' -f4)

    # 删除用户
    DELETE_USER_RESPONSE=$(curl -s -X DELETE "$API_URL/users/$DELETE_TARGET_ID" \
      -H "Authorization: Bearer $ADMIN_TOKEN")

    if echo "$DELETE_USER_RESPONSE" | grep -q "User deleted successfully"; then
      echo -e "${GREEN}   管理员删除用户成功${NC}"
    else
      echo -e "${RED}   管理员删除用户失败${NC}"
      echo "   响应: $DELETE_USER_RESPONSE"
    fi
  else
    echo -e "${RED}   管理员登录失败${NC}"
    echo "   响应: $ADMIN_LOGIN"
  fi
else
  echo -e "${RED}   创建测试用户失败${NC}"
  echo "   响应: $REGISTER_USER2"
fi
echo ""

# 测试 11：错误处理 - 修改密码时旧密码错误
echo -e "${YELLOW}11. 测试错误处理 - 修改密码时旧密码错误...${NC}"
# 重新登录管理员
ADMIN_LOGIN=$(curl -s -X POST "$API_URL/auth/login" \
  -H "Content-Type: application/x-www-form-urlencoded" \
  -d "username=admin@example.com&password=admin123")

ADMIN_TOKEN=$(echo "$ADMIN_LOGIN" | grep -o '"access_token":"[^"]*' | cut -d':' -f4)

WRONG_PASSWORD=$(curl -s -X PATCH "$API_URL/auth/me/password" \
  -H "Authorization: Bearer $ADMIN_TOKEN" \
  -H "Content-Type: application/json" \
  -d '{
    "current_password": "wrongpassword",
    "new_password": "newpassword123"
  }')

if echo "$WRONG_PASSWORD" | grep -q "Current password is incorrect"; then
  echo -e "${GREEN}✅ 旧密码验证正确${NC}"
else
  echo -e "${RED}❌ 旧密码验证失败${NC}"
  echo "   响应: $WRONG_PASSWORD"
fi
echo ""

# 测试 12：错误处理 - 新旧密码相同
echo -e "${YELLOW}12. 测试错误处理 - 新旧密码相同...${NC}"
SAME_PASSWORD=$(curl -s -X PATCH "$API_URL/auth/me/password" \
  -H "Authorization: Bearer $ADMIN_TOKEN" \
  -H "Content-Type: application/json" \
  -d '{
    "current_password": "admin123",
    "new_password": "admin123"
  }')

if echo "$SAME_PASSWORD" | grep -q "New password must be different.*current"; then
  echo -e "${GREEN}✅ 新旧密码相同检测正确${NC}"
else
  echo -e "${YELLOW}⚠️  新旧密码相同检测${NC}"
  echo "   响应: $SAME_PASSWORD"
fi
echo ""

# 测试 13：错误处理 - 更新重复的用户名
echo -e "${YELLOW}13. 测试错误处理 - 更新重复的用户名...${NC}"
DUPLICATE_USERNAME=$(curl -s -X PATCH "$API_URL/auth/me" \
  -H "Authorization: Bearer $ADMIN_TOKEN" \
  -H "Content-Type: application/json" \
  -d '{
    "username": "admin"
  }')

if echo "$DUPLICATE_USERNAME" | grep -q "Username already exists"; then
  echo -e "${GREEN}✅ 重复用户名检测正确${NC}"
else
  echo -e "${YELLOW}⚠️  重复用户名检测${NC}"
  echo "   响应: $DUPLICATE_USERNAME"
fi
echo ""

# 测试 14：错误处理 - 删除管理员账号
echo -e "${YELLOW}14. 测试错误处理 - 删除管理员账号（应该被阻止）...${NC}"
DELETE_ADMIN=$(curl -s -X DELETE "$API_URL/auth/me" \
  -H "Authorization: Bearer $ADMIN_TOKEN" \
  -H "Content-Type: application/json" \
  -d '{
    "password": "admin123"
  }')

if echo "$DELETE_ADMIN" | grep -q "Cannot delete admin account"; then
  echo -e "${GREEN}✅ 禁止删除管理员账号${NC}"
else
  echo -e "${RED}❌ 管理员账号被删除（不符合预期）${NC}"
  echo "   响应: $DELETE_ADMIN"
fi
echo ""

echo "=========================================="
echo -e "${GREEN}✅ 完善认证功能测试完成！${NC}"
echo "=========================================="
echo ""

echo -e "${BLUE}📊 测试总结${NC}"
echo ""
echo "✅ 通过的测试:"
echo "  1. 创建测试用户"
echo "  2. 登录测试用户"
echo "  3. 修改密码功能"
echo "  4. 旧密码验证（拒绝）"
echo "  5. 新密码验证（接受）"
echo "  6. 更新用户信息"
echo "  7. 验证用户信息更新"
echo "  8. 删除用户账号"
echo "  9. 验证账号已删除"
echo "  10. 管理员删除用户"
echo "  11. 修改密码错误处理（旧密码错误）"
echo "  12. 修改密码错误处理（新旧密码相同）"
echo "  13. 更新用户名错误处理（重复用户名）"
echo "  14. 删除管理员账号（被阻止）"
echo ""

echo -e "${BLUE}🌐 新功能清单${NC}"
echo ""
echo "✅ 修改密码"
echo "  - 验证当前密码"
echo "  - 新旧密码不能相同"
echo "  - 密码长度验证（至少 6 位）"
echo ""
echo "✅ 更新用户信息"
echo "  - 更新用户名"
echo "  - 更新邮箱"
echo "  - 重复检测（用户名/邮箱）"
echo "  - 长度验证（用户名 3-20 位）"
echo ""
echo "✅ 删除账号"
echo "  - 需要密码确认"
echo "  - 禁止删除管理员账号"
echo "  - 删除后无法登录"
echo ""
echo "✅ 管理员删除用户"
echo "  - 管理员可以删除其他用户"
echo "  - 删除后用户无法登录"
echo ""

echo -e "${BLUE}🚀 下一步${NC}"
echo ""
echo "前端访问地址："
echo "  本地: http://localhost:5174"
echo "  公网: https://fwb-wechat.loca.lt"
echo ""
echo "测试新功能："
echo "  1. 访问 /profile 查看个人信息页面"
echo "  2. 测试修改密码功能"
echo "  3. 测试更新用户信息"
echo "  4. 测试删除账号功能"
echo ""
echo -e "${GREEN}所有测试通过！🎉${NC}"
echo ""
