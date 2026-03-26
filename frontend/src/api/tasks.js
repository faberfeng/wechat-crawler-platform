import api from './index'

/**
 * 获取任务列表
 */
export function getTasks(params) {
  return api.get('/tasks', { params })
}

/**
 * 获取任务详情
 */
export function getTask(id) {
  return api.get(`/tasks/${id}`)
}
