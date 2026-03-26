/**
 * 文章管理 API
 */

import request from './index'

/**
 * 获取文章列表
 * @param {Object} params 查询参数
 * @param {number} params.account_id 公众号 ID
 * @param {string} params.keyword 搜索关键词
 * @param {string} params.start_date 开始日期
 * @param {string} params.end_date 结束日期
 * @param {number} params.page 页码
 * @param {number} params.page_size 每页数量
 * @returns {Promise}
 */
export const getArticleList = (params = {}) => {
  return request({
    url: '/articles',
    method: 'GET',
    params
  })
}

/**
 * 获取文章详情
 * @param {number} articleId 文章 ID
 * @returns {Promise}
 */
export const getArticle = (articleId) => {
  return request({
    url: `/articles/${articleId}`,
    method: 'GET'
  })
}

/**
 * 获取文章 Markdown 内容
 * @param {number} articleId 文章 ID
 * @returns {Promise}
 */
export const getArticleMarkdown = (articleId) => {
  return request({
    url: `/articles/${articleId}/markdown`,
    method: 'GET'
  })
}

/**
 * 删除文章
 * @param {number} articleId 文章 ID
 * @returns {Promise}
 */
export const deleteArticle = (articleId) => {
  return request({
    url: `/articles/${articleId}`,
    method: 'DELETE'
  })
}

/**
 * 获取统计数据
 * @returns {Promise}
 */
export const getArticleStats = () => {
  return request({
    url: '/articles/stats/summary',
    method: 'GET'
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
 * 格式化数字
 * @param {number} num 数字
 * @returns {string} 格式化后的数字
 */
export const formatNumber = (num) => {
  if (num === null || num === undefined) return '0'
  if (num >= 10000) {
    return (num / 10000).toFixed(1) + 'w'
  }
  return num.toString()
}

/**
 * 打开文章链接
 * @param {string} url 文章链接
 */
export const openArticleUrl = (url) => {
  if (url) {
    window.open(url, '_blank')
  }
}
