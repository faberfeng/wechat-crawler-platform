/**
 * 抓取相关 API
 */

import request from './index'

/**
 * 抓取单个 URL 的文章内容
 * @param {string} url 文章 URL
 * @param {number} userId 用户 ID
 * @returns {Promise}
 */
export const crawlSingleUrl = (url, userId = null) => {
  return request({
    url: '/crawl/url',
    method: 'POST',
    data: {
      url,
      user_id: userId
    }
  })
}

/**
 * 批量抓取多个 URL
 * @param {Array} urls URL 列表
 * @param {number} userId 用户 ID
 * @returns {Promise}
 */
export const crawlUrlsBatch = (urls, userId = null) => {
  return request({
    url: '/crawl/batch',
    method: 'POST',
    data: {
      urls,
      user_id: userId
    }
  })
}

/**
 * 抓取微信文章
 * @param {string} url 微信文章 URL
 * @param {number} accountId 公众号 ID（可选）
 * @param {number} userId 用户 ID
 * @returns {Promise}
 */
export const crawlWeChatArticle = (url, accountId = null, userId = null) => {
  return request({
    url: '/crawl/wechat',
    method: 'POST',
    data: {
      url,
      account_id: accountId,
      user_id: userId
    }
  })
}

/**
 * 获取文章的 Markdown 内容
 * @param {number} articleId 文章 ID
 * @returns {Promise}
 */
export const getArticleMarkdown = (articleId) => {
  return request({
    url: `/articles/${articleId}/markdown`,
    method: 'GET'
  })
}
