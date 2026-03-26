import axios from 'axios'
import { ElMessage } from 'element-plus'
import { useAuthStore } from '@/stores/auth'

// 根据 environment 自动选择 API baseURL
const getApiBaseURL = () => {
  const hostname = window.location.hostname

  // 公网环境 - LocalTunnel
  if (hostname === 'wechat-crawler-fwb.loca.lt') {
    return 'https://wechat-crawler-api.loca.lt/api/v1'
  }

  // 本地开发环境
  if (hostname === 'localhost' || hostname === '127.0.0.1') {
    return 'http://localhost:8002/api/v1'
  }

  // 其他环境默认使用本地
  return 'http://localhost:8002/api/v1'
}

const api = axios.create({
  baseURL: getApiBaseURL(),
  timeout: 30000
})

// 请求拦截器
api.interceptors.request.use(
  config => {
    // 自动添加 Authorization 头
    const authStore = useAuthStore()
    if (authStore.token) {
      config.headers.Authorization = `Bearer ${authStore.token}`
    }
    return config
  },
  error => {
    return Promise.reject(error)
  }
)

// 响应拦截器
api.interceptors.response.use(
  response => {
    return response.data
  },
  error => {
    const authStore = useAuthStore()

    // 处理 401 未授权错误
    if (error.response?.status === 401) {
      ElMessage.error('登录已过期，请重新登录')
      authStore.handleLogout()
      // 跳转到登录页
      window.location.href = '/login'
      return Promise.reject(error)
    }

    // 处理 403 权限错误
    if (error.response?.status === 403) {
      ElMessage.error('权限不足')
      return Promise.reject(error)
    }

    // 处理其他错误
    const message = error.response?.data?.detail || error.message || '请求失败'
    ElMessage.error(message)

    return Promise.reject(error)
  }
)

export default api
