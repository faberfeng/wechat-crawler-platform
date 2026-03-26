<template>
  <div class="crawl-container">
    <!-- 页面标题 -->
    <div class="page-header">
      <h1>文章抓取</h1>
      <p>抓取任意网页的文章内容，自动保存为 Markdown 文件</p>
    </div>

    <!-- 功能选择 -->
    <el-card class="mode-card">
      <el-radio-group v-model="crawlMode" size="large">
        <el-radio-button value="single">单个 URL</el-radio-button>
        <el-radio-button value="batch">批量抓取</el-radio-button>
        <el-radio-button value="wechat">微信文章</el-radio-button>
      </el-radio-group>
    </el-card>

    <!-- 单个 URL 抓取 -->
    <el-card v-if="crawlMode === 'single'" class="crawl-card">
      <template #header>
        <span class="card-title">单个 URL 抓取</span>
      </template>

      <el-form :model="singleForm" label-width="100px">
        <el-form-item label="文章 URL">
          <el-input
            v-model="singleForm.url"
            placeholder="请输入文章 URL，例如：https://example.com/article/123"
            size="large"
            clearable
          />
        </el-form-item>

        <el-form-item>
          <el-button
            type="primary"
            :loading="loading"
            @click="handleSingleCrawl"
            size="large"
          >
            开始抓取
          </el-button>
          <el-button @click="singleForm.url = ''" size="large">
            清空
          </el-button>
        </el-form-item>
      </el-form>
    </el-card>

    <!-- 批量抓取 -->
    <el-card v-if="crawlMode === 'batch'" class="crawl-card">
      <template #header>
        <span class="card-title">批量抓取</span>
      </template>

      <el-form :model="batchForm" label-width="100px">
        <el-form-item label="URL 列表">
          <el-input
            v-model="batchForm.urlsText"
            type="textarea"
            :rows="6"
            placeholder="请输入多个 URL，每行一个&#10;例如：&#10;https://example.com/article/1&#10;https://example.com/article/2"
          />
        </el-form-item>

        <el-form-item label="URL 数量">
          <el-tag>{{ urlList.length }}</el-tag>
        </el-form-item>

        <el-form-item>
          <el-button
            type="primary"
            :loading="loading"
            @click="handleBatchCrawl"
            size="large"
          >
            批量抓取
          </el-button>
          <el-button @click="handleClearUrls" size="large">
            清空
          </el-button>
        </el-form-item>
      </el-form>
    </el-card>

    <!-- 微信文章抓取 -->
    <el-card v-if="crawlMode === 'wechat'" class="crawl-card">
      <template #header>
        <span class="card-title">微信文章抓取</span>
      </template>

      <el-form :model="wechatForm" label-width="120px">
        <el-form-item label="文章 URL">
          <el-input
            v-model="wechatForm.url"
            placeholder="请输入微信文章 URL"
            size="large"
            clearable
          />
        </el-form-item>

        <el-form-item label="关联公众号">
          <el-select
            v-model="wechatForm.accountId"
            placeholder="选择公众号（可选）"
            clearable
            style="width: 100%"
          >
            <el-option
              v-for="account in accounts"
              :key="account.id"
              :value="account.id"
              :label="account.name"
            />
          </el-select>
        </el-form-item>

        <el-form-item>
          <el-button
            type="primary"
            :loading="loading"
            @click="handleWeChatCrawl"
            size="large"
          >
            抓取微信文章
          </el-button>
          <el-button @click="wechatForm.url = ''" size="large">
            清空
          </el-button>
        </el-form-item>
      </el-form>
    </el-card>

    <!-- 抓取结果 -->
    <el-card v-if="crawlResult" class="result-card">
      <template #header>
        <div class="result-header">
          <span class="card-title">抓取结果</span>
          <el-tag :type="crawlResult.success ? 'success' : 'danger'">
            {{ crawlResult.success ? '成功' : '失败' }}
          </el-tag>
        </div>
      </template>

      <el-alert
        :title="crawlResult.message"
        :type="crawlResult.success ? 'success' : 'error'"
        :closable="false"
        style="margin-bottom: 20px"
      />

      <!-- 文章信息 -->
      <div v-if="crawlResult.success && crawlResult.article" class="article-info">
        <h3>{{ crawlResult.article.title }}</h3>
        <p class="meta">
          <span v-if="crawlResult.article.author">作者：{{ crawlResult.article.author }}</span>
          <span v-if="crawlResult.article.publish_time">
            发布时间：{{ formatDate(crawlResult.article.publish_time) }}
          </span>
        </p>
        <p v-if="crawlResult.article.cover_img" class="cover">
          <img :src="crawlResult.article.cover_img" alt="封面图" />
        </p>

        <!-- 操作按钮 -->
        <div class="actions">
          <el-button type="primary" @click="handleViewMarkdown">
            查看 Markdown
          </el-button>
          <el-button @click="handleGotoArticleList">
            查看文章列表
          </el-button>
        </div>
      </div>

      <!-- 批量结果统计 -->
      <div v-if="crawlResult.summary" class="batch-summary">
        <el-row :gutter="20">
          <el-col :span="8">
            <div class="stat-item">
              <div class="stat-value">{{ crawlResult.summary.total }}</div>
              <div class="stat-label">总数</div>
            </div>
          </el-col>
          <el-col :span="8">
            <div class="stat-item success">
              <div class="stat-value">{{ crawlResult.summary.success }}</div>
              <div class="stat-label">成功</div>
            </div>
          </el-col>
          <el-col :span="8">
            <div class="stat-item error">
              <div class="stat-value">{{ crawlResult.summary.failed }}</div>
              <div class="stat-label">失败</div>
            </div>
          </el-col>
        </el-row>
      </div>
    </el-card>

    <!-- Markdown 预览对话框 -->
    <el-dialog
      v-model="markdownVisible"
      title="Markdown 内容"
      width="80%"
    >
      <div class="markdown-preview">
        <pre>{{ markdownContent }}</pre>
      </div>
      <template #footer>
        <el-button @click="markdownVisible = false">关闭</el-button>
      </template>
    </el-dialog>
  </div>
