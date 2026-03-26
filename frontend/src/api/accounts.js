import api from './index'

/**
 * 添加公众号
 */
export function addAccount(data) {
  return api.post('/accounts', data)
}

/**
 * 获取公众号列表
 */
export function getAccounts(params) {
  return api.get('/accounts', { params })
}

/**
 * 获取公众号详情
 */
export function getAccount(id) {
  return api.get(`/accounts/${id}`)
}

/**
 * 更新公众号
 */
export function updateAccount(id, data) {
  return api.put(`/accounts/${id}`, data)
}

/**
 * 删除公众号
 */
export function deleteAccount(id) {
  return api.delete(`/accounts/${id}`)
}

/**
 * 立即抓取公众号
 */
export function triggerCrawl(id) {
  return api.post(`/accounts/${id}/crawl`)
}

/**
 * 切换公众号启用状态
 */
export function toggleAccount(id) {
  return api.put(`/accounts/${id}/toggle`)
}
