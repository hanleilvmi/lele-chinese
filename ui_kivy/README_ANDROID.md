# Android 打包说明

## 环境准备

### 1. 安装 Buildozer（在 Linux/WSL 中）
```bash
pip install buildozer
pip install cython
```

### 2. 安装依赖（Ubuntu/Debian）
```bash
sudo apt-get install -y \
    python3-pip \
    build-essential \
    git \
    python3 \
    python3-dev \
    ffmpeg \
    libsdl2-dev \
    libsdl2-image-dev \
    libsdl2-mixer-dev \
    libsdl2-ttf-dev \
    libportmidi-dev \
    libswscale-dev \
    libavformat-dev \
    libavcodec-dev \
    zlib1g-dev \
    libgstreamer1.0 \
    gstreamer1.0-plugins-base \
    gstreamer1.0-plugins-good \
    openjdk-11-jdk \
    autoconf \
    automake \
    libtool \
    pkg-config
```

## 打包步骤

### 1. 进入项目目录
```bash
cd /path/to/乐乐的学习乐园
```

### 2. 初始化（首次）
```bash
buildozer init
```

### 3. 编译 APK
```bash
buildozer android debug
```

### 4. 编译并安装到设备
```bash
buildozer android debug deploy run
```

## 常见问题

### Q: 编译失败
A: 检查 buildozer.spec 中的 requirements 是否正确

### Q: 中文显示问题
A: 确保 font_config.py 中配置了正确的字体路径

### Q: 音频不工作
A: Android 需要使用 android.tts 模块

## 文件结构
```
ui_kivy/
├── app_main.py      # 主入口
├── font_config.py   # 字体配置
├── audio_kivy.py    # 音频模块
├── math_module.py   # 数学乐园
├── pinyin_module.py # 拼音乐园
├── english_module.py# 英语乐园
├── chinese_module.py# 识字乐园
├── thinking_module.py# 思维乐园
└── vehicles_module.py# 交通乐园
```
