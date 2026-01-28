# -*- coding: utf-8 -*-
"""
趣味装饰模块 - 用Canvas绘制可爱的装饰图形和动画
代替Emoji，增加儿童应用的趣味性
v2.0 - 大幅扩展，更多图案和动画
"""
from kivy.uix.widget import Widget
from kivy.uix.floatlayout import FloatLayout
from kivy.graphics import Color, Ellipse, Line, Rectangle, Triangle, Rotate, PushMatrix, PopMatrix
from kivy.graphics.instructions import InstructionGroup
from kivy.metrics import dp
from kivy.clock import Clock
from kivy.animation import Animation
from kivy.properties import NumericProperty, ListProperty
import random
import math


# ============================================================
# 基础装饰图形
# ============================================================

class StarWidget(Widget):
    """可爱的星星"""
    rotation = NumericProperty(0)
    
    def __init__(self, color=(1, 0.8, 0), filled=True, **kwargs):
        super().__init__(**kwargs)
        self.star_color = color
        self.filled = filled
        self.bind(size=self.draw, pos=self.draw, rotation=self.draw)
        Clock.schedule_once(lambda dt: self.draw(), 0)
    
    def draw(self, *args):
        self.canvas.clear()
        cx, cy = self.center_x, self.center_y
        r = min(self.width, self.height) * 0.4
        with self.canvas:
            PushMatrix()
            Rotate(angle=self.rotation, origin=(cx, cy))
            Color(*self.star_color)
            points = []
            for i in range(5):
                angle = math.radians(90 + i * 72)
                points.extend([cx + r * math.cos(angle), cy + r * math.sin(angle)])
                angle = math.radians(90 + i * 72 + 36)
                points.extend([cx + r * 0.4 * math.cos(angle), cy + r * 0.4 * math.sin(angle)])
            if self.filled:
                # 填充星星用三角形
                for i in range(5):
                    idx = i * 4
                    Triangle(points=[cx, cy, points[idx], points[idx+1], points[(idx+2)%20], points[(idx+3)%20]])
            Line(points=points, width=dp(2), close=True)
            PopMatrix()


class HeartWidget(Widget):
    """可爱的爱心"""
    scale = NumericProperty(1)
    
    def __init__(self, color=(1, 0.4, 0.4), **kwargs):
        super().__init__(**kwargs)
        self.heart_color = color
        self.bind(size=self.draw, pos=self.draw, scale=self.draw)
        Clock.schedule_once(lambda dt: self.draw(), 0)
    
    def draw(self, *args):
        self.canvas.clear()
        cx, cy = self.center_x, self.center_y
        r = min(self.width, self.height) * 0.25 * self.scale
        with self.canvas:
            Color(*self.heart_color)
            Ellipse(pos=(cx - r * 1.3, cy - r * 0.2), size=(r * 1.4, r * 1.4))
            Ellipse(pos=(cx - r * 0.1, cy - r * 0.2), size=(r * 1.4, r * 1.4))
            Triangle(points=[cx - r * 1.4, cy + r * 0.2, cx + r * 1.4, cy + r * 0.2, cx, cy - r * 1.5])


class SunWidget(Widget):
    """可爱的太阳（带笑脸）"""
    rotation = NumericProperty(0)
    
    def __init__(self, with_face=True, **kwargs):
        super().__init__(**kwargs)
        self.with_face = with_face
        self.bind(size=self.draw, pos=self.draw, rotation=self.draw)
        Clock.schedule_once(lambda dt: self.draw(), 0)
    
    def draw(self, *args):
        self.canvas.clear()
        cx, cy = self.center_x, self.center_y
        r = min(self.width, self.height) * 0.25
        with self.canvas:
            PushMatrix()
            Rotate(angle=self.rotation, origin=(cx, cy))
            # 光芒
            Color(1, 0.6, 0)
            for i in range(12):
                angle = math.radians(i * 30)
                x1 = cx + r * 1.2 * math.cos(angle)
                y1 = cy + r * 1.2 * math.sin(angle)
                x2 = cx + r * 1.7 * math.cos(angle)
                y2 = cy + r * 1.7 * math.sin(angle)
                Line(points=[x1, y1, x2, y2], width=dp(3))
            PopMatrix()
            # 太阳本体
            Color(1, 0.85, 0)
            Ellipse(pos=(cx - r, cy - r), size=(r * 2, r * 2))
            if self.with_face:
                # 眼睛
                Color(0.2, 0.2, 0.2)
                Ellipse(pos=(cx - r * 0.5, cy + r * 0.1), size=(r * 0.25, r * 0.3))
                Ellipse(pos=(cx + r * 0.25, cy + r * 0.1), size=(r * 0.25, r * 0.3))
                # 笑脸
                Color(1, 0.5, 0)
                Line(bezier=[cx - r * 0.4, cy - r * 0.2, cx, cy - r * 0.5, cx + r * 0.4, cy - r * 0.2], width=dp(2))
                # 腮红
                Color(1, 0.6, 0.6, 0.5)
                Ellipse(pos=(cx - r * 0.7, cy - r * 0.3), size=(r * 0.3, r * 0.2))
                Ellipse(pos=(cx + r * 0.4, cy - r * 0.3), size=(r * 0.3, r * 0.2))


class MoonWidget(Widget):
    """可爱的月亮"""
    def __init__(self, with_face=True, **kwargs):
        super().__init__(**kwargs)
        self.with_face = with_face
        self.bind(size=self.draw, pos=self.draw)
        Clock.schedule_once(lambda dt: self.draw(), 0)
    
    def draw(self, *args):
        self.canvas.clear()
        cx, cy = self.center_x, self.center_y
        r = min(self.width, self.height) * 0.35
        with self.canvas:
            # 月亮本体
            Color(1, 0.95, 0.6)
            Ellipse(pos=(cx - r, cy - r), size=(r * 2, r * 2))
            # 遮挡形成月牙
            Color(0.1, 0.1, 0.3)
            Ellipse(pos=(cx - r * 0.2, cy - r * 0.6), size=(r * 1.6, r * 1.6))
            if self.with_face:
                # 眼睛（闭着的）
                Color(0.3, 0.3, 0.2)
                Line(bezier=[cx - r * 0.6, cy + r * 0.1, cx - r * 0.4, cy + r * 0.2, cx - r * 0.2, cy + r * 0.1], width=dp(2))
                # 微笑
                Line(bezier=[cx - r * 0.7, cy - r * 0.2, cx - r * 0.4, cy - r * 0.4, cx - r * 0.1, cy - r * 0.2], width=dp(2))


