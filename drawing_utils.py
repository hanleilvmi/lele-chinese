# -*- coding: utf-8 -*-
"""
彩色图形绘制工具
用于在Canvas上绘制各种彩色卡通图形
"""

import math
import random


def draw_circle(canvas, x, y, radius, color="#FF6B6B", outline_color=None, width=3):
    """绘制彩色圆形"""
    if outline_color is None:
        outline_color = darken_color(color)
    canvas.create_oval(x-radius, y-radius, x+radius, y+radius, 
                       fill=color, outline=outline_color, width=width)
    # 高光效果
    highlight_r = radius * 0.3
    canvas.create_oval(x-radius*0.4-highlight_r, y-radius*0.4-highlight_r,
                       x-radius*0.4+highlight_r, y-radius*0.4+highlight_r,
                       fill="white", outline="")


def draw_triangle(canvas, x, y, size, color="#4ECDC4", outline_color=None, width=3):
    """绘制彩色三角形"""
    if outline_color is None:
        outline_color = darken_color(color)
    h = size * math.sqrt(3) / 2
    points = [
        x, y - h * 0.6,           # 顶点
        x - size/2, y + h * 0.4,  # 左下
        x + size/2, y + h * 0.4,  # 右下
    ]
    canvas.create_polygon(points, fill=color, outline=outline_color, width=width)


def draw_square(canvas, x, y, size, color="#45B7D1", outline_color=None, width=3):
    """绘制彩色正方形"""
    if outline_color is None:
        outline_color = darken_color(color)
    half = size / 2
    canvas.create_rectangle(x-half, y-half, x+half, y+half, 
                           fill=color, outline=outline_color, width=width)


def draw_rectangle(canvas, x, y, width_size, height_size, color="#96CEB4", outline_color=None, line_width=3):
    """绘制彩色长方形"""
    if outline_color is None:
        outline_color = darken_color(color)
    canvas.create_rectangle(x-width_size/2, y-height_size/2, 
                           x+width_size/2, y+height_size/2,
                           fill=color, outline=outline_color, width=line_width)


def draw_star(canvas, x, y, outer_r, inner_r=None, color="#FFD93D", outline_color=None, width=2, points=5):
    """绘制彩色星形"""
    if inner_r is None:
        inner_r = outer_r * 0.4
    if outline_color is None:
        outline_color = darken_color(color)
    
    coords = []
    for i in range(points * 2):
        angle = math.pi / 2 + i * math.pi / points
        r = outer_r if i % 2 == 0 else inner_r
        coords.append(x + r * math.cos(angle))
        coords.append(y - r * math.sin(angle))
    
    canvas.create_polygon(coords, fill=color, outline=outline_color, width=width)


def draw_heart(canvas, x, y, size, color="#FF69B4", outline_color=None, width=2):
    """绘制彩色心形"""
    if outline_color is None:
        outline_color = darken_color(color)
    
    # 使用多边形近似心形
    coords = []
    for i in range(100):
        t = i * 2 * math.pi / 100
        hx = 16 * math.sin(t) ** 3
        hy = 13 * math.cos(t) - 5 * math.cos(2*t) - 2 * math.cos(3*t) - math.cos(4*t)
        coords.append(x + hx * size / 20)
        coords.append(y - hy * size / 20)
    
    canvas.create_polygon(coords, fill=color, outline=outline_color, width=width, smooth=True)


def draw_diamond(canvas, x, y, size, color="#9C27B0", outline_color=None, width=3):
    """绘制彩色菱形"""
    if outline_color is None:
        outline_color = darken_color(color)
    
    points = [
        x, y - size * 0.6,  # 上
        x + size * 0.4, y,  # 右
        x, y + size * 0.6,  # 下
        x - size * 0.4, y,  # 左
    ]
    canvas.create_polygon(points, fill=color, outline=outline_color, width=width)


def draw_pentagon(canvas, x, y, radius, color="#FF9800", outline_color=None, width=3):
    """绘制彩色五边形"""
    if outline_color is None:
        outline_color = darken_color(color)
    
    coords = []
    for i in range(5):
        angle = math.pi / 2 + i * 2 * math.pi / 5
        coords.append(x + radius * math.cos(angle))
        coords.append(y - radius * math.sin(angle))
    
    canvas.create_polygon(coords, fill=color, outline=outline_color, width=width)


def draw_hexagon(canvas, x, y, radius, color="#00BCD4", outline_color=None, width=3):
    """绘制彩色六边形"""
    if outline_color is None:
        outline_color = darken_color(color)
    
    coords = []
    for i in range(6):
        angle = i * math.pi / 3
        coords.append(x + radius * math.cos(angle))
        coords.append(y - radius * math.sin(angle))
    
    canvas.create_polygon(coords, fill=color, outline=outline_color, width=width)


