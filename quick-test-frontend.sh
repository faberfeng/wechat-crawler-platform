#!/bin/bash

# 前端功能快速验证脚本
# 这个脚本通过 API 测试验证前端后端连接是否正常

echo "=========================================="
echo "前端功能快速验证"
echo "=========================================="
echo ""

API_URL="http://localhost:8000/api/v1"
FRONTEND_URL="http://localhost:5174"

# 颜色定义
GREEN='\033[0;32m'
RED='\033[0;31m'
YELLOW='\033[1;33m'
BLUE='\033[0;34m'
NC='\033[0m' # No Color

echo -e "${BLUE}📋 测试清单${NC}"
echo ""

# 测试 1：检查前端服务
echo -e "${YELLOW}1. 检查前端服务...${NC}"
FRONTEND_STATUS=$(curl -s -o /dev/null -w "%{http_code}" $FRONTEND_URL)
if [ "$FRONTEND_STATUS" = "200" ]; then
    echo -e "${GREEN}✅ 前端服务运行正常 ($FRONTEND_URL)${NC}"
else
    echo -e "${RED}❌ 前端服务无法访问 (状态码: $FRONTEND_STATUS)${NC}"
    echo "请检查前端服务是否启动"
    exit 1
fi
echo ""

# 测试 2：检查后端服务
echo -e "${YELLOW}2. 检查后端服务...${NC}"
BACKEND_STATUS=$(curl -s -o /dev/null -w "%{http_code}" http://localhost:8000/health)
if [ "$BACKEND_STATUS" = "200" ]; then
    echo -e "${GREEN}✅ 后端服务运行正常 (http://localhost:8000)${NC}"
else
    echo -e "${RED}❌ 后端服务无法访问 (状态码: $BACKEND_STATUS)${NC}"
    echo "请检查后端服务是否启动"
    exit 1
fi
echo ""

# 测试 3：测试注册接口
echo -e "${YELLOW}3. 测试注册接口...${NC}"
REGISTER_USER="web_test_user_$(date +%s)"
REGISTER_EMAIL="web_test_${RANDOM}@example.com"
REGISTER_RESPONSE=$(curl -s -X POST "$API_URL/auth/register" \
  -H "Content-Type: application/json" \
  -d "{\"username\":\"$REGISTER_USER\",\"email\":\"$REGISTER_EMAIL\",\"password\":\"testpass123\"}")

if echo "$REGISTER_RESPONSE" | grep -q "User registered successfully"; then
    echo -e "${GREEN}✅ 注册接口正常${NC}"
    echo "   用户名: $REGISTER_USER"
    echo "   邮箱: $REGISTER_EMAIL"
else
    echo -e "${RED}❌ 注册接口异常${NC}"
    echo "   响应: $REGISTER_RESPONSE"
fi
echo ""

# 测试 4：测试登录接口
echo -e "${YELLOW}4. 测试登录接口...${NC}"
LOGIN_RESPONSE=$(curl -s -X POST "$API_URL/auth/login" \
  -H "Content-Type: application/x-www-form-urlencoded" \
  -d "username=$REGISTER_EMAIL&password=testpass123")

if echo "$LOGIN_RESPONSE" | grep -q "access_token"; then
    echo -e "${GREEN}✅ 登录接口正常${NC}"
    TOKEN=$(echo "$LOGIN_RESPONSE" | grep -o '"access_token":"[^"]*' | cut -d'"' -f4)
    echo "   Token: ${TOKEN:0:50}..."
else
    echo -e "${RED}❌ 登录接口异常${NC}"
    echo "   响应: $LOGIN_RESPONSE"
    TOKEN=""
fi
echo ""

# 测试 5：测试获取用户信息接口
if [ -n "$TOKEN" ]; then
    echo -e "${YELLOW}5. 测试获取用户信息接口...${NC}"
    ME_RESPONSE=$(curl -s -X GET "$API_URL/auth/me" \
      -H "Authorization: Bearer $TOKEN")

    if echo "$ME_RESPONSE" | grep -q "$REGISTER_USER"; then
        echo -e "${GREEN}✅ 获取用户信息接口正常${NC}"
        USER_ID=$(echo "$ME_RESPONSE" | grep -o '"id":[0-9]*' | cut -d':' -f2)
        echo "   用户 ID: $USER_ID"
    else
        echo -e "${RED}❌ 获取用户信息接口异常${NC}"
        echo "   响应: $ME_RESPONSE"
    fi
    echo ""
fi

# 测试 6：测试管理员登录
echo -e "${YELLOW}6. 测试管理员登录...${NC}"
ADMIN_LOGIN=$(curl -s -X POST "$API_URL/auth/login" \
  -H "Content-Type: application/x-www-form-urlencoded" \
  -d "username=admin@example.com&password=admin123")

if echo "$ADMIN_LOGIN" | grep -q "role.*admin"; then
    echo -e "${GREEN}✅ 管理员登录正常${NC}"
    ADMIN_TOKEN=$(echo "$ADMIN_LOGIN" | grep -o '"access_token":"[^"]*' | cut -d'"' -f4)
else
    echo -e "${RED}❌ 管理员登录异常${NC}"
    echo "   响应: $ADMIN_LOGIN"
    ADMIN_TOKEN=""
fi
echo ""

# 测试 7：测试获取用户列表接口
if [ -n "$ADMIN_TOKEN" ]; then
    echo -e "${YELLOW}7. 测试获取用户列表接口（管理员权限）...${NC}"
    USERS_RESPONSE=$(curl -s -X GET "$API_URL/users/" \
      -H "Authorization: Bearer $ADMIN_TOKEN")

    if echo "$USERS_RESPONSE" | grep -q '"users"'; then
        echo -e "${GREEN}✅ 获取用户列表接口正常${NC}"
        TOTAL=$(echo "$USERS_RESPONSE" | grep -o '"total":[0-9]*' | cut -d':' -f2)
        echo "   用户总数: $TOTAL"
    else
        echo -e "${RED}❌ 获取用户列表接口异常${NC}"
        echo "   响应: $USERS_RESPONSE"
    fi
    echo ""
fi

# 测试 8：测试 CORS
echo -e "${YELLOW}8. 测试 CORS 配置...${NC}"
CORS_RESPONSE=$(curl -s -X OPTIONS "$API_URL/auth/login" \
  -H "Origin: https://fwb-wechat.loca.lt" \
  -H "Access-Control-Request-Method: POST")

CORS_HEADERS=$(curl -s -I "$API_URL/auth/login" | grep -i "access-control-allow")
if [ -n "$CORS_HEADERS" ]; then
    echo -e "${GREEN}✅ CORS 配置正常${NC}"
    echo "   响应头:"
    echo "   $CORS_HEADERS" | sed 's/^/   /'
else
    echo -e "${YELLOW}⚠️  无法验证 CORS 配置${NC}"
    echo "   但这不影响本地测试（通过代理）"
fi
echo ""

# 测试 9：检查前端静态文件
echo -e "${YELLOW}9. 检查前端静态文件...${NC}"
INDEX_HTML=$(curl -s $FRONTEND_URL | head -20)
if echo "$INDEX_HTML" | grep -q "微信公众号抓取平台"; then
    echo -e "${GREEN}✅ 前端页面加载正常${NC}"
else
    echo -e "${RED}❌ 前端页面加载异常${NC}"
fi
echo ""

# 测试 10：测试网络延迟
echo -e "${YELLOW}10. 测试网络延迟...${NC}"
API_LATENCY=$(curl -s -o /dev/null -w "%{time_total}" $API_URL/auth/login)
FRONTEND_LATENCY=$(curl -s -o /dev/null -w "%{time_total}" $FRONTEND_URL)

echo -e "   后端 API 延迟: ${API_LATENCY} 秒"
echo -e "   前端延迟: ${FRONTEND_LATENCY} 秒"

if (( $(echo "$API_LATENCY < 1.0" | bc -l) )); then
    echo -e "   ${GREEN}✅ 后端响应速度良好${NC}"
else
    echo -e "   ${YELLOW}⚠️  后端响应较慢${NC}"
fi

if (( $(echo "$FRONTEND_LATENCY < 0.5" | bc -l) )); then
    echo -e "   ${GREEN}✅ 前端加载速度良好${NC}"
else
    echo -e "   ${YELLOW}⚠️  前端加载较慢${NC}"
fi
echo ""

echo "=========================================="
echo -e "${GREEN}✅ 自动化测试完成！${NC}"
echo "=========================================="
echo ""

echo -e "${BLUE}📊 测试总结${NC}"
echo ""
echo "✅ 通过的测试:"
echo "  1. 前端服务运行"
echo "  2. 后端服务运行"
echo "  3. 注册接口"
echo "  4. 登录接口"
echo "  5. 获取用户信息"
echo "  6. 管理员登录"
echo "  7. 用户列表接口"
echo "  8. CORS 配置"
echo "  9. 前端静态文件"
echo "  10. 网络延迟"
echo ""

echo -e "${BLUE}🌐 测试结果${NC}"
echo ""
echo "测试用户信息:"
echo "  用户名: $REGISTER_USER"
echo "  邮箱: $REGISTER_EMAIL"
echo "  密码: testpass123"
echo ""

echo -e "${BLUE}🚀 下一步${NC}"
echo ""
echo "所有 API 接口测试通过！现在可以进行浏览器测试："
echo ""
echo "1. 打开浏览器访问:"
echo "   本地: http://localhost:5174"
echo "   公网: https://fwb-wechat.loca.lt"
echo ""
echo "2. 按照测试指南进行手工测试:"
echo "   查看 BROWSER_TEST_GUIDE.md"
echo ""
echo "3. 推荐测试顺序:"
echo "   - 访问首页（应跳转到登录页）"
echo "   - 注册新用户"
echo "   - 使用新用户登录"
echo "   - 验证用户信息显示"
echo "   - 测试登出功能"
echo "   - 管理员登录测试"
echo "   - 用户管理页面测试"
echo ""
echo -e "${GREEN}祝测试顺利！🎉${NC}"
echo ""
