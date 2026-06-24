@echo off
title W.O.L.F. DECODER
cd /d "%~dp0"
"C:\Users\djarj\AppData\Local\Programs\Python\Python311\python.exe" "WOLF_DECODER.py"
if %ERRORLEVEL% NEQ 0 (
    python "WOLF_DECODER.py"
)
pause
