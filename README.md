# 📱 arXiv Paper Assistant - iOS 论文助手

![Swift](https://img.shields.io/badge/Swift-5.9-orange?logo=swift)
![FastAPI](https://img.shields.io/badge/FastAPI-0.104-green?logo=fastapi)
![iOS](https://img.shields.io/badge/iOS-17.0+-blue?logo=apple)
![License](https://img.shields.io/badge/License-MIT-yellow)

一个智能的iOS原生应用，自动爬取arXiv论文并推送个性化通知，帮助研究人员及时获取最新研究成果。

## ✨ 核心功能

### 📚 智能论文推荐
- **自动爬取**：定时从arXiv获取最新论文
- **个性化推荐**：基于用户兴趣和阅读历史
- **多学科覆盖**：支持CS、物理、数学等多个领域

### 🔔 实时通知推送
- **关键词提醒**：设置关注的关键词，匹配时立即通知
- **定时摘要**：每日/每周研究摘要推送
- **团队协作**：与团队成员共享重要发现

### 👥 团队协作
- **研究小组**：创建和管理研究团队
- **论文共享**：一键分享重要论文给团队成员
- **讨论区**：针对论文进行讨论和注释

## 🏗️ 项目架构

### 前端 (iOS App)
- **技术栈**: SwiftUI + Combine + Alamofire
- **架构模式**: MVVM (Model-View-ViewModel)
- **主要特性**:
  - 原生iOS体验
  - 离线阅读支持
  - 深色/浅色主题
  - 手势操作优化

### 后端 (API服务)
- **技术栈**: FastAPI + PostgreSQL + Redis
- **部署**: Docker + 云服务器
- **主要特性**:
  - RESTful API设计
  - JWT身份认证
  - 异步任务处理
  - 实时WebSocket通知

## 📁 项目结构

```
arxiv_mobile_app/
├── mobile_app/                    # 移动应用核心代码
│   ├── ios/                      # iOS SwiftUI应用
│   │   └── ArxivPaperAssistant/  # iOS项目主目录
│   │       ├── App/              # 应用入口和配置
│   │       ├── Models/           # 数据模型
│   │       ├── Views/            # 视图组件
│   │       ├── ViewModels/       # 视图模型
│   │       ├── Services/         # 网络服务
│   │       └── Utils/            # 工具类
│   └── backend/                  # 后端API服务
│       ├── app/                  # FastAPI应用
│       │   ├── api/              # API路由
│       │   ├── models/           # 数据库模型
│       │   ├── schemas/          # Pydantic模型
│       │   └── services/         # 业务逻辑
│       ├── alembic/              # 数据库迁移
│       └── requirements.txt      # Python依赖
├── 项目规划.md                   # 完整开发计划和时间线
├── 开发进展.md                   # 实时开发进度报告
└── README.md                     # 项目说明文档
```

## 🚀 快速开始

### 环境要求
- **macOS**: 14.0+ (用于iOS开发)
- **Xcode**: 15.0+
- **Python**: 3.11+
- **PostgreSQL**: 14.0+

### 后端启动
```bash
# 进入后端目录
cd mobile_app/backend

# 安装依赖
pip install -r requirements.txt

# 配置环境变量
cp .env.example .env
# 编辑.env文件，设置数据库连接等

# 启动服务
uvicorn app.main:app --reload --host 0.0.0.0 --port 8000
```

### iOS应用启动
1. 打开 `mobile_app/ios/ArxivPaperAssistant.xcodeproj`
2. 选择模拟器或连接真机
3. 点击运行按钮 (⌘R)

## 📊 开发进展

### ✅ 已完成
- [x] **项目基础架构** - GitHub仓库配置、项目结构设计
- [x] **iOS认证系统** - 登录、注册、重置密码完整实现
- [x] **后端API框架** - FastAPI基础架构、数据库模型设计
- [x] **UI设计系统** - SwiftUI界面、状态管理、错误处理

### 🚧 进行中
- [ ] **论文爬取服务** - arXiv API集成、定时任务
- [ ] **论文列表界面** - 列表展示、详情页面、收藏功能
- [ ] **推送通知系统** - 本地通知、推送服务器

### 📅 开发计划
查看 [项目规划.md](项目规划.md) 获取完整的时间线和里程碑。

## 🛠️ 技术栈详情

### iOS开发
| 技术 | 用途 | 版本 |
|------|------|------|
| SwiftUI | 界面框架 | 5.0+ |
| Combine | 响应式编程 | 内置 |
| Alamofire | 网络请求 | 5.8+ |
| KeychainAccess | 安全存储 | 4.2+ |
| UserNotifications | 推送通知 | 内置 |

### 后端开发
| 技术 | 用途 | 版本 |
|------|------|------|
| FastAPI | Web框架 | 0.104+ |
| SQLAlchemy | ORM | 2.0+ |
| Alembic | 数据库迁移 | 1.12+ |
| Redis | 缓存和消息队列 | 7.0+ |
| Celery | 异步任务 | 5.3+ |

## 🤝 贡献指南

我们欢迎各种形式的贡献！请查看以下指南：

1. **报告问题**：使用GitHub Issues报告bug或提出功能建议
2. **提交代码**：Fork仓库，创建功能分支，提交Pull Request
3. **代码规范**：遵循Swift和Python的官方编码规范
4. **测试要求**：新功能需要包含单元测试

### 开发流程
```bash
# 1. Fork仓库
# 2. 克隆你的fork
git clone https://github.com/YOUR_USERNAME/arxiv-scraper.git

# 3. 创建功能分支
git checkout -b feature/your-feature-name

# 4. 提交更改
git add .
git commit -m "Add: your feature description"

# 5. 推送到你的fork
git push origin feature/your-feature-name

# 6. 创建Pull Request
```

## 📱 App Store发布计划

### 测试阶段
1. **内部测试**：使用TestFlight进行团队测试
2. **公开测试**：邀请外部用户参与测试
3. **反馈收集**：收集用户反馈并优化

### 发布准备
1. **应用图标**：设计符合App Store规范的应用图标
2. **截图和视频**：准备各尺寸的应用截图和演示视频
3. **应用描述**：编写吸引人的应用描述和关键词
4. **隐私政策**：准备完整的隐私政策文档

### 审核要点
- 确保符合App Store审核指南
- 测试所有核心功能
- 准备审核说明文档
- 处理可能的审核拒绝情况

## 📄 许可证

本项目采用 MIT 许可证 - 查看 [LICENSE](LICENSE) 文件了解详情。

## 📞 联系与支持

- **GitHub Issues**: [报告问题或建议](https://github.com/dndxlihao/arxiv-scraper/issues)
- **电子邮件**: 通过GitHub个人资料联系
- **讨论区**: 欢迎在GitHub Discussions中交流

## 🙏 致谢

感谢所有为这个项目做出贡献的开发者！特别感谢：

- arXiv.org 提供开放的论文数据
- SwiftUI 和 FastAPI 社区提供的优秀框架
- 所有测试用户提供的宝贵反馈

---

**开始使用** → 查看 [开发进展.md](开发进展.md) 了解最新开发状态  
**参与开发** → 查看 [项目规划.md](项目规划.md) 了解开发计划  
**报告问题** → 前往 [GitHub Issues](https://github.com/dndxlihao/arxiv-scraper/issues)

⭐ **如果这个项目对你有帮助，请给我们一个Star！** ⭐