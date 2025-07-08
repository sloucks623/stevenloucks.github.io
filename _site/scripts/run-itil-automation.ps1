# ITIL 4 Automation PowerShell Wrapper
# Handles Python version selection and execution
# Author: Steven Loucks

param(
    [Parameter(Mandatory=$false)]
    [string]$Directory = ".",
    
    [Parameter(Mandatory=$false)]
    [switch]$CreateMissing = $false,
    
    [Parameter(Mandatory=$false)]
    [switch]$FullSection = $false,
    
    [Parameter(Mandatory=$false)]
    [switch]$Help = $false
)

function Find-Python {
    # Try to find the best Python installation
    $pythonCommands = @("python3", "python", "py")
    
    foreach ($cmd in $pythonCommands) {
        try {
            $version = & $cmd --version 2>&1
            if ($version -match "Python 3\.\d+") {
                Write-Host "✅ Found Python: $version" -ForegroundColor Green
                return $cmd
            }
        }
        catch {
            # Command not found, continue
        }
    }
    
    # If no python found, try the Windows Python Launcher with specific version
    try {
        $version = & py -3 --version 2>&1
        if ($version -match "Python 3\.\d+") {
            Write-Host "✅ Found Python via launcher: $version" -ForegroundColor Green
            return "py -3"
        }
    }
    catch {
        # Python launcher not available
    }
    
    return $null
}

function Show-PythonHelp {
    Write-Host @"
🔧 PYTHON SETUP HELP

It looks like Python isn't properly configured. Here's how to fix it:

OPTION 1 - Install Python from Microsoft Store (Recommended):
1. Open Microsoft Store
2. Search for "Python 3.11" or "Python 3.12"
3. Install the latest version
4. Restart PowerShell and try again

OPTION 2 - Install from Python.org:
1. Go to https://python.org/downloads
2. Download Python 3.11 or newer
3. During installation, check "Add Python to PATH"
4. Restart PowerShell and try again

OPTION 3 - Use existing Python installation:
If you have Python installed but getting version prompts:
- Run: py -3 --version
- Or: python3 --version
- Or: python --version

Then manually run the script:
py -3 itil-automation.py [options]

"@ -ForegroundColor Yellow
}

# Main execution
Write-Host "🚀 ITIL 4 Lab Documentation Automation" -ForegroundColor Cyan
Write-Host "=" * 50

if ($Help) {
    Write-Host @"
POWERSHELL WRAPPER USAGE:
    .\run-itil-automation.ps1 [options]

OPTIONS:
    -Directory <path>     Directory to scan (default: current)
    -CreateMissing        Create missing README files
    -FullSection          Add complete ITIL 4 sections
    -Help                 Show this help

EXAMPLES:
    .\run-itil-automation.ps1
    .\run-itil-automation.ps1 -Directory "C:\Labs" -CreateMissing
    .\run-itil-automation.ps1 -FullSection

"@ -ForegroundColor Green
    exit 0
}

# Find Python
$pythonCmd = Find-Python

if (-not $pythonCmd) {
    Write-Host "❌ Python 3 not found or not properly configured" -ForegroundColor Red
    Show-PythonHelp
    exit 1
}

# Build arguments for Python script
$scriptPath = Join-Path $PSScriptRoot "itil-automation.py"
$scriptArgs = @($scriptPath, $Directory)

if ($CreateMissing) {
    $scriptArgs += "--create-missing"
}

if ($FullSection) {
    $scriptArgs += "--full-section"
}

Write-Host "🐍 Executing Python script..." -ForegroundColor Yellow
Write-Host "Command: $pythonCmd $($scriptArgs -join ' ')" -ForegroundColor Gray
Write-Host ""

try {
    # Execute the Python script
    & $pythonCmd @scriptArgs
    
    if ($LASTEXITCODE -eq 0) {
        Write-Host ""
        Write-Host "🎉 Script completed successfully!" -ForegroundColor Green
    } else {
        Write-Host ""
        Write-Host "⚠️  Script completed with warnings or errors." -ForegroundColor Yellow
    }
}
catch {
    Write-Host "❌ Error executing Python script: $($_.Exception.Message)" -ForegroundColor Red
    Write-Host ""
    Write-Host "💡 Try running the Python script directly:" -ForegroundColor Yellow
    Write-Host "$pythonCmd `"$scriptPath`" --help" -ForegroundColor White
}
