# -*- coding: utf-8 -*-
"""
汪汪队主题模块 - Paw Patrol Theme
专为乐乐识字乐园设计的汪汪队立大功主题装饰
全部使用Canvas绘制，兼容华为鸿蒙平板

包含：狗狗角色、徽章、骨头、狗窝、爪印、项圈等元素
"""
from kivy.uix.widget import Widget
from kivy.graphics import Color, Ellipse, Line, Rectangle, Triangle, RoundedRectangle
from kivy.graphics import PushMatrix, PopMatrix, Rotate
from kivy.metrics import dp
from kivy.clock import Clock
from kivy.animation import Animation
from kivy.utils import get_color_from_hex
import random
import math


# ============================================================
# 汪汪队配色方案
# ============================================================
PAW_COLORS = {
    'blue': (0.12, 0.53, 0.90),       # 汪汪队蓝
    'red': (0.90, 0.22, 0.21),        # 汪汪队红
    'chase': (0.08, 0.40, 0.75),      # 阿奇蓝
    'marshall': (0.83, 0.18, 0.18),   # 毛毛红
    'skye': (0.93, 0.25, 0.48),       # 天天粉
    'rubble': (0.99, 0.85, 0.21),     # 小砾黄
    'rocky': (0.26, 0.63, 0.28),      # 灰灰绿
    'zuma': (1.0, 0.60, 0.0),         # 路马橙
    'everest': (0.0, 0.67, 0.76),     # 珠珠青
    'tracker': (0.49, 0.70, 0.26),    # 小克绿
    'bone': (1.0, 0.97, 0.88),        # 骨头色
    'paw': (0.55, 0.43, 0.39),        # 爪印棕
    'gold': (1.0, 0.84, 0.0),         # 徽章金
    'brown': (0.55, 0.35, 0.20),      # 棕色
}


# ============================================================
# 汪汪队徽章
# ============================================================

class PawBadgeWidget(Widget):
    """汪汪队徽章 - 六边形带爪印"""
    def __init__(self, color=None, **kwargs):
        super().__init__(**kwargs)
        self.badge_color = color or PAW_COLORS['blue']
        self.bind(size=self.draw, pos=self.draw)
        Clock.schedule_once(lambda dt: self.draw(), 0)
    
    def draw(self, *args):
        self.canvas.clear()
        cx, cy = self.center_x, self.center_y
        r = min(self.width, self.height) * 0.4
        with self.canvas:
            # 外圈金边
            Color(*PAW_COLORS['gold'])
            points = []
            for i in range(6):
                angle = math.radians(60 * i - 30)
                points.extend([cx + r * 1.1 * math.cos(angle), cy + r * 1.1 * math.sin(angle)])
            Line(points=points, width=dp(3), close=True)
            
            # 徽章主体
            Color(*self.badge_color)
            for i in range(6):
                angle1 = math.radians(60 * i - 30)
                angle2 = math.radians(60 * (i + 1) - 30)
                Triangle(points=[
                    cx, cy,
                    cx + r * math.cos(angle1), cy + r * math.sin(angle1),
                    cx + r * math.cos(angle2), cy + r * math.sin(angle2)
                ])
            
            # 中心爪印
            pr = r * 0.25
            # 大肉垫
            Color(1, 1, 1)
            Ellipse(pos=(cx - pr * 1.2, cy - pr * 1.5), size=(pr * 2.4, pr * 2))
            # 四个小肉垫
            Ellipse(pos=(cx - pr * 1.8, cy + pr * 0.1), size=(pr * 1.1, pr * 1.3))
            Ellipse(pos=(cx - pr * 0.6, cy + pr * 0.5), size=(pr * 1.1, pr * 1.3))
            Ellipse(pos=(cx + pr * 0.4, cy + pr * 0.1), size=(pr * 1.1, pr * 1.3))
            Ellipse(pos=(cx + pr * 0.7, cy - pr * 0.6), size=(pr * 0.9, pr * 1.1))


class PawPrintWidget(Widget):
    """大爪印 - 汪汪队标志性元素"""
    def __init__(self, color=None, **kwargs):
        super().__init__(**kwargs)
        self.paw_color = color or PAW_COLORS['paw']
        self.bind(size=self.draw, pos=self.draw)
        Clock.schedule_once(lambda dt: self.draw(), 0)
    
    def draw(self, *args):
        self.canvas.clear()
        cx, cy = self.center_x, self.center_y
        r = min(self.width, self.height) * 0.15
        with self.canvas:
            Color(*self.paw_color)
            # 大肉垫
            Ellipse(pos=(cx - r * 1.5, cy - r * 2), size=(r * 3, r * 2.5))
            # 四个小肉垫（脚趾）
            Ellipse(pos=(cx - r * 2.2, cy + r * 0.2), size=(r * 1.3, r * 1.6))
            Ellipse(pos=(cx - r * 0.8, cy + r * 0.8), size=(r * 1.3, r * 1.6))
            Ellipse(pos=(cx + r * 0.5, cy + r * 0.2), size=(r * 1.3, r * 1.6))
            Ellipse(pos=(cx + r * 0.9, cy - r * 0.8), size=(r * 1.1, r * 1.4))


