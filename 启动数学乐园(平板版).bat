@echo off
chcp 65001 >nul
echo 正在启动乐乐数学乐园...
cd /d "%~dp0"
python ui_kivy/math_app.py
pause
