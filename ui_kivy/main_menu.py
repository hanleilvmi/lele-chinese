# -*- coding: utf-8 -*-
"""
Kivy 主菜单示例
展示如何创建类似 Tkinter 版本的主菜单界面
"""
import sys
import os
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from kivy.app import App
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.gridlayout import GridLayout
from kivy.uix.button import Button
from kivy.uix.label import Label
from kivy.uix.screenmanager import ScreenManager, Screen
from kivy.graphics import Color, Rectangle, RoundedRectangle
from kivy.core.window import Window
from kivy.utils import get_color_from_hex

# 设置窗口大小
Window.size = (900, 700)


class GameCard(BoxLayout):
    """游戏卡片组件"""
    
    def __init__(self, icon, title, desc, color, callback=None, **kwargs):
        super().__init__(**kwargs)
        self.orientation = 'vertical'
        self.padding = 8
        self.spacing = 5
        self.callback = callback
        
        # 背景
        self.bg_color = get_color_from_hex(color)
        with self.canvas.before:
            Color(*self.bg_color)
            self.rect = RoundedRectangle(pos=self.pos, size=self.size, radius=[15])
        self.bind(pos=self.update_rect, size=self.update_rect)
        
        # 图标
        self.add_widget(Label(
            text=icon,
            font_size='40sp',
            size_hint=(1, 0.5)
        ))
        
        # 标题
        self.add_widget(Label(
            text=title,
            font_size='16sp',
            color=(1, 1, 1, 1),
            bold=True,
            size_hint=(1, 0.3)
        ))
        
        # 描述
        self.add_widget(Label(
            text=desc,
            font_size='12sp',
            color=(1, 1, 1, 0.9),
            size_hint=(1, 0.2)
        ))
        
        self.bind(on_touch_down=self.on_touch)
    
    def update_rect(self, *args):
        self.rect.pos = self.pos
        self.rect.size = self.size
    
    def on_touch(self, instance, touch):
        if self.collide_point(*touch.pos):
            if self.callback:
                self.callback()
            return True
        return False


class MainMenuScreen(Screen):
    """主菜单界面"""
    
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        
        layout = BoxLayout(orientation='vertical', padding=20, spacing=15)
        
        # 背景
        with layout.canvas.before:
            Color(*get_color_from_hex('#E3F2FD'))
            self.bg = Rectangle(pos=layout.pos, size=layout.size)
        layout.bind(pos=self.update_bg, size=self.update_bg)
        self.layout = layout
        
        # 标题区
        title_box = BoxLayout(size_hint=(1, 0.12), spacing=10)
        title_box.add_widget(Label(
            text='🐾 乐乐的学习乐园 🐾',
            font_size='32sp',
            color=get_color_from_hex('#1976D2'),
            bold=True
        ))
        layout.add_widget(title_box)
        
        # 副标题
        layout.add_widget(Label(
            text='汪汪队陪你快乐学习！',
            font_size='16sp',
            color=get_color_from_hex('#666666'),
            size_hint=(1, 0.05)
        ))
        
        # 游戏选择区
        games_layout = GridLayout(cols=3, spacing=15, size_hint=(1, 0.65), padding=10)
        
        games = [
            ('🔤', '拼音乐园', '学拼音', '#FF6B6B', self.go_pinyin),
            ('🔢', '数学乐园', '学数学', '#4ECDC4', self.go_math),
            ('🔤', '英语乐园', '学英语', '#45B7D1', self.go_english),
            ('🧠', '思维乐园', '动脑筋', '#9C27B0', self.go_thinking),
            ('📚', '识字乐园', '学汉字', '#FF9800', self.go_chinese),
            ('🚗', '交通乐园', '学交通', '#8BC34A', self.go_vehicles),
        ]
        
        for icon, title, desc, color, callback in games:
            card = GameCard(icon, title, desc, color, callback)
            games_layout.add_widget(card)
        
        layout.add_widget(games_layout)
        
        # 底部按钮
        bottom = BoxLayout(size_hint=(1, 0.1), spacing=20, padding=[200, 0])
        
        settings_btn = Button(
            text='⚙️ 设置',
            font_size='16sp',
            background_color=get_color_from_hex('#9E9E9E'),
            background_normal=''
        )
        bottom.add_widget(settings_btn)
        
        exit_btn = Button(
            text='👋 退出',
            font_size='16sp',
            background_color=get_color_from_hex('#FF6B6B'),
            background_normal=''
        )
        exit_btn.bind(on_press=self.exit_app)
        bottom.add_widget(exit_btn)
        
        layout.add_widget(bottom)
        self.add_widget(layout)
    
    def update_bg(self, instance, value):
        self.bg.pos = instance.pos
        self.bg.size = instance.size
    
    def go_pinyin(self):
        print("进入拼音乐园")
        # self.manager.current = 'pinyin'
    
    def go_math(self):
        print("进入数学乐园")
        self.manager.current = 'math'
    
    def go_english(self):
        print("进入英语乐园")
    
    def go_thinking(self):
        print("进入思维乐园")
    
    def go_chinese(self):
        print("进入识字乐园")
    
    def go_vehicles(self):
        print("进入交通乐园")
    
    def exit_app(self, instance):
        App.get_running_app().stop()


