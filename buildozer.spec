[app]
title = 乐乐的识字乐园
package.name = lelehanzi
package.domain = com.lele

source.dir = .
source.include_exts = py,png,jpg,jpeg,kv,atlas,json,ttc,ttf,mp3
source.include_patterns = 汪汪队图片/*,core/*,ui_kivy/*,audio/generated/*
source.exclude_patterns = backup_*,build,dist,__pycache__,.git,.github,*.pyc,*.pyo
source.main = main.py

version = 1.8.0

# 应用图标 (莱德)
icon.filename = icon.png

# 启动画面 - 使用纯色背景，避免图片拉伸问题
# presplash.filename = 汪汪队图片/多个狗狗.jpg

# 依赖：添加pyjnius用于Android TTS
requirements = python3,kivy,pyjnius

# 权限：添加存储权限用于保存学习进度
android.permissions = INTERNET,WRITE_EXTERNAL_STORAGE,READ_EXTERNAL_STORAGE

android.api = 33
android.minapi = 21
android.ndk = 25b
android.sdk = 33

orientation = landscape
fullscreen = 1

# 支持的CPU架构
android.archs = arm64-v8a,armeabi-v7a

android.accept_sdk_license = True
android.allow_backup = True

[buildozer]
log_level = 2
warn_on_root = 1
