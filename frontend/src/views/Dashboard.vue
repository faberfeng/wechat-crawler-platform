<template>
  <div class="dashboard-container">
    <!-- 页面标题 -->
    <div class="page-header">
      <h1>仪表盘</h1>
      <p>平台概览和统计数据</p>
    </div>

    <!-- 统计卡片 -->
    <el-row :gutter="20" class="stats-row">
      <el-col :xs="24" :sm="12" :md="6">
        <el-card class="stat-card" v-loading="loading">
          <div class="stat-content">
            <el-icon class="stat-icon" color="#409eff"><Platform /></el-icon>
            <div class="stat-info">
              <div class="stat-value">{{ stats.total_accounts || 0 }}</div>
              <div class="stat-label">公众号总数</div>
            </div>
          </div>
        </el-card>
      </el-col>

      <el-col :xs="24" :sm="12" :md="6">
        <el-card class="stat-card" v-loading="loading">
          <div class="stat-content">
            <el-icon class="stat-icon" color="#67c23a"><Coin /></el-icon>
            <div class="stat-info">
              <div class="stat-value">{{ stats.active_accounts || 0 }}</div>
              <div class="stat-label">活跃公众号</div>
            </div>
          </div>
        </el-card>
      </el-col>

      <el-col :xs="24" :sm="12" :md="6">
        <el-card class="stat-card" v-loading="loading">
          <div class="stat-content">
            <el-icon class="stat-icon" color="#e6a23c"><Document /></el-icon>
            <div class="stat-info">
              <div class="stat-value">{{ stats.total_articles || 0 }}</div>
              <div class="stat-label">文章总数</div>
            </div>
          </div>
        </el-card>
      </el-col>

      <el-col :xs="24" :sm="12" :md="6">
        <el-card class="stat-card" v-loading="loading">
          <div class="stat-content">
            <el-icon class="stat-icon" color="#f56c6c"><Clock /></el-icon>
            <div class="stat-info">
              <div class="stat-value">{{ formatDate(stats.latest_crawl_time) }}</div>
              <div class="stat-label">最近抓取</div>
            </div>
          </div>
        </el-card>
      </el-col>
    </el-row>

    <!-- 公众号列表 -->
    <el-card class="list-card">
      <template #header>
        <div class="card-header">
          <span>公众号列表</span>
          <el-button type="primary" link :icon="Plus" @click="goToAccounts">
            添加公众号
          </el-button>
        </div>
      </template>

      <el-skeleton :loading="loading" :rows="5" animated>
        <el-table :data="accountList" stripe empty-text="暂无公众号">
          <el-table-column label="公众号" min-width="150">
            <template #default="{ row }">
              <div class="account-name">{{ row.name }}</div>
            </template>
          </el-table-column>

          <el-table-column label="状态" width="80" align="center">
            <template #default="{ row }">
              <el-tag :type="row.is_active ? 'success' : 'info'" size="small">
                {{ row.is_active ? '启用' : '禁用' }}
              </el-tag>
            </template>
          </el-table-column>

          <el-table-column label="文章数" width="80" align="center">
            <template #default="{ row }">
              <el-tag type="info" size="small">{{ row.article_count }}</el-tag>
            </template>
          </el-table-column>

          <el-table-column label="最后抓取" width="150">
            <template #default="{ row }">
              {{ formatDate(row.last_crawl_time) }}
            </template>
          </el-table-column>
        </el-table>
      </el-skeleton>
    </el-card>

    <!-- 最近文章 -->
    <el-card class="list-card">
      <template #header>
        <div class="card-header">
          <span>最近文章</span>
          <el-button type="primary" link :icon="Document" @click="goToArticles">
            查看全部
          </el-button>
        </div>
      </template>

      <el-skeleton :loading="loading" :rows="5" animated>
        <el-table :data="recentArticles" stripe empty-text="暂无文章">
          <el-table-column label="标题" min-width="200">
            <template #default="{ row }">
              <div class="article-title">{{ row.title }}</div>
            </template>
          </el-table-column>

          <el-table-column label="公众号" min-width="100">
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
        </el-table>
      </el-skeleton>
    </el-card>
  </div>
</template>

<script setup>
import { ref, onMounted } from 'vue'
import { useRouter } from 'vue-router'
import { Platform, Coin, Document, Clock, Plus } from '@element-plus/icons-vue'
import { getStats, getRecentArticles, getAccountStats } from '@/api/stats'
import { formatDate } from '@/api/accounts'
import { formatNumber } from '@/api/articles'

const router = useRouter()

// 响应式数据
const loading = ref(false)
const stats = ref({
  total_accounts: 0,
  active_accounts: 0,
  total_articles: 0,
  latest_crawl_time: null
})

const accountList = ref([])
const recentArticles = ref([])

// 方法
const loadData = async () => {
  try {
    loading.value = true

    // 加载统计数据
    const statsData = await getStats()
    stats.value = statsData || {}

    // 加载公众号列表
    const accountsData = await getAccountStats(true)
    accountList.value = accountsData?.slice(0, 8) || []

    // 加载最近文章
    const articlesData = await getRecentArticles(8)
    if (articlesData?.items) {
      recentArticles.value = articlesData.items
    }
  } catch (error) {
    console.error(error)
  } finally {
    loading.value = false
  }
}

const goToAccounts = () => {
  router.push('/accounts')
}

const goToArticles = () => {
  router.push('/articles')
}

// 生命周期
onMounted(() => {
  loadData()
})
</script>

<style scoped>
.dashboard-container {
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

.stats-row {
  margin-bottom: 20px;
}

.stat-card {
  transition: all 0.3s ease;
}

.stat-card:hover {
  transform: translateY(-4px);
  box-shadow: 0 4px 20px rgba(0, 0, 0, 0.1);
}

.stat-content {
  display: flex;
  align-items: center;
  gap: 16px;
}

.stat-icon {
  font-size: 48px;
}

.stat-info {
  flex: 1;
}

.stat-value {
  font-size: 32px;
  font-weight: 600;
  color: #303133;
  line-height: 1;
  margin-bottom: 8px;
}

.stat-label {
  font-size: 14px;
  color: #909399;
}

.list-card {
  margin-bottom: 20px;
}

.card-header {
  display: flex;
  justify-content: space-between;
  align-items: center;
}

.card-header span {
  font-size: 16px;
  font-weight: 600;
  color: #303133;
}

.account-name,
.article-title {
  font-size: 14px;
  color: #303133;
  overflow: hidden;
  text-overflow: ellipsis;
  white-space: nowrap;
}

@media (max-width: 768px) {
  .dashboard-container {
    padding: 12px;
  }

  .page-header h1 {
    font-size: 24px;
  }

  .stat-value {
    font-size: 24px;
  }

  .stat-icon {
    font-size: 36px;
  }
}
</style>
