# -*- coding: utf-8 -*-
"""
Kivy 识字乐园模块
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
from kivy.uix.screenmanager import ScreenManager, Screen
from kivy.graphics import Color, Rectangle
from kivy.core.window import Window
from kivy.utils import get_color_from_hex
from kivy.clock import Clock
import random

from core.data_chinese import ChineseData
from core.game_logic import GameLogic, GameType

Window.size = (900, 700)


class ChineseMenuScreen(Screen):
    """识字乐园菜单"""
    
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        layout = BoxLayout(orientation='vertical', padding=20, spacing=15)
        
        with layout.canvas.before:
            Color(*get_color_from_hex('#FFF8E1'))
            self.bg = Rectangle(pos=layout.pos, size=layout.size)
        layout.bind(pos=lambda i,v: setattr(self.bg, 'pos', v),
                   size=lambda i,v: setattr(self.bg, 'size', v))
        
        # 导航栏
        nav = BoxLayout(size_hint=(1, 0.1))
        back_btn = Button(text='< 返回', size_hint=(0.2, 1), font_size='16sp',
                         background_color=get_color_from_hex('#FFA726'), background_normal='')
        back_btn.bind(on_press=self.go_back)
        nav.add_widget(back_btn)
        nav.add_widget(Label(text='【识字乐园】', font_size='28sp',
                            color=get_color_from_hex('#E65100'), bold=True, size_hint=(0.6, 1)))
        nav.add_widget(Label(text='', size_hint=(0.2, 1)))
        layout.add_widget(nav)
        
        # 游戏选择
        games = GridLayout(cols=2, spacing=15, size_hint=(1, 0.75), padding=20)
        game_list = [
            ('字', '学汉字', '基础汉字', '#FF7043', lambda: self.go_game('learn')),
            ('?', '汉字测验', '考考你', '#66BB6A', lambda: self.go_game('quiz')),
        ]
        for icon, title, desc, color, cb in game_list:
            btn = Button(background_normal='', background_color=get_color_from_hex(color))
            btn.markup = True
            btn.text = f'[size=48]{icon}[/size]\n\n[b]{title}[/b]\n[size=12]{desc}[/size]'
            btn.bind(on_press=lambda x, c=cb: c())
            games.add_widget(btn)
        layout.add_widget(games)
        self.add_widget(layout)
    
    def go_back(self, instance):
        if 'main' in [s.name for s in self.manager.screens]:
            self.manager.current = 'main'
    
    def go_game(self, game_name):
        if game_name == 'learn':
            self.manager.current = 'chinese_learn'
        elif game_name == 'quiz':
            self.manager.current = 'chinese_quiz'


class ChineseLearnScreen(Screen):
    """学汉字"""
    
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.build_ui()
    
    def build_ui(self):
        layout = BoxLayout(orientation='vertical', padding=20, spacing=10)
        with layout.canvas.before:
            Color(*get_color_from_hex('#FFF3E0'))
            self.bg = Rectangle(pos=layout.pos, size=layout.size)
        layout.bind(pos=lambda i,v: setattr(self.bg, 'pos', v),
                   size=lambda i,v: setattr(self.bg, 'size', v))
        
        # 导航栏
        nav = BoxLayout(size_hint=(1, 0.1))
        back_btn = Button(text='< 返回', size_hint=(0.15, 1), font_size='16sp',
                         background_color=get_color_from_hex('#FF7043'), background_normal='')
        back_btn.bind(on_press=lambda x: setattr(self.manager, 'current', 'chinese_menu'))
        nav.add_widget(back_btn)
        nav.add_widget(Label(text='【学汉字】', font_size='24sp',
                            color=get_color_from_hex('#E65100'), bold=True, size_hint=(0.7, 1)))
        nav.add_widget(Label(text='', size_hint=(0.15, 1)))
        layout.add_widget(nav)
        
        # 提示
        self.hint = Label(text='点击卡片学习汉字！', font_size='18sp',
                         color=get_color_from_hex('#666666'), size_hint=(1, 0.08))
        layout.add_widget(self.hint)
        
        # 汉字卡片
        grid = GridLayout(cols=4, spacing=12, padding=10, size_hint=(1, 0.72))
        words = ChineseData.get_words(level=1)
        colors = ['#FF6B6B', '#4ECDC4', '#45B7D1', '#96CEB4', '#DDA0DD', '#FFD93D',
                  '#FF9800', '#8BC34A', '#E91E63', '#9C27B0', '#00BCD4', '#CDDC39']
        
        for i, (char, pinyin, word, emoji) in enumerate(words):
            btn = Button(background_normal='', background_color=get_color_from_hex(colors[i % len(colors)]))
            btn.markup = True
            btn.text = f'[size=48][b]{char}[/b][/size]\n[size=18]{pinyin}[/size]\n[size=14]{word}[/size]'
            btn.char_data = (char, pinyin, word)
            btn.bind(on_press=self.on_card_press)
            grid.add_widget(btn)
        
        layout.add_widget(grid)
        self.add_widget(layout)
    
    def on_card_press(self, instance):
        if hasattr(instance, 'char_data'):
            char, pinyin, word = instance.char_data
            self.hint.text = f'"{char}" 读作 {pinyin}，组词：{word}'


class ChineseQuizScreen(Screen):
    """汉字测验"""
    
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.logic = GameLogic()
        self.session = None
        self.current_word = None
        self.build_ui()
    
    def build_ui(self):
        layout = BoxLayout(orientation='vertical', padding=20, spacing=15)
        with layout.canvas.before:
            Color(*get_color_from_hex('#E8F5E9'))
            self.bg = Rectangle(pos=layout.pos, size=layout.size)
        layout.bind(pos=lambda i,v: setattr(self.bg, 'pos', v),
                   size=lambda i,v: setattr(self.bg, 'size', v))
        
        # 导航栏
        nav = BoxLayout(size_hint=(1, 0.1))
        back_btn = Button(text='< 返回', size_hint=(0.15, 1), font_size='16sp',
                         background_color=get_color_from_hex('#66BB6A'), background_normal='')
        back_btn.bind(on_press=lambda x: setattr(self.manager, 'current', 'chinese_menu'))
        nav.add_widget(back_btn)
        nav.add_widget(Label(text='【汉字测验】', font_size='24sp',
                            color=get_color_from_hex('#2E7D32'), bold=True, size_hint=(0.55, 1)))
        self.score_label = Label(text='得分: 0', font_size='18sp',
                                color=get_color_from_hex('#FF6B6B'), size_hint=(0.15, 1))
        nav.add_widget(self.score_label)
        self.progress_label = Label(text='0/10', font_size='16sp',
                                   color=get_color_from_hex('#666666'), size_hint=(0.15, 1))
        nav.add_widget(self.progress_label)
        layout.add_widget(nav)
        
        # 题目
        self.question_label = Label(text='这个字怎么读？', font_size='24sp',
                                   color=get_color_from_hex('#333333'), size_hint=(1, 0.1))
        layout.add_widget(self.question_label)
        
        # 汉字显示
        self.display_label = Label(text='?', font_size='120sp',
                                  color=get_color_from_hex('#E65100'), size_hint=(1, 0.3))
        layout.add_widget(self.display_label)
        
        # 反馈
        self.feedback_label = Label(text='', font_size='24sp',
                                   color=get_color_from_hex('#4CAF50'), size_hint=(1, 0.1))
        layout.add_widget(self.feedback_label)
        
        # 答案按钮
        self.answers_layout = GridLayout(cols=4, spacing=10, padding=10, size_hint=(1, 0.2))
        layout.add_widget(self.answers_layout)
        
        # 开始按钮
        self.start_btn = Button(text='开始测验', font_size='20sp', size_hint=(1, 0.1),
                               background_color=get_color_from_hex('#FF9800'), background_normal='')
        self.start_btn.bind(on_press=self.start_game)
        layout.add_widget(self.start_btn)
        
        self.add_widget(layout)
    
    def start_game(self, instance):
        self.session = self.logic.create_session(GameType.QUIZ, total_questions=10)
        self.score_label.text = '得分: 0'
        self.feedback_label.text = ''
        self.start_btn.text = '重新开始'
        self.next_question()
    
    def next_question(self):
        if self.session.is_complete():
            self.show_result()
            return
        
        words = ChineseData.get_words(level=1)
        self.current_word = random.choice(words)
        char, pinyin, word, emoji = self.current_word
        
        self.display_label.text = char
        
        # 生成选项
        self.answers_layout.clear_widgets()
        all_pinyin = [w[1] for w in words]
        options = self.logic.get_random_options(pinyin, all_pinyin, count=4)
        
        for opt in options:
            btn = Button(text=opt, font_size='24sp',
                        background_color=get_color_from_hex('#64B5F6'), background_normal='')
            btn.bind(on_press=self.on_answer)
            self.answers_layout.add_widget(btn)
        
        self.progress_label.text = f'{self.session.current_question + 1}/10'
    
    def on_answer(self, instance):
        if self.current_word is None:
            return
        
        user_answer = instance.text
        correct_answer = self.current_word[1]
        
        is_correct = self.logic.check_answer(self.session, user_answer, correct_answer)
        
        if is_correct:
            self.feedback_label.text = f'正确！"{self.current_word[0]}" 读作 {correct_answer}'
            self.feedback_label.color = get_color_from_hex('#4CAF50')
        else:
            self.feedback_label.text = f'错误，正确答案是 {correct_answer}'
            self.feedback_label.color = get_color_from_hex('#F44336')
        
        self.score_label.text = f'得分: {self.session.score}'
        
        for btn in self.answers_layout.children:
            btn.disabled = True
        
        Clock.schedule_once(lambda dt: self.next_question(), 1.5)
    
    def show_result(self):
        stars = self.logic.calculate_stars(self.session)
        praise = self.logic.get_praise_message(self.session.accuracy)
        star_text = '★' * stars + '☆' * (3 - stars)
        self.question_label.text = f'{star_text} 测验完成！'
        self.display_label.text = '棒！'
        self.feedback_label.text = f'{praise}\n正确率: {self.session.accuracy*100:.0f}%'


class ChineseApp(App):
    def build(self):
        self.title = '乐乐的识字乐园 - Kivy版'
        sm = ScreenManager()
        sm.add_widget(ChineseMenuScreen(name='chinese_menu'))
        sm.add_widget(ChineseLearnScreen(name='chinese_learn'))
        sm.add_widget(ChineseQuizScreen(name='chinese_quiz'))
        return sm


if __name__ == '__main__':
    ChineseApp().run()
