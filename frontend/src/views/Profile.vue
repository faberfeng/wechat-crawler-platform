<template>
  <div class="profile-container">
    <div class="profile-header">
      <h1>个人信息</h1>
      <p>管理您的账号信息</p>
    </div>

    <el-row :gutter="20">
      <!-- 左侧：用户信息卡片 -->
      <el-col :xs="24" :sm="24" :md="8" :lg="8" :xl="8">
        <el-card class="info-card">
          <template #header>
            <div class="card-header">
              <span>基本信息</span>
            </div>
          </template>

          <div class="info-content">
            <div class="avatar-section">
              <el-avatar :size="80" icon="UserFilled" />
            </div>

            <el-descriptions :column="1" border>
              <el-descriptions-item label="用户名">
                {{ user.username }}
              </el-descriptions-item>
              <el-descriptions-item label="邮箱">
                {{ user.email }}
              </el-descriptions-item>
              <el-descriptions-item label="角色">
                <el-tag :type="user.role === 'admin' ? 'danger' : 'primary'">
                  {{ user.role === 'admin' ? '管理员' : '普通用户' }}
                </el-tag>
              </el-descriptions-item>
              <el-descriptions-item label="注册时间">
                {{ formatDate(user.created_at) }}
              </el-descriptions-item>
              <el-descriptions-item label="更新时间">
                {{ user.updated_at ? formatDate(user.updated_at) : '未更新' }}
              </el-descriptions-item>
            </el-descriptions>
          </div>
        </el-card>
      </el-col>

      <!-- 右侧：操作卡片 -->
      <el-col :xs="24" :sm="24" :md="16" :lg="16" :xl="16">
        <el-row :gutter="20">
          <!-- 更新用户信息 -->
          <el-col :xs="24" :sm="24" :md="12" :lg="12" :xl="12">
            <el-card class="action-card">
              <template #header>
                <div class="card-header">
                  <span>更新信息</span>
                </div>
              </template>

              <el-form
                ref="updateFormRef"
                :model="updateForm"
                :rules="updateRules"
                label-width="80px"
                @submit.prevent="handleUpdate"
              >
                <el-form-item label="用户名" prop="username">
                  <el-input
                    v-model="updateForm.username"
                    placeholder="新的用户名"
                    clearable
                  />
                </el-form-item>

                <el-form-item label="邮箱" prop="email">
                  <el-input
                    v-model="updateForm.email"
                    placeholder="新的邮箱"
                    clearable
                  />
                </el-form-item>

                <el-form-item>
                  <el-button
                    type="primary"
                    :loading="updateLoading"
                    @click="handleUpdate"
                  >
                    更新信息
                  </el-button>
                  <el-button @click="resetUpdateForm">重置</el-button>
                </el-form-item>
              </el-form>
            </el-card>
          </el-col>

          <!-- 修改密码 -->
          <el-col :xs="24" :sm="24" :md="12" :lg="12" :xl="12">
            <el-card class="action-card">
              <template #header>
                <div class="card-header">
                  <span>修改密码</span>
                </div>
              </template>

              <el-form
                ref="passwordFormRef"
                :model="passwordForm"
                :rules="passwordRules"
                label-width="100px"
                @submit.prevent="handleChangePassword"
              >
                <el-form-item label="当前密码" prop="currentPassword">
                  <el-input
                    v-model="passwordForm.currentPassword"
                    type="password"
                    placeholder="输入当前密码"
                    show-password
                    clearable
                  />
                </el-form-item>

                <el-form-item label="新密码" prop="newPassword">
                  <el-input
                    v-model="passwordForm.newPassword"
                    type="password"
                    placeholder="输入新密码（至少 6 位）"
                    show-password
                    clearable
                  />
                </el-form-item>

                <el-form-item label="确认密码" prop="confirmPassword">
                  <el-input
                    v-model="passwordForm.confirmPassword"
                    type="password"
                    placeholder="再次输入新密码"
                    show-password
                    clearable
                    @keyup.enter="handleChangePassword"
                  />
                </el-form-item>

                <el-form-item>
                  <el-button
                    type="primary"
                    :loading="passwordLoading"
                    @click="handleChangePassword"
                  >
                    修改密码
                  </el-button>
                  <el-button @click="resetPasswordForm">重置</el-button>
                </el-form-item>
              </el-form>
            </el-card>
          </el-col>

          <!-- 危险操作 -->
          <el-col :xs="24" :sm="24" :md="24" :lg="24" :xl="24">
            <el-card class="danger-card">
              <template #header>
                <div class="card-header danger">
                  <span>危险操作</span>
                </div>
              </template>

              <el-alert
                title="删除账号后，所有数据将无法恢复！"
                type="error"
                :closable="false"
                show-icon
              />

              <div class="delete-section">
                <el-button
                  type="danger"
                  :loading="deleteLoading"
                  @click="showDeleteDialog"
                >
                  删除账号
                </el-button>
              </div>
            </el-card>
          </el-col>
        </el-row>
      </el-col>
    </el-row>

    <!-- 删除账号确认对话框 -->
    <el-dialog
      v-model="deleteDialogVisible"
      title="确认删除账号"
      width="400px"
      :close-on-click-modal="false"
    >
      <el-alert
        title="此操作不可逆！删除账号后，所有数据包括文章、收藏等都将被永久删除。"
        type="warning"
        :closable="false"
        show-icon
      />

      <el-form
        ref="deleteFormRef"
        :model="deleteForm"
        :rules="deleteRules"
        label-width="80px"
        style="margin-top: 20px"
      >
        <el-form-item label="密码" prop="password">
          <el-input
            v-model="deleteForm.password"
            type="password"
            placeholder="输入密码以确认删除"
            show-password
            clearable
          />
        </el-form-item>
      </el-form>

      <template #footer>
        <el-button @click="deleteDialogVisible = false">取消</el-button>
        <el-button type="danger" :loading="deleteLoading" @click="handleDelete">
          确认删除
        </el-button>
      </template>
    </el-dialog>
  </div>