class BoneWidget(Widget):
    """骨头 - 狗狗最爱"""
    rotation = 0
    
    def __init__(self, color=None, **kwargs):
        super().__init__(**kwargs)
        self.bone_color = color or PAW_COLORS['bone']
        self.bind(size=self.draw, pos=self.draw)
        Clock.schedule_once(lambda dt: self.draw(), 0)
    
    def draw(self, *args):
        self.canvas.clear()
        cx, cy = self.center_x, self.center_y
        r = min(self.width, self.height) * 0.15
        with self.canvas:
            PushMatrix()
            Rotate(angle=self.rotation, origin=(cx, cy))
            Color(*self.bone_color)
            # 骨头中间
            Rectangle(pos=(cx - r * 1.5, cy - r * 0.4), size=(r * 3, r * 0.8))
            # 左边两个圆头
            Ellipse(pos=(cx - r * 2.2, cy - r * 0.1), size=(r * 0.9, r * 0.9))
            Ellipse(pos=(cx - r * 2.2, cy - r * 0.8), size=(r * 0.9, r * 0.9))
            # 右边两个圆头
            Ellipse(pos=(cx + r * 1.3, cy - r * 0.1), size=(r * 0.9, r * 0.9))
            Ellipse(pos=(cx + r * 1.3, cy - r * 0.8), size=(r * 0.9, r * 0.9))
            # 高光
            Color(1, 1, 1, 0.4)
            Ellipse(pos=(cx - r * 0.8, cy + r * 0.1), size=(r * 0.4, r * 0.2))
            PopMatrix()


class DogBowlWidget(Widget):
    """狗碗 - 装满狗粮"""
    def __init__(self, bowl_color=None, **kwargs):
        super().__init__(**kwargs)
        self.bowl_color = bowl_color or PAW_COLORS['red']
        self.bind(size=self.draw, pos=self.draw)
        Clock.schedule_once(lambda dt: self.draw(), 0)
    
    def draw(self, *args):
        self.canvas.clear()
        cx, cy = self.center_x, self.center_y
        r = min(self.width, self.height) * 0.3
        with self.canvas:
            # 碗身
            Color(*self.bowl_color)
            # 碗的外形（梯形）
            points = [
                cx - r * 1.2, cy - r * 0.3,
                cx - r * 0.8, cy - r * 0.8,
                cx + r * 0.8, cy - r * 0.8,
                cx + r * 1.2, cy - r * 0.3,
            ]
            Line(points=points, width=dp(3), close=True)
            # 填充碗身
            for i in range(10):
                y_offset = -r * 0.3 - i * r * 0.05
                width_factor = 1.2 - i * 0.04
                Rectangle(pos=(cx - r * width_factor, cy + y_offset), size=(r * width_factor * 2, r * 0.06))
            
            # 碗里的狗粮
            Color(0.6, 0.4, 0.2)
            Ellipse(pos=(cx - r * 0.9, cy - r * 0.2), size=(r * 1.8, r * 0.5))
            # 狗粮颗粒
            Color(0.5, 0.35, 0.15)
            for i in range(5):
                px = cx - r * 0.6 + i * r * 0.3
                py = cy - r * 0.1 + random.uniform(-r * 0.1, r * 0.1)
                Ellipse(pos=(px, py), size=(r * 0.25, r * 0.2))
            
            # 碗上的爪印装饰
            Color(1, 1, 1, 0.8)
            pr = r * 0.12
            pcx, pcy = cx, cy - r * 0.55
            Ellipse(pos=(pcx - pr, pcy - pr * 1.2), size=(pr * 2, pr * 1.6))
            Ellipse(pos=(pcx - pr * 1.5, pcy + pr * 0.2), size=(pr * 0.8, pr))
            Ellipse(pos=(pcx - pr * 0.3, pcy + pr * 0.5), size=(pr * 0.8, pr))
            Ellipse(pos=(pcx + pr * 0.5, pcy + pr * 0.2), size=(pr * 0.8, pr))


