# arXiv文献推荐APP - 完整原型

一个基于小红书/知乎风格的arXiv文献推荐移动应用，支持个性化推荐、团队协作、每日简报等功能。

## 📱 功能特性

### 核心功能
- 🔍 **个性化推荐**：基于用户兴趣的arXiv论文智能推荐
- 📚 **每日简报**：每天早上9点推送10篇优秀论文
- 🏷️ **关键词标签**：自动提取论文关键词，支持标签筛选
- ❤️ **收藏管理**：个人文献库，支持分类整理
- 👥 **团队协作**：团队空间，老板推荐文章，员工标记待阅读
- ⏰ **任务提醒**：阅读任务管理和提醒

### 社交功能
- 📤 **文章推荐**：向团队推荐文章
- 💬 **评论讨论**：论文讨论区
- 🏷️ **待阅读标签**：团队协作阅读管理
- 📊 **阅读统计**：个人和团队阅读进度

## 🏗️ 项目结构

```
arxiv_app_prototype/
├── backend/                    # 后端服务
│   ├── app.py                 # FastAPI主应用
│   ├── requirements.txt       # Python依赖
│   └── arxiv_app.db          # SQLite数据库
├── frontend/                  # 移动端应用
│   ├── App.js                # React Native主组件
│   ├── package.json          # Node.js依赖
│   ├── babel.config.js       # Babel配置
│   └── metro.config.js       # Metro配置
└── README.md                 # 项目说明
```

## 🚀 快速开始

### 后端启动

```bash
# 进入后端目录
cd backend

# 安装依赖
pip install -r requirements.txt

# 启动服务
python app.py

# 服务将在 http://localhost:8000 运行
```

### 前端启动

```bash
# 进入前端目录
cd frontend

# 安装依赖
npm install

# 启动React Native开发服务器
npx react-native start

# 在另一个终端运行iOS/Android
npx react-native run-ios    # iOS
npx react-native run-android # Android
```

## 📊 API接口

### 用户相关
- `POST /users/register` - 用户注册
- `GET /users/{username}/recommendations` - 获取个性化推荐
- `POST /users/{username}/collect/{paper_id}` - 收藏论文
- `GET /users/{username}/collections` - 获取收藏列表

### 论文相关
- `GET /papers/search` - 搜索论文
- `GET /papers/{paper_id}` - 获取论文详情
- `GET /papers/{paper_id}/related` - 获取相关论文

### 团队相关
- `POST /teams/create` - 创建团队
- `POST /teams/{team_id}/recommend` - 向团队推荐文章

### 任务相关
- `POST /reading-tasks/create` - 创建阅读任务
- `GET /daily-digest/{username}` - 获取每日简报

## 🎨 界面设计

### 首页（小红书式feed流）
- 个性化论文推荐卡片
- 关键词标签展示
- 收藏/分享功能
- 每日简报入口

### 搜索页
- 关键词搜索
- 兴趣标签快速搜索
- 搜索结果卡片展示

### 收藏页
- 个人文献库
- 分类管理
- 阅读进度跟踪

### 个人中心
- 用户信息
- 兴趣标签管理
- 阅读统计
- 团队管理
- 设置

## 🔧 技术栈

### 后端
- **框架**：FastAPI (Python)
- **数据库**：SQLite (开发) / PostgreSQL (生产)
- **任务队列**：Celery + Redis
- **API文档**：自动生成的OpenAPI文档

### 前端
- **框架**：React Native
- **导航**：React Navigation
- **UI组件**：React Native Vector Icons
- **状态管理**：React Hooks

### 基础设施
- **容器化**：Docker
- **部署**：AWS/GCP/Azure
- **CI/CD**：GitHub Actions
- **推送通知**：Firebase Cloud Messaging

## 📅 定时任务

### 每日简报系统
- **时间**：每天上午9:00
- **内容**：
  1. 爬取最新arXiv论文
  2. 基于用户兴趣智能筛选
  3. 生成10篇优质论文简报
  4. 发送推送通知

### 阅读任务提醒
- **时间**：用户设置的提醒时间
- **内容**：
  1. 检查待阅读任务
  2. 发送提醒通知
  3. 更新任务状态

## 🚀 部署指南

### 开发环境
```bash
# 1. 克隆项目
git clone <repository-url>
cd arxiv_app_prototype

# 2. 启动后端
cd backend
pip install -r requirements.txt
python app.py

# 3. 启动前端
cd ../frontend
npm install
npx react-native start
npx react-native run-ios
```

### 生产环境
```bash
# 使用Docker部署
docker build -t arxiv-app-backend ./backend
docker build -t arxiv-app-frontend ./frontend

# 使用docker-compose
docker-compose up -d
```

## 📈 扩展计划

### 阶段1：MVP (已完成)
- 基础推荐功能
- 简单用户界面
- 收藏功能

### 阶段2：增强版
- 智能推荐算法优化
- 团队协作功能
- 每日简报系统

### 阶段3：社交版
- 评论讨论功能
- 高级团队管理
- 数据分析面板

### 阶段4：企业版
- 多团队管理
- 高级权限控制
- 数据导出功能

## 🤝 贡献指南

欢迎提交Issue和Pull Request！

1. Fork项目
2. 创建功能分支
3. 提交更改
4. 创建Pull Request

## 📄 许可证

MIT License