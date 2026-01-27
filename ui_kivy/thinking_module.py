# -*- coding: utf-8 -*-
"""
Kivy 思维乐园模块
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

from core.data_thinking import ThinkingData
from core.game_logic import GameLogic, GameType

Window.size = (900, 700)


class ThinkingMenuScreen(Screen):
    """思维乐园菜单"""
    
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        layout = BoxLayout(orientation='vertical', padding=20, spacing=15)
        
        with layout.canvas.before:
            Color(*get_color_from_hex('#F3E5F5'))
            self.bg = Rectangle(pos=layout.pos, size=layout.size)
        layout.bind(pos=lambda i,v: setattr(self.bg, 'pos', v),
                   size=lambda i,v: setattr(self.bg, 'size', v))
        
        # 导航栏
        nav = BoxLayout(size_hint=(1, 0.1))
        back_btn = Button(text='< 返回', size_hint=(0.2, 1), font_size='16sp',
                         background_color=get_color_from_hex('#AB47BC'), background_normal='')
        back_btn.bind(on_press=self.go_back)
        nav.add_widget(back_btn)
        nav.add_widget(Label(text='【思维乐园】', font_size='28sp',
                            color=get_color_from_hex('#6A1B9A'), bold=True, size_hint=(0.6, 1)))
        nav.add_widget(Label(text='', size_hint=(0.2, 1)))
        layout.add_widget(nav)
        
        # 游戏选择
        games = GridLayout(cols=2, spacing=15, size_hint=(1, 0.75), padding=20)
        game_list = [
            ('?', '找不同', '哪个不一样', '#AB47BC', lambda: self.go_game('different')),
            ('...', '找规律', '下一个是什么', '#7E57C2', lambda: self.go_game('pattern')),
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
        if game_name == 'different':
            self.manager.current = 'find_different'
        elif game_name == 'pattern':
            self.manager.current = 'find_pattern'


class FindDifferentScreen(Screen):
    """找不同游戏"""
    
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.logic = GameLogic()
        self.session = None
        self.correct_idx = None
        self.build_ui()
    
    def build_ui(self):
        layout = BoxLayout(orientation='vertical', padding=20, spacing=15)
        with layout.canvas.before:
            Color(*get_color_from_hex('#EDE7F6'))
            self.bg = Rectangle(pos=layout.pos, size=layout.size)
        layout.bind(pos=lambda i,v: setattr(self.bg, 'pos', v),
                   size=lambda i,v: setattr(self.bg, 'size', v))
        
        # 导航栏
        nav = BoxLayout(size_hint=(1, 0.1))
        back_btn = Button(text='< 返回', size_hint=(0.15, 1), font_size='16sp',
                         background_color=get_color_from_hex('#AB47BC'), background_normal='')
        back_btn.bind(on_press=lambda x: setattr(self.manager, 'current', 'thinking_menu'))
        nav.add_widget(back_btn)
        nav.add_widget(Label(text='【找不同】', font_size='24sp',
                            color=get_color_from_hex('#6A1B9A'), bold=True, size_hint=(0.55, 1)))
        self.score_label = Label(text='得分: 0', font_size='18sp',
                                color=get_color_from_hex('#FF6B6B'), size_hint=(0.15, 1))
        nav.add_widget(self.score_label)
        self.progress_label = Label(text='0/10', font_size='16sp',
                                   color=get_color_from_hex('#666666'), size_hint=(0.15, 1))
        nav.add_widget(self.progress_label)
        layout.add_widget(nav)
        
        # 题目
        self.question_label = Label(text='哪个和其他不一样？点击它！', font_size='24sp',
                                   color=get_color_from_hex('#333333'), size_hint=(1, 0.1))
        layout.add_widget(self.question_label)
        
        # 选项区
        self.items_layout = GridLayout(cols=4, spacing=20, padding=40, size_hint=(1, 0.4))
        layout.add_widget(self.items_layout)
        
        # 反馈
        self.feedback_label = Label(text='', font_size='24sp',
                                   color=get_color_from_hex('#4CAF50'), size_hint=(1, 0.15))
        layout.add_widget(self.feedback_label)
        
        # 开始按钮
        self.start_btn = Button(text='开始游戏', font_size='20sp', size_hint=(1, 0.12),
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
        
        # 用简单字符代替emoji
        shapes = ['O', 'X', '+', '*', '#', '@', '&', '%']
        base = random.choice(shapes)
        items = [base] * 4
        self.correct_idx = random.randint(0, 3)
        different = random.choice([s for s in shapes if s != base])
        items[self.correct_idx] = different
        
        self.items_layout.clear_widgets()
        for i, item in enumerate(items):
            btn = Button(text=item, font_size='60sp',
                        background_color=get_color_from_hex('#CE93D8'), background_normal='')
            btn.idx = i
            btn.bind(on_press=self.on_answer)
            self.items_layout.add_widget(btn)
        
        self.progress_label.text = f'{self.session.current_question + 1}/10'
    
    def on_answer(self, instance):
        if self.correct_idx is None:
            return
        
        is_correct = self.logic.check_answer(self.session, instance.idx, self.correct_idx)
        
        if is_correct:
            self.feedback_label.text = '太棒了！找对了！'
            self.feedback_label.color = get_color_from_hex('#4CAF50')
        else:
            self.feedback_label.text = '错了，再仔细看看'
            self.feedback_label.color = get_color_from_hex('#F44336')
        
        self.score_label.text = f'得分: {self.session.score}'
        
        for btn in self.items_layout.children:
            btn.disabled = True
        
        Clock.schedule_once(lambda dt: self.next_question(), 1.5)
    
    def show_result(self):
        stars = self.logic.calculate_stars(self.session)
        praise = self.logic.get_praise_message(self.session.accuracy)
        star_text = '★' * stars + '☆' * (3 - stars)
        self.question_label.text = f'{star_text} 游戏完成！'
        self.feedback_label.text = f'{praise}\n正确率: {self.session.accuracy*100:.0f}%'


class FindPatternScreen(Screen):
    """找规律游戏"""
    
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.logic = GameLogic()
        self.session = None
        self.correct_answer = None
        self.build_ui()
    
    def build_ui(self):
        layout = BoxLayout(orientation='vertical', padding=20, spacing=15)
        with layout.canvas.before:
            Color(*get_color_from_hex('#E8EAF6'))
            self.bg = Rectangle(pos=layout.pos, size=layout.size)
        layout.bind(pos=lambda i,v: setattr(self.bg, 'pos', v),
                   size=lambda i,v: setattr(self.bg, 'size', v))
        
        # 导航栏
        nav = BoxLayout(size_hint=(1, 0.1))
        back_btn = Button(text='< 返回', size_hint=(0.15, 1), font_size='16sp',
                         background_color=get_color_from_hex('#7E57C2'), background_normal='')
        back_btn.bind(on_press=lambda x: setattr(self.manager, 'current', 'thinking_menu'))
        nav.add_widget(back_btn)
        nav.add_widget(Label(text='【找规律】', font_size='24sp',
                            color=get_color_from_hex('#4527A0'), bold=True, size_hint=(0.55, 1)))
        self.score_label = Label(text='得分: 0', font_size='18sp',
                                color=get_color_from_hex('#FF6B6B'), size_hint=(0.15, 1))
        nav.add_widget(self.score_label)
        self.progress_label = Label(text='0/10', font_size='16sp',
                                   color=get_color_from_hex('#666666'), size_hint=(0.15, 1))
        nav.add_widget(self.progress_label)
        layout.add_widget(nav)
        
        # 题目
        self.question_label = Label(text='下一个是什么？', font_size='24sp',
                                   color=get_color_from_hex('#333333'), size_hint=(1, 0.1))
        layout.add_widget(self.question_label)
        
        # 规律显示
        self.pattern_label = Label(text='? ? ? ?', font_size='48sp',
                                  color=get_color_from_hex('#5E35B1'), size_hint=(1, 0.25))
        layout.add_widget(self.pattern_label)
        
        # 反馈
        self.feedback_label = Label(text='', font_size='24sp',
                                   color=get_color_from_hex('#4CAF50'), size_hint=(1, 0.1))
        layout.add_widget(self.feedback_label)
        
        # 选项
        self.answers_layout = GridLayout(cols=4, spacing=15, padding=20, size_hint=(1, 0.25))
        layout.add_widget(self.answers_layout)
        
        # 开始按钮
        self.start_btn = Button(text='开始游戏', font_size='20sp', size_hint=(1, 0.12),
                               background_color=get_color_from_hex('#FF9800'), background_normal='')
        self.start_btn.bind(on_press=self.start_game)
        layout.add_widget(self.start_btn)
        
        self.add_widget(layout)
    
    def start_game(self, instance):
        self.session = self.logic.create_session(GameType.PATTERN, total_questions=10)
        self.score_label.text = '得分: 0'
        self.feedback_label.text = ''
        self.start_btn.text = '重新开始'
        self.next_question()
    
    def next_question(self):
        if self.session.is_complete():
            self.show_result()
            return
        
        # 简单AB规律
        shapes = ['O', 'X', '+', '*', '#', '@']
        a, b = random.sample(shapes, 2)
        pattern = [a, b, a, b]
        self.correct_answer = a  # 下一个是a
        
        self.pattern_label.text = '  '.join(pattern) + '  ?'
        
        # 生成选项
        self.answers_layout.clear_widgets()
        options = random.sample(shapes, 4)
        if self.correct_answer not in options:
            options[0] = self.correct_answer
        random.shuffle(options)
        
        for opt in options:
            btn = Button(text=opt, font_size='36sp',
                        background_color=get_color_from_hex('#9575CD'), background_normal='')
            btn.bind(on_press=self.on_answer)
            self.answers_layout.add_widget(btn)
        
        self.progress_label.text = f'{self.session.current_question + 1}/10'
    
    def on_answer(self, instance):
        if self.correct_answer is None:
            return
        
        is_correct = self.logic.check_answer(self.session, instance.text, self.correct_answer)
        
        if is_correct:
            self.feedback_label.text = f'太棒了！下一个是 {self.correct_answer}'
            self.feedback_label.color = get_color_from_hex('#4CAF50')
        else:
            self.feedback_label.text = f'错了，正确答案是 {self.correct_answer}'
            self.feedback_label.color = get_color_from_hex('#F44336')
        
        self.score_label.text = f'得分: {self.session.score}'
        
        for btn in self.answers_layout.children:
            btn.disabled = True
        
        Clock.schedule_once(lambda dt: self.next_question(), 1.5)
    
    def show_result(self):
        stars = self.logic.calculate_stars(self.session)
        praise = self.logic.get_praise_message(self.session.accuracy)
        star_text = '★' * stars + '☆' * (3 - stars)
        self.question_label.text = f'{star_text} 游戏完成！'
        self.pattern_label.text = '棒！'
        self.feedback_label.text = f'{praise}\n正确率: {self.session.accuracy*100:.0f}%'


class ThinkingApp(App):
    def build(self):
        self.title = '乐乐的思维乐园 - Kivy版'
        sm = ScreenManager()
        sm.add_widget(ThinkingMenuScreen(name='thinking_menu'))
        sm.add_widget(FindDifferentScreen(name='find_different'))
        sm.add_widget(FindPatternScreen(name='find_pattern'))
        return sm


if __name__ == '__main__':
    ThinkingApp().run()
