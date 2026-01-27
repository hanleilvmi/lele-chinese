@echo off
chcp 65001 >nul
title 乐乐的识字乐园
cd /d "%~dp0"
python ui_kivy/chinese_app.py
pause
