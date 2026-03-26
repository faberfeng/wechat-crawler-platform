<template>
  <el-container class="app-container" v-if="authStore.isAuthenticated">
    <!-- 侧边栏 -->
    <el-aside
      :width="sidebarCollapsed ? '64px' : '200px'"
      class="sidebar"
    >
      <div class="logo" @click="toggleSidebar">
        <h3 v-show="!sidebarCollapsed">微信公众号<br>抓取平台</h3>
        <el-icon v-show="sidebarCollapsed" :size="24"><Platform /></el-icon>
      </div>

      <el-menu
        :default-active="$route.path"
        router
        :collapse="sidebarCollapsed"
        :collapse-transition="false"
        class="sidebar-menu"
      >
        <el-tooltip
          v-if="sidebarCollapsed"
          content="仪表盘"
          placement="right"
          :show-after="500"
        >
          <el-menu-item index="/dashboard">
            <el-icon><HomeFilled /></el-icon>
            <template #title>仪表盘</template>
          </el-menu-item>
        </el-tooltip>

        <el-menu-item v-else index="/dashboard">
          <el-icon><HomeFilled /></el-icon>
          <span>仪表盘</span>
        </el-menu-item>

        <el-tooltip
          v-if="sidebarCollapsed"
          content="公众号管理"
          placement="right"
          :show-after="500"
        >
          <el-menu-item index="/accounts">
            <el-icon><Management /></el-icon>
            <template #title>公众号管理</template>
          </el-menu-item>
        </el-tooltip>

        <el-menu-item v-else index="/accounts">
          <el-icon><Management /></el-icon>
          <span>公众号管理</span>
        </el-menu-item>

        <el-tooltip
          v-if="sidebarCollapsed"
          content="文章列表"
          placement="right"
          :show-after="500"
        >
          <el-menu-item index="/articles">
            <el-icon><Document /></el-icon>
            <template #title>文章列表</template>
          </el-menu-item>
        </el-tooltip>

        <el-menu-item v-else index="/articles">
          <el-icon><Document /></el-icon>
          <span>文章列表</span>
        </el-menu-item>

        <el-tooltip
          v-if="sidebarCollapsed"
          content="文章抓取"
          placement="right"
          :show-after="500"
        >
          <el-menu-item index="/crawl">
            <el-icon><Download /></el-icon>
            <template #title>文章抓取</template>
          </el-menu-item>
        </el-tooltip>

        <el-menu-item v-else index="/crawl">
          <el-icon><Download /></el-icon>
          <span>文章抓取</span>
        </el-menu-item>

        <el-tooltip
          v-if="sidebarCollapsed"
          content="用户管理"
          placement="right"
          :show-after="500"
        >
          <el-menu-item v-if="authStore.isAdmin()" index="/users">
            <el-icon><User /></el-icon>
            <template #title>用户管理</template>
          </el-menu-item>
        </el-tooltip>

        <el-menu-item v-else-if="authStore.isAdmin()" index="/users">
          <el-icon><User /></el-icon>
          <span>用户管理</span>
        </el-menu-item>

        <el-tooltip
          v-if="sidebarCollapsed"
          content="文件管理"
          placement="right"
          :show-after="500"
        >
          <el-menu-item index="/files">
            <el-icon><Folder /></el-icon>
            <template #title>文件管理</template>
          </el-menu-item>
        </el-tooltip>

        <el-menu-item v-else index="/files">
          <el-icon><Folder /></el-icon>
          <span>文件管理</span>
        </el-menu-item>

        <el-tooltip
          v-if="sidebarCollapsed"
          content="个人信息"
          placement="right"
          :show-after="500"
        >
          <el-menu-item index="/profile">
            <el-icon><UserFilled /></el-icon>
            <template #title>个人信息</template>
          </el-menu-item>
        </el-tooltip>

        <el-menu-item v-else index="/profile">
          <el-icon><UserFilled /></el-icon>
          <span>个人信息</span>
        </el-menu-item>
      </el-menu>
    </el-aside>

    <!-- 主内容区 -->
    <el-container>
      <!-- 头部 -->
      <el-header class="app-header">
        <div class="header-left">
          <el-button
            :icon="Fold"
            circle
            @click="toggleSidebar"
            class="sidebar-toggle"
          />
          <h2>{{ currentPageTitle }}</h2>
        </div>

        <div class="header-right">
          <!-- 用户信息 -->
          <el-dropdown @command="handleUserCommand" trigger="click">
            <div class="user-info">
              <el-avatar :size="32" :icon="UserFilled" />
              <span class="username no-select">{{ authStore.user?.username }}</span>
              <el-tag
                v-if="authStore.user?.role === 'admin'"
                type="danger"
                size="small"
                class="admin-tag"
              >
                管理员
              </el-tag>
              <el-icon class="dropdown-icon"><ArrowDown /></el-icon>
            </div>
            <template #dropdown>
              <el-dropdown-menu>
                <el-dropdown-item command="profile">
                  <el-icon><UserFilled /></el-icon>
                  个人信息
                </el-dropdown-item>
                <el-dropdown-item divided command="logout">
                  <el-icon><SwitchButton /></el-icon>
                  退出登录
                </el-dropdown-item>
              </el-dropdown-menu>
            </template>
          </el-dropdown>
        </div>
      </el-header>

      <!-- 主内容 -->
      <el-main>
        <router-view v-slot="{ Component, route }">
          <transition name="page" mode="out-in">
            <component :is="Component" :key="route.path" />
          </transition>
        </router-view>
      </el-main>
    </el-container>
  </el-container>

  <!-- 未登录时直接显示页面（登录/注册） -->
  <router-view v-else />
