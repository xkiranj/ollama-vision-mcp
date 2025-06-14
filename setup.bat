@echo off
echo ====================================
echo Ollama Vision MCP Setup (Windows)
echo ====================================
echo.

REM Check if Python is installed
python --version >nul 2>&1
if errorlevel 1 (
    echo ERROR: Python is not installed or not in PATH
    echo Please install Python 3.8+ from https://python.org
    pause
    exit /b 1
)

echo [1/5] Creating virtual environment...
python -m venv venv
if errorlevel 1 (
    echo ERROR: Failed to create virtual environment
    pause
    exit /b 1
)

echo [2/5] Activating virtual environment...
call venv\Scripts\activate.bat

echo [3/5] Upgrading pip...
python -m pip install --upgrade pip

echo [4/5] Installing dependencies...
pip install -r requirements.txt
if errorlevel 1 (
    echo ERROR: Failed to install dependencies
    pause
    exit /b 1
)

echo [5/5] Installing package in development mode...
pip install -e .
if errorlevel 1 (
    echo WARNING: Failed to install in development mode
    echo Continuing with basic installation...
)

echo.
echo ====================================
echo Setup Complete!
echo ====================================
echo.
echo Virtual environment created at: %CD%\venv
echo.
echo To use this server:
echo 1. Make sure Ollama is running: ollama serve
echo 2. Pull a vision model: ollama pull llava-phi3
echo 3. Configure your MCP client with:
echo    Command: %CD%\venv\Scripts\python.exe
echo    Args: -m src.server
echo    CWD: %CD%
echo.
echo To activate the virtual environment manually:
echo    venv\Scripts\activate
echo.
pause
