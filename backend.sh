#!/usr/bin/env bash
set -e

cd "$(dirname "$0")/back-end"

echo "==> 安装后端依赖..."
uv sync

echo "==> 运行数据库迁移..."
uv run python manage.py migrate

echo "==> 启动 Django 开发服务器..."
uv run python manage.py runserver "0.0.0.0:${DJANGO_PORT:-8000}"
