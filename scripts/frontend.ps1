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

function Invoke-CommandChecked {
    param (
        [string]$FilePath,
        [string[]]$Arguments
    )

    & $FilePath @Arguments

    if ($LASTEXITCODE -ne 0) {
        throw "命令执行失败: $FilePath $($Arguments -join ' ')"
    }
}

$ScriptDir = Split-Path -Parent $MyInvocation.MyCommand.Path
$ProjectDir = Resolve-Path (Join-Path $ScriptDir "..")

Set-Location $ProjectDir

Load-DotEnv -EnvPath (Join-Path $ProjectDir ".env")

$VitePort = Get-EnvOrDefault -Name "VITE_PORT" -DefaultValue "3000"
$BackendUrl = Get-EnvOrDefault -Name "VITE_BACKEND_URL" -DefaultValue "http://127.0.0.1:8001"
$FrontendEnvType = Get-EnvOrDefault -Name "FRONTEND_ENV_TYPE" -DefaultValue "system"
$PackageManager = Get-EnvOrDefault -Name "PACKAGE_MANAGER" -DefaultValue "npm"

Write-Host "========================================"
Write-Host "  前端启动"
Write-Host "========================================"
Write-Host "  Vite:    http://127.0.0.1:${VitePort}"
Write-Host "  Proxy:   /api -> ${BackendUrl}"
Write-Host "  Env:     ${FrontendEnvType}"
Write-Host "  PM:      ${PackageManager}"
Write-Host "========================================"

switch ($FrontendEnvType) {
    "system" {
        Write-Host ">> 使用系统 Node 环境"
    }

    "conda" {
        Write-Host ">> 使用 Conda Node 环境"

        Require-Command -CommandName "conda"

        $CondaVenvName = [Environment]::GetEnvironmentVariable("CONDA_VENV_NAME", "Process")

        if ([string]::IsNullOrWhiteSpace($CondaVenvName)) {
            throw "FRONTEND_ENV_TYPE=conda 时必须配置 CONDA_VENV_NAME"
        }

        Write-Host ">> 初始化 Conda PowerShell 环境..."
        (& conda "shell.powershell" "hook") | Out-String | Invoke-Expression

        Write-Host ">> 激活 Conda 环境: $CondaVenvName"
        conda activate $CondaVenvName
    }

    default {
        throw "不支持的 FRONTEND_ENV_TYPE: $FrontendEnvType。允许值: system, conda"
    }
}

$FrontendDir = Join-Path $ProjectDir "front-end"

if (-not (Test-Path $FrontendDir)) {
    throw "未找到 frontend 目录: $FrontendDir"
}

Set-Location $FrontendDir

if (-not (Test-Path "package.json")) {
    throw "当前目录不是前端项目目录，未找到 package.json"
}

switch ($PackageManager) {
    "npm" {
        Require-Command -CommandName "npm"

        $InstallFile = "npm"
        $InstallArgs = @("install")

        $DevFile = "npm"
        $DevArgs = @("run", "dev", "--", "--host", "0.0.0.0", "--port", $VitePort)
    }

    "pnpm" {
        Require-Command -CommandName "pnpm"

        $InstallFile = "pnpm"
        $InstallArgs = @("install")

        $DevFile = "pnpm"
        $DevArgs = @("run", "dev", "--", "--host", "0.0.0.0", "--port", $VitePort)
    }

    "yarn" {
        Require-Command -CommandName "yarn"

        $InstallFile = "yarn"
        $InstallArgs = @("install")

        $DevFile = "yarn"
        $DevArgs = @("run", "dev", "--host", "0.0.0.0", "--port", $VitePort)
    }

    default {
        throw "不支持的 PACKAGE_MANAGER: $PackageManager。允许值: npm, pnpm, yarn"
    }
}

if (-not (Test-Path "node_modules")) {
    Write-Host ">> 安装依赖..."
    Invoke-CommandChecked -FilePath $InstallFile -Arguments $InstallArgs
}

Write-Host ""
Write-Host ">> 启动 Vite 开发服务器..."
& $DevFile @DevArgs