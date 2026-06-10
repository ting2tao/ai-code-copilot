# ai-code-copilot Windows 安装脚本
#
# 使用方式:
#   1. 远程一行安装(推荐):
#      irm https://raw.githubusercontent.com/ting2tao/ai-code-copilot/main/install.ps1 | iex
#
#   2. 指定平台:
#      .\install.ps1 -Codex
#      .\install.ps1 -Claude
#
#   3. 本地安装(已 git clone 后):
#      .\install.ps1 -Codex
#
#   4. 卸载:
#      .\install.ps1 -Codex -Uninstall

param(
    [switch]$Uninstall,
    [switch]$Codex,
    [switch]$Claude
)

Set-StrictMode -Version Latest
$ErrorActionPreference = 'Stop'

# ============ 配置 ============
$RepoUrl    = if ($env:CODE_COPILOT_REPO) { $env:CODE_COPILOT_REPO } else { "https://github.com/ting2tao/ai-code-copilot.git" }
$Platform   = if ($Codex) { "codex" } elseif ($Claude) { "claude" } elseif ($env:CODE_COPILOT_PLATFORM) { $env:CODE_COPILOT_PLATFORM } else { "auto" }
if ($Platform -eq "auto") {
    if ($env:CODEX_HOME -or (Get-Command codex -ErrorAction SilentlyContinue)) { $Platform = "codex" } else { $Platform = "claude" }
}
if ($Platform -eq "codex") {
    $AppName = "Codex"
    $AppHome = if ($env:CODEX_HOME) { $env:CODEX_HOME } else { Join-Path $env:USERPROFILE ".codex" }
} elseif ($Platform -eq "claude") {
    $AppName = "Claude Code"
    $AppHome = if ($env:CLAUDE_HOME) { $env:CLAUDE_HOME } else { Join-Path $env:USERPROFILE ".claude" }
} else {
    Write-Host "x  平台必须是 auto、codex 或 claude" -ForegroundColor Red
    exit 1
}
$InstallDir = if ($env:AI_CODE_COPILOT_HOME) { $env:AI_CODE_COPILOT_HOME } else { Join-Path $AppHome "ai_code_copilot" }
$SkillsDir  = Join-Path $AppHome "skills"
$SkillLink  = Join-Path $SkillsDir "ai-code-copilot"

# ============ 工具函数 ============
function Info { param($msg) Write-Host "i  $msg" -ForegroundColor Cyan }
function Ok   { param($msg) Write-Host "v  $msg" -ForegroundColor Green }
function Warn { param($msg) Write-Host "!  $msg" -ForegroundColor Yellow }
function Err  { param($msg) Write-Host "x  $msg" -ForegroundColor Red; exit 1 }