class CloudWidget(Widget):
    """可爱的云朵"""
    def __init__(self, color=(1, 1, 1), **kwargs):
        super().__init__(**kwargs)
        self.cloud_color = color
        self.bind(size=self.draw, pos=self.draw)
        Clock.schedule_once(lambda dt: self.draw(), 0)
    
    def draw(self, *args):
        self.canvas.clear()
        cx, cy = self.center_x, self.center_y
        r = min(self.width, self.height) * 0.18
        with self.canvas:
            Color(*self.cloud_color)
            Ellipse(pos=(cx - r * 2.2, cy - r * 0.8), size=(r * 1.8, r * 1.6))
            Ellipse(pos=(cx - r * 1, cy - r * 0.3), size=(r * 2, r * 1.8))
            Ellipse(pos=(cx + r * 0.3, cy - r * 0.6), size=(r * 1.6, r * 1.5))
            Ellipse(pos=(cx - r * 1.8, cy - r * 1.2), size=(r * 1.4, r * 1.2))
            Ellipse(pos=(cx, cy - r * 1), size=(r * 1.5, r * 1.3))


class RainbowWidget(Widget):
    """彩虹"""
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.bind(size=self.draw, pos=self.draw)
        Clock.schedule_once(lambda dt: self.draw(), 0)
    
    def draw(self, *args):
        self.canvas.clear()
        cx, cy = self.center_x, self.center_y - self.height * 0.15
        r = min(self.width, self.height) * 0.7
        colors = [(1, 0, 0), (1, 0.5, 0), (1, 1, 0), (0, 0.8, 0), (0, 0.5, 1), (0.3, 0, 0.5), (0.6, 0, 0.6)]
        with self.canvas:
            for i, color in enumerate(colors):
                Color(*color)
                radius = r - i * r * 0.1
                Line(ellipse=(cx - radius, cy - radius, radius * 2, radius * 2, 0, 180), width=dp(5))


# ============================================================
# 植物类装饰
# ============================================================

class FlowerWidget(Widget):
    """可爱的花朵"""
    rotation = NumericProperty(0)
    
    def __init__(self, petal_color=(1, 0.5, 0.7), center_color=(1, 0.9, 0), petals=5, **kwargs):
        super().__init__(**kwargs)
        self.petal_color = petal_color
        self.center_color = center_color
        self.petals = petals
        self.bind(size=self.draw, pos=self.draw, rotation=self.draw)
        Clock.schedule_once(lambda dt: self.draw(), 0)
    
    def draw(self, *args):
        self.canvas.clear()
        cx, cy = self.center_x, self.center_y
        r = min(self.width, self.height) * 0.2
        with self.canvas:
            PushMatrix()
            Rotate(angle=self.rotation, origin=(cx, cy))
            # 花瓣
            Color(*self.petal_color)
            for i in range(self.petals):
                angle = math.radians(i * (360 / self.petals))
                px = cx + r * 0.7 * math.cos(angle)
                py = cy + r * 0.7 * math.sin(angle)
                Ellipse(pos=(px - r * 0.55, py - r * 0.55), size=(r * 1.1, r * 1.1))
            # 花心
            Color(*self.center_color)
            Ellipse(pos=(cx - r * 0.45, cy - r * 0.45), size=(r * 0.9, r * 0.9))
            # 花心纹理
            Color(self.center_color[0] * 0.8, self.center_color[1] * 0.8, 0)
            for i in range(6):
                angle = math.radians(i * 60)
                Ellipse(pos=(cx + r * 0.15 * math.cos(angle) - r * 0.08, cy + r * 0.15 * math.sin(angle) - r * 0.08), size=(r * 0.16, r * 0.16))
            PopMatrix()


class TreeWidget(Widget):
    """可爱的小树"""
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.bind(size=self.draw, pos=self.draw)
        Clock.schedule_once(lambda dt: self.draw(), 0)
    
    def draw(self, *args):
        self.canvas.clear()
        cx, cy = self.center_x, self.center_y
        r = min(self.width, self.height) * 0.2
        with self.canvas:
            # 树干
            Color(0.55, 0.35, 0.2)
            Rectangle(pos=(cx - r * 0.3, cy - r * 2), size=(r * 0.6, r * 1.5))
            # 树冠（三层）
            Color(0.3, 0.75, 0.3)
            Triangle(points=[cx - r * 1.5, cy - r * 0.5, cx + r * 1.5, cy - r * 0.5, cx, cy + r * 1])
            Color(0.35, 0.8, 0.35)
            Triangle(points=[cx - r * 1.2, cy, cx + r * 1.2, cy, cx, cy + r * 1.5])
            Color(0.4, 0.85, 0.4)
            Triangle(points=[cx - r * 0.9, cy + r * 0.5, cx + r * 0.9, cy + r * 0.5, cx, cy + r * 2])


class GrassWidget(Widget):
    """小草"""
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.bind(size=self.draw, pos=self.draw)
        Clock.schedule_once(lambda dt: self.draw(), 0)
    
    def draw(self, *args):
        self.canvas.clear()
        cx, cy = self.center_x, self.center_y - self.height * 0.3
        r = min(self.width, self.height) * 0.15
        with self.canvas:
            Color(0.3, 0.75, 0.3)
            # 多根草
            for offset in [-r * 1.5, -r * 0.8, 0, r * 0.8, r * 1.5]:
                height = r * random.uniform(2, 3)
                curve = r * random.uniform(-0.3, 0.3)
                Line(bezier=[cx + offset, cy, cx + offset + curve, cy + height * 0.6, cx + offset + curve * 1.5, cy + height], width=dp(3))


class MushroomWidget(Widget):
    """可爱的蘑菇"""
    def __init__(self, cap_color=(1, 0.3, 0.3), **kwargs):
        super().__init__(**kwargs)
        self.cap_color = cap_color
        self.bind(size=self.draw, pos=self.draw)
        Clock.schedule_once(lambda dt: self.draw(), 0)
    
    def draw(self, *args):
        self.canvas.clear()
        cx, cy = self.center_x, self.center_y
        r = min(self.width, self.height) * 0.25
        with self.canvas:
            # 蘑菇柄
            Color(0.95, 0.9, 0.8)
            Rectangle(pos=(cx - r * 0.4, cy - r * 1.2), size=(r * 0.8, r * 1.2))
            # 蘑菇帽
            Color(*self.cap_color)
            Ellipse(pos=(cx - r * 1.2, cy - r * 0.3), size=(r * 2.4, r * 1.5))
            # 白点
            Color(1, 1, 1)
            Ellipse(pos=(cx - r * 0.7, cy + r * 0.3), size=(r * 0.35, r * 0.35))
            Ellipse(pos=(cx + r * 0.3, cy + r * 0.2), size=(r * 0.3, r * 0.3))
            Ellipse(pos=(cx - r * 0.2, cy + r * 0.5), size=(r * 0.25, r * 0.25))


# ============================================================
# 动物类装饰
# ============================================================