</template>

<script setup>
import { computed, onMounted, ref } from 'vue'
import { useRoute, useRouter } from 'vue-router'
import { ElMessage, ElMessageBox } from 'element-plus'
import { useAuthStore } from '@/stores/auth'

const route = useRoute()
const router = useRouter()
const authStore = useAuthStore()

// 侧边栏折叠状态
const sidebarCollapsed = ref(false)

// 当前页面标题
const currentPageTitle = computed(() => {
  return route.meta?.title || route.meta?.name || '微信公众号抓取平台'
})

// 切换侧边栏
const toggleSidebar = () => {
  sidebarCollapsed.value = !sidebarCollapsed.value
}

// 处理用户下拉菜单命令
const handleUserCommand = async (command) => {
  if (command === 'profile') {
    router.push('/profile')
  } else if (command === 'logout') {
    await handleLogout()
  }
}

// 处理登出
const handleLogout = async () => {
  try {
    await ElMessageBox.confirm(
      '确定要退出登录吗？',
      '退出登录',
      {
        confirmButtonText: '确定',
        cancelButtonText: '取消',
        type: 'warning',
        confirmButtonClass: 'el-button--danger'
      }
    )

    await authStore.handleLogout()
    ElMessage.success({
      message: '退出成功',
      duration: 2000,
      showClose: true
    })
    router.push('/login')
  } catch (error) {
    // 用户取消登出
  }
}

