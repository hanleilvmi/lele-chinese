# -*- coding: utf-8 -*-
"""
Kivy 英语乐园模块
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

from core.data_english import EnglishData
from core.game_logic import GameLogic, GameType

Window.size = (900, 700)


class EnglishMenuScreen(Screen):
    """英语乐园菜单"""
    
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        layout = BoxLayout(orientation='vertical', padding=20, spacing=15)
        
        with layout.canvas.before:
            Color(*get_color_from_hex('#E3F2FD'))
            self.bg = Rectangle(pos=layout.pos, size=layout.size)
        layout.bind(pos=lambda i,v: setattr(self.bg, 'pos', v),
                   size=lambda i,v: setattr(self.bg, 'size', v))
        
        nav = BoxLayout(size_hint=(1, 0.1))
        back_btn = Button(text='< 返回', size_hint=(0.2, 1), font_size='16sp',
                         background_color=get_color_from_hex('#42A5F5'), background_normal='')
        back_btn.bind(on_press=self.go_back)
        nav.add_widget(back_btn)
        nav.add_widget(Label(text='【英语乐园】', font_size='28sp',
                            color=get_color_from_hex('#1565C0'), bold=True, size_hint=(0.6, 1)))
        nav.add_widget(Label(text='', size_hint=(0.2, 1)))
        layout.add_widget(nav)
        
        games = GridLayout(cols=3, spacing=15, size_hint=(1, 0.75), padding=20)
        game_list = [
            ('ABC', '学字母', '26个字母', '#42A5F5', lambda: self.go_game('letters')),
            ('色', '学颜色', '10种颜色', '#66BB6A', lambda: self.go_game('colors')),
            ('123', '学数字', '1-10', '#FFA726', lambda: self.go_game('numbers')),
            ('动物', '动物英语', '学动物', '#96CEB4', lambda: self.go_game('animals')),
            ('听', '听音选词', '听声音', '#DDA0DD', lambda: self.go_game('listen')),
            ('锤', '英语打地鼠', '快反应', '#FFD93D', lambda: self.go_game('whack')),
        ]
        for icon, title, desc, color, cb in game_list:
            btn = Button(background_normal='', background_color=get_color_from_hex(color))
            btn.markup = True
            btn.text = f'[size=32]{icon}[/size]\n\n[b]{title}[/b]\n[size=12]{desc}[/size]'
            btn.bind(on_press=lambda x, c=cb: c())
            games.add_widget(btn)
        layout.add_widget(games)
        self.add_widget(layout)
    
    def go_back(self, instance):
        if 'main' in [s.name for s in self.manager.screens]:
            self.manager.current = 'main'
    
    def go_game(self, game_name):
        screens = {
            'letters': 'letters_learn',
            'colors': 'colors_learn',
            'numbers': 'numbers_learn',
            'animals': 'animals_learn',
            'listen': 'english_listen',
            'whack': 'english_whack',
        }
        if game_name in screens:
            self.manager.current = screens[game_name]


class LettersLearnScreen(Screen):
    """学字母"""
    
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.build_ui()
    
    def build_ui(self):
        layout = BoxLayout(orientation='vertical', padding=20, spacing=10)
        with layout.canvas.before:
            Color(*get_color_from_hex('#E3F2FD'))
            self.bg = Rectangle(pos=layout.pos, size=layout.size)
        layout.bind(pos=lambda i,v: setattr(self.bg, 'pos', v),
                   size=lambda i,v: setattr(self.bg, 'size', v))
        
        nav = BoxLayout(size_hint=(1, 0.1))
        back_btn = Button(text='< 返回', size_hint=(0.15, 1), font_size='16sp',
                         background_color=get_color_from_hex('#42A5F5'), background_normal='')
        back_btn.bind(on_press=lambda x: setattr(self.manager, 'current', 'english_menu'))
        nav.add_widget(back_btn)
        nav.add_widget(Label(text='【学字母 A-L】', font_size='24sp',
                            color=get_color_from_hex('#1565C0'), bold=True, size_hint=(0.7, 1)))
        nav.add_widget(Label(text='', size_hint=(0.15, 1)))
        layout.add_widget(nav)
        
        self.hint = Label(text='点击卡片学习字母！', font_size='18sp',
                         color=get_color_from_hex('#666666'), size_hint=(1, 0.08))
        layout.add_widget(self.hint)
        
        grid = GridLayout(cols=4, spacing=12, padding=10, size_hint=(1, 0.72))
        letters = EnglishData.get_letters(level=1)
        colors = ['#FF6B6B', '#4ECDC4', '#45B7D1', '#96CEB4', '#DDA0DD', '#FFD93D',
                  '#FF9800', '#8BC34A', '#E91E63', '#9C27B0', '#00BCD4', '#CDDC39']
        
        for i, (upper, lower, word, chinese, emoji) in enumerate(letters):
            btn = Button(background_normal='', background_color=get_color_from_hex(colors[i]))
            btn.markup = True
            btn.text = f'[size=36][b]{upper} {lower}[/b][/size]\n[size=16]{word}[/size]\n[size=14]{chinese}[/size]'
            btn.letter_data = (upper, lower, word, chinese)
            btn.bind(on_press=self.on_card_press)
            grid.add_widget(btn)
        
        layout.add_widget(grid)
        self.add_widget(layout)
    
    def on_card_press(self, instance):
        if hasattr(instance, 'letter_data'):
            upper, lower, word, chinese = instance.letter_data
            self.hint.text = f'{upper} {lower} - {word}（{chinese}）'


class ColorsLearnScreen(Screen):
    """学颜色"""
    
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.build_ui()
    
    def build_ui(self):
        layout = BoxLayout(orientation='vertical', padding=20, spacing=10)
        with layout.canvas.before:
            Color(*get_color_from_hex('#F3E5F5'))
            self.bg = Rectangle(pos=layout.pos, size=layout.size)
        layout.bind(pos=lambda i,v: setattr(self.bg, 'pos', v),
                   size=lambda i,v: setattr(self.bg, 'size', v))
        
        nav = BoxLayout(size_hint=(1, 0.1))
        back_btn = Button(text='< 返回', size_hint=(0.15, 1), font_size='16sp',
                         background_color=get_color_from_hex('#AB47BC'), background_normal='')
        back_btn.bind(on_press=lambda x: setattr(self.manager, 'current', 'english_menu'))
        nav.add_widget(back_btn)
        nav.add_widget(Label(text='【学颜色】', font_size='24sp',
                            color=get_color_from_hex('#6A1B9A'), bold=True, size_hint=(0.7, 1)))
        nav.add_widget(Label(text='', size_hint=(0.15, 1)))
        layout.add_widget(nav)
        
        self.hint = Label(text='点击卡片学习颜色！', font_size='18sp',
                         color=get_color_from_hex('#666666'), size_hint=(1, 0.08))
        layout.add_widget(self.hint)
        
        grid = GridLayout(cols=5, spacing=12, padding=10, size_hint=(1, 0.72))
        colors = EnglishData.get_colors()
        
        for english, chinese, color_code, emoji in colors:
            bg_color = color_code
            if color_code in ['#FFFF00', '#FFFFFF']:
                bg_color = '#CCCCCC' if color_code == '#FFFFFF' else '#FFD700'
            
            btn = Button(background_normal='', background_color=get_color_from_hex(bg_color))
            btn.markup = True
            btn.text = f'[size=20][b]{english}[/b][/size]\n[size=16]{chinese}[/size]'
            btn.color_data = (english, chinese)
            btn.bind(on_press=self.on_card_press)
            grid.add_widget(btn)
        
        layout.add_widget(grid)
        self.add_widget(layout)
    
    def on_card_press(self, instance):
        if hasattr(instance, 'color_data'):
            english, chinese = instance.color_data
            self.hint.text = f'{english} = {chinese}'


class NumbersLearnScreen(Screen):
    """学数字英语"""
    
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
        
        nav = BoxLayout(size_hint=(1, 0.1))
        back_btn = Button(text='< 返回', size_hint=(0.15, 1), font_size='16sp',
                         background_color=get_color_from_hex('#FFA726'), background_normal='')
        back_btn.bind(on_press=lambda x: setattr(self.manager, 'current', 'english_menu'))
        nav.add_widget(back_btn)
        nav.add_widget(Label(text='【学数字】', font_size='24sp',
                            color=get_color_from_hex('#E65100'), bold=True, size_hint=(0.7, 1)))
        nav.add_widget(Label(text='', size_hint=(0.15, 1)))
        layout.add_widget(nav)
        
        self.hint = Label(text='点击卡片学习数字英语！', font_size='18sp',
                         color=get_color_from_hex('#666666'), size_hint=(1, 0.08))
        layout.add_widget(self.hint)
        
        grid = GridLayout(cols=5, spacing=12, padding=10, size_hint=(1, 0.72))
        numbers = EnglishData.get_numbers(10)
        colors = ['#FF6B6B', '#4ECDC4', '#45B7D1', '#96CEB4', '#DDA0DD',
                  '#FFD93D', '#FF9800', '#8BC34A', '#E91E63', '#9C27B0']
        
        for i, (num, english, chinese) in enumerate(numbers):
            btn = Button(background_normal='', background_color=get_color_from_hex(colors[i]))
            btn.markup = True
            btn.text = f'[size=36][b]{num}[/b][/size]\n[size=18]{english}[/size]\n[size=14]{chinese}[/size]'
            btn.num_data = (num, english, chinese)
            btn.bind(on_press=self.on_card_press)
            grid.add_widget(btn)
        
        layout.add_widget(grid)
        self.add_widget(layout)
    
    def on_card_press(self, instance):
        if hasattr(instance, 'num_data'):
            num, english, chinese = instance.num_data
            self.hint.text = f'{num} = {english}（{chinese}）'


class AnimalsLearnScreen(Screen):
    """动物英语"""
    
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.build_ui()
    
    def build_ui(self):
        layout = BoxLayout(orientation='vertical', padding=20, spacing=10)
        with layout.canvas.before:
            Color(*get_color_from_hex('#E8F5E9'))
            self.bg = Rectangle(pos=layout.pos, size=layout.size)
        layout.bind(pos=lambda i,v: setattr(self.bg, 'pos', v),
                   size=lambda i,v: setattr(self.bg, 'size', v))
        
        nav = BoxLayout(size_hint=(1, 0.1))
        back_btn = Button(text='< 返回', size_hint=(0.15, 1), font_size='16sp',
                         background_color=get_color_from_hex('#66BB6A'), background_normal='')
        back_btn.bind(on_press=lambda x: setattr(self.manager, 'current', 'english_menu'))
        nav.add_widget(back_btn)
        nav.add_widget(Label(text='【动物英语】', font_size='24sp',
                            color=get_color_from_hex('#2E7D32'), bold=True, size_hint=(0.7, 1)))
        nav.add_widget(Label(text='', size_hint=(0.15, 1)))
        layout.add_widget(nav)
        
        self.hint = Label(text='点击卡片学习动物英语！', font_size='18sp',
                         color=get_color_from_hex('#666666'), size_hint=(1, 0.08))
        layout.add_widget(self.hint)
        
        grid = GridLayout(cols=4, spacing=12, padding=10, size_hint=(1, 0.72))
        animals = EnglishData.get_animals()
        colors = ['#FF6B6B', '#4ECDC4', '#45B7D1', '#96CEB4', '#DDA0DD', '#FFD93D',
                  '#FF9800', '#8BC34A', '#E91E63', '#9C27B0', '#00BCD4', '#CDDC39']
        
        for i, (english, chinese, emoji) in enumerate(animals):
            btn = Button(background_normal='', background_color=get_color_from_hex(colors[i % len(colors)]))
            btn.markup = True
            # 用文字代替emoji
            btn.text = f'[size=28][b]{english}[/b][/size]\n[size=18]{chinese}[/size]'
            btn.animal_data = (english, chinese)
            btn.bind(on_press=self.on_card_press)
            grid.add_widget(btn)
        
        layout.add_widget(grid)
        self.add_widget(layout)
    
    def on_card_press(self, instance):
        if hasattr(instance, 'animal_data'):
            english, chinese = instance.animal_data
            self.hint.text = f'{english} = {chinese}'


class EnglishListenScreen(Screen):
    """听音选词"""
    
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.logic = GameLogic()
        self.session = None
        self.current_item = None
        self.correct_answer = None
        self.build_ui()
    
    def build_ui(self):
        layout = BoxLayout(orientation='vertical', padding=20, spacing=15)
        with layout.canvas.before:
            Color(*get_color_from_hex('#FCE4EC'))
            self.bg = Rectangle(pos=layout.pos, size=layout.size)
        layout.bind(pos=lambda i,v: setattr(self.bg, 'pos', v),
                   size=lambda i,v: setattr(self.bg, 'size', v))
        
        nav = BoxLayout(size_hint=(1, 0.1))
        back_btn = Button(text='< 返回', size_hint=(0.15, 1), font_size='16sp',
                         background_color=get_color_from_hex('#E91E63'), background_normal='')
        back_btn.bind(on_press=lambda x: setattr(self.manager, 'current', 'english_menu'))
        nav.add_widget(back_btn)
        nav.add_widget(Label(text='【听音选词】', font_size='24sp',
                            color=get_color_from_hex('#C2185B'), bold=True, size_hint=(0.55, 1)))
        self.score_label = Label(text='得分: 0', font_size='18sp',
                                color=get_color_from_hex('#FF6B6B'), size_hint=(0.15, 1))
        nav.add_widget(self.score_label)
        self.progress_label = Label(text='0/10', font_size='16sp',
                                   color=get_color_from_hex('#666666'), size_hint=(0.15, 1))
        nav.add_widget(self.progress_label)
        layout.add_widget(nav)
        
        self.question_label = Label(text='听英语，选中文！', font_size='24sp',
                                   color=get_color_from_hex('#333333'), size_hint=(1, 0.1))
        layout.add_widget(self.question_label)
        
        # 显示英文单词
        self.display_label = Label(text='?', font_size='60sp',
                                  color=get_color_from_hex('#E91E63'), size_hint=(1, 0.25))
        layout.add_widget(self.display_label)
        
        self.feedback_label = Label(text='', font_size='24sp',
                                   color=get_color_from_hex('#4CAF50'), size_hint=(1, 0.1))
        layout.add_widget(self.feedback_label)
        
        self.answers_layout = GridLayout(cols=4, spacing=10, padding=10, size_hint=(1, 0.25))
        layout.add_widget(self.answers_layout)
        
        self.start_btn = Button(text='开始游戏', font_size='20sp', size_hint=(1, 0.1),
                               background_color=get_color_from_hex('#E91E63'), background_normal='')
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
        
        # 随机选择题目类型
        q_type = random.choice(['animal', 'color', 'number'])
        
        if q_type == 'animal':
            animals = EnglishData.get_animals()
            self.current_item = random.choice(animals)
            english, chinese, emoji = self.current_item
            self.display_label.text = english
            all_chinese = [a[1] for a in animals]
            options = self.logic.get_random_options(chinese, all_chinese, count=4)
            self.correct_answer = chinese
        elif q_type == 'color':
            colors = EnglishData.get_colors()
            self.current_item = random.choice(colors)
            english, chinese, code, emoji = self.current_item
            self.display_label.text = english
            all_chinese = [c[1] for c in colors]
            options = self.logic.get_random_options(chinese, all_chinese, count=4)
            self.correct_answer = chinese
        else:
            numbers = EnglishData.get_numbers(10)
            self.current_item = random.choice(numbers)
            num, english, chinese = self.current_item
            self.display_label.text = english
            all_chinese = [n[2] for n in numbers]
            options = self.logic.get_random_options(chinese, all_chinese, count=4)
            self.correct_answer = chinese
        
        self.answers_layout.clear_widgets()
        colors = ['#FF6B6B', '#4ECDC4', '#45B7D1', '#96CEB4']
        for i, opt in enumerate(options):
            btn = Button(text=opt, font_size='24sp',
                        background_color=get_color_from_hex(colors[i % len(colors)]), background_normal='')
            btn.bind(on_press=self.on_answer)
            self.answers_layout.add_widget(btn)
        
        self.progress_label.text = f'{self.session.current_question + 1}/10'
    
    def on_answer(self, instance):
        if self.current_item is None:
            return
        
        user_answer = instance.text
        is_correct = self.logic.check_answer(self.session, user_answer, self.correct_answer)
        
        if is_correct:
            self.feedback_label.text = f'Correct! {self.display_label.text} = {self.correct_answer}'
            self.feedback_label.color = get_color_from_hex('#4CAF50')
            instance.background_color = get_color_from_hex('#4CAF50')
        else:
            self.feedback_label.text = f'错误，正确答案是 {self.correct_answer}'
            self.feedback_label.color = get_color_from_hex('#F44336')
            instance.background_color = get_color_from_hex('#F44336')
        
        self.score_label.text = f'得分: {self.session.score}'
        
        for btn in self.answers_layout.children:
            btn.disabled = True
        
        Clock.schedule_once(lambda dt: self.next_question(), 1.5)
    
    def show_result(self):
        stars = self.logic.calculate_stars(self.session)
        praise = self.logic.get_praise_message(self.session.accuracy)
        star_text = '★' * stars + '☆' * (3 - stars)
        self.question_label.text = f'{star_text} 游戏完成！'
        self.display_label.text = 'Good!'
        self.feedback_label.text = f'{praise}\n正确率: {self.session.accuracy*100:.0f}%'
