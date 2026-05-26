# ai-code-copilot Windows 安装脚本
#
# 使用方式:
#   1. 远程一行安装(推荐):
#      irm https://git.eminxing.com/ai/ai-code-copilot/raw/master/install.ps1 | iex
#
#   2. 本地安装(已 git clone 后):
#      .\install.ps1
#
#   3. 卸载:
#      .\install.ps1 -Uninstall

param(
    [switch]$Uninstall
)

Set-StrictMode -Version Latest
$ErrorActionPreference = 'Stop'

# ============ 配置 ============
$RepoUrl    = if ($env:CODE_COPILOT_REPO) { $env:CODE_COPILOT_REPO } else { "https://git.eminxing.com/ai/ai-code-copilot.git" }
$InstallDir = Join-Path $env:USERPROFILE ".claude\ai_code_copilot"
$SkillsDir  = Join-Path $env:USERPROFILE ".claude\skills"
$SkillLink  = Join-Path $SkillsDir "ai-code-copilot"

# ============ 工具函数 ============
function Info { param($msg) Write-Host "i  $msg" -ForegroundColor Cyan }
function Ok   { param($msg) Write-Host "v  $msg" -ForegroundColor Green }
function Warn { param($msg) Write-Host "!  $msg" -ForegroundColor Yellow }
function Err  { param($msg) Write-Host "x  $msg" -ForegroundColor Red; exit 1 }

# ============ 卸载 ============
if ($Uninstall) {
    Write-Host "卸载 ai-code-copilot" -ForegroundColor White
    Write-Host ""
    if (Test-Path $SkillLink) {
        Remove-Item $SkillLink -Force -Recurse
        Ok "已移除 skill junction: $SkillLink"
    } else {
        Info "skill junction 不存在，跳过"
    }
    if (Test-Path $InstallDir) {
        Warn "保留框架目录: $InstallDir"
        Warn "如需彻底删除: Remove-Item -Recurse -Force '$InstallDir'"
    }
    Ok "卸载完成"
    exit 0
}

# ============ Banner ============
Write-Host "╔══════════════════════════════════════════╗"
Write-Host "║   ai-code-copilot — 安装/更新              ║"
Write-Host "╚══════════════════════════════════════════╝"
Write-Host ""

# ============ 环境检测 ============
if (-not (Get-Command git -ErrorAction SilentlyContinue)) {
    Write-Host "x  未找到 git，请先安装 Git for Windows: https://git-scm.com" -ForegroundColor Red
    exit 1
}

if (-not (Get-Command claude -ErrorAction SilentlyContinue)) {
    Warn "未检测到 claude 命令"
    Warn "本脚本只负责框架安装，Claude Code 需另行安装(https://docs.claude.com/claude-code)"
    Write-Host ""
}

# ============ 安装或更新 ============
if (Test-Path (Join-Path $InstallDir ".git")) {
    Info "检测到已安装，执行更新..."
    Push-Location $InstallDir
    try {
        $before = git rev-parse --short HEAD
        git pull --ff-only
        if ($LASTEXITCODE -ne 0) {
            Write-Host "x  更新失败，请手动检查: cd '$InstallDir' && git status" -ForegroundColor Red
            exit 1
        }
        $after = git rev-parse --short HEAD
        if ($before -eq $after) { Ok "已是最新版本 ($after)" } else { Ok "已更新: $before → $after" }
    } finally {
        Pop-Location
    }
} elseif (Test-Path $InstallDir) {
    Info "检测到本地目录(非 git 仓库)，跳过 clone，仅创建 junction"
} else {
    Info "首次安装，从 $RepoUrl clone..."
    $parent = Split-Path $InstallDir -Parent
    if (-not (Test-Path $parent)) { New-Item -ItemType Directory -Path $parent -Force | Out-Null }
    git clone $RepoUrl $InstallDir
    if ($LASTEXITCODE -ne 0) {
        Write-Host "x  git clone 失败" -ForegroundColor Red
        Write-Host "x  请确认仓库地址正确，或先手动 clone 到 $InstallDir 后再跑本脚本" -ForegroundColor Red
        exit 1
    }
    Ok "已 clone 到 $InstallDir"
}

