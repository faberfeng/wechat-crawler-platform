/**
 * 任务管理 API
 */

import request from './index'
import { formatDate } from './accounts'

/**
 * 获取任务列表
 * @param {Object} params 查询参数
 * @param {number} params.account_id 公众号 ID
 * @param {string} params.status 任务状态
 * @param {number} params.page 页码
 * @param {number} params.page_size 每页数量
 * @returns {Promise}
 */
export const getTaskList = (params = {}) => {
  return request({
    url: '/tasks',
    method: 'GET',
    params
  })
}

/**
 * 获取任务详情
 * @param {number} taskId 任务 ID
 * @returns {Promise}
 */
export const getTask = (taskId) => {
  return request({
    url: `/tasks/${taskId}`,
    method: 'GET'
  })
}

/**
 * 健康检查
 * @param {number} accountId 公众号 ID
 * @returns {Promise}
 */
export const healthCheck = (accountId) => {
  return request({
    url: '/tasks/health-check',
    method: 'POST',
    params: { account_id: accountId }
  })
}

/**
 * 格式化日期（重导出）
 */
export { formatDate }

/**
 * 获取状态配置
 * @param {string} status 任务状态
 * @returns {Object} 状态配置
 */
export const getStatusConfig = (status) => {
  const configs = {
    pending: { type: 'info', label: '等待中', color: '#909399', icon: 'Clock' },
    running: { type: 'warning', label: '运行中', color: '#e6a23c', icon: 'Loading' },
    success: { type: 'success', label: '成功', color: '#67c23a', icon: 'Select' },
    failed: { type: 'danger', label: '失败', color: '#f56c6c', icon: 'CloseBold' }
  }

  return configs[status] || configs.pending
}

/**
 * 计算任务耗时
 * @param {string} startTime 开始时间
 * @param {string} endTime 结束时间
 * @returns {string} 耗时字符串
 */
export const calculateDuration = (startTime, endTime) => {
  if (!startTime || !endTime) return '-'

  const start = new Date(startTime)
  const end = new Date(endTime)
  const diff = Math.floor((end - start) / 1000) // 秒

  if (diff < 60) {
    return `${diff}秒`
  } else if (diff < 3600) {
    return `${Math.floor(diff / 60)}分钟`
  } else {
    const hours = Math.floor(diff / 3600)
    const minutes = Math.floor((diff % 3600) / 60)
    return `${hours}小时${minutes}分钟`
  }
}
