# -*- coding: utf-8 -*-
"""
乐乐的识字乐园 - Android APK 入口文件
"""
import os
import sys

# 确保能找到模块
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

# 导入并运行应用
from ui_kivy.chinese_app import ChineseLearnApp

if __name__ == '__main__':
    ChineseLearnApp().run()
