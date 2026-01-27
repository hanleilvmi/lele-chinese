# -*- coding: utf-8 -*-
"""
Kivy 数学乐园模块
整合 core 模块的数据和游戏逻辑
"""
import sys
import os
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

# 必须在导入其他 kivy 模块之前配置字体
import font_config

from kivy.app import App
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.gridlayout import GridLayout
from kivy.uix.button import Button
from kivy.uix.label import Label
from kivy.uix.screenmanager import ScreenManager, Screen
from kivy.graphics import Color, Rectangle, RoundedRectangle
from kivy.core.window import Window
from kivy.utils import get_color_from_hex
from kivy.clock import Clock
from kivy.animation import Animation
import random

from core.data_math import MathData
from core.game_logic import GameLogic, GameType

Window.size = (900, 700)


class GameCard(Button):
    """可点击的游戏卡片 - 使用Button基类确保点击可靠"""
    
    def __init__(self, icon, title, desc, color, callback=None, **kwargs):
        super().__init__(**kwargs)
        self.background_normal = ''
        self.background_color = get_color_from_hex(color)
        self.callback = callback
        
        # 使用markup显示多行文本
        self.markup = True
        self.halign = 'center'
        self.valign = 'middle'
        self.text = f'[size=40]{icon}[/size]\n\n[b]{title}[/b]\n[size=12]{desc}[/size]'
        self.text_size = (None, None)
        
        if callback:
            self.bind(on_press=lambda x: callback())


class AnswerButton(Button):
    """答案按钮，带动画效果"""
    
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.font_size = '24sp'
        self.background_normal = ''
        self.original_color = None
    
    def flash_correct(self):
        self.background_color = get_color_from_hex('#4CAF50')
        Clock.schedule_once(lambda dt: self.reset_color(), 0.5)
    
    def flash_wrong(self):
        self.background_color = get_color_from_hex('#F44336')
        Clock.schedule_once(lambda dt: self.reset_color(), 0.5)
    
    def reset_color(self):
        if self.original_color:
            self.background_color = self.original_color


class MathMenuScreen(Screen):
    """数学乐园菜单"""
    
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        layout = BoxLayout(orientation='vertical', padding=20, spacing=15)
        
        with layout.canvas.before:
            Color(*get_color_from_hex('#E8F5E9'))
            self.bg = Rectangle(pos=layout.pos, size=layout.size)
        layout.bind(pos=lambda i,v: setattr(self.bg, 'pos', v), 
                   size=lambda i,v: setattr(self.bg, 'size', v))
        
        # 顶部导航
        nav = BoxLayout(size_hint=(1, 0.1))
        back_btn = Button(text='< 返回', size_hint=(0.2, 1), font_size='16sp',
                         background_color=get_color_from_hex('#96CEB4'), background_normal='')
        back_btn.bind(on_press=self.go_back)
        nav.add_widget(back_btn)
        nav.add_widget(Label(text='【数学乐园】', font_size='28sp', 
                            color=get_color_from_hex('#2E7D32'), bold=True, size_hint=(0.6, 1)))
        nav.add_widget(Label(text='', size_hint=(0.2, 1)))
        layout.add_widget(nav)

        # 游戏选择
        games = GridLayout(cols=3, spacing=15, size_hint=(1, 0.75), padding=20)
        game_list = [
            ('1~10', '数字卡片', '认识1-10', '#FF6B6B', lambda: self.go_game('numbers')),
            ('数', '数一数', '数数量', '#4ECDC4', lambda: self.go_game('count')),
            ('形', '认形状', '学形状', '#96CEB4', lambda: self.go_game('shapes')),
            ('><', '比大小', '谁更大', '#45B7D1', lambda: self.go_game('compare')),
            ('+', '学加法', '做加法', '#DDA0DD', lambda: self.go_game('addition')),
            ('锤', '打地鼠', '快反应', '#FFD93D', lambda: self.go_game('whack')),
        ]
        for icon, title, desc, color, cb in game_list:
            games.add_widget(GameCard(icon, title, desc, color, cb))
        layout.add_widget(games)
        self.add_widget(layout)
    
    def go_back(self, instance):
        if 'main' in [s.name for s in self.manager.screens]:
            self.manager.current = 'main'
    
    def go_game(self, game_name):
        if game_name == 'numbers':
            self.manager.current = 'number_cards'
        elif game_name == 'addition':
            self.manager.current = 'addition'
        elif game_name == 'compare':
            self.manager.current = 'compare'
        elif game_name == 'whack':
            self.manager.current = 'whack_game'
        elif game_name == 'count':
            self.manager.current = 'count_game'
        elif game_name == 'shapes':
            self.manager.current = 'shapes_game'


