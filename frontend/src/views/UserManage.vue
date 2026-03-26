<template>
  <div class="user-manage">
    <div class="page-header">
      <h2>用户管理</h2>
      <el-button type="primary" @click="showAddUserDialog">
        <el-icon><Plus /></el-icon>
        添加用户
      </el-button>
    </div>

    <el-table
      v-loading="loading"
      :data="users"
      stripe
      class="users-table"
    >
      <el-table-column prop="id" label="ID" width="80" />
      <el-table-column prop="username" label="用户名" width="150" />
      <el-table-column prop="email" label="邮箱" width="200" />
      <el-table-column label="角色" width="120">
        <template #default="{ row }">
          <el-tag :type="row.role === 'admin' ? 'danger' : 'primary'">
            {{ row.role === 'admin' ? '管理员' : '普通用户' }}
          </el-tag>
        </template>
      </el-table-column>
      <el-table-column label="创建时间" width="180">
        <template #default="{ row }">
          {{ formatDate(row.created_at) }}
        </template>
      </el-table-column>
      <el-table-column label="操作" fixed="right" width="200">
        <template #default="{ row }">
          <el-button
            v-if="row.id !== authStore.user?.id"
            type="primary"
            size="small"
            @click="showEditUserDialog(row)"
          >
            编辑
          </el-button>
          <el-button
            v-if="row.id !== authStore.user?.id"
            type="danger"
            size="small"
            @click="handleDeleteUser(row)"
          >
            删除
          </el-button>
          <el-tag v-else type="info" size="small">当前用户</el-tag>
        </template>
      </el-table-column>
    </el-table>

    <!-- 分页 -->
    <div class="pagination">
      <el-pagination
        v-model:current-page="currentPage"
        v-model:page-size="pageSize"
        :total="total"
        :page-sizes="[10, 20, 50, 100]"
        layout="total, sizes, prev, pager, next"
        @change="fetchUsers"
      />
    </div>

    <!-- 添加/编辑用户对话框 -->
    <el-dialog
      v-model="dialogVisible"
      :title="isEdit ? '编辑用户' : '添加用户'"
      width="500px"
      @close="resetDialog"
    >
      <el-form
        ref="userFormRef"
        :model="userForm"
        :rules="userRules"
        label-width="80px"
      >
        <el-form-item label="用户名" prop="username">
          <el-input v-model="userForm.username" placeholder="请输入用户名" />
        </el-form-item>

        <el-form-item label="邮箱" prop="email">
          <el-input v-model="userForm.email" placeholder="请输入邮箱" />
        </el-form-item>

        <el-form-item v-if="!isEdit" label="密码" prop="password">
          <el-input
            v-model="userForm.password"
            type="password"
            placeholder="请输入密码"
            show-password
          />
        </el-form-item>

        <el-form-item label="角色" prop="role">
          <el-select v-model="userForm.role" placeholder="请选择角色">
            <el-option label="普通用户" value="user" />
            <el-option label="管理员" value="admin" />
          </el-select>
        </el-form-item>
      </el-form>

      <template #footer>
        <el-button @click="dialogVisible = false">取消</el-button>
        <el-button type="primary" :loading="submitting" @click="handleSubmit">
          确定
        </el-button>
      </template>
    </el-dialog>
  </div>
</template>

<script setup>
import { ref, reactive, onMounted } from 'vue'
import { ElMessage, ElMessageBox } from 'element-plus'
import { getUsers, createUser, updateUser, deleteUser } from '@/api/auth'
import { useAuthStore } from '@/stores/auth'

const authStore = useAuthStore()

// 用户列表数据
const users = ref([])
const loading = ref(false)
const total = ref(0)
const currentPage = ref(1)
const pageSize = ref(10)

// 对话框相关
const dialogVisible = ref(false)
const isEdit = ref(false)
const submitting = ref(false)
const userId = ref(null)