class ButterflyWidget(Widget):
    """可爱的蝴蝶"""
    wing_angle = NumericProperty(0)
    
    def __init__(self, color=(0.9, 0.5, 0.9), **kwargs):
        super().__init__(**kwargs)
        self.butterfly_color = color
        self.bind(size=self.draw, pos=self.draw, wing_angle=self.draw)
        Clock.schedule_once(lambda dt: self.draw(), 0)
    
    def draw(self, *args):
        self.canvas.clear()
        cx, cy = self.center_x, self.center_y
        r = min(self.width, self.height) * 0.2
        wing_scale = 1 + math.sin(math.radians(self.wing_angle)) * 0.15
        with self.canvas:
            # 上翅膀
            Color(*self.butterfly_color)
            Ellipse(pos=(cx - r * 1.8 * wing_scale, cy), size=(r * 1.5 * wing_scale, r * 1.8))
            Ellipse(pos=(cx + r * 0.3 * wing_scale, cy), size=(r * 1.5 * wing_scale, r * 1.8))
            # 下翅膀
            Color(self.butterfly_color[0] * 0.8, self.butterfly_color[1] * 0.8, self.butterfly_color[2] * 0.8)
            Ellipse(pos=(cx - r * 1.5 * wing_scale, cy - r * 1.2), size=(r * 1.2 * wing_scale, r * 1.3))
            Ellipse(pos=(cx + r * 0.3 * wing_scale, cy - r * 1.2), size=(r * 1.2 * wing_scale, r * 1.3))
            # 翅膀花纹
            Color(1, 1, 1, 0.6)
            Ellipse(pos=(cx - r * 1.3, cy + r * 0.4), size=(r * 0.5, r * 0.5))
            Ellipse(pos=(cx + r * 0.8, cy + r * 0.4), size=(r * 0.5, r * 0.5))
            # 身体
            Color(0.3, 0.2, 0.1)
            Ellipse(pos=(cx - r * 0.15, cy - r * 0.8), size=(r * 0.3, r * 1.8))
            # 触角
            Line(points=[cx, cy + r * 0.9, cx - r * 0.4, cy + r * 1.4], width=dp(1.5))
            Line(points=[cx, cy + r * 0.9, cx + r * 0.4, cy + r * 1.4], width=dp(1.5))
            Ellipse(pos=(cx - r * 0.5, cy + r * 1.3), size=(r * 0.15, r * 0.15))
            Ellipse(pos=(cx + r * 0.35, cy + r * 1.3), size=(r * 0.15, r * 0.15))


class BeeWidget(Widget):
    """可爱的小蜜蜂"""
    wing_angle = NumericProperty(0)
    
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.bind(size=self.draw, pos=self.draw, wing_angle=self.draw)
        Clock.schedule_once(lambda dt: self.draw(), 0)
    
    def draw(self, *args):
        self.canvas.clear()
        cx, cy = self.center_x, self.center_y
        r = min(self.width, self.height) * 0.2
        wing_offset = math.sin(math.radians(self.wing_angle)) * r * 0.3
        with self.canvas:
            # 翅膀
            Color(0.9, 0.95, 1, 0.7)
            Ellipse(pos=(cx - r * 1.5, cy + r * 0.3 + wing_offset), size=(r * 1.2, r * 1.5))
            Ellipse(pos=(cx + r * 0.3, cy + r * 0.3 - wing_offset), size=(r * 1.2, r * 1.5))
            # 身体
            Color(1, 0.85, 0)
            Ellipse(pos=(cx - r * 0.8, cy - r * 0.6), size=(r * 1.6, r * 1.2))
            # 条纹
            Color(0.1, 0.1, 0.1)
            for i in range(3):
                Rectangle(pos=(cx - r * 0.5 + i * r * 0.4, cy - r * 0.5), size=(r * 0.2, r * 1))
            # 头
            Color(1, 0.85, 0)
            Ellipse(pos=(cx - r * 1.3, cy - r * 0.4), size=(r * 0.7, r * 0.8))
            # 眼睛
            Color(0, 0, 0)
            Ellipse(pos=(cx - r * 1.15, cy), size=(r * 0.2, r * 0.2))
            # 触角
            Line(points=[cx - r * 1, cy + r * 0.3, cx - r * 1.2, cy + r * 0.7], width=dp(1.5))
            Line(points=[cx - r * 0.8, cy + r * 0.3, cx - r * 0.6, cy + r * 0.7], width=dp(1.5))


class LadybugWidget(Widget):
    """可爱的瓢虫"""
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.bind(size=self.draw, pos=self.draw)
        Clock.schedule_once(lambda dt: self.draw(), 0)
    
    def draw(self, *args):
        self.canvas.clear()
        cx, cy = self.center_x, self.center_y
        r = min(self.width, self.height) * 0.3
        with self.canvas:
            # 身体
            Color(1, 0.2, 0.1)
            Ellipse(pos=(cx - r, cy - r * 0.8), size=(r * 2, r * 1.6))
            # 中线
            Color(0.1, 0.1, 0.1)
            Line(points=[cx, cy - r * 0.8, cx, cy + r * 0.8], width=dp(2))
            # 黑点
            Ellipse(pos=(cx - r * 0.7, cy + r * 0.2), size=(r * 0.35, r * 0.35))
            Ellipse(pos=(cx + r * 0.35, cy + r * 0.2), size=(r * 0.35, r * 0.35))
            Ellipse(pos=(cx - r * 0.5, cy - r * 0.3), size=(r * 0.3, r * 0.3))
            Ellipse(pos=(cx + r * 0.2, cy - r * 0.3), size=(r * 0.3, r * 0.3))
            # 头
            Color(0.1, 0.1, 0.1)
            Ellipse(pos=(cx - r * 0.4, cy + r * 0.6), size=(r * 0.8, r * 0.6))
            # 眼睛
            Color(1, 1, 1)
            Ellipse(pos=(cx - r * 0.3, cy + r * 0.8), size=(r * 0.2, r * 0.2))
            Ellipse(pos=(cx + r * 0.1, cy + r * 0.8), size=(r * 0.2, r * 0.2))


class BirdWidget(Widget):
    """可爱的小鸟"""
    def __init__(self, color=(1, 0.6, 0.2), **kwargs):
        super().__init__(**kwargs)
        self.bird_color = color
        self.bind(size=self.draw, pos=self.draw)
        Clock.schedule_once(lambda dt: self.draw(), 0)
    
    def draw(self, *args):
        self.canvas.clear()
        cx, cy = self.center_x, self.center_y
        r = min(self.width, self.height) * 0.25
        with self.canvas:
            # 身体
            Color(*self.bird_color)
            Ellipse(pos=(cx - r, cy - r * 0.6), size=(r * 2, r * 1.4))
            # 翅膀
            Color(self.bird_color[0] * 0.8, self.bird_color[1] * 0.8, self.bird_color[2] * 0.8)
            Ellipse(pos=(cx - r * 0.3, cy - r * 0.2), size=(r * 1.2, r * 0.8))
            # 头
            Color(*self.bird_color)
            Ellipse(pos=(cx - r * 1.5, cy + r * 0.1), size=(r * 1, r * 1))
            # 眼睛
            Color(1, 1, 1)
            Ellipse(pos=(cx - r * 1.2, cy + r * 0.4), size=(r * 0.4, r * 0.4))
            Color(0, 0, 0)
            Ellipse(pos=(cx - r * 1.1, cy + r * 0.5), size=(r * 0.2, r * 0.2))
            # 嘴巴
            Color(1, 0.7, 0)
            Triangle(points=[cx - r * 1.5, cy + r * 0.5, cx - r * 2, cy + r * 0.3, cx - r * 1.5, cy + r * 0.2])
            # 尾巴
            Color(self.bird_color[0] * 0.7, self.bird_color[1] * 0.7, self.bird_color[2] * 0.7)
            Triangle(points=[cx + r * 0.8, cy, cx + r * 1.8, cy + r * 0.3, cx + r * 1.8, cy - r * 0.3])


