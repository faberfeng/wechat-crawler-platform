<template>
  <el-container class="app-container">
    <el-aside width="200px">
      <div class="logo">
        <h3>微信公众号<br>抓取平台</h3>
      </div>
      <el-menu
        :default-active="$route.path"
        router
        class="sidebar"
      >
        <el-menu-item index="/dashboard">
          <el-icon><HomeFilled /></el-icon>
          <span>仪表盘</span>
        </el-menu-item>
        <el-menu-item index="/accounts">
          <el-icon><Management /></el-icon>
          <span>公众号管理</span>
        </el-menu-item>
        <el-menu-item index="/articles">
          <el-icon><Document /></el-icon>
          <span>文章列表</span>
        </el-menu-item>
      </el-menu>
    </el-aside>

    <el-container>
      <el-header>
        <h2>{{ currentPageTitle }}</h2>
      </el-header>
      <el-main>
        <router-view />
      </el-main>
    </el-container>
  </el-container>
</template>

<script setup>
import { computed } from 'vue'
import { useRoute } from 'vue-router'

const route = useRoute()

const currentPageTitle = computed(() => {
  return route.meta?.title || route.meta?.name || '微信公众号抓取平台'
})
</script>

<style scoped>
* {
  margin: 0;
  padding: 0;
  box-sizing: border-box;
}

.app-container {
  height: 100vh;
}

.el-aside {
  background: #304156;
  color: #fff;
}

.logo {
  padding: 20px;
  text-align: center;
  border-bottom: 1px solid #434a50;
}

.logo h3 {
  font-size: 16px;
  line-height: 1.5;
}

.sidebar {
  border: none;
  background: transparent;
}

.el-header {
  background: #fff;
  border-bottom: 1px solid #e6e6e6;
  display: flex;
  align-items: center;
  padding: 0 20px;
}

.el-header h2 {
  font-size: 18px;
  font-weight: 500;
}

.el-main {
  background: #f5f5f5;
  padding: 20px;
}
</style>

<style>
body {
  font-family: -apple-system, BlinkMacSystemFont, 'Segoe UI', Roboto, 'Helvetica Neue', Arial, sans-serif;
}
</style>