class NumberCardsScreen(Screen):
    """数字卡片学习"""
    
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
                         background_color=get_color_from_hex('#FF9800'), background_normal='')
        back_btn.bind(on_press=lambda x: setattr(self.manager, 'current', 'math_menu'))
        nav.add_widget(back_btn)
        nav.add_widget(Label(text='【数字卡片】', font_size='24sp',
                            color=get_color_from_hex('#E65100'), bold=True, size_hint=(0.7, 1)))
        nav.add_widget(Label(text='', size_hint=(0.15, 1)))
        layout.add_widget(nav)
        
        # 提示
        self.hint = Label(text='点击卡片学习数字！', font_size='18sp',
                         color=get_color_from_hex('#666666'), size_hint=(1, 0.08))
        layout.add_widget(self.hint)
        
        # 数字卡片网格
        grid = GridLayout(cols=5, spacing=12, padding=10, size_hint=(1, 0.72))
        numbers = MathData.get_numbers(10)
        colors = ['#FF6B6B', '#4ECDC4', '#45B7D1', '#96CEB4', '#DDA0DD',
                  '#FFD93D', '#FF9800', '#8BC34A', '#E91E63', '#9C27B0']
        
        # 用星号代替emoji
        dot_display = ['*', '**', '***', '****', '*****', '******', '*******', '********', '*********', '**********']
        
        for i, (num, cn, emoji) in enumerate(numbers):
            # 使用Button确保点击可靠
            card = Button(background_normal='', background_color=get_color_from_hex(colors[i]))
            card.markup = True
            card.text = f'[size=48][b]{num}[/b][/size]\n[size=24]{cn}[/size]\n[size=14]{dot_display[i]}[/size]'
            card.num_data = (num, cn)
            card.bind(on_press=self.on_card_press)
            grid.add_widget(card)
        
        layout.add_widget(grid)
        self.add_widget(layout)
    
    def on_card_press(self, instance):
        if hasattr(instance, 'num_data'):
            num, cn = instance.num_data
            self.hint.text = f'这是数字 {num}，读作"{cn}"'


class AdditionScreen(Screen):
    """加法练习"""
    
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.logic = GameLogic()
        self.session = None
        self.current_problem = None
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
                         background_color=get_color_from_hex('#4CAF50'), background_normal='')
        back_btn.bind(on_press=lambda x: setattr(self.manager, 'current', 'math_menu'))
        nav.add_widget(back_btn)
        nav.add_widget(Label(text='【学加法】', font_size='24sp',
                            color=get_color_from_hex('#2E7D32'), bold=True, size_hint=(0.55, 1)))
        self.score_label = Label(text='得分: 0', font_size='18sp',
                                color=get_color_from_hex('#FF6B6B'), size_hint=(0.15, 1))
        nav.add_widget(self.score_label)
        self.progress_label = Label(text='0/10', font_size='16sp',
                                   color=get_color_from_hex('#666666'), size_hint=(0.15, 1))
        nav.add_widget(self.progress_label)
        layout.add_widget(nav)
        
        # 题目显示区
        self.question_label = Label(text='点击开始按钮开始练习', font_size='48sp',
                                   color=get_color_from_hex('#333333'), size_hint=(1, 0.25))
        layout.add_widget(self.question_label)
        
        # 反馈区
        self.feedback_label = Label(text='', font_size='24sp',
                                   color=get_color_from_hex('#4CAF50'), size_hint=(1, 0.1))
        layout.add_widget(self.feedback_label)
        
        # 答案按钮区
        self.answers_layout = GridLayout(cols=4, spacing=15, padding=20, size_hint=(1, 0.35))
        for i in range(4):
            btn = AnswerButton(text='', background_color=get_color_from_hex('#64B5F6'))
            btn.original_color = get_color_from_hex('#64B5F6')
            btn.bind(on_press=self.on_answer)
            self.answers_layout.add_widget(btn)
        layout.add_widget(self.answers_layout)
        
        # 开始按钮
        self.start_btn = Button(text='开始练习', font_size='20sp', size_hint=(1, 0.12),
                               background_color=get_color_from_hex('#FF9800'), background_normal='')
        self.start_btn.bind(on_press=self.start_game)
        layout.add_widget(self.start_btn)
        
        self.add_widget(layout)
    
    def start_game(self, instance):
        self.session = self.logic.create_session(GameType.ADDITION, total_questions=10)
        self.score_label.text = '得分: 0'
        self.feedback_label.text = ''
        self.start_btn.text = '重新开始'
        self.next_question()
    
    def next_question(self):
        if self.session.is_complete():
            self.show_result()
            return
        
        self.current_problem = MathData.generate_addition(max_num=10)
        a, b, answer = self.current_problem
        self.question_label.text = f'{a} + {b} = ?'
        
        options = self.logic.get_random_options(answer, list(range(0, 11)), count=4)
        for i, btn in enumerate(self.answers_layout.children[::-1]):
            btn.text = str(options[i])
            btn.disabled = False
        
        self.progress_label.text = f'{self.session.current_question + 1}/10'
    
    def on_answer(self, instance):
        if not self.current_problem:
            return
        
        user_answer = int(instance.text)
        correct_answer = self.current_problem[2]
        
        is_correct = self.logic.check_answer(self.session, user_answer, correct_answer)
        
        if is_correct:
            instance.flash_correct()
            self.feedback_label.text = '正确！太棒了！'
            self.feedback_label.color = get_color_from_hex('#4CAF50')
        else:
            instance.flash_wrong()
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
        self.question_label.text = f'{star_text}\n{praise}'
        self.feedback_label.text = f'正确率: {self.session.accuracy*100:.0f}%'
        self.feedback_label.color = get_color_from_hex('#FF9800')


