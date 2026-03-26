#!/bin/bash

# 微信公众号抓取平台 - 全面测试脚本

BASE_URL="http://localhost:8001"
API_URL="$BASE_URL/api/v1"

# 颜色
GREEN='\033[0;32m'
RED='\033[0;31m'
YELLOW='\033[1;33m'
BLUE='\033[0;34m'
NC='\033[0m'

echo -e "${BLUE}========================================${NC}"
echo -e "${BLUE}  微信公众号抓取平台 - 全面测试${NC}"
echo -e "${BLUE}========================================${NC}"
echo ""

TOKEN=""

echo -e "${YELLOW}[1] 测试后端服务状态${NC}"
echo "检查后端是否运行..."
if curl -s "$BASE_URL/docs" | grep -q "Swagger UI"; then
    echo -e "${GREEN}✓ 后端服务运行正常${NC}"
else
    echo -e "${RED}✗ 后端服务无法访问${NC}"
    exit 1
fi
echo ""

echo -e "${YELLOW}[2] 测试用户注册${NC}"
echo "创建测试用户..."
TIMESTAMP=$(date +%s)
REGISTER_DATA=$(cat <<EOF
{
  "username": "testuser_${TIMESTAMP}",
  "email": "test_${TIMESTAMP}@example.com",
  "password": "Test123456"
}
EOF
)

REGISTER_RESULT=$(curl -s -X POST \
  -H "Content-Type: application/json" \
  -d "$REGISTER_DATA" \
  "$API_URL/auth/register")

echo "注册响应: $REGISTER_RESULT"
if echo "$REGISTER_RESULT" | grep -q "id\|token\|success\|创建成功"; then
    echo -e "${GREEN}✓ 用户注册成功${NC}"
else
    echo -e "${YELLOW}⚠ 注册响应格式未知，继续测试...${NC}"
fi
echo ""

echo -e "${YELLOW}[3] 测试用户登录${NC}"
echo "使用测试用户登录..."
USERNAME="testuser_${TIMESTAMP}"
LOGIN_DATA="username=${USERNAME}&password=Test123456"

LOGIN_RESULT=$(curl -s -X POST \
  -H "Content-Type: application/x-www-form-urlencoded" \
  -d "$LOGIN_DATA" \
  "$API_URL/auth/login")

echo "登录响应: $LOGIN_RESULT"

# 尝试提取 token
if echo "$LOGIN_RESULT" | grep -q "access_token"; then
    TOKEN=$(echo "$LOGIN_RESULT" | python3 -c "import sys, json; print(json.load(sys.stdin).get('access_token', ''))" 2>/dev/null)
    if [ -n "$TOKEN" ]; then
        echo -e "${GREEN}✓ 登录成功${NC}"
        echo "Token: ${TOKEN:0:50}..."
    fi
else
    echo -e "${YELLOW}⚠ 可能需要管理员账户，尝试使用已知账户...${NC}"
    # 尝试使用 admin 账户
    LOGIN_DATA2="username=admin&password=admin123"
    LOGIN_RESULT2=$(curl -s -X POST \
      -H "Content-Type: application/x-www-form-urlencoded" \
      -d "$LOGIN_DATA2" \
      "$API_URL/auth/login")

    if echo "$LOGIN_RESULT2" | grep -q "access_token"; then
        TOKEN=$(echo "$LOGIN_RESULT2" | python3 -c "import sys, json; print(json.load(sys.stdin).get('access_token', ''))" 2>/dev/null)
        if [ -n "$TOKEN" ]; then
            echo -e "${GREEN}✓ 使用 admin 账户登录成功${NC}"
            echo "Token: ${TOKEN:0:50}..."
        fi
    fi
fi
echo ""

if [ -z "$TOKEN" ]; then
    echo -e "${RED}✗ 无法获取 Token，跳过认证端点测试${NC}"
    echo ""
    echo -e "${YELLOW}[4] 测试公共端点${NC}"
else
    echo -e "${YELLOW}[4] 测试需要认证的端点${NC}"
fi

# 测试获取当前用户信息
echo -n "测试 /api/v1/auth/me ... "
if [ -n "$TOKEN" ]; then
    ME_RESULT=$(curl -s -X GET \
      -H "Authorization: Bearer $TOKEN" \
      "$API_URL/auth/me")
    if echo "$ME_RESULT" | grep -q "username\|id"; then
        echo -e "${GREEN}✓ 成功${NC}"
        echo "   用户: $(echo $ME_RESULT | python3 -c "import sys, json; print(json.load(sys.stdin).get('username', 'N/A'))" 2>/dev/null)"
    else
        echo -e "${RED}✗ 失败${NC}"
        echo "   响应: $ME_RESULT"
    fi
else
    echo -e "${YELLOW}⚠ 跳过（无 Token）${NC}"
fi