class FishWidget(Widget):
    """可爱的小鱼"""
    def __init__(self, color=(0.3, 0.7, 1), **kwargs):
        super().__init__(**kwargs)
        self.fish_color = color
        self.bind(size=self.draw, pos=self.draw)
        Clock.schedule_once(lambda dt: self.draw(), 0)
    
    def draw(self, *args):
        self.canvas.clear()
        cx, cy = self.center_x, self.center_y
        r = min(self.width, self.height) * 0.25
        with self.canvas:
            # 尾巴
            Color(self.fish_color[0] * 0.8, self.fish_color[1] * 0.8, self.fish_color[2] * 0.8)
            Triangle(points=[cx + r * 0.6, cy, cx + r * 1.5, cy + r * 0.8, cx + r * 1.5, cy - r * 0.8])
            # 身体
            Color(*self.fish_color)
            Ellipse(pos=(cx - r * 1.2, cy - r * 0.7), size=(r * 2, r * 1.4))
            # 鳍
            Color(self.fish_color[0] * 0.9, self.fish_color[1] * 0.9, self.fish_color[2] * 0.9)
            Triangle(points=[cx - r * 0.3, cy + r * 0.5, cx, cy + r * 1.2, cx + r * 0.3, cy + r * 0.5])
            # 眼睛
            Color(1, 1, 1)
            Ellipse(pos=(cx - r * 0.9, cy + r * 0.1), size=(r * 0.4, r * 0.4))
            Color(0, 0, 0)
            Ellipse(pos=(cx - r * 0.8, cy + r * 0.2), size=(r * 0.2, r * 0.2))
            # 鳞片纹理
            Color(1, 1, 1, 0.3)
            for i in range(3):
                for j in range(2):
                    Ellipse(pos=(cx - r * 0.4 + i * r * 0.35, cy - r * 0.3 + j * r * 0.4), size=(r * 0.25, r * 0.25))


class CatWidget(Widget):
    """可爱的小猫"""
    def __init__(self, color=(1, 0.7, 0.4), **kwargs):
        super().__init__(**kwargs)
        self.cat_color = color
        self.bind(size=self.draw, pos=self.draw)
        Clock.schedule_once(lambda dt: self.draw(), 0)
    
    def draw(self, *args):
        self.canvas.clear()
        cx, cy = self.center_x, self.center_y
        r = min(self.width, self.height) * 0.25
        with self.canvas:
            # 身体
            Color(*self.cat_color)
            Ellipse(pos=(cx - r * 0.8, cy - r * 1.2), size=(r * 1.6, r * 1.4))
            # 头
            Ellipse(pos=(cx - r, cy - r * 0.2), size=(r * 2, r * 1.8))
            # 耳朵
            Triangle(points=[cx - r * 0.9, cy + r * 1.2, cx - r * 0.5, cy + r * 2, cx - r * 0.1, cy + r * 1.2])
            Triangle(points=[cx + r * 0.1, cy + r * 1.2, cx + r * 0.5, cy + r * 2, cx + r * 0.9, cy + r * 1.2])
            # 内耳
            Color(1, 0.7, 0.7)
            Triangle(points=[cx - r * 0.7, cy + r * 1.3, cx - r * 0.5, cy + r * 1.7, cx - r * 0.3, cy + r * 1.3])
            Triangle(points=[cx + r * 0.3, cy + r * 1.3, cx + r * 0.5, cy + r * 1.7, cx + r * 0.7, cy + r * 1.3])
            # 眼睛
            Color(0.4, 0.8, 0.4)
            Ellipse(pos=(cx - r * 0.6, cy + r * 0.4), size=(r * 0.5, r * 0.5))
            Ellipse(pos=(cx + r * 0.1, cy + r * 0.4), size=(r * 0.5, r * 0.5))
            Color(0, 0, 0)
            Ellipse(pos=(cx - r * 0.45, cy + r * 0.5), size=(r * 0.2, r * 0.3))
            Ellipse(pos=(cx + r * 0.25, cy + r * 0.5), size=(r * 0.2, r * 0.3))
            # 鼻子
            Color(1, 0.5, 0.5)
            Triangle(points=[cx - r * 0.1, cy + r * 0.1, cx + r * 0.1, cy + r * 0.1, cx, cy - r * 0.1])
            # 嘴巴
            Color(0.3, 0.2, 0.2)
            Line(bezier=[cx - r * 0.3, cy - r * 0.2, cx, cy - r * 0.4, cx + r * 0.3, cy - r * 0.2], width=dp(1.5))
            # 胡须
            Line(points=[cx - r * 0.2, cy, cx - r * 0.8, cy + r * 0.1], width=dp(1))
            Line(points=[cx - r * 0.2, cy - r * 0.1, cx - r * 0.8, cy - r * 0.1], width=dp(1))
            Line(points=[cx + r * 0.2, cy, cx + r * 0.8, cy + r * 0.1], width=dp(1))
            Line(points=[cx + r * 0.2, cy - r * 0.1, cx + r * 0.8, cy - r * 0.1], width=dp(1))


class DogWidget(Widget):
    """可爱的小狗"""
    def __init__(self, color=(0.7, 0.5, 0.3), **kwargs):
        super().__init__(**kwargs)
        self.dog_color = color
        self.bind(size=self.draw, pos=self.draw)
        Clock.schedule_once(lambda dt: self.draw(), 0)
    
    def draw(self, *args):
        self.canvas.clear()
        cx, cy = self.center_x, self.center_y
        r = min(self.width, self.height) * 0.25
        with self.canvas:
            # 身体
            Color(*self.dog_color)
            Ellipse(pos=(cx - r * 0.8, cy - r * 1.3), size=(r * 1.6, r * 1.4))
            # 头
            Ellipse(pos=(cx - r, cy - r * 0.3), size=(r * 2, r * 1.8))
            # 耳朵（垂下的）
            Color(self.dog_color[0] * 0.8, self.dog_color[1] * 0.8, self.dog_color[2] * 0.8)
            Ellipse(pos=(cx - r * 1.4, cy + r * 0.3), size=(r * 0.7, r * 1.2))
            Ellipse(pos=(cx + r * 0.7, cy + r * 0.3), size=(r * 0.7, r * 1.2))
            # 眼睛
            Color(0.2, 0.15, 0.1)
            Ellipse(pos=(cx - r * 0.5, cy + r * 0.5), size=(r * 0.4, r * 0.4))
            Ellipse(pos=(cx + r * 0.1, cy + r * 0.5), size=(r * 0.4, r * 0.4))
            Color(1, 1, 1)
            Ellipse(pos=(cx - r * 0.4, cy + r * 0.6), size=(r * 0.15, r * 0.15))
            Ellipse(pos=(cx + r * 0.2, cy + r * 0.6), size=(r * 0.15, r * 0.15))
            # 鼻子
            Color(0.1, 0.1, 0.1)
            Ellipse(pos=(cx - r * 0.2, cy + r * 0.1), size=(r * 0.4, r * 0.3))
            # 舌头
            Color(1, 0.5, 0.5)
            Ellipse(pos=(cx - r * 0.15, cy - r * 0.5), size=(r * 0.3, r * 0.5))


