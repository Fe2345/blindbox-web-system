# 乐抽盲盒平台 (BlindBox Platform)

在线盲盒抽奖与交易平台，支持用户抽盒、二手交易、积分兑换、订单管理，商家后台与管理员后台。

## 技术栈

| 层 | 技术 |
|---|------|
| 后端框架 | Django + Django REST Framework |
| 认证 | SimpleJWT (httpOnly Cookie) |
| 数据库 | MariaDB 11.8 (Docker) |
| 缓存 | Redis |
| 前端框架 | Vue 3 + TypeScript |
| 构建工具 | Vite |
| UI 组件库 | Element Plus |
| 状态管理 | Pinia |
| HTTP 客户端 | Axios |
| 虚拟环境 | uv (推荐) / conda |

## 项目结构

```
system/
├── back-end/               # Django 后端
│   ├── apps/
│   │   ├── accounts/       # 用户、登录、地址、行政区划
│   │   ├── blindbox/       # 盲盒商品、抽盒逻辑
│   │   ├── assets/         # 用户资产（拥有的盲盒）
│   │   ├── orders/         # 订单管理
│   │   ├── exchange/       # 二手交易/转卖
│   │   ├── points/         # 积分系统
│   │   ├── merchant/       # 商家后台
│   │   └── operations/     # 运营管理
│   ├── config/             # Django 配置、路由
│   └── media/              # 上传文件存储（头像等）
├── front-end/              # Vue 3 前端
│   ├── src/
│   │   ├── api/            # 接口请求封装
│   │   ├── components/     # 公共组件
│   │   ├── router/         # 路由配置
│   │   ├── stores/         # Pinia 状态管理
│   │   ├── types/          # TypeScript 类型
│   │   └── views/          # 页面组件
│   │       ├── user/       # 用户端页面
│   │       ├── admin/      # 管理端页面
│   │       └── merchant/   # 商家端页面
│   ├── index.html          # 用户端入口
│   ├── admin.html          # 管理端入口
│   └── merchant.html       # 商家端入口
├── scripts/                # 启动脚本与数据导出
│   ├── backend.sh          # Linux/macOS 后端启动
│   ├── frontend.sh         # Linux/macOS 前端启动
│   ├── backend.ps1         # Windows PowerShell 后端启动
│   ├── frontend.ps1        # Windows PowerShell 前端启动
│   └── data.sql            # 数据库导出 (REPLACE 模式)
├── docs/                   # 项目文档
├── .env.example            # 环境变量模板
└── README.md
```

## 快速开始

### 1. 环境准备

- **Python 3.12+** （通过 uv 或 conda 管理）
- **Node.js 18+** （通过系统安装或 conda）
- **Docker**（运行 MariaDB 和 Redis）

### 2. 启动数据库

```bash
# 启动 MariaDB（端口 3306）
docker run -d --name mariadb \
  -e MARIADB_ROOT_PASSWORD=root123 \
  -p 3306:3306 \
  mariadb:11.8

# 启动 Redis（端口 6379）
docker run -d --name redis \
  -p 6379:6379 \
  redis:7-alpine
```

### 3. 配置环境变量

```bash
# 从模板创建 .env 文件
cp .env.example .env
```

按需修改 `.env` 中的配置项，特别是数据库密码 `DB_PASSWORD` 和 `DJANGO_SECRET_KEY`。

### 4. 导入数据（可选）

```bash
# 方式一：通过 Docker 容器导入
docker exec -i mariadb mariadb -u root -proot123 blindbox < scripts/data.sql

# 方式二：通过宿主机客户端导入
mariadb -h 127.0.0.1 -P 3306 -u root -proot123 blindbox < scripts/data.sql
```

> `data.sql` 使用 `REPLACE INTO` 语法，可重复导入覆盖数据而不报主键冲突。

### 5. 启动服务

**后端：**

```bash
# Linux / macOS
bash scripts/backend.sh

# Windows PowerShell
.\scripts\backend.ps1
```

后端默认运行在 `http://127.0.0.1:8002`（通过 `DJANGO_PORT` 配置）。

**前端：**

```bash
# Linux / macOS
bash scripts/frontend.sh

# Windows PowerShell
.\scripts\frontend.ps1
```

前端默认运行在 `http://127.0.0.1:3000`（通过 `VITE_PORT` 配置）。

### 6. 访问

| 入口 | 地址 | 说明 |
|------|------|------|
| 用户端 | http://127.0.0.1:3000 | 盲盒购买、抽盒、个人中心 |
| 商家端 | http://127.0.0.1:3000/merchant | 商品管理、订单处理 |
| 管理端 | http://127.0.0.1:3000/admin | 平台运营管理 |
| Django Admin | http://127.0.0.1:8002/admin/ | Django 原生后台 |

## 启动脚本说明

所有启动脚本均从项目根目录执行，脚本会自动：

1. 加载 `.env` 中的环境变量
2. 根据 `VENV_TYPE`（`uv` 或 `conda`）激活/创建 Python 虚拟环境
3. 执行数据库迁移 `migrate`
4. 根据 `FRONTEND_ENV_TYPE`（`system` 或 `conda`）选择 Node 环境
5. 自动安装前端依赖（如 `node_modules` 不存在）

关键环境变量（`.env`）：

| 变量 | 说明 | 默认值 |
|------|------|--------|
| `VENV_TYPE` | Python 虚拟环境类型: `uv` / `conda` | `uv` |
| `CONDA_VENV_NAME` | conda 环境名称 | `uv` |
| `FRONTEND_ENV_TYPE` | Node 运行环境: `system` / `conda` | `system` |
| `PACKAGE_MANAGER` | 前端包管理器: `npm` / `pnpm` / `yarn` | `npm` |
| `DJANGO_PORT` | Django 监听端口 | `8002` |
| `VITE_PORT` | Vite 开发服务器端口 | `3000` |
| `VITE_BACKEND_URL` | 后端地址（Vite proxy 目标） | `http://127.0.0.1:8002` |

## 数据库导出

```bash
# 导出当前数据库（REPLACE 模式，不含建表语句）
docker exec mariadb mariadb-dump -u root -proot123 \
  --replace --skip-add-drop-table --no-create-info \
  blindbox > scripts/data.sql
```

## 后端 API 路由

| 前缀 | 端 | 说明 |
|------|---|------|
| `/user/api/` | 用户端 | 登录、注册、用户信息、盲盒、订单、地址等 |
| `/merchant/api/` | 商家端 | 商品管理、发货、数据统计 |
| `/admin/api/` | 管理端 | 用户管理、运营配置、订单审核 |
| `/admin/` | Django | 原生后台管理 |
| `/media/` | 静态文件 | 用户上传文件（头像等） |
