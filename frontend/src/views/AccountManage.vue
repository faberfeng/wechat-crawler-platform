<template>
  <div class="account-manage-container">
    <!-- 页面标题 -->
    <div class="page-header">
      <h1>公众号管理</h1>
      <p>添加和管理微信公众号</p>
    </div>

    <!-- 操作栏 -->
    <el-card class="action-card">
      <el-row :gutter="20" align="middle">
        <el-col :xs="24" :sm="12" :md="8">
          <el-button
            type="primary"
            :icon="Plus"
            @click="handleAdd"
            style="width: 100%"
          >
            添加公众号
          </el-button>
        </el-col>

        <el-col :xs="24" :sm="12" :md="8">
          <el-switch
            v-model="activeOnly"
            active-text="仅显示已启用"
            @change="loadAccounts"
            style="width: 100%"
          />
        </el-col>

        <el-col :xs="24" :sm="24" :md="8" style="text-align: right">
          <el-button
            :icon="Refresh"
            @click="loadAccounts"
            :loading="loading"
          >
            刷新
          </el-button>
        </el-col>
      </el-row>
    </el-card>

    <!-- 公众号列表 -->
    <el-card class="list-card">
      <el-skeleton :loading="loading" :rows="5" animated>
        <el-table
          :data="accountList"
          stripe
          v-loading="loading"
          empty-text="暂无公众号"
        >
          <el-table-column label="公众号" min-width="150">
            <template #default="{ row }">
              <div class="account-info">
                <el-avatar
                  :src="row.avatar_url"
                  :size="40"
                  style="margin-right: 12px"
                >
                  {{ row.name.charAt(0) }}
                </el-avatar>
                <div>
                  <div class="account-name">{{ row.name }}</div>
                  <div class="account-biz">{{ row.biz }}</div>
                </div>
              </div>
            </template>
          </el-table-column>

          <el-table-column label="文章数" width="100" align="center">
            <template #default="{ row }">
              <el-tag type="info">{{ row.article_count }}</el-tag>
            </template>
          </el-table-column>

          <el-table-column label="状态" width="120" align="center">
            <template #default="{ row }">
              <el-tag :type="getStatusConfig(row.is_active).type">
                {{ getStatusConfig(row.is_active).label }}
              </el-tag>
            </template>
          </el-table-column>

          <el-table-column label="最后抓取" width="150">
            <template #default="{ row }">
              {{ formatDate(row.last_crawl_time) }}
            </template>
          </el-table-column>

          <el-table-column label="操作" width="250" fixed="right">
            <template #default="{ row }">
              <el-button
                type="primary"
                link
                :icon="VideoPlay"
                @click="handleCrawl(row)"
                :disabled="!row.is_active"
              >
                抓取
              </el-button>
              <el-button
                type="warning"
                link
                :icon="Switch"
                @click="handleToggle(row)"
              >
                {{ row.is_active ? '禁用' : '启用' }}
              </el-button>
              <el-button
                type="danger"
                link
                :icon="Delete"
                @click="handleDelete(row)"
              >
                删除
              </el-button>
            </template>
          </el-table-column>
        </el-table>
      </el-skeleton>
    </el-card>

    <!-- 添加公众号对话框 -->
    <el-dialog
      v-model="addDialogVisible"
      title="添加公众号"
      width="500px"
    >
      <el-form :model="formData" :rules="rules" ref="formRef" label-width="100px">
        <el-form-item label="公众号名称" prop="name">
          <el-input
            v-model="formData.name"
            placeholder="请输入公众号名称（可选）"
            clearable
          />
        </el-form-item>

        <el-form-item label="文章链接" prop="url">
          <el-input
            v-model="formData.url"
            type="textarea"
            :rows="3"
            placeholder="请输入公众号任意文章链接"
          />
        </el-form-item>

        <el-form-item label="启用状态">
          <el-switch v-model="formData.is_active" />
        </el-form-item>
      </el-form>

      <template #footer>
        <el-button @click="addDialogVisible = false">取消</el-button>
        <el-button type="primary" @click="handleSubmit" :loading="submitting">
          确定
        </el-button>
      </template>
    </el-dialog>
  </div>
