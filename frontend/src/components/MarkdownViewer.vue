<template>
  <div class="markdown-viewer">
    <div class="toolbar">
      <el-button-group>
        <el-button size="small" @click="toggleTheme">
          {{ isDark ? '🌙' : '☀️' }}
        </el-button>
        <el-button size="small" @click="copyContent">复制内容</el-button>
        <el-button size="small" @click="exportMarkdown">导出 Markdown</el-button>
      </el-button-group>
    </div>
    <div v-html="htmlContent" :class="['markdown-body', { 'markdown-dark': isDark }]"></div>
  </div>
</template>

<script setup>
import { ref, computed, watch } from 'vue'
import { marked } from 'marked'
import { ElMessage } from 'element-plus'

const props = defineProps({
  content: {
    type: String,
    default: ''
  }
})

const isDark = ref(false)

// 配置 marked
marked.setOptions({
  breaks: true,
  gfm: true
})

const htmlContent = computed(() => {
  if (!props.content) return '<p class="empty">暂无内容</p>'
  return marked(props.content)
})

function toggleTheme() {
  isDark.value = !isDark.value

  // 应用代码高亮主题
  if (isDark.value) {
    document.getElementById('hljs-theme')?.remove()
    const link = document.createElement('link')
    link.id = 'hljs-theme'
    link.rel = 'stylesheet'
    link.href = 'https://cdnjs.cloudflare.com/ajax/libs/highlight.js/11.9.0/styles/github-dark.min.css'
    document.head.appendChild(link)
  } else {
    document.getElementById('hljs-theme')?.remove()
    const link = document.createElement('link')
    link.id = 'hljs-theme'
    link.rel = 'stylesheet'
    link.href = 'https://cdnjs.cloudflare.com/ajax/libs/highlight.js/11.9.0/styles/github.min.css'
    document.head.appendChild(link)
  }
}

function copyContent() {
  navigator.clipboard.writeText(props.content)
  ElMessage.success('已复制到剪贴板')
}

function exportMarkdown() {
  const blob = new Blob([props.content], { type: 'text/markdown' })
  const url = URL.createObjectURL(blob)
  const a = document.createElement('a')
  a.href = url
  a.download = `article_${Date.now()}.md`
  a.click()
  URL.revokeObjectURL(url)
  ElMessage.success('导出成功')
}

// 初始化代码高亮主题
if (typeof document !== 'undefined') {
  const link = document.createElement('link')
  link.rel = 'stylesheet'
  link.href = 'https://cdnjs.cloudflare.com/ajax/libs/highlight.js/11.9.0/styles/github.min.css'
  document.head.appendChild(link)
}
</script>

<style scoped>
.markdown-viewer {
  padding: 20px;
}

.toolbar {
  margin-bottom: 20px;
  display: flex;
  gap: 10px;
}

.markdown-body {
  padding: 20px;
  background: #fff;
  border-radius: 8px;
  color: #24292e;
  line-height: 1.6;
}

.markdown-dark {
  background: #0d1117;
  color: #c9d1d9;
}

.markdown-body :deep(h1),
.markdown-body :deep(h2),
.markdown-body :deep(h3),
.markdown-body :deep(h4) {
  margin-top: 1.5em;
  margin-bottom: 0.5em;
  font-weight: 600;
}

.markdown-body :deep(p) {
  margin-bottom: 1em;
}

.markdown-body :deep(code) {
  background: #f6f8fa;
  padding: 0.2em 0.4em;
  border-radius: 3px;
  font-size: 0.9em;
}

.markdown-dark :deep(code) {
  background: #161b22;
}

.markdown-body :deep(pre) {
  background: #f6f8fa;
  padding: 16px;
  border-radius: 6px;
  overflow-x: auto;
}

.markdown-dark :deep(pre) {
  background: #161b22;
}

.markdown-body :deep(img) {
  max-width: 100%;
  height: auto;
  border-radius: 4px;
}

.markdown-body :deep(blockquote) {
  border-left: 4px solid #d0d7de;
  padding-left: 16px;
  color: #6e7781;
}

.markdown-dark :deep(blockquote) {
  border-left-color: #30363d;
  color: #8b949e;
}

.markdown-body :deep(a) {
  color: #0969da;
  text-decoration: none;
}

.markdown-body :deep(a:hover) {
  text-decoration: underline;
}

.empty {
  text-align: center;
  color: #999;
  padding: 40px;
}
</style>
