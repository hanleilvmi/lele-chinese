# -*- coding: utf-8 -*-
"""
TTS测试入口 - 用于调试语音问题
临时使用：将buildozer.spec中的source.main改为main_test_tts.py
"""
import os
import sys

app_dir = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, app_dir)
sys.path.insert(0, os.path.join(app_dir, 'ui_kivy'))
sys.path.insert(0, os.path.join(app_dir, 'core'))

os.environ['KIVY_NO_FILELOG'] = '1'

if __name__ == '__main__':
    from ui_kivy.test_tts import TTSTestApp
    TTSTestApp().run()
