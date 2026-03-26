import api from './index'

/**
 * 获取文章列表
 */
export function getArticles(params) {
  return api.get('/articles', { params })
}

/**
 * 获取文章详情
 */
export function getArticle(id) {
  return api.get(`/articles/${id}`)
}

/**
 * 获取文章 Markdown 内容
 */
export function getArticleMarkdown(id) {
  return api.get(`/articles/${id}/markdown`)
}

/**
 * 删除文章
 */
export function deleteArticle(id) {
  return api.delete(`/articles/${id}`)
}

/**
 * 获取统计数据
 */
export function getStats() {
  return api.get('/articles/stats/summary')
}
