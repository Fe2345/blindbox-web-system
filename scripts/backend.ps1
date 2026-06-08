$ErrorActionPreference = "Stop"
Set-StrictMode -Version Latest

function Load-DotEnv {
    param (
        [string]$EnvPath
    )

    if (-not (Test-Path $EnvPath)) {
        return
    }

    Get-Content $EnvPath | ForEach-Object {
        $line = $_.Trim()

        if ($line -eq "") {
            return
        }

        if ($line.StartsWith("#")) {
            return
        }

        if ($line -notmatch "^\s*([A-Za-z_][A-Za-z0-9_]*)\s*=\s*(.*)\s*$") {
            return
        }

        $name = $matches[1]
        $value = $matches[2].Trim()

        if (
            ($value.StartsWith('"') -and $value.EndsWith('"')) -or
            ($value.StartsWith("'") -and $value.EndsWith("'"))
        ) {
            $value = $value.Substring(1, $value.Length - 2)
        }

        [Environment]::SetEnvironmentVariable($name, $value, "Process")
    }
}

function Get-EnvOrDefault {
    param (
        [string]$Name,
        [string]$DefaultValue
    )

    $value = [Environment]::GetEnvironmentVariable($Name, "Process")

    if ([string]::IsNullOrWhiteSpace($value)) {
        return $DefaultValue
    }

    return $value
}

function Require-Command {
    param (
        [string]$CommandName
    )

    if (-not (Get-Command $CommandName -ErrorAction SilentlyContinue)) {
        throw "未找到命令: $CommandName"
    }
}

$ScriptDir = Split-Path -Parent $MyInvocation.MyCommand.Path
$ProjectDir = Resolve-Path (Join-Path $ScriptDir "..")

Set-Location $ProjectDir

Load-DotEnv -EnvPath (Join-Path $ProjectDir ".env")

$DjangoPort = Get-EnvOrDefault -Name "DJANGO_PORT" -DefaultValue "8001"
$VenvType = Get-EnvOrDefault -Name "VENV_TYPE" -DefaultValue "uv"

$DbHost = Get-EnvOrDefault -Name "DB_HOST" -DefaultValue "127.0.0.1"
$DbPort = Get-EnvOrDefault -Name "DB_PORT" -DefaultValue "3306"
$DbName = Get-EnvOrDefault -Name "DB_NAME" -DefaultValue "gugou"

$RedisHost = Get-EnvOrDefault -Name "REDIS_HOST" -DefaultValue "127.0.0.1"
$RedisPort = Get-EnvOrDefault -Name "REDIS_PORT" -DefaultValue "6379"
$UseRedis = Get-EnvOrDefault -Name "USE_REDIS" -DefaultValue "false"

Write-Host "========================================"
Write-Host "  后端启动"
Write-Host "========================================"
Write-Host "  数据库: ${DbHost}:${DbPort}/${DbName}"
Write-Host "  Redis:  ${RedisHost}:${RedisPort} (USE_REDIS=${UseRedis})"
Write-Host "  Django: http://127.0.0.1:${DjangoPort}"
Write-Host "  VENV:   ${VenvType}"
Write-Host "========================================"

$BackendDir = Join-Path $ProjectDir "back-end"

if (-not (Test-Path $BackendDir)) {
    throw "未找到 back-end 目录: $BackendDir"
}

Set-Location $BackendDir

switch ($VenvType) {
    "uv" {
        Write-Host ">> 使用 uv 环境"

        Require-Command -CommandName "uv"

        if (-not (Test-Path ".venv")) {
            Write-Host ">> 创建 uv 虚拟环境..."
            uv sync
        }

        Write-Host ">> 执行数据库迁移..."
        uv run python manage.py migrate --noinput

        Write-Host ""
        Write-Host ">> 启动 Django 开发服务器 (0.0.0.0:${DjangoPort})..."
        uv run python manage.py runserver "0.0.0.0:${DjangoPort}"
    }

    "conda" {
        Write-Host ">> 使用 conda 环境"

        Require-Command -CommandName "conda"

        $CondaVenvName = [Environment]::GetEnvironmentVariable("CONDA_VENV_NAME", "Process")

        if ([string]::IsNullOrWhiteSpace($CondaVenvName)) {
            throw "CONDA_VENV_NAME 未配置"
        }

        Write-Host ">> 初始化 Conda PowerShell 环境..."
        (& conda "shell.powershell" "hook") | Out-String | Invoke-Expression

        Write-Host ">> 激活 Conda 环境: $CondaVenvName"
        conda activate $CondaVenvName

        Write-Host ">> 执行数据库迁移..."
        python manage.py migrate --noinput

        Write-Host ""
        Write-Host ">> 启动 Django 开发服务器 (0.0.0.0:${DjangoPort})..."
        python manage.py runserver "0.0.0.0:${DjangoPort}"
    }

    default {
        throw "不支持的 VENV_TYPE: $VenvType。允许值: uv, conda"
    }
}