</template>

<script setup>
import { ref, reactive, onMounted } from 'vue'
import { useRouter } from 'vue-router'
import { ElMessage, ElMessageBox } from 'element-plus'
import { useAuthStore } from '@/stores/auth'
import { updateProfile, changePassword, deleteAccount } from '@/api/auth'

const router = useRouter()
const authStore = useAuthStore()

// 用户信息
const user = ref({})

// 更新信息表单
const updateForm = reactive({
  username: '',
  email: ''
})

const updateRules = {
  username: [
    { min: 3, max: 20, message: '用户名长度在 3 到 20 个字符', trigger: 'blur' }
  ],
  email: [
    { type: 'email', message: '请输入正确的邮箱格式', trigger: 'blur' }
  ]
}

const updateFormRef = ref(null)
const updateLoading = ref(false)

// 修改密码表单
const passwordForm = reactive({
  currentPassword: '',
  newPassword: '',
  confirmPassword: ''
})

const validateConfirmPassword = (rule, value, callback) => {
  if (value === '') {
    callback(new Error('请再次输入密码'))
  } else if (value !== passwordForm.newPassword) {
    callback(new Error('两次输入的密码不一致'))
  } else {
    callback()
  }
}

const passwordRules = {
  currentPassword: [
    { required: true, message: '请输入当前密码', trigger: 'blur' }
  ],
  newPassword: [
    { required: true, message: '请输入新密码', trigger: 'blur' },
    { min: 6, message: '密码长度不能少于 6 位', trigger: 'blur' }
  ],
  confirmPassword: [
    { required: true, validator: validateConfirmPassword, trigger: 'blur' }
  ]
}

const passwordFormRef = ref(null)
const passwordLoading = ref(false)

// 删除账号
const deleteDialogVisible = ref(false)
const deleteForm = reactive({
  password: ''
})

const deleteRules = {
  password: [
    { required: true, message: '请输入密码', trigger: 'blur' }
  ]
}

