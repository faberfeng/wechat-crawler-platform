<template>
  <transition name="fade">
    <div v-if="message" class="form-validator" :class="`form-validator--${type}`">
      <el-icon class="form-validator__icon">
        <SuccessFilled v-if="type === 'success'" />
        <WarningFilled v-if="type === 'warning'" />
        <CircleCloseFilled v-if="type === 'error'" />
        <InfoFilled v-if="type === 'info'" />
      </el-icon>
      <span class="form-validator__message">{{ message }}</span>
    </div>
  </transition>
</template>

<script setup>
import { computed } from 'vue'
import {
  SuccessFilled,
  WarningFilled,
  CircleCloseFilled,
  InfoFilled
} from '@element-plus/icons-vue'

const props = defineProps({
  type: {
    type: String,
    default: 'error',
    validator: (value) => ['success', 'warning', 'error', 'info'].includes(value)
  },
  message: {
    type: String,
    default: ''
  }
})
</script>

<style scoped>
.form-validator {
  display: flex;
  align-items: center;
  gap: 8px;
  padding: 8px 12px;
  border-radius: 8px;
  font-size: 14px;
  margin-top: 4px;
  transition: all 0.3s ease;
}

.form-validator--success {
  background: #f0f9ff;
  color: #00c853;
  border: 1px solid #b9f6ca;
}

.form-validator--warning {
  background: #fff8e1;
  color: #ff9800;
  border: 1px solid #ffe082;
}

.form-validator--error {
  background: #ffebee;
  color: #f44336;
  border: 1px solid #ffcdd2;
}

.form-validator--info {
  background: #e3f2fd;
  color: #2196f3;
  border: 1px solid #bbdefb;
}

.form-validator__icon {
  font-size: 16px;
}

.form-validator__message {
  flex: 1;
  line-height: 1.5;
}

.fade-enter-active,
.fade-leave-active {
  transition: all 0.3s ease;
}

.fade-enter-from,
.fade-leave-to {
  opacity: 0;
  transform: translateY(-10px);
}
</style>
