#!/bin/bash

# arXiv推荐APP原型测试启动脚本

echo "🚀 启动arXiv推荐APP原型测试..."
echo "========================================"

# 检查Python环境
echo "🔍 检查Python环境..."
python3 --version
if [ $? -ne 0 ]; then
    echo "❌ Python3未安装"
    exit 1
fi

# 检查后端依赖
echo "🔍 检查后端依赖..."
cd backend
if [ ! -f "requirements.txt" ]; then
    echo "❌ requirements.txt不存在"
    exit 1
fi

echo "📦 安装Python依赖..."
pip3 install -r requirements.txt > /dev/null 2>&1
if [ $? -ne 0 ]; then
    echo "❌ 依赖安装失败"
    exit 1
fi

# 启动后端服务
echo "🚀 启动后端服务..."
python3 app.py &
BACKEND_PID=$!
echo "✅ 后端服务启动成功 (PID: $BACKEND_PID)"

# 等待后端启动
echo "⏳ 等待后端服务就绪..."
sleep 5

# 测试后端连接
echo "🔌 测试后端连接..."
curl -s http://localhost:8000/ > /dev/null
if [ $? -eq 0 ]; then
    echo "✅ 后端服务连接成功"
else
    echo "❌ 后端服务连接失败"
    kill $BACKEND_PID 2>/dev/null
    exit 1
fi

# 运行API测试
echo "🧪 运行API测试..."
cd ..
node test_api.js 2>/dev/null
if [ $? -eq 0 ]; then
    echo "✅ API测试通过"
else
    echo "⚠️ API测试部分失败，但服务仍在运行"
fi

# 显示测试仪表板
echo "📊 打开测试仪表板..."
echo "========================================"
echo "🌐 测试仪表板: file://$(pwd)/test_dashboard.html"
echo "📚 API文档: http://localhost:8000/docs"
echo "🔧 后端服务: http://localhost:8000/"
echo ""
echo "📱 可用测试用户:"
echo "   用户名: testuser"
echo "   用户名: testuser2"
echo "   用户名: dashboard_test_user"
echo ""
echo "🛑 停止服务: kill $BACKEND_PID"
echo "========================================"

# 保持脚本运行
echo "🏃 服务运行中...按Ctrl+C停止"
wait $BACKEND_PID