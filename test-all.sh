#!/bin/bash

# 前后端全面测试脚本
# 测试所有可用的 API 端点和功能

BASE_URL="http://localhost:8001"
API_URL="$BASE_URL/api/v1"

# 颜色定义
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
NC='\033[0m' # No Color

# 测试计数
PASS=0
FAIL=0

# 测试函数
test_endpoint() {
    local name="$1"
    local method="$2"
    local url="$3"
    local data="$4"
    local token="$5"

    local full_url="$API_URL$url"
    local cmd="curl -s -X $method"

    if [ -n "$token" ]; then
        cmd="$cmd -H 'Authorization: Bearer $token'"
    fi

    if [ -n "$data" ]; then
        cmd="$cmd -H 'Content-Type: application/json' -d '$data'"
    fi

    cmd="$cmd $full_url"

    echo -n "测试 $name... "
    local response=$(eval $cmd)
    local code=$?

    if [ $code -eq 0 ]; then
        echo -e "${GREEN}✓ PASS${NC}"
        ((PASS++))
        echo "   响应: $(echo $response | head -c 100)..."
    else
        echo -e "${RED}✗ FAIL${NC} (退出码: $code)"
        ((FAIL++))
    fi
}

# 测试 POST 请求（表单数据）
test_form_endpoint() {
    local name="$1"
    local url="$2"
    local data="$3"

    local full_url="$API_URL$url"
    local cmd="curl -s -X POST -H 'Content-Type: application/x-www-form-urlencoded' -d '$data' $full_url"

    echo -n "测试 $name... "
    local response=$(eval $cmd)
    local code=$?

    if [ $code -eq 0 ]; then
        echo -e "${GREEN}✓ PASS${NC}"
        ((PASS++))
        echo "   响应: $(echo $response | head -c 100)..."
    else
        echo -e "${RED}✗ FAIL${NC} (退出码: $code)"
        ((FAIL++))
    fi
}

echo "========================================="
echo "  微信公众号抓取平台 - 全面测试"
echo "========================================="
echo ""

# 1. 测试后端服务是否运行
echo -e "${YELLOW}[1] 测试后端服务${NC}"
if curl -s "$BASE_URL/docs" > /dev/null; then
    echo -e "${GREEN}✓ 后端服务正常运行${NC}"
    ((PASS++))
else
    echo -e "${RED}✗ 后端服务无法访问${NC}"
    ((FAIL++))
    exit 1
fi
echo ""

# 2. 测试 API 文档
echo -e "${YELLOW}[2] 测试 API 文档${NC}"
if curl -s "$BASE_URL/openapi.json" > /dev/null; then
    echo -e "${GREEN}✓ API 文档可访问${NC}"
    ((PASS++))
else
    echo -e "${RED}✗ API 文档无法访问${NC}"
    ((FAIL++))
fi
echo ""

# 3. 测试用户注册
echo -e "${YELLOW}[3] 测试用户注册${NC}"
test_form_endpoint "用户注册" "/auth/register" \
    "username=testuser_$(date +%s)&email=test$(date +%s)@example.com&password=Test123456"
echo ""

# 4. 测试用户登录
echo -e "${YELLOW}[4] 测试用户登录${NC}"
echo -n "测试用户登录... "
local login_response=$(curl -s -X POST \
    -H "Content-Type: application/x-www-form-urlencoded" \
    -d "username=testuser9999999999&password=Test123456" \
    "$API_URL/auth/login")

if echo "$login_response" | grep -q "access_token"; then
    echo -e "${GREEN}✓ PASS${NC}"
    ((PASS++))
    TOKEN=$(echo "$login_response" | python3 -c "import sys, json; print(json.load(sys.stdin).get('access_token', ''))" 2>/dev/null)
    echo "   Token: ${TOKEN:0:50}..."
else
    echo -e "${RED}✗ FAIL${NC}（可能是用户不存在）"
    ((FAIL++))
    echo "   响应: $login_response"
fi
echo ""

# 5. 测试需要认证的端点（如果有 Token）
if [ -n "$TOKEN" ]; then
    echo -e "${YELLOW}[5] 测试认证端点（Token: ${TOKEN:0:20}...）${NC}"

    # 获取当前用户信息
    test_endpoint "获取当前用户信息" "GET" "/auth/me" "" "$TOKEN"

    # 获取公众号列表
    test_endpoint "获取公众号列表" "GET" "/accounts" "" "$TOKEN"

    # 获取文章列表
    test_endpoint "获取文章列表" "GET" "/articles" "" "$TOKEN"

    # 获取文章统计
    test_endpoint "获取文章统计" "GET" "/articles/stats/summary" "" "$TOKEN"

    # 获取文件列表
    test_endpoint "获取文件列表" "GET" "/files/" "" "$TOKEN"

    # 获取文件统计
    test_endpoint "获取文件统计" "GET" "/files/stats/summary" "" "$TOKEN"
else
    echo -e "${YELLOW}[5] 跳过认证端点测试（没有有效 Token）${NC}"
fi

# 摘要
echo ""
echo "========================================="
echo "  测试摘要"
echo "========================================="
echo -e "总测试数: $((PASS + FAIL))"
echo -e "${GREEN}通过: $PASS${NC}"
echo -e "${RED}失败: $FAIL${NC}"
echo ""

if [ $FAIL -eq 0 ]; then
    echo -e "${GREEN}✓ 所有测试通过！${NC}"
    exit 0
else
    echo -e "${RED}✗ 有 $FAIL 个测试失败${NC}"
    exit 1
fi
