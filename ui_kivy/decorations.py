# -*- coding: utf-8 -*-
"""
趣味装饰模块 - 用Canvas绘制可爱的装饰图形
代替Emoji，增加儿童应用的趣味性
"""
from kivy.uix.widget import Widget
from kivy.graphics import Color, Ellipse, Line, Rectangle, Triangle
from kivy.metrics import dp
from kivy.clock import Clock
from kivy.animation import Animation
import random
import math


class StarWidget(Widget):
    """可爱的星星装饰"""
    def __init__(self, color=(1, 0.8, 0), **kwargs):
        super().__init__(**kwargs)
        self.star_color = color
        self.bind(size=self.draw, pos=self.draw)
        Clock.schedule_once(lambda dt: self.draw(), 0)
    
    def draw(self, *args):
        self.canvas.clear()
        cx, cy = self.center_x, self.center_y
        r = min(self.width, self.height) * 0.4
        with self.canvas:
            Color(*self.star_color)
            # 五角星
            points = []
            for i in range(5):
                angle = math.radians(90 + i * 72)
                points.extend([cx + r * math.cos(angle), cy + r * math.sin(angle)])
                angle = math.radians(90 + i * 72 + 36)
                points.extend([cx + r * 0.4 * math.cos(angle), cy + r * 0.4 * math.sin(angle)])
            Line(points=points, width=dp(2), close=True)


class HeartWidget(Widget):
    """可爱的爱心装饰"""
    def __init__(self, color=(1, 0.4, 0.4), **kwargs):
        super().__init__(**kwargs)
        self.heart_color = color
        self.bind(size=self.draw, pos=self.draw)
        Clock.schedule_once(lambda dt: self.draw(), 0)
    
    def draw(self, *args):
        self.canvas.clear()
        cx, cy = self.center_x, self.center_y
        r = min(self.width, self.height) * 0.3
        with self.canvas:
            Color(*self.heart_color)
            # 两个圆形成爱心顶部
            Ellipse(pos=(cx - r * 1.1, cy), size=(r * 1.2, r * 1.2))
            Ellipse(pos=(cx - r * 0.1, cy), size=(r * 1.2, r * 1.2))
            # 三角形成爱心底部
            Triangle(points=[cx - r * 1.2, cy + r * 0.3, cx + r * 1.2, cy + r * 0.3, cx, cy - r * 1.2])


class SunWidget(Widget):
    """可爱的太阳装饰"""
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.bind(size=self.draw, pos=self.draw)
        Clock.schedule_once(lambda dt: self.draw(), 0)
    
    def draw(self, *args):
        self.canvas.clear()
        cx, cy = self.center_x, self.center_y
        r = min(self.width, self.height) * 0.25
        with self.canvas:
            # 太阳本体
            Color(1, 0.8, 0)
            Ellipse(pos=(cx - r, cy - r), size=(r * 2, r * 2))
            # 光芒
            Color(1, 0.6, 0)
            for i in range(8):
                angle = math.radians(i * 45)
                x1 = cx + r * 1.3 * math.cos(angle)
                y1 = cy + r * 1.3 * math.sin(angle)
                x2 = cx + r * 1.8 * math.cos(angle)
                y2 = cy + r * 1.8 * math.sin(angle)
                Line(points=[x1, y1, x2, y2], width=dp(3))


class CloudWidget(Widget):
    """可爱的云朵装饰"""
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.bind(size=self.draw, pos=self.draw)
        Clock.schedule_once(lambda dt: self.draw(), 0)
    
    def draw(self, *args):
        self.canvas.clear()
        cx, cy = self.center_x, self.center_y
        r = min(self.width, self.height) * 0.2
        with self.canvas:
            Color(1, 1, 1)
            # 多个圆组成云朵
            Ellipse(pos=(cx - r * 2, cy - r * 0.5), size=(r * 1.5, r * 1.5))
            Ellipse(pos=(cx - r * 0.8, cy), size=(r * 1.8, r * 1.8))
            Ellipse(pos=(cx + r * 0.5, cy - r * 0.3), size=(r * 1.4, r * 1.4))
            Ellipse(pos=(cx - r * 1.5, cy - r), size=(r * 1.2, r * 1.2))
            Ellipse(pos=(cx + r * 0.2, cy - r * 0.8), size=(r * 1.3, r * 1.3))