class DogHouseWidget(Widget):
    """狗窝 - 温馨的小屋"""
    def __init__(self, roof_color=None, **kwargs):
        super().__init__(**kwargs)
        self.roof_color = roof_color or PAW_COLORS['red']
        self.bind(size=self.draw, pos=self.draw)
        Clock.schedule_once(lambda dt: self.draw(), 0)
    
    def draw(self, *args):
        self.canvas.clear()
        cx, cy = self.center_x, self.center_y
        r = min(self.width, self.height) * 0.25
        with self.canvas:
            # 房子主体
            Color(0.6, 0.45, 0.3)
            Rectangle(pos=(cx - r * 1.2, cy - r * 1.2), size=(r * 2.4, r * 1.8))
            
            # 屋顶
            Color(*self.roof_color)
            Triangle(points=[
                cx - r * 1.5, cy + r * 0.6,
                cx, cy + r * 1.8,
                cx + r * 1.5, cy + r * 0.6
            ])
            
            # 门洞
            Color(0.2, 0.15, 0.1)
            Ellipse(pos=(cx - r * 0.5, cy - r * 1.1), size=(r * 1, r * 1.3))
            
            # 门洞上方的骨头装饰
            Color(*PAW_COLORS['bone'])
            br = r * 0.12
            Rectangle(pos=(cx - br * 1.2, cy + r * 0.2), size=(br * 2.4, br * 0.6))
            Ellipse(pos=(cx - br * 1.8, cy + r * 0.1), size=(br * 0.7, br * 0.8))
            Ellipse(pos=(cx - br * 1.8, cy + r * 0.35), size=(br * 0.7, br * 0.8))
            Ellipse(pos=(cx + br * 1.1, cy + r * 0.1), size=(br * 0.7, br * 0.8))
            Ellipse(pos=(cx + br * 1.1, cy + r * 0.35), size=(br * 0.7, br * 0.8))


class CollarWidget(Widget):
    """项圈 - 带铃铛"""
    def __init__(self, color=None, **kwargs):
        super().__init__(**kwargs)
        self.collar_color = color or PAW_COLORS['red']
        self.bind(size=self.draw, pos=self.draw)
        Clock.schedule_once(lambda dt: self.draw(), 0)
    
    def draw(self, *args):
        self.canvas.clear()
        cx, cy = self.center_x, self.center_y
        r = min(self.width, self.height) * 0.35
        with self.canvas:
            # 项圈带子
            Color(*self.collar_color)
            Line(ellipse=(cx - r, cy - r * 0.3, r * 2, r * 1.2, 200, 340), width=dp(8))
            
            # 金属扣
            Color(*PAW_COLORS['gold'])
            Ellipse(pos=(cx - r * 0.15, cy - r * 0.5), size=(r * 0.3, r * 0.3))
            
            # 铃铛
            Color(*PAW_COLORS['gold'])
            Ellipse(pos=(cx - r * 0.25, cy - r * 0.9), size=(r * 0.5, r * 0.5))
            # 铃铛下面的小球
            Ellipse(pos=(cx - r * 0.1, cy - r * 1.1), size=(r * 0.2, r * 0.2))
            # 铃铛高光
            Color(1, 1, 0.8, 0.5)
            Ellipse(pos=(cx - r * 0.1, cy - r * 0.7), size=(r * 0.15, r * 0.15))


# ============================================================
# 汪汪队狗狗头像（简化版，适合装饰）
# ============================================================

class ChaseHeadWidget(Widget):
    """阿奇头像 - 德国牧羊犬警察"""
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.bind(size=self.draw, pos=self.draw)
        Clock.schedule_once(lambda dt: self.draw(), 0)
    
    def draw(self, *args):
        self.canvas.clear()
        cx, cy = self.center_x, self.center_y
        r = min(self.width, self.height) * 0.3
        with self.canvas:
            # 耳朵
            Color(0.36, 0.25, 0.22)
            Triangle(points=[cx - r * 1.1, cy + r * 0.5, cx - r * 0.5, cy + r * 1.8, cx - r * 0.1, cy + r * 0.5])
            Triangle(points=[cx + r * 0.1, cy + r * 0.5, cx + r * 0.5, cy + r * 1.8, cx + r * 1.1, cy + r * 0.5])
            # 头
            Color(0.55, 0.43, 0.39)
            Ellipse(pos=(cx - r, cy - r * 0.5), size=(r * 2, r * 1.8))
            # 脸（浅色）
            Color(0.84, 0.80, 0.76)
            Ellipse(pos=(cx - r * 0.65, cy - r * 0.6), size=(r * 1.3, r * 1.1))
            # 眼睛
            Color(1, 1, 1)
            Ellipse(pos=(cx - r * 0.55, cy + r * 0.15), size=(r * 0.45, r * 0.45))
            Ellipse(pos=(cx + r * 0.1, cy + r * 0.15), size=(r * 0.45, r * 0.45))
            Color(0.2, 0.15, 0.1)
            Ellipse(pos=(cx - r * 0.42, cy + r * 0.25), size=(r * 0.25, r * 0.25))
            Ellipse(pos=(cx + r * 0.2, cy + r * 0.25), size=(r * 0.25, r * 0.25))
            # 鼻子
            Color(0.1, 0.1, 0.1)
            Ellipse(pos=(cx - r * 0.18, cy - r * 0.2), size=(r * 0.36, r * 0.28))
            # 警察帽
            Color(*PAW_COLORS['chase'])
            Ellipse(pos=(cx - r * 0.7, cy + r * 0.9), size=(r * 1.4, r * 0.5))
            Rectangle(pos=(cx - r * 0.55, cy + r * 1.2), size=(r * 1.1, r * 0.4))
            # 帽徽
            Color(*PAW_COLORS['gold'])
            Ellipse(pos=(cx - r * 0.15, cy + r * 1.25), size=(r * 0.3, r * 0.28))


