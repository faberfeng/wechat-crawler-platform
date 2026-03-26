<template>
  <div class="login-container">
    <transition name="slide-up" appear>
      <div class="login-box">
        <div class="login-header">
          <h1>微信公众号抓取平台</h1>
          <p>欢迎回来</p>
        </div>

        <el-form
          ref="loginFormRef"
          :model="loginForm"
          :rules="loginRules"
          class="login-form"
          @submit.prevent="handleLogin"
        >
          <el-form-item prop="email">
            <el-input
              v-model="loginForm.email"
              placeholder="请输入邮箱"
              size="large"
              prefix-icon="Message"
              clearable
              @blur="validateField(loginFormRef, 'email')"
            />
            <FormValidator
              :type="getValidatorType('email')"
              :message="getValidatorMessage('email')"
            />
          </el-form-item>

          <el-form-item prop="password">
            <el-input
              v-model="loginForm.password"
              type="password"
              placeholder="请输入密码"
              size="large"
              prefix-icon="Lock"
              show-password
              clearable
              @keyup.enter="handleLogin"
              @blur="validateField(loginFormRef, 'password')"
            />
            <FormValidator
              :type="getValidatorType('password')"
              :message="getValidatorMessage('password')"
            />
          </el-form-item>

          <el-form-item class="login-actions">
            <el-checkbox v-model="rememberMe" class="remember-checkbox">
              记住我
            </el-checkbox>
            <el-link type="primary" :underline="false" class="forgot-link">
              忘记密码？
            </el-link>
          </el-form-item>

          <el-form-item>
            <el-button
              type="primary"
              size="large"
              :loading="loading"
              class="login-button"
              @click="handleLogin"
            >
              {{ loading ? '登录中...' : '登录' }}
            </el-button>
          </el-form-item>
        </el-form>

        <div class="login-footer">
          <span>还没有账号？</span>
          <router-link to="/register" class="link">立即注册</router-link>
        </div>
      </div>
    </transition>
  </div>
</template>

<script setup>
import { ref, reactive } from 'vue'
import { useRouter } from 'vue-router'
import { ElMessage } from 'element-plus'
import { useAuthStore } from '@/stores/auth'
import FormValidator from '@/components/FormValidator.vue'

const router = useRouter()
const authStore = useAuthStore()

// 登录表单
const loginForm = reactive({
  email: '',
  password: ''
})

// 表单验证规则
const loginRules = {
  email: [
    { required: true, message: '请输入邮箱', trigger: 'blur' },
    { type: 'email', message: '请输入正确的邮箱格式', trigger: 'blur' }
  ],
  password: [
    { required: true, message: '请输入密码', trigger: 'blur' },
    { min: 6, message: '密码长度不能少于 6 位', trigger: 'blur' }
  ]
}

const loginFormRef = ref(null)
const loading = ref(false)
const rememberMe = ref(false)

// 字段验证状态
const fieldValidation = reactive({
  email: { isValid: false, message: '', isTouched: false },
  password: { isValid: false, message: '', isTouched: false }
})

// 获取验证器类型
const getValidatorType = (field) => {
  const validation = fieldValidation[field]
  if (!validation.isTouched) return ''
  return validation.isValid ? 'success' : 'error'
}

// 获取验证器消息
const getValidatorMessage = (field) => {
  const validation = fieldValidation[field]
  if (!validation.isTouched) return ''
  return validation.isValid ? '格式正确' : validation.message
}

// 验证字段
const validateField = async (formRef, field) => {
  fieldValidation[field].isTouched = true

  try {
    if (formRef) {
      await formRef.validateField(field)
      fieldValidation[field].isValid = true
      fieldValidation[field].message = ''
    }
  } catch (error) {
    fieldValidation[field].isValid = false
    fieldValidation[field].message = error.message || ''
  }
}

// 处理登录
const handleLogin = async () => {
  if (!loginFormRef.value) return

  try {
    // 标记所有字段为已触摸
    fieldValidation.email.isTouched = true
    fieldValidation.password.isTouched = true

    // 表单验证
    await loginFormRef.value.validate()

    loading.value = true

    // 调用登录接口
    await authStore.handleLogin(loginForm.email, loginForm.password)

    ElMessage.success({
      message: '登录成功',
      duration: 2000,
      showClose: true
    })

    // 跳转到首页
    setTimeout(() => {
      router.push('/')
    }, 500)
  } catch (error) {
    if (error !== false) {
      ElMessage.error({
        message: authStore.error || '登录失败，请检查邮箱和密码',
        duration: 3000,
        showClose: true
      })
    }
  } finally {
    loading.value = false
  }
}
</script>

<style scoped>
.login-container {
  display: flex;
  justify-content: center;
  align-items: center;
  min-height: 100vh;
  background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
  position: relative;
  overflow: hidden;
}

/* 背景装饰 */
.login-container::before,
.login-container::after {
  content: '';
  position: absolute;
  border-radius: 50%;
  background: rgba(255, 255, 255, 0.1);
}

.login-container::before {
  width: 400px;
  height: 400px;
  top: -200px;
  right: -100px;
}

.login-container::after {
  width: 300px;
  height: 300px;
  bottom: -150px;
  left: -100px;
}

.login-box {
  width: 100%;
  max-width: 400px;
  padding: 40px;
  background: white;
  border-radius: 16px;
  box-shadow: 0 20px 60px rgba(0, 0, 0, 0.2);
  position: relative;
  z-index: 1;
  backdrop-filter: blur(10px);
  background: rgba(255, 255, 255, 0.95);
}

.login-header {
  text-align: center;
  margin-bottom: 40px;
}

.login-header h1 {
  margin: 0 0 10px 0;
  font-size: 28px;
  font-weight: 600;
  color: #1a1a1a;
  background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
  -webkit-background-clip: text;
  -webkit-text-fill-color: transparent;
  background-clip: text;
}

.login-header p {
  margin: 0;
  font-size: 16px;
  color: #86909c;
}

.login-form {
  margin-bottom: 30px;
}

.login-actions {
  margin-bottom: 10px;
}

.remember-checkbox {
  font-size: 14px;
  color: #606266;
}

.forgot-link {
  float: right;
  font-size: 14px;
  color: #667eea;
  text-decoration: none;
  transition: all 0.3s ease;
}

.forgot-link:hover {
  color: #764ba2;
  text-decoration: underline;
}

.login-button {
  width: 100%;
  font-size: 16px;
  font-weight: 500;
  height: 44px;
  background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
  border: none;
  transition: all 0.3s ease;
}

.login-button:hover {
  transform: translateY(-2px);
  box-shadow: 0 8px 20px rgba(102, 126, 234, 0.4);
}

.login-button:active {
  transform: translateY(0);
}

.login-footer {
  text-align: center;
  font-size: 14px;
  color: #86909c;
}

.link {
  color: #667eea;
  text-decoration: none;
  font-weight: 500;
  transition: all 0.3s ease;
}

.link:hover {
  color: #764ba2;
  text-decoration: underline;
}

/* 响应式设计 */
@media (max-width: 576px) {
  .login-box {
    max-width: 90%;
    padding: 30px 20px;
  }

  .login-header h1 {
    font-size: 24px;
  }

  .login-header p {
    font-size: 14px;
  }
}
</style>
