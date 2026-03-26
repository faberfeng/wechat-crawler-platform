/**
 * 统计数据 API
 */

import request from './index'

/**
 * 获取统计数据
 * @returns {Promise}
 */
export const getStats = () => {
  return request({
    url: '/articles/stats/summary',
    method: 'GET'
  })
}

/**
 * 获取最近文章
 * @param {number} limit 数量限制
 * @returns {Promise}
 */
export const getRecentArticles = (limit = 5) => {
  return request({
    url: '/articles',
    method: 'GET',
    params: {
      page: 1,
      page_size: limit
    }
  })
}

/**
 * 获取公众号统计
 * @param {boolean} activeOnly 仅统计活跃公众号
 * @returns {Promise}
 */
export const getAccountStats = (activeOnly = true) => {
  return request({
    url: '/accounts',
    method: 'GET',
    params: {
      active_only: activeOnly,
      limit: 100
    }
  })
}
