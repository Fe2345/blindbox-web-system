#!/usr/bin/env bash

set -euo pipefail

SCRIPT_DIR="$(cd "$(dirname "$0")" && pwd)"
PROJECT_DIR="$(cd "$SCRIPT_DIR/.." && pwd)"
cd "$PROJECT_DIR"

# --- 加载 .env ---
if [ -f .env ]; then
    set -a
    source .env
    set +a
fi

DJANGO_PORT="${DJANGO_PORT:-8001}"
VENV_TYPE="${VENV_TYPE:-uv}"

echo "========================================"
echo "  后端启动"
echo "========================================"
echo "  数据库: ${DB_HOST:-127.0.0.1}:${DB_PORT:-3306}/${DB_NAME:-gugou}"
echo "  Redis:  ${REDIS_HOST:-127.0.0.1}:${REDIS_PORT:-6379} (USE_REDIS=${USE_REDIS:-false})"
echo "  Django: http://127.0.0.1:${DJANGO_PORT}"
echo "  VENV:   ${VENV_TYPE}"
echo "========================================"

cd back-end

# --------------------------------------------------
# 虚拟环境初始化
# --------------------------------------------------

case "$VENV_TYPE" in
    uv)
        echo ">> 使用 uv 环境"

        if [ ! -d ".venv" ]; then
            echo ">> 创建 uv 虚拟环境..."
            uv sync
        fi

        RUN_CMD="uv run"
        ;;

    conda)
        echo ">> 使用 conda 环境"

        CONDA_VENV_NAME="${CONDA_VENV_NAME:?CONDA_VENV_NAME 未配置}"

        if ! command -v conda >/dev/null 2>&1; then
            echo "错误: 未找到 conda"
            exit 1
        fi

        eval "$(conda shell.bash hook)"

        echo ">> 激活 Conda 环境: ${CONDA_VENV_NAME}"
        conda activate "${CONDA_VENV_NAME}"

        RUN_CMD=""
        ;;

    *)
        echo "错误: 不支持的 VENV_TYPE=${VENV_TYPE}"
        echo "允许值: uv, conda"
        exit 1
        ;;
esac

# --------------------------------------------------
# 数据库迁移
# --------------------------------------------------

echo ">> 执行数据库迁移..."

if [ "$VENV_TYPE" = "uv" ]; then
    uv run python manage.py migrate --noinput
else
    python manage.py migrate --noinput
fi

echo ""
echo ">> 启动 Django 开发服务器 (0.0.0.0:${DJANGO_PORT})..."

if [ "$VENV_TYPE" = "uv" ]; then
    exec uv run python manage.py runserver "0.0.0.0:${DJANGO_PORT}"
else
    exec python manage.py runserver "0.0.0.0:${DJANGO_PORT}"
fi