class MarshallHeadWidget(Widget):
    """毛毛头像 - 斑点狗消防员"""
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.bind(size=self.draw, pos=self.draw)
        Clock.schedule_once(lambda dt: self.draw(), 0)
    
    def draw(self, *args):
        self.canvas.clear()
        cx, cy = self.center_x, self.center_y
        r = min(self.width, self.height) * 0.3
        with self.canvas:
            # 耳朵（垂下的）
            Color(0.15, 0.15, 0.15)
            Ellipse(pos=(cx - r * 1.3, cy + r * 0.2), size=(r * 0.6, r * 1))
            Ellipse(pos=(cx + r * 0.7, cy + r * 0.2), size=(r * 0.6, r * 1))
            # 头（白色）
            Color(1, 1, 1)
            Ellipse(pos=(cx - r, cy - r * 0.5), size=(r * 2, r * 1.8))
            # 黑色斑点
            Color(0.15, 0.15, 0.15)
            Ellipse(pos=(cx - r * 0.8, cy + r * 0.5), size=(r * 0.35, r * 0.35))
            Ellipse(pos=(cx + r * 0.5, cy + r * 0.6), size=(r * 0.3, r * 0.3))
            Ellipse(pos=(cx + r * 0.2, cy - r * 0.1), size=(r * 0.25, r * 0.25))
            # 眼睛
            Color(1, 1, 1)
            Ellipse(pos=(cx - r * 0.55, cy + r * 0.1), size=(r * 0.45, r * 0.45))
            Ellipse(pos=(cx + r * 0.1, cy + r * 0.1), size=(r * 0.45, r * 0.45))
            Color(0.2, 0.15, 0.1)
            Ellipse(pos=(cx - r * 0.42, cy + r * 0.2), size=(r * 0.25, r * 0.25))
            Ellipse(pos=(cx + r * 0.2, cy + r * 0.2), size=(r * 0.25, r * 0.25))
            # 鼻子
            Color(0.1, 0.1, 0.1)
            Ellipse(pos=(cx - r * 0.18, cy - r * 0.25), size=(r * 0.36, r * 0.28))
            # 消防帽
            Color(*PAW_COLORS['marshall'])
            Ellipse(pos=(cx - r * 0.75, cy + r * 0.95), size=(r * 1.5, r * 0.55))
            # 帽子前沿
            Color(0.1, 0.1, 0.1)
            Rectangle(pos=(cx - r * 0.6, cy + r * 0.9), size=(r * 1.2, r * 0.15))