</template>

<script setup>
import { ref, computed, onMounted } from 'vue'
import { ElMessage } from 'element-plus'
import { useRouter } from 'vue-router'
import {
  crawlSingleUrl,
  crawlUrlsBatch,
  crawlWeChatArticle,
  getArticleMarkdown
} from '@/api/crawler'
import { getAccountList } from '@/api/accounts'

const router = useRouter()

// 状态
const crawlMode = ref('single')
const loading = ref(false)
const crawlResult = ref(null)
const accounts = ref([])
const markdownVisible = ref(false)
const markdownContent = ref('')

// 表单数据
const singleForm = ref({
  url: ''
})

const batchForm = ref({
  urlsText: ''
})

const wechatForm = ref({
  url: '',
  accountId: null
})

// 计算属性
const urlList = computed(() => {
  const text = batchForm.value.urlsText.trim()
  if (!text) return []
  return text.split('\n').filter(url => url.trim())
})

// 方法
const loadAccounts = async () => {
  try {
    const result = await getAccountList()
    if (Array.isArray(result)) {
      accounts.value = result
    }
  } catch (error) {
    console.error('加载公众号列表失败:', error)
  }
}

const handleSingleCrawl = async () => {
  if (!singleForm.value.url.trim()) {
    ElMessage.warning('请输入文章 URL')
    return
  }

  loading.value = true
  crawlResult.value = null

  try {
    const result = await crawlSingleUrl(singleForm.value.url)
    crawlResult.value = result

    if (result.success) {
      ElMessage.success(result.message)
    }
  } catch (error) {
    ElMessage.error('抓取失败：' + error.message)
    crawlResult.value = {
      success: false,
      message: error.message
    }
  } finally {
    loading.value = false
  }
}