class CompareScreen(Screen):
    """比大小游戏"""
    
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.logic = GameLogic()
        self.session = None
        self.current_pair = None
        self.build_ui()
    
    def build_ui(self):
        layout = BoxLayout(orientation='vertical', padding=20, spacing=15)
        with layout.canvas.before:
            Color(*get_color_from_hex('#E3F2FD'))
            self.bg = Rectangle(pos=layout.pos, size=layout.size)
        layout.bind(pos=lambda i,v: setattr(self.bg, 'pos', v),
                   size=lambda i,v: setattr(self.bg, 'size', v))
        
        # 导航栏
        nav = BoxLayout(size_hint=(1, 0.1))
        back_btn = Button(text='< 返回', size_hint=(0.15, 1), font_size='16sp',
                         background_color=get_color_from_hex('#2196F3'), background_normal='')
        back_btn.bind(on_press=lambda x: setattr(self.manager, 'current', 'math_menu'))
        nav.add_widget(back_btn)
        nav.add_widget(Label(text='【比大小】', font_size='24sp',
                            color=get_color_from_hex('#1565C0'), bold=True, size_hint=(0.55, 1)))
        self.score_label = Label(text='得分: 0', font_size='18sp',
                                color=get_color_from_hex('#FF6B6B'), size_hint=(0.15, 1))
        nav.add_widget(self.score_label)
        self.progress_label = Label(text='0/10', font_size='16sp',
                                   color=get_color_from_hex('#666666'), size_hint=(0.15, 1))
        nav.add_widget(self.progress_label)
        layout.add_widget(nav)
        
        # 提示
        self.hint_label = Label(text='点击更大的数字！', font_size='20sp',
                               color=get_color_from_hex('#666666'), size_hint=(1, 0.08))
        layout.add_widget(self.hint_label)
        
        # 数字对比区
        compare_layout = BoxLayout(spacing=30, padding=40, size_hint=(1, 0.45))
        
        self.left_btn = Button(text='?', font_size='72sp', 
                              background_color=get_color_from_hex('#FF6B6B'), background_normal='')
        self.left_btn.bind(on_press=lambda x: self.on_choose('left'))
        compare_layout.add_widget(self.left_btn)
        
        compare_layout.add_widget(Label(text='VS', font_size='36sp',
                                       color=get_color_from_hex('#333333'), size_hint=(0.2, 1)))
        
        self.right_btn = Button(text='?', font_size='72sp',
                               background_color=get_color_from_hex('#4ECDC4'), background_normal='')
        self.right_btn.bind(on_press=lambda x: self.on_choose('right'))
        compare_layout.add_widget(self.right_btn)
        
        layout.add_widget(compare_layout)
        
        # 反馈区
        self.feedback_label = Label(text='', font_size='28sp',
                                   color=get_color_from_hex('#4CAF50'), size_hint=(1, 0.12))
        layout.add_widget(self.feedback_label)
        
        # 开始按钮
        self.start_btn = Button(text='开始游戏', font_size='20sp', size_hint=(1, 0.12),
                               background_color=get_color_from_hex('#FF9800'), background_normal='')
        self.start_btn.bind(on_press=self.start_game)
        layout.add_widget(self.start_btn)
        
        self.add_widget(layout)
    
    def start_game(self, instance):
        self.session = self.logic.create_session(GameType.COMPARE, total_questions=10)
        self.score_label.text = '得分: 0'
        self.feedback_label.text = ''
        self.start_btn.text = '重新开始'
        self.next_question()
    
    def next_question(self):
        if self.session.is_complete():
            self.show_result()
            return
        
        a = random.randint(1, 10)
        b = random.randint(1, 10)
        while b == a:
            b = random.randint(1, 10)
        
        self.current_pair = (a, b)
        self.left_btn.text = str(a)
        self.right_btn.text = str(b)
        self.left_btn.disabled = False
        self.right_btn.disabled = False
        
        self.progress_label.text = f'{self.session.current_question + 1}/10'
        self.hint_label.text = '哪个数字更大？点击它！'
    
    def on_choose(self, side):
        if not self.current_pair:
            return
        
        a, b = self.current_pair
        correct = 'left' if a > b else 'right'
        
        is_correct = self.logic.check_answer(self.session, side, correct)
        
        if is_correct:
            self.feedback_label.text = '答对了！太棒了！'
            self.feedback_label.color = get_color_from_hex('#4CAF50')
        else:
            bigger = a if a > b else b
            self.feedback_label.text = f'错误，{bigger} 更大哦！'
            self.feedback_label.color = get_color_from_hex('#F44336')
        
        self.score_label.text = f'得分: {self.session.score}'
        self.left_btn.disabled = True
        self.right_btn.disabled = True
        
        Clock.schedule_once(lambda dt: self.next_question(), 1.5)
    
    def show_result(self):
        stars = self.logic.calculate_stars(self.session)
        praise = self.logic.get_praise_message(self.session.accuracy)
        star_text = '★' * stars + '☆' * (3 - stars)
        self.hint_label.text = f'{star_text} {praise}'
        self.feedback_label.text = f'正确率: {self.session.accuracy*100:.0f}%'
        self.left_btn.text = '棒'
        self.right_btn.text = '棒'