def draw_arrow(canvas, x, y, size, direction="right", color="#4CAF50", outline_color=None, width=2):
    """绘制彩色箭头"""
    if outline_color is None:
        outline_color = darken_color(color)
    
    if direction == "right":
        points = [
            x - size*0.5, y - size*0.2,
            x + size*0.2, y - size*0.2,
            x + size*0.2, y - size*0.4,
            x + size*0.5, y,
            x + size*0.2, y + size*0.4,
            x + size*0.2, y + size*0.2,
            x - size*0.5, y + size*0.2,
        ]
    elif direction == "left":
        points = [
            x + size*0.5, y - size*0.2,
            x - size*0.2, y - size*0.2,
            x - size*0.2, y - size*0.4,
            x - size*0.5, y,
            x - size*0.2, y + size*0.4,
            x - size*0.2, y + size*0.2,
            x + size*0.5, y + size*0.2,
        ]
    elif direction == "up":
        points = [
            x - size*0.2, y + size*0.5,
            x - size*0.2, y - size*0.2,
            x - size*0.4, y - size*0.2,
            x, y - size*0.5,
            x + size*0.4, y - size*0.2,
            x + size*0.2, y - size*0.2,
            x + size*0.2, y + size*0.5,
        ]
    else:  # down
        points = [
            x - size*0.2, y - size*0.5,
            x - size*0.2, y + size*0.2,
            x - size*0.4, y + size*0.2,
            x, y + size*0.5,
            x + size*0.4, y + size*0.2,
            x + size*0.2, y + size*0.2,
            x + size*0.2, y - size*0.5,
        ]
    
    canvas.create_polygon(points, fill=color, outline=outline_color, width=width)


def draw_cloud(canvas, x, y, scale=1.0):
    """绘制彩色云朵"""
    s = scale
    for dx, dy, r in [(-30*s, 0, 25*s), (0, -15*s, 30*s), (30*s, 0, 25*s), 
                       (0, 10*s, 20*s), (-20*s, 5*s, 18*s), (20*s, 5*s, 18*s)]:
        canvas.create_oval(x+dx-r, y+dy-r, x+dx+r, y+dy+r, fill="white", outline="#E0E0E0")


def draw_sun(canvas, x, y, radius, color="#FFD700"):
    """绘制彩色太阳"""
    # 光芒
    for i in range(12):
        angle = i * math.pi / 6
        x1 = x + radius * 0.8 * math.cos(angle)
        y1 = y + radius * 0.8 * math.sin(angle)
        x2 = x + radius * 1.4 * math.cos(angle)
        y2 = y + radius * 1.4 * math.sin(angle)
        canvas.create_line(x1, y1, x2, y2, fill="#FFA500", width=3)
    
    # 太阳本体
    canvas.create_oval(x-radius, y-radius, x+radius, y+radius, 
                       fill=color, outline="#FFA500", width=3)
    
    # 笑脸
    canvas.create_arc(x-radius*0.5, y-radius*0.2, x+radius*0.5, y+radius*0.5,
                      start=200, extent=140, style="arc", outline="#FF8C00", width=2)
    # 眼睛
    canvas.create_oval(x-radius*0.35, y-radius*0.3, x-radius*0.15, y-radius*0.1, fill="#FF8C00", outline="")
    canvas.create_oval(x+radius*0.15, y-radius*0.3, x+radius*0.35, y-radius*0.1, fill="#FF8C00", outline="")


def draw_tree(canvas, x, y, scale=1.0):
    """绘制彩色树"""
    s = scale
    # 树干
    canvas.create_rectangle(x-10*s, y, x+10*s, y+50*s, fill="#8B4513", outline="#654321", width=2)
    # 树冠
    canvas.create_oval(x-40*s, y-60*s, x+40*s, y+10*s, fill="#228B22", outline="#006400", width=2)
    canvas.create_oval(x-30*s, y-80*s, x+30*s, y-20*s, fill="#32CD32", outline="#228B22", width=2)


def draw_flower(canvas, x, y, size, petal_color="#FF69B4", center_color="#FFD700"):
    """绘制彩色花朵"""
    # 花瓣
    for i in range(6):
        angle = i * math.pi / 3
        px = x + size * 0.5 * math.cos(angle)
        py = y + size * 0.5 * math.sin(angle)
        canvas.create_oval(px-size*0.3, py-size*0.3, px+size*0.3, py+size*0.3,
                          fill=petal_color, outline=darken_color(petal_color), width=1)
    # 花心
    canvas.create_oval(x-size*0.25, y-size*0.25, x+size*0.25, y+size*0.25,
                      fill=center_color, outline="#FFA500", width=2)


