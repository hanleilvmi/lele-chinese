# -*- coding: utf-8 -*-
"""测试测验页面"""
import sys
sys.path.insert(0, 'ui_kivy')
sys.path.insert(0, '.')

from kivy.app import App
from kivy.uix.screenmanager import ScreenManager
from kivy.core.window import Window

Window.size = (1280, 800)

from chinese_app import ChineseQuizScreen, ChineseMenuScreen, init_audio

class TestApp(App):
    def build(self):
        # 初始化音频
        init_audio()
        
        sm = ScreenManager()
        sm.add_widget(ChineseMenuScreen(name='chinese_menu'))
        sm.add_widget(ChineseQuizScreen(name='chinese_quiz'))
        sm.current = 'chinese_quiz'
        return sm

if __name__ == '__main__':
    TestApp().run()
