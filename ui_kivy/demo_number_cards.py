# -*- coding: utf-8 -*-
"""
Kivy 示例 - 数字卡片学习
这是一个简单的 Kivy 示例，展示如何使用 core 模块的数据
"""
import sys
import os

# 添加父目录到路径，以便导入 core 模块
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from kivy.app import App
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.gridlayout import GridLayout
from kivy.uix.button import Button
from kivy.uix.label import Label
from kivy.uix.widget import Widget
from kivy.graphics import Color, Ellipse, Rectangle, RoundedRectangle
from kivy.core.window import Window
from kivy.utils import get_color_from_hex
from kivy.clock import Clock

# 导入核心数据模块
from core.data_math import MathData

# 设置窗口大小（模拟平板）
Window.size = (800, 600)


class NumberCard(BoxLayout):
    """数字卡片组件"""
    
    def __init__(self, number_data, on_click=None, **kwargs):
        super().__init__(**kwargs)
        self.orientation = 'vertical'
        self.padding = 10
        self.spacing = 5
        
        self.number = number_data[0]  # 数字
        self.chinese = number_data[1]  # 中文
        self.emoji = number_data[2]    # emoji表示
        self.on_click_callback = on_click
        
        # 背景色
        self.bg_color = get_color_from_hex('#FF6B6B')
        
        with self.canvas.before:
            Color(*self.bg_color)
            self.rect = RoundedRectangle(pos=self.pos, size=self.size, radius=[20])
        
        self.bind(pos=self.update_rect, size=self.update_rect)
        
        # 数字显示
        self.number_label = Label(
            text=str(self.number),
            font_size='60sp',
            color=(1, 1, 1, 1),
            bold=True,
            size_hint=(1, 0.4)
        )
        self.add_widget(self.number_label)
        
        # 中文显示
        self.chinese_label = Label(
            text=self.chinese,
            font_size='30sp',
            color=(1, 1, 1, 1),
            size_hint=(1, 0.2)
        )
        self.add_widget(self.chinese_label)
        
        # Emoji 显示
        self.emoji_label = Label(
            text=self.emoji,
            font_size='24sp',
            size_hint=(1, 0.3)
        )
        self.add_widget(self.emoji_label)
        
        # 点击事件
        self.bind(on_touch_down=self.on_touch)
    
    def update_rect(self, *args):
        self.rect.pos = self.pos
        self.rect.size = self.size
    
    def on_touch(self, instance, touch):
        if self.collide_point(*touch.pos):
            if self.on_click_callback:
                self.on_click_callback(self.number)
            return True
        return False


class NumberCardsScreen(BoxLayout):
    """数字卡片主界面"""
    
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.orientation = 'vertical'
        self.padding = 20
        self.spacing = 10
        
        # 背景色
        with self.canvas.before:
            Color(*get_color_from_hex('#E3F2FD'))
            self.bg_rect = Rectangle(pos=self.pos, size=self.size)
        self.bind(pos=self.update_bg, size=self.update_bg)
        
        # 标题栏
        title_layout = BoxLayout(size_hint=(1, 0.12), spacing=10)
        
        # 返回按钮
        back_btn = Button(
            text='🏠 返回',
            font_size='18sp',
            size_hint=(0.15, 1),
            background_color=get_color_from_hex('#96CEB4'),
            background_normal=''
        )
        title_layout.add_widget(back_btn)
        
        # 标题
        title = Label(
            text='🔢 数字卡片学习 🔢',
            font_size='28sp',
            color=get_color_from_hex('#1976D2'),
            bold=True,
            size_hint=(0.7, 1)
        )
        title_layout.add_widget(title)
        
        # 分数
        self.score_label = Label(
            text='⭐ 0',
            font_size='20sp',
            color=get_color_from_hex('#FF6B6B'),
            size_hint=(0.15, 1)
        )
        title_layout.add_widget(self.score_label)
        
        self.add_widget(title_layout)
        
        # 提示文字
        self.hint_label = Label(
            text='点击卡片学习数字！',
            font_size='18sp',
            color=get_color_from_hex('#666666'),
            size_hint=(1, 0.08)
        )
        self.add_widget(self.hint_label)
        
        # 卡片网格
        self.cards_grid = GridLayout(
            cols=5,
            spacing=15,
            padding=10,
            size_hint=(1, 0.7)
        )
        
        # 获取数字数据并创建卡片
        numbers = MathData.get_numbers(10)
        colors = ['#FF6B6B', '#4ECDC4', '#45B7D1', '#96CEB4', '#DDA0DD',
                  '#FFD93D', '#FF9800', '#8BC34A', '#E91E63', '#9C27B0']
        
        for i, num_data in enumerate(numbers):
            card = NumberCard(
                num_data,
                on_click=self.on_card_click,
                size_hint=(1, 1)
            )
            # 设置不同颜色
            card.bg_color = get_color_from_hex(colors[i % len(colors)])
            card.canvas.before.clear()
            with card.canvas.before:
                Color(*card.bg_color)
                card.rect = RoundedRectangle(pos=card.pos, size=card.size, radius=[20])
            
            self.cards_grid.add_widget(card)
        
        self.add_widget(self.cards_grid)
        
        # 底部按钮
        bottom_layout = BoxLayout(size_hint=(1, 0.1), spacing=20, padding=[100, 0])
        
        quiz_btn = Button(
            text='🎯 开始测验',
            font_size='18sp',
            background_color=get_color_from_hex('#4ECDC4'),
            background_normal=''
        )
        quiz_btn.bind(on_press=self.start_quiz)
        bottom_layout.add_widget(quiz_btn)
        
        self.add_widget(bottom_layout)
        
        self.score = 0
    
    def update_bg(self, *args):
        self.bg_rect.pos = self.pos
        self.bg_rect.size = self.size
    
    def on_card_click(self, number):
        """点击卡片"""
        self.hint_label.text = f'你点击了数字 {number}！'
        # 这里可以添加语音播放
        print(f"点击数字: {number}")
    
    def start_quiz(self, instance):
        """开始测验"""
        self.hint_label.text = '测验功能开发中...'


class NumberCardsApp(App):
    """数字卡片应用"""
    
    def build(self):
        self.title = '乐乐的数学乐园 - Kivy版'
        return NumberCardsScreen()


if __name__ == '__main__':
    NumberCardsApp().run()