class FlowerWidget(Widget):
    """可爱的花朵装饰"""
    def __init__(self, petal_color=(1, 0.5, 0.7), **kwargs):
        super().__init__(**kwargs)
        self.petal_color = petal_color
        self.bind(size=self.draw, pos=self.draw)
        Clock.schedule_once(lambda dt: self.draw(), 0)
    
    def draw(self, *args):
        self.canvas.clear()
        cx, cy = self.center_x, self.center_y
        r = min(self.width, self.height) * 0.2
        with self.canvas:
            # 花瓣
            Color(*self.petal_color)
            for i in range(5):
                angle = math.radians(i * 72)
                px = cx + r * 0.8 * math.cos(angle)
                py = cy + r * 0.8 * math.sin(angle)
                Ellipse(pos=(px - r * 0.5, py - r * 0.5), size=(r, r))
            # 花心
            Color(1, 0.9, 0)
            Ellipse(pos=(cx - r * 0.4, cy - r * 0.4), size=(r * 0.8, r * 0.8))


class ButterflyWidget(Widget):
    """可爱的蝴蝶装饰"""
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.bind(size=self.draw, pos=self.draw)
        Clock.schedule_once(lambda dt: self.draw(), 0)
    
    def draw(self, *args):
        self.canvas.clear()
        cx, cy = self.center_x, self.center_y
        r = min(self.width, self.height) * 0.25
        with self.canvas:
            # 翅膀
            Color(0.9, 0.5, 0.9)
            Ellipse(pos=(cx - r * 1.5, cy - r * 0.3), size=(r * 1.2, r * 1.5))
            Ellipse(pos=(cx + r * 0.3, cy - r * 0.3), size=(r * 1.2, r * 1.5))
            Color(0.7, 0.3, 0.7)
            Ellipse(pos=(cx - r * 1.2, cy - r * 0.8), size=(r * 0.8, r * 1))
            Ellipse(pos=(cx + r * 0.4, cy - r * 0.8), size=(r * 0.8, r * 1))
            # 身体
            Color(0.3, 0.2, 0.1)
            Ellipse(pos=(cx - r * 0.15, cy - r * 0.8), size=(r * 0.3, r * 1.2))
            # 触角
            Line(points=[cx, cy + r * 0.4, cx - r * 0.3, cy + r * 0.8], width=dp(1))
            Line(points=[cx, cy + r * 0.4, cx + r * 0.3, cy + r * 0.8], width=dp(1))


class RainbowWidget(Widget):
    """可爱的彩虹装饰"""
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.bind(size=self.draw, pos=self.draw)
        Clock.schedule_once(lambda dt: self.draw(), 0)
    
    def draw(self, *args):
        self.canvas.clear()
        cx, cy = self.center_x, self.center_y - self.height * 0.2
        r = min(self.width, self.height) * 0.8
        colors = [(1, 0, 0), (1, 0.5, 0), (1, 1, 0), (0, 1, 0), (0, 0.5, 1), (0.3, 0, 0.5), (0.5, 0, 0.5)]
        with self.canvas:
            for i, color in enumerate(colors):
                Color(*color)
                radius = r - i * r * 0.08
                Line(ellipse=(cx - radius, cy - radius, radius * 2, radius * 2, 0, 180), width=dp(4))