class PawPrintWidget(Widget):
    """可爱的爪印（汪汪队主题）"""
    def __init__(self, color=(0.6, 0.4, 0.2), **kwargs):
        super().__init__(**kwargs)
        self.paw_color = color
        self.bind(size=self.draw, pos=self.draw)
        Clock.schedule_once(lambda dt: self.draw(), 0)
    
    def draw(self, *args):
        self.canvas.clear()
        cx, cy = self.center_x, self.center_y
        r = min(self.width, self.height) * 0.12
        with self.canvas:
            Color(*self.paw_color)
            # 大肉垫
            Ellipse(pos=(cx - r * 1.5, cy - r * 2), size=(r * 3, r * 2.5))
            # 四个小肉垫
            Ellipse(pos=(cx - r * 2.2, cy + r * 0.2), size=(r * 1.3, r * 1.6))
            Ellipse(pos=(cx - r * 0.8, cy + r * 0.8), size=(r * 1.3, r * 1.6))
            Ellipse(pos=(cx + r * 0.5, cy + r * 0.2), size=(r * 1.3, r * 1.6))
            Ellipse(pos=(cx + r * 0.9, cy - r * 0.8), size=(r * 1.1, r * 1.4))


# ============================================================
# 其他可爱装饰
# ============================================================

class BalloonWidget(Widget):
    """可爱的气球"""
    def __init__(self, color=(1, 0.4, 0.4), **kwargs):
        super().__init__(**kwargs)
        self.balloon_color = color
        self.bind(size=self.draw, pos=self.draw)
        Clock.schedule_once(lambda dt: self.draw(), 0)
    
    def draw(self, *args):
        self.canvas.clear()
        cx, cy = self.center_x, self.center_y + self.height * 0.1
        r = min(self.width, self.height) * 0.3
        with self.canvas:
            # 气球本体
            Color(*self.balloon_color)
            Ellipse(pos=(cx - r, cy - r * 0.3), size=(r * 2, r * 2.3))
            # 气球结
            Triangle(points=[cx - r * 0.2, cy - r * 0.4, cx + r * 0.2, cy - r * 0.4, cx, cy - r * 0.7])
            # 高光
            Color(1, 1, 1, 0.4)
            Ellipse(pos=(cx - r * 0.5, cy + r * 0.8), size=(r * 0.5, r * 0.6))
            # 线
            Color(0.5, 0.5, 0.5)
            Line(bezier=[cx, cy - r * 0.7, cx - r * 0.2, cy - r * 1.5, cx + r * 0.1, cy - r * 2], width=dp(1.5))


class CandyWidget(Widget):
    """可爱的糖果"""
    rotation = NumericProperty(0)
    
    def __init__(self, colors=None, **kwargs):
        super().__init__(**kwargs)
        self.candy_colors = colors or [(1, 0.4, 0.4), (1, 1, 1)]
        self.bind(size=self.draw, pos=self.draw, rotation=self.draw)
        Clock.schedule_once(lambda dt: self.draw(), 0)
    
    def draw(self, *args):
        self.canvas.clear()
        cx, cy = self.center_x, self.center_y
        r = min(self.width, self.height) * 0.2
        with self.canvas:
            PushMatrix()
            Rotate(angle=self.rotation, origin=(cx, cy))
            # 糖果本体（条纹）
            for i in range(6):
                Color(*self.candy_colors[i % 2])
                angle_start = i * 60
                Line(ellipse=(cx - r, cy - r, r * 2, r * 2, angle_start, angle_start + 60), width=r * 0.8)
            # 包装纸
            Color(1, 0.9, 0.5)
            Triangle(points=[cx - r * 1.2, cy, cx - r * 2.2, cy + r * 0.5, cx - r * 2.2, cy - r * 0.5])
            Triangle(points=[cx + r * 1.2, cy, cx + r * 2.2, cy + r * 0.5, cx + r * 2.2, cy - r * 0.5])
            PopMatrix()


class GiftBoxWidget(Widget):
    """可爱的礼物盒"""
    def __init__(self, box_color=(1, 0.4, 0.6), ribbon_color=(1, 0.9, 0.3), **kwargs):
        super().__init__(**kwargs)
        self.box_color = box_color
        self.ribbon_color = ribbon_color
        self.bind(size=self.draw, pos=self.draw)
        Clock.schedule_once(lambda dt: self.draw(), 0)
    
    def draw(self, *args):
        self.canvas.clear()
        cx, cy = self.center_x, self.center_y
        r = min(self.width, self.height) * 0.3
        with self.canvas:
            # 盒子
            Color(*self.box_color)
            Rectangle(pos=(cx - r, cy - r), size=(r * 2, r * 1.6))
            # 盖子
            Color(self.box_color[0] * 0.9, self.box_color[1] * 0.9, self.box_color[2] * 0.9)
            Rectangle(pos=(cx - r * 1.1, cy + r * 0.6), size=(r * 2.2, r * 0.5))
            # 丝带
            Color(*self.ribbon_color)
            Rectangle(pos=(cx - r * 0.15, cy - r), size=(r * 0.3, r * 1.6))
            Rectangle(pos=(cx - r, cy + r * 0.1), size=(r * 2, r * 0.3))
            # 蝴蝶结
            Ellipse(pos=(cx - r * 0.7, cy + r * 0.9), size=(r * 0.6, r * 0.5))
            Ellipse(pos=(cx + r * 0.1, cy + r * 0.9), size=(r * 0.6, r * 0.5))
            Ellipse(pos=(cx - r * 0.2, cy + r * 0.95), size=(r * 0.4, r * 0.35))


