# arXiv Paper Scraper

一个简单高效的arXiv论文爬取工具，支持关键词搜索、日期筛选、分类过滤和多种输出格式。

## 功能特性

- 🔍 **智能搜索**：支持关键词、日期范围、分类筛选
- 📊 **多种格式**：JSON、TXT、CSV三种输出格式
- ⚡ **高效稳定**：内置延迟机制避免频率限制
- 📝 **完整信息**：提取标题、作者、摘要、分类、链接等完整信息
- 🐍 **易于使用**：命令行界面，简单直观

## 安装

```bash
# 克隆仓库
git clone https://github.com/yourusername/arxiv-scraper.git
cd arxiv-scraper

# 安装依赖
pip install -r requirements.txt
```

## 快速开始

```bash
# 基本搜索
python src/arxiv_scraper.py --query "machine learning"

# 指定结果数量
python src/arxiv_scraper.py --query "deep learning" --max-results 10

# 指定日期范围
python src/arxiv_scraper.py --query "transformer" --start-date 2026-01-01

# 指定分类
python src/arxiv_scraper.py --query "computer vision" --category cs.CV

# 指定输出格式
python src/arxiv_scraper.py --query "nlp" --output txt
```

## 详细用法

### 命令行参数

| 参数 | 简写 | 说明 | 默认值 |
|------|------|------|--------|
| `--query` | `-q` | 搜索关键词（必需） | - |
| `--max-results` | `-m` | 最大结果数量 | 10 |
| `--start-date` | `-s` | 开始日期（YYYY-MM-DD） | - |
| `--end-date` | `-e` | 结束日期（YYYY-MM-DD） | 今天 |
| `--category` | `-c` | arXiv分类（如cs.AI, cs.LG） | - |
| `--output` | `-o` | 输出格式（json/txt/csv） | json |
| `--filename` | `-f` | 输出文件名 | 自动生成 |
| `--delay` | `-d` | 请求延迟（秒） | 3.0 |

### 输出格式

1. **JSON格式**：完整的结构化数据，适合程序处理
2. **TXT格式**：易读的文本格式，适合快速浏览
3. **CSV格式**：表格格式，适合导入Excel或数据分析工具

## 项目结构

```
arxiv-scraper/
├── src/
│   └── arxiv_scraper.py    # 主程序
├── docs/                   # 文档
├── tests/                  # 测试文件
├── examples/               # 使用示例
├── data/                   # 示例数据
├── requirements.txt        # 依赖列表
└── README.md              # 项目说明
```

## 示例

查看 `examples/` 目录中的使用示例。

## 贡献

欢迎提交Issue和Pull Request！

## 许可证

MIT License