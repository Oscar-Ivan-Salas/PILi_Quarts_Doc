$ErrorActionPreference = "Stop"

Write-Host "==============================================" -ForegroundColor Cyan
Write-Host "   NotebookLM MCP Server Setup (by PILi)" -ForegroundColor Cyan
Write-Host "==============================================" -ForegroundColor Cyan

# Define paths
$VenvPath = "$PSScriptRoot\.agent\mcp\notebooklm\venv"
$PythonExe = "$VenvPath\Scripts\python.exe"
$McpExe = "$VenvPath\Scripts\notebooklm-mcp.exe"
$ConfigFile = "$PSScriptRoot\.agent\mcp\notebooklm\config.yaml"

# Check if venv exists
if (-not (Test-Path $PythonExe)) {
    Write-Host "Error: Virtual environment not found at $VenvPath" -ForegroundColor Red
    Write-Host "Please ask PILi to reinstall notebooklm-mcp."
    exit 1
}

# Ensure directory exists
$ConfigDir = Split-Path $ConfigFile
if (-not (Test-Path $ConfigDir)) {
    New-Item -ItemType Directory -Path $ConfigDir -Force | Out-Null
}

Write-Host "`nStep 1: Notebook Requirement" -ForegroundColor Yellow
Write-Host "To initialize the MCP server, we need a target Notebook."
Write-Host "1. Go to https://notebooklm.google.com/"
Write-Host "2. Open an existing notebook or create a new one."
Write-Host "3. Copy the URL from your browser address bar."
Write-Host "   (It looks like: https://notebooklm.google.com/notebook/xxxxxxxx-xxxx-xxxx-xxxx-xxxxxxxxxxxx)"

$NotebookUrl = Read-Host -Prompt "`nPaste your Notebook URL here"

if ([string]::IsNullOrWhiteSpace($NotebookUrl)) {
    Write-Host "Error: No URL provided." -ForegroundColor Red
    exit 1
}

Write-Host "`nStep 2: Authentication" -ForegroundColor Yellow
Write-Host "A browser window will open for you to log in to Google."
Write-Host "Configurations will be saved to: $ConfigFile"

# Run setup with explicit config path and notebook
& $McpExe quick-setup --config "$ConfigFile" --notebook "$NotebookUrl"

Write-Host "`n==============================================" -ForegroundColor Cyan
Write-Host "   Configuration for your IDE" -ForegroundColor Cyan
Write-Host "==============================================" -ForegroundColor Cyan
Write-Host "Add this to your MCP settings (e.g. claude_desktop_config.json):" -ForegroundColor Green

$ConfigJson = @"
{
  `"mcpServers`": {
    `"notebooklm`": {
      `"command`": `"$PWD\.agent\mcp\notebooklm\venv\Scripts\notebooklm-mcp.exe`",
      `"args`": [`"run`", `"--config`", `"$ConfigFile`"],
      `"env`": {}
    }
  }
}
"@

Write-Host $ConfigJson -ForegroundColor Gray
Write-Host "`nDone! You can now use NotebookLM tools in your AI assistant." -ForegroundColor Cyan
Pause
