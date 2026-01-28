# -*- coding: utf-8 -*-
"""
字体配置模块 - 支持Android/鸿蒙系统
"""
import os
from kivy.core.text import LabelBase
from kivy.utils import platform

# 中文字体路径列表（按优先级排序）
FONT_PATHS = {
    'android': [
        # 鸿蒙系统字体（优先）
        "/system/fonts/HarmonyOS_Sans_SC_Regular.ttf",
        "/system/fonts/HarmonyOS_Sans_SC.ttf",
        "/system/fonts/HarmonyOSSans-Regular.ttf",
        # 华为设备字体
        "/system/fonts/HwChinese-Regular.ttf",
        # 标准Android字体
        "/system/fonts/NotoSansCJK-Regular.ttc",
        "/system/fonts/NotoSansSC-Regular.otf",
        "/system/fonts/DroidSansFallback.ttf",
        "/system/fonts/DroidSansChinese.ttf",
    ],
    'win': [
        "C:/Windows/Fonts/msyh.ttc",
        "C:/Windows/Fonts/msyh.ttf",
        "C:/Windows/Fonts/simhei.ttf",
    ],
    'linux': [
        "/usr/share/fonts/truetype/noto/NotoSansCJK-Regular.ttc",
        "/usr/share/fonts/opentype/noto/NotoSansCJK-Regular.ttc",
    ],
    'macosx': [
        "/System/Library/Fonts/PingFang.ttc",
        "/System/Library/Fonts/STHeiti Light.ttc",
    ]
}

_font_loaded = False

def setup_fonts():
    """配置中文字体"""
    global _font_loaded
    if _font_loaded:
        return True
    
    # 获取当前平台的字体列表
    paths = FONT_PATHS.get(platform, FONT_PATHS.get('linux', []))
    
    for path in paths:
        if os.path.exists(path):
            try:
                LabelBase.register(name='Roboto', fn_regular=path)
                print(f"[font_config] 已加载字体: {path}")
                _font_loaded = True
                return True
            except Exception as e:
                print(f"[font_config] 加载字体失败 {path}: {e}")
    
    print("[font_config] 警告: 未找到中文字体，使用系统默认")
    return False

def get_font_path():
    """获取已加载的字体路径"""
    paths = FONT_PATHS.get(platform, [])
    for path in paths:
        if os.path.exists(path):
            return path
    return None

# 模块加载时自动配置字体
setup_fonts()