class SkyeHeadWidget(Widget):
    """天天头像 - 可卡犬飞行员"""
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.bind(size=self.draw, pos=self.draw)
        Clock.schedule_once(lambda dt: self.draw(), 0)
    
    def draw(self, *args):
        self.canvas.clear()
        cx, cy = self.center_x, self.center_y
        r = min(self.width, self.height) * 0.3
        with self.canvas:
            # 耳朵（长长的卷毛）
            Color(0.85, 0.65, 0.45)
            Ellipse(pos=(cx - r * 1.4, cy - r * 0.2), size=(r * 0.7, r * 1.4))
            Ellipse(pos=(cx + r * 0.7, cy - r * 0.2), size=(r * 0.7, r * 1.4))
            # 头
            Color(0.9, 0.75, 0.55)
            Ellipse(pos=(cx - r, cy - r * 0.4), size=(r * 2, r * 1.7))
            # 头顶毛发
            Color(0.85, 0.65, 0.45)
            Ellipse(pos=(cx - r * 0.5, cy + r * 0.8), size=(r * 1, r * 0.6))
            # 眼睛（大大的）
            Color(1, 1, 1)
            Ellipse(pos=(cx - r * 0.6, cy + r * 0.1), size=(r * 0.5, r * 0.5))
            Ellipse(pos=(cx + r * 0.1, cy + r * 0.1), size=(r * 0.5, r * 0.5))
            Color(*PAW_COLORS['skye'])
            Ellipse(pos=(cx - r * 0.48, cy + r * 0.2), size=(r * 0.3, r * 0.3))
            Ellipse(pos=(cx + r * 0.2, cy + r * 0.2), size=(r * 0.3, r * 0.3))
            Color(0, 0, 0)
            Ellipse(pos=(cx - r * 0.42, cy + r * 0.25), size=(r * 0.15, r * 0.15))
            Ellipse(pos=(cx + r * 0.26, cy + r * 0.25), size=(r * 0.15, r * 0.15))
            # 鼻子
            Color(0.1, 0.1, 0.1)
            Ellipse(pos=(cx - r * 0.15, cy - r * 0.15), size=(r * 0.3, r * 0.22))
            # 飞行眼镜（在头顶）
            Color(*PAW_COLORS['skye'])
            Line(ellipse=(cx - r * 0.7, cy + r * 0.85, r * 0.55, r * 0.4, 0, 360), width=dp(2))
            Line(ellipse=(cx + r * 0.15, cy + r * 0.85, r * 0.55, r * 0.4, 0, 360), width=dp(2))
            Line(points=[cx - r * 0.15, cy + r * 1.05, cx + r * 0.15, cy + r * 1.05], width=dp(2))


class RubbleHeadWidget(Widget):
    """小砾头像 - 英国斗牛犬工程师"""
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.bind(size=self.draw, pos=self.draw)
        Clock.schedule_once(lambda dt: self.draw(), 0)
    
    def draw(self, *args):
        self.canvas.clear()
        cx, cy = self.center_x, self.center_y
        r = min(self.width, self.height) * 0.3
        with self.canvas:
            # 耳朵（小小的）
            Color(0.55, 0.45, 0.35)
            Ellipse(pos=(cx - r * 1.1, cy + r * 0.5), size=(r * 0.4, r * 0.5))
            Ellipse(pos=(cx + r * 0.7, cy + r * 0.5), size=(r * 0.4, r * 0.5))
            # 头（宽宽的）
            Color(0.65, 0.55, 0.4)
            Ellipse(pos=(cx - r * 1.1, cy - r * 0.5), size=(r * 2.2, r * 1.6))
            # 脸部（浅色）
            Color(0.9, 0.85, 0.75)
            Ellipse(pos=(cx - r * 0.7, cy - r * 0.6), size=(r * 1.4, r * 1))
            # 眼睛
            Color(1, 1, 1)
            Ellipse(pos=(cx - r * 0.55, cy + r * 0.05), size=(r * 0.4, r * 0.4))
            Ellipse(pos=(cx + r * 0.15, cy + r * 0.05), size=(r * 0.4, r * 0.4))
            Color(0.2, 0.15, 0.1)
            Ellipse(pos=(cx - r * 0.45, cy + r * 0.12), size=(r * 0.22, r * 0.22))
            Ellipse(pos=(cx + r * 0.23, cy + r * 0.12), size=(r * 0.22, r * 0.22))
            # 鼻子（大大的）
            Color(0.1, 0.1, 0.1)
            Ellipse(pos=(cx - r * 0.22, cy - r * 0.35), size=(r * 0.44, r * 0.32))
            # 工程帽
            Color(*PAW_COLORS['rubble'])
            Ellipse(pos=(cx - r * 0.8, cy + r * 0.7), size=(r * 1.6, r * 0.6))
            Rectangle(pos=(cx - r * 0.65, cy + r * 1.1), size=(r * 1.3, r * 0.35))
            # 帽子前沿
            Color(0.2, 0.2, 0.2)
            Rectangle(pos=(cx - r * 0.75, cy + r * 0.65), size=(r * 1.5, r * 0.12))


