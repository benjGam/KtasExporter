@echo off
setlocal EnableDelayedExpansion

:: Get script directory
set "SCRIPT_DIR=%~dp0"
set "SCRIPT_DIR=%SCRIPT_DIR:~0,-1%"
set "VENV_PYTHON=%SCRIPT_DIR%\venv\Scripts\python.exe"

:: Run setup if virtual environment doesn't exist
if not exist "%VENV_PYTHON%" (
    echo Setting up environment...
    call "%SCRIPT_DIR%\setup.bat"
    echo.
    echo Press any key to continue...
    pause >nul
    cls
)

:: Check if Python in virtual environment is executable
if not exist "%VENV_PYTHON%" (
    echo Error: Python in virtual environment is not accessible
    exit /b 1
)

:: Run the main script
"%VENV_PYTHON%" "%SCRIPT_DIR%\src\main.py"

endlocal 