// 用户表单
const userForm = reactive({
  username: '',
  email: '',
  password: '',
  role: 'user'
})

// 表单验证规则
const userRules = {
  username: [
    { required: true, message: '请输入用户名', trigger: 'blur' },
    { min: 3, max: 20, message: '用户名长度在 3 到 20 个字符', trigger: 'blur' }
  ],
  email: [
    { required: true, message: '请输入邮箱', trigger: 'blur' },
    { type: 'email', message: '请输入正确的邮箱格式', trigger: 'blur' }
  ],
  password: [
    { required: true, message: '请输入密码', trigger: 'blur' },
    { min: 6, message: '密码长度不能少于 6 位', trigger: 'blur' }
  ],
  role: [
    { required: true, message: '请选择角色', trigger: 'change' }
  ]
}

const userFormRef = ref(null)

// 获取用户列表
const fetchUsers = async () => {
  loading.value = true
  try {
    const response = await getUsers({
      skip: (currentPage.value - 1) * pageSize.value,
      limit: pageSize.value
    })
    users.value = response.users
    total.value = response.total
  } catch (error) {
    ElMessage.error('获取用户列表失败')
  } finally {
    loading.value = false
  }
}

// 显示添加用户对话框
const showAddUserDialog = () => {
  isEdit.value = false
  userId.value = null
  dialogVisible.value = true
}

// 显示编辑用户对话框
const showEditUserDialog = (row) => {
  isEdit.value = true
  userId.value = row.id
  Object.assign(userForm, {
    username: row.username,
    email: row.email,
    password: '',
    role: row.role
  })
  dialogVisible.value = true
}

// 重置对话框
const resetDialog = () => {
  Object.assign(userForm, {
    username: '',
    email: '',
    password: '',
    role: 'user'
  })
  if (userFormRef.value) {
    userFormRef.value.resetFields()
  }
}

// 处理提交
const handleSubmit = async () => {
  if (!userFormRef.value) return

  try {
    await userFormRef.value.validate()
    submitting.value = true

    if (isEdit.value) {
      // 更新用户
      await updateUser(userId.value, {
        role: userForm.role
      })
      ElMessage.success('用户更新成功')
    } else {
      // 创建用户
      await createUser(userForm)
      ElMessage.success('用户创建成功')
    }

    dialogVisible.value = false
    await fetchUsers()
  } catch (error) {
    if (error !== false) {
      ElMessage.error(isEdit.value ? '更新用户失败' : '创建用户失败')
    }
  } finally {
    submitting.value = false
  }
}

// 处理删除用户
const handleDeleteUser = async (row) => {
  try {
    await ElMessageBox.confirm(
      `确定要删除用户 "${row.username}" 吗？`,
      '警告',
      {
        confirmButtonText: '确定',
        cancelButtonText: '取消',
        type: 'warning'
      }
    )

    await deleteUser(row.id)
    ElMessage.success('用户删除成功')
    await fetchUsers()
  } catch (error) {
    // 用户取消
  }
}

// 格式化日期
const formatDate = (dateStr) => {
  if (!dateStr) return '-'
  const date = new Date(dateStr)
  return date.toLocaleString('zh-CN')
}

// 获取路由并添加用户管理路由
onMounted(async () => {
  // 检查是否为管理员
  if (!authStore.isAdmin()) {
    ElMessage.error('权限不足')
    return
  }

  await fetchUsers()
})
</script>

<style scoped>
.user-manage {
  background: white;
  border-radius: 8px;
  padding: 20px;
}

.page-header {
  display: flex;
  justify-content: space-between;
  align-items: center;
  margin-bottom: 20px;
}

.page-header h2 {
  margin: 0;
  font-size: 20px;
  font-weight: 500;
}

.users-table {
  margin-bottom: 20px;
}

.pagination {
  display: flex;
  justify-content: flex-end;
  padding-top: 20px;
  border-top: 1px solid #e6e6e6;
}
</style>
