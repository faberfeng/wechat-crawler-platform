/**
 * 前端全面测试脚本
 * 在浏览器控制台中运行以测试前后端连接
 */

console.log('========================================');
console.log('  微信公众号抓取平台 - 前端测试');
console.log('========================================');
console.log('');

const API_BASE = 'http://localhost:8001/api/v1';
let token = '';

// 测试 API 连接
async function testConnection() {
  console.log('%c[1] 测试 API 连接...', 'color: #3399ff');
  try {
    const response = await fetch(`${API_BASE}/auth/me`);
    console.log('✓ API 服务器响应正常');
    console.log(`  状态码: ${response.status}`);
  } catch (error) {
    console.error('✗ API 连接失败:', error);
  }
  console.log('');
}

// 测试用户注册
async function testRegister() {
  console.log('%c[2] 测试用户注册...', 'color: #3399ff');
  const timestamp = Date.now();
  const userData = {
    username: `testuser_${timestamp}`,
    email: `test_${timestamp}@example.com`,
    password: 'Test123456'
  };

  try {
    const response = await fetch(`${API_BASE}/auth/register`, {
      method: 'POST',
      headers: {
        'Content-Type': 'application/json'
      },
      body: JSON.stringify(userData)
    });

    const data = await response.json();
    console.log(`  状态码: ${response.status}`);

    if (response.ok) {
      console.log('✓ 注册成功:', data);
    } else {
      console.log('✗ 注册失败:', data);
    }
  } catch (error) {
    console.error('✗ 请求失败:', error);
  }
  console.log('');
}

// 测试用户登录
async function testLogin() {
  console.log('%c[3] 测试用户登录...', 'color: #3399ff');

  // 尝试使用注册的用户登录
  const loginData = new URLSearchParams({
    username: 'admin',
    password: 'admin123'
  });

  try {
    const response = await fetch(`${API_BASE}/auth/login`, {
      method: 'POST',
      headers: {
        'Content-Type': 'application/x-www-form-urlencoded'
      },
      body: loginData
    });

    const data = await response.json();
    console.log(`  状态码: ${response.status}`);

    if (response.ok && data.access_token) {
      console.log('✓ 登录成功');
      token = data.access_token;
      console.log(`  Token: ${token.substring(0, 50)}...`);
    } else {
      console.log('✗ 登录失败:', data);
    }
  } catch (error) {
    console.error('✗ 请求失败:', error);
  }
  console.log('');
}

// 测试获取当前用户信息
async function testGetMe() {
  console.log('%c[4] 测试 /api/v1/auth/me...', 'color: #3399ff');

  if (!token) {
    console.log('⚠ 跳过（无 Token）');
    console.log('');
    return;
  }

  try {
    const response = await fetch(`${API_BASE}/auth/me`, {
      method: 'GET',
      headers: {
        'Authorization': `Bearer ${token}`
      }
    });

    const data = await response.json();
    console.log(`  状态码: ${response.status}`);

    if (response.ok) {
      console.log('✓ 成功');
      console.log(`  用户: ${data.username}, 邮箱: ${data.email}, 角色: ${data.role}`);
    } else {
      console.log('✗ 失败:', data);
    }
  } catch (error) {
    console.error('✗ 请求失败:', error);
  }
  console.log('');
}

// 测试获取公众号列表
async function testGetAccounts() {
  console.log('%c[5] 测试 /api/v1/accounts...', 'color: #3399ff');

  if (!token) {
    console.log('⚠ 跳过（无 Token）');
    console.log('');
    return;
  }

  try {
    const response = await fetch(`${API_URL}/accounts`, {
      method: 'GET',
      headers: {
        'Authorization': `Bearer ${token}`
      }
    });

    const data = await response.json();
    console.log(`  状态码: ${response.status}`);

    if (response.ok) {
      console.log('✓ 成功');
      console.log(`  公众号数量: ${data.length}`);
      if (data.length > 0) {
        console.log(`  第一个公众号: ${data[0].name}`);
      }
    } else {
      console.log('✗ 失败:', data);
    }
  } catch (error) {
    console.error('✗ 请求失败:', error);
  }
  console.log('');
}

