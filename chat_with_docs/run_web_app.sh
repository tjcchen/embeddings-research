#!/bin/bash

# Chat with Documents - Web App Launcher
echo "🚀 启动文档问答系统 Web 应用"
echo "================================"

# Check if virtual environment exists
if [ -d "venv" ]; then
    echo "📦 激活虚拟环境..."
    source venv/bin/activate
fi

# Check if requirements are installed
echo "🔍 检查依赖包..."
python -c "import streamlit, langchain, openai" 2>/dev/null
if [ $? -ne 0 ]; then
    echo "❌ 缺少依赖包，正在安装..."
    pip install -r requirements.txt
fi

# Check for API key
if [ -z "$OPENAI_API_KEY" ] && [ ! -f ".env" ]; then
    echo "⚠️  未找到 OpenAI API Key"
    echo "请创建 .env 文件并添加: OPENAI_API_KEY=your_api_key_here"
    echo "或者设置环境变量: export OPENAI_API_KEY=your_api_key_here"
    exit 1
fi

echo "✅ 准备就绪，启动 Streamlit 应用..."
echo "🌐 应用将在浏览器中打开: http://localhost:8501"
echo ""

# Launch Streamlit app
streamlit run main.py
