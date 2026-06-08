#!/usr/bin/env bash
# 日期: 2026-06-08
# 用途: 根据 FRONTEND_ENV_TYPE 和 PACKAGE_MANAGER 启动前端 Vite 开发服务器

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

VITE_PORT="${VITE_PORT:-3000}"
BACKEND_URL="${VITE_BACKEND_URL:-http://127.0.0.1:8001}"
FRONTEND_ENV_TYPE="${FRONTEND_ENV_TYPE:-system}"
PACKAGE_MANAGER="${PACKAGE_MANAGER:-npm}"

require_command() {
  local command_name="$1"

  if ! command -v "$command_name" >/dev/null 2>&1; then
    echo "错误: 未找到命令: $command_name"
    exit 1
  fi
}

activate_conda_env() {
  require_command conda

  if [ -z "${CONDA_VENV_NAME:-}" ]; then
    echo "错误: FRONTEND_ENV_TYPE=conda 时必须配置 CONDA_VENV_NAME"
    exit 1
  fi

  eval "$(conda shell.bash hook)"

  echo ">> 激活 Conda 环境: ${CONDA_VENV_NAME}"
  conda activate "${CONDA_VENV_NAME}"
}

echo "========================================"
echo "  前端启动"
echo "========================================"
echo "  Vite:    http://127.0.0.1:${VITE_PORT}"
echo "  Proxy:   /api -> ${BACKEND_URL}"
echo "  Env:     ${FRONTEND_ENV_TYPE}"
echo "  PM:      ${PACKAGE_MANAGER}"
echo "========================================"

case "$FRONTEND_ENV_TYPE" in
  system)
    echo ">> 使用系统 Node 环境"
    ;;

  conda)
    echo ">> 使用 Conda Node 环境"
    activate_conda_env
    ;;

  *)
    echo "错误: 不支持的 FRONTEND_ENV_TYPE=${FRONTEND_ENV_TYPE}"
    echo "允许值: system, conda"
    exit 1
    ;;
esac

cd front-end

if [ ! -f package.json ]; then
  echo "错误: 当前目录不是前端项目目录，未找到 package.json"
  exit 1
fi

case "$PACKAGE_MANAGER" in
  npm)
    require_command npm
    INSTALL_CMD=(npm install)
    DEV_CMD=(npm run dev -- --host 0.0.0.0 --port "$VITE_PORT")
    ;;

  pnpm)
    require_command pnpm
    INSTALL_CMD=(pnpm install)
    DEV_CMD=(pnpm run dev -- --host 0.0.0.0 --port "$VITE_PORT")
    ;;

  yarn)
    require_command yarn
    INSTALL_CMD=(yarn install)
    DEV_CMD=(yarn run dev --host 0.0.0.0 --port "$VITE_PORT")
    ;;

  *)
    echo "错误: 不支持的 PACKAGE_MANAGER=${PACKAGE_MANAGER}"
    echo "允许值: npm, pnpm, yarn"
    exit 1
    ;;
esac

if [ ! -d node_modules ]; then
  echo ">> 安装依赖..."
  "${INSTALL_CMD[@]}"
fi

echo ""
echo ">> 启动 Vite 开发服务器..."
exec "${DEV_CMD[@]}"