class NumberQuizScreen(Screen):
    """数字测验"""
    
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.logic = GameLogic()
        self.session = None
        self.current_number = None
        self.build_ui()
    
    def build_ui(self):
        layout = BoxLayout(orientation='vertical', padding=20, spacing=15)
        with layout.canvas.before:
            Color(*get_color_from_hex('#FFF8E1'))
            self.bg = Rectangle(pos=layout.pos, size=layout.size)
        layout.bind(pos=lambda i,v: setattr(self.bg, 'pos', v),
                   size=lambda i,v: setattr(self.bg, 'size', v))
        
        # 导航栏
        nav = BoxLayout(size_hint=(1, 0.1))
        back_btn = Button(text='< 返回', size_hint=(0.15, 1), font_size='16sp',
                         background_color=get_color_from_hex('#FFC107'), background_normal='')
        back_btn.bind(on_press=lambda x: setattr(self.manager, 'current', 'math_menu'))
        nav.add_widget(back_btn)
        nav.add_widget(Label(text='【数字测验】', font_size='24sp',
                            color=get_color_from_hex('#F57F17'), bold=True, size_hint=(0.55, 1)))
        self.score_label = Label(text='得分: 0', font_size='18sp',
                                color=get_color_from_hex('#FF6B6B'), size_hint=(0.15, 1))
        nav.add_widget(self.score_label)
        self.progress_label = Label(text='0/10', font_size='16sp',
                                   color=get_color_from_hex('#666666'), size_hint=(0.15, 1))
        nav.add_widget(self.progress_label)
        layout.add_widget(nav)
        
        # 题目显示
        self.question_label = Label(text='准备好了吗？', font_size='28sp',
                                   color=get_color_from_hex('#333333'), size_hint=(1, 0.15))
        layout.add_widget(self.question_label)
        
        # 数字/图案显示区 - 深色文字
        self.display_label = Label(text='?', font_size='80sp', 
                                  color=get_color_from_hex('#F57F17'),
                                  size_hint=(1, 0.25))
        layout.add_widget(self.display_label)
        
        # 反馈区
        self.feedback_label = Label(text='', font_size='24sp',
                                   color=get_color_from_hex('#4CAF50'), size_hint=(1, 0.1))
        layout.add_widget(self.feedback_label)
        
        # 答案按钮
        self.answers_layout = GridLayout(cols=5, spacing=10, padding=10, size_hint=(1, 0.2))
        for i in range(10):
            btn = Button(text=str(i+1), font_size='24sp',
                        background_color=get_color_from_hex('#64B5F6'), background_normal='')
            btn.bind(on_press=self.on_answer)
            self.answers_layout.add_widget(btn)
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
        
        numbers = MathData.get_numbers(10)
        self.current_number = random.choice(numbers)
        num, cn, emoji = self.current_number
        
        # 用圆点代替emoji
        dot_display = {1:'●', 2:'●●', 3:'●●●', 4:'●●●●', 5:'●●●●●',
                       6:'●●●●●●', 7:'●●●●●●●', 8:'●●●●●●●●', 9:'●●●●●●●●●', 10:'●●●●●●●●●●'}
        
        q_type = random.choice(['dots', 'chinese'])
        if q_type == 'dots':
            self.question_label.text = '数一数，有几个？'
            self.display_label.text = dot_display.get(num, str(num))
        else:
            self.question_label.text = '这是数字几？'
            self.display_label.text = cn
        
        for btn in self.answers_layout.children:
            btn.disabled = False
        
        self.progress_label.text = f'{self.session.current_question + 1}/10'
    
    def on_answer(self, instance):
        if not self.current_number:
            return
        
        user_answer = int(instance.text)
        correct_answer = self.current_number[0]
        
        is_correct = self.logic.check_answer(self.session, user_answer, correct_answer)
        
        if is_correct:
            self.feedback_label.text = '太棒了！答对了！'
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