const deleteFormRef = ref(null)
const deleteLoading = ref(false)

// 格式化日期
const formatDate = (dateString) => {
  if (!dateString) return '-'
  const date = new Date(dateString)
  return date.toLocaleDateString('zh-CN', {
    year: 'numeric',
    month: '2-digit',
    day: '2-digit',
    hour: '2-digit',
    minute: '2-digit'
  })
}

// 处理更新信息
const handleUpdate = async () => {
  if (!updateFormRef.value) return

  try {
    await updateFormRef.value.validate()
    updateLoading.value = true

    const updateData = {}
    if (updateForm.username) updateData.username = updateForm.username
    if (updateForm.email) updateData.email = updateForm.email

    const response = await updateProfile(updateData)

    ElMessage.success(response.message || '更新成功')

    // 刷新用户信息
    await authStore.fetchCurrentUser()
    user.value = authStore.user

    // 重置表单
    resetUpdateForm()
  } catch (error) {
    if (error !== false) {
      ElMessage.error(error.response?.data?.detail || '更新失败')
    }
  } finally {
    updateLoading.value = false
  }
}

// 重置更新表单
const resetUpdateForm = () => {
  if (updateFormRef.value) {
    updateFormRef.value.resetFields()
  }
  updateForm.username = ''
  updateForm.email = ''
}

// 处理修改密码
const handleChangePassword = async () => {
  if (!passwordFormRef.value) return

  try {
    await passwordFormRef.value.validate()
    passwordLoading.value = true

    const response = await changePassword(
      passwordForm.currentPassword,
      passwordForm.newPassword
    )

    ElMessage.success(response.message || '修改密码成功')
    resetPasswordForm()
  } catch (error) {
    if (error !== false) {
      ElMessage.error(error.response?.data?.detail || '修改密码失败')
    }
  } finally {
    passwordLoading.value = false
  }
}

// 重置密码表单
const resetPasswordForm = () => {
  if (passwordFormRef.value) {
    passwordFormRef.value.resetFields()
  }
}

// 显示删除对话框
const showDeleteDialog = () => {
  deleteDialogVisible.value = true
}

// 处理删除账号
const handleDelete = async () => {
  if (!deleteFormRef.value) return

  try {
    await deleteFormRef.value.validate()
    deleteLoading.value = true

    const response = await deleteAccount(deleteForm.password)

    ElMessage.success(response.message || '账号已删除')

    // 登出并跳转到首页
    await authStore.handleLogout()
    router.push('/login')
  } catch (error) {
    if (error !== false) {
      ElMessage.error(error.response?.data?.detail || '删除账号失败')
    }
  } finally {
    deleteLoading.value = false
  }
}

// 从 Pinia store 加载用户信息
onMounted(async () => {
  try {
    // 获取最新的用户信息
    await authStore.fetchCurrentUser()
    user.value = authStore.user

    // 初始化表单
    updateForm.username = user.value.username || ''
    updateForm.email = user.value.email || ''
  } catch (error) {
    ElMessage.error('获取用户信息失败')
  }
})
</script>

<style scoped>
.profile-container {
  padding: 20px;
  max-width: 1200px;
  margin: 0 auto;
}

.profile-header {
  margin-bottom: 30px;
  text-align: center;
}

.profile-header h1 {
  margin: 0 0 10px 0;
  font-size: 32px;
  font-weight: 600;
  color: #1a1a1a;
}

.profile-header p {
  margin: 0;
  font-size: 16px;
  color: #86909c;
}

.card-header {
  display: flex;
  justify-content: space-between;
  align-items: center;
  font-weight: 600;
}

.card-header.danger {
  color: #f53f3f;
}

.info-card,
.action-card,
.danger-card {
  margin-bottom: 20px;
}

.info-content {
  padding: 10px 0;
}

.avatar-section {
  display: flex;
  justify-content: center;
  margin-bottom: 20px;
}

.delete-section {
  margin-top: 20px;
}
</style>
