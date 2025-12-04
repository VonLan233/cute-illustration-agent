#!/bin/bash

# 可爱插图生成智能体 - 启动脚本

# 检查 Python 环境
if ! command -v python3 &> /dev/null; then
    echo "错误: 未找到 Python3，请先安装 Python 3.9+"
    exit 1
fi

# 进入后端目录
cd "$(dirname "$0")"

# 检查虚拟环境
if [ ! -d "venv" ]; then
    echo "创建虚拟环境..."
    python3 -m venv venv
fi

# 激活虚拟环境
source venv/bin/activate

# 安装依赖
echo "检查依赖..."
pip install -r requirements.txt -q

# 检查 .env 文件
if [ ! -f ".env" ]; then
    echo "警告: 未找到 .env 文件，请复制 .env.example 并配置 API 密钥"
    echo "  cp .env.example .env"
    echo "  然后编辑 .env 填入您的 API 密钥"
    exit 1
fi

# 启动服务
echo "启动服务..."
echo "API 文档: http://localhost:8000/docs"
echo "健康检查: http://localhost:8000/health"
echo ""

uvicorn main:app --host 0.0.0.0 --port 8000 --reload
