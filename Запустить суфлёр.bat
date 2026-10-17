@echo off
chcp 65001 >nul
cd /d "%~dp0"
where python >nul 2>nul && (python start_server.py & goto :eof)
where py >nul 2>nul && (py start_server.py & goto :eof)
echo Python не найден. Установите Python с https://www.python.org/downloads/ (галочка "Add Python to PATH") и запустите этот файл снова.
pause
