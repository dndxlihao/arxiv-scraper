# GitHub仓库设置指南

## 步骤1：创建GitHub仓库

### 方法A：通过GitHub网站创建
1. 访问 https://github.com/new
2. 填写仓库信息：
   - **Repository name**: `arxiv-paper-assistant`
   - **Description**: `arXiv论文助手 - 完整的iOS原生应用，自动爬取论文并提供个性化推送`
   - **Public** (公开) 或 **Private** (私有)
   - 不要勾选 "Initialize this repository with a README" (我们已经有了)
3. 点击 "Create repository"

### 方法B：通过GitHub CLI创建 (如果已安装)
```bash
gh repo create arxiv-paper-assistant \
  --description "arXiv论文助手 - 完整的iOS原生应用" \
  --public \
  --source=. \
  --remote=origin \
  --push
```

## 步骤2：连接到远程仓库

### 如果已经创建了仓库，执行以下命令：

```bash
cd /Users/lihao/.openclaw/workspace/arxiv_mobile_app

# 添加远程仓库（替换 YOUR_USERNAME 为你的GitHub用户名）
git remote add origin https://github.com/YOUR_USERNAME/arxiv-paper-assistant.git

# 或者使用SSH（推荐）
git remote add origin git@github.com:YOUR_USERNAME/arxiv-paper-assistant.git
```

## 步骤3：推送代码到GitHub

```bash
# 首次推送
git push -u origin main

# 如果遇到错误，可能需要先拉取
git pull origin main --allow-unrelated-histories

# 或者强制推送（如果确定要覆盖）
git push -u origin main --force
```

## 步骤4：配置GitHub Actions（可选）

仓库中已经包含了基本的GitHub Actions配置，用于：
- 自动测试
- 代码质量检查
- 自动部署

## 步骤5：设置仓库特性

### 推荐设置：
1. **分支保护规则** (Settings → Branches)
   - 要求Pull Request审查
   - 要求状态检查通过
   - 要求线性历史

2. **Issue模板** (已经包含在仓库中)
   - Bug报告模板
   - 功能请求模板

3. **Pull Request模板** (已经包含)

4. **CODEOWNERS文件** (已经包含)

## 步骤6：配置Secrets（用于CI/CD）

在GitHub仓库的 Settings → Secrets and variables → Actions 中添加：

### 必需的环境变量：
- `DOCKER_USERNAME` - Docker Hub用户名
- `DOCKER_PASSWORD` - Docker Hub密码
- `SSH_PRIVATE_KEY` - 服务器SSH私钥
- `SERVER_HOST` - 服务器地址
- `SERVER_USER` - 服务器用户名

### 可选的环境变量：
- `SENTRY_DSN` - Sentry错误监控
- `CODECOV_TOKEN` - 代码覆盖率
- `SLACK_WEBHOOK` - Slack通知

## 步骤7：启用GitHub Pages（用于文档）

1. Settings → Pages
2. Source: GitHub Actions
3. 文档会自动部署到：https://YOUR_USERNAME.github.io/arxiv-paper-assistant/

## 步骤8：项目管理

### 使用GitHub Projects：
1. 创建新项目
2. 添加列：Backlog, To Do, In Progress, Review, Done
3. 连接仓库，自动同步Issue和PR

### 使用Milestones：
1. 创建里程碑：v1.0.0, v1.1.0等
2. 分配Issue和PR到对应里程碑

## 步骤9：协作设置

### 添加协作者：
1. Settings → Collaborators
2. 添加团队成员
3. 设置权限级别

### 代码审查：
1. 要求所有PR至少有一个审查
2. 使用代码审查模板

## 步骤10：监控和分析

### 启用Insights：
1. Pulse - 查看项目活跃度
2. Graphs - 贡献统计
3. Traffic - 访问统计

### 集成服务：
1. **Codecov** - 代码覆盖率
2. **SonarCloud** - 代码质量
3. **Dependabot** - 依赖更新

## 故障排除

### 常见问题：

**Q: 推送时提示 "remote: Permission denied"**
A: 检查SSH密钥配置或使用HTTPS URL

**Q: 无法连接到远程仓库**
A: 检查网络连接，或使用 `git remote -v` 查看配置

**Q: 合并冲突**
A: 使用 `git pull --rebase origin main` 然后解决冲突

**Q: 忘记添加文件**
A: 使用 `git add .` 然后 `git commit --amend` 或创建新的提交

## 下一步

1. 创建GitHub仓库
2. 推送代码
3. 配置CI/CD
4. 开始功能开发

---

**提示**：建议使用SSH密钥进行认证，更安全方便。可以在GitHub Settings → SSH and GPG keys中添加SSH公钥。