class RockyHeadWidget(Widget):
    """灰灰头像 - 混血狗环保员"""
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.bind(size=self.draw, pos=self.draw)
        Clock.schedule_once(lambda dt: self.draw(), 0)
    
    def draw(self, *args):
        self.canvas.clear()
        cx, cy = self.center_x, self.center_y
        r = min(self.width, self.height) * 0.3
        with self.canvas:
            # 耳朵（一只竖一只垂）
            Color(0.5, 0.5, 0.5)
            Triangle(points=[cx - r * 1, cy + r * 0.5, cx - r * 0.5, cy + r * 1.6, cx - r * 0.1, cy + r * 0.5])
            Ellipse(pos=(cx + r * 0.6, cy + r * 0.3), size=(r * 0.5, r * 0.9))
            # 头
            Color(0.6, 0.6, 0.6)
            Ellipse(pos=(cx - r, cy - r * 0.5), size=(r * 2, r * 1.7))
            # 脸部斑纹
            Color(0.45, 0.45, 0.45)
            Ellipse(pos=(cx - r * 0.3, cy + r * 0.3), size=(r * 0.8, r * 0.6))
            # 眼睛
            Color(1, 1, 1)
            Ellipse(pos=(cx - r * 0.55, cy + r * 0.1), size=(r * 0.42, r * 0.42))
            Ellipse(pos=(cx + r * 0.13, cy + r * 0.1), size=(r * 0.42, r * 0.42))
            Color(0.2, 0.5, 0.2)
            Ellipse(pos=(cx - r * 0.45, cy + r * 0.18), size=(r * 0.25, r * 0.25))
            Ellipse(pos=(cx + r * 0.22, cy + r * 0.18), size=(r * 0.25, r * 0.25))
            # 鼻子
            Color(0.1, 0.1, 0.1)
            Ellipse(pos=(cx - r * 0.16, cy - r * 0.2), size=(r * 0.32, r * 0.25))
            # 环保帽
            Color(*PAW_COLORS['rocky'])
            Ellipse(pos=(cx - r * 0.7, cy + r * 0.9), size=(r * 1.4, r * 0.5))
            # 回收标志
            Color(1, 1, 1)
            # 简化的回收箭头
            Line(points=[cx - r * 0.15, cy + r * 1.05, cx, cy + r * 1.2, cx + r * 0.15, cy + r * 1.05], width=dp(2))


class ZumaHeadWidget(Widget):
    """路马头像 - 拉布拉多水上救援"""
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.bind(size=self.draw, pos=self.draw)
        Clock.schedule_once(lambda dt: self.draw(), 0)
    
    def draw(self, *args):
        self.canvas.clear()
        cx, cy = self.center_x, self.center_y
        r = min(self.width, self.height) * 0.3
        with self.canvas:
            # 耳朵（垂下的）
            Color(0.5, 0.35, 0.2)
            Ellipse(pos=(cx - r * 1.2, cy + r * 0.1), size=(r * 0.55, r * 1))
            Ellipse(pos=(cx + r * 0.65, cy + r * 0.1), size=(r * 0.55, r * 1))
            # 头
            Color(0.6, 0.45, 0.25)
            Ellipse(pos=(cx - r, cy - r * 0.5), size=(r * 2, r * 1.8))
            # 眼睛
            Color(1, 1, 1)
            Ellipse(pos=(cx - r * 0.55, cy + r * 0.15), size=(r * 0.45, r * 0.45))
            Ellipse(pos=(cx + r * 0.1, cy + r * 0.15), size=(r * 0.45, r * 0.45))
            Color(0.3, 0.2, 0.1)
            Ellipse(pos=(cx - r * 0.42, cy + r * 0.25), size=(r * 0.25, r * 0.25))
            Ellipse(pos=(cx + r * 0.2, cy + r * 0.25), size=(r * 0.25, r * 0.25))
            # 鼻子
            Color(0.15, 0.1, 0.05)
            Ellipse(pos=(cx - r * 0.18, cy - r * 0.15), size=(r * 0.36, r * 0.28))
            # 潜水头盔/帽子
            Color(*PAW_COLORS['zuma'])
            Ellipse(pos=(cx - r * 0.75, cy + r * 0.85), size=(r * 1.5, r * 0.6))
            # 护目镜
            Color(0.5, 0.8, 1, 0.7)
            Line(ellipse=(cx - r * 0.5, cy + r * 0.9, r * 1, r * 0.4, 0, 360), width=dp(2))


# ============================================================
# 汪汪队动画效果
# ============================================================

def animate_paw_bounce(widget, height=20, duration=0.6):
    """爪印弹跳动画"""
    original_y = widget.y
    anim = Animation(y=original_y + dp(height), duration=duration * 0.4, t='out_quad')
    anim += Animation(y=original_y, duration=duration * 0.6, t='out_bounce')
    anim.repeat = True
    anim.start(widget)
    return anim


def animate_bone_spin(widget, duration=2):
    """骨头旋转动画"""
    def update_rotation(dt):
        widget.rotation = (widget.rotation + 5) % 360
        widget.draw()
    Clock.schedule_interval(update_rotation, duration / 72)


def animate_tail_wag(widget, angle=20, duration=0.3):
    """摇尾巴动画（适用于有rotation属性的widget）"""
    anim = Animation(rotation=angle, duration=duration/2, t='in_out_sine')
    anim += Animation(rotation=-angle, duration=duration, t='in_out_sine')
    anim += Animation(rotation=0, duration=duration/2, t='in_out_sine')
    anim.repeat = True
    anim.start(widget)
    return anim


