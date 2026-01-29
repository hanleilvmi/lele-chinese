# -*- coding: utf-8 -*-
"""
汉字图片绘制模块 - 用Kivy Canvas绘制汉字对应的图形
"""
from kivy.uix.widget import Widget
from kivy.graphics import Color, Ellipse, Line, Rectangle, Triangle
from kivy.metrics import dp


class PictureCanvas(Widget):
    """绘制汉字对应图片的画布"""
    
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.current_char = None
        self.bind(size=self.redraw, pos=self.redraw)
    
    def redraw(self, *args):
        if self.current_char:
            self.draw_char(self.current_char)
    
    def draw_char(self, char):
        """根据汉字绘制对应图形"""
        self.current_char = char
        self.canvas.clear()
        
        cx = self.center_x
        cy = self.center_y
        size = min(self.width, self.height) * 0.8
        
        draw_funcs = {
            '日': self.draw_sun,
            '月': self.draw_moon,
            '水': self.draw_water,
            '火': self.draw_fire,
            '山': self.draw_mountain,
            '石': self.draw_stone,
            '田': self.draw_field,
            '土': self.draw_soil,
            '人': self.draw_person,
            '口': self.draw_mouth,
            '手': self.draw_hand,
            '足': self.draw_foot,
            '大': self.draw_big,
            '小': self.draw_small,
            '上': self.draw_up,
            '下': self.draw_down,
            '天': self.draw_sky,
            '地': self.draw_earth,
            '花': self.draw_flower,
            '草': self.draw_grass,
            '树': self.draw_tree,
            '鸟': self.draw_bird,
            '爸': self.draw_father,
            '妈': self.draw_mother,
            '爷': self.draw_grandpa,
            '奶': self.draw_grandma,
            '哥': self.draw_brother,
            '姐': self.draw_sister,
            '弟': self.draw_young_brother,
            '妹': self.draw_young_sister,
            '吃': self.draw_eat,
            '喝': self.draw_drink,
            '看': self.draw_see,
            '听': self.draw_hear,
            '左': self.draw_left,
            '右': self.draw_right,
            # 新增汉字绘图
            '风': self.draw_wind,
            '宝': self.draw_baby,
            '开': self.draw_open,
            '关': self.draw_close,
            '里': self.draw_inside,
            '他': self.draw_he,
            '工': self.draw_worker,
            '儿': self.draw_child,
            '老': self.draw_old,
            '好': self.draw_good,
            '饭': self.draw_rice,
            '玩': self.draw_play,
            '叔': self.draw_uncle,
            '自': self.draw_self,
            '姑': self.draw_aunt,
            '娘': self.draw_girl,
            '电': self.draw_electric,
            '木': self.draw_wood,
            '比': self.draw_compare,
            '图': self.draw_picture,
            '一': self.draw_one,
            '三': self.draw_three,
            '四': self.draw_four,
            '五': self.draw_five,
            '羊': self.draw_sheep,
            '白': self.draw_white,
            '牛': self.draw_cow,
            '鼠': self.draw_mouse,
            '心': self.draw_heart,
            '可': self.draw_ok,
            '说': self.draw_speak,
            '两': self.draw_two,
            '男': self.draw_boy,
            '你': self.draw_you,
            '不': self.draw_no,
            '子': self.draw_kid,
            '在': self.draw_at,
            '头': self.draw_head,
            '我': self.draw_me,
            '房': self.draw_house,
        }
        
        func = draw_funcs.get(char, self.draw_default)
        func(cx, cy, size)
    
    def draw_sun(self, cx, cy, size):
        """画太阳"""
        with self.canvas:
            # 太阳本体 - 黄色圆
            Color(1, 0.8, 0)
            r = size * 0.25
            Ellipse(pos=(cx - r, cy - r), size=(r*2, r*2))
            # 光芒
            Color(1, 0.6, 0)
            for i in range(8):
                import math
                angle = i * 45 * math.pi / 180
                x1 = cx + r * 1.2 * math.cos(angle)
                y1 = cy + r * 1.2 * math.sin(angle)
                x2 = cx + r * 1.8 * math.cos(angle)
                y2 = cy + r * 1.8 * math.sin(angle)
                Line(points=[x1, y1, x2, y2], width=dp(3))
    
    def draw_moon(self, cx, cy, size):
        """画月亮"""
        with self.canvas:
            Color(1, 0.95, 0.6)
            r = size * 0.3
            Ellipse(pos=(cx - r, cy - r), size=(r*2, r*2))
            # 用深色圆遮挡形成月牙
            Color(0.88, 0.96, 1)
            Ellipse(pos=(cx - r*0.3, cy - r*0.8), size=(r*1.8, r*1.8))

    def draw_water(self, cx, cy, size):
        """画水滴"""
        with self.canvas:
            Color(0.2, 0.6, 1)
            # 水滴形状用线条
            r = size * 0.25
            points = [
                cx, cy + r * 1.5,  # 顶点
                cx - r, cy - r * 0.5,
                cx - r * 0.8, cy - r,
                cx, cy - r * 1.2,
                cx + r * 0.8, cy - r,
                cx + r, cy - r * 0.5,
                cx, cy + r * 1.5,
            ]
            Line(points=points, width=dp(3), close=True)
            # 填充效果 - 画几条波浪线
            Color(0.4, 0.7, 1)
            Line(points=[cx - r*0.5, cy, cx, cy + r*0.3, cx + r*0.5, cy], width=dp(2))
            Line(points=[cx - r*0.3, cy - r*0.4, cx, cy - r*0.2, cx + r*0.3, cy - r*0.4], width=dp(2))
    
    def draw_fire(self, cx, cy, size):
        """画火焰"""
        with self.canvas:
            r = size * 0.3
            # 外层火焰 - 橙色
            Color(1, 0.5, 0)
            points = [
                cx, cy + r * 1.5,
                cx - r * 0.8, cy,
                cx - r * 0.4, cy + r * 0.3,
                cx - r * 0.6, cy - r,
                cx, cy - r * 0.5,
                cx + r * 0.6, cy - r,
                cx + r * 0.4, cy + r * 0.3,
                cx + r * 0.8, cy,
            ]
            Line(points=points, width=dp(4), close=True)
            # 内层火焰 - 黄色
            Color(1, 0.9, 0)
            inner = [
                cx, cy + r,
                cx - r * 0.4, cy + r * 0.2,
                cx - r * 0.3, cy - r * 0.3,
                cx, cy,
                cx + r * 0.3, cy - r * 0.3,
                cx + r * 0.4, cy + r * 0.2,
            ]
            Line(points=inner, width=dp(3), close=True)
    
    def draw_mountain(self, cx, cy, size):
        """画山"""
        with self.canvas:
            r = size * 0.4
            # 大山
            Color(0.4, 0.7, 0.3)
            Line(points=[cx - r, cy - r*0.6, cx, cy + r*0.8, cx + r, cy - r*0.6], width=dp(4), close=True)
            # 小山
            Color(0.5, 0.8, 0.4)
            Line(points=[cx - r*1.2, cy - r*0.6, cx - r*0.5, cy + r*0.3, cx, cy - r*0.6], width=dp(3), close=True)
            Line(points=[cx, cy - r*0.6, cx + r*0.5, cy + r*0.3, cx + r*1.2, cy - r*0.6], width=dp(3), close=True)
            # 山顶雪
            Color(1, 1, 1)
            Ellipse(pos=(cx - dp(8), cy + r*0.6), size=(dp(16), dp(12)))
    
    def draw_stone(self, cx, cy, size):
        """画石头"""
        with self.canvas:
            Color(0.6, 0.6, 0.6)
            r = size * 0.3
            # 不规则石头形状
            points = [
                cx - r, cy - r*0.3,
                cx - r*0.7, cy + r*0.5,
                cx + r*0.3, cy + r*0.6,
                cx + r, cy + r*0.2,
                cx + r*0.8, cy - r*0.5,
                cx, cy - r*0.6,
            ]
            Line(points=points, width=dp(4), close=True)
            # 纹理
            Color(0.5, 0.5, 0.5)
            Line(points=[cx - r*0.3, cy + r*0.2, cx + r*0.2, cy - r*0.1], width=dp(2))
    
    def draw_field(self, cx, cy, size):
        """画田地"""
        with self.canvas:
            r = size * 0.35
            # 外框
            Color(0.6, 0.4, 0.2)
            Line(rectangle=(cx - r, cy - r, r*2, r*2), width=dp(3))
            # 十字分割
            Line(points=[cx, cy - r, cx, cy + r], width=dp(3))
            Line(points=[cx - r, cy, cx + r, cy], width=dp(3))
            # 绿色庄稼
            Color(0.3, 0.7, 0.3)
            offset = r * 0.5
            for dx, dy in [(-offset, offset), (offset, offset), (-offset, -offset), (offset, -offset)]:
                Ellipse(pos=(cx + dx - dp(8), cy + dy - dp(8)), size=(dp(16), dp(16)))
    
    def draw_soil(self, cx, cy, size):
        """画土"""
        with self.canvas:
            r = size * 0.35
            Color(0.6, 0.4, 0.2)
            # 土堆形状
            Rectangle(pos=(cx - r, cy - r*0.8), size=(r*2, r*0.6))
            # 上面的土丘
            Ellipse(pos=(cx - r*0.8, cy - r*0.3), size=(r*1.6, r*0.8))
            # 小草
            Color(0.3, 0.7, 0.3)
            Line(points=[cx - r*0.3, cy + r*0.2, cx - r*0.2, cy + r*0.5], width=dp(2))
            Line(points=[cx, cy + r*0.2, cx + r*0.1, cy + r*0.6], width=dp(2))
            Line(points=[cx + r*0.3, cy + r*0.2, cx + r*0.2, cy + r*0.5], width=dp(2))

    def draw_person(self, cx, cy, size):
        """画人"""
        with self.canvas:
            r = size * 0.35
            Color(0.9, 0.7, 0.5)
            # 头
            Ellipse(pos=(cx - r*0.25, cy + r*0.4), size=(r*0.5, r*0.5))
            Color(0.3, 0.5, 0.8)
            # 身体
            Line(points=[cx, cy + r*0.4, cx, cy - r*0.3], width=dp(4))
            # 手臂
            Line(points=[cx - r*0.5, cy + r*0.1, cx, cy + r*0.2, cx + r*0.5, cy + r*0.1], width=dp(3))
            # 腿
            Line(points=[cx, cy - r*0.3, cx - r*0.3, cy - r*0.8], width=dp(3))
            Line(points=[cx, cy - r*0.3, cx + r*0.3, cy - r*0.8], width=dp(3))
    
    def draw_mouth(self, cx, cy, size):
        """画嘴巴/口"""
        with self.canvas:
            r = size * 0.3
            Color(1, 0.6, 0.6)
            # 嘴唇外框
            Line(rectangle=(cx - r, cy - r*0.6, r*2, r*1.2), width=dp(4))
            # 舌头
            Color(1, 0.4, 0.4)
            Ellipse(pos=(cx - r*0.4, cy - r*0.4), size=(r*0.8, r*0.5))
    
    def draw_hand(self, cx, cy, size):
        """画手"""
        with self.canvas:
            r = size * 0.35
            Color(0.9, 0.75, 0.6)
            # 手掌
            Ellipse(pos=(cx - r*0.5, cy - r*0.6), size=(r, r*0.8))
            # 五个手指
            for i, offset in enumerate([-0.4, -0.2, 0, 0.2, 0.4]):
                finger_len = r*0.7 if i == 2 else r*0.5
                Line(points=[cx + r*offset, cy + r*0.1, cx + r*offset, cy + r*0.1 + finger_len], width=dp(6))
    
    def draw_foot(self, cx, cy, size):
        """画脚"""
        with self.canvas:
            r = size * 0.35
            Color(0.9, 0.75, 0.6)
            # 脚掌
            Ellipse(pos=(cx - r*0.4, cy - r*0.5), size=(r*1.2, r*0.6))
            # 脚趾
            for i, offset in enumerate([-0.3, -0.1, 0.1, 0.3, 0.5]):
                Ellipse(pos=(cx + r*offset - dp(6), cy + r*0.1), size=(dp(12), dp(15)))
    
    def draw_big(self, cx, cy, size):
        """画大 - 一个大圆"""
        with self.canvas:
            r = size * 0.4
            Color(1, 0.5, 0.3)
            Ellipse(pos=(cx - r, cy - r), size=(r*2, r*2))
            Color(1, 0.7, 0.5)
            Ellipse(pos=(cx - r*0.7, cy - r*0.7), size=(r*1.4, r*1.4))
    
    def draw_small(self, cx, cy, size):
        """画小 - 一个小圆"""
        with self.canvas:
            r = size * 0.12
            Color(0.5, 0.8, 1)
            Ellipse(pos=(cx - r, cy - r), size=(r*2, r*2))
    
    def draw_up(self, cx, cy, size):
        """画上 - 向上箭头"""
        with self.canvas:
            r = size * 0.35
            Color(0.3, 0.7, 0.3)
            # 箭头
            Line(points=[cx, cy - r, cx, cy + r*0.8], width=dp(4))
            Line(points=[cx - r*0.5, cy + r*0.3, cx, cy + r*0.8, cx + r*0.5, cy + r*0.3], width=dp(4))
    
    def draw_down(self, cx, cy, size):
        """画下 - 向下箭头"""
        with self.canvas:
            r = size * 0.35
            Color(0.8, 0.4, 0.3)
            # 箭头
            Line(points=[cx, cy + r, cx, cy - r*0.8], width=dp(4))
            Line(points=[cx - r*0.5, cy - r*0.3, cx, cy - r*0.8, cx + r*0.5, cy - r*0.3], width=dp(4))
    
    def draw_left(self, cx, cy, size):
        """画左 - 向左箭头"""
        with self.canvas:
            r = size * 0.35
            Color(0.3, 0.5, 0.8)
            Line(points=[cx + r, cy, cx - r*0.8, cy], width=dp(4))
            Line(points=[cx - r*0.3, cy + r*0.5, cx - r*0.8, cy, cx - r*0.3, cy - r*0.5], width=dp(4))
    
    def draw_right(self, cx, cy, size):
        """画右 - 向右箭头"""
        with self.canvas:
            r = size * 0.35
            Color(0.8, 0.5, 0.3)
            Line(points=[cx - r, cy, cx + r*0.8, cy], width=dp(4))
            Line(points=[cx + r*0.3, cy + r*0.5, cx + r*0.8, cy, cx + r*0.3, cy - r*0.5], width=dp(4))

    def draw_sky(self, cx, cy, size):
        """画天空"""
        with self.canvas:
            r = size * 0.4
            # 蓝天
            Color(0.5, 0.8, 1)
            Rectangle(pos=(cx - r, cy - r*0.5), size=(r*2, r*1.2))
            # 白云
            Color(1, 1, 1)
            Ellipse(pos=(cx - r*0.8, cy + r*0.2), size=(r*0.5, r*0.3))
            Ellipse(pos=(cx - r*0.5, cy + r*0.3), size=(r*0.6, r*0.4))
            Ellipse(pos=(cx - r*0.1, cy + r*0.2), size=(r*0.5, r*0.3))
            # 太阳
            Color(1, 0.9, 0.3)
            Ellipse(pos=(cx + r*0.4, cy + r*0.3), size=(r*0.4, r*0.4))
    
    def draw_earth(self, cx, cy, size):
        """画大地"""
        with self.canvas:
            r = size * 0.4
            # 地面
            Color(0.6, 0.4, 0.2)
            Rectangle(pos=(cx - r, cy - r*0.6), size=(r*2, r*0.8))
            # 草地
            Color(0.3, 0.7, 0.3)
            Rectangle(pos=(cx - r, cy + r*0.1), size=(r*2, r*0.3))
            # 小花
            Color(1, 0.5, 0.5)
            Ellipse(pos=(cx - r*0.5, cy + r*0.2), size=(dp(10), dp(10)))
            Color(1, 1, 0.5)
            Ellipse(pos=(cx + r*0.3, cy + r*0.15), size=(dp(10), dp(10)))
    
    def draw_flower(self, cx, cy, size):
        """画花"""
        with self.canvas:
            r = size * 0.25
            # 花瓣
            Color(1, 0.5, 0.7)
            for i in range(5):
                import math
                angle = i * 72 * math.pi / 180
                px = cx + r * 0.6 * math.cos(angle)
                py = cy + r * 0.6 * math.sin(angle)
                Ellipse(pos=(px - r*0.35, py - r*0.35), size=(r*0.7, r*0.7))
            # 花心
            Color(1, 0.9, 0.3)
            Ellipse(pos=(cx - r*0.3, cy - r*0.3), size=(r*0.6, r*0.6))
            # 茎
            Color(0.3, 0.7, 0.3)
            Line(points=[cx, cy - r*0.5, cx, cy - r*1.5], width=dp(3))
            # 叶子
            Ellipse(pos=(cx - r*0.6, cy - r*1.2), size=(r*0.5, r*0.25))
    
    def draw_grass(self, cx, cy, size):
        """画草"""
        with self.canvas:
            r = size * 0.35
            Color(0.3, 0.7, 0.3)
            # 多根草
            for offset in [-0.4, -0.2, 0, 0.2, 0.4]:
                x = cx + r * offset
                Line(points=[x, cy - r*0.6, x - r*0.1, cy + r*0.5], width=dp(3))
                Line(points=[x, cy - r*0.6, x + r*0.1, cy + r*0.6], width=dp(3))
            # 地面
            Color(0.5, 0.35, 0.2)
            Rectangle(pos=(cx - r, cy - r*0.7), size=(r*2, r*0.2))
    
    def draw_tree(self, cx, cy, size):
        """画树"""
        with self.canvas:
            r = size * 0.35
            # 树干
            Color(0.5, 0.3, 0.1)
            Rectangle(pos=(cx - r*0.15, cy - r), size=(r*0.3, r*1.2))
            # 树冠
            Color(0.2, 0.6, 0.2)
            Ellipse(pos=(cx - r*0.7, cy + r*0.1), size=(r*1.4, r*1.0))
            Color(0.3, 0.7, 0.3)
            Ellipse(pos=(cx - r*0.5, cy + r*0.3), size=(r*1.0, r*0.8))
    
    def draw_bird(self, cx, cy, size):
        """画鸟"""
        with self.canvas:
            r = size * 0.3
            # 身体
            Color(1, 0.8, 0.3)
            Ellipse(pos=(cx - r*0.5, cy - r*0.3), size=(r*1.0, r*0.6))
            # 头
            Ellipse(pos=(cx + r*0.2, cy), size=(r*0.5, r*0.5))
            # 嘴
            Color(1, 0.5, 0)
            Line(points=[cx + r*0.7, cy + r*0.25, cx + r*1.0, cy + r*0.2], width=dp(3))
            # 翅膀
            Color(1, 0.6, 0.2)
            Ellipse(pos=(cx - r*0.3, cy + r*0.1), size=(r*0.6, r*0.4))
            # 眼睛
            Color(0, 0, 0)
            Ellipse(pos=(cx + r*0.35, cy + r*0.2), size=(dp(6), dp(6)))

    def draw_father(self, cx, cy, size):
        """画爸爸"""
        with self.canvas:
            r = size * 0.3
            # 头
            Color(0.9, 0.75, 0.6)
            Ellipse(pos=(cx - r*0.35, cy + r*0.3), size=(r*0.7, r*0.7))
            # 头发
            Color(0.2, 0.15, 0.1)
            Ellipse(pos=(cx - r*0.3, cy + r*0.7), size=(r*0.6, r*0.3))
            # 身体 - 蓝色衬衫
            Color(0.2, 0.4, 0.7)
            Rectangle(pos=(cx - r*0.4, cy - r*0.5), size=(r*0.8, r*0.8))
            # 眼睛
            Color(0, 0, 0)
            Ellipse(pos=(cx - r*0.15, cy + r*0.55), size=(dp(5), dp(5)))
            Ellipse(pos=(cx + r*0.05, cy + r*0.55), size=(dp(5), dp(5)))
            # 微笑
            Color(0.8, 0.4, 0.3)
            Line(points=[cx - r*0.1, cy + r*0.4, cx, cy + r*0.35, cx + r*0.1, cy + r*0.4], width=dp(2))
    
    def draw_mother(self, cx, cy, size):
        """画妈妈"""
        with self.canvas:
            r = size * 0.3
            # 头
            Color(0.9, 0.75, 0.6)
            Ellipse(pos=(cx - r*0.35, cy + r*0.3), size=(r*0.7, r*0.7))
            # 长发
            Color(0.3, 0.2, 0.1)
            Ellipse(pos=(cx - r*0.5, cy + r*0.5), size=(r*0.4, r*0.6))
            Ellipse(pos=(cx + r*0.1, cy + r*0.5), size=(r*0.4, r*0.6))
            Ellipse(pos=(cx - r*0.35, cy + r*0.75), size=(r*0.7, r*0.3))
            # 身体 - 红色裙子
            Color(0.9, 0.3, 0.4)
            Rectangle(pos=(cx - r*0.4, cy - r*0.6), size=(r*0.8, r*0.9))
            # 眼睛
            Color(0, 0, 0)
            Ellipse(pos=(cx - r*0.15, cy + r*0.55), size=(dp(5), dp(5)))
            Ellipse(pos=(cx + r*0.05, cy + r*0.55), size=(dp(5), dp(5)))
            # 微笑
            Color(0.9, 0.4, 0.4)
            Line(points=[cx - r*0.1, cy + r*0.4, cx, cy + r*0.35, cx + r*0.1, cy + r*0.4], width=dp(2))
    
    def draw_grandpa(self, cx, cy, size):
        """画爷爷"""
        with self.canvas:
            r = size * 0.3
            # 头
            Color(0.9, 0.78, 0.65)
            Ellipse(pos=(cx - r*0.35, cy + r*0.3), size=(r*0.7, r*0.7))
            # 白发
            Color(0.9, 0.9, 0.9)
            Ellipse(pos=(cx - r*0.3, cy + r*0.75), size=(r*0.6, r*0.25))
            # 身体
            Color(0.5, 0.5, 0.5)
            Rectangle(pos=(cx - r*0.4, cy - r*0.5), size=(r*0.8, r*0.8))
            # 眼镜
            Color(0.3, 0.3, 0.3)
            Line(points=[cx - r*0.25, cy + r*0.55, cx - r*0.05, cy + r*0.55], width=dp(2))
            Line(points=[cx + r*0.05, cy + r*0.55, cx + r*0.25, cy + r*0.55], width=dp(2))
    
    def draw_grandma(self, cx, cy, size):
        """画奶奶"""
        with self.canvas:
            r = size * 0.3
            # 头
            Color(0.9, 0.78, 0.65)
            Ellipse(pos=(cx - r*0.35, cy + r*0.3), size=(r*0.7, r*0.7))
            # 白发卷
            Color(0.85, 0.85, 0.85)
            for dx in [-0.25, 0, 0.25]:
                Ellipse(pos=(cx + r*dx - dp(8), cy + r*0.75), size=(dp(16), dp(16)))
            # 身体 - 紫色
            Color(0.6, 0.4, 0.7)
            Rectangle(pos=(cx - r*0.4, cy - r*0.5), size=(r*0.8, r*0.8))
            # 眼睛
            Color(0, 0, 0)
            Ellipse(pos=(cx - r*0.12, cy + r*0.55), size=(dp(4), dp(4)))
            Ellipse(pos=(cx + r*0.05, cy + r*0.55), size=(dp(4), dp(4)))
    
    def draw_brother(self, cx, cy, size):
        """画哥哥"""
        with self.canvas:
            r = size * 0.28
            # 头
            Color(0.9, 0.75, 0.6)
            Ellipse(pos=(cx - r*0.35, cy + r*0.35), size=(r*0.7, r*0.7))
            # 短发
            Color(0.2, 0.15, 0.1)
            Ellipse(pos=(cx - r*0.3, cy + r*0.8), size=(r*0.6, r*0.25))
            # 身体 - 绿色T恤
            Color(0.3, 0.7, 0.4)
            Rectangle(pos=(cx - r*0.35, cy - r*0.4), size=(r*0.7, r*0.75))
            # 眼睛
            Color(0, 0, 0)
            Ellipse(pos=(cx - r*0.12, cy + r*0.6), size=(dp(5), dp(5)))
            Ellipse(pos=(cx + r*0.05, cy + r*0.6), size=(dp(5), dp(5)))
    
    def draw_sister(self, cx, cy, size):
        """画姐姐"""
        with self.canvas:
            r = size * 0.28
            # 头
            Color(0.9, 0.75, 0.6)
            Ellipse(pos=(cx - r*0.35, cy + r*0.35), size=(r*0.7, r*0.7))
            # 马尾辫
            Color(0.25, 0.15, 0.1)
            Ellipse(pos=(cx - r*0.3, cy + r*0.85), size=(r*0.6, r*0.2))
            Ellipse(pos=(cx + r*0.25, cy + r*0.6), size=(r*0.2, r*0.4))
            # 身体 - 粉色
            Color(1, 0.6, 0.7)
            Rectangle(pos=(cx - r*0.35, cy - r*0.4), size=(r*0.7, r*0.75))
            # 眼睛
            Color(0, 0, 0)
            Ellipse(pos=(cx - r*0.12, cy + r*0.6), size=(dp(5), dp(5)))
            Ellipse(pos=(cx + r*0.05, cy + r*0.6), size=(dp(5), dp(5)))
    
    def draw_young_brother(self, cx, cy, size):
        """画弟弟"""
        with self.canvas:
            r = size * 0.25
            # 头 - 稍大显得可爱
            Color(0.9, 0.75, 0.6)
            Ellipse(pos=(cx - r*0.4, cy + r*0.3), size=(r*0.8, r*0.8))
            # 短发
            Color(0.2, 0.15, 0.1)
            Ellipse(pos=(cx - r*0.3, cy + r*0.85), size=(r*0.6, r*0.25))
            # 身体 - 蓝色
            Color(0.4, 0.6, 0.9)
            Rectangle(pos=(cx - r*0.3, cy - r*0.35), size=(r*0.6, r*0.65))
            # 大眼睛
            Color(0, 0, 0)
            Ellipse(pos=(cx - r*0.15, cy + r*0.55), size=(dp(6), dp(6)))
            Ellipse(pos=(cx + r*0.05, cy + r*0.55), size=(dp(6), dp(6)))
    
    def draw_young_sister(self, cx, cy, size):
        """画妹妹"""
        with self.canvas:
            r = size * 0.25
            # 头
            Color(0.9, 0.75, 0.6)
            Ellipse(pos=(cx - r*0.4, cy + r*0.3), size=(r*0.8, r*0.8))
            # 双马尾
            Color(0.25, 0.15, 0.1)
            Ellipse(pos=(cx - r*0.55, cy + r*0.5), size=(r*0.25, r*0.4))
            Ellipse(pos=(cx + r*0.3, cy + r*0.5), size=(r*0.25, r*0.4))
            Ellipse(pos=(cx - r*0.3, cy + r*0.9), size=(r*0.6, r*0.2))
            # 身体 - 粉色裙子
            Color(1, 0.7, 0.8)
            Rectangle(pos=(cx - r*0.3, cy - r*0.4), size=(r*0.6, r*0.7))
            # 大眼睛
            Color(0, 0, 0)
            Ellipse(pos=(cx - r*0.15, cy + r*0.55), size=(dp(6), dp(6)))
            Ellipse(pos=(cx + r*0.05, cy + r*0.55), size=(dp(6), dp(6)))

    def draw_eat(self, cx, cy, size):
        """画吃 - 碗和筷子"""
        with self.canvas:
            r = size * 0.3
            # 碗
            Color(1, 1, 1)
            Ellipse(pos=(cx - r*0.6, cy - r*0.3), size=(r*1.2, r*0.6))
            Color(0.3, 0.5, 0.8)
            Line(points=[cx - r*0.6, cy, cx - r*0.4, cy - r*0.5, cx + r*0.4, cy - r*0.5, cx + r*0.6, cy], width=dp(3))
            # 米饭
            Color(1, 1, 0.9)
            Ellipse(pos=(cx - r*0.4, cy - r*0.1), size=(r*0.8, r*0.4))
            # 筷子
            Color(0.6, 0.4, 0.2)
            Line(points=[cx + r*0.3, cy - r*0.2, cx + r*0.7, cy + r*0.8], width=dp(3))
            Line(points=[cx + r*0.5, cy - r*0.2, cx + r*0.9, cy + r*0.8], width=dp(3))
    
    def draw_drink(self, cx, cy, size):
        """画喝 - 杯子"""
        with self.canvas:
            r = size * 0.3
            # 杯子
            Color(0.8, 0.9, 1)
            Line(points=[cx - r*0.4, cy + r*0.6, cx - r*0.5, cy - r*0.6, cx + r*0.5, cy - r*0.6, cx + r*0.4, cy + r*0.6], width=dp(3), close=True)
            # 水
            Color(0.4, 0.7, 1)
            Rectangle(pos=(cx - r*0.35, cy - r*0.4), size=(r*0.7, r*0.7))
            # 吸管
            Color(1, 0.4, 0.4)
            Line(points=[cx + r*0.1, cy - r*0.3, cx + r*0.3, cy + r*0.9], width=dp(4))
    
    def draw_see(self, cx, cy, size):
        """画看 - 眼睛"""
        with self.canvas:
            r = size * 0.35
            # 眼睛轮廓
            Color(1, 1, 1)
            Ellipse(pos=(cx - r*0.8, cy - r*0.3), size=(r*1.6, r*0.6))
            # 眼球
            Color(0.4, 0.25, 0.1)
            Ellipse(pos=(cx - r*0.3, cy - r*0.25), size=(r*0.5, r*0.5))
            # 瞳孔
            Color(0, 0, 0)
            Ellipse(pos=(cx - r*0.15, cy - r*0.15), size=(r*0.25, r*0.25))
            # 高光
            Color(1, 1, 1)
            Ellipse(pos=(cx - r*0.05, cy + r*0.0), size=(r*0.1, r*0.1))
            # 眼睫毛
            Color(0.2, 0.15, 0.1)
            for i in range(5):
                x = cx - r*0.5 + i * r*0.25
                Line(points=[x, cy + r*0.3, x, cy + r*0.45], width=dp(2))
    
    def draw_hear(self, cx, cy, size):
        """画听 - 耳朵"""
        with self.canvas:
            r = size * 0.35
            # 耳朵外轮廓
            Color(0.9, 0.75, 0.6)
            Ellipse(pos=(cx - r*0.5, cy - r*0.8), size=(r*1.0, r*1.6))
            # 耳朵内部
            Color(0.95, 0.8, 0.7)
            Ellipse(pos=(cx - r*0.3, cy - r*0.5), size=(r*0.6, r*1.0))
            # 声波
            Color(0.5, 0.7, 1)
            for i in range(3):
                offset = (i + 1) * r * 0.3
                Line(points=[cx + r*0.5 + offset, cy + r*0.3, cx + r*0.5 + offset, cy - r*0.3], width=dp(2))
    
    def draw_default(self, cx, cy, size):
        """默认图形 - 问号"""
        with self.canvas:
            r = size * 0.3
            Color(0.7, 0.7, 0.7)
            # 问号
            Line(points=[cx - r*0.3, cy + r*0.5, cx, cy + r*0.8, cx + r*0.3, cy + r*0.5, cx + r*0.2, cy, cx, cy - r*0.2], width=dp(4))
            Ellipse(pos=(cx - dp(5), cy - r*0.6), size=(dp(10), dp(10)))

    # ========== 新增汉字绘图函数 ==========
    
    def draw_wind(self, cx, cy, size):
        with self.canvas:
            r = size * 0.35
            Color(0.6, 0.8, 0.9)
            for i in range(3):
                y_offset = (i - 1) * r * 0.4
                Line(points=[cx - r*0.8, cy + y_offset, cx + r*0.8, cy + y_offset], width=dp(3))

    def draw_baby(self, cx, cy, size):
        with self.canvas:
            r = size * 0.3
            Color(0.95, 0.8, 0.7)
            Ellipse(pos=(cx - r*0.4, cy + r*0.1), size=(r*0.8, r*0.8))
            Color(1, 0.8, 0.9)
            Rectangle(pos=(cx - r*0.35, cy - r*0.5), size=(r*0.7, r*0.6))

    def draw_open(self, cx, cy, size):
        with self.canvas:
            r = size * 0.35
            Color(0.6, 0.4, 0.2)
            Line(rectangle=(cx - r*0.6, cy - r*0.8, r*1.2, r*1.6), width=dp(3))
            Color(0.8, 0.6, 0.4)
            Rectangle(pos=(cx - r*0.5, cy - r*0.7), size=(r*0.8, r*1.4))

    def draw_close(self, cx, cy, size):
        with self.canvas:
            r = size * 0.35
            Color(0.5, 0.35, 0.2)
            Rectangle(pos=(cx - r*0.45, cy - r*0.75), size=(r*0.9, r*1.5))

    def draw_inside(self, cx, cy, size):
        with self.canvas:
            r = size * 0.35
            Color(0.8, 0.6, 0.4)
            Line(rectangle=(cx - r*0.6, cy - r*0.5, r*1.2, r*1.0), width=dp(3))
            Color(1, 0.5, 0.5)
            Ellipse(pos=(cx - r*0.15, cy - r*0.15), size=(r*0.3, r*0.3))

    def draw_he(self, cx, cy, size):
        with self.canvas:
            r = size * 0.28
            Color(0.9, 0.75, 0.6)
            Ellipse(pos=(cx - r*0.3, cy + r*0.3), size=(r*0.6, r*0.6))
            Color(0.3, 0.5, 0.8)
            Rectangle(pos=(cx - r*0.3, cy - r*0.4), size=(r*0.6, r*0.7))

    def draw_worker(self, cx, cy, size):
        with self.canvas:
            r = size * 0.3
            Color(1, 0.8, 0)
            Ellipse(pos=(cx - r*0.35, cy + r*0.5), size=(r*0.7, r*0.4))
            Color(0.9, 0.75, 0.6)
            Ellipse(pos=(cx - r*0.3, cy + r*0.2), size=(r*0.6, r*0.5))
            Color(0.2, 0.4, 0.8)
            Rectangle(pos=(cx - r*0.35, cy - r*0.5), size=(r*0.7, r*0.7))

    def draw_child(self, cx, cy, size):
        with self.canvas:
            r = size * 0.25
            Color(0.9, 0.75, 0.6)
            Ellipse(pos=(cx - r*0.35, cy + r*0.25), size=(r*0.7, r*0.7))
            Color(0.4, 0.7, 0.9)
            Rectangle(pos=(cx - r*0.3, cy - r*0.4), size=(r*0.6, r*0.65))

    def draw_old(self, cx, cy, size):
        with self.canvas:
            r = size * 0.3
            Color(0.9, 0.78, 0.65)
            Ellipse(pos=(cx - r*0.3, cy + r*0.25), size=(r*0.6, r*0.6))
            Color(0.9, 0.9, 0.9)
            Ellipse(pos=(cx - r*0.25, cy + r*0.65), size=(r*0.5, r*0.2))
            Color(0.5, 0.4, 0.3)
            Rectangle(pos=(cx - r*0.3, cy - r*0.5), size=(r*0.6, r*0.75))

    def draw_good(self, cx, cy, size):
        with self.canvas:
            r = size * 0.35
            Color(0.9, 0.75, 0.6)
            Rectangle(pos=(cx - r*0.15, cy - r*0.6), size=(r*0.3, r*0.8))
            Ellipse(pos=(cx - r*0.2, cy + r*0.1), size=(r*0.4, r*0.5))

    def draw_rice(self, cx, cy, size):
        with self.canvas:
            r = size * 0.35
            Color(0.3, 0.5, 0.8)
            Line(points=[cx - r*0.5, cy, cx - r*0.35, cy - r*0.5, cx + r*0.35, cy - r*0.5, cx + r*0.5, cy], width=dp(3))
            Color(1, 1, 0.95)
            Ellipse(pos=(cx - r*0.35, cy - r*0.1), size=(r*0.7, r*0.35))

    def draw_play(self, cx, cy, size):
        with self.canvas:
            r = size * 0.35
            Color(1, 0.4, 0.4)
            Ellipse(pos=(cx - r*0.5, cy - r*0.5), size=(r*1.0, r*1.0))
            Color(1, 1, 0.4)
            Line(points=[cx - r*0.35, cy, cx + r*0.35, cy], width=dp(3))

    def draw_uncle(self, cx, cy, size):
        with self.canvas:
            r = size * 0.28
            Color(0.9, 0.75, 0.6)
            Ellipse(pos=(cx - r*0.3, cy + r*0.3), size=(r*0.6, r*0.6))
            Color(0.3, 0.3, 0.3)
            Rectangle(pos=(cx - r*0.35, cy - r*0.45), size=(r*0.7, r*0.75))

    def draw_self(self, cx, cy, size):
        with self.canvas:
            r = size * 0.3
            Color(0.9, 0.75, 0.6)
            Ellipse(pos=(cx - r*0.3, cy + r*0.2), size=(r*0.6, r*0.6))
            Color(0.4, 0.6, 0.9)
            Rectangle(pos=(cx - r*0.3, cy - r*0.5), size=(r*0.6, r*0.7))

    def draw_aunt(self, cx, cy, size):
        with self.canvas:
            r = size * 0.28
            Color(0.9, 0.75, 0.6)
            Ellipse(pos=(cx - r*0.3, cy + r*0.3), size=(r*0.6, r*0.6))
            Color(0.8, 0.4, 0.6)
            Rectangle(pos=(cx - r*0.3, cy - r*0.45), size=(r*0.6, r*0.75))

    def draw_girl(self, cx, cy, size):
        with self.canvas:
            r = size * 0.28
            Color(0.9, 0.75, 0.6)
            Ellipse(pos=(cx - r*0.3, cy + r*0.3), size=(r*0.6, r*0.6))
            Color(1, 0.5, 0.6)
            Rectangle(pos=(cx - r*0.35, cy - r*0.5), size=(r*0.7, r*0.8))

    def draw_electric(self, cx, cy, size):
        with self.canvas:
            r = size * 0.4
            Color(1, 0.9, 0.2)
            Line(points=[cx, cy + r*0.8, cx + r*0.2, cy, cx - r*0.1, cy, cx + r*0.1, cy - r*0.8], width=dp(5))

    def draw_wood(self, cx, cy, size):
        with self.canvas:
            r = size * 0.35
            Color(0.6, 0.4, 0.2)
            Rectangle(pos=(cx - r*0.15, cy - r*0.8), size=(r*0.3, r*1.2))
            Line(points=[cx - r*0.5, cy + r*0.2, cx, cy + r*0.4, cx + r*0.5, cy + r*0.2], width=dp(3))

    def draw_compare(self, cx, cy, size):
        with self.canvas:
            r = size * 0.25
            Color(0.4, 0.6, 0.9)
            Ellipse(pos=(cx - r*1.0, cy + r*0.3), size=(r*0.5, r*0.5))
            Rectangle(pos=(cx - r*0.95, cy - r*0.4), size=(r*0.4, r*0.7))
            Color(0.9, 0.5, 0.5)
            Ellipse(pos=(cx + r*0.5, cy + r*0.5), size=(r*0.5, r*0.5))
            Rectangle(pos=(cx + r*0.55, cy - r*0.2), size=(r*0.4, r*0.7))

    def draw_picture(self, cx, cy, size):
        with self.canvas:
            r = size * 0.4
            Color(0.9, 0.85, 0.7)
            Rectangle(pos=(cx - r*0.6, cy - r*0.5), size=(r*1.2, r*1.0))
            Color(0.6, 0.4, 0.2)
            Line(rectangle=(cx - r*0.6, cy - r*0.5, r*1.2, r*1.0), width=dp(3))

    def draw_one(self, cx, cy, size):
        with self.canvas:
            r = size * 0.4
            Color(0.9, 0.3, 0.3)
            Line(points=[cx - r*0.6, cy, cx + r*0.6, cy], width=dp(8))

    def draw_three(self, cx, cy, size):
        with self.canvas:
            r = size * 0.4
            Color(0.3, 0.7, 0.4)
            Line(points=[cx - r*0.5, cy + r*0.4, cx + r*0.5, cy + r*0.4], width=dp(6))
            Line(points=[cx - r*0.4, cy, cx + r*0.4, cy], width=dp(6))
            Line(points=[cx - r*0.5, cy - r*0.4, cx + r*0.5, cy - r*0.4], width=dp(6))

    def draw_four(self, cx, cy, size):
        with self.canvas:
            r = size * 0.35
            Color(0.3, 0.5, 0.8)
            Line(rectangle=(cx - r*0.5, cy - r*0.5, r*1.0, r*1.0), width=dp(4))
            Line(points=[cx - r*0.5, cy, cx + r*0.5, cy], width=dp(3))
            Line(points=[cx, cy - r*0.5, cx, cy + r*0.5], width=dp(3))

    def draw_five(self, cx, cy, size):
        with self.canvas:
            r = size * 0.4
            Color(0.8, 0.5, 0.2)
            Line(points=[cx - r*0.5, cy + r*0.5, cx + r*0.5, cy + r*0.5], width=dp(5))
            Line(points=[cx - r*0.5, cy - r*0.5, cx + r*0.5, cy - r*0.5], width=dp(5))

    def draw_sheep(self, cx, cy, size):
        with self.canvas:
            r = size * 0.35
            Color(1, 1, 1)
            Ellipse(pos=(cx - r*0.5, cy - r*0.3), size=(r*1.0, r*0.7))
            Ellipse(pos=(cx - r*0.3, cy + r*0.2), size=(r*0.5, r*0.5))
            Color(0, 0, 0)
            Ellipse(pos=(cx - r*0.15, cy + r*0.4), size=(dp(5), dp(5)))
            Ellipse(pos=(cx + r*0.02, cy + r*0.4), size=(dp(5), dp(5)))

    def draw_white(self, cx, cy, size):
        with self.canvas:
            r = size * 0.4
            Color(1, 1, 1)
            Ellipse(pos=(cx - r*0.5, cy - r*0.5), size=(r*1.0, r*1.0))
            Color(0.8, 0.8, 0.8)
            Line(circle=(cx, cy, r*0.5), width=dp(2))

    def draw_cow(self, cx, cy, size):
        with self.canvas:
            r = size * 0.35
            Color(0.9, 0.85, 0.8)
            Ellipse(pos=(cx - r*0.6, cy - r*0.4), size=(r*1.2, r*0.8))
            Ellipse(pos=(cx - r*0.35, cy + r*0.2), size=(r*0.6, r*0.5))
            Color(0, 0, 0)
            Ellipse(pos=(cx - r*0.2, cy + r*0.35), size=(dp(6), dp(6)))
            Ellipse(pos=(cx + r*0.05, cy + r*0.35), size=(dp(6), dp(6)))

    def draw_mouse(self, cx, cy, size):
        with self.canvas:
            r = size * 0.3
            Color(0.7, 0.7, 0.7)
            Ellipse(pos=(cx - r*0.5, cy - r*0.3), size=(r*1.0, r*0.6))
            Ellipse(pos=(cx + r*0.3, cy), size=(r*0.4, r*0.4))
            Color(1, 0.8, 0.8)
            Ellipse(pos=(cx - r*0.5, cy + r*0.2), size=(r*0.35, r*0.4))
            Ellipse(pos=(cx + r*0.15, cy + r*0.2), size=(r*0.35, r*0.4))

    def draw_heart(self, cx, cy, size):
        with self.canvas:
            r = size * 0.35
            Color(1, 0.3, 0.4)
            Ellipse(pos=(cx - r*0.5, cy), size=(r*0.5, r*0.5))
            Ellipse(pos=(cx, cy), size=(r*0.5, r*0.5))

    def draw_ok(self, cx, cy, size):
        with self.canvas:
            r = size * 0.4
            Color(0.3, 0.8, 0.4)
            Ellipse(pos=(cx - r*0.5, cy - r*0.5), size=(r*1.0, r*1.0))
            Color(1, 1, 1)
            Line(points=[cx - r*0.25, cy, cx - r*0.05, cy - r*0.25, cx + r*0.3, cy + r*0.25], width=dp(5))

    def draw_speak(self, cx, cy, size):
        with self.canvas:
            r = size * 0.35
            Color(0.9, 0.75, 0.6)
            Ellipse(pos=(cx - r*0.6, cy - r*0.1), size=(r*0.6, r*0.6))
            Color(0.8, 0.9, 1)
            Ellipse(pos=(cx + r*0.1, cy + r*0.1), size=(r*0.7, r*0.5))

    def draw_two(self, cx, cy, size):
        with self.canvas:
            r = size * 0.3
            Color(0.9, 0.5, 0.3)
            Ellipse(pos=(cx - r*0.8, cy - r*0.3), size=(r*0.6, r*0.6))
            Ellipse(pos=(cx + r*0.2, cy - r*0.3), size=(r*0.6, r*0.6))

    def draw_boy(self, cx, cy, size):
        with self.canvas:
            r = size * 0.28
            Color(0.9, 0.75, 0.6)
            Ellipse(pos=(cx - r*0.35, cy + r*0.3), size=(r*0.7, r*0.7))
            Color(0.3, 0.5, 0.8)
            Rectangle(pos=(cx - r*0.35, cy - r*0.45), size=(r*0.7, r*0.75))

    def draw_you(self, cx, cy, size):
        with self.canvas:
            r = size * 0.3
            Color(0.9, 0.75, 0.6)
            Rectangle(pos=(cx - r*0.6, cy - r*0.1), size=(r*0.8, r*0.25))
            Ellipse(pos=(cx + r*0.2, cy - r*0.15), size=(r*0.35, r*0.35))

    def draw_no(self, cx, cy, size):
        with self.canvas:
            r = size * 0.4
            Color(1, 0.3, 0.3)
            Line(circle=(cx, cy, r*0.5), width=dp(4))
            Line(points=[cx - r*0.35, cy + r*0.35, cx + r*0.35, cy - r*0.35], width=dp(4))

    def draw_kid(self, cx, cy, size):
        with self.canvas:
            r = size * 0.25
            Color(0.95, 0.8, 0.7)
            Ellipse(pos=(cx - r*0.4, cy + r*0.2), size=(r*0.8, r*0.8))
            Color(1, 0.7, 0.8)
            Rectangle(pos=(cx - r*0.35, cy - r*0.45), size=(r*0.7, r*0.65))

    def draw_at(self, cx, cy, size):
        with self.canvas:
            r = size * 0.35
            Color(0.8, 0.6, 0.4)
            Line(rectangle=(cx - r*0.5, cy - r*0.5, r*1.0, r*0.8), width=dp(3))
            Color(0.9, 0.4, 0.3)
            Line(points=[cx - r*0.6, cy + r*0.3, cx, cy + r*0.8, cx + r*0.6, cy + r*0.3], width=dp(3))

    def draw_head(self, cx, cy, size):
        with self.canvas:
            r = size * 0.4
            Color(0.9, 0.75, 0.6)
            Ellipse(pos=(cx - r*0.45, cy - r*0.1), size=(r*0.9, r*0.9))
            Color(0.2, 0.15, 0.1)
            Ellipse(pos=(cx - r*0.4, cy + r*0.5), size=(r*0.8, r*0.35))

    def draw_me(self, cx, cy, size):
        with self.canvas:
            r = size * 0.3
            Color(0.9, 0.75, 0.6)
            Ellipse(pos=(cx - r*0.3, cy + r*0.2), size=(r*0.6, r*0.6))
            Color(0.4, 0.6, 0.9)
            Rectangle(pos=(cx - r*0.3, cy - r*0.5), size=(r*0.6, r*0.7))

    def draw_house(self, cx, cy, size):
        with self.canvas:
            r = size * 0.4
            Color(0.9, 0.85, 0.7)
            Rectangle(pos=(cx - r*0.5, cy - r*0.5), size=(r*1.0, r*0.8))
            Color(0.8, 0.4, 0.3)
            Line(points=[cx - r*0.6, cy + r*0.3, cx, cy + r*0.9, cx + r*0.6, cy + r*0.3], width=dp(4), close=True)
            Color(0.5, 0.35, 0.2)
            Rectangle(pos=(cx - r*0.15, cy - r*0.5), size=(r*0.3, r*0.5))