// 初始化认证状态
onMounted(() => {
  authStore.initializeAuth()
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
  overflow: hidden;
}

/* 侧边栏 */
.sidebar {
  background: linear-gradient(180deg, #304156 0%, #263445 100%);
  color: #fff;
  transition: all 0.3s ease;
  box-shadow: 2px 0 8px rgba(0, 0, 0, 0.1);
}

.logo {
  padding: 20px;
  text-align: center;
  border-bottom: 1px solid rgba(255, 255, 255, 0.1);
  cursor: pointer;
  transition: all 0.3s ease;
  height: 60px;
  display: flex;
  align-items: center;
  justify-content: center;
}

.logo:hover {
  background: rgba(255, 255, 255, 0.05);
}

.logo h3 {
  font-size: 16px;
  line-height: 1.5;
  font-weight: 600;
  color: #fff;
}

/* 侧边栏菜单 */
.sidebar-menu {
  border: none;
  background: transparent;
  height: calc(100vh - 60px);
  overflow-y: auto;
}

.sidebar-menu:not(.el-menu--collapse) {
  width: 200px;
}

.el-menu-item {
  margin: 4px 12px;
  border-radius: 8px;
  color: #bfcbd9;
}

.el-menu-item:hover {
  background: rgba(255, 255, 255, 0.1);
  color: #fff;
}

.el-menu-item.is-active {
  background: var(--el-color-primary);
  color: #fff;
}

.el-menu-item.is-active:hover {
  background: var(--el-color-primary-light-3);
}

/* 头部 */
.app-header {
  background: #fff;
  border-bottom: 1px solid #e6e6e6;
  display: flex;
  align-items: center;
  justify-content: space-between;
  padding: 0 20px;
  box-shadow: 0 2px 4px rgba(0, 0, 0, 0.05);
  z-index: 10;
}

.header-left {
  display: flex;
  align-items: center;
  gap: 16px;
}

.sidebar-toggle {
  border: none;
  background: #f5f7fa;
  color: #606266;
  transition: all 0.3s ease;
}

.sidebar-toggle:hover {
  background: var(--el-color-primary-light-9);
  color: var(--el-color-primary);
}

.header-left h2 {
  font-size: 18px;
  font-weight: 500;
  color: #303133;
}

.header-right {
  display: flex;
  align-items: center;
}

/* 用户信息 */
.user-info {
  display: flex;
  align-items: center;
  gap: 12px;
  padding: 8px 16px;
  border-radius: 8px;
  cursor: pointer;
  transition: all 0.3s ease;
}

.user-info:hover {
  background: #f5f7fa;
}

.username {
  font-size: 14px;
  color: #303133;
  font-weight: 500;
}

.admin-tag {
  font-weight: 500;
}

.dropdown-icon {
  color: #909399;
  transition: transform 0.3s ease;
}

.user-info:hover .dropdown-icon {
  transform: rotate(180deg);
}

/* 主内容区 */
.el-main {
  background: #f5f7fa;
  padding: 24px;
  overflow-y: auto;
  min-height: calc(100vh - 60px);
}

/* 响应式设计 */
@media (max-width: 768px) {
  .sidebar {
    position: absolute;
    left: 0;
    top: 0;
    z-index: 999;
    height: 100vh;
  }

  .sidebar.is-mobile-hidden {
    transform: translateX(-100%);
  }

  .app-header {
    padding: 0 12px;
  }

  .header-left h2 {
    font-size: 16px;
  }

  .username {
    display: none;
  }

  .admin-tag {
    display: none;
  }

  .el-main {
    padding: 16px;
  }
}

@media (max-width: 576px) {
  .el-main {
    padding: 12px;
  }
}
</style>

<style>
/* Element Plus 样式覆盖 */
.el-message {
  box-shadow: 0 4px 12px rgba(0, 0, 0, 0.15) !important;
  border-radius: 8px !important;
}

.el-message-box {
  border-radius: 12px !important;
}

.el-dialog {
  border-radius: 12px !important;
}

.el-card {
  border-radius: 12px !important;
  border: none !important;
}

.el-button {
  border-radius: 8px !important;
  font-weight: 500 !important;
}

.el-input__wrapper {
  border-radius: 8px !important;
}

.el-select .el-input__wrapper {
  border-radius: 8px !important;
}

.el-form-item__label {
  font-weight: 500 !important;
}

.el-tag {
  border-radius: 6px !important;
}

body {
  font-family: -apple-system, BlinkMacSystemFont, 'Segoe UI', Roboto, 'Helvetica Neue', Arial,
    'Noto Sans', sans-serif, 'Apple Color Emoji', 'Segoe UI Emoji', 'Segoe UI Symbol',
    'Noto Color Emoji';
  -webkit-font-smoothing: antialiased;
  -moz-osx-font-smoothing: grayscale;
}
</style>
