# 乐乐的识字乐园 - Android平板部署指南

## 功能概述

识字模块包含4个游戏：
1. **学汉字** - 卡片学习，支持3个难度等级（36个汉字）
2. **汉字测验** - 选择题模式，根据汉字选拼音
3. **汉字配对** - 记忆配对游戏，汉字和拼音配对
4. **汉字打地鼠** - 快速反应游戏，找到目标汉字

## 平板优化特性

- 大按钮设计，适合儿童触摸操作
- 横屏模式，充分利用平板屏幕
- 动态字体大小，适配不同分辨率
- 中文字体自动检测（Android系统字体）

## 部署步骤

### 1. 安装依赖（Linux/WSL环境）

```bash
pip install buildozer cython
sudo apt install -y git zip unzip openjdk-17-jdk
```

### 2. 编译APK

```bash
# 使用识字模块专用配置
buildozer -v android debug -c buildozer_chinese.spec
```

### 3. 安装到平板

```bash
adb install bin/lelehanzi-1.0.0-debug.apk
```

## 文件结构

```
ui_kivy/
├── chinese_app.py      # 识字模块主程序
├── font_config.py      # 字体配置（支持Android）
core/
├── data_chinese.py     # 汉字数据
├── game_logic.py       # 游戏逻辑
buildozer_chinese.spec  # Android编译配置
```

## 注意事项

1. Android中文字体会自动使用系统字体
2. 首次编译需要下载SDK/NDK，约需30分钟
3. 建议在Linux或WSL2环境下编译
