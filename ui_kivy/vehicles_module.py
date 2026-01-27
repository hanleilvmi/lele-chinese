# -*- coding: utf-8 -*-
"""
Kivy 交通乐园模块
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

from core.data_vehicles import VehiclesData
from core.game_logic import GameLogic, GameType

Window.size = (900, 700)


class VehiclesMenuScreen(Screen):
    """交通乐园菜单"""
    
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        layout = BoxLayout(orientation='vertical', padding=20, spacing=15)
        
        with layout.canvas.before:
            Color(*get_color_from_hex('#E8F5E9'))
            self.bg = Rectangle(pos=layout.pos, size=layout.size)
        layout.bind(pos=lambda i,v: setattr(self.bg, 'pos', v),
                   size=lambda i,v: setattr(self.bg, 'size', v))
        
        # 导航栏
        nav = BoxLayout(size_hint=(1, 0.1))
        back_btn = Button(text='< 返回', size_hint=(0.2, 1), font_size='16sp',
                         background_color=get_color_from_hex('#66BB6A'), background_normal='')
        back_btn.bind(on_press=self.go_back)
        nav.add_widget(back_btn)
        nav.add_widget(Label(text='【交通乐园】', font_size='28sp',
                            color=get_color_from_hex('#2E7D32'), bold=True, size_hint=(0.6, 1)))
        nav.add_widget(Label(text='', size_hint=(0.2, 1)))
        layout.add_widget(nav)
        
        # 游戏选择
        games = GridLayout(cols=2, spacing=15, size_hint=(1, 0.75), padding=20)
        game_list = [
            ('车', '认交通工具', '学习各种车', '#66BB6A', lambda: self.go_game('learn')),
            ('灯', '红绿灯', '交通规则', '#EF5350', lambda: self.go_game('traffic')),
            ('狗', '汪汪队', '认识狗狗', '#42A5F5', lambda: self.go_game('paw')),
            ('?', '交通测验', '考考你', '#FFA726', lambda: self.go_game('quiz')),
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
        screens = {
            'learn': 'vehicles_learn',
            'traffic': 'traffic_light',
            'paw': 'paw_patrol',
            'quiz': 'vehicles_quiz'
        }
        if game_name in screens:
            self.manager.current = screens[game_name]


class VehiclesLearnScreen(Screen):
    """认交通工具"""
    
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
        
        # 导航栏
        nav = BoxLayout(size_hint=(1, 0.1))
        back_btn = Button(text='< 返回', size_hint=(0.15, 1), font_size='16sp',
                         background_color=get_color_from_hex('#66BB6A'), background_normal='')
        back_btn.bind(on_press=lambda x: setattr(self.manager, 'current', 'vehicles_menu'))
        nav.add_widget(back_btn)
        nav.add_widget(Label(text='【认交通工具】', font_size='24sp',
                            color=get_color_from_hex('#2E7D32'), bold=True, size_hint=(0.7, 1)))
        nav.add_widget(Label(text='', size_hint=(0.15, 1)))
        layout.add_widget(nav)
        
        # 提示
        self.hint = Label(text='点击卡片学习交通工具！', font_size='18sp',
                         color=get_color_from_hex('#666666'), size_hint=(1, 0.08))
        layout.add_widget(self.hint)
        
        # 交通工具卡片
        grid = GridLayout(cols=5, spacing=10, padding=10, size_hint=(1, 0.72))
        vehicles = VehiclesData.get_vehicles()[:10]  # 取前10个
        
        for name, vtype, emoji, color, desc in vehicles:
            btn = Button(background_normal='', background_color=get_color_from_hex(color))
            btn.markup = True
            btn.text = f'[size=24][b]{name}[/b][/size]\n[size=12]{desc}[/size]'
            btn.vehicle_data = (name, vtype, desc)
            btn.bind(on_press=self.on_card_press)
            grid.add_widget(btn)
        
        layout.add_widget(grid)
        self.add_widget(layout)
    
    def on_card_press(self, instance):
        if hasattr(instance, 'vehicle_data'):
            name, vtype, desc = instance.vehicle_data
            self.hint.text = f'{name} - {vtype}交通工具，{desc}'


class TrafficLightScreen(Screen):
    """红绿灯游戏"""
    
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.logic = GameLogic()
        self.session = None
        self.current_light = None
        self.build_ui()
    
    def build_ui(self):
        layout = BoxLayout(orientation='vertical', padding=20, spacing=15)
        with layout.canvas.before:
            Color(*get_color_from_hex('#FFEBEE'))
            self.bg = Rectangle(pos=layout.pos, size=layout.size)
        layout.bind(pos=lambda i,v: setattr(self.bg, 'pos', v),
                   size=lambda i,v: setattr(self.bg, 'size', v))
        
        # 导航栏
        nav = BoxLayout(size_hint=(1, 0.1))
        back_btn = Button(text='< 返回', size_hint=(0.15, 1), font_size='16sp',
                         background_color=get_color_from_hex('#EF5350'), background_normal='')
        back_btn.bind(on_press=lambda x: setattr(self.manager, 'current', 'vehicles_menu'))
        nav.add_widget(back_btn)
        nav.add_widget(Label(text='【红绿灯】', font_size='24sp',
                            color=get_color_from_hex('#C62828'), bold=True, size_hint=(0.55, 1)))
        self.score_label = Label(text='得分: 0', font_size='18sp',
                                color=get_color_from_hex('#FF6B6B'), size_hint=(0.15, 1))
        nav.add_widget(self.score_label)
        self.progress_label = Label(text='0/10', font_size='16sp',
                                   color=get_color_from_hex('#666666'), size_hint=(0.15, 1))
        nav.add_widget(self.progress_label)
        layout.add_widget(nav)
        
        # 题目
        self.question_label = Label(text='看到这个灯，应该怎么做？', font_size='24sp',
                                   color=get_color_from_hex('#333333'), size_hint=(1, 0.1))
        layout.add_widget(self.question_label)
        
        # 灯显示
        self.display_label = Label(text='?', font_size='100sp', size_hint=(1, 0.3))
        layout.add_widget(self.display_label)
        
        # 反馈
        self.feedback_label = Label(text='', font_size='24sp',
                                   color=get_color_from_hex('#4CAF50'), size_hint=(1, 0.1))
        layout.add_widget(self.feedback_label)

        # 选项
        self.answers_layout = GridLayout(cols=3, spacing=15, padding=20, size_hint=(1, 0.2))
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
        
        rules = VehiclesData.get_traffic_rules()[:3]
        self.current_light = random.choice(rules)
        name, action, symbol, desc = self.current_light
        
        # 用颜色文字代替emoji
        color_map = {'红灯': '#F44336', '绿灯': '#4CAF50', '黄灯': '#FFC107'}
        self.display_label.text = name
        self.display_label.color = get_color_from_hex(color_map.get(name, '#333333'))
        
        self.answers_layout.clear_widgets()
        for opt in ['停', '行', '等']:
            btn = Button(text=opt, font_size='36sp',
                        background_color=get_color_from_hex('#64B5F6'), background_normal='')
            btn.bind(on_press=self.on_answer)
            self.answers_layout.add_widget(btn)
        
        self.progress_label.text = f'{self.session.current_question + 1}/10'
    
    def on_answer(self, instance):
        if self.current_light is None:
            return
        correct = self.current_light[1]
        is_correct = self.logic.check_answer(self.session, instance.text, correct)
        if is_correct:
            self.feedback_label.text = f'正确！{self.current_light[3]}'
            self.feedback_label.color = get_color_from_hex('#4CAF50')
        else:
            self.feedback_label.text = f'错误，{self.current_light[3]}'
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
        self.display_label.color = get_color_from_hex('#4CAF50')
        self.feedback_label.text = f'{praise}\n正确率: {self.session.accuracy*100:.0f}%'


class PawPatrolScreen(Screen):
    """汪汪队"""
    
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
        back_btn.bind(on_press=lambda x: setattr(self.manager, 'current', 'vehicles_menu'))
        nav.add_widget(back_btn)
        nav.add_widget(Label(text='【汪汪队】', font_size='24sp',
                            color=get_color_from_hex('#1565C0'), bold=True, size_hint=(0.7, 1)))
        nav.add_widget(Label(text='', size_hint=(0.15, 1)))
        layout.add_widget(nav)
        
        self.hint = Label(text='点击认识汪汪队的狗狗们！', font_size='18sp',
                         color=get_color_from_hex('#666666'), size_hint=(1, 0.08))
        layout.add_widget(self.hint)
        
        grid = GridLayout(cols=5, spacing=10, padding=10, size_hint=(1, 0.72))
        paw_data = VehiclesData.get_paw_patrol()
        
        for pup_id, info in paw_data.items():
            btn = Button(background_normal='', background_color=get_color_from_hex(info['color']))
            btn.markup = True
            btn.text = f'[size=20][b]{info["name"]}[/b][/size]\n[size=12]{info["role"]}[/size]'
            btn.pup_info = info
            btn.bind(on_press=self.on_card_press)
            grid.add_widget(btn)
        
        layout.add_widget(grid)
        self.add_widget(layout)
    
    def on_card_press(self, instance):
        if hasattr(instance, 'pup_info'):
            info = instance.pup_info
            self.hint.text = f'{info["name"]} - {info["role"]}，开{info["vehicle"]}'


class VehiclesQuizScreen(Screen):
    """交通测验"""
    
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.logic = GameLogic()
        self.session = None
        self.current_vehicle = None
        self.build_ui()
    
    def build_ui(self):
        layout = BoxLayout(orientation='vertical', padding=20, spacing=15)
        with layout.canvas.before:
            Color(*get_color_from_hex('#FFF3E0'))
            self.bg = Rectangle(pos=layout.pos, size=layout.size)
        layout.bind(pos=lambda i,v: setattr(self.bg, 'pos', v),
                   size=lambda i,v: setattr(self.bg, 'size', v))
        
        nav = BoxLayout(size_hint=(1, 0.1))
        back_btn = Button(text='< 返回', size_hint=(0.15, 1), font_size='16sp',
                         background_color=get_color_from_hex('#FFA726'), background_normal='')
        back_btn.bind(on_press=lambda x: setattr(self.manager, 'current', 'vehicles_menu'))
        nav.add_widget(back_btn)
        nav.add_widget(Label(text='【交通测验】', font_size='24sp',
                            color=get_color_from_hex('#E65100'), bold=True, size_hint=(0.55, 1)))
        self.score_label = Label(text='得分: 0', font_size='18sp',
                                color=get_color_from_hex('#FF6B6B'), size_hint=(0.15, 1))
        nav.add_widget(self.score_label)
        self.progress_label = Label(text='0/10', font_size='16sp',
                                   color=get_color_from_hex('#666666'), size_hint=(0.15, 1))
        nav.add_widget(self.progress_label)
        layout.add_widget(nav)
        
        self.question_label = Label(text='这是什么交通工具？', font_size='24sp',
                                   color=get_color_from_hex('#333333'), size_hint=(1, 0.1))
        layout.add_widget(self.question_label)
        
        self.display_label = Label(text='?', font_size='48sp',
                                  color=get_color_from_hex('#E65100'), size_hint=(1, 0.25))
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
        vehicles = VehiclesData.get_vehicles()
        self.current_vehicle = random.choice(vehicles)
        name, vtype, emoji, color, desc = self.current_vehicle
        self.display_label.text = desc
        self.answers_layout.clear_widgets()
        all_names = [v[0] for v in vehicles]
        options = self.logic.get_random_options(name, all_names, count=4)
        for opt in options:
            btn = Button(text=opt, font_size='20sp',
                        background_color=get_color_from_hex('#64B5F6'), background_normal='')
            btn.bind(on_press=self.on_answer)
            self.answers_layout.add_widget(btn)
        self.progress_label.text = f'{self.session.current_question + 1}/10'
    
    def on_answer(self, instance):
        if self.current_vehicle is None:
            return
        correct = self.current_vehicle[0]
        is_correct = self.logic.check_answer(self.session, instance.text, correct)
        if is_correct:
            self.feedback_label.text = f'正确！这是{correct}'
            self.feedback_label.color = get_color_from_hex('#4CAF50')
        else:
            self.feedback_label.text = f'错误，正确答案是{correct}'
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


class VehiclesApp(App):
    def build(self):
        self.title = '乐乐的交通乐园 - Kivy版'
        sm = ScreenManager()
        sm.add_widget(VehiclesMenuScreen(name='vehicles_menu'))
        sm.add_widget(VehiclesLearnScreen(name='vehicles_learn'))
        sm.add_widget(TrafficLightScreen(name='traffic_light'))
        sm.add_widget(PawPatrolScreen(name='paw_patrol'))
        sm.add_widget(VehiclesQuizScreen(name='vehicles_quiz'))
        return sm


if __name__ == '__main__':
    VehiclesApp().run()
