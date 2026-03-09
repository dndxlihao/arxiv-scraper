# PaperFlow

智能论文管理应用，让研究更流畅。即将发布到 Apple Store 的现代化学术论文管理工具。

## 🚀 项目概览

PaperFlow 是一个专为研究人员设计的智能论文管理应用，帮助您高效地发现、跟踪、阅读和管理学术论文，让研究流程更加顺畅。

### ✨ 核心功能

- **🔍 智能论文搜索** - 支持关键词、日期范围、分类筛选
- **📱 iOS 原生应用** - 专为 iPhone 和 iPad 优化
- **📚 论文收藏管理** - 创建个人图书馆和阅读列表
- **🎯 个性化推荐** - 基于研究兴趣的智能推荐
- **📈 阅读进度跟踪** - 记录阅读历史和笔记

## 📁 项目结构

```
PaperFlow/
├── src/                    # 核心论文爬虫代码
│   └── arxiv_scraper.py
├── paperflow_app/          # iOS 应用项目
│   ├── PaperFlow.xcodeproj # Xcode 项目文件
│   ├── Assets.xcassets/    # 应用图标和资源
│   └── Sources/            # Swift 源代码
├── backend/               # 后端 API 服务
│   └── app.py
├── docs/                  # 项目文档
├── examples/              # 使用示例
├── data/                  # 示例数据
└── tests/                 # 测试文件
```

## 🛠️ 快速开始

### 1. 环境准备

```bash
# 克隆项目
git clone https://github.com/dndxlihao/PaperFlow.git
cd PaperFlow

# 安装 Python 依赖
pip install -r requirements.txt
```

### 2. 基础爬虫使用

```bash
# 搜索机器学习相关论文
python src/arxiv_scraper.py --query "machine learning"

# 指定结果数量和日期范围
python src/arxiv_scraper.py --query "deep learning" --max-results 20 --from-date 2026-01-01

# 导出为 TXT 格式
python src/arxiv_scraper.py --query "computer vision" --category cs.CV --output-format txt
```

### 3. 开发 iOS 应用

```bash
# 打开 Xcode 项目
open paperflow_app/PaperFlow.xcodeproj
```

## 📱 iOS 应用功能

### 核心功能
- **原生 iOS 体验** - 专为 iPhone 和 iPad 优化
- **离线阅读** - 下载论文供离线查看
- **智能搜索** - 支持自然语言搜索和高级筛选
- **阅读列表** - 创建和管理个人阅读计划

### 用户界面
- **现代设计** - 遵循 iOS 设计规范
- **暗色模式** - 支持系统级暗色模式
- **手势操作** - 流畅的滑动手势支持
- **分享集成** - 与 iOS 分享菜单深度集成

## 🎯 应用特色

### 智能功能
- **个性化推荐** - 基于阅读历史和兴趣的智能推荐
- **阅读统计** - 可视化阅读进度和习惯分析
- **引用管理** - 自动生成引用格式
- **协作功能** - 与同事分享论文和笔记

### 发布计划
- **App Store 发布** - 计划于 2026 年第二季度上线
- **免费增值模式** - 基础功能免费，高级功能订阅
- **学术合作** - 与高校和研究机构合作推广

## 📊 技术架构

### 后端服务
- **Python Flask API** - 提供论文搜索和数据服务
- **SQLite 数据库** - 存储用户数据和收藏
- **Redis 缓存** - 提高搜索响应速度
- **任务队列** - 异步处理论文更新

### iOS 客户端
- **SwiftUI** - 现代声明式 UI 框架
- **Core Data** - 本地数据持久化
- **Combine** - 响应式编程框架
- **Swift Concurrency** - 异步任务处理

## 🔧 开发指南

### iOS 开发环境
```bash
# 系统要求
- macOS 13.0 或更高版本
- Xcode 15.0 或更高版本
- iOS 16.0 作为部署目标

# 安装依赖
cd paperflow_app
pod install  # 如果使用 CocoaPods
```

### 代码规范
- 遵循 Swift API 设计指南
- 使用 SwiftLint 进行代码检查
- 编写单元测试和 UI 测试
- 文档注释使用 DocC 格式

## 📈 性能优化

- **图片懒加载** - 优化列表滚动性能
- **数据预取** - 提前加载下一页数据
- **内存管理** - 智能缓存和资源释放
- **网络优化** - 请求合并和压缩传输

## 🤝 贡献指南

欢迎为 PaperFlow 贡献代码、设计或文档！

1. Fork 本仓库
2. 创建功能分支 (`git checkout -b feature/amazing-feature`)
3. 提交更改 (`git commit -m 'Add amazing feature'`)
4. 推送到分支 (`git push origin feature/amazing-feature`)
5. 开启 Pull Request

## 📄 许可证

本项目采用 MIT 许可证 - 查看 [LICENSE](LICENSE) 文件了解详情。

## 🙏 致谢

- arXiv API 提供论文数据
- Apple Developer 社区
- 所有测试用户和贡献者

---

**🎯 愿景**: 让学术研究更流畅、更智能、更愉悦！

**📱 App Store**: 即将上线，敬请期待！

**📞 支持**: 如有问题，请提交 Issue 或通过邮件联系。