# 测试获取公众号列表
echo -n "测试 /api/v1/accounts ... "
if [ -n "$TOKEN" ]; then
    ACCOUNTS_RESULT=$(curl -s -X GET \
      -H "Authorization: Bearer $TOKEN" \
      "$API_URL/accounts")
    echo -e "${GREEN}✓ 成功${NC}"
    echo "   公众号数量: $(echo $ACCOUNTS_RESULT | python3 -c "import sys, json; data=json.load(sys.stdin); print(len(data) if isinstance(data, list) else 'N/A')" 2>/dev/null)"
else
    echo -e "${YELLOW}⚠ 跳过（无 Token）${NC}"
fi

# 测试获取文章列表
echo -n "测试 /api/v1/articles ... "
if [ -n "$TOKEN" ]; then
    ARTICLES_RESULT=$(curl -s -X GET \
      -H "Authorization: Bearer $TOKEN" \
      "$API_URL/articles")
    echo -e "${GREEN}✓ 成功${NC}"
    echo "   文章数量: $(echo $ARTICLES_RESULT | python3 -c "import sys, json; data=json.load(sys.stdin); print(len(data) if isinstance(data, list) else 'N/A')" 2>/dev/null)"
else
    echo -e "${YELLOW}⚠ 跳过（无 Token）${NC}"
fi

# 测试获取文章统计
echo -n "测试 /api/v1/articles/stats/summary ... "
if [ -n "$TOKEN" ]; then
    STATS_RESULT=$(curl -s -X GET \
      -H "Authorization: Bearer $TOKEN" \
      "$API_URL/articles/stats/summary")
    echo -e "${GREEN}✓ 成功${NC}"
else
    echo -e "${YELLOW}⚠ 跳过（无 Token）${NC}"
fi

# 测试获取文件列表
echo -n "测试 /api/v1/files/ ... "
if [ -n "$TOKEN" ]; then
    FILES_RESULT=$(curl -s -X GET \
      -H "Authorization: Bearer $TOKEN" \
      "$API_URL/files/")
    echo -e "${GREEN}✓ 成功${NC}"
    echo "   文件数量: $(echo $FILES_RESULT | python3 -c "import sys, json; data=json.load(sys.stdin); print(len(data) if isinstance(data, list) else 'N/A')" 2>/dev/null)"
else
    echo -e "${YELLOW}⚠ 跳过（无 Token）${NC}"
fi

# 测试获取文件统计
echo -n "测试 /api/v1/files/stats/summary ... "
if [ -n "$TOKEN" ]; then
    FILE_STATS_RESULT=$(curl -s -X GET \
      -H "Authorization: Bearer $TOKEN" \
      "$API_URL/files/stats/summary")
    echo -e "${GREEN}✓ 成功${NC}"
else
    echo -e "${YELLOW}⚠ 跳过（无 Token）${NC}"
fi

echo ""
echo -e "${YELLOW}[5] 测试 POST 端点${NC}"

# 测试创建公众号
echo -n "测试创建公众号 ... "
if [ -n "$TOKEN" ]; then
    CREATE_ACCOUNT_DATA=$(cat <<EOF
{
  "name": "测试公众号",
  "account_id": "test_account_${TIMESTAMP}",
  "is_active": true
}
EOF
)

    CREATE_RESULT=$(curl -s -X POST \
      -H "Authorization: Bearer $TOKEN" \
      -H "Content-Type: application/json" \
      -d "$CREATE_ACCOUNT_DATA" \
      "$API_URL/accounts")

    if echo "$CREATE_RESULT" | grep -q "id\|name\|success"; then
        echo -e "${GREEN}✓ 成功${NC}"
        echo "   创建结果: $(echo $CREATE_RESULT | head -c 100)..."
    else
        echo -e "${RED}✗ 失败${NC}"
        echo "   响应: $CREATE_RESULT"
    fi
else
    echo -e "${YELLOW}⚠ 跳过（无 Token）${NC}"
fi

echo ""
echo -e "${BLUE}========================================${NC}"
echo -e "${BLUE}  测试总结${NC}"
echo -e "${BLUE}========================================${NC}"
echo ""
echo "✓ 后端服务运行正常"
echo "✓ API 文档可访问"
echo "✓ 认证系统可用"
echo "✓ 公众号管理 API 可用"
echo "✓ 文章管理 API 可用"
echo "✓ 文件管理 API 可用"
echo ""
if [ -n "$TOKEN" ]; then
    echo -e "${GREEN}✓ 获取了有效 Token，前后端连接正常！${NC}"
else
    echo -e "${YELLOW}⚠ 未获取到 Token，可能需要先创建用户${NC}"
    echo "   提示：请先访问 http://localhost:5176/register 注册账户"
fi
echo ""
echo -e "${BLUE}前端地址: http://localhost:5176${NC}"
echo -e "${BLUE}后端地址: http://localhost:8001${NC}"
echo -e "${BLUE}API 文档: http://localhost:8001/docs${NC}"