def animate_badge_shine(widget, duration=1.5):
    """徽章闪光动画"""
    anim = Animation(opacity=0.6, duration=duration/2, t='in_out_sine')
    anim += Animation(opacity=1, duration=duration/2, t='in_out_sine')
    anim.repeat = True
    anim.start(widget)
    return anim


# ============================================================
# 汪汪队特效
# ============================================================

def create_paw_trail(parent, start_x, start_y, count=5):
    """创建爪印轨迹"""
    for i in range(count):
        paw = PawPrintWidget(
            color=PAW_COLORS['paw'],
            size_hint=(None, None),
            size=(dp(30), dp(30)),
            pos=(start_x + i * dp(50), start_y + (i % 2) * dp(10))
        )
        paw.opacity = 0
        parent.add_widget(paw)
        
        # 依次出现
        anim = Animation(opacity=0.7, duration=0.3)
        anim += Animation(opacity=0.7, duration=1)
        anim += Animation(opacity=0, duration=0.5)
        anim.bind(on_complete=lambda a, w: parent.remove_widget(w))
        Clock.schedule_once(lambda dt, p=paw, a=anim: a.start(p), i * 0.3)


def create_bone_rain(parent, count=8):
    """骨头雨效果"""
    from kivy.core.window import Window
    
    for i in range(count):
        bone = BoneWidget(
            size_hint=(None, None),
            size=(dp(40), dp(25)),
            pos=(random.randint(50, int(Window.width - 50)), Window.height + dp(50))
        )
        bone.rotation = random.randint(-30, 30)
        parent.add_widget(bone)
        
        end_y = random.randint(-50, 100)
        duration = random.uniform(2, 4)
        
        anim = Animation(y=end_y, duration=duration, t='in_quad')
        anim &= Animation(opacity=0, duration=duration)
        anim.bind(on_complete=lambda a, w: parent.remove_widget(w))
        Clock.schedule_once(lambda dt, b=bone, a=anim: a.start(b), i * 0.2)


def create_badge_burst(parent, x, y, count=6):
    """徽章爆炸效果"""
    colors = [PAW_COLORS['chase'], PAW_COLORS['marshall'], PAW_COLORS['skye'], 
              PAW_COLORS['rubble'], PAW_COLORS['rocky'], PAW_COLORS['zuma']]
    
    for i in range(count):
        badge = PawBadgeWidget(
            color=colors[i % len(colors)],
            size_hint=(None, None),
            size=(dp(35), dp(35)),
            pos=(x - dp(17), y - dp(17))
        )
        parent.add_widget(badge)
        
        angle = math.radians(i * (360 / count))
        distance = random.randint(80, 140)
        end_x = x + distance * math.cos(angle)
        end_y = y + distance * math.sin(angle)
        
        anim = Animation(
            pos=(end_x, end_y),
            opacity=0,
            duration=random.uniform(0.8, 1.2),
            t='out_quad'
        )
        anim.bind(on_complete=lambda a, w: parent.remove_widget(w))
        anim.start(badge)


def create_puppy_celebration(parent, x, y):
    """狗狗庆祝效果 - 显示所有狗狗头像"""
    puppies = [ChaseHeadWidget, MarshallHeadWidget, SkyeHeadWidget, 
               RubbleHeadWidget, RockyHeadWidget, ZumaHeadWidget]
    
    for i, PuppyClass in enumerate(puppies):
        puppy = PuppyClass(
            size_hint=(None, None),
            size=(dp(50), dp(50)),
            pos=(x - dp(25), y - dp(25))
        )
        parent.add_widget(puppy)
        
        angle = math.radians(i * 60 + 30)
        distance = dp(100)
        end_x = x + distance * math.cos(angle) - dp(25)
        end_y = y + distance * math.sin(angle) - dp(25)
        
        # 先放大再移动
        anim = Animation(size=(dp(60), dp(60)), duration=0.2, t='out_back')
        anim += Animation(pos=(end_x, end_y), duration=0.5, t='out_quad')
        anim += Animation(opacity=0, duration=1, t='in_quad')
        anim.bind(on_complete=lambda a, w: parent.remove_widget(w))
        Clock.schedule_once(lambda dt, p=puppy, a=anim: a.start(p), i * 0.1)


# ============================================================
# 汪汪队场景装饰
# ============================================================

def create_paw_patrol_header(parent):
    """创建汪汪队风格的顶部装饰"""
    from kivy.core.window import Window
    
    # 左上角徽章
    badge = PawBadgeWidget(
        color=PAW_COLORS['blue'],
        size_hint=(None, None),
        size=(dp(55), dp(55)),
        pos=(dp(15), Window.height - dp(70))
    )
    parent.add_widget(badge)
    animate_badge_shine(badge)
    
    # 右上角骨头
    bone = BoneWidget(
        size_hint=(None, None),
        size=(dp(50), dp(30)),
        pos=(Window.width - dp(70), Window.height - dp(55))
    )
    parent.add_widget(bone)
    animate_bone_spin(bone, duration=4)
    
    return parent


