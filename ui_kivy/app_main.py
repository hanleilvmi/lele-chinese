# -*- coding: utf-8 -*-
"""
乐乐的学习乐园 - Kivy 主应用
整合所有学习模块
"""
import sys
import os
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

import font_config

from kivy.app import App
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.gridlayout import GridLayout
from kivy.uix.button import Button
from kivy.uix.label import Label
from kivy.uix.screenmanager import ScreenManager, Screen, FadeTransition
from kivy.graphics import Color, Rectangle
from kivy.core.window import Window
from kivy.utils import get_color_from_hex

# 导入所有模块
from math_module import (MathMenuScreen, NumberCardsScreen, AdditionScreen, 
                         CompareScreen, CountGameScreen, ShapesGameScreen, WhackGameScreen)
from pinyin_module import (PinyinMenuScreen, VowelsLearnScreen, ConsonantsLearnScreen, 
                          PinyinQuizScreen, PinyinPictureScreen, PinyinMatchScreen, PinyinWhackScreen)
from english_module import (EnglishMenuScreen, LettersLearnScreen, ColorsLearnScreen, 
                           NumbersLearnScreen, EnglishQuizScreen)
from chinese_module import ChineseMenuScreen, ChineseLearnScreen, ChineseQuizScreen
from thinking_module import ThinkingMenuScreen, FindDifferentScreen, FindPatternScreen
from vehicles_module import (VehiclesMenuScreen, VehiclesLearnScreen, TrafficLightScreen,
                            PawPatrolScreen, VehiclesQuizScreen)

Window.size = (900, 700)


class MainMenuScreen(Screen):
    """主菜单界面"""
    
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        
        layout = BoxLayout(orientation='vertical', padding=20, spacing=15)
        
        with layout.canvas.before:
            Color(*get_color_from_hex('#E3F2FD'))
            self.bg = Rectangle(pos=layout.pos, size=layout.size)
        layout.bind(pos=lambda i,v: setattr(self.bg, 'pos', v),
                   size=lambda i,v: setattr(self.bg, 'size', v))
        
        # 标题
        title_box = BoxLayout(size_hint=(1, 0.12))
        title_box.add_widget(Label(text='乐乐的学习乐园', font_size='32sp',
                                  color=get_color_from_hex('#1976D2'), bold=True))
        layout.add_widget(title_box)
        
        # 副标题
        layout.add_widget(Label(text='汪汪队陪你快乐学习！', font_size='16sp',
                               color=get_color_from_hex('#666666'), size_hint=(1, 0.05)))

        # 游戏选择区
        games_layout = GridLayout(cols=3, spacing=15, size_hint=(1, 0.65), padding=10)
        
        games = [
            ('拼', '拼音乐园', '学拼音', '#FF6B6B', 'pinyin_menu'),
            ('数', '数学乐园', '学数学', '#4ECDC4', 'math_menu'),
            ('ABC', '英语乐园', '学英语', '#45B7D1', 'english_menu'),
            ('脑', '思维乐园', '动脑筋', '#9C27B0', 'thinking_menu'),
            ('字', '识字乐园', '学汉字', '#FF9800', 'chinese_menu'),
            ('车', '交通乐园', '学交通', '#8BC34A', 'vehicles_menu'),
        ]
        
        for icon, title, desc, color, screen in games:
            btn = Button(background_normal='', background_color=get_color_from_hex(color))
            btn.markup = True
            btn.text = f'[size=40]{icon}[/size]\n\n[b]{title}[/b]\n[size=12]{desc}[/size]'
            btn.target_screen = screen
            btn.bind(on_press=self.go_screen)
            games_layout.add_widget(btn)
        
        layout.add_widget(games_layout)
        
        # 底部按钮
        bottom = BoxLayout(size_hint=(1, 0.1), spacing=20, padding=[200, 0])
        
        settings_btn = Button(text='设置', font_size='16sp',
                             background_color=get_color_from_hex('#9E9E9E'), background_normal='')
        bottom.add_widget(settings_btn)
        
        exit_btn = Button(text='退出', font_size='16sp',
                         background_color=get_color_from_hex('#FF6B6B'), background_normal='')
        exit_btn.bind(on_press=self.exit_app)
        bottom.add_widget(exit_btn)
        
        layout.add_widget(bottom)
        self.add_widget(layout)
    
    def go_screen(self, instance):
        if hasattr(instance, 'target_screen'):
            self.manager.current = instance.target_screen
    
    def exit_app(self, instance):
        App.get_running_app().stop()


class LearningApp(App):
    """乐乐的学习乐园主应用"""
    
    def build(self):
        self.title = '乐乐的学习乐园 - Kivy版'
        sm = ScreenManager(transition=FadeTransition())
        
        # 主菜单
        sm.add_widget(MainMenuScreen(name='main'))
        
        # 数学乐园
        sm.add_widget(MathMenuScreen(name='math_menu'))
        sm.add_widget(NumberCardsScreen(name='number_cards'))
        sm.add_widget(AdditionScreen(name='addition'))
        sm.add_widget(CompareScreen(name='compare'))
        sm.add_widget(CountGameScreen(name='count_game'))
        sm.add_widget(ShapesGameScreen(name='shapes_game'))
        sm.add_widget(WhackGameScreen(name='whack_game'))
        
        # 拼音乐园
        sm.add_widget(PinyinMenuScreen(name='pinyin_menu'))
        sm.add_widget(VowelsLearnScreen(name='vowels_learn'))
        sm.add_widget(ConsonantsLearnScreen(name='consonants_learn'))
        sm.add_widget(PinyinQuizScreen(name='pinyin_quiz'))
        sm.add_widget(PinyinPictureScreen(name='pinyin_picture'))
        sm.add_widget(PinyinMatchScreen(name='pinyin_match'))
        sm.add_widget(PinyinWhackScreen(name='pinyin_whack'))
        
        # 英语乐园
        sm.add_widget(EnglishMenuScreen(name='english_menu'))
        sm.add_widget(LettersLearnScreen(name='letters_learn'))
        sm.add_widget(ColorsLearnScreen(name='colors_learn'))
        sm.add_widget(NumbersLearnScreen(name='numbers_learn'))
        sm.add_widget(EnglishQuizScreen(name='english_quiz'))
        
        # 识字乐园
        sm.add_widget(ChineseMenuScreen(name='chinese_menu'))
        sm.add_widget(ChineseLearnScreen(name='chinese_learn'))
        sm.add_widget(ChineseQuizScreen(name='chinese_quiz'))
        
        # 思维乐园
        sm.add_widget(ThinkingMenuScreen(name='thinking_menu'))
        sm.add_widget(FindDifferentScreen(name='find_different'))
        sm.add_widget(FindPatternScreen(name='find_pattern'))
        
        # 交通乐园
        sm.add_widget(VehiclesMenuScreen(name='vehicles_menu'))
        sm.add_widget(VehiclesLearnScreen(name='vehicles_learn'))
        sm.add_widget(TrafficLightScreen(name='traffic_light'))
        sm.add_widget(PawPatrolScreen(name='paw_patrol'))
        sm.add_widget(VehiclesQuizScreen(name='vehicles_quiz'))
        
        return sm


if __name__ == '__main__':
    LearningApp().run()
