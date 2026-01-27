[app]
# 应用名称
title = 乐乐的识字乐园

# 包名
package.name = lelehanzi

# 包域名
package.domain = com.lele

# 源代码目录
source.dir = .

# 包含的文件扩展名
source.include_exts = py,png,jpg,kv,atlas,json,ttc,ttf

# 主入口文件
source.main = ui_kivy/chinese_app.py

# 包含的文件/目录
source.include_patterns = ui_kivy/*.py,core/*.py,voice_config_shared.py

# 排除的目录
source.exclude_dirs = tests,bin,build,dist,backup*,__pycache__,.git,.kiro

# 排除的文件模式
source.exclude_patterns = *_test.py,test_*.py,kids_*.py,preview_*.py,pack_*.py,build_*.py,fix_*.py,add_*.py,optimize_*.py,update_*.py,apply_*.py,config_*.py,base_module.py,learning_*.py,word_database.py,theme_*.py,paw_patrol_*.py,ui_config.py

# 应用版本
version = 1.0.0

# 依赖
requirements = python3,kivy,android,pyjnius

# Android 权限
android.permissions = INTERNET

# Android API 版本
android.api = 33
android.minapi = 21
android.ndk = 25b
android.sdk = 33

# 屏幕方向 (landscape=横屏适合平板)
orientation = landscape

# 全屏
fullscreen = 1

# Android 架构
android.archs = arm64-v8a,armeabi-v7a

# 日志级别
log_level = 2

# 警告模式
warn_on_root = 1

# Android 特定设置
android.accept_sdk_license = True
android.allow_backup = True
android.enable_androidx = True

# p4a 分支
p4a.branch = master

[buildozer]
log_level = 2
warn_on_root = 1