class CrownWidget(Widget):
    """可爱的皇冠"""
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.bind(size=self.draw, pos=self.draw)
        Clock.schedule_once(lambda dt: self.draw(), 0)
    
    def draw(self, *args):
        self.canvas.clear()
        cx, cy = self.center_x, self.center_y
        r = min(self.width, self.height) * 0.3
        with self.canvas:
            # 皇冠主体
            Color(1, 0.85, 0)
            points = [
                cx - r * 1.2, cy - r * 0.5,
                cx - r * 0.8, cy + r * 0.8,
                cx - r * 0.4, cy + r * 0.2,
                cx, cy + r * 1,
                cx + r * 0.4, cy + r * 0.2,
                cx + r * 0.8, cy + r * 0.8,
                cx + r * 1.2, cy - r * 0.5,
            ]
            # 填充
            for i in range(0, len(points) - 4, 2):
                Triangle(points=[cx, cy - r * 0.5, points[i], points[i+1], points[i+2], points[i+3]])
            Line(points=points, width=dp(2), close=True)
            # 底边
            Rectangle(pos=(cx - r * 1.2, cy - r * 0.7), size=(r * 2.4, r * 0.3))
            # 宝石
            Color(1, 0.2, 0.3)
            Ellipse(pos=(cx - r * 0.15, cy + r * 0.6), size=(r * 0.3, r * 0.3))
            Color(0.2, 0.6, 1)
            Ellipse(pos=(cx - r * 0.9, cy + r * 0.4), size=(r * 0.25, r * 0.25))
            Ellipse(pos=(cx + r * 0.65, cy + r * 0.4), size=(r * 0.25, r * 0.25))


class TrophyWidget(Widget):
    """奖杯"""
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.bind(size=self.draw, pos=self.draw)
        Clock.schedule_once(lambda dt: self.draw(), 0)
    
    def draw(self, *args):
        self.canvas.clear()
        cx, cy = self.center_x, self.center_y
        r = min(self.width, self.height) * 0.25
        with self.canvas:
            # 杯身
            Color(1, 0.85, 0)
            Ellipse(pos=(cx - r, cy), size=(r * 2, r * 1.5))
            Rectangle(pos=(cx - r * 0.8, cy - r * 0.3), size=(r * 1.6, r * 0.8))
            # 把手
            Color(1, 0.8, 0)
            Line(ellipse=(cx - r * 1.6, cy + r * 0.2, r * 0.8, r * 1, 90, 270), width=dp(4))
            Line(ellipse=(cx + r * 0.8, cy + r * 0.2, r * 0.8, r * 1, 270, 450), width=dp(4))
            # 底座
            Color(0.6, 0.5, 0.3)
            Rectangle(pos=(cx - r * 0.3, cy - r * 0.8), size=(r * 0.6, r * 0.5))
            Rectangle(pos=(cx - r * 0.6, cy - r * 1.1), size=(r * 1.2, r * 0.4))
            # 星星装饰
            Color(1, 1, 0.8)
            Ellipse(pos=(cx - r * 0.2, cy + r * 0.5), size=(r * 0.4, r * 0.4))


# ============================================================
# 动画效果函数
# ============================================================

def animate_float(widget, amplitude=15, duration=2):
    """漂浮动画"""
    original_y = widget.y
    anim = Animation(y=original_y + dp(amplitude), duration=duration, t='in_out_sine')
    anim += Animation(y=original_y, duration=duration, t='in_out_sine')
    anim.repeat = True
    anim.start(widget)
    return anim


def animate_rotate(widget, duration=4):
    """旋转动画"""
    anim = Animation(rotation=360, duration=duration)
    anim.repeat = True
    anim.start(widget)
    return anim


def animate_pulse(widget, min_scale=0.9, max_scale=1.1, duration=0.8):
    """脉冲缩放动画"""
    anim = Animation(scale=max_scale, duration=duration/2, t='in_out_sine')
    anim += Animation(scale=min_scale, duration=duration/2, t='in_out_sine')
    anim.repeat = True
    anim.start(widget)
    return anim


def animate_heartbeat(widget, duration=0.6):
    """心跳动画（适合爱心）"""
    anim = Animation(scale=1.2, duration=duration * 0.15, t='out_quad')
    anim += Animation(scale=0.95, duration=duration * 0.15, t='in_quad')
    anim += Animation(scale=1.15, duration=duration * 0.1, t='out_quad')
    anim += Animation(scale=1, duration=duration * 0.6, t='out_quad')
    anim.repeat = True
    anim.start(widget)
    return anim


def animate_wing_flap(widget, duration=0.3):
    """翅膀扇动动画（适合蝴蝶、蜜蜂）"""
    def update_wing(dt):
        widget.wing_angle = (widget.wing_angle + 30) % 360
    Clock.schedule_interval(update_wing, duration / 12)


def animate_bounce(widget, height=30, duration=0.5):
    """弹跳动画"""
    original_y = widget.y
    anim = Animation(y=original_y + dp(height), duration=duration * 0.4, t='out_quad')
    anim += Animation(y=original_y, duration=duration * 0.6, t='out_bounce')
    anim.repeat = True
    anim.start(widget)
    return anim


def animate_swing(widget, angle=15, duration=1):
    """摇摆动画"""
    anim = Animation(rotation=angle, duration=duration/2, t='in_out_sine')
    anim += Animation(rotation=-angle, duration=duration, t='in_out_sine')
    anim += Animation(rotation=0, duration=duration/2, t='in_out_sine')
    anim.repeat = True
    anim.start(widget)
    return anim


def animate_twinkle(widget, duration=1):
    """闪烁动画（适合星星）"""
    anim = Animation(opacity=0.3, duration=duration/2, t='in_out_sine')
    anim += Animation(opacity=1, duration=duration/2, t='in_out_sine')
    anim.repeat = True
    anim.start(widget)
    return anim


def animate_color_cycle(widget, colors, duration=2):
    """颜色循环动画"""
    def cycle_color(dt):
        if not hasattr(widget, '_color_index'):
            widget._color_index = 0
        widget._color_index = (widget._color_index + 1) % len(colors)
        if hasattr(widget, 'star_color'):
            widget.star_color = colors[widget._color_index]
        elif hasattr(widget, 'heart_color'):
            widget.heart_color = colors[widget._color_index]
        widget.draw()
    Clock.schedule_interval(cycle_color, duration / len(colors))


# ============================================================
# 特效函数
# ============================================================

def create_confetti_burst(parent, x, y, count=15):
    """彩色纸屑爆炸效果"""
    colors = [(1, 0, 0), (1, 0.5, 0), (1, 1, 0), (0, 1, 0), (0, 0.7, 1), (0.6, 0, 0.8), (1, 0.4, 0.7)]
    
    for i in range(count):
        confetti = Widget(size_hint=(None, None), size=(dp(12), dp(12)), pos=(x, y))
        color = random.choice(colors)
        shape = random.choice(['circle', 'rect', 'star'])
        
        with confetti.canvas:
            Color(*color)
            if shape == 'circle':
                Ellipse(pos=(0, 0), size=(dp(12), dp(12)))
            elif shape == 'rect':
                Rectangle(pos=(0, 0), size=(dp(10), dp(10)))
            else:
                # 小星星
                cx, cy = dp(6), dp(6)
                r = dp(5)
                points = []
                for j in range(5):
                    angle = math.radians(90 + j * 72)
                    points.extend([cx + r * math.cos(angle), cy + r * math.sin(angle)])
                    angle = math.radians(90 + j * 72 + 36)
                    points.extend([cx + r * 0.4 * math.cos(angle), cy + r * 0.4 * math.sin(angle)])
                Line(points=points, width=dp(1.5), close=True)
        
        parent.add_widget(confetti)
        
        end_x = x + random.randint(-180, 180)
        end_y = y + random.randint(-50, 200)
        
        anim = Animation(
            pos=(end_x, end_y), 
            opacity=0, 
            duration=random.uniform(0.8, 1.5), 
            t='out_quad'
        )
        anim.bind(on_complete=lambda a, w: parent.remove_widget(w))
        anim.start(confetti)


