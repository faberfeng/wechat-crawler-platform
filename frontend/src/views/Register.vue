<template>
  <div class="register-container">
    <transition name="slide-up" appear>
      <div class="register-box">
        <div class="register-header">
          <h1>创建账号</h1>
          <p>加入微信公众号抓取平台</p>
        </div>

        <el-form
          ref="registerFormRef"
          :model="registerForm"
          :rules="registerRules"
          class="register-form"
          @submit.prevent="handleRegister"
        >
          <el-form-item prop="username">
            <el-input
              v-model="registerForm.username"
              placeholder="请输入用户名"
              size="large"
              prefix-icon="User"
              clearable
              @blur="validateField(registerFormRef, 'username')"
            />
            <FormValidator
              :type="getValidatorType('username')"
              :message="getValidatorMessage('username')"
            />
          </el-form-item>

          <el-form-item prop="email">
            <el-input
              v-model="registerForm.email"
              placeholder="请输入邮箱"
              size="large"
              prefix-icon="Message"
              clearable
              @blur="validateField(registerFormRef, 'email')"
            />
            <FormValidator
              :type="getValidatorType('email')"
              :message="getValidatorMessage('email')"
            />
          </el-form-item>

          <el-form-item prop="password">
            <el-input
              v-model="registerForm.password"
              type="password"
              placeholder="请输入密码（至少 6 位）"
              size="large"
              prefix-icon="Lock"
              show-password
              clearable
              @blur="validateField(registerFormRef, 'password')"
            />
            <FormValidator
              :type="getValidatorType('password')"
              :message="getValidatorMessage('password')"
            />
            <div v-if="registerForm.password" class="password-strength">
              <div class="password-strength-bar">
                <div
                  class="password-strength-fill"
                  :class="passwordStrengthClass"
                  :style="{ width: passwordStrength.width }"
                ></div>
              </div>
              <span class="password-strength-text">{{ passwordStrength.text }}</span>
            </div>
          </el-form-item>

          <el-form-item prop="confirmPassword">
            <el-input
              v-model="registerForm.confirmPassword"
              type="password"
              placeholder="请再次输入密码"
              size="large"
              prefix-icon="Lock"
              show-password
              clearable
              @keyup.enter="handleRegister"
              @blur="validateField(registerFormRef, 'confirmPassword')"
            />
            <FormValidator
              :type="getValidatorType('confirmPassword')"
              :message="getValidatorMessage('confirmPassword')"
            />
          </el-form-item>

          <el-form-item class="register-actions">
            <el-checkbox v-model="agreeTerms" class="agree-checkbox">
              我已阅读并同意
              <el-link type="primary" :underline="false">服务条款</el-link>
              和
              <el-link type="primary" :underline="false">隐私政策</el-link>
            </el-checkbox>
          </el-form-item>

          <el-form-item>
            <el-button
              type="primary"
              size="large"
              :loading="loading"
              :disabled="!agreeTerms"
              class="register-button"
              @click="handleRegister"
            >
              {{ loading ? '注册中...' : '注册' }}
            </el-button>
          </el-form-item>
        </el-form>

        <div class="register-footer">
          <span>已有账号？</span>
          <router-link to="/login" class="link">立即登录</router-link>
        </div>
      </div>
    </transition>
  </div>
</template>

<script setup>
import { ref, reactive, computed } from 'vue'
import { useRouter } from 'vue-router'
import { ElMessage } from 'element-plus'
import { useAuthStore } from '@/stores/auth'
import FormValidator from '@/components/FormValidator.vue'

const router = useRouter()
const authStore = useAuthStore()

// 注册表单
const registerForm = reactive({
  username: '',
  email: '',
  password: '',
  confirmPassword: ''
})

// 自定义验证规则：确认密码
const validateConfirmPassword = (rule, value, callback) => {
  if (value === '') {
    callback(new Error('请再次输入密码'))
  } else if (value !== registerForm.password) {
    callback(new Error('两次输入的密码不一致'))
  } else {
    callback()
  }
}

// 表单验证规则
const registerRules = {
  username: [
    { required: true, message: '请输入用户名', trigger: 'blur' },
    { min: 3, max: 20, message: '用户名长度在 3 到 20 个字符', trigger: 'blur' }
  ],
  email: [
    { required: true, message: '请输入邮箱', trigger: 'blur' },
    { type: 'email', message: '请输入正确的邮箱格式', trigger: 'blur' }
  ],
  password: [
    { required: true, message: '请输入密码', trigger: 'blur' },
    { min: 6, message: '密码长度不能少于 6 位', trigger: 'blur' }
  ],
  confirmPassword: [
    { required: true, validator: validateConfirmPassword, trigger: 'blur' }
  ]
}

const registerFormRef = ref(null)
const loading = ref(false)
const agreeTerms = ref(false)

