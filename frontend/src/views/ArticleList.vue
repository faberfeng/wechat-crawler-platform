<template>
  <div class="article-list-container">
    <!-- 页面标题 -->
    <div class="page-header">
      <h1>文章列表</h1>
      <p>搜索和管理抓取的文章</p>
    </div>

    <!-- 搜索和筛选 -->
    <el-card class="filter-card">
      <el-row :gutter="20">
        <el-col :xs="24" :sm="12" :md="8">
          <el-input
            v-model="filters.keyword"
            placeholder="搜索标题"
            clearable
            :prefix-icon="Search"
            @change="handleFilterChange"
          />
        </el-col>

        <el-col :xs="24" :sm="12" :md="8">
          <el-select
            v-model="filters.account_id"
            placeholder="选择公众号"
            clearable
            @change="handleFilterChange"
            style="width: 100%"
          >
            <el-option
              v-for="account in accountList"
              :key="account.id"
              :label="account.name"
              :value="account.id"
            />
          </el-select>
        </el-col>

        <el-col :xs="24" :sm="24" :md="8" style="text-align: right">
          <el-button :icon="Refresh" @click="loadArticles" :loading="loading">
            刷新
          </el-button>
        </el-col>
      </el-row>
    </el-card>

    <!-- 文章列表 -->
    <el-card class="list-card">
      <template #header>
        <span class="card-title">
          共 {{ total }} 篇文章
        </span>
      </template>

      <el-skeleton :loading="loading" :rows="5" animated>
        <el-table
          :data="articleList"
          stripe
          v-loading="loading"
          empty-text="暂无文章"
        >
          <el-table-column label="标题" min-width="200">
            <template #default="{ row }">
              <div class="article-title" @click="handleViewArticle(row)">
                {{ row.title }}
              </div>
            </template>
          </el-table-column>

          <el-table-column label="公众号" width="120">
            <template #default="{ row }">
              <el-tag size="small">{{ row.account_name }}</el-tag>
            </template>
          </el-table-column>

          <el-table-column label="阅读" width="80" align="center">
            <template #default="{ row }">
              {{ formatNumber(row.read_count) }}
            </template>
          </el-table-column>

          <el-table-column label="点赞" width="80" align="center">
            <template #default="{ row }">
              {{ formatNumber(row.like_count) }}
            </template>
          </el-table-column>

          <el-table-column label="发布时间" width="150">
            <template #default="{ row }">
              {{ formatDate(row.publish_time) }}
            </template>
          </el-table-column>

          <el-table-column label="操作" width="150" fixed="right">
            <template #default="{ row }">
              <el-button
                type="primary"
                link
                :icon="View"
                @click="handleViewArticle(row)"
              >
                查看
              </el-button>
              <el-button
                type="primary"
                link
                :icon="Share"
                @click="handleOpenLink(row)"
              >
                打开
              </el-button>
            </template>
          </el-table-column>
        </el-table>

        <!-- 分页 -->
        <div class="pagination-container">
          <el-pagination
            v-model:current-page="currentPage"
            v-model:page-size="pageSize"
            :page-sizes="[10, 20, 50, 100]"
            :total="total"
            layout="total, sizes, prev, pager, next, jumper"
            @size-change="loadArticles"
            @current-change="loadArticles"
          />
        </div>
      </el-skeleton>
    </el-card>

    <!-- 文章详情对话框 -->
    <el-dialog
      v-model="detailDialogVisible"
      :title="currentArticle?.title"
      width="80%"
    >
      <div v-loading="loadingDetail">
        <div class="article-meta">
          <el-tag>{{ currentArticle?.account_name }}</el-tag>
          <el-space>
            阅读: {{ formatNumber(currentArticle?.read_count) }}
            点赞: {{ formatNumber(currentArticle?.like_count) }}
          </el-space>
        </div>

        <div class="article-content">
          <pre>{{ markdownContent }}</pre>
        </div>
      </div>

      <template #footer>
        <el-button @click="detailDialogVisible = false">关闭</el-button>
        <el-button
          v-if="currentArticle"
          type="primary"
          @click="handleOpenLink(currentArticle)"
        >
          打开原文
        </el-button>
      </template>
    </el-dialog>
  </div>
</template>

<script setup>
import { ref, onMounted } from 'vue'
import { ElMessage } from 'element-plus'
import { Search, Refresh, View, Share } from '@element-plus/icons-vue'
import { getArticleList, getArticle, deleteArticle, formatDate, formatNumber, openArticleUrl } from '@/api/articles'
import { getAccountList } from '@/api/accounts'

// 响应式数据
const loading = ref(false)
const articleList = ref([])
const accountList = ref([])
const total = ref(0)

const currentPage = ref(1)
const pageSize = ref(20)

const filters = ref({
  keyword: '',
  account_id: null
})

const detailDialogVisible = ref(false)
const currentArticle = ref(null)
const markdownContent = ref('')
const loadingDetail = ref(false)

// 方法
const loadArticles = async () => {
  try {
    loading.value = true

    const params = {
      page: currentPage.value,
      page_size: pageSize.value
    }

    if (filters.value.keyword) {
      params.keyword = filters.value.keyword
    }

    if (filters.value.account_id) {
      params.account_id = filters.value.account_id
    }

    const result = await getArticleList(params)

    if (result?.items) {
      articleList.value = result.items
      total.value = result.total || 0
    }
  } catch (error) {
    console.error(error)
  } finally {
    loading.value = false
  }
}

const loadAccounts = async () => {
  try {
    const result = await getAccountList({ active_only: true })
    accountList.value = result || []
  } catch (error) {
    console.error(error)
  }
}

const handleFilterChange = () => {
  currentPage.value = 1
  loadArticles()
}

const handleViewArticle = async (row) => {
  try {
    currentArticle.value = row
    detailDialogVisible.value = true

    loadingDetail.value = true

    const result = await getArticle(row.id)

    if (result?.markdown_content) {
      markdownContent.value = result.markdown_content
    }
  } catch (error) {
    ElMessage.error('加载文章失败')
    detailDialogVisible.value = false
  } finally {
    loadingDetail.value = false
  }
}

const handleOpenLink = (row) => {
  openArticleUrl(row.url)
}

// 生命周期
onMounted(async () => {
  await loadAccounts()
  await loadArticles()
})
</script>

<style scoped>
.article-list-container {
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

.filter-card {
  margin-bottom: 20px;
}

.list-card {
  margin-bottom: 20px;
}

.card-title {
  font-size: 16px;
  font-weight: 600;
  color: #303133;
}

.article-title {
  font-size: 14px;
  color: #303133;
  cursor: pointer;
  transition: color 0.3s ease;
}

.article-title:hover {
  color: #409eff;
}

.pagination-container {
  margin-top: 20px;
  display: flex;
  justify-content: center;
}

.article-meta {
  margin-bottom: 20px;
  padding: 12px;
  background: #f5f7fa;
  border-radius: 4px;
  display: flex;
  justify-content: space-between;
  align-items: center;
}

.article-content {
  min-height: 400px;
  max-height: 600px;
  overflow: auto;
  padding: 20px;
  background: #fafafa;
  border-radius: 4px;
}

.article-content pre {
  font-size: 14px;
  line-height: 1.6;
  white-space: pre-wrap;
  word-wrap: break-word;
}

@media (max-width: 768px) {
  .article-list-container {
    padding: 12px;
  }

  .page-header h1 {
    font-size: 24px;
  }
}
</style>
