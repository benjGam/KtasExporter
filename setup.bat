@echo off
setlocal EnableDelayedExpansion

:: Get script directory
set "SCRIPT_DIR=%~dp0"
set "SCRIPT_DIR=%SCRIPT_DIR:~0,-1%"

:: Create virtual environment if it doesn't exist
if not exist "%SCRIPT_DIR%\venv" (
    echo Creating virtual environment...
    python -m venv "%SCRIPT_DIR%\venv"
)

:: Install dependencies
echo Installing dependencies...
call "%SCRIPT_DIR%\venv\Scripts\pip" install -U selenium python-dotenv bs4

:: Ask for alias creation
echo.
set /p "ADD_ALIAS=Do you want to add 'ktasexport' command to your PATH? [Y/n] "
if /i "!ADD_ALIAS!"=="n" goto :eof

:: Create batch file for the command
set "CMD_FILE=%USERPROFILE%\ktasexport.bat"
(
    echo @echo off
    echo "%SCRIPT_DIR%\run.bat" %%*
) > "%CMD_FILE%"

:: Add command directory to PATH if not already present
for %%I in ("%USERPROFILE%") do set "USER_DIR=%%~fI"
echo !PATH! | findstr /i /c:"!USER_DIR!" >nul
if errorlevel 1 (
    setx PATH "!USER_DIR!;!PATH!"
    echo Added user directory to PATH
)

echo.
echo To use the 'ktasexport' command in this terminal session, please restart your terminal
echo or run: set "PATH=!USER_DIR!;!PATH!"

endlocal 