// 字段验证状态
const fieldValidation = reactive({
  username: { isValid: false, message: '', isTouched: false },
  email: { isValid: false, message: '', isTouched: false },
  password: { isValid: false, message: '', isTouched: false },
  confirmPassword: { isValid: false, message: '', isTouched: false }
})

// 密码强度
const passwordStrength = computed(() => {
  const password = registerForm.password

  if (!password) {
    return { width: '0%', text: '', class: '' }
  }

  let strength = 0
  if (password.length >= 6) strength++
  if (password.length >= 8) strength++
  if (/[A-Z]/.test(password)) strength++
  if (/[0-9]/.test(password)) strength++
  if (/[^A-Za-z0-9]/.test(password)) strength++

  if (strength <= 2) {
    return { width: '33%', text: '弱', class: 'weak' }
  } else if (strength <= 4) {
    return { width: '66%', text: '中', class: 'medium' }
  } else {
    return { width: '100%', text: '强', class: 'strong' }
  }
})

const passwordStrengthClass = computed(() => {
  return passwordStrength.value.class
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

// 处理注册
const handleRegister = async () => {
  if (!agreeTerms.value) {
    ElMessage.warning('请先同意服务条款和隐私政策')
    return
  }

  if (!registerFormRef.value) return

  try {
    // 标记所有字段为已触摸
    Object.keys(fieldValidation).forEach(key => {
      fieldValidation[key].isTouched = true
    })

    // 表单验证
    await registerFormRef.value.validate()

    loading.value = true

    // 调用注册接口
    await authStore.handleRegister(
      registerForm.username,
      registerForm.email,
      registerForm.password
    )

    ElMessage.success({
      message: '注册成功，请登录',
      duration: 2000,
      showClose: true
    })

    // 跳转到登录页
    setTimeout(() => {
      router.push('/login')
    }, 500)
  } catch (error) {
    if (error !== false) {
      ElMessage.error({
        message: authStore.error || '注册失败，请检查输入信息',
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
.register-container {
  display: flex;
  justify-content: center;
  align-items: center;
  min-height: 100vh;
  background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
  position: relative;
  overflow: hidden;
  padding: 20px;
}

/* 背景装饰 */
.register-container::before,
.register-container::after {
  content: '';
  position: absolute;
  border-radius: 50%;
  background: rgba(255, 255, 255, 0.1);
}

.register-container::before {
  width: 400px;
  height: 400px;
  top: -200px;
  right: -100px;
}

.register-container::after {
  width: 300px;
  height: 300px;
  bottom: -150px;
  left: -100px;
}

.register-box {
  width: 100%;
  max-width: 450px;
  padding: 40px;
  background: white;
  border-radius: 16px;
  box-shadow: 0 20px 60px rgba(0, 0, 0, 0.2);
  position: relative;
  z-index: 1;
  backdrop-filter: blur(10px);
  background: rgba(255, 255, 255, 0.95);
}

.register-header {
  text-align: center;
  margin-bottom: 40px;
}

.register-header h1 {
  margin: 0 0 10px 0;
  font-size: 28px;
  font-weight: 600;
  color: #1a1a1a;
  background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
  -webkit-background-clip: text;
  -webkit-text-fill-color: transparent;
  background-clip: text;
}

.register-header p {
  margin: 0;
  font-size: 16px;
  color: #86909c;
}

.register-form {
  margin-bottom: 30px;
}

.register-actions {
  margin-bottom: 10px;
}

.agree-checkbox {
  font-size: 14px;
  color: #606266;
  line-height: 1.5;
}

.agree-checkbox :deep(.el-checkbox__label) {
  white-space: normal;
}

.password-strength {
  margin-top: 8px;
  padding: 12px;
  background: #f5f7fa;
  border-radius: 8px;
}

.password-strength-bar {
  height: 6px;
  background: #e4e7ed;
  border-radius: 3px;
  overflow: hidden;
  margin-bottom: 8px;
}

.password-strength-fill {
  height: 100%;
  transition: all 0.3s ease;
}

.password-strength-fill.weak {
  background: #f56c6c;
}

.password-strength-fill.medium {
  background: #e6a23c;
}

.password-strength-fill.strong {
  background: #67c23a;
}

.password-strength-text {
  font-size: 12px;
  color: #909399;
}

.register-button {
  width: 100%;
  font-size: 16px;
  font-weight: 500;
  height: 44px;
  background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
  border: none;
  transition: all 0.3s ease;
}

.register-button:hover:not(:disabled) {
  transform: translateY(-2px);
  box-shadow: 0 8px 20px rgba(102, 126, 234, 0.4);
}

.register-button:active:not(:disabled) {
  transform: translateY(0);
}

.register-button:disabled {
  opacity: 0.6;
  cursor: not-allowed;
}

.register-footer {
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
  .register-box {
    max-width: 95%;
    padding: 30px 20px;
  }

  .register-header h1 {
    font-size: 24px;
  }

  .register-header p {
    font-size: 14px;
  }

  .agree-checkbox {
    font-size: 12px;
  }
}
</style>
