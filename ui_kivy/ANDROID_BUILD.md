# 🐕 乐乐的识字乐园 - Android 打包指南

## 快速开始（推荐方法）

### 第一步：准备打包文件

在电脑上运行打包脚本：
```
python pack_for_android.py
```

这会生成 `lele_chinese.zip` 文件（约26KB）。

### 第二步：使用 Google Colab 编译

1. 打开 Google Colab: https://colab.research.google.com/

2. 上传 `build_android_colab.ipynb` 文件，或者新建笔记本

3. 按顺序运行代码块：
   - 步骤1：安装编译工具
   - 步骤2：上传 `lele_chinese.zip`
   - 步骤3：解压项目
   - 步骤4：编译APK（约30分钟）
   - 步骤5：下载APK

4. 下载生成的APK文件

### 第三步：安装到平板

1. 将APK传输到平板（微信/QQ/USB都可以）
2. 在平板上点击APK文件
3. 如果提示"未知来源"，去设置中允许
4. 安装完成后打开应用

### 第四步：设置语音

应用使用Android系统TTS，需要安装中文语音：

1. 打开平板 **设置**
2. 找到 **语言和输入法** → **文字转语音**
3. 点击 **安装中文语音包**
4. 设置默认语音为中文

---

## 备选方法：本地Linux环境

如果你有Linux电脑或WSL，可以本地编译：

### 安装依赖
```bash
sudo apt-get update
sudo apt-get install -y \
    python3-pip build-essential git python3 python3-dev \
    ffmpeg libsdl2-dev libsdl2-image-dev libsdl2-mixer-dev libsdl2-ttf-dev \
    libportmidi-dev libswscale-dev libavformat-dev libavcodec-dev zlib1g-dev \
    openjdk-17-jdk

pip3 install buildozer cython
```

### 编译
```bash
cd 乐乐的学习乐园
buildozer -v android debug -c buildozer_chinese.spec
```

### 安装
```bash
adb install bin/lelehanzi-1.0.0-arm64-v8a-debug.apk
```

---

## 常见问题

### Q: 首次编译很慢？
A: 正常，需要下载Android SDK/NDK（约2GB），之后会快很多。

### Q: Colab编译失败？
A: 
- 重新运行编译步骤
- 检查是否有网络错误
- 尝试重启Colab运行时

### Q: APK安装失败？
A:
- 允许安装未知来源应用
- 确保Android版本 >= 5.0

### Q: 语音不工作？
A:
- 安装中文TTS语音包
- 检查系统TTS设置

### Q: 应用闪退？
A:
- 检查Android版本
- 查看logcat日志

---

## 技术信息

- 目标API: Android 13 (API 33)
- 最低版本: Android 5.0 (API 21)
- 架构: arm64-v8a, armeabi-v7a
- 屏幕: 横屏模式，适合平板
