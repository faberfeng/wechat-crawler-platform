/**
 * 公众号管理 API
 */

import request from './index'

/**
 * 添加公众号
 * @param {Object} data 公众号数据
 * @param {string} data.url 公众号文章链接
 * @param {string} data.name 公众号名称
 * @returns {Promise}
 */
export const createAccount = (data) => {
  return request({
    url: '/accounts',
    method: 'POST',
    data
  })
}

/**
 * 获取公众号列表
 * @param {Object} params 查询参数
 * @param {number} params.skip 跳过数量
 * @param {number} params.limit 返回数量
 * @param {boolean} params.active_only 仅返回活跃公众号
 * @returns {Promise}
 */
export const getAccountList = (params = {}) => {
  return request({
    url: '/accounts',
    method: 'GET',
    params
  })
}

/**
 * 获取公众号详情
 * @param {number} accountId 公众号 ID
 * @returns {Promise}
 */
export const getAccount = (accountId) => {
  return request({
    url: `/accounts/${accountId}`,
    method: 'GET'
  })
}

/**
 * 更新公众号
 * @param {number} accountId 公众号 ID
 * @param {Object} data 更新数据
 * @returns {Promise}
 */
export const updateAccount = (accountId, data) => {
  return request({
    url: `/accounts/${accountId}`,
    method: 'PUT',
    data
  })
}

/**
 * 删除公众号
 * @param {number} accountId 公众号 ID
 * @returns {Promise}
 */
export const deleteAccount = (accountId) => {
  return request({
    url: `/accounts/${accountId}`,
    method: 'DELETE'
  })
}

/**
 * 切换公众号启用状态
 * @param {number} accountId 公众号 ID
 * @returns {Promise}
 */
export const toggleAccount = (accountId) => {
  return request({
    url: `/accounts/${accountId}/toggle`,
    method: 'PUT'
  })
}

/**
 * 触发抓取
 * @param {number} accountId 公众号 ID
 * @returns {Promise}
 */
export const triggerCrawl = (accountId) => {
  return request({
    url: `/accounts/${accountId}/crawl`,
    method: 'POST'
  })
}

/**
 * 格式化日期
 * @param {string} dateStr 日期字符串
 * @returns {string} 格式化后的日期
 */
export const formatDate = (dateStr) => {
  if (!dateStr) return '-'

  const date = new Date(dateStr)
  const year = date.getFullYear()
  const month = String(date.getMonth() + 1).padStart(2, '0')
  const day = String(date.getDate()).padStart(2, '0')
  const hours = String(date.getHours()).padStart(2, '0')
  const minutes = String(date.getMinutes()).padStart(2, '0')

  return `${year}-${month}-${day} ${hours}:${minutes}`
}

/**
 * 获取状态配置
 * @param {boolean} isActive 是否活跃
 * @returns {Object} 状态配置
 */
export const getStatusConfig = (isActive) => {
  return isActive
    ? { type: 'success', label: '已启用', color: '#67c23a' }
    : { type: 'info', label: '已禁用', color: '#909399' }
}