def create_star_burst(parent, x, y, count=8):
    """星星爆炸效果"""
    colors = [(1, 0.9, 0), (1, 0.7, 0), (1, 1, 0.5), (1, 0.8, 0.3)]
    
    for i in range(count):
        star = StarWidget(
            color=random.choice(colors),
            size_hint=(None, None),
            size=(dp(25), dp(25)),
            pos=(x - dp(12), y - dp(12))
        )
        parent.add_widget(star)
        
        angle = math.radians(i * (360 / count))
        distance = random.randint(80, 150)
        end_x = x + distance * math.cos(angle)
        end_y = y + distance * math.sin(angle)
        
        anim = Animation(
            pos=(end_x, end_y),
            opacity=0,
            rotation=360,
            duration=random.uniform(0.6, 1),
            t='out_quad'
        )
        anim.bind(on_complete=lambda a, w: parent.remove_widget(w))
        anim.start(star)


def create_heart_burst(parent, x, y, count=6):
    """爱心爆炸效果"""
    colors = [(1, 0.3, 0.4), (1, 0.5, 0.6), (1, 0.4, 0.5), (1, 0.6, 0.7)]
    
    for i in range(count):
        heart = HeartWidget(
            color=random.choice(colors),
            size_hint=(None, None),
            size=(dp(20), dp(20)),
            pos=(x - dp(10), y - dp(10))
        )
        parent.add_widget(heart)
        
        angle = math.radians(random.randint(0, 360))
        distance = random.randint(60, 120)
        end_x = x + distance * math.cos(angle)
        end_y = y + distance * math.sin(angle)
        
        anim = Animation(
            pos=(end_x, end_y),
            opacity=0,
            scale=0.3,
            duration=random.uniform(0.8, 1.2),
            t='out_quad'
        )
        anim.bind(on_complete=lambda a, w: parent.remove_widget(w))
        anim.start(heart)


def create_firework(parent, x, y):
    """烟花效果"""
    colors = [
        [(1, 0.3, 0.3), (1, 0.6, 0.3)],
        [(0.3, 0.8, 1), (0.5, 0.9, 1)],
        [(1, 0.9, 0.3), (1, 1, 0.6)],
        [(0.8, 0.4, 1), (0.9, 0.6, 1)],
        [(0.3, 1, 0.5), (0.5, 1, 0.7)],
    ]
    color_set = random.choice(colors)
    
    for i in range(12):
        particle = Widget(size_hint=(None, None), size=(dp(8), dp(8)), pos=(x, y))
        with particle.canvas:
            Color(*random.choice(color_set))
            Ellipse(pos=(0, 0), size=(dp(8), dp(8)))
        
        parent.add_widget(particle)
        
        angle = math.radians(i * 30)
        distance = random.randint(100, 180)
        end_x = x + distance * math.cos(angle)
        end_y = y + distance * math.sin(angle)
        
        # 先上升再散开
        anim = Animation(pos=(end_x, end_y), duration=0.5, t='out_quad')
        anim += Animation(opacity=0, duration=0.5, t='in_quad')
        anim.bind(on_complete=lambda a, w: parent.remove_widget(w))
        anim.start(particle)


def create_bubble_float(parent, x, y, count=5):
    """气泡上升效果"""
    for i in range(count):
        size = random.randint(15, 35)
        bubble = Widget(size_hint=(None, None), size=(dp(size), dp(size)), pos=(x + random.randint(-30, 30), y))
        
        with bubble.canvas:
            Color(0.7, 0.9, 1, 0.6)
            Ellipse(pos=(0, 0), size=(dp(size), dp(size)))
            Color(1, 1, 1, 0.4)
            Ellipse(pos=(dp(size * 0.2), dp(size * 0.5)), size=(dp(size * 0.3), dp(size * 0.3)))
        
        parent.add_widget(bubble)
        
        end_y = y + random.randint(200, 400)
        end_x = x + random.randint(-50, 50)
        
        anim = Animation(
            pos=(end_x, end_y),
            opacity=0,
            duration=random.uniform(2, 4),
            t='out_quad'
        )
        Clock.schedule_once(lambda dt, a=anim, b=bubble: a.start(b), i * 0.2)
        anim.bind(on_complete=lambda a, w: parent.remove_widget(w))


# ============================================================
# 场景装饰生成器
# ============================================================

def create_sky_scene(parent):
    """创建天空场景（太阳、云朵）"""
    from kivy.core.window import Window
    
    # 太阳
    sun = SunWidget(size_hint=(None, None), size=(dp(70), dp(70)), pos=(dp(30), Window.height - dp(90)))
    sun.opacity = 0.9
    parent.add_widget(sun)
    animate_rotate(sun, duration=20)
    
    # 云朵
    for i in range(3):
        cloud = CloudWidget(size_hint=(None, None), size=(dp(80), dp(50)))
        cloud.pos = (Window.width * (0.3 + i * 0.25), Window.height - dp(60 + i * 30))
        cloud.opacity = 0.8
        parent.add_widget(cloud)
        animate_float(cloud, amplitude=10, duration=3 + i * 0.5)
    
    return parent


def create_garden_scene(parent):
    """创建花园场景（花朵、蝴蝶、草地）"""
    from kivy.core.window import Window
    
    # 花朵
    flower_colors = [(1, 0.5, 0.7), (1, 0.8, 0.3), (0.7, 0.5, 1), (1, 0.4, 0.4), (0.5, 0.8, 1)]
    for i in range(4):
        flower = FlowerWidget(
            petal_color=flower_colors[i % len(flower_colors)],
            size_hint=(None, None),
            size=(dp(45), dp(45)),
            pos=(dp(50 + i * 100), dp(30))
        )
        flower.opacity = 0.85
        parent.add_widget(flower)
        animate_swing(flower, angle=10, duration=2 + i * 0.3)
    
    # 蝴蝶
    butterfly = ButterflyWidget(
        color=(0.9, 0.5, 0.9),
        size_hint=(None, None),
        size=(dp(50), dp(50)),
        pos=(Window.width - dp(100), dp(150))
    )
    parent.add_widget(butterfly)
    animate_wing_flap(butterfly)
    animate_float(butterfly, amplitude=20, duration=2.5)
    
    return parent


