# Nephro API Backend Service Startup Script (PowerShell)
# This script starts the Nephrology AI Agent API server

param(
    [switch]$Direct,
    [int]$Port = 8002,
    [string]$Host = "0.0.0.0"
)

# Configuration
$ApiFile = "nephro_api.py"
$EnvFile = ".env"
$RequirementsFile = "requirements.txt"
$ScriptDir = Split-Path -Parent $MyInvocation.MyCommand.Path

# Colors for output
$Colors = @{
    Red = "Red"
    Green = "Green"
    Yellow = "Yellow"
    Blue = "Cyan"
    White = "White"
}

function Write-ColorOutput {
    param(
        [string]$Message,
        [string]$Color = "White"
    )
    Write-Host $Message -ForegroundColor $Colors[$Color]
}

function Test-PortInUse {
    param([int]$Port)
    try {
        $listener = [System.Net.NetworkInformation.IPGlobalProperties]::GetIPGlobalProperties().GetActiveTcpListeners()
        return $listener | Where-Object { $_.Port -eq $Port }
    }
    catch {
        return $false
    }
}

function Stop-ProcessOnPort {
    param([int]$Port)
    try {
        $processes = Get-NetTCPConnection -LocalPort $Port -ErrorAction SilentlyContinue | Select-Object -ExpandProperty OwningProcess
        foreach ($processId in $processes) {
            Write-ColorOutput "Stopping process $processId on port $Port..." "Yellow"
            Stop-Process -Id $processId -Force -ErrorAction SilentlyContinue
        }
        Start-Sleep -Seconds 2
        Write-ColorOutput "Processes stopped successfully" "Green"
    }
    catch {
        Write-ColorOutput "Could not stop processes on port $Port" "Yellow"
    }
}

function Test-PythonInstallation {
    $pythonCommands = @("python", "python3", "py")
    foreach ($cmd in $pythonCommands) {
        try {
            $version = & $cmd --version 2>$null
            if ($LASTEXITCODE -eq 0) {
                return $cmd
            }
        }
        catch {
            continue
        }
    }
    return $null
}

function Read-EnvFile {
    param([string]$FilePath)
    $envVars = @{}
    if (Test-Path $FilePath) {
        Get-Content $FilePath | ForEach-Object {
            if ($_ -match '^([^#][^=]+)=(.*)$') {
                $envVars[$matches[1].Trim()] = $matches[2].Trim()
            }
        }
    }
    return $envVars
}

# Main script execution
Clear-Host
Write-ColorOutput "===============================================" "Blue"
Write-ColorOutput "    Nephro API Backend Service Startup" "Blue"
Write-ColorOutput "===============================================" "Blue"
Write-ColorOutput "Script Directory: $ScriptDir" "Blue"
Write-ColorOutput "Timestamp: $(Get-Date)" "Blue"
Write-ColorOutput "" "White"

# Change to script directory
Set-Location $ScriptDir

# Check if .env file exists
if (-not (Test-Path $EnvFile)) {
    Write-ColorOutput "[ERROR] $EnvFile file not found!" "Red"
    Write-ColorOutput "[WARNING] Please copy .env.example to .env and configure your API keys" "Yellow"
    Read-Host "Press Enter to exit"
    exit 1
}

# Check if API file exists
if (-not (Test-Path $ApiFile)) {
    Write-ColorOutput "[ERROR] $ApiFile not found!" "Red"
    Read-Host "Press Enter to exit"
    exit 1
}

# Install dependencies if requirements file exists
if (Test-Path $RequirementsFile) {
    Write-ColorOutput "[INFO] Installing/updating Python dependencies..." "Blue"
    try {
        pip install -r $RequirementsFile --quiet
        if ($LASTEXITCODE -eq 0) {
            Write-ColorOutput "[SUCCESS] Dependencies installed successfully" "Green"
        } else {
            Write-ColorOutput "[WARNING] Some dependencies may not have installed correctly" "Yellow"
        }
    }
    catch {
        Write-ColorOutput "[WARNING] Could not install dependencies: $($_.Exception.Message)" "Yellow"
    }
} else {
    Write-ColorOutput "[WARNING] $RequirementsFile not found" "Yellow"
}

