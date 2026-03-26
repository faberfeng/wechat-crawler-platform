<template>
  <div class="dashboard">
    <el-row :gutter="20">
      <el-col :span="6">
        <el-card>
          <el-statistic title="公众号总数" :value="stats.total_accounts || 0">
            <template #prefix>
              <el-icon><Management /></el-icon>
            </template>
          </el-statistic>
        </el-card>
      </el-col>
      <el-col :span="6">
        <el-card>
          <el-statistic title="活跃公众号" :value="stats.active_accounts || 0">
            <template #prefix>
              <el-icon><CircleCheck /></el-icon>
            </template>
          </el-statistic>
        </el-card>
      </el-col>
      <el-col :span="6">
        <el-card>
          <el-statistic title="文章总数" :value="stats.total_articles || 0">
            <template #prefix>
              <el-icon><Document /></el-icon>
            </template>
          </el-statistic>
        </el-card>
      </el-col>
      <el-col :span="6">
        <el-card>
          <div class="latest-crawl">
            <div style="color: #666; margin-bottom: 8px;">最近抓取</div>
            <div v-if="stats.latest_crawl_time" style="color: #409eff; font-weight: 500;">
              {{ formatTime(stats.latest_crawl_time) }}
            </div>
            <div v-else style="color: #999;">暂无记录</div>
          </div>
        </el-card>
      </el-col>
    </el-row>

    <el-row :gutter="20" style="margin-top: 20px;">
      <el-col :span="12">
        <el-card>
          <template #header>
            <div class="card-header">
              <span>快捷操作</span>
            </div>
          </template>
          <div class="quick-actions">
            <el-button type="primary" size="large" @click="$router.push('/accounts')">
              <el-icon><Plus /></el-icon>
              添加公众号
            </el-button>
            <el-button type="success" size="large" @click="$router.push('/articles')">
              <el-icon><Search /></el-icon>
              查看文章
            </el-button>
          </div>
        </el-card>
      </el-col>
      <el-col :span="12">
        <el-card>
          <template #header>
            <div class="card-header">
              <span>使用说明</span>
            </div>
          </template>
          <div class="help-text">
            <p>1. 添加公众号：输入任意文章链接，自动识别公众号</p>
            <p>2. 定时抓取：每6小时自动更新公众号文章</p>
            <p>3. 手动触发：支持立即抓取指定公众号</p>
            <p>4. 文章管理：支持搜索、导出 Markdown</p>
          </div>
        </el-card>
      </el-col>
    </el-row>
  </div>
</template>

<script setup>
import { ref, onMounted } from 'vue'
import { getStats } from '../api/articles'
import dayjs from 'dayjs'
import relativeTime from 'dayjs/plugin/relativeTime'
import 'dayjs/locale/zh-cn'

dayjs.extend(relativeTime)
dayjs.locale('zh-cn')

const stats = ref({
  total_accounts: 0,
  active_accounts: 0,
  total_articles: 0,
  latest_crawl_time: null
})

onMounted(async () => {
  await loadStats()
})

async function loadStats() {
  try {
    const data = await getStats()
    stats.value = data
  } catch (error) {
    console.error('加载统计数据失败', error)
  }
}

function formatTime(time) {
  return dayjs(time).fromNow()
}
</script>

<style scoped>
.dashboard {
  max-width: 1400px;
  margin: 0 auto;
}

.card-header {
  display: flex;
  justify-content: space-between;
  align-items: center;
  font-weight: 600;
}

.quick-actions {
  display: flex;
  gap: 16px;
  flex-wrap: wrap;
}

.quick-actions .el-button {
  flex: 1;
  min-width: 120px;
}

.help-text p {
  margin-bottom: 12px;
  line-height: 1.6;
  color: #606266;
}

.help-text p:last-child {
  margin-bottom: 0;
}

.latest-crawl {
  padding: 10px 0;
}
</style>
