#!/bin/bash

# arXiv推荐APP - 快速启动脚本

echo "🚀 arXiv推荐APP原型 - 快速启动"
echo "========================================"

# 颜色定义
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
BLUE='\033[0;34m'
NC='\033[0m' # No Color

# 检查Python
echo -e "${BLUE}🔍 检查环境...${NC}"
if ! command -v python3 &> /dev/null; then
    echo -e "${RED}❌ Python3未安装${NC}"
    exit 1
fi

echo -e "${GREEN}✅ Python3可用${NC}"

# 进入后端目录
cd backend

# 安装依赖
echo -e "${BLUE}📦 安装依赖...${NC}"
pip3 install -r requirements_simple.txt > /dev/null 2>&1
if [ $? -eq 0 ]; then
    echo -e "${GREEN}✅ 依赖安装成功${NC}"
else
    echo -e "${YELLOW}⚠️ 依赖安装可能有问题，继续尝试...${NC}"
fi

# 启动后端服务
echo -e "${BLUE}🚀 启动后端服务...${NC}"
python3 app.py &
BACKEND_PID=$!

# 等待启动
echo -e "${BLUE}⏳ 等待服务启动...${NC}"
sleep 8

# 检查服务状态
if curl -s http://localhost:8000/ > /dev/null; then
    echo -e "${GREEN}✅ 后端服务启动成功${NC}"
else
    echo -e "${RED}❌ 后端服务启动失败${NC}"
    kill $BACKEND_PID 2>/dev/null
    exit 1
fi

# 返回项目根目录
cd ..

echo ""
echo -e "${GREEN}🎉 arXiv推荐APP原型启动成功！${NC}"
echo "========================================"
echo ""
echo -e "${YELLOW}📱 访问方式：${NC}"
echo "1. 🌐 测试仪表板:"
echo "   file://$(pwd)/test_dashboard.html"
echo ""
echo "2. 📚 API文档:"
echo "   http://localhost:8000/docs"
echo ""
echo "3. 🔧 后端API:"
echo "   http://localhost:8000/"
echo ""
echo -e "${YELLOW}👤 测试用户：${NC}"
echo "   用户名: demo_user"
echo "   用户名: testuser"
echo "   邮箱: demo@example.com"
echo "   兴趣: machine learning, AI, deep learning"
echo ""
echo -e "${YELLOW}🔍 快速测试命令：${NC}"
echo "   # 获取推荐"
echo "   curl http://localhost:8000/users/demo_user/recommendations"
echo ""
echo "   # 搜索论文"
echo "   curl 'http://localhost:8000/papers/search?query=transformer&limit=2'"
echo ""
echo "   # 注册新用户"
echo "   curl -X POST http://localhost:8000/users/register \\"
echo "     -H 'Content-Type: application/json' \\"
echo "     -d '{\"username\":\"new_user\",\"email\":\"new@example.com\",\"interests\":[\"offline RL\",\"power system\"]}'"
echo ""
echo "========================================"
echo -e "${RED}🛑 按 Ctrl+C 停止服务${NC}"
echo ""

# 保持运行
wait $BACKEND_PID