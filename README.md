# arXiv Research Assistant

一个现代化的 arXiv 论文搜索与管理系统，包含 Web 前端、移动应用原型和强大的论文爬取功能。

## 🚀 项目概览

arXiv Research Assistant 是一个完整的学术论文管理解决方案，帮助研究人员高效地发现、跟踪和管理 arXiv 上的最新研究成果。

### ✨ 核心功能

- **🔍 智能论文搜索** - 支持关键词、日期范围、分类筛选
- **📱 多平台访问** - Web 界面 + 移动应用原型
- **📊 数据导出** - JSON、TXT、CSV 多种格式
- **🎯 个性化推荐** - 基于兴趣的论文推荐
- **📈 趋势分析** - 热门领域和作者分析

## 📁 项目结构

```
arxiv-research-assistant/
├── src/                    # arXiv 爬虫核心代码
│   └── arxiv_scraper.py
├── arxiv_app_prototype/    # Web 应用原型
│   ├── backend/           # Flask 后端 API
│   │   └── app.py
│   ├── frontend/          # React Native 前端
│   │   ├── App.js
│   │   ├── babel.config.js
│   │   └── metro.config.js
│   ├── simple_frontend.html  # 简易 Web 界面
│   └── test_dashboard.html   # 测试仪表板
├── docs/                  # 项目文档
├── examples/              # 使用示例
├── data/                  # 示例数据
├── tests/                 # 测试文件
└── arxiv_mobile_app/      # 移动应用项目（独立仓库）
```

## 🛠️ 快速开始

### 1. 环境准备

```bash
# 克隆项目
git clone https://github.com/yourusername/arxiv-research-assistant.git
cd arxiv-research-assistant

# 安装依赖
pip install -r requirements.txt
```

### 2. 基础爬虫使用

```bash
# 搜索机器学习相关论文
python src/arxiv_scraper.py --query "machine learning"

# 指定结果数量和日期范围
python src/arxiv_scraper.py --query "deep learning" --max-results 20 --start-date 2026-01-01

# 导出为 CSV 格式
python src/arxiv_scraper.py --query "computer vision" --category cs.CV --output csv
```

### 3. 启动 Web 应用

```bash
# 启动后端 API 服务器
cd arxiv_app_prototype/backend
python app.py

# 访问 Web 界面
# 打开浏览器访问: http://localhost:5000
```

## 🌐 Web 应用功能

### 后端 API (Flask)
- **论文搜索** - `/api/search?q=<query>`
- **分类浏览** - `/api/category/<category>`
- **热门论文** - `/api/trending`
- **作者分析** - `/api/author/<author_name>`

### 前端界面
- **响应式设计** - 适配桌面和移动设备
- **实时搜索** - 输入时即时显示结果
- **论文收藏** - 保存感兴趣的论文
- **导出功能** - 一键导出搜索结果

## 📱 移动应用原型

项目包含一个 React Native 移动应用原型，位于 `arxiv_mobile_app/` 目录中（独立 Git 仓库）。

### 移动应用功能
- **原生体验** - iOS/Android 原生应用
- **离线阅读** - 缓存论文供离线查看
- **推送通知** - 新论文提醒
- **个性化推荐** - 基于阅读历史的智能推荐

## 📊 数据格式

### JSON 输出示例
```json
{
  "title": "Attention Is All You Need",
  "authors": ["Ashish Vaswani", "Noam Shazeer", "Niki Parmar"],
  "abstract": "The dominant sequence transduction models...",
  "categories": ["cs.CL", "cs.LG"],
  "published": "2017-06-12",
  "updated": "2023-12-01",
  "pdf_url": "https://arxiv.org/pdf/1706.03762.pdf",
  "arxiv_url": "https://arxiv.org/abs/1706.03762"
}
```

## 🔧 高级配置

### 自定义搜索参数
```python
from src.arxiv_scraper import ArxivScraper

scraper = ArxivScraper(
    max_results=50,
    delay=2.0,  # 请求延迟（避免频率限制）
    timeout=30  # 请求超时
)

results = scraper.search(
    query="quantum computing",
    start_date="2026-01-01",
    category="quant-ph"
)
```

### 数据库集成
项目支持 SQLite 数据库存储，自动记录搜索历史和个人收藏。

## 📈 性能优化

- **智能缓存** - 减少重复 arXiv API 调用
- **批量处理** - 高效处理大量论文数据
- **并发搜索** - 支持多关键词并行搜索
- **增量更新** - 只获取最新论文，减少数据量

## 🤝 贡献指南

欢迎贡献代码、报告问题或提出改进建议！

1. Fork 本仓库
2. 创建功能分支 (`git checkout -b feature/amazing-feature`)
3. 提交更改 (`git commit -m 'Add amazing feature'`)
4. 推送到分支 (`git push origin feature/amazing-feature`)
5. 开启 Pull Request

## 📄 许可证

本项目采用 MIT 许可证 - 查看 [LICENSE](LICENSE) 文件了解详情。

## 🙏 致谢

- arXiv API 提供论文数据
- Flask 和 React Native 社区
- 所有贡献者和用户

---

**🎯 愿景**: 让学术研究更高效、更智能、更易访问！

**📞 支持**: 如有问题，请提交 Issue 或通过邮件联系。