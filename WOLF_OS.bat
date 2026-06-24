@echo off
title W.O.L.F. STRATEGIC OS
cd /d "%~dp0"
echo [BOOT] INITIALIZING STRATEGIC DEFENSE NETWORK...
echo [BOOT] SYSTEM DIRECTORY: %CD%

:: First, try the user's specific Python path
if exist "C:\Users\djarj\AppData\Local\Programs\Python\Python311\python.exe" (
    "C:\Users\djarj\AppData\Local\Programs\Python\Python311\python.exe" "WOLF_OS.py"
) else (
    echo [BOOT] Python 3.11 path not found. Checking system environment...
    python "WOLF_OS.py"
)

if %ERRORLEVEL% NEQ 0 (
    echo.
    echo [BOOT] Primary launch failed. Retrying with 'py -3'...
    py -3 "WOLF_OS.py"
)

if %ERRORLEVEL% NEQ 0 (
    echo.
    echo [FATAL ERROR] System unable to boot. Traceback above.
)

pause
