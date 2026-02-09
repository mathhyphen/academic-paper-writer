@echo off
REM Overleaf 自动化配置脚本
REM 设置环境变量（仅在当前窗口有效，不会保存到系统）

echo Setting up Overleaf credentials...

set OVERLEAF_EMAIL=wanghaifeng1991@stu.xjtu.edu.cn
set OVERLEAF_PASSWORD=Whf19910205

echo Credentials set for this session only.
echo.
echo Now you can run:
echo   python full_workflow.py D:\vibe_coding\your_project --auto --name your-paper-name
echo.

REM 保持窗口打开
pause
