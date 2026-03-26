<template>
  <div class="article-list">
    <el-card>
      <el-form :inline="true" :model="filters" class="search-form">
        <el-form-item label="公众号">
          <el-select
            v-model="filters.account_id"
            placeholder="选择公众号"
            clearable
            style="width: 200px"
          >
            <el-option
              v-for="acc in accountOptions"
              :key="acc.id"
              :label="acc.name"
              :value="acc.id"
            />
          </el-select>
        </el-form-item>
        <el-form-item label="关键词">
          <el-input
            v-model="filters.keyword"
            placeholder="搜索标题"
            style="width: 200px"
            clearable
            @keyup.enter="handleSearch"
          />
        </el-form-item>
        <el-form-item>
          <el-button type="primary" @click="handleSearch">
            <el-icon><Search /></el-icon>
            搜索
          </el-button>
          <el-button @click="handleReset">
            <el-icon><RefreshLeft /></el-icon>
            重置
          </el-button>
        </el-form-item>
      </el-form>

      <el-table :data="articles" v-loading="loading" stripe>
        <el-table-column prop="title" label="标题" min-width="300">
          <template #default="{ row }">
            <el-link type="primary" @click="viewArticle(row)">
              {{ row.title }}
            </el-link>
          </template>
        </el-table-column>
        <el-table-column prop="account_name" label="公众号" width="150" />
        <el-table-column prop="publish_time" label="发布时间" width="160">
          <template #default="{ row }">
            {{ formatDate(row.publish_time) }}
          </template>
        </el-table-column>
        <el-table-column prop="read_count" label="阅读" width="100" align="right" />
        <el-table-column prop="like_count" label="在看" width="100" align="right" />
        <el-table-column label="操作" width="120">
          <template #default="{ row }">
            <el-button size="small" @click="openUrl(row.url)" type="primary" link>
              原文
            </el-button>
            <el-button size="small" @click="viewArticle(row)" type="primary" link>
              详情
            </el-button>
          </template>
        </el-table-column>
      </el-table>

      <el-pagination
        v-model:current-page="pagination.page"
        v-model:page-size="pagination.page_size"
        :total="pagination.total"
        :page-sizes="[10, 20, 50, 100]"
        layout="total, sizes, prev, pager, next, jumper"
        @current-change="loadArticles"
        @size-change="loadArticles"
        style="margin-top: 20px; justify-content: center;"
      />

      <div class="empty" v-if="!loading && articles.length === 0">
        <el-empty description="暂无文章" />
      </div>
    </el-card>

    <!-- 文章详情抽屉 -->
    <el-drawer v-model="showDetail" title="文章详情" size="70%" @open="loadDetail">
      <div v-loading="detailLoading">
        <div v-if="currentArticle">
          <h2>{{ currentArticle.title }}</h2>
          <div class="meta">
            <span>{{ currentArticle.account_name }}</span>
            <span>{{ formatDate(currentArticle.publish_time) }}</span>
          </div>
          <MarkdownViewer v-if="currentArticle.markdown_content" :content="currentArticle.markdown_content" />
          <div v-else class="no-content">暂无内容</div>
        </div>
      </div>
    </el-drawer>
  </div>
</template>

<script setup>
import { ref, onMounted } from 'vue'
import { ElMessage } from 'element-plus'
import dayjs from 'dayjs'
import { getArticles } from '../api/articles'
import { getAccounts } from '../api/accounts'
import MarkdownViewer from '../components/MarkdownViewer.vue'

const articles = ref([])
const accountOptions = ref([])
const loading = ref(false)
const showDetail = ref(false)
const detailLoading = ref(false)
const currentArticle = ref(null)

const filters = ref({
  account_id: null,
  keyword: ''
})

const pagination = ref({
  page: 1,
  page_size: 20,
  total: 0
})

onMounted(async () => {
  await Promise.all([loadAccounts(), loadArticles()])
})

async function loadAccounts() {
  try {
    accountOptions.value = await getAccounts()
  } catch (error) {
    console.error('加载公众号列表失败', error)
  }
}

async function loadArticles() {
  loading.value = true
  try {
    const params = {
      page: pagination.value.page,
      page_size: pagination.value.page_size,
      account_id: filters.value.account_id || undefined,
      keyword: filters.value.keyword || undefined
    }
    const res = await getArticles(params)
    articles.value = res.items
    pagination.value.total = res.total
  } catch (error) {
    ElMessage.error('加载文章列表失败：' + (error.message || '未知错误'))
  } finally {
    loading.value = false
  }
}

function handleSearch() {
  pagination.value.page = 1
  loadArticles()
}

function handleReset() {
  filters.value = { account_id: null, keyword: '' }
  pagination.value.page = 1
  loadArticles()
}

async function viewArticle(row) {
  currentArticle.value = row
  showDetail.value = true
}

async function loadDetail() {
  if (!currentArticle.value) return

  detailLoading.value = true
  try {
    const { getArticle } = await import('../api/articles')
    const detail = await getArticle(currentArticle.value.id)
    currentArticle.value = { ...currentArticle.value, ...detail }
  } catch (error) {
    ElMessage.error('加载文章详情失败：' + (error.message || '未知错误'))
  } finally {
    detailLoading.value = false
  }
}

function openUrl(url) {
  window.open(url, '_blank')
}

function formatDate(time) {
  return time ? dayjs(time).format('YYYY-MM-DD HH:mm') : '-'
}
</script>

<style scoped>
.article-list {
  max-width: 1400px;
  margin: 0 auto;
}

.search-form {
  margin-bottom: 20px;
}

.empty {
  padding: 40px 0;
}

.meta {
  color: #666;
  margin: 10px 0 20px;
}

.meta span {
  margin-right: 20px;
}

.no-content {
  text-align: center;
  color: #999;
  padding: 40px;
}
</style>