class PawPrintWidget(Widget):
    """可爱的爪印装饰（汪汪队主题）"""
    def __init__(self, color=(0.6, 0.4, 0.2), **kwargs):
        super().__init__(**kwargs)
        self.paw_color = color
        self.bind(size=self.draw, pos=self.draw)
        Clock.schedule_once(lambda dt: self.draw(), 0)
    
    def draw(self, *args):
        self.canvas.clear()
        cx, cy = self.center_x, self.center_y
        r = min(self.width, self.height) * 0.15
        with self.canvas:
            Color(*self.paw_color)
            # 大肉垫
            Ellipse(pos=(cx - r * 1.2, cy - r * 1.5), size=(r * 2.4, r * 2))
            # 四个小肉垫
            Ellipse(pos=(cx - r * 1.8, cy + r * 0.3), size=(r * 1.1, r * 1.3))
            Ellipse(pos=(cx - r * 0.5, cy + r * 0.8), size=(r * 1.1, r * 1.3))
            Ellipse(pos=(cx + r * 0.7, cy + r * 0.3), size=(r * 1.1, r * 1.3))
            Ellipse(pos=(cx - r * 1.8, cy - r * 0.5), size=(r * 0.9, r * 1.1))


def create_floating_decorations(parent, count=5):
    """在父组件上创建漂浮的装饰"""
    decorations = [StarWidget, HeartWidget, FlowerWidget]
    colors = [(1, 0.8, 0), (1, 0.4, 0.4), (0.4, 0.8, 1), (0.9, 0.5, 0.9), (0.5, 0.9, 0.5)]
    
    for i in range(count):
        deco_class = random.choice(decorations)
        size = random.randint(30, 50)
        x = random.randint(0, int(parent.width - size)) if parent.width > size else 0
        y = random.randint(0, int(parent.height - size)) if parent.height > size else 0
        
        if deco_class == StarWidget:
            deco = deco_class(color=random.choice(colors), size_hint=(None, None), size=(dp(size), dp(size)), pos=(x, y))
        elif deco_class == HeartWidget:
            deco = deco_class(color=(1, random.uniform(0.3, 0.5), random.uniform(0.3, 0.5)), size_hint=(None, None), size=(dp(size), dp(size)), pos=(x, y))
        else:
            deco = deco_class(size_hint=(None, None), size=(dp(size), dp(size)), pos=(x, y))
        
        deco.opacity = 0.6
        parent.add_widget(deco)
        
        # 添加漂浮动画
        animate_float(deco)
    
    return parent


def animate_float(widget):
    """让装饰漂浮动画"""
    original_y = widget.y
    anim = Animation(y=original_y + dp(15), duration=random.uniform(1.5, 2.5), t='in_out_sine')
    anim += Animation(y=original_y, duration=random.uniform(1.5, 2.5), t='in_out_sine')
    anim.repeat = True
    anim.start(widget)


def create_confetti_burst(parent, x, y, count=10):
    """创建彩色纸屑爆炸效果"""
    colors = [(1, 0, 0), (1, 0.5, 0), (1, 1, 0), (0, 1, 0), (0, 0.5, 1), (0.5, 0, 0.5), (1, 0.4, 0.7)]
    
    for i in range(count):
        confetti = Widget(size_hint=(None, None), size=(dp(10), dp(10)), pos=(x, y))
        color = random.choice(colors)
        with confetti.canvas:
            Color(*color)
            if random.random() > 0.5:
                Ellipse(pos=(0, 0), size=(dp(10), dp(10)))
            else:
                Rectangle(pos=(0, 0), size=(dp(8), dp(8)))
        
        parent.add_widget(confetti)
        
        # 随机方向飞出
        end_x = x + random.randint(-150, 150)
        end_y = y + random.randint(-50, 150)
        
        anim = Animation(pos=(end_x, end_y), opacity=0, duration=random.uniform(0.8, 1.2), t='out_quad')
        anim.bind(on_complete=lambda a, w: parent.remove_widget(w))
        anim.start(confetti)
