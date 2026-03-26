/**
 * 认证状态管理
 * 使用 Pinia 管理用户认证状态
 */
import { defineStore } from 'pinia'
import { ref } from 'vue'
import { login, register, logout, getCurrentUser } from '@/api/auth'

export const useAuthStore = defineStore('auth', () => {
  // 状态
  const user = ref(null)
  const token = ref(localStorage.getItem('token') || null)
  const isAuthenticated = ref(!!localStorage.getItem('token'))
  const loading = ref(false)
  const error = ref(null)

  /**
   * 用户登录
   */
  const handleLogin = async (email, password) => {
    loading.value = true
    error.value = null

    try {
      const response = await login(email, password)
      token.value = response.access_token
      user.value = response.user
      isAuthenticated.value = true

      // 存储到 localStorage
      localStorage.setItem('token', response.access_token)
      localStorage.setItem('user', JSON.stringify(response.user))

      return response
    } catch (err) {
      error.value = err.response?.data?.detail || err.message || '登录失败'
      throw error.value
    } finally {
      loading.value = false
    }
  }

  /**
   * 用户注册
   */
  const handleRegister = async (username, email, password) => {
    loading.value = true
    error.value = null

    try {
      const response = await register(username, email, password)
      return response
    } catch (err) {
      error.value = err.response?.data?.detail || err.message || '注册失败'
      throw error.value
    } finally {
      loading.value = false
    }
  }

  /**
   * 用户登出
   */
  const handleLogout = async () => {
    loading.value = true
    error.value = null

    try {
      await logout()
    } catch (err) {
      console.error('Logout error:', err)
    } finally {
      // 清除状态
      token.value = null
      user.value = null
      isAuthenticated.value = false
      loading.value = false

      // 清除 localStorage
      localStorage.removeItem('token')
      localStorage.removeItem('user')
    }
  }

  /**
   * 获取当前用户信息
   */
  const fetchCurrentUser = async () => {
    loading.value = true
    error.value = null

    try {
      const response = await getCurrentUser()
      user.value = response
      isAuthenticated.value = true

      // 更新 localStorage
      localStorage.setItem('user', JSON.stringify(response))

      return response
    } catch (err) {
      error.value = err.response?.data?.detail || err.message || '获取用户信息失败'
      // 如果获取用户信息失败，可能是 token 过期，清除认证状态
      await handleLogout()
      throw error.value
    } finally {
      loading.value = false
    }
  }

  /**
   * 初始化认证状态（从 localStorage 恢复）
   */
  const initializeAuth = () => {
    const savedToken = localStorage.getItem('token')
    const savedUser = localStorage.getItem('user')

    if (savedToken) {
      token.value = savedToken
      isAuthenticated.value = true

      if (savedUser) {
        try {
          user.value = JSON.parse(savedUser)
        } catch (err) {
          console.error('Failed to parse saved user:', err)
        }
      }
    }
  }

  /**
   * 检查是否为管理员
   */
  const isAdmin = () => {
    return user.value?.role === 'admin'
  }

  /**
   * 清除错误
   */
  const clearError = () => {
    error.value = null
  }

  return {
    // 状态
    user,
    token,
    isAuthenticated,
    loading,
    error,

    // 方法
    handleLogin,
    handleRegister,
    handleLogout,
    fetchCurrentUser,
    initializeAuth,
    isAdmin,
    clearError
  }
})
