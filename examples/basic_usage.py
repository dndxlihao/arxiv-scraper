#!/usr/bin/env python3
"""
arXiv Scraper 基本使用示例
"""

import subprocess
import json
import os

def run_scraper_example():
    """运行爬取器示例"""
    
    print("=== arXiv Scraper 使用示例 ===\n")
    
    # 示例1：基本搜索
    print("1. 基本搜索（机器学习）")
    cmd1 = ["python", "src/arxiv_scraper.py", "--query", "machine learning", "--max-results", "3"]
    subprocess.run(cmd1)
    
    print("\n" + "="*50 + "\n")
    
    # 示例2：指定分类搜索
    print("2. 指定分类搜索（计算机视觉）")
    cmd2 = ["python", "src/arxiv_scraper.py", "--query", "object detection", "--category", "cs.CV", "--max-results", "2"]
    subprocess.run(cmd2)
    
    print("\n" + "="*50 + "\n")
    
    # 示例3：输出为文本格式
    print("3. 输出为文本格式（自然语言处理）")
    cmd3 = ["python", "src/arxiv_scraper.py", "--query", "natural language processing", "--output", "txt", "--max-results", "2", "--filename", "examples/nlp_papers.txt"]
    subprocess.run(cmd3)
    
    print("\n" + "="*50 + "\n")
    
    # 示例4：日期范围搜索
    print("4. 日期范围搜索（2026年3月发布的论文）")
    cmd4 = ["python", "src/arxiv_scraper.py", "--query", "transformer", "--start-date", "2026-03-01", "--max-results", "2"]
    subprocess.run(cmd4)

def analyze_json_output():
    """分析JSON输出文件"""
    print("\n" + "="*50 + "\n")
    print("分析JSON输出文件内容：")
    
    # 查找最新的JSON文件
    json_files = [f for f in os.listdir(".") if f.endswith(".json") and f.startswith("arxiv_papers_")]
    if json_files:
        latest_file = sorted(json_files)[-1]
        print(f"找到最新文件: {latest_file}")
        
        with open(latest_file, 'r', encoding='utf-8') as f:
            data = json.load(f)
            
        print(f"包含 {len(data)} 篇论文")
        if data:
            print("\n第一篇论文信息：")
            paper = data[0]
            print(f"标题: {paper.get('title', 'N/A')}")
            print(f"作者: {', '.join(paper.get('authors', []))}")
            print(f"arXiv ID: {paper.get('arxiv_id', 'N/A')}")
            print(f"分类: {', '.join(paper.get('categories', []))}")
            print(f"摘要预览: {paper.get('summary', 'N/A')[:200]}...")

if __name__ == "__main__":
    # 创建examples目录
    os.makedirs("examples", exist_ok=True)
    
    run_scraper_example()
    analyze_json_output()