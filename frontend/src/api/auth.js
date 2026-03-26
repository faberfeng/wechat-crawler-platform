/**
 * 认证相关 API
 */
import request from './index'

/**
 * 用户登录
 * @param {string} email - 邮箱
 * @param {string} password - 密码
 * @returns {Promise<Object>}
 */
export const login = async (email, password) => {
  // 使用 FormData 格式（OAuth2 要求）
  const formData = new FormData()
  formData.append('username', email)
  formData.append('password', password)

  return request({
    url: '/auth/login',
    method: 'POST',
    data: formData,
    headers: {
      'Content-Type': 'application/x-www-form-urlencoded'
    }
  })
}

/**
 * 用户注册
 * @param {string} username - 用户名
 * @param {string} email - 邮箱
 * @param {string} password - 密码
 * @returns {Promise<Object>}
 */
export const register = async (username, email, password) => {
  return request({
    url: '/auth/register',
    method: 'POST',
    data: {
      username,
      email,
      password
    }
  })
}

/**
 * 用户登出
 * @returns {Promise<Object>}
 */
export const logout = async () => {
  return request({
    url: '/auth/logout',
    method: 'POST'
  })
}

/**
 * 获取当前用户信息
 * @returns {Promise<Object>}
 */
export const getCurrentUser = async () => {
  return request({
    url: '/auth/me',
    method: 'GET'
  })
}

/**
 * 修改密码
 * @param {string} currentPassword - 当前密码
 * @param {string} newPassword - 新密码
 * @returns {Promise<Object>}
 */
export const changePassword = async (currentPassword, newPassword) => {
  return request({
    url: '/auth/me/password',
    method: 'PATCH',
    data: {
      current_password: currentPassword,
      new_password: newPassword
    }
  })
}

/**
 * 更新个人信息
 * @param {Object} data - 更新数据
 * @param {string} data.username - 用户名（可选）
 * @param {string} data.email - 邮箱（可选）
 * @returns {Promise<Object>}
 */
export const updateProfile = async (data) => {
  return request({
    url: '/auth/me',
    method: 'PATCH',
    data
  })
}

/**
 * 删除当前账号
 * @param {string} password - 密码（用于确认）
 * @returns {Promise<Object>}
 */
export const deleteAccount = async (password) => {
  return request({
    url: '/auth/me',
    method: 'DELETE',
    data: {
      password
    }
  })
}

/**
 * 获取用户列表（仅管理员）
 * @param {Object} params - 查询参数
 * @param {number} params.skip - 跳过数量
 * @param {number} params.limit - 限制数量
 * @returns {Promise<Object>}
 */
export const getUsers = async (params = {}) => {
  return request({
    url: '/users/',
    method: 'GET',
    params
  })
}

/**
 * 获取单个用户信息（仅管理员）
 * @param {number} userId - 用户 ID
 * @returns {Promise<Object>}
 */
export const getUser = async (userId) => {
  return request({
    url: `/users/${userId}/`,
    method: 'GET'
  })
}

/**
 * 创建用户（仅管理员）
 * @param {Object} data - 用户数据
 * @param {string} data.username - 用户名
 * @param {string} data.email - 邮箱
 * @param {string} data.password - 密码
 * @param {string} data.role - 角色
 * @returns {Promise<Object>}
 */
export const createUser = async (data) => {
  return request({
    url: '/users/',
    method: 'POST',
    data
  })
}

/**
 * 更新用户（仅管理员）
 * @param {number} userId - 用户 ID
 * @param {Object} data - 更新数据
 * @returns {Promise<Object>}
 */
export const updateUser = async (userId, data) => {
  return request({
    url: `/users/${userId}/`,
    method: 'PATCH',
    data
  })
}

/**
 * 删除用户（仅管理员）
 * @param {number} userId - 用户 ID
 * @returns {Promise<Object>}
 */
export const deleteUser = async (userId) => {
  return request({
    url: `/users/${userId}/`,
    method: 'DELETE'
  })
}