</template>

<script setup>
import { ref, onMounted } from 'vue'
import { ElMessage, ElMessageBox } from 'element-plus'
import { Plus, Refresh, VideoPlay, Switch, Delete } from '@element-plus/icons-vue'
import { getAccountList, createAccount, deleteAccount, toggleAccount, triggerCrawl, formatDate, getStatusConfig } from '@/api/accounts'

// 响应式数据
const loading = ref(false)
const accountList = ref([])
const activeOnly = ref(false)

const addDialogVisible = ref(false)
const formData = ref({
  name: '',
  url: '',
  is_active: true
})

const submitting = ref(false)
const formRef = ref(null)

const rules = {
  url: [
    { required: true, message: '请输入文章链接', trigger: 'blur' }
  ]
}

// 方法
const loadAccounts = async () => {
  try {
    loading.value = true
    const result = await getAccountList({
      active_only: activeOnly.value
    })
    accountList.value = result || []
  } catch (error) {
    console.error(error)
  } finally {
    loading.value = false
  }
}

const handleAdd = () => {
  formData.value = {
    name: '',
    url: '',
    is_active: true
  }
  addDialogVisible.value = true
}

const handleSubmit = async () => {
  if (!formRef.value) return

  try {
    await formRef.value.validate()

    submitting.value = true

    await createAccount(formData.value)

    ElMessage.success('公众号添加成功')
    addDialogVisible.value = false

    await loadAccounts()
  } catch (error) {
    if (error !== false) {
      ElMessage.error('添加失败')
    }
  } finally {
    submitting.value = false
  }
}

const handleCrawl = async (row) => {
  try {
    await ElMessageBox.confirm(
      `确定要立即抓取 ${row.name} 的文章吗？`,
      '确认操作',
      {
        confirmButtonText: '确定',
        cancelButtonText: '取消',
        type: 'warning'
      }
    )

    loading.value = true

    await triggerCrawl(row.id)

    ElMessage.success('抓取任务已触发')
  } catch (error) {
    if (error !== 'cancel') {
      ElMessage.error('抓取失败')
    }
  } finally {
    loading.value = false
  }
}

const handleToggle = async (row) => {
  try {
    await toggleAccount(row.id)
    await loadAccounts()
    ElMessage.success('状态已更新')
  } catch (error) {
    ElMessage.error('更新失败')
  }
}

const handleDelete = async (row) => {
  try {
    await ElMessageBox.confirm(
      `确定要删除公众号 ${row.name} 吗？同时会删除其所有文章。`,
      '删除公众号',
      {
        confirmButtonText: '确定',
        cancelButtonText: '取消',
        type: 'warning'
      }
    )

    loading.value = true

    await deleteAccount(row.id)

    ElMessage.success('公众号已删除')

    await loadAccounts()
  } catch (error) {
    if (error !== 'cancel') {
      ElMessage.error('删除失败')
    }
  } finally {
    loading.value = false
  }
}

// 生命周期
onMounted(() => {
  loadAccounts()
})
</script>

<style scoped>
.account-manage-container {
  padding: 20px;
  max-width: 1400px;
  margin: 0 auto;
}

.page-header {
  margin-bottom: 24px;
}

.page-header h1 {
  margin: 0 0 8px 0;
  font-size: 28px;
  font-weight: 600;
  color: #303133;
}

.page-header p {
  margin: 0;
  font-size: 14px;
  color: #909399;
}

.action-card {
  margin-bottom: 20px;
}

.list-card {
  margin-bottom: 20px;
}

.account-info {
  display: flex;
  align-items: center;
}

.account-name {
  font-size: 14px;
  font-weight: 500;
  color: #303133;
  margin-bottom: 4px;
}

.account-biz {
  font-size: 12px;
  color: #909399;
}

@media (max-width: 768px) {
  .account-manage-container {
    padding: 12px;
  }

  .page-header h1 {
    font-size: 24px;
  }
}
</style>