def draw_house(canvas, x, y, scale=1.0):
    """绘制彩色房子"""
    s = scale
    # 房身
    canvas.create_rectangle(x-40*s, y-20*s, x+40*s, y+40*s, fill="#FFE4B5", outline="#DEB887", width=2)
    # 屋顶
    canvas.create_polygon(x-50*s, y-20*s, x, y-60*s, x+50*s, y-20*s,
                         fill="#DC143C", outline="#8B0000", width=2)
    # 门
    canvas.create_rectangle(x-12*s, y+5*s, x+12*s, y+40*s, fill="#8B4513", outline="#654321", width=2)
    # 窗户
    canvas.create_rectangle(x-35*s, y-10*s, x-15*s, y+10*s, fill="#87CEEB", outline="#4682B4", width=2)
    canvas.create_rectangle(x+15*s, y-10*s, x+35*s, y+10*s, fill="#87CEEB", outline="#4682B4", width=2)


def draw_apple(canvas, x, y, size, color="#FF0000"):
    """绘制彩色苹果"""
    # 苹果身体
    canvas.create_oval(x-size*0.45, y-size*0.4, x+size*0.45, y+size*0.5,
                      fill=color, outline=darken_color(color), width=2)
    # 叶子
    canvas.create_oval(x+size*0.1, y-size*0.55, x+size*0.35, y-size*0.35,
                      fill="#228B22", outline="#006400", width=1)
    # 茎
    canvas.create_line(x, y-size*0.4, x+size*0.05, y-size*0.55, fill="#8B4513", width=3)
    # 高光
    canvas.create_oval(x-size*0.25, y-size*0.25, x-size*0.1, y-size*0.1,
                      fill="white", outline="")


def draw_banana(canvas, x, y, size):
    """绘制彩色香蕉"""
    # 香蕉弧形
    canvas.create_arc(x-size*0.5, y-size*0.3, x+size*0.5, y+size*0.5,
                     start=30, extent=120, style="chord",
                     fill="#FFD700", outline="#DAA520", width=2)


def draw_watermelon(canvas, x, y, size):
    """绘制彩色西瓜"""
    # 外皮
    canvas.create_arc(x-size*0.5, y-size*0.3, x+size*0.5, y+size*0.5,
                     start=0, extent=180, style="chord",
                     fill="#228B22", outline="#006400", width=2)
    # 果肉
    canvas.create_arc(x-size*0.4, y-size*0.2, x+size*0.4, y+size*0.4,
                     start=0, extent=180, style="chord",
                     fill="#FF6B6B", outline="#DC143C", width=1)
    # 籽
    for dx in [-size*0.2, 0, size*0.2]:
        canvas.create_oval(x+dx-3, y+size*0.05, x+dx+3, y+size*0.15, fill="#333", outline="")


def draw_rainbow(canvas, x, y, width, height):
    """绘制彩虹"""
    colors = ["#FF0000", "#FF7F00", "#FFFF00", "#00FF00", "#0000FF", "#4B0082", "#9400D3"]
    band_height = height / len(colors)
    
    for i, color in enumerate(colors):
        r_outer = width / 2 - i * band_height
        r_inner = r_outer - band_height
        if r_inner < 0:
            r_inner = 0
        canvas.create_arc(x - r_outer, y - r_outer, x + r_outer, y + r_outer,
                         start=0, extent=180, style="arc", outline=color, width=band_height)


def darken_color(hex_color, factor=0.7):
    """将颜色变暗"""
    hex_color = hex_color.lstrip('#')
    r = int(hex_color[0:2], 16)
    g = int(hex_color[2:4], 16)
    b = int(hex_color[4:6], 16)
    r = int(r * factor)
    g = int(g * factor)
    b = int(b * factor)
    return f"#{r:02x}{g:02x}{b:02x}"


def lighten_color(hex_color, factor=1.3):
    """将颜色变亮"""
    hex_color = hex_color.lstrip('#')
    r = min(255, int(int(hex_color[0:2], 16) * factor))
    g = min(255, int(int(hex_color[2:4], 16) * factor))
    b = min(255, int(int(hex_color[4:6], 16) * factor))
    return f"#{r:02x}{g:02x}{b:02x}"


# 形状绘制函数映射
SHAPE_DRAWERS = {
    "圆形": draw_circle,
    "三角形": draw_triangle,
    "正方形": draw_square,
    "长方形": draw_rectangle,
    "星形": draw_star,
    "心形": draw_heart,
    "菱形": draw_diamond,
    "五边形": draw_pentagon,
    "六边形": draw_hexagon,
}

# 形状颜色
SHAPE_COLORS = {
    "圆形": "#FF6B6B",
    "三角形": "#4ECDC4", 
    "正方形": "#45B7D1",
    "长方形": "#96CEB4",
    "星形": "#FFD93D",
    "心形": "#FF69B4",
    "菱形": "#9C27B0",
    "五边形": "#FF9800",
    "六边形": "#00BCD4",
}
