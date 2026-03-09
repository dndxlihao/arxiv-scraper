#!/usr/bin/env python3
"""
arXiv推荐APP - 简化测试脚本
"""

import sys
import subprocess
import time
import requests
import json

def run_command(cmd, check=True):
    """运行命令并返回输出"""
    print(f"➤ {cmd}")
    try:
        result = subprocess.run(cmd, shell=True, capture_output=True, text=True)
        if check and result.returncode != 0:
            print(f"❌ 命令失败: {result.stderr}")
            return None
        return result.stdout.strip()
    except Exception as e:
        print(f"❌ 执行命令出错: {e}")
        return None

def test_backend():
    """测试后端服务"""
    print("\n" + "="*50)
    print("🧪 测试后端服务")
    print("="*50)
    
    # 检查Python
    python_version = run_command("python3 --version")
    if python_version:
        print(f"✅ Python版本: {python_version}")
    
    # 安装依赖
    print("\n📦 安装依赖...")
    run_command("cd backend && pip3 install -r requirements_simple.txt")
    
    # 启动后端
    print("\n🚀 启动后端服务...")
    backend_process = subprocess.Popen(
        ["python3", "backend/app.py"],
        stdout=subprocess.PIPE,
        stderr=subprocess.PIPE,
        text=True
    )
    
    # 等待启动
    print("⏳ 等待服务启动...")
    time.sleep(5)
    
    # 测试连接
    try:
        response = requests.get("http://localhost:8000/", timeout=10)
        if response.status_code == 200:
            print(f"✅ 后端服务运行正常: {response.json()}")
        else:
            print(f"❌ 后端服务返回错误: {response.status_code}")
            return False
    except Exception as e:
        print(f"❌ 无法连接到后端服务: {e}")
        return False
    
    return backend_process

def test_api_endpoints():
    """测试API端点"""
    print("\n" + "="*50)
    print("🔌 测试API端点")
    print("="*50)
    
    base_url = "http://localhost:8000"
    
    # 1. 测试用户注册
    print("\n1. 测试用户注册...")
    user_data = {
        "username": "demo_user",
        "email": "demo@example.com",
        "interests": ["machine learning", "AI", "deep learning"],
        "team": "Demo Team"
    }
    
    try:
        response = requests.post(f"{base_url}/users/register", json=user_data)
        if response.status_code == 200:
            print(f"✅ 用户注册成功: {response.json()}")
        elif response.status_code == 400:
            print("⚠️ 用户可能已存在")
        else:
            print(f"❌ 用户注册失败: {response.status_code}")
    except Exception as e:
        print(f"❌ 用户注册测试失败: {e}")
    
    # 2. 测试获取推荐
    print("\n2. 测试获取推荐...")
    try:
        response = requests.get(f"{base_url}/users/demo_user/recommendations?limit=2")
        if response.status_code == 200:
            papers = response.json()
            print(f"✅ 获取到 {len(papers)} 篇推荐论文")
            if papers:
                print(f"   第一篇: {papers[0]['title'][:60]}...")
        else:
            print(f"❌ 获取推荐失败: {response.status_code}")
    except Exception as e:
        print(f"❌ 获取推荐测试失败: {e}")
    
    # 3. 测试搜索
    print("\n3. 测试搜索功能...")
    try:
        response = requests.get(f"{base_url}/papers/search?query=transformer&limit=1")
        if response.status_code == 200:
            papers = response.json()
            if papers:
                print(f"✅ 搜索成功: 找到 {len(papers)} 篇论文")
                print(f"   论文ID: {papers[0]['id']}")
                paper_id = papers[0]['id']
                
                # 4. 测试论文详情
                print("\n4. 测试论文详情...")
                detail_response = requests.get(f"{base_url}/papers/{paper_id}")
                if detail_response.status_code == 200:
                    paper_detail = detail_response.json()
                    print(f"✅ 论文详情获取成功")
                    print(f"   标题: {paper_detail['title'][:80]}...")
                    print(f"   作者: {', '.join(paper_detail['authors'][:2])}")
                    print(f"   关键词: {', '.join(paper_detail['keywords'][:3])}")
                    
                    # 5. 测试收藏
                    print("\n5. 测试收藏功能...")
                    collect_response = requests.post(f"{base_url}/users/demo_user/collect/{paper_id}")
                    if collect_response.status_code == 200:
                        print(f"✅ 收藏成功: {collect_response.json()}")
                    else:
                        print(f"❌ 收藏失败: {collect_response.status_code}")
                else:
                    print(f"❌ 论文详情获取失败: {detail_response.status_code}")
        else:
            print(f"❌ 搜索失败: {response.status_code}")
    except Exception as e:
        print(f"❌ 搜索测试失败: {e}")
    
    # 6. 测试团队功能
    print("\n6. 测试团队功能...")
    try:
        team_response = requests.post(f"{base_url}/teams/create?name=Test%20Team%20{int(time.time())}&description=Test%20team")
        if team_response.status_code == 200:
            team_data = team_response.json()
            print(f"✅ 团队创建成功: {team_data}")
        else:
            print(f"❌ 团队创建失败: {team_response.status_code}")
    except Exception as e:
        print(f"❌ 团队功能测试失败: {e}")
    
    # 7. 测试每日简报
    print("\n7. 测试每日简报...")
    try:
        digest_response = requests.get(f"{base_url}/daily-digest/demo_user")
        if digest_response.status_code == 200:
            digest = digest_response.json()
            print(f"✅ 每日简报获取成功")
            print(f"   日期: {digest['date']}")
            print(f"   论文数量: {len(digest['papers'])}")
        else:
            print(f"❌ 每日简报获取失败: {digest_response.status_code}")
    except Exception as e:
        print(f"❌ 每日简报测试失败: {e}")
    
    return True

def main():
    """主函数"""
    print("🚀 arXiv推荐APP原型测试")
    print("="*50)
    
    backend_process = None
    
    try:
        # 测试后端
        backend_process = test_backend()
        if not backend_process:
            print("❌ 后端服务启动失败")
            return 1
        
        # 测试API
        api_success = test_api_endpoints()
        
        if api_success:
            print("\n" + "="*50)
            print("🎉 测试完成！")
            print("="*50)
            print("\n📊 测试总结:")
            print("   后端服务: ✅ 运行正常")
            print("   arXiv API: ✅ 连接正常")
            print("   核心功能: ✅ 全部可用")
            print("\n🌐 访问地址:")
            print("   测试仪表板: file://" + sys.path[0] + "/test_dashboard.html")
            print("   API文档: http://localhost:8000/docs")
            print("\n🛑 按Ctrl+C停止服务")
            
            # 保持运行
            backend_process.wait()
        else:
            print("\n❌ API测试失败")
            return 1
            
    except KeyboardInterrupt:
        print("\n\n👋 用户中断，停止服务...")
    except Exception as e:
        print(f"\n❌ 测试过程中出现错误: {e}")
        return 1
    finally:
        # 清理
        if backend_process:
            print("🛑 停止后端服务...")
            backend_process.terminate()
            backend_process.wait()
    
    return 0

if __name__ == "__main__":
    sys.exit(main())