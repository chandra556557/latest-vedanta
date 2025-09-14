@echo off
REM Nephro API Backend Service Startup Script (Windows)
REM This script starts the Nephrology AI Agent API server

setlocal enabledelayedexpansion

REM Configuration
set API_PORT=8002
set API_HOST=0.0.0.0
set API_FILE=nephro_api.py
set ENV_FILE=.env
set REQUIREMENTS_FILE=requirements.txt

echo ===============================================
echo    Nephro API Backend Service Startup
echo ===============================================
echo Script Directory: %~dp0
echo Timestamp: %date% %time%
echo.

REM Change to script directory
cd /d "%~dp0"

REM Check if .env file exists
if not exist "%ENV_FILE%" (
    echo [ERROR] %ENV_FILE% file not found!
    echo [WARNING] Please copy .env.example to .env and configure your API keys
    pause
    exit /b 1
)

REM Check if API file exists
if not exist "%API_FILE%" (
    echo [ERROR] %API_FILE% not found!
    pause
    exit /b 1
)

REM Check if requirements file exists and install dependencies
if exist "%REQUIREMENTS_FILE%" (
    echo [INFO] Installing/updating Python dependencies...
    pip install -r "%REQUIREMENTS_FILE%" --quiet
    if !errorlevel! equ 0 (
        echo [SUCCESS] Dependencies installed successfully
    ) else (
        echo [WARNING] Some dependencies may not have installed correctly
    )
) else (
    echo [WARNING] %REQUIREMENTS_FILE% not found
)

REM Check if port is already in use
netstat -an | find ":%API_PORT% " | find "LISTENING" >nul
if !errorlevel! equ 0 (
    echo [WARNING] Port %API_PORT% is already in use
    set /p "choice=Do you want to continue anyway? (y/N): "
    if /i not "!choice!"=="y" (
        echo [INFO] Startup cancelled
        pause
        exit /b 1
    )
)

REM Load and validate environment variables
echo [INFO] Loading environment variables...
for /f "usebackq tokens=1,2 delims==" %%a in ("%ENV_FILE%") do (
    if not "%%a"=="" if not "%%a:~0,1"=="#" (
        set "%%a=%%b"
    )
)

REM Check if GEMINI_API_KEY is set
if "%GEMINI_API_KEY%"=="" (
    echo [ERROR] GEMINI_API_KEY is not set in %ENV_FILE%
    echo [WARNING] Please set a valid Google Gemini API key
    pause
    exit /b 1
)

if "%GEMINI_API_KEY%"=="your-api-key-here" (
    echo [ERROR] GEMINI_API_KEY is not properly configured in %ENV_FILE%
    echo [WARNING] Please set a valid Google Gemini API key
    pause
    exit /b 1
)

echo [SUCCESS] Environment configuration validated
echo.

REM Start the API server
echo [INFO] Starting Nephro API Backend Service...
echo [INFO] Host: %API_HOST%
echo [INFO] Port: %API_PORT%
echo [INFO] API File: %API_FILE%
echo.

REM Check for Python installation
python --version >nul 2>&1
if !errorlevel! equ 0 (
    set PYTHON_CMD=python
) else (
    python3 --version >nul 2>&1
    if !errorlevel! equ 0 (
        set PYTHON_CMD=python3
    ) else (
        echo [ERROR] Python not found in PATH
        echo [WARNING] Please install Python or add it to your PATH
        pause
        exit /b 1
    )
)

echo [SUCCESS] Using Python command: !PYTHON_CMD!
echo [INFO] Starting server...
echo.
echo =============== API Server Output ===============

REM Check if first argument is --direct
if "%1"=="--direct" (
    echo [INFO] Starting with direct Python execution...
    !PYTHON_CMD! "%API_FILE%"
) else (
    REM Try to use uvicorn (recommended)
    uvicorn --version >nul 2>&1
    if !errorlevel! equ 0 (
        echo [INFO] Starting with uvicorn (recommended)...
        uvicorn nephro_api:app --host %API_HOST% --port %API_PORT% --reload
    ) else (
        echo [WARNING] uvicorn not found, installing...
        pip install uvicorn --quiet
        if !errorlevel! equ 0 (
            echo [INFO] Starting with uvicorn...
            uvicorn nephro_api:app --host %API_HOST% --port %API_PORT% --reload
        ) else (
            echo [WARNING] Failed to install uvicorn, using direct Python execution...
            !PYTHON_CMD! "%API_FILE%"
        )
    )
)

REM If we reach here, the server has stopped
echo.
echo [INFO] Server has stopped
pause