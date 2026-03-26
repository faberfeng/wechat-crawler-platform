<template>
  <div class="account-manage">
    <el-card>
      <template #header>
        <div class="card-header">
          <span>公众号管理</span>
          <el-button type="primary" @click="showAddDialog = true">
            <el-icon><Plus /></el-icon>
            添加公众号
          </el-button>
        </div>
      </template>

      <el-table :data="accounts" v-loading="loading" stripe>
        <el-table-column prop="name" label="公众号名称" min-width="200" />
        <el-table-column prop="biz" label="Biz ID" width="200" show-overflow-tooltip />
        <el-table-column prop="last_crawl_time" label="上次抓取" width="160">
          <template #default="{ row }">
            {{ formatDate(row.last_crawl_time) }}
          </template>
        </el-table-column>
        <el-table-column prop="article_count" label="文章数" width="100" align="right" />
        <el-table-column label="状态" width="100">
          <template #default="{ row }">
            <el-tag :type="row.is_active ? 'success' : 'info'">
              {{ row.is_active ? '启用' : '禁用' }}
            </el-tag>
          </template>
        </el-table-column>
        <el-table-column label="操作" width="260">
          <template #default="{ row }">
            <el-button-group>
              <el-button size="small" @click="handleCrawl(row.id)">
                <el-icon><Refresh /></el-icon>
                抓取
              </el-button>
              <el-button size="small" @click="handleToggle(row)">
                <el-icon><Switch /></el-icon>
              </el-button>
              <el-button size="small" type="danger" @click="handleDelete(row.id)">
                <el-icon><Delete /></el-icon>
              </el-button>
            </el-button-group>
          </template>
        </el-table-column>
      </el-table>

      <div class="empty" v-if="!loading && accounts.length === 0">
        <el-empty description="暂无公众号，点击右上角添加" />
      </div>
    </el-card>

    <!-- 添加公众号对话框 -->
    <el-dialog v-model="showAddDialog" title="添加公众号" width="500px">
      <el-form :model="newAccount" label-width="100px">
        <el-form-item label="公众号名称">
          <el-input v-model="newAccount.name" placeholder="公众号名称（可选）" />
        </el-form-item>
        <el-form-item label="文章链接" required>
          <el-input
            v-model="newAccount.url"
            placeholder="输入该公众号任意一篇文章链接"
            type="textarea"
            :rows="3"
          />
          <div class="tips">
            <el-alert
              title="系统将自动从链接中识别公众号信息"
              type="info"
              :closable="false"
            />
          </div>
        </el-form-item>
      </el-form>
      <template #footer>
        <el-button @click="showAddDialog = false">取消</el-button>
        <el-button type="primary" @click="handleAdd" :loading="adding">
          添加并开始抓取
        </el-button>
      </template>
    </el-dialog>
  </div>
</template>

<script setup>
import { ref, onMounted } from 'vue'
import { ElMessage, ElMessageBox } from 'element-plus'
import dayjs from 'dayjs'
import { getAccounts, addAccount, deleteAccount, triggerCrawl, toggleAccount } from '../api/accounts'

const accounts = ref([])
const loading = ref(false)
const showAddDialog = ref(false)
const adding = ref(false)
const newAccount = ref({ name: '', url: '' })

onMounted(async () => {
  await loadAccounts()
})

async function loadAccounts() {
  loading.value = true
  try {
    accounts.value = await getAccounts()
  } catch (error) {
    console.error('加载公众号列表失败', error)
  } finally {
    loading.value = false
  }
}

async function handleAdd() {
  if (!newAccount.value.url) {
    ElMessage.warning('请输入文章链接')
    return
  }

  adding.value = true
  try {
    await addAccount(newAccount.value)
    ElMessage.success('添加成功')
    showAddDialog.value = false
    newAccount.value = { name: '', url: '' }
    await loadAccounts()
  } catch (error) {
    ElMessage.error('添加失败：' + (error.message || '未知错误'))
  } finally {
    adding.value = false
  }
}

async function handleCrawl(id) {
  try {
    await triggerCrawl(id)
    ElMessage.success('抓取任务已触发')
  } catch (error) {
    ElMessage.error('触发失败：' + (error.message || '未知错误'))
  }
}

async function handleToggle(row) {
  try {
    await toggleAccount(row.id)
    ElMessage.success(row.is_active ? '已禁用' : '已启用')
    await loadAccounts()
  } catch (error) {
    ElMessage.error('操作失败：' + (error.message || '未知错误'))
  }
}

async function handleDelete(id) {
  await ElMessageBox.confirm(
    '删除公众号会同时删除所有关联文章，确定要删除吗？',
    '确认删除',
    {
      type: 'warning'
    }
  )

  try {
    await deleteAccount(id)
    ElMessage.success('删除成功')
    await loadAccounts()
  } catch (error) {
    if (error !== 'cancel') {
      ElMessage.error('删除失败：' + (error.message || '未知错误'))
    }
  }
}

function formatDate(time) {
  return time ? dayjs(time).format('YYYY-MM-DD HH:mm') : '-'
}
</script>

<style scoped>
.account-manage {
  max-width: 1400px;
  margin: 0 auto;
}

.card-header {
  display: flex;
  justify-content: space-between;
  align-items: center;
}

.tips {
  margin-top: 8px;
}

.empty {
  padding: 40px 0;
}
</style>
