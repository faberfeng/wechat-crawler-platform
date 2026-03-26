import { createApp } from 'vue'
import { createRouter, createWebHistory } from 'vue-router'
import { createPinia } from 'pinia'
import ElementPlus from 'element-plus'
import 'element-plus/dist/index.css'
import * as ElementPlusIconsVue from '@element-plus/icons-vue'
import zhCn from 'element-plus/es/locale/lang/zh-cn'
import { ElMessage } from 'element-plus'

import App from './App.vue'
import Dashboard from './views/Dashboard.vue'
import AccountManage from './views/AccountManage.vue'
import ArticleList from './views/ArticleList.vue'
import CrawlArticle from './views/CrawlArticle.vue'
import Login from './views/Login.vue'
import Register from './views/Register.vue'
import UserManage from './views/UserManage.vue'
import Profile from './views/Profile.vue'
import FileManage from './views/FileManage.vue'
import { useAuthStore } from './stores/auth'
import './styles/animations.css'

const routes = [
  { path: '/', redirect: '/dashboard' },
  { path: '/dashboard', component: Dashboard, name: '仪表盘', meta: { requiresAuth: true } },
  { path: '/accounts', component: AccountManage, name: '公众号管理', meta: { requiresAuth: true } },
  { path: '/articles', component: ArticleList, name: '文章列表', meta: { requiresAuth: true } },
  { path: '/crawl', component: CrawlArticle, name: '文章抓取', meta: { requiresAuth: true } },
  { path: '/users', component: UserManage, name: '用户管理', meta: { requiresAuth: true, requiresAdmin: true } },
  { path: '/files', component: FileManage, name: '文件管理', meta: { requiresAuth: true } },
  { path: '/profile', component: Profile, name: '个人信息', meta: { requiresAuth: true } },
  { path: '/login', component: Login, name: '登录', meta: { public: true } },
  { path: '/register', component: Register, name: '注册', meta: { public: true } }
]

const router = createRouter({
  history: createWebHistory(),
  routes
})

// 路由守卫
router.beforeEach(async (to, from, next) => {
  const authStore = useAuthStore()

  // 如果访问的是公开路由（登录/注册），直接放行
  if (to.meta.public) {
    // 如果已经登录，访问登录/注册页面则跳转到首页
    if (authStore.isAuthenticated && (to.path === '/login' || to.path === '/register')) {
      return next('/')
    }
    return next()
  }

  // 如果需要认证但未登录，跳转到登录页
  if (to.meta.requiresAuth && !authStore.isAuthenticated) {
    next('/login')
    return
  }

  // 如果需要管理员权限但用户不是管理员
  if (to.meta.requiresAdmin && !authStore.isAdmin()) {
    ElMessage.error('权限不足，只有管理员可以访问')
    next('/')
    return
  }

  next()
})

const pinia = createPinia()

const app = createApp(App)

// 注册所有图标
for (const [key, component] of Object.entries(ElementPlusIconsVue)) {
  app.component(key, component)
}

app.use(pinia)
app.use(router)
app.use(ElementPlus, { locale: zhCn })

// 初始化认证状态（在 pinia 安装后）
const authStore = useAuthStore()
authStore.initializeAuth()

app.mount('#app')
