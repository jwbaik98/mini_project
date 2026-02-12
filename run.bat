@echo off
title Library Installer and Server Launcher
color 0e

echo ========================================================
echo   PHASE 1: INSTALLING MISSING LIBRARIES
echo ========================================================

:: 1. 가상환경 활성화
set PYTHON_EXE=C:\ProgramData\anaconda3\envs\py310\python.exe


:: 2. 필요한 환경 설치
echo [+] Installing/Updating required packages...
"%PYTHON_EXE%" -m pip install flask opencv-python ultralytics shapely numpy

echo.
echo ========================================================
echo   PHASE 2: STARTING FLASK SERVER
echo ========================================================

:: 3. Flask 서버를 백그라운드에서 실행 준비
echo [+] Starting Flask Server (app.py)...
start /b "" "%PYTHON_EXE%" app.py

:: 4. 서버가 뜰 때까지 잠시 대기 (5초)
echo [+] Waiting 5 seconds for the server to stabilize...
timeout /t 5 /nobreak > nul

:: 5. 브라우저 자동 실행
echo [+] Opening Dashboard: http://127.0.0.1:5000
start http://127.0.0.1:5000

echo.
echo [+] Setup Complete! Keep this window open.
pause