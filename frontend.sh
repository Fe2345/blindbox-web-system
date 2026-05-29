#!/usr/bin/env bash
set -e

cd "$(dirname "$0")/front-end"

echo "==> 安装前端依赖..."
npm install

echo "==> 启动 Vite 开发服务器..."
npm run dev