def create_ocean_scene(parent):
    """创建海洋场景（鱼、气泡）"""
    from kivy.core.window import Window
    
    # 小鱼
    fish_colors = [(0.3, 0.7, 1), (1, 0.6, 0.3), (0.4, 0.9, 0.5), (1, 0.5, 0.7)]
    for i in range(3):
        fish = FishWidget(
            color=fish_colors[i % len(fish_colors)],
            size_hint=(None, None),
            size=(dp(55), dp(40)),
            pos=(dp(80 + i * 150), dp(50 + i * 30))
        )
        fish.opacity = 0.85
        parent.add_widget(fish)
        animate_float(fish, amplitude=15, duration=2 + i * 0.4)
    
    return parent


def create_celebration_scene(parent):
    """创建庆祝场景（气球、星星、礼物）"""
    from kivy.core.window import Window
    
    # 气球
    balloon_colors = [(1, 0.4, 0.4), (0.4, 0.8, 1), (1, 0.9, 0.3), (0.8, 0.5, 1), (0.4, 0.9, 0.5)]
    for i in range(4):
        balloon = BalloonWidget(
            color=balloon_colors[i % len(balloon_colors)],
            size_hint=(None, None),
            size=(dp(45), dp(55)),
            pos=(dp(60 + i * 120), Window.height - dp(120))
        )
        balloon.opacity = 0.9
        parent.add_widget(balloon)
        animate_float(balloon, amplitude=12, duration=2.5 + i * 0.3)
    
    # 星星
    for i in range(5):
        star = StarWidget(
            color=(1, 0.9, 0.3),
            size_hint=(None, None),
            size=(dp(25), dp(25)),
            pos=(random.randint(50, int(Window.width - 50)), random.randint(100, int(Window.height - 100)))
        )
        star.opacity = 0.8
        parent.add_widget(star)
        animate_twinkle(star, duration=1 + random.random())
        animate_rotate(star, duration=5 + random.random() * 3)
    
    return parent


def create_night_scene(parent):
    """创建夜晚场景（月亮、星星）"""
    from kivy.core.window import Window
    
    # 月亮
    moon = MoonWidget(size_hint=(None, None), size=(dp(60), dp(60)), pos=(Window.width - dp(100), Window.height - dp(90)))
    moon.opacity = 0.9
    parent.add_widget(moon)
    
    # 星星
    for i in range(8):
        star = StarWidget(
            color=(1, 1, 0.8),
            size_hint=(None, None),
            size=(dp(15 + random.randint(0, 10)), dp(15 + random.randint(0, 10))),
            pos=(random.randint(30, int(Window.width - 30)), random.randint(int(Window.height * 0.5), int(Window.height - 50)))
        )
        star.opacity = 0.7
        parent.add_widget(star)
        animate_twinkle(star, duration=0.8 + random.random() * 0.8)
    
    return parent


def create_forest_scene(parent):
    """创建森林场景（树、蘑菇、小鸟）"""
    from kivy.core.window import Window
    
    # 树
    for i in range(2):
        tree = TreeWidget(size_hint=(None, None), size=(dp(70), dp(90)), pos=(dp(40 + i * 200), dp(20)))
        tree.opacity = 0.85
        parent.add_widget(tree)
    
    # 蘑菇
    mushroom_colors = [(1, 0.3, 0.3), (1, 0.6, 0.2), (0.9, 0.4, 0.6)]
    for i in range(3):
        mushroom = MushroomWidget(
            cap_color=mushroom_colors[i % len(mushroom_colors)],
            size_hint=(None, None),
            size=(dp(40), dp(45)),
            pos=(dp(100 + i * 130), dp(25))
        )
        mushroom.opacity = 0.85
        parent.add_widget(mushroom)
    
    # 小鸟
    bird = BirdWidget(
        color=(1, 0.6, 0.2),
        size_hint=(None, None),
        size=(dp(45), dp(35)),
        pos=(Window.width - dp(120), Window.height - dp(100))
    )
    parent.add_widget(bird)
    animate_float(bird, amplitude=15, duration=2)
    
    return parent


# ============================================================
# 便捷装饰函数
# ============================================================

def add_corner_decorations(parent, style='default'):
    """在四角添加装饰"""
    from kivy.core.window import Window
    
    if style == 'stars':
        positions = [
            (dp(20), dp(20)),
            (Window.width - dp(50), dp(20)),
            (dp(20), Window.height - dp(50)),
            (Window.width - dp(50), Window.height - dp(50)),
        ]
        colors = [(1, 0.9, 0.3), (1, 0.7, 0.4), (1, 0.8, 0.2), (1, 0.6, 0.3)]
        for i, pos in enumerate(positions):
            star = StarWidget(color=colors[i], size_hint=(None, None), size=(dp(35), dp(35)), pos=pos)
            star.opacity = 0.8
            parent.add_widget(star)
            animate_twinkle(star, duration=1 + i * 0.2)
            animate_rotate(star, duration=6 + i)
    
    elif style == 'hearts':
        positions = [
            (dp(20), dp(20)),
            (Window.width - dp(50), dp(20)),
            (dp(20), Window.height - dp(50)),
            (Window.width - dp(50), Window.height - dp(50)),
        ]
        colors = [(1, 0.4, 0.5), (1, 0.5, 0.6), (1, 0.3, 0.4), (1, 0.6, 0.7)]
        for i, pos in enumerate(positions):
            heart = HeartWidget(color=colors[i], size_hint=(None, None), size=(dp(30), dp(30)), pos=pos)
            heart.opacity = 0.8
            parent.add_widget(heart)
            animate_heartbeat(heart)
    
    elif style == 'flowers':
        positions = [
            (dp(15), dp(15)),
            (Window.width - dp(55), dp(15)),
            (dp(15), Window.height - dp(55)),
            (Window.width - dp(55), Window.height - dp(55)),
        ]
        colors = [(1, 0.5, 0.7), (1, 0.8, 0.3), (0.7, 0.5, 1), (0.5, 0.9, 0.6)]
        for i, pos in enumerate(positions):
            flower = FlowerWidget(petal_color=colors[i], size_hint=(None, None), size=(dp(45), dp(45)), pos=pos)
            flower.opacity = 0.8
            parent.add_widget(flower)
            animate_swing(flower, angle=8, duration=2 + i * 0.3)
    
    else:  # default - mixed
        decorations = [
            (SunWidget, (dp(60), dp(60)), (dp(20), Window.height - dp(80)), {}),
            (CloudWidget, (dp(70), dp(45)), (Window.width - dp(90), Window.height - dp(65)), {}),
            (FlowerWidget, (dp(40), dp(40)), (dp(25), dp(25)), {'petal_color': (1, 0.5, 0.7)}),
            (PawPrintWidget, (dp(40), dp(40)), (Window.width - dp(60), dp(30)), {}),
        ]
        for widget_class, size, pos, kwargs in decorations:
            try:
                deco = widget_class(size_hint=(None, None), size=size, pos=pos, **kwargs)
                deco.opacity = 0.75
                parent.add_widget(deco)
            except:
                pass
    
    return parent
