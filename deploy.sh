#!/bin/bash

# 可爱插图生成智能体 - 服务器部署脚本
# 使用方式: ./deploy.sh

set -e

echo "=== 可爱插图生成智能体 部署脚本 ==="

# 检查环境变量
if [ -z "$DEEPSEEK_API_KEY" ] || [ -z "$DOUBAO_API_KEY" ]; then
    echo "请先设置环境变量:"
    echo "  export DEEPSEEK_API_KEY=your_key"
    echo "  export DOUBAO_API_KEY=your_key"
    exit 1
fi

# 检查 Docker
if ! command -v docker &> /dev/null; then
    echo "请先安装 Docker"
    exit 1
fi

# 构建后端镜像
echo ">>> 构建后端镜像..."
docker build -t cute-illustration-backend ./backend

# 构建前端镜像
echo ">>> 构建前端镜像..."
docker build -t cute-illustration-frontend ./frontend

# 创建网络
docker network create cute-illustration-net 2>/dev/null || true

# 停止旧容器
echo ">>> 停止旧容器..."
docker stop cute-backend cute-frontend 2>/dev/null || true
docker rm cute-backend cute-frontend 2>/dev/null || true

# 启动后端
echo ">>> 启动后端..."
docker run -d \
    --name cute-backend \
    --network cute-illustration-net \
    -e DEEPSEEK_API_KEY=$DEEPSEEK_API_KEY \
    -e DOUBAO_API_KEY=$DOUBAO_API_KEY \
    -p 8000:8000 \
    --restart unless-stopped \
    cute-illustration-backend

# 启动前端
echo ">>> 启动前端..."
docker run -d \
    --name cute-frontend \
    --network cute-illustration-net \
    -p 80:80 \
    --restart unless-stopped \
    cute-illustration-frontend

echo ""
echo "=== 部署完成 ==="
echo "前端: http://服务器IP"
echo "后端API: http://服务器IP:8000/docs"
