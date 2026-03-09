# arXiv论文助手 - 完整移动应用

一个完整的iOS原生应用，自动爬取arXiv论文并提供个性化推送通知。

## 🎯 项目概述

这是一个从零开始开发的完整移动应用项目，目标上架Apple App Store。应用主要功能包括：
- 自动爬取arXiv最新论文
- 基于用户兴趣的个性化推荐
- 实时推送通知
- 团队协作功能
- 阅读任务管理

## 📱 技术栈

### 前端 (iOS)
- **语言**: Swift 5.9+
- **框架**: SwiftUI
- **架构**: MVVM
- **数据库**: Core Data
- **推送**: Apple Push Notification Service (APNs)

### 后端
- **语言**: Python 3.9+
- **框架**: FastAPI
- **数据库**: PostgreSQL
- **异步**: asyncio, aiohttp
- **认证**: JWT
- **部署**: Docker, Nginx

### 第三方服务
- **推送**: APNs (iOS原生推送)
- **分析**: Firebase Analytics (可选)
- **存储**: AWS S3 (PDF存储)

## 🏗️ 项目结构

```
arxiv_mobile_app/
├── ios/                    # iOS原生代码
│   ├── ArxivReader/       # SwiftUI项目
│   ├── Tests/            # 测试文件
│   └── README.md         # iOS开发指南
├── backend/              # 后端API服务
│   ├── main.py          # 主程序
│   ├── models.py        # 数据模型
│   ├── database.py      # 数据库连接
│   ├── routers/         # API路由
│   ├── services/        # 业务服务
│   ├── utils/           # 工具函数
│   └── requirements.txt # Python依赖
├── design/              # 设计文件
│   ├── wireframes/      # 线框图
│   ├── mockups/         # 设计稿
│   └── assets/          # 资源文件
├── docs/                # 文档
│   ├── API文档.md       # API接口文档
│   ├── 数据库设计.md    # 数据库设计
│   └── 部署指南.md      # 部署说明
└── scripts/             # 脚本文件
    ├── deploy.sh        # 部署脚本
    └── setup.sh         # 环境设置脚本
```

## 🚀 快速开始

### 后端开发环境

1. **克隆项目**
   ```bash
   git clone https://github.com/yourusername/arxiv-paper-assistant.git
   cd arxiv-paper-assistant/backend
   ```

2. **创建虚拟环境**
   ```bash
   python -m venv venv
   source venv/bin/activate  # Linux/Mac
   # 或 venv\Scripts\activate  # Windows
   ```

3. **安装依赖**
   ```bash
   pip install -r requirements.txt
   ```

4. **配置环境变量**
   ```bash
   cp .env.example .env
   # 编辑 .env 文件，设置数据库连接等
   ```

5. **启动服务**
   ```bash
   python main.py
   ```

### iOS开发环境

1. **打开Xcode项目**
   ```bash
   open ios/ArxivReader.xcodeproj
   ```

2. **配置证书**
   - 在Xcode中配置Apple Developer账号
   - 配置推送通知证书

3. **运行应用**
   - 选择模拟器或连接真机
   - 点击 Run (⌘R)

## 📋 功能清单

### 核心功能
- [ ] 用户注册/登录
- [ ] 兴趣标签设置
- [ ] arXiv论文爬取
- [ ] 个性化推荐
- [ ] 推送通知
- [ ] 论文详情查看

### 高级功能
- [ ] 团队协作
- [ ] 阅读任务
- [ ] 离线阅读
- [ ] PDF下载
- [ ] 阅读统计

### 管理功能
- [ ] 用户管理
- [ ] 内容审核
- [ ] 数据分析
- [ ] 系统监控

## 🔧 开发指南

### 代码规范
- **Python**: 遵循PEP 8规范
- **Swift**: 遵循Swift API设计指南
- **Git**: 使用语义化提交信息

### 分支策略
- `main`: 生产环境代码
- `develop`: 开发分支
- `feature/*`: 功能分支
- `bugfix/*`: 修复分支
- `release/*`: 发布分支

### 提交信息格式
```
类型(范围): 描述

详细说明（可选）

关闭 #issue号
```

类型包括：
- `feat`: 新功能
- `fix`: 修复bug
- `docs`: 文档更新
- `style`: 代码格式
- `refactor`: 重构
- `test`: 测试
- `chore`: 构建/工具

## 🧪 测试

### 后端测试
```bash
# 运行所有测试
pytest

# 运行特定测试
pytest tests/test_auth.py

# 生成测试报告
pytest --cov=backend --cov-report=html
```

### iOS测试
- 在Xcode中运行单元测试 (⌘U)
- 运行UI测试

## 📦 部署

### 后端部署
1. **构建Docker镜像**
   ```bash
   docker build -t arxiv-backend:latest .
   ```

2. **运行容器**
   ```bash
   docker-compose up -d
   ```

3. **配置Nginx**
   ```nginx
   server {
       listen 80;
       server_name api.arxiv-reader.app;
       
       location / {
           proxy_pass http://localhost:8000;
       }
   }
   ```

### iOS发布
1. **构建归档**
   - Xcode → Product → Archive

2. **上传到App Store Connect**
   - 使用Xcode Organizer
   - 或使用Transporter

3. **提交审核**
   - 在App Store Connect中提交审核

## 📊 监控和维护

### 监控指标
- API响应时间
- 错误率
- 用户活跃度
- 推送送达率

### 日志管理
- 应用日志
- 访问日志
- 错误日志
- 性能日志

## 🤝 贡献指南

1. Fork项目
2. 创建功能分支 (`git checkout -b feature/amazing-feature`)
3. 提交更改 (`git commit -m 'feat: add amazing feature'`)
4. 推送到分支 (`git push origin feature/amazing-feature`)
5. 创建Pull Request

## 📄 许可证

本项目采用 MIT 许可证 - 查看 [LICENSE](LICENSE) 文件了解详情。

## 📞 支持

- 问题: [GitHub Issues](https://github.com/yourusername/arxiv-paper-assistant/issues)
- 讨论: [GitHub Discussions](https://github.com/yourusername/arxiv-paper-assistant/discussions)
- 邮件: support@arxiv-reader.app

## 🙏 致谢

- arXiv.org 提供论文数据
- FastAPI 团队提供优秀的Web框架
- SwiftUI 团队提供现代化的UI框架

---

**开始开发**: 2026-03-09  
**目标上架**: 2026-06-09  
**状态**: 开发中 🚧