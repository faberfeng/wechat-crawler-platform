/**
 * 文件管理 API
 */

import request from './index'

export const uploadFile = (file) => {
  const formData = new FormData()
  formData.append('file', file)
  return request({
    url: '/files/upload',
    method: 'POST',
    data: formData,
    headers: {
      'Content-Type': 'multipart/form-data'
    }
  })
}

export const getFileList = (params = {}) => {
  return request({
    url: '/files/',
    method: 'GET',
    params
  })
}

export const getFileInfo = (fileId) => {
  return request({
    url: `/files/${fileId}`,
    method: 'GET'
  })
}

export const downloadFile = (fileId) => {
  return `${request.defaults.baseURL}/files/${fileId}/download`
}

export const previewFile = (fileId) => {
  return `${request.defaults.baseURL}/files/${fileId}/preview`
}

export const deleteFile = (fileId) => {
  return request({
    url: `/files/${fileId}`,
    method: 'DELETE'
  })
}

export const getFileStats = () => {
  return request({
    url: '/files/stats/summary',
    method: 'GET'
  })
}

export const formatFileSize = (size) => {
  for (const unit of ['B', 'KB', 'MB', 'GB']) {
    if (size < 1024.0) {
      return `${size.toFixed(2)} ${unit}`
    }
    size /= 1024.0
  }
  return `${size.toFixed(2)} TB`
}

export const getCategoryConfig = (category) => {
  const configs = {
    image: { type: 'success', label: '图片', color: '#67c23a' },
    document: { type: 'primary', label: '文档', color: '#409eff' },
    archive: { type: 'warning', label: '压缩包', color: '#e6a23c' },
    other: { type: 'info', label: '其他', color: '#909399' }
  }
  return configs[category] || configs.other
}