class MathScreen(Screen):
    """数学乐园界面（简化版）"""
    
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        
        layout = BoxLayout(orientation='vertical', padding=20, spacing=15)
        
        with layout.canvas.before:
            Color(*get_color_from_hex('#E8F5E9'))
            self.bg = Rectangle(pos=layout.pos, size=layout.size)
        layout.bind(pos=self.update_bg, size=self.update_bg)
        self.layout = layout
        
        # 顶部导航
        nav = BoxLayout(size_hint=(1, 0.1))
        back_btn = Button(
            text='🏠 返回',
            size_hint=(0.2, 1),
            font_size='16sp',
            background_color=get_color_from_hex('#96CEB4'),
            background_normal=''
        )
        back_btn.bind(on_press=self.go_back)
        nav.add_widget(back_btn)
        
        nav.add_widget(Label(
            text='🔢 数学乐园 🔢',
            font_size='28sp',
            color=get_color_from_hex('#2E7D32'),
            bold=True,
            size_hint=(0.6, 1)
        ))
        
        nav.add_widget(Label(
            text='⭐ 0',
            font_size='18sp',
            color=get_color_from_hex('#FF6B6B'),
            size_hint=(0.2, 1)
        ))
        layout.add_widget(nav)
        
        # 游戏选择
        games = GridLayout(cols=3, spacing=15, size_hint=(1, 0.7), padding=20)
        
        math_games = [
            ('🔢', '数字卡片', '认数字', '#FF6B6B'),
            ('📊', '数一数', '数数量', '#4ECDC4'),
            ('🔺', '认形状', '学形状', '#96CEB4'),
            ('⚖️', '比大小', '谁更大', '#45B7D1'),
            ('➕', '学加法', '做加法', '#DDA0DD'),
            ('🔨', '打地鼠', '快反应', '#FFD93D'),
        ]
        
        for icon, title, desc, color in math_games:
            card = GameCard(icon, title, desc, color)
            games.add_widget(card)
        
        layout.add_widget(games)
        self.add_widget(layout)
    
    def update_bg(self, instance, value):
        self.bg.pos = instance.pos
        self.bg.size = instance.size
    
    def go_back(self, instance):
        self.manager.current = 'main'


class LearningApp(App):
    """学习乐园主应用"""
    
    def build(self):
        self.title = '乐乐的学习乐园 - Kivy版'
        
        # 创建屏幕管理器
        sm = ScreenManager()
        sm.add_widget(MainMenuScreen(name='main'))
        sm.add_widget(MathScreen(name='math'))
        
        return sm


if __name__ == '__main__':
    LearningApp().run()