# Check if port is already in use
if (Test-PortInUse -Port $Port) {
    Write-ColorOutput "[WARNING] Port $Port is already in use" "Yellow"
    $choice = Read-Host "Do you want to kill the existing process and restart? (y/N)"
    if ($choice -match '^[Yy]$') {
        Stop-ProcessOnPort -Port $Port
    } else {
        Write-ColorOutput "[INFO] Startup cancelled" "Red"
        Read-Host "Press Enter to exit"
        exit 1
    }
}

# Load and validate environment variables
Write-ColorOutput "[INFO] Loading environment variables..." "Blue"
$envVars = Read-EnvFile -FilePath $EnvFile

# Set environment variables for current session
foreach ($key in $envVars.Keys) {
    [Environment]::SetEnvironmentVariable($key, $envVars[$key], "Process")
}

# Check if GEMINI_API_KEY is set
if (-not $envVars.ContainsKey("GEMINI_API_KEY") -or 
    [string]::IsNullOrEmpty($envVars["GEMINI_API_KEY"]) -or 
    $envVars["GEMINI_API_KEY"] -eq "your-api-key-here") {
    Write-ColorOutput "[ERROR] GEMINI_API_KEY is not properly configured in $EnvFile" "Red"
    Write-ColorOutput "[WARNING] Please set a valid Google Gemini API key" "Yellow"
    Read-Host "Press Enter to exit"
    exit 1
}

Write-ColorOutput "[SUCCESS] Environment configuration validated" "Green"
Write-ColorOutput "" "White"

# Find Python installation
$pythonCmd = Test-PythonInstallation
if (-not $pythonCmd) {
    Write-ColorOutput "[ERROR] Python not found in PATH" "Red"
    Write-ColorOutput "[WARNING] Please install Python or add it to your PATH" "Yellow"
    Read-Host "Press Enter to exit"
    exit 1
}

Write-ColorOutput "[SUCCESS] Using Python command: $pythonCmd" "Green"

# Start the API server
Write-ColorOutput "[INFO] Starting Nephro API Backend Service..." "Blue"
Write-ColorOutput "[INFO] Host: $Host" "Blue"
Write-ColorOutput "[INFO] Port: $Port" "Blue"
Write-ColorOutput "[INFO] API File: $ApiFile" "Blue"
Write-ColorOutput "" "White"
Write-ColorOutput "=============== API Server Output ===============" "Yellow"

try {
    if ($Direct) {
        Write-ColorOutput "[INFO] Starting with direct Python execution..." "Blue"
        & $pythonCmd $ApiFile
    } else {
        # Try to use uvicorn (recommended)
        try {
            uvicorn --version | Out-Null
            Write-ColorOutput "[INFO] Starting with uvicorn (recommended)..." "Blue"
            uvicorn nephro_api:app --host $Host --port $Port --reload
        }
        catch {
            Write-ColorOutput "[WARNING] uvicorn not found, installing..." "Yellow"
            try {
                pip install uvicorn --quiet
                Write-ColorOutput "[INFO] Starting with uvicorn..." "Blue"
                uvicorn nephro_api:app --host $Host --port $Port --reload
            }
            catch {
                Write-ColorOutput "[WARNING] Failed to install uvicorn, using direct Python execution..." "Yellow"
                & $pythonCmd $ApiFile
            }
        }
    }
}
catch {
    Write-ColorOutput "[ERROR] Failed to start server: $($_.Exception.Message)" "Red"
}
finally {
    Write-ColorOutput "" "White"
    Write-ColorOutput "[INFO] Server has stopped" "Blue"
    Read-Host "Press Enter to exit"
}