const handleBatchCrawl = async () => {
  if (urlList.value.length === 0) {
    ElMessage.warning('请输入至少一个 URL')
    return
  }

  loading.value = true
  crawlResult.value = null

  try {
    const result = await crawlUrlsBatch(urlList.value)
    crawlResult.value = result

    if (result.success) {
      ElMessage.success(`批量抓取完成：成功 ${result.summary.success}，失败 ${result.summary.failed}`)
    }
  } catch (error) {
    ElMessage.error('批量抓取失败：' + error.message)
    crawlResult.value = {
      success: false,
      message: error.message
    }
  } finally {
    loading.value = false
  }
}

const handleWeChatCrawl = async () => {
  if (!wechatForm.value.url.trim()) {
    ElMessage.warning('请输入微信文章 URL')
    return
  }

  if (!wechatForm.value.url.includes('mp.weixin.qq.com')) {
    ElMessage.warning('请输入微信公众号文章 URL')
    return
  }

  loading.value = true
  crawlResult.value = null

  try {
    const result = await crawlWeChatArticle(
      wechatForm.value.url,
      wechatForm.value.accountId
    )
    crawlResult.value = result

    if (result.success) {
      ElMessage.success(result.message)
    }
  } catch (error) {
    ElMessage.error('抓取失败：' + error.message)
    crawlResult.value = {
      success: false,
      message: error.message
    }
  } finally {
    loading.value = false
  }
}

const handleClearUrls = () => {
  batchForm.value.urlsText = ''
}

const formatDate = (dateStr) => {
  if (!dateStr) return '-'
  const date = new Date(dateStr)
  return date.toLocaleString('zh-CN')
}

const handleViewMarkdown = async () => {
  if (!crawlResult.value || !crawlResult.value.article) return

  try {
    const result = await getArticleMarkdown(crawlResult.value.article.id)
    if (result.success) {
      markdownContent.value = result.content
      markdownVisible.value = true
    }
  } catch (error) {
    ElMessage.error('加载 Markdown 失败')
  }
}

const handleGotoArticleList = () => {
  router.push('/articles')
}

// 生命周期
onMounted(() => {
  loadAccounts()
})
</script>

<style scoped>
.crawl-container {
  padding: 20px;
  max-width: 1200px;
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

.mode-card,
.crawl-card,
.result-card {
  margin-bottom: 20px;
}

.card-title {
  font-size: 16px;
  font-weight: 600;
  color: #303133;
}

.result-header {
  display: flex;
  justify-content: space-between;
  align-items: center;
}

.article-info h3 {
  font-size: 20px;
  margin: 0 0 12px 0;
}

.article-info .meta {
  color: #909399;
  font-size: 14px;
  margin-bottom: 12px;
}

.article-info .meta span {
  margin-right: 20px;
}

.article-info .cover img {
  max-width: 100%;
  max-height: 300px;
  border-radius: 4px;
  margin-bottom: 16px;
}

.article-info .actions {
  margin-top: 20px;
}

.batch-summary {
  padding: 20px 0;
}

.stat-item {
  text-align: center;
  padding: 20px;
  background: #f5f7fa;
  border-radius: 4px;
}

.stat-item.success {
  background: #f0f9ff;
}

.stat-item.error {
  background: #fef0f0;
}

.stat-value {
  font-size: 32px;
  font-weight: 600;
  color: #303133;
  margin-bottom: 8px;
}

.stat-label {
  font-size: 14px;
  color: #909399;
}

.markdown-preview {
  max-height: 60vh;
  overflow-y: auto;
}

.markdown-preview pre {
  margin: 0;
  font-family: "Monaco", "Consolas", monospace;
  font-size: 13px;
  line-height: 1.6;
  white-space: pre-wrap;
  word-wrap: break-word;
}
</style>
