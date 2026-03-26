<template>
  <div class="file-manage-container">
    <div class="page-header">
      <h1>文件管理</h1>
    </div>

    <el-card class="stats-card">
      <el-row :gutter="20">
        <el-col :xs="24" :sm="12" :md="8">
          <div class="stat-item">
            <span>文件总数: {{ stats.total_count || 0 }}</span>
          </div>
        </el-col>
        <el-col :xs="24" :sm="12" :md="8">
          <div class="stat-item">
            <span>总大小: {{ stats.total_size_formatted || '0 B' }}</span>
          </div>
        </el-col>
        <el-col :xs="24" :sm="12" :md="8">
          <div class="stat-item">
            <el-button type="primary" @click="handleUpload">上传文件</el-button>
          </div>
        </el-col>
      </el-row>
    </el-card>

    <el-card class="list-card">
      <el-table :data="fileList" stripe empty-text="暂无文件">
        <el-table-column label="文件名" min-width="200">
          <template #default="{ row }">
            {{ row.original_filename }}
          </template>
        </el-table-column>

        <el-table-column label="大小" width="100">
          <template #default="{ row }">
            {{ formatFileSize(row.file_size) }}
          </template>
        </el-table-column>

        <el-table-column label="操作" width="200">
          <template #default="{ row }">
            <el-button type="primary" link @click="handleDownload(row)">下载</el-button>
            <el-button type="danger" link @click="handleDelete(row)">删除</el-button>
          </template>
        </el-table-column>
      </el-table>
    </el-card>

    <input
      ref="fileInput"
      type="file"
      style="display: none"
      @change="handleFileChange"
    />
  </div>
</template>

<script setup>
import { ref, onMounted, reactive } from 'vue'
import { ElMessage } from 'element-plus'

const fileList = ref([])
const stats = reactive({
  total_count: 0,
  total_size: 0,
  total_size_formatted: '0 B'
})

const fileInput = ref(null)

const formatFileSize = (size) => {
  for (const unit of ['B', 'KB', 'MB', 'GB']) {
    if (size < 1024.0) {
      return `${size.toFixed(2)} ${unit}`
    }
    size /= 1024.0
  }
  return `${size.toFixed(2)} TB`
}

const loadFiles = () => {
  console.log('Loading files...')
}

const loadStats = () => {
  console.log('Loading stats...')
}

const handleUpload = () => {
  fileInput.value.click()
}

const handleFileChange = (event) => {
  console.log('File change:', event.target.files[0])
  ElMessage.success('上传成功')
}

const handleDownload = (row) => {
  console.log('Download:', row)
  ElMessage.success('开始下载')
}

const handleDelete = (row) => {
  console.log('Delete:', row)
  ElMessage.success('删除成功')
}

onMounted(() => {
  loadStats()
  loadFiles()
})
</script>

<style scoped>
.file-manage-container {
  padding: 20px;
  max-width: 1400px;
  margin: 0 auto;
}

.page-header h1 {
  margin: 0 0 24px 0;
  font-size: 28px;
  font-weight: 600;
}

.stats-card,
.list-card {
  margin-bottom: 20px;
}

.stat-item {
  padding: 16px;
  background: #f5f7fa;
  border-radius: 4px;
}
</style>
