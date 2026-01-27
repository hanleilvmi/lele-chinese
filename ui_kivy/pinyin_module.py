# -*- coding: utf-8 -*-
"""
Kivy 拼音乐园模块
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

from core.data_pinyin import PinyinData
from core.game_logic import GameLogic, GameType

Window.size = (900, 700)


class PinyinMenuScreen(Screen):
    """拼音乐园菜单"""
    
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        layout = BoxLayout(orientation='vertical', padding=20, spacing=15)
        
        with layout.canvas.before:
            Color(*get_color_from_hex('#FFEBEE'))
            self.bg = Rectangle(pos=layout.pos, size=layout.size)
        layout.bind(pos=lambda i,v: setattr(self.bg, 'pos', v),
                   size=lambda i,v: setattr(self.bg, 'size', v))
        
        # 导航栏
        nav = BoxLayout(size_hint=(1, 0.1))
        back_btn = Button(text='< 返回', size_hint=(0.2, 1), font_size='16sp',
                         background_color=get_color_from_hex('#EF5350'), background_normal='')
        back_btn.bind(on_press=self.go_back)
        nav.add_widget(back_btn)
        nav.add_widget(Label(text='【拼音乐园】', font_size='28sp',
                            color=get_color_from_hex('#C62828'), bold=True, size_hint=(0.6, 1)))
        nav.add_widget(Label(text='', size_hint=(0.2, 1)))
        layout.add_widget(nav)
        
        # 游戏选择
        games = GridLayout(cols=3, spacing=15, size_hint=(1, 0.75), padding=20)
        game_list = [
            ('a o e', '学韵母', '6个韵母', '#FF6B6B', lambda: self.go_game('vowels')),
            ('b p m', '学声母', '声母卡片', '#FF8A65', lambda: self.go_game('consonants')),
            ('图', '看图选拼音', '看图片', '#96CEB4', lambda: self.go_game('picture')),
            ('对', '拼音配对', '找朋友', '#DDA0DD', lambda: self.go_game('match')),
            ('锤', '拼音打地鼠', '快反应', '#FFD93D', lambda: self.go_game('whack')),
            ('?', '拼音测验', '考考你', '#FFB74D', lambda: self.go_game('quiz')),
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
        if game_name == 'vowels':
            self.manager.current = 'vowels_learn'
        elif game_name == 'consonants':
            self.manager.current = 'consonants_learn'
        elif game_name == 'quiz':
            self.manager.current = 'pinyin_quiz'
        elif game_name == 'picture':
            self.manager.current = 'pinyin_picture'
        elif game_name == 'match':
            self.manager.current = 'pinyin_match'
        elif game_name == 'whack':
            self.manager.current = 'pinyin_whack'


class VowelsLearnScreen(Screen):
    """学韵母"""
    
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
                         background_color=get_color_from_hex('#FF7043'), background_normal='')
        back_btn.bind(on_press=lambda x: setattr(self.manager, 'current', 'pinyin_menu'))
        nav.add_widget(back_btn)
        nav.add_widget(Label(text='【学韵母】', font_size='24sp',
                            color=get_color_from_hex('#E65100'), bold=True, size_hint=(0.7, 1)))
        nav.add_widget(Label(text='', size_hint=(0.15, 1)))
        layout.add_widget(nav)
        
        self.hint = Label(text='点击卡片学习韵母！', font_size='18sp',
                         color=get_color_from_hex('#666666'), size_hint=(1, 0.08))
        layout.add_widget(self.hint)
        
        grid = GridLayout(cols=3, spacing=15, padding=10, size_hint=(1, 0.72))
        vowels = PinyinData.get_vowels()
        colors = ['#FF6B6B', '#4ECDC4', '#45B7D1', '#96CEB4', '#DDA0DD', '#FFD93D']
        
        for i, (pinyin, sound, emoji, desc) in enumerate(vowels):
            btn = Button(background_normal='', background_color=get_color_from_hex(colors[i]))
            btn.markup = True
            btn.text = f'[size=48][b]{pinyin}[/b][/size]\n[size=24]{sound}[/size]\n[size=14]{desc}[/size]'
            btn.pinyin_data = (pinyin, sound, desc)
            btn.bind(on_press=self.on_card_press)
            grid.add_widget(btn)
        
        layout.add_widget(grid)
        self.add_widget(layout)
    
    def on_card_press(self, instance):
        if hasattr(instance, 'pinyin_data'):
            pinyin, sound, desc = instance.pinyin_data
            self.hint.text = f'{pinyin} 读作 "{sound}"，{desc}'


class ConsonantsLearnScreen(Screen):
    """学声母"""
    
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
        back_btn.bind(on_press=lambda x: setattr(self.manager, 'current', 'pinyin_menu'))
        nav.add_widget(back_btn)
        nav.add_widget(Label(text='【学声母】', font_size='24sp',
                            color=get_color_from_hex('#2E7D32'), bold=True, size_hint=(0.7, 1)))
        nav.add_widget(Label(text='', size_hint=(0.15, 1)))
        layout.add_widget(nav)
        
        self.hint = Label(text='点击卡片学习声母！', font_size='18sp',
                         color=get_color_from_hex('#666666'), size_hint=(1, 0.08))
        layout.add_widget(self.hint)
        
        grid = GridLayout(cols=6, spacing=10, padding=10, size_hint=(1, 0.72))
        consonants = PinyinData.get_consonants(level=2)
        colors = ['#FF6B6B', '#4ECDC4', '#45B7D1', '#96CEB4', '#DDA0DD', '#FFD93D',
                  '#FF9800', '#8BC34A', '#E91E63', '#9C27B0', '#00BCD4', '#CDDC39']
        
        for i, (pinyin, sound, emoji, desc) in enumerate(consonants):
            btn = Button(background_normal='', background_color=get_color_from_hex(colors[i % len(colors)]))
            btn.markup = True
            btn.text = f'[size=36][b]{pinyin}[/b][/size]\n[size=18]{sound}[/size]'
            btn.pinyin_data = (pinyin, sound, desc)
            btn.bind(on_press=self.on_card_press)
            grid.add_widget(btn)
        
        layout.add_widget(grid)
        self.add_widget(layout)
    
    def on_card_press(self, instance):
        if hasattr(instance, 'pinyin_data'):
            pinyin, sound, desc = instance.pinyin_data
            self.hint.text = f'{pinyin} 读作 "{sound}"，{desc}'


class PinyinQuizScreen(Screen):
    """拼音测验"""
    
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.logic = GameLogic()
        self.session = None
        self.current_pinyin = None
        self.build_ui()
    
    def build_ui(self):
        layout = BoxLayout(orientation='vertical', padding=20, spacing=15)
        with layout.canvas.before:
            Color(*get_color_from_hex('#FFF8E1'))
            self.bg = Rectangle(pos=layout.pos, size=layout.size)
        layout.bind(pos=lambda i,v: setattr(self.bg, 'pos', v),
                   size=lambda i,v: setattr(self.bg, 'size', v))
        
        nav = BoxLayout(size_hint=(1, 0.1))
        back_btn = Button(text='< 返回', size_hint=(0.15, 1), font_size='16sp',
                         background_color=get_color_from_hex('#FFC107'), background_normal='')
        back_btn.bind(on_press=lambda x: setattr(self.manager, 'current', 'pinyin_menu'))
        nav.add_widget(back_btn)
        nav.add_widget(Label(text='【拼音测验】', font_size='24sp',
                            color=get_color_from_hex('#F57F17'), bold=True, size_hint=(0.55, 1)))
        self.score_label = Label(text='得分: 0', font_size='18sp',
                                color=get_color_from_hex('#FF6B6B'), size_hint=(0.15, 1))
        nav.add_widget(self.score_label)
        self.progress_label = Label(text='0/10', font_size='16sp',
                                   color=get_color_from_hex('#666666'), size_hint=(0.15, 1))
        nav.add_widget(self.progress_label)
        layout.add_widget(nav)
        
        self.question_label = Label(text='这个拼音怎么读？', font_size='24sp',
                                   color=get_color_from_hex('#333333'), size_hint=(1, 0.1))
        layout.add_widget(self.question_label)
        
        self.display_label = Label(text='?', font_size='100sp',
                                  color=get_color_from_hex('#E65100'), size_hint=(1, 0.3))
        layout.add_widget(self.display_label)
        
        self.feedback_label = Label(text='', font_size='24sp',
                                   color=get_color_from_hex('#4CAF50'), size_hint=(1, 0.1))
        layout.add_widget(self.feedback_label)
        
        self.answers_layout = GridLayout(cols=4, spacing=10, padding=10, size_hint=(1, 0.2))
        layout.add_widget(self.answers_layout)
        
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
        
        all_pinyin = PinyinData.get_all_pinyin(level=2)
        self.current_pinyin = random.choice(all_pinyin)
        pinyin, sound, emoji, desc = self.current_pinyin
        
        self.display_label.text = pinyin
        
        self.answers_layout.clear_widgets()
        all_sounds = [p[1] for p in all_pinyin]
        options = self.logic.get_random_options(sound, all_sounds, count=4)
        
        for opt in options:
            btn = Button(text=opt, font_size='24sp',
                        background_color=get_color_from_hex('#64B5F6'), background_normal='')
            btn.bind(on_press=self.on_answer)
            self.answers_layout.add_widget(btn)
        
        self.progress_label.text = f'{self.session.current_question + 1}/10'
    
    def on_answer(self, instance):
        if self.current_pinyin is None:
            return
        
        user_answer = instance.text
        correct_answer = self.current_pinyin[1]
        
        is_correct = self.logic.check_answer(self.session, user_answer, correct_answer)
        
        if is_correct:
            self.feedback_label.text = f'正确！{self.current_pinyin[0]} 读作 "{correct_answer}"'
            self.feedback_label.color = get_color_from_hex('#4CAF50')
        else:
            self.feedback_label.text = f'错误，正确答案是 "{correct_answer}"'
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


class PinyinPictureScreen(Screen):
    """看图选拼音"""
    
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.logic = GameLogic()
        self.session = None
        self.current_pinyin = None
        self.build_ui()
    
    def build_ui(self):
        layout = BoxLayout(orientation='vertical', padding=20, spacing=15)
        with layout.canvas.before:
            Color(*get_color_from_hex('#E8F5E9'))
            self.bg = Rectangle(pos=layout.pos, size=layout.size)
        layout.bind(pos=lambda i,v: setattr(self.bg, 'pos', v),
                   size=lambda i,v: setattr(self.bg, 'size', v))
        
        nav = BoxLayout(size_hint=(1, 0.1))
        back_btn = Button(text='< 返回', size_hint=(0.15, 1), font_size='16sp',
                         background_color=get_color_from_hex('#66BB6A'), background_normal='')
        back_btn.bind(on_press=lambda x: setattr(self.manager, 'current', 'pinyin_menu'))
        nav.add_widget(back_btn)
        nav.add_widget(Label(text='【看图选拼音】', font_size='24sp',
                            color=get_color_from_hex('#2E7D32'), bold=True, size_hint=(0.55, 1)))
        self.score_label = Label(text='得分: 0', font_size='18sp',
                                color=get_color_from_hex('#FF6B6B'), size_hint=(0.15, 1))
        nav.add_widget(self.score_label)
        self.progress_label = Label(text='0/10', font_size='16sp',
                                   color=get_color_from_hex('#666666'), size_hint=(0.15, 1))
        nav.add_widget(self.progress_label)
        layout.add_widget(nav)
        
        self.question_label = Label(text='看图片，选拼音！', font_size='24sp',
                                   color=get_color_from_hex('#333333'), size_hint=(1, 0.08))
        layout.add_widget(self.question_label)
        
        # 图片显示区（用描述文字代替emoji）
        self.display_label = Label(text='?', font_size='80sp',
                                  color=get_color_from_hex('#2E7D32'), size_hint=(1, 0.28))
        layout.add_widget(self.display_label)
        
        self.desc_label = Label(text='', font_size='20sp',
                               color=get_color_from_hex('#666666'), size_hint=(1, 0.08))
        layout.add_widget(self.desc_label)
        
        self.feedback_label = Label(text='', font_size='24sp',
                                   color=get_color_from_hex('#4CAF50'), size_hint=(1, 0.1))
        layout.add_widget(self.feedback_label)
        
        self.answers_layout = GridLayout(cols=4, spacing=10, padding=10, size_hint=(1, 0.2))
        layout.add_widget(self.answers_layout)
        
        self.start_btn = Button(text='开始游戏', font_size='20sp', size_hint=(1, 0.1),
                               background_color=get_color_from_hex('#4CAF50'), background_normal='')
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
        
        all_pinyin = PinyinData.get_all_pinyin(level=2)
        self.current_pinyin = random.choice(all_pinyin)
        pinyin, sound, emoji, desc = self.current_pinyin
        
        # 显示描述作为提示
        self.display_label.text = sound
        self.desc_label.text = desc
        
        self.answers_layout.clear_widgets()
        all_letters = [p[0] for p in all_pinyin]
        options = self.logic.get_random_options(pinyin, all_letters, count=4)
        
        colors = ['#FF6B6B', '#4ECDC4', '#45B7D1', '#96CEB4']
        for i, opt in enumerate(options):
            btn = Button(text=opt, font_size='36sp',
                        background_color=get_color_from_hex(colors[i % len(colors)]), background_normal='')
            btn.bind(on_press=self.on_answer)
            self.answers_layout.add_widget(btn)
        
        self.progress_label.text = f'{self.session.current_question + 1}/10'
    
    def on_answer(self, instance):
        if self.current_pinyin is None:
            return
        
        user_answer = instance.text
        correct_answer = self.current_pinyin[0]
        
        is_correct = self.logic.check_answer(self.session, user_answer, correct_answer)
        
        if is_correct:
            self.feedback_label.text = f'太棒了！是 {correct_answer}！'
            self.feedback_label.color = get_color_from_hex('#4CAF50')
            instance.background_color = get_color_from_hex('#4CAF50')
        else:
            self.feedback_label.text = f'错误，正确答案是 {correct_answer}'
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
        self.display_label.text = '棒！'
        self.desc_label.text = ''
        self.feedback_label.text = f'{praise}\n正确率: {self.session.accuracy*100:.0f}%'


class PinyinMatchScreen(Screen):
    """拼音配对游戏"""
    
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.logic = GameLogic()
        self.cards = []
        self.card_data = []
        self.selected = None
        self.matched = set()
        self.score = 0
        self.build_ui()
    
    def build_ui(self):
        layout = BoxLayout(orientation='vertical', padding=20, spacing=10)
        with layout.canvas.before:
            Color(*get_color_from_hex('#FFFDE7'))
            self.bg = Rectangle(pos=layout.pos, size=layout.size)
        layout.bind(pos=lambda i,v: setattr(self.bg, 'pos', v),
                   size=lambda i,v: setattr(self.bg, 'size', v))
        
        nav = BoxLayout(size_hint=(1, 0.1))
        back_btn = Button(text='< 返回', size_hint=(0.15, 1), font_size='16sp',
                         background_color=get_color_from_hex('#DDA0DD'), background_normal='')
        back_btn.bind(on_press=lambda x: setattr(self.manager, 'current', 'pinyin_menu'))
        nav.add_widget(back_btn)
        nav.add_widget(Label(text='【拼音配对】', font_size='24sp',
                            color=get_color_from_hex('#9C27B0'), bold=True, size_hint=(0.55, 1)))
        self.score_label = Label(text='得分: 0', font_size='18sp',
                                color=get_color_from_hex('#FF6B6B'), size_hint=(0.15, 1))
        nav.add_widget(self.score_label)
        nav.add_widget(Label(text='', size_hint=(0.15, 1)))
        layout.add_widget(nav)
        
        self.hint_label = Label(text='找到拼音和它的读音配对！', font_size='18sp',
                               color=get_color_from_hex('#666666'), size_hint=(1, 0.08))
        layout.add_widget(self.hint_label)
        
        self.feedback_label = Label(text='', font_size='20sp',
                                   color=get_color_from_hex('#4CAF50'), size_hint=(1, 0.08))
        layout.add_widget(self.feedback_label)
        
        self.cards_layout = GridLayout(cols=4, spacing=10, padding=10, size_hint=(1, 0.54))
        layout.add_widget(self.cards_layout)
        
        self.start_btn = Button(text='开始游戏', font_size='20sp', size_hint=(1, 0.1),
                               background_color=get_color_from_hex('#9C27B0'), background_normal='')
        self.start_btn.bind(on_press=self.start_game)
        layout.add_widget(self.start_btn)
        
        self.add_widget(layout)
    
    def start_game(self, instance):
        self.cards = []
        self.card_data = []
        self.selected = None
        self.matched = set()
        self.score = 0
        self.score_label.text = '得分: 0'
        self.feedback_label.text = ''
        self.start_btn.text = '重新开始'
        
        self.cards_layout.clear_widgets()
        
        # 选择6个拼音
        all_pinyin = PinyinData.get_all_pinyin(level=2)
        selected = random.sample(all_pinyin, 6)
        
        # 创建配对数据：拼音字母 + 读音
        for item in selected:
            pinyin, sound, emoji, desc = item
            self.card_data.append({'type': 'pinyin', 'value': pinyin, 'match_id': pinyin})
            self.card_data.append({'type': 'sound', 'value': sound, 'match_id': pinyin})
        
        random.shuffle(self.card_data)
        
        colors = ['#FFB6C1', '#98FB98', '#87CEEB', '#DDA0DD', '#F0E68C', '#FFA07A',
                  '#B0E0E6', '#FFE4B5', '#E6E6FA', '#FFDAB9', '#D8BFD8', '#F5DEB3']
        
        for i in range(12):
            card = self.card_data[i]
            btn = Button(text='?', font_size='32sp',
                        background_color=get_color_from_hex(colors[i]), background_normal='')
            btn.card_index = i
            btn.card_value = card['value']
            btn.card_type = card['type']
            btn.original_color = get_color_from_hex(colors[i])
            btn.bind(on_press=self.on_card_press)
            self.cards_layout.add_widget(btn)
            self.cards.append(btn)
        
        # 先显示所有卡片3秒
        self.show_all_cards()
        Clock.schedule_once(lambda dt: self.hide_all_cards(), 3.0)
    
    def show_all_cards(self):
        for i, btn in enumerate(self.cards):
            btn.text = self.card_data[i]['value']
        self.hint_label.text = '记住位置！3秒后翻回去...'
    
    def hide_all_cards(self):
        for i, btn in enumerate(self.cards):
            if i not in self.matched:
                btn.text = '?'
        self.hint_label.text = '点击卡片找配对！'
    
    def on_card_press(self, instance):
        idx = instance.card_index
        if idx in self.matched:
            return
        
        # 显示卡片
        instance.text = self.card_data[idx]['value']
        
        if self.selected is None:
            self.selected = idx
            instance.background_color = get_color_from_hex('#FFEB3B')
        else:
            first_idx = self.selected
            first_btn = self.cards[first_idx]
            first_data = self.card_data[first_idx]
            second_data = self.card_data[idx]
            
            # 检查是否配对成功（同一个match_id但不同类型）
            if (first_data['match_id'] == second_data['match_id'] and 
                first_data['type'] != second_data['type'] and first_idx != idx):
                # 配对成功
                self.score += 20
                self.score_label.text = f'得分: {self.score}'
                self.matched.add(first_idx)
                self.matched.add(idx)
                first_btn.background_color = get_color_from_hex('#4CAF50')
                instance.background_color = get_color_from_hex('#4CAF50')
                self.feedback_label.text = f'太棒了！{first_data["match_id"]} 配对成功！'
                self.feedback_label.color = get_color_from_hex('#4CAF50')
                
                if len(self.matched) == 12:
                    Clock.schedule_once(lambda dt: self.show_complete(), 1.0)
            else:
                # 配对失败
                self.feedback_label.text = '不是配对，再试试！'
                self.feedback_label.color = get_color_from_hex('#FF9800')
                Clock.schedule_once(lambda dt: self.flip_back(first_idx, idx), 1.0)
            
            self.selected = None
    
    def flip_back(self, idx1, idx2):
        if idx1 not in self.matched:
            self.cards[idx1].text = '?'
            self.cards[idx1].background_color = self.cards[idx1].original_color
        if idx2 not in self.matched:
            self.cards[idx2].text = '?'
            self.cards[idx2].background_color = self.cards[idx2].original_color
    
    def show_complete(self):
        self.hint_label.text = '★★★ 太厉害了！全部配对成功！★★★'
        self.feedback_label.text = f'总得分: {self.score}'
        self.feedback_label.color = get_color_from_hex('#FF6B6B')


class PinyinWhackScreen(Screen):
    """拼音打地鼠游戏"""
    
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.logic = GameLogic()
        self.session = None
        self.target_pinyin = None
        self.holes = []
        self.hole_states = [None] * 9
        self.game_active = False
        self.spawn_event = None
        self.build_ui()
    
    def build_ui(self):
        layout = BoxLayout(orientation='vertical', padding=20, spacing=10)
        with layout.canvas.before:
            Color(*get_color_from_hex('#90EE90'))
            self.bg = Rectangle(pos=layout.pos, size=layout.size)
        layout.bind(pos=lambda i,v: setattr(self.bg, 'pos', v),
                   size=lambda i,v: setattr(self.bg, 'size', v))
        
        nav = BoxLayout(size_hint=(1, 0.08))
        back_btn = Button(text='< 返回', size_hint=(0.15, 1), font_size='16sp',
                         background_color=get_color_from_hex('#228B22'), background_normal='')
        back_btn.bind(on_press=self.go_back)
        nav.add_widget(back_btn)
        nav.add_widget(Label(text='【拼音打地鼠】', font_size='24sp',
                            color=get_color_from_hex('#006400'), bold=True, size_hint=(0.55, 1)))
        self.score_label = Label(text='得分: 0', font_size='18sp',
                                color=get_color_from_hex('#FF6B6B'), size_hint=(0.15, 1))
        nav.add_widget(self.score_label)
        self.round_label = Label(text='0/10', font_size='16sp',
                                color=get_color_from_hex('#333333'), size_hint=(0.15, 1))
        nav.add_widget(self.round_label)
        layout.add_widget(nav)
        
        # 目标提示
        target_box = BoxLayout(size_hint=(1, 0.12), padding=[100, 5])
        target_bg = Button(text='', background_color=get_color_from_hex('#FFD700'), 
                          background_normal='', size_hint=(1, 1))
        target_box.add_widget(target_bg)
        layout.add_widget(target_box)
        
        self.target_label = Label(text='点击开始游戏！', font_size='28sp',
                                 color=get_color_from_hex('#DC143C'), size_hint=(1, 0.01))
        layout.add_widget(self.target_label)
        
        self.feedback_label = Label(text='', font_size='20sp',
                                   color=get_color_from_hex('#4CAF50'), size_hint=(1, 0.08))
        layout.add_widget(self.feedback_label)
        
        # 地鼠洞网格 3x3
        self.holes_layout = GridLayout(cols=3, spacing=15, padding=20, size_hint=(1, 0.52))
        hole_colors = ['#8B4513', '#A0522D', '#8B4513', '#A0522D', '#8B4513', '#A0522D',
                       '#8B4513', '#A0522D', '#8B4513']
        
        for i in range(9):
            hole_btn = Button(text='', font_size='36sp',
                             background_color=get_color_from_hex(hole_colors[i]), 
                             background_normal='')
            hole_btn.hole_index = i
            hole_btn.bind(on_press=self.on_hole_press)
            self.holes_layout.add_widget(hole_btn)
            self.holes.append(hole_btn)
        
        layout.add_widget(self.holes_layout)
        
        self.start_btn = Button(text='开始游戏', font_size='20sp', size_hint=(1, 0.1),
                               background_color=get_color_from_hex('#FF9800'), background_normal='')
        self.start_btn.bind(on_press=self.start_game)
        layout.add_widget(self.start_btn)
        
        self.add_widget(layout)
    
    def go_back(self, instance):
        self.stop_game()
        self.manager.current = 'pinyin_menu'
    
    def start_game(self, instance):
        self.session = self.logic.create_session(GameType.WHACK, total_questions=10)
        self.score_label.text = '得分: 0'
        self.feedback_label.text = ''
        self.start_btn.text = '重新开始'
        self.game_active = True
        self.spawn_moles()
    
    def stop_game(self):
        self.game_active = False
        if self.spawn_event:
            self.spawn_event.cancel()
            self.spawn_event = None
        for hole in self.holes:
            hole.text = ''
            hole.background_color = get_color_from_hex('#8B4513')
        self.hole_states = [None] * 9
    
    def spawn_moles(self):
        if not self.game_active:
            return
        
        if self.session.current_question >= self.session.total_questions:
            self.show_result()
            return
        
        # 清空所有洞
        for i, hole in enumerate(self.holes):
            hole.text = ''
            hole.background_color = get_color_from_hex('#8B4513')
            self.hole_states[i] = None
        
        # 选择目标拼音
        all_pinyin = PinyinData.get_all_pinyin(level=2)
        target = random.choice(all_pinyin)
        self.target_pinyin = target[0]
        self.target_label.text = f'快打 {self.target_pinyin}！'
        
        # 随机选择3-4个洞放地鼠
        num_moles = random.randint(3, 4)
        mole_positions = random.sample(range(9), num_moles)
        
        # 确保目标拼音在其中
        others = random.sample([p for p in all_pinyin if p[0] != self.target_pinyin], num_moles - 1)
        pinyin_list = [self.target_pinyin] + [p[0] for p in others]
        random.shuffle(pinyin_list)
        
        # 放置地鼠
        for i, pos in enumerate(mole_positions):
            hole = self.holes[pos]
            pinyin = pinyin_list[i]
            hole.text = f'{pinyin}'
            hole.background_color = get_color_from_hex('#FFE4B5')
            self.hole_states[pos] = pinyin
        
        self.round_label.text = f'{self.session.current_question + 1}/10'
        
        # 2.5秒后地鼠消失
        self.spawn_event = Clock.schedule_once(self.moles_hide, 2.5)
    
    def moles_hide(self, dt):
        if not self.game_active:
            return
        
        self.feedback_label.text = f'错过了！目标是 {self.target_pinyin}'
        self.feedback_label.color = get_color_from_hex('#FF9800')
        self.session.add_wrong()
        
        Clock.schedule_once(lambda dt: self.spawn_moles(), 1.0)
    
    def on_hole_press(self, instance):
        if not self.game_active:
            return
        
        idx = instance.hole_index
        pinyin = self.hole_states[idx]
        
        if pinyin is None:
            return
        
        # 取消自动隐藏
        if self.spawn_event:
            self.spawn_event.cancel()
        
        if pinyin == self.target_pinyin:
            # 打中目标
            self.session.add_correct(10)
            self.score_label.text = f'得分: {self.session.score}'
            self.feedback_label.text = f'太棒了！打中 {self.target_pinyin}！'
            self.feedback_label.color = get_color_from_hex('#4CAF50')
            instance.background_color = get_color_from_hex('#4CAF50')
            instance.text = '棒!'
        else:
            # 打错了
            self.session.add_wrong()
            self.feedback_label.text = f'打错了！要打 {self.target_pinyin}'
            self.feedback_label.color = get_color_from_hex('#F44336')
            instance.background_color = get_color_from_hex('#F44336')
            instance.text = 'X'
        
        # 清空该洞状态
        self.hole_states[idx] = None
        
        Clock.schedule_once(lambda dt: self.spawn_moles(), 1.0)
    
    def show_result(self):
        self.game_active = False
        stars = self.logic.calculate_stars(self.session)
        praise = self.logic.get_praise_message(self.session.accuracy)
        star_text = '★' * stars + '☆' * (3 - stars)
        self.target_label.text = f'{star_text} 游戏完成！'
        self.feedback_label.text = f'{praise}\n正确率: {self.session.accuracy*100:.0f}%'
        self.feedback_label.color = get_color_from_hex('#FF9800')
        
        for hole in self.holes:
            hole.text = '棒'
            hole.background_color = get_color_from_hex('#4CAF50')


class PinyinApp(App):
    """拼音乐园独立应用"""
    
    def build(self):
        self.title = '乐乐的拼音乐园 - Kivy版'
        sm = ScreenManager()
        sm.add_widget(PinyinMenuScreen(name='pinyin_menu'))
        sm.add_widget(VowelsLearnScreen(name='vowels_learn'))
        sm.add_widget(ConsonantsLearnScreen(name='consonants_learn'))
        sm.add_widget(PinyinQuizScreen(name='pinyin_quiz'))
        sm.add_widget(PinyinPictureScreen(name='pinyin_picture'))
        sm.add_widget(PinyinMatchScreen(name='pinyin_match'))
        sm.add_widget(PinyinWhackScreen(name='pinyin_whack'))
        return sm


if __name__ == '__main__':
    PinyinApp().run()
