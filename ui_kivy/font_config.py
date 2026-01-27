# -*- coding: utf-8 -*-
"""
字体配置 - 解决中文显示问题
支持 Windows 和 Android 平台
"""
import os
from kivy.core.text import LabelBase
from kivy.utils import platform

def setup_chinese_font():
    """配置中文字体"""
    font_path = None
    
    if platform == 'android':
        # Android 系统字体路径
        android_fonts = [
            "/system/fonts/NotoSansCJK-Regular.ttc",
            "/system/fonts/DroidSansFallback.ttf",
            "/system/fonts/NotoSansSC-Regular.otf",
            "/system/fonts/DroidSansChinese.ttf",
        ]
        for path in android_fonts:
            if os.path.exists(path):
                font_path = path
                break
    else:
        # Windows 系统字体路径
        windows_fonts = [
            "C:/Windows/Fonts/msyh.ttc",      # 微软雅黑
            "C:/Windows/Fonts/simhei.ttf",    # 黑体
            "C:/Windows/Fonts/simsun.ttc",    # 宋体
        ]
        for path in windows_fonts:
            if os.path.exists(path):
                font_path = path
                break
    
    if font_path:
        # 注册为默认字体
        LabelBase.register(name='Roboto', fn_regular=font_path)
        print(f"已加载中文字体: {font_path}")
        return True
    else:
        print("警告: 未找到中文字体，中文可能无法正常显示")
        return False

# 自动配置
if __name__ != '__main__':
    setup_chinese_font()
