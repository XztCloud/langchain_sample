@echo off
chcp 65001 >nul

REM 设置虚拟环境路径（请修改为您的实际路径）
set VENV_PATH=D:\Code\full-stack-fastapi-template\backend\venv

REM 检查虚拟环境是否存在
if not exist "%VENV_PATH%" (
    echo 虚拟环境路径不存在: %VENV_PATH%
    pause
    exit /b 1
)

REM 激活虚拟环境
call "%VENV_PATH%\Scripts\activate.bat"

REM 检查是否激活成功
if errorlevel 1 (
    echo 激活虚拟环境失败
    pause
    exit /b 1
)

REM 启动Jupyter Lab
jupyter-lab.exe

REM 保持窗口打开（可选）
echo Jupyter Lab已关闭
pause