# ============ 创建 Junction ============
Write-Host ""
Info "注册 skill..."

if (-not (Test-Path $SkillsDir)) {
    New-Item -ItemType Directory -Path $SkillsDir -Force | Out-Null
}

$SkillTarget = Join-Path $InstallDir "skill"
if (-not (Test-Path $SkillTarget)) {
    Write-Host "x  未找到 skill 源目录: $SkillTarget" -ForegroundColor Red
    Write-Host "x  仓库结构可能异常" -ForegroundColor Red
    exit 1
}

if (Test-Path $SkillLink) { Remove-Item $SkillLink -Force -Recurse }

New-Item -ItemType Junction -Path $SkillLink -Target $SkillTarget | Out-Null
Ok "skill junction: $SkillLink → $SkillTarget"

# ============ 注册 SessionStart Hook ============
Write-Host ""
Info "注册 session-start hook..."

$HookScript   = Join-Path $InstallDir "hooks\session-start"
$SettingsFile = Join-Path $env:USERPROFILE ".claude\settings.json"

if (-not (Test-Path $SettingsFile)) {
    '{}' | Set-Content $SettingsFile -Encoding UTF8
}

$settingsRaw = Get-Content $SettingsFile -Raw -Encoding UTF8
if ($settingsRaw -match "ai-code-copilot") {
    Ok "hook 已注册，跳过"
} else {
    # 找到 bash.exe（Git for Windows 提供）
    $bashExe = (Get-Command bash -ErrorAction SilentlyContinue)?.Source
    if (-not $bashExe) { $bashExe = "bash" }
    $hookCmd = "$bashExe `"$HookScript`""

    $settings = $settingsRaw | ConvertFrom-Json
    if (-not (Get-Member -InputObject $settings -Name hooks -MemberType NoteProperty)) {
        $settings | Add-Member -NotePropertyName hooks -NotePropertyValue ([PSCustomObject]@{})
    }
    if (-not (Get-Member -InputObject $settings.hooks -Name SessionStart -MemberType NoteProperty)) {
        $settings.hooks | Add-Member -NotePropertyName SessionStart -NotePropertyValue @()
    }
    $hookEntry = [PSCustomObject]@{
        matcher = ""
        hooks   = @([PSCustomObject]@{ type = "command"; command = $hookCmd; async = $false })
    }
    $settings.hooks.SessionStart = @($settings.hooks.SessionStart) + $hookEntry
    $settings | ConvertTo-Json -Depth 10 | Set-Content $SettingsFile -Encoding UTF8
    Ok "hook 已注册到 $SettingsFile"
}

# ============ 自检 ============
Write-Host ""
Info "自检..."

if (-not (Test-Path $SkillLink)) {
    Write-Host "x  junction 创建失败" -ForegroundColor Red; exit 1
}
if (-not (Test-Path (Join-Path $SkillLink "SKILL.md"))) {
    Write-Host "x  SKILL.md 不可读: $SkillLink\SKILL.md" -ForegroundColor Red; exit 1
}
Ok "junction 与 SKILL.md 正常"

if (Test-Path (Join-Path $InstallDir ".git")) {
    Push-Location $InstallDir
    $version = git rev-parse --short HEAD
    Pop-Location
    Ok "当前版本: $version"
}

# ============ 完成提示 ============
Write-Host ""
Write-Host "╔══════════════════════════════════════════╗" -ForegroundColor Green
Write-Host "║  ✅ ai-code-copilot 安装完成                ║" -ForegroundColor Green
Write-Host "╚══════════════════════════════════════════╝" -ForegroundColor Green
Write-Host ""
Write-Host "下一步:"
Write-Host "  1. 重启 Claude Code 会话(让 skill 生效)"
Write-Host "  2. cd 到业务项目根目录"
Write-Host "  3. 输入: 初始化项目"
Write-Host "  4. 之后输入: 帮我做 xxx 需求 即可触发流程"
Write-Host ""
Write-Host "更新:     powershell -ExecutionPolicy Bypass -File `"$InstallDir\install.ps1`""
Write-Host "卸载:     powershell -ExecutionPolicy Bypass -File `"$InstallDir\install.ps1`" -Uninstall"
Write-Host ""
