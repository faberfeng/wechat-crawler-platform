# 贡献指南

感谢你有意参与 WeChat Crawler Platform 的开发！

---

## 🤝 如何贡献

### 报告 Bug

如果你发现了 Bug，请：

1. 先在 [Issues](../../issues) 中搜索，确认问题未被报告
2. 创建新的 Issue，使用 Bug 模板
3. 详细描述问题的复现步骤、预期行为和实际行为
4. 提供相关日志、截图等信息

### 提出新功能

如果你有新功能建议：

1. 先在 [Issues](../../issues) 中搜索，确认功能未被提出
2. 创建新的 Issue，使用 Feature Request 模板
3. 详细描述功能需求、使用场景和预期效果
4. 讨论实现方案的可行性

### 提交代码

如果你想贡献代码：

1. Fork 本仓库
2. 创建功能分支 (`git checkout -b feature/AmazingFeature`)
3. 提交更改 (`git commit -m 'Add some AmazingFeature'`)
4. 推送到分支 (`git push origin feature/AmazingFeature`)
5. 创建 Pull Request

---

## 📝 开发规范

### 代码风格

**Python**:
- 遵循 PEP 8 规范
- 使用 4 空格缩进
- 使用类型提示
- 添加必要的文档字符串

**JavaScript/Vue**:
- 使用 ESLint 进行代码检查
- 使用 2 空格缩进
- 组件命名使用 PascalCase
- 文件名使用 kebab-case

### Git Commit 规范

使用语义化的提交信息格式：

```
<type>(<scope>): <subject>

<body>

<footer>
```

**类型 (type)**:
- `feat`: 新功能
- `fix`: 修复 Bug
- `docs`: 文档更新
- `style`: 代码格式（不影响代码运行）
- `refactor`: 重构（既不是新功能也不是修复 Bug）
- `perf`: 性能优化
- `test`: 测试相关
- `chore`: 构建过程或辅助工具的变动

**示例**:
```
feat(auth): 添加 JWT 登录功能

- 实现用户认证中间件
- 添加登录和登出 API
- 更新前端登录界面

Closes #123
```

---

## 🧪 测试

### 运行测试

**后端测试**:
```bash
cd backend
pytest
```

**前端测试**:
```bash
cd frontend
npm run test
```

### 添加测试

- 为新功能添加单元测试
- 确保所有测试通过后再提交 PR
- 保持测试覆盖率在合理水平

---

## 📚 文档

当你添加新功能或修改现有功能时：

1. 更新 README.md 的相关部分
2. 更新 API 文档
3. 添加必要的注释
4. 更新使用示例

---

## 🎯 开发流程建议

### 开始开发前

1. 先在 Issues 中讨论你的想法
2. 确认 Issue 已经被分配给你
3. 创建对应的开发分支

### 开发过程

1. 实现功能
2. 编写测试
3. 运行本地测试
4. 更新文档

### 提交 PR 前

1. 运行所有测试
2. 确保代码通过 lint 检查
3. 压缩或最小化 commit（squash commits）
4. 更新相关文档
5. 在 PR 描述中写明做了什么和为什么

### PR 审查

- 保持对反馈的开放态度
- 及时回应维护者的评论
- 根据建议修改代码

---

## 📞 联系方式

如有任何问题，欢迎：

- 提交 [Issue](../../issues)
- 发起 [Discussion](../../discussions)
- 联系维护者: faberfeng

---

感谢你的贡献！🎉
