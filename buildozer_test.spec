# Buildozer spec for TTS testing
# 用于调试TTS问题

[app]
title = TTS测试
package.name = ttstest
package.domain = com.lele

source.dir = .
source.include_exts = py,png,jpg,json
source.include_patterns = core/*,ui_kivy/*
source.exclude_patterns = backup_*,build,dist,__pycache__,.git,.github

# 使用测试入口
source.main = main_test_tts.py

version = 1.0.0

requirements = python3,kivy,pyjnius

# 不需要特殊权限
android.permissions = INTERNET

android.api = 33
android.minapi = 21
android.ndk = 25b
android.sdk = 33

orientation = landscape
fullscreen = 1

android.archs = arm64-v8a

android.accept_sdk_license = True

[buildozer]
log_level = 2
warn_on_root = 1