# ============ 卸载 ============
if ($Uninstall) {
    Write-Host "卸载 ai-code-copilot ($AppName)" -ForegroundColor White
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

if ($Platform -eq "codex" -and -not (Get-Command codex -ErrorAction SilentlyContinue)) {
    Warn "未检测到 codex 命令"
    Warn "本脚本只负责框架安装，Codex 需另行安装"
    Write-Host ""
} elseif ($Platform -eq "claude" -and -not (Get-Command claude -ErrorAction SilentlyContinue)) {
    Warn "未检测到 claude 命令"
    Warn "本脚本只负责框架安装，Claude Code 需另行安装(https://docs.claude.com/claude-code)"
    Write-Host ""
}

Info "目标平台: $AppName"
Info "安装目录: $InstallDir"

# ============ 安装或更新 ============
$SourceDir = $PWD
$IsSourceDir = (Test-Path (Join-Path $SourceDir "skill\SKILL.md")) -and (Test-Path (Join-Path $SourceDir "agents\copilot-prompt.md"))

if (Test-Path (Join-Path $InstallDir ".git")) {
    Info "检测到已安装，执行更新..."
    Push-Location $InstallDir
    try {
        $before = git rev-parse --short HEAD
        git pull --ff-only
        if ($LASTEXITCODE -ne 0) {
            if ($IsSourceDir) {
                Warn "远程更新失败，从本地源码目录同步..."
                $src = $SourceDir + "\*"
                Copy-Item -Path $src -Destination $InstallDir -Recurse -Force -Exclude ".git",".DS_Store"
                Ok "已从本地源码同步"
            } else {
                Write-Host "x  更新失败，请手动检查: cd '$InstallDir' && git status" -ForegroundColor Red
                exit 1
            }
        } else {
            $after = git rev-parse --short HEAD
            if ($before -eq $after) { Ok "已是最新版本 ($after)" } else { Ok "已更新: $before → $after" }
        }
    } finally {
        Pop-Location
    }
} elseif (Test-Path $InstallDir) {
    if ($IsSourceDir) {
        Info "检测到本地目录(非 git 仓库)，从源码目录同步..."
        $src = $SourceDir + "\*"
        Copy-Item -Path $src -Destination $InstallDir -Recurse -Force -Exclude ".git",".DS_Store"
        Ok "已从本地源码同步"
    } else {
        Info "检测到本地目录(非 git 仓库)，重新 clone..."
        Remove-Item $InstallDir -Force -Recurse
        git clone $RepoUrl $InstallDir
        Ok "已 clone 到 $InstallDir"
    }
} else {
    $parent = Split-Path $InstallDir -Parent
    if (-not (Test-Path $parent)) { New-Item -ItemType Directory -Path $parent -Force | Out-Null }
    if ($IsSourceDir) {
        Info "从本地源码目录安装..."
        Copy-Item -Path $SourceDir -Destination $InstallDir -Recurse -Force -Exclude ".git",".DS_Store"
        Ok "已复制到 $InstallDir"
    } else {
        Info "首次安装，从 $RepoUrl clone..."
        git clone $RepoUrl $InstallDir
        if ($LASTEXITCODE -ne 0) {
            Write-Host "x  git clone 失败" -ForegroundColor Red
            Write-Host "x  请确认仓库地址正确，或先手动 clone 到 $InstallDir 后再跑本脚本" -ForegroundColor Red
            exit 1
        }
        Ok "已 clone 到 $InstallDir"
    }
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
$SettingsFile = Join-Path $AppHome "settings.json"

$pythonCommand = Get-Command python3 -ErrorAction SilentlyContinue
if (-not $pythonCommand) {
    $pythonCommand = Get-Command python -ErrorAction SilentlyContinue
}
if (-not $pythonCommand) {
    Write-Host "!  未找到 Python；hook 仍会注入 L0 安全规则，但 context freshness 与 active change 摘要会被跳过。" -ForegroundColor Yellow
    Write-Host "!  建议安装 Python 3，并确保 python3 或 python 在 PATH 中。" -ForegroundColor Yellow
}

if (-not (Test-Path $SettingsFile)) {
    $settingsParent = Split-Path $SettingsFile -Parent
    if (-not (Test-Path $settingsParent)) { New-Item -ItemType Directory -Path $settingsParent -Force | Out-Null }
    '{}' | Set-Content $SettingsFile -Encoding UTF8
}

$settingsRaw = Get-Content $SettingsFile -Raw -Encoding UTF8
# 找到 bash.exe（Git for Windows 提供）
$bashCommand = Get-Command bash -ErrorAction SilentlyContinue
$bashExe = if ($bashCommand) { $bashCommand.Source } else { "bash" }
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
$existingHooks = @($settings.hooks.SessionStart) | Where-Object {
    $entry = $_
    -not (@($entry.hooks) | Where-Object { $_.command -like "*$HookScript*" })
}
$settings.hooks.SessionStart = @($existingHooks) + $hookEntry
$settings | ConvertTo-Json -Depth 10 | Set-Content $SettingsFile -Encoding UTF8
Ok "hook 已注册到 $SettingsFile"

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
Write-Host "  1. 重启 $AppName 会话(让 skill 生效)"
Write-Host "  2. cd 到业务项目根目录"
Write-Host "  3. 输入: 初始化项目"
Write-Host "  4. 之后输入: 帮我做 xxx 需求 即可触发流程"
Write-Host ""
Write-Host "更新:     powershell -ExecutionPolicy Bypass -File `"$InstallDir\install.ps1`" -$Platform"
Write-Host "卸载:     powershell -ExecutionPolicy Bypass -File `"$InstallDir\install.ps1`" -$Platform -Uninstall"
Write-Host ""
