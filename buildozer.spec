[app]
title = 乐乐的识字乐园
package.name = lelehanzi
package.domain = com.lele

source.dir = .
source.include_exts = py,png,jpg,jpeg,kv,atlas,json,ttc,ttf
source.include_patterns = 汪汪队图片/*,core/*,ui_kivy/*
source.exclude_patterns = backup_*,build,dist,__pycache__,.git,.github,*.pyc,*.pyo
source.main = main.py

version = 1.2.0

# 应用图标 (莱德)
icon.filename = icon.png

requirements = python3,kivy,pyjnius

android.permissions = INTERNET

android.api = 33
android.minapi = 21
android.ndk = 25b
android.sdk = 33

orientation = landscape
fullscreen = 1

android.archs = arm64-v8a,armeabi-v7a

android.accept_sdk_license = True
android.allow_backup = True

[buildozer]
log_level = 2
warn_on_root = 1