class CountGameScreen(Screen):
    """数一数游戏"""
    
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.logic = GameLogic()
        self.session = None
        self.current_count = None
        self.build_ui()
    
    def build_ui(self):
        layout = BoxLayout(orientation='vertical', padding=20, spacing=15)
        with layout.canvas.before:
            Color(*get_color_from_hex('#E0F7FA'))
            self.bg = Rectangle(pos=layout.pos, size=layout.size)
        layout.bind(pos=lambda i,v: setattr(self.bg, 'pos', v),
                   size=lambda i,v: setattr(self.bg, 'size', v))
        
        # 导航栏
        nav = BoxLayout(size_hint=(1, 0.1))
        back_btn = Button(text='< 返回', size_hint=(0.15, 1), font_size='16sp',
                         background_color=get_color_from_hex('#00BCD4'), background_normal='')
        back_btn.bind(on_press=lambda x: setattr(self.manager, 'current', 'math_menu'))
        nav.add_widget(back_btn)
        nav.add_widget(Label(text='【数一数】', font_size='24sp',
                            color=get_color_from_hex('#006064'), bold=True, size_hint=(0.55, 1)))
        self.score_label = Label(text='得分: 0', font_size='18sp',
                                color=get_color_from_hex('#FF6B6B'), size_hint=(0.15, 1))
        nav.add_widget(self.score_label)
        self.progress_label = Label(text='0/10', font_size='16sp',
                                   color=get_color_from_hex('#666666'), size_hint=(0.15, 1))
        nav.add_widget(self.progress_label)
        layout.add_widget(nav)
        
        # 题目显示
        self.question_label = Label(text='数一数有几个？', font_size='24sp',
                                   color=get_color_from_hex('#333333'), size_hint=(1, 0.1))
        layout.add_widget(self.question_label)
        
        # 图案显示区 - 深色文字
        self.display_label = Label(text='?', font_size='60sp', 
                                  color=get_color_from_hex('#00838F'),
                                  size_hint=(1, 0.35))
        layout.add_widget(self.display_label)
        
        # 反馈区
        self.feedback_label = Label(text='', font_size='24sp',
                                   color=get_color_from_hex('#4CAF50'), size_hint=(1, 0.1))
        layout.add_widget(self.feedback_label)
        
        # 答案按钮
        self.answers_layout = GridLayout(cols=5, spacing=10, padding=10, size_hint=(1, 0.2))
        for i in range(10):
            btn = Button(text=str(i+1), font_size='24sp',
                        background_color=get_color_from_hex('#4DD0E1'), background_normal='')
            btn.bind(on_press=self.on_answer)
            self.answers_layout.add_widget(btn)
        layout.add_widget(self.answers_layout)
        
        # 开始按钮
        self.start_btn = Button(text='开始游戏', font_size='20sp', size_hint=(1, 0.1),
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
        
        # 随机生成1-10个图案，用简单字符
        self.current_count = random.randint(1, 10)
        # 用简单的圆圈或O代替特殊符号
        symbols = ['O', 'o', '@', '#', '*']
        symbol = random.choice(symbols)
        # 每5个换行，方便数
        display = ''
        for i in range(self.current_count):
            display += symbol + ' '
            if (i + 1) % 5 == 0:
                display += '\n'
        self.display_label.text = display.strip()
        
        for btn in self.answers_layout.children:
            btn.disabled = False
        
        self.progress_label.text = f'{self.session.current_question + 1}/10'
    
    def on_answer(self, instance):
        if self.current_count is None:
            return
        
        user_answer = int(instance.text)
        is_correct = self.logic.check_answer(self.session, user_answer, self.current_count)
        
        if is_correct:
            self.feedback_label.text = '太棒了！数对了！'
            self.feedback_label.color = get_color_from_hex('#4CAF50')
        else:
            self.feedback_label.text = f'错误，正确答案是 {self.current_count}'
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
        self.display_label.text = '棒！'
        self.feedback_label.text = f'{praise}\n正确率: {self.session.accuracy*100:.0f}%'


class ShapesGameScreen(Screen):
    """认形状游戏"""
    
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.logic = GameLogic()
        self.session = None
        self.current_shape = None
        # 用简单字符和颜色区分形状
        self.shapes_data = [
            ('O', '圆形', '#FF6B6B'),
            ('口', '正方形', '#4ECDC4'),
            ('△', '三角形', '#FFD93D'),
            ('◇', '菱形', '#9C27B0'),
            ('☆', '五角星', '#FF9800'),
        ]
        self.build_ui()
    
    def build_ui(self):
        layout = BoxLayout(orientation='vertical', padding=20, spacing=15)
        with layout.canvas.before:
            Color(*get_color_from_hex('#F3E5F5'))
            self.bg = Rectangle(pos=layout.pos, size=layout.size)
        layout.bind(pos=lambda i,v: setattr(self.bg, 'pos', v),
                   size=lambda i,v: setattr(self.bg, 'size', v))
        
        # 导航栏
        nav = BoxLayout(size_hint=(1, 0.1))
        back_btn = Button(text='< 返回', size_hint=(0.15, 1), font_size='16sp',
                         background_color=get_color_from_hex('#9C27B0'), background_normal='')
        back_btn.bind(on_press=lambda x: setattr(self.manager, 'current', 'math_menu'))
        nav.add_widget(back_btn)
        nav.add_widget(Label(text='【认形状】', font_size='24sp',
                            color=get_color_from_hex('#6A1B9A'), bold=True, size_hint=(0.55, 1)))
        self.score_label = Label(text='得分: 0', font_size='18sp',
                                color=get_color_from_hex('#FF6B6B'), size_hint=(0.15, 1))
        nav.add_widget(self.score_label)
        self.progress_label = Label(text='0/10', font_size='16sp',
                                   color=get_color_from_hex('#666666'), size_hint=(0.15, 1))
        nav.add_widget(self.progress_label)
        layout.add_widget(nav)
        
        # 题目显示
        self.question_label = Label(text='这是什么形状？', font_size='24sp',
                                   color=get_color_from_hex('#333333'), size_hint=(1, 0.1))
        layout.add_widget(self.question_label)
        
        # 形状显示区 - 深色文字
        self.display_label = Label(text='?', font_size='120sp', 
                                  color=get_color_from_hex('#6A1B9A'),
                                  size_hint=(1, 0.35))
        layout.add_widget(self.display_label)
        
        # 反馈区
        self.feedback_label = Label(text='', font_size='24sp',
                                   color=get_color_from_hex('#4CAF50'), size_hint=(1, 0.1))
        layout.add_widget(self.feedback_label)
        
        # 答案按钮
        self.answers_layout = GridLayout(cols=5, spacing=10, padding=10, size_hint=(1, 0.2))
        layout.add_widget(self.answers_layout)
        
        # 开始按钮
        self.start_btn = Button(text='开始游戏', font_size='20sp', size_hint=(1, 0.1),
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
        
        # 随机选择一个形状
        self.current_shape = random.choice(self.shapes_data)
        symbol, name, color = self.current_shape
        self.display_label.text = symbol
        self.display_label.color = get_color_from_hex(color)
        
        # 生成选项
        self.answers_layout.clear_widgets()
        options = [s[1] for s in self.shapes_data]
        random.shuffle(options)
        
        for opt in options:
            btn = Button(text=opt, font_size='18sp',
                        background_color=get_color_from_hex('#CE93D8'), background_normal='')
            btn.bind(on_press=self.on_answer)
            self.answers_layout.add_widget(btn)
        
        self.progress_label.text = f'{self.session.current_question + 1}/10'
    
    def on_answer(self, instance):
        if self.current_shape is None:
            return
        
        user_answer = instance.text
        correct_answer = self.current_shape[1]
        is_correct = self.logic.check_answer(self.session, user_answer, correct_answer)
        
        if is_correct:
            self.feedback_label.text = f'太棒了！这是{correct_answer}！'
            self.feedback_label.color = get_color_from_hex('#4CAF50')
        else:
            self.feedback_label.text = f'错误，这是{correct_answer}'
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
        self.display_label.text = '棒！'
        self.feedback_label.text = f'{praise}\n正确率: {self.session.accuracy*100:.0f}%'


class WhackGameScreen(Screen):
    """数字打地鼠游戏"""
    
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.logic = GameLogic()
        self.session = None
        self.target_number = None
        self.holes = []  # 9个洞
        self.game_active = False
        self.spawn_event = None
        self.build_ui()
    
    def build_ui(self):
        layout = BoxLayout(orientation='vertical', padding=20, spacing=10)
        with layout.canvas.before:
            Color(*get_color_from_hex('#FFFDE7'))
            self.bg = Rectangle(pos=layout.pos, size=layout.size)
        layout.bind(pos=lambda i,v: setattr(self.bg, 'pos', v),
                   size=lambda i,v: setattr(self.bg, 'size', v))
        
        # 导航栏
        nav = BoxLayout(size_hint=(1, 0.08))
        back_btn = Button(text='< 返回', size_hint=(0.15, 1), font_size='16sp',
                         background_color=get_color_from_hex('#FFC107'), background_normal='')
        back_btn.bind(on_press=self.go_back)
        nav.add_widget(back_btn)
        nav.add_widget(Label(text='【打地鼠】', font_size='24sp',
                            color=get_color_from_hex('#F57F17'), bold=True, size_hint=(0.55, 1)))
        self.score_label = Label(text='得分: 0', font_size='18sp',
                                color=get_color_from_hex('#FF6B6B'), size_hint=(0.15, 1))
        nav.add_widget(self.score_label)
        self.round_label = Label(text='0/10', font_size='16sp',
                                color=get_color_from_hex('#666666'), size_hint=(0.15, 1))
        nav.add_widget(self.round_label)
        layout.add_widget(nav)
        
        # 目标提示
        self.target_label = Label(text='点击开始游戏！', font_size='28sp',
                                 color=get_color_from_hex('#E65100'), size_hint=(1, 0.1))
        layout.add_widget(self.target_label)
        
        # 反馈区
        self.feedback_label = Label(text='', font_size='20sp',
                                   color=get_color_from_hex('#4CAF50'), size_hint=(1, 0.08))
        layout.add_widget(self.feedback_label)
        
        # 地鼠洞网格 3x3
        self.holes_layout = GridLayout(cols=3, spacing=15, padding=20, size_hint=(1, 0.54))
        hole_colors = ['#8D6E63', '#A1887F', '#BCAAA4', '#8D6E63', '#A1887F', '#BCAAA4',
                       '#8D6E63', '#A1887F', '#BCAAA4']
        
        for i in range(9):
            hole_btn = Button(text='', font_size='48sp',
                             background_color=get_color_from_hex(hole_colors[i]), 
                             background_normal='')
            hole_btn.hole_index = i
            hole_btn.has_mole = False
            hole_btn.mole_number = None
            hole_btn.bind(on_press=self.on_hole_press)
            self.holes_layout.add_widget(hole_btn)
            self.holes.append(hole_btn)
        
        layout.add_widget(self.holes_layout)
        
        # 开始按钮
        self.start_btn = Button(text='开始游戏', font_size='20sp', size_hint=(1, 0.1),
                               background_color=get_color_from_hex('#FF9800'), background_normal='')
        self.start_btn.bind(on_press=self.start_game)
        layout.add_widget(self.start_btn)
        
        self.add_widget(layout)
    
    def go_back(self, instance):
        self.stop_game()
        self.manager.current = 'math_menu'
    
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
        # 清空所有洞
        for hole in self.holes:
            hole.text = ''
            hole.has_mole = False
            hole.mole_number = None
    
    def spawn_moles(self):
        if not self.game_active:
            return
        
        if self.session.current_question >= self.session.total_questions:
            self.show_result()
            return
        
        # 清空所有洞
        for hole in self.holes:
            hole.text = ''
            hole.has_mole = False
            hole.mole_number = None
            hole.background_color = get_color_from_hex('#8D6E63')
        
        # 生成目标数字
        self.target_number = random.randint(1, 10)
        self.target_label.text = f'快打数字 {self.target_number}！'
        
        # 随机选择3-4个洞放地鼠
        num_moles = random.randint(3, 4)
        mole_positions = random.sample(range(9), num_moles)
        
        # 确保目标数字在其中
        numbers = [self.target_number]
        while len(numbers) < num_moles:
            n = random.randint(1, 10)
            if n not in numbers:
                numbers.append(n)
        random.shuffle(numbers)
        
        # 放置地鼠
        for i, pos in enumerate(mole_positions):
            hole = self.holes[pos]
            hole.has_mole = True
            hole.mole_number = numbers[i]
            hole.text = str(numbers[i])
            hole.background_color = get_color_from_hex('#FFD54F')
        
        self.round_label.text = f'{self.session.current_question + 1}/10'
        
        # 2秒后地鼠消失
        self.spawn_event = Clock.schedule_once(self.moles_hide, 2.0)
    
    def moles_hide(self, dt):
        if not self.game_active:
            return
        
        # 检查是否错过了目标
        target_hit = False
        for hole in self.holes:
            if hole.has_mole and hole.mole_number == self.target_number:
                target_hit = False
                break
        
        if not target_hit:
            # 错过了
            self.feedback_label.text = f'错过了！目标是 {self.target_number}'
            self.feedback_label.color = get_color_from_hex('#FF9800')
            self.session.add_wrong()
        
        # 清空并生成下一轮
        Clock.schedule_once(lambda dt: self.spawn_moles(), 1.0)
    
    def on_hole_press(self, instance):
        if not self.game_active or not instance.has_mole:
            return
        
        # 取消自动隐藏
        if self.spawn_event:
            self.spawn_event.cancel()
        
        if instance.mole_number == self.target_number:
            # 打中目标
            self.session.add_correct(10)
            self.score_label.text = f'得分: {self.session.score}'
            self.feedback_label.text = '太棒了！打中了！'
            self.feedback_label.color = get_color_from_hex('#4CAF50')
            instance.background_color = get_color_from_hex('#4CAF50')
        else:
            # 打错了
            self.session.add_wrong()
            self.feedback_label.text = f'打错了！要打 {self.target_number}'
            self.feedback_label.color = get_color_from_hex('#F44336')
            instance.background_color = get_color_from_hex('#F44336')
        
        # 清空该洞
        instance.has_mole = False
        
        # 下一轮
        Clock.schedule_once(lambda dt: self.spawn_moles(), 1.0)
    
    def show_result(self):
        self.game_active = False
        stars = self.logic.calculate_stars(self.session)
        praise = self.logic.get_praise_message(self.session.accuracy)
        star_text = '★' * stars + '☆' * (3 - stars)
        self.target_label.text = f'{star_text} 游戏完成！'
        self.feedback_label.text = f'{praise}\n正确率: {self.session.accuracy*100:.0f}%'
        self.feedback_label.color = get_color_from_hex('#FF9800')
        
        # 清空所有洞
        for hole in self.holes:
            hole.text = '棒'
            hole.background_color = get_color_from_hex('#4CAF50')


class MathApp(App):
    """数学乐园独立应用（用于测试）"""
    
    def build(self):
        self.title = '乐乐的数学乐园 - Kivy版'
        sm = ScreenManager()
        sm.add_widget(MathMenuScreen(name='math_menu'))
        sm.add_widget(NumberCardsScreen(name='number_cards'))
        sm.add_widget(AdditionScreen(name='addition'))
        sm.add_widget(CompareScreen(name='compare'))
        sm.add_widget(CountGameScreen(name='count_game'))
        sm.add_widget(ShapesGameScreen(name='shapes_game'))
        sm.add_widget(WhackGameScreen(name='whack_game'))
        return sm


if __name__ == '__main__':
    MathApp().run()