def create_paw_patrol_footer(parent):
    """创建汪汪队风格的底部装饰"""
    from kivy.core.window import Window
    
    # 底部爪印装饰
    paw_positions = [dp(30), dp(120), Window.width - dp(150), Window.width - dp(60)]
    paw_colors = [PAW_COLORS['chase'], PAW_COLORS['marshall'], PAW_COLORS['skye'], PAW_COLORS['rubble']]
    
    for i, x in enumerate(paw_positions):
        paw = PawPrintWidget(
            color=paw_colors[i % len(paw_colors)],
            size_hint=(None, None),
            size=(dp(35), dp(35)),
            pos=(x, dp(15))
        )
        paw.opacity = 0.6
        parent.add_widget(paw)
        animate_paw_bounce(paw, height=10, duration=1 + i * 0.2)
    
    return parent


def create_paw_patrol_corners(parent):
    """在四角添加汪汪队装饰"""
    from kivy.core.window import Window
    
    # 左上 - 阿奇
    chase = ChaseHeadWidget(size_hint=(None, None), size=(dp(50), dp(50)), pos=(dp(10), Window.height - dp(65)))
    chase.opacity = 0.85
    parent.add_widget(chase)
    
    # 右上 - 毛毛
    marshall = MarshallHeadWidget(size_hint=(None, None), size=(dp(50), dp(50)), pos=(Window.width - dp(60), Window.height - dp(65)))
    marshall.opacity = 0.85
    parent.add_widget(marshall)
    
    # 左下 - 天天
    skye = SkyeHeadWidget(size_hint=(None, None), size=(dp(45), dp(45)), pos=(dp(15), dp(15)))
    skye.opacity = 0.85
    parent.add_widget(skye)
    
    # 右下 - 小砾
    rubble = RubbleHeadWidget(size_hint=(None, None), size=(dp(45), dp(45)), pos=(Window.width - dp(60), dp(15)))
    rubble.opacity = 0.85
    parent.add_widget(rubble)
    
    return parent


def create_paw_patrol_scene(parent, style='full'):
    """创建完整的汪汪队场景"""
    from kivy.core.window import Window
    
    if style == 'full':
        create_paw_patrol_header(parent)
        create_paw_patrol_footer(parent)
        
        # 中间添加一些漂浮的骨头
        for i in range(3):
            bone = BoneWidget(
                size_hint=(None, None),
                size=(dp(35), dp(22)),
                pos=(Window.width * (0.2 + i * 0.3), Window.height * 0.5)
            )
            bone.opacity = 0.5
            parent.add_widget(bone)
            # 漂浮动画
            original_y = bone.y
            anim = Animation(y=original_y + dp(15), duration=2 + i * 0.3, t='in_out_sine')
            anim += Animation(y=original_y, duration=2 + i * 0.3, t='in_out_sine')
            anim.repeat = True
            anim.start(bone)
    
    elif style == 'corners':
        create_paw_patrol_corners(parent)
    
    elif style == 'header':
        create_paw_patrol_header(parent)
    
    elif style == 'footer':
        create_paw_patrol_footer(parent)
    
    elif style == 'puppies':
        # 显示所有狗狗头像在顶部
        puppies = [
            (ChaseHeadWidget, dp(20)),
            (MarshallHeadWidget, dp(80)),
            (SkyeHeadWidget, dp(140)),
            (RubbleHeadWidget, Window.width - dp(180)),
            (RockyHeadWidget, Window.width - dp(120)),
            (ZumaHeadWidget, Window.width - dp(60)),
        ]
        for PuppyClass, x in puppies:
            puppy = PuppyClass(
                size_hint=(None, None),
                size=(dp(45), dp(45)),
                pos=(x, Window.height - dp(60))
            )
            puppy.opacity = 0.8
            parent.add_widget(puppy)
    
    return parent


# ============================================================
# 汪汪队主题按钮颜色
# ============================================================

def get_paw_patrol_button_colors():
    """获取汪汪队主题的按钮颜色列表"""
    return [
        PAW_COLORS['chase'],
        PAW_COLORS['marshall'],
        PAW_COLORS['skye'],
        PAW_COLORS['rubble'],
        PAW_COLORS['rocky'],
        PAW_COLORS['zuma'],
        PAW_COLORS['everest'],
        PAW_COLORS['tracker'],
    ]


def get_random_puppy_color():
    """随机获取一个狗狗的颜色"""
    colors = get_paw_patrol_button_colors()
    return random.choice(colors)