// 测试获取文章列表
async function testGetArticles() {
  console.log('%c[6] 测试 /api/v1/articles...', 'color: #3399ff');

  if (!token) {
    console.log('⚠ 跳过（无 Token）');
    console.log('');
    return;
  }

  try {
    const response = await fetch(`${API_BASE}/articles`, {
      method: 'GET',
      headers: {
        'Authorization': `Bearer ${token}`
      }
    });

    const data = await response.json();
    console.log(`  状态码: ${response.status}`);

    if (response.ok) {
      console.log('✓ 成功');
      console.log(`  文章数量: ${data.length}`);
      if (data.length > 0) {
        console.log(`  第一篇文章: ${data[0].title}`);
      }
    } else {
      console.log('✗ 失败:', data);
    }
  } catch (error) {
    console.error('✗ 请求失败:', error);
  }
  console.log('');
}

// 测试获取文章统计
async function testGetArticleStats() {
  console.log('%c[7] 测试 /api/v1/articles/stats/summary...', 'color: #3399ff');

  if (!token) {
    console.log('⚠ 跳过（无 Token）');
    console.log('');
    return;
  }

  try {
    const response = await fetch(`${API_BASE}/articles/stats/summary`, {
      method: 'GET',
      headers: {
        'Authorization': `Bearer ${token}`
      }
    });

    const data = await response.json();
    console.log(`  状态码: ${response.status}`);

    if (response.ok) {
      console.log('✓ 成功');
      console.log('  统计数据:', data);
    } else {
      console.log('✗ 失败:', data);
    }
  } catch (error) {
    console.error('✗ 请求失败:', error);
  }
  console.log('');
}

// 测试获取文件列表
async function testGetFiles() {
  console.log('%c[8] 测试 /api/v1/files/...', 'color: #3399ff');

  if (!token) {
    console.log('⚠ 跳过（无 Token）');
    console.log('');
    return;
  }

  try {
    const response = await fetch(`${API_BASE}/files/`, {
      method: 'GET',
      headers: {
        'Authorization': `Bearer ${token}`
      }
    });

    const data = await response.json();
    console.log(`  状态码: ${response.status}`);

    if (response.ok) {
      console.log('✓ 成功');
      console.log(`  文件数量: ${data.length}`);
    } else {
      console.log('✗ 失败:', data);
    }
  } catch (error) {
    console.error('✗ 请求失败:', error);
  }
  console.log('');
}

// 测试获取文件统计
async function testGetFileStats() {
  console.log('%c[9] 测试 /api/v1/files/stats/summary...', 'color: #3399ff');

  if (!token) {
    console.log('⚠ 跳过（无 Token）');
    console.log('');
    return;
  }

  try {
    const response = await fetch(`${API_BASE}/files/stats/summary`, {
      method: 'GET',
      headers: {
        'Authorization': `Bearer ${token}`
      }
    });

    const data = await response.json();
    console.log(`  状态码: ${response.status}`);

    if (response.ok) {
      console.log('✓ 成功');
      console.log('  统计数据:', data);
    } else {
      console.log('✗ 失败:', data);
    }
  } catch (error) {
    console.error('✗ 请求失败:', error);
  }
  console.log('');
}

// 运行所有测试
async function runAllTests() {
  await testConnection();
  await testRegister();
  await testLogin();
  await testGetMe();
  await testGetAccounts();
  await testGetArticles();
  await testGetArticleStats();
  await testGetFiles();
  await testGetFileStats();

  console.log('========================================');
  console.log('  测试总结');
  console.log('========================================');
  console.log('');
  console.log('✓ 所有测试完成');
  console.log('');
  console.log('前端地址: http://localhost:5176');
  console.log('后端地址: http://localhost:8001');
  console.log('API 文档: http://localhost:8001/docs');
  console.log('');
}

// 执行
runAllTests();
