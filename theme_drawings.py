# -*- coding: utf-8 -*-
"""
主题绘图模块 v3.0 - 超精细卡通角色
增加毛发质感、阴影高光、更多细节
"""

import math


class ThemeDrawings:
    """主题绘图类 - 超精细版"""
    
    @staticmethod
    def draw_puppy_chase(canvas, x, y, scale=1.0):
        """阿奇 - 德国牧羊犬警犬 - 超精细版本
        特点：竖立的大耳朵、棕褐色毛发、蓝色警察装备
        """
        s = scale
        
        # ========== 尾巴（先画，在身体后面）==========
        canvas.create_polygon(
            x+20*s, y+45*s, x+35*s, y+25*s, x+42*s, y+20*s,
            x+40*s, y+28*s, x+28*s, y+48*s,
            fill="#6B5344", outline="#5A4636", width=1, smooth=True
        )
        canvas.create_line(x+28*s, y+38*s, x+36*s, y+26*s, fill="#7D6352", width=2)
        
        # ========== 后腿 ==========
        canvas.create_oval(x-30*s, y+42*s, x-12*s, y+72*s, fill="#6B5344", outline="")
        canvas.create_oval(x-32*s, y+62*s, x-14*s, y+75*s, fill="#4A3728", outline="")
        canvas.create_oval(x+12*s, y+42*s, x+30*s, y+72*s, fill="#6B5344", outline="")
        canvas.create_oval(x+14*s, y+62*s, x+32*s, y+75*s, fill="#4A3728", outline="")
        
        # ========== 身体（多层渐变）==========
        canvas.create_oval(x-32*s, y+5*s, x+32*s, y+58*s, fill="#6B5344", outline="")
        canvas.create_oval(x-29*s, y+8*s, x+29*s, y+55*s, fill="#7D6352", outline="")
        canvas.create_oval(x-26*s, y+12*s, x+26*s, y+52*s, fill="#8B7355", outline="")
        
        # 胸前浅色毛发
        canvas.create_oval(x-15*s, y+12*s, x+15*s, y+42*s, fill="#C4A574", outline="")
        canvas.create_oval(x-12*s, y+15*s, x+12*s, y+38*s, fill="#D4B896", outline="")
        for i in range(-8, 9, 4):
            canvas.create_line(x+i*s, y+18*s, x+i*s, y+35*s, fill="#BFA068", width=1)
        
        # ========== 前腿 ==========
        canvas.create_polygon(x-24*s, y+38*s, x-14*s, y+38*s, x-12*s, y+68*s, x-26*s, y+68*s,
                             fill="#7D6352", outline="#5A4636", width=1)
        canvas.create_line(x-20*s, y+40*s, x-18*s, y+60*s, fill="#8B7355", width=2)
        canvas.create_oval(x-28*s, y+63*s, x-10*s, y+76*s, fill="#4A3728", outline="#3A2A1E", width=1)
        
        canvas.create_polygon(x+14*s, y+38*s, x+24*s, y+38*s, x+26*s, y+68*s, x+12*s, y+68*s,
                             fill="#7D6352", outline="#5A4636", width=1)
        canvas.create_line(x+18*s, y+40*s, x+20*s, y+60*s, fill="#8B7355", width=2)
        canvas.create_oval(x+10*s, y+63*s, x+28*s, y+76*s, fill="#4A3728", outline="#3A2A1E", width=1)
        
        # ========== 项圈 ==========
        canvas.create_rectangle(x-22*s, y+2*s, x+22*s, y+14*s, fill="#1565C0", outline="#0D47A1", width=2)
        canvas.create_line(x-20*s, y+5*s, x+20*s, y+5*s, fill="#1976D2", width=2)
        canvas.create_oval(x-4*s, y+3*s, x+4*s, y+13*s, fill="#FFD700", outline="#FFA000", width=2)
        ThemeDrawings._draw_paw_badge(canvas, x, y+8*s, 5*s)
        
        # ========== 头部（多层渐变）==========
        canvas.create_oval(x-30*s, y-40*s, x+30*s, y+20*s, fill="#6B5344", outline="")
        canvas.create_oval(x-28*s, y-38*s, x+28*s, y+18*s, fill="#C4A574", outline="")
        canvas.create_oval(x-26*s, y-36*s, x+26*s, y+16*s, fill="#D4B896", outline="")
        
        # 脸部深色"面具"
        canvas.create_polygon(
            x, y-32*s, x-22*s, y-15*s, x-18*s, y+5*s, x-8*s, y+12*s,
            x, y+15*s, x+8*s, y+12*s, x+18*s, y+5*s, x+22*s, y-15*s,
            fill="#7D6352", outline="", smooth=True
        )
        canvas.create_polygon(
            x, y-28*s, x-18*s, y-12*s, x-14*s, y+2*s,
            x, y+10*s, x+14*s, y+2*s, x+18*s, y-12*s,
            fill="#8B7355", outline="", smooth=True
        )
        
        # ========== 耳朵（大竖耳）==========
        canvas.create_polygon(x-18*s, y-25*s, x-28*s, y-70*s, x-22*s, y-72*s, x-8*s, y-30*s,
                             fill="#6B5344", outline="#5A4636", width=2, smooth=True)
        canvas.create_polygon(x-16*s, y-28*s, x-24*s, y-62*s, x-20*s, y-64*s, x-10*s, y-30*s,
                             fill="#7D6352", outline="", smooth=True)
        canvas.create_polygon(x-14*s, y-30*s, x-20*s, y-52*s, x-17*s, y-54*s, x-11*s, y-32*s,
                             fill="#FFB6C1", outline="", smooth=True)
        
        canvas.create_polygon(x+18*s, y-25*s, x+28*s, y-70*s, x+22*s, y-72*s, x+8*s, y-30*s,
                             fill="#6B5344", outline="#5A4636", width=2, smooth=True)
        canvas.create_polygon(x+16*s, y-28*s, x+24*s, y-62*s, x+20*s, y-64*s, x+10*s, y-30*s,
                             fill="#7D6352", outline="", smooth=True)
        canvas.create_polygon(x+14*s, y-30*s, x+20*s, y-52*s, x+17*s, y-54*s, x+11*s, y-32*s,
                             fill="#FFB6C1", outline="", smooth=True)
        
        # ========== 眼睛（大而有神）==========
        canvas.create_oval(x-17*s, y-22*s, x-3*s, y-5*s, fill="#5A4636", outline="")
        canvas.create_oval(x+3*s, y-22*s, x+17*s, y-5*s, fill="#5A4636", outline="")
        canvas.create_oval(x-16*s, y-21*s, x-4*s, y-6*s, fill="white", outline="#333", width=1)
        canvas.create_oval(x+4*s, y-21*s, x+16*s, y-6*s, fill="white", outline="#333", width=1)
        canvas.create_oval(x-14*s, y-19*s, x-6*s, y-8*s, fill="#3E2723", outline="")
        canvas.create_oval(x+6*s, y-19*s, x+14*s, y-8*s, fill="#3E2723", outline="")
        canvas.create_oval(x-12*s, y-17*s, x-8*s, y-11*s, fill="#1a1a1a", outline="")
        canvas.create_oval(x+8*s, y-17*s, x+12*s, y-11*s, fill="#1a1a1a", outline="")
        canvas.create_oval(x-13*s, y-18*s, x-10*s, y-15*s, fill="white", outline="")
        canvas.create_oval(x+9*s, y-18*s, x+12*s, y-15*s, fill="white", outline="")
        canvas.create_oval(x-9*s, y-12*s, x-7*s, y-10*s, fill="#EEEEEE", outline="")
        canvas.create_oval(x+7*s, y-12*s, x+9*s, y-10*s, fill="#EEEEEE", outline="")
        
        # 眉毛
        canvas.create_arc(x-18*s, y-28*s, x-4*s, y-18*s, start=20, extent=140, style="arc", outline="#4A3728", width=int(2*s)+1)
        canvas.create_arc(x+4*s, y-28*s, x+18*s, y-18*s, start=20, extent=140, style="arc", outline="#4A3728", width=int(2*s)+1)
        
        # ========== 鼻子 ==========
        canvas.create_polygon(x-6*s, y-8*s, x+6*s, y-8*s, x+8*s, y+5*s, x-8*s, y+5*s,
                             fill="#8B7355", outline="", smooth=True)
        canvas.create_oval(x-10*s, y+0*s, x+10*s, y+15*s, fill="#1a1a1a", outline="#111", width=1)
        canvas.create_oval(x-6*s, y+2*s, x-1*s, y+7*s, fill="#444", outline="")
        canvas.create_oval(x-4*s, y+3*s, x-2*s, y+5*s, fill="#666", outline="")
        canvas.create_oval(x-6*s, y+8*s, x-2*s, y+12*s, fill="#000", outline="")
        canvas.create_oval(x+2*s, y+8*s, x+6*s, y+12*s, fill="#000", outline="")
        
        # ========== 嘴巴 ==========
        canvas.create_oval(x-14*s, y+10*s, x-4*s, y+22*s, fill="#D4B896", outline="")
        canvas.create_oval(x+4*s, y+10*s, x+14*s, y+22*s, fill="#D4B896", outline="")
        canvas.create_line(x, y+15*s, x, y+20*s, fill="#4A3728", width=int(2*s)+1)
        canvas.create_arc(x-10*s, y+14*s, x, y+25*s, start=270, extent=70, style="arc", outline="#4A3728", width=int(2*s)+1)
        canvas.create_arc(x, y+14*s, x+10*s, y+25*s, start=200, extent=70, style="arc", outline="#4A3728", width=int(2*s)+1)
        
        # ========== 警察帽 ==========
        canvas.create_oval(x-32*s, y-42*s, x+32*s, y-30*s, fill="#0D47A1", outline="")
        canvas.create_oval(x-30*s, y-40*s, x+30*s, y-28*s, fill="#1565C0", outline="#0D47A1", width=2)
        canvas.create_arc(x-25*s, y-38*s, x+25*s, y-30*s, start=0, extent=180, style="arc", outline="#1E88E5", width=2)
        canvas.create_arc(x-26*s, y-62*s, x+26*s, y-32*s, start=0, extent=180, fill="#1976D2", outline="#1565C0", width=2)
        canvas.create_arc(x-20*s, y-58*s, x+20*s, y-38*s, start=20, extent=140, style="arc", outline="#42A5F5", width=2)
        canvas.create_rectangle(x-24*s, y-40*s, x+24*s, y-35*s, fill="#0D47A1", outline="")
        canvas.create_rectangle(x-5*s, y-41*s, x+5*s, y-34*s, fill="#FFD700", outline="#FFA000", width=1)
        ThemeDrawings._draw_star_badge(canvas, x, y-50*s, 10*s)
        
        # 脸颊腮红
        canvas.create_oval(x-24*s, y-5*s, x-16*s, y+3*s, fill="#FFCDD2", outline="")
        canvas.create_oval(x+16*s, y-5*s, x+24*s, y+3*s, fill="#FFCDD2", outline="")
    
    @staticmethod
    def _draw_paw_badge(canvas, x, y, size):
        """绘制爪印徽章"""
        s = size
        canvas.create_oval(x-s*0.7, y-s*0.2, x+s*0.7, y+s*0.8, fill="#0D47A1", outline="")
        for dx, dy in [(-s*0.5, -s*0.5), (-s*0.15, -s*0.7), (s*0.15, -s*0.7), (s*0.5, -s*0.5)]:
            canvas.create_oval(x+dx-s*0.2, y+dy-s*0.2, x+dx+s*0.2, y+dy+s*0.2, fill="#0D47A1", outline="")
    
    @staticmethod
    def _draw_star_badge(canvas, x, y, size):
        """绘制星星徽章"""
        s = size
        canvas.create_oval(x-s*1.2, y-s*1.2, x+s*1.2, y+s*1.2, fill="#FFA000", outline="#FF8F00", width=2)
        points = []
        for i in range(5):
            angle = math.radians(90 + i * 72)
            points.extend([x + s * math.cos(angle), y - s * math.sin(angle)])
            angle = math.radians(90 + i * 72 + 36)
            points.extend([x + s * 0.4 * math.cos(angle), y - s * 0.4 * math.sin(angle)])
        canvas.create_polygon(points, fill="#FFD700", outline="#FFC107", width=1)
        canvas.create_oval(x-s*0.3, y-s*0.5, x+s*0.1, y-s*0.1, fill="#FFECB3", outline="")
    
    @staticmethod
    def _draw_mini_star(canvas, x, y, size, color="#FFD700"):
        """绘制小星星"""
        points = []
        for i in range(5):
            angle = math.radians(90 + i * 72)
            points.extend([x + size * math.cos(angle), y - size * math.sin(angle)])
            angle = math.radians(90 + i * 72 + 36)
            points.extend([x + size * 0.4 * math.cos(angle), y - size * 0.4 * math.sin(angle)])
        canvas.create_polygon(points, fill=color, outline="#DAA520", width=1)
    
    @staticmethod
    def _draw_mini_paw(canvas, x, y, size):
        """绘制小爪印"""
        s = size
        canvas.create_oval(x-s*0.8, y-s*0.3, x+s*0.8, y+s*0.8, fill="#1565C0", outline="")
        for dx, dy in [(-s*0.6, -s*0.6), (-s*0.2, -s*0.9), (s*0.2, -s*0.9), (s*0.6, -s*0.6)]:
            canvas.create_oval(x+dx-s*0.25, y+dy-s*0.25, x+dx+s*0.25, y+dy+s*0.25, fill="#1565C0", outline="")

    @staticmethod
    def draw_puppy_marshall(canvas, x, y, scale=1.0):
        """毛毛 - 斑点狗消防犬 - 超精细版本
        特点：白色身体黑色斑点、下垂的黑耳朵、红色消防装备
        """
        s = scale
        
        # ========== 尾巴（先画，在身体后面）==========
        canvas.create_polygon(
            x+18*s, y+42*s, x+32*s, y+28*s, x+38*s, y+25*s,
            x+36*s, y+32*s, x+24*s, y+46*s,
            fill="#FAFAFA", outline="#E0E0E0", width=1, smooth=True
        )
        # 尾巴斑点
        canvas.create_oval(x+28*s, y+30*s, x+34*s, y+36*s, fill="#1a1a1a", outline="")
        
        # ========== 后腿 ==========
        canvas.create_oval(x-28*s, y+40*s, x-10*s, y+70*s, fill="#FAFAFA", outline="")
        canvas.create_oval(x-30*s, y+60*s, x-12*s, y+75*s, fill="#E0E0E0", outline="")
        canvas.create_oval(x+10*s, y+40*s, x+28*s, y+70*s, fill="#FAFAFA", outline="")
        canvas.create_oval(x+12*s, y+60*s, x+30*s, y+75*s, fill="#E0E0E0", outline="")
        
        # ========== 身体（多层渐变）==========
        canvas.create_oval(x-30*s, y+5*s, x+30*s, y+58*s, fill="#E8E8E8", outline="")
        canvas.create_oval(x-28*s, y+8*s, x+28*s, y+55*s, fill="#F0F0F0", outline="")
        canvas.create_oval(x-26*s, y+10*s, x+26*s, y+52*s, fill="#FAFAFA", outline="")
        
        # 身体斑点（更自然的分布）
        spots_body = [(-14, 18, 7), (12, 22, 6), (-6, 35, 8), (16, 40, 5), (-18, 42, 6), (8, 48, 5)]
        for dx, dy, r in spots_body:
            canvas.create_oval(x+dx*s-r*s, y+dy*s-r*s, x+dx*s+r*s, y+dy*s+r*s, fill="#1a1a1a", outline="")
            # 斑点高光
            canvas.create_oval(x+(dx-1)*s, y+(dy-2)*s, x+(dx+2)*s, y+(dy+1)*s, fill="#333", outline="")
        
        # ========== 前腿 ==========
        canvas.create_polygon(x-24*s, y+38*s, x-12*s, y+38*s, x-10*s, y+68*s, x-26*s, y+68*s,
                             fill="#FAFAFA", outline="#E0E0E0", width=1)
        canvas.create_line(x-18*s, y+40*s, x-17*s, y+62*s, fill="#F5F5F5", width=2)
        canvas.create_oval(x-28*s, y+63*s, x-8*s, y+76*s, fill="#E0E0E0", outline="#BDBDBD", width=1)
        
        canvas.create_polygon(x+12*s, y+38*s, x+24*s, y+38*s, x+26*s, y+68*s, x+10*s, y+68*s,
                             fill="#FAFAFA", outline="#E0E0E0", width=1)
        canvas.create_line(x+18*s, y+40*s, x+17*s, y+62*s, fill="#F5F5F5", width=2)
        canvas.create_oval(x+8*s, y+63*s, x+28*s, y+76*s, fill="#E0E0E0", outline="#BDBDBD", width=1)
        
        # ========== 项圈 ==========
        canvas.create_rectangle(x-22*s, y+2*s, x+22*s, y+14*s, fill="#D32F2F", outline="#B71C1C", width=2)
        canvas.create_line(x-20*s, y+5*s, x+20*s, y+5*s, fill="#E53935", width=2)
        canvas.create_line(x-20*s, y+11*s, x+20*s, y+11*s, fill="#C62828", width=1)
        canvas.create_oval(x-5*s, y+3*s, x+5*s, y+13*s, fill="#FFD700", outline="#FFA000", width=2)
        ThemeDrawings._draw_paw_badge(canvas, x, y+8*s, 5*s)
        
        # ========== 头部（多层渐变）==========
        canvas.create_oval(x-28*s, y-38*s, x+28*s, y+20*s, fill="#E8E8E8", outline="")
        canvas.create_oval(x-26*s, y-36*s, x+26*s, y+18*s, fill="#F5F5F5", outline="")
        canvas.create_oval(x-24*s, y-34*s, x+24*s, y+16*s, fill="#FAFAFA", outline="")
        
        # 头部斑点
        spots_head = [(-16, -26, 6), (14, -22, 5), (-4, -32, 5), (8, -28, 4), (-20, -12, 4)]
        for dx, dy, r in spots_head:
            canvas.create_oval(x+dx*s-r*s, y+dy*s-r*s, x+dx*s+r*s, y+dy*s+r*s, fill="#1a1a1a", outline="")
            canvas.create_oval(x+(dx-1)*s, y+(dy-1)*s, x+(dx+1)*s, y+(dy+1)*s, fill="#333", outline="")
        
        # ========== 耳朵（下垂的黑耳朵）==========
        # 左耳
        canvas.create_oval(x-38*s, y-24*s, x-10*s, y+12*s, fill="#1a1a1a", outline="#111", width=2)
        canvas.create_oval(x-35*s, y-20*s, x-14*s, y+8*s, fill="#2a2a2a", outline="")
        canvas.create_oval(x-32*s, y-16*s, x-18*s, y+2*s, fill="#FFB6C1", outline="")
        canvas.create_oval(x-30*s, y-12*s, x-20*s, y-2*s, fill="#FFC0CB", outline="")
        # 右耳
        canvas.create_oval(x+10*s, y-24*s, x+38*s, y+12*s, fill="#1a1a1a", outline="#111", width=2)
        canvas.create_oval(x+14*s, y-20*s, x+35*s, y+8*s, fill="#2a2a2a", outline="")
        canvas.create_oval(x+18*s, y-16*s, x+32*s, y+2*s, fill="#FFB6C1", outline="")
        canvas.create_oval(x+20*s, y-12*s, x+30*s, y-2*s, fill="#FFC0CB", outline="")
        
        # ========== 眼睛（大而有神）==========
        # 眼眶阴影
        canvas.create_oval(x-17*s, y-18*s, x-3*s, y-1*s, fill="#E0E0E0", outline="")
        canvas.create_oval(x+3*s, y-18*s, x+17*s, y-1*s, fill="#E0E0E0", outline="")
        # 眼白
        canvas.create_oval(x-16*s, y-17*s, x-4*s, y-2*s, fill="white", outline="#333", width=1)
        canvas.create_oval(x+4*s, y-17*s, x+16*s, y-2*s, fill="white", outline="#333", width=1)
        # 虹膜
        canvas.create_oval(x-14*s, y-15*s, x-6*s, y-4*s, fill="#6D4C41", outline="")
        canvas.create_oval(x+6*s, y-15*s, x+14*s, y-4*s, fill="#6D4C41", outline="")
        # 瞳孔
        canvas.create_oval(x-12*s, y-13*s, x-8*s, y-7*s, fill="#1a1a1a", outline="")
        canvas.create_oval(x+8*s, y-13*s, x+12*s, y-7*s, fill="#1a1a1a", outline="")
        # 高光
        canvas.create_oval(x-13*s, y-14*s, x-10*s, y-11*s, fill="white", outline="")
        canvas.create_oval(x+9*s, y-14*s, x+12*s, y-11*s, fill="white", outline="")
        canvas.create_oval(x-9*s, y-8*s, x-7*s, y-6*s, fill="#EEEEEE", outline="")
        canvas.create_oval(x+7*s, y-8*s, x+9*s, y-6*s, fill="#EEEEEE", outline="")
        
        # ========== 鼻子 ==========
        canvas.create_polygon(x-5*s, y-5*s, x+5*s, y-5*s, x+7*s, y+5*s, x-7*s, y+5*s,
                             fill="#FAFAFA", outline="", smooth=True)
        canvas.create_oval(x-10*s, y+2*s, x+10*s, y+16*s, fill="#1a1a1a", outline="#111", width=1)
        canvas.create_oval(x-6*s, y+4*s, x-1*s, y+9*s, fill="#444", outline="")
        canvas.create_oval(x-4*s, y+5*s, x-2*s, y+7*s, fill="#666", outline="")
        # 鼻孔
        canvas.create_oval(x-5*s, y+10*s, x-1*s, y+14*s, fill="#000", outline="")
        canvas.create_oval(x+1*s, y+10*s, x+5*s, y+14*s, fill="#000", outline="")
        
        # ========== 嘴巴（开心的笑）==========
        canvas.create_oval(x-16*s, y+10*s, x-4*s, y+24*s, fill="#FAFAFA", outline="")
        canvas.create_oval(x+4*s, y+10*s, x+16*s, y+24*s, fill="#FAFAFA", outline="")
        canvas.create_line(x, y+16*s, x, y+22*s, fill="#333", width=int(2*s)+1)
        canvas.create_arc(x-12*s, y+16*s, x, y+28*s, start=270, extent=70, style="arc", outline="#333", width=int(2*s)+1)
        canvas.create_arc(x, y+16*s, x+12*s, y+28*s, start=200, extent=70, style="arc", outline="#333", width=int(2*s)+1)
        # 舌头
        canvas.create_oval(x-6*s, y+20*s, x+6*s, y+32*s, fill="#FF6B6B", outline="#E53935", width=1)
        canvas.create_line(x, y+22*s, x, y+30*s, fill="#E53935", width=1)
        
        # ========== 消防帽 ==========
        # 帽檐
        canvas.create_rectangle(x-32*s, y-42*s, x+32*s, y-34*s, fill="#B71C1C", outline="")
        canvas.create_rectangle(x-30*s, y-40*s, x+30*s, y-32*s, fill="#D32F2F", outline="#B71C1C", width=2)
        canvas.create_line(x-28*s, y-38*s, x+28*s, y-38*s, fill="#E53935", width=2)
        # 帽身
        canvas.create_arc(x-26*s, y-62*s, x+26*s, y-32*s, start=0, extent=180, fill="#F44336", outline="#D32F2F", width=2)
        canvas.create_arc(x-22*s, y-58*s, x+22*s, y-38*s, start=20, extent=140, style="arc", outline="#EF5350", width=2)
        # 帽徽底座
        canvas.create_oval(x-10*s, y-54*s, x+10*s, y-40*s, fill="#FFA000", outline="#FF8F00", width=2)
        # 帽徽文字
        canvas.create_oval(x-8*s, y-52*s, x+8*s, y-42*s, fill="#FFD700", outline="")
        canvas.create_text(x, y-47*s, text="119", font=("Arial", int(6*s), "bold"), fill="#D32F2F")
        
        # 脸颊腮红
        canvas.create_oval(x-22*s, y-2*s, x-14*s, y+6*s, fill="#FFCDD2", outline="")
        canvas.create_oval(x+14*s, y-2*s, x+22*s, y+6*s, fill="#FFCDD2", outline="")
    
    @staticmethod
    def draw_puppy_skye(canvas, x, y, scale=1.0):
        """天天 - 可卡犬飞行员 - 超精细版本
        特点：奶油色长卷毛、大眼睛睫毛、粉色飞行装备
        """
        s = scale
        
        # ========== 尾巴（先画）==========
        canvas.create_polygon(
            x+16*s, y+40*s, x+28*s, y+25*s, x+35*s, y+22*s,
            x+32*s, y+30*s, x+22*s, y+44*s,
            fill="#C4A574", outline="#B8956A", width=1, smooth=True
        )
        # 尾巴毛发纹理
        canvas.create_line(x+22*s, y+35*s, x+28*s, y+26*s, fill="#D4B896", width=2)
        
        # ========== 后腿 ==========
        canvas.create_oval(x-26*s, y+38*s, x-8*s, y+65*s, fill="#DEB887", outline="")
        canvas.create_oval(x-28*s, y+58*s, x-10*s, y+70*s, fill="#C4A574", outline="")
        canvas.create_oval(x+8*s, y+38*s, x+26*s, y+65*s, fill="#DEB887", outline="")
        canvas.create_oval(x+10*s, y+58*s, x+28*s, y+70*s, fill="#C4A574", outline="")
        
        # ========== 身体（多层渐变）==========
        canvas.create_oval(x-26*s, y+8*s, x+26*s, y+52*s, fill="#C4A574", outline="")
        canvas.create_oval(x-24*s, y+10*s, x+24*s, y+50*s, fill="#DEB887", outline="")
        canvas.create_oval(x-22*s, y+12*s, x+22*s, y+48*s, fill="#F5DEB3", outline="")
        
        # 胸前浅色毛发
        canvas.create_oval(x-14*s, y+14*s, x+14*s, y+40*s, fill="#FFF8DC", outline="")
        # 毛发纹理
        for i in range(-10, 11, 5):
            canvas.create_line(x+i*s, y+18*s, x+i*s, y+36*s, fill="#F5DEB3", width=1)
        
        # ========== 前腿 ==========
        canvas.create_polygon(x-20*s, y+36*s, x-10*s, y+36*s, x-8*s, y+62*s, x-22*s, y+62*s,
                             fill="#DEB887", outline="#C4A574", width=1)
        canvas.create_line(x-15*s, y+38*s, x-14*s, y+58*s, fill="#F5DEB3", width=2)
        canvas.create_oval(x-24*s, y+58*s, x-6*s, y+70*s, fill="#C4A574", outline="#B8956A", width=1)
        
        canvas.create_polygon(x+10*s, y+36*s, x+20*s, y+36*s, x+22*s, y+62*s, x+8*s, y+62*s,
                             fill="#DEB887", outline="#C4A574", width=1)
        canvas.create_line(x+15*s, y+38*s, x+14*s, y+58*s, fill="#F5DEB3", width=2)
        canvas.create_oval(x+6*s, y+58*s, x+24*s, y+70*s, fill="#C4A574", outline="#B8956A", width=1)
        
        # ========== 翅膀背包 ==========
        # 左翅膀
        canvas.create_polygon(
            x-22*s, y+20*s, x-38*s, y+8*s, x-42*s, y+12*s, x-36*s, y+32*s, x-24*s, y+35*s,
            fill="#EC407A", outline="#D81B60", width=2, smooth=True
        )
        canvas.create_polygon(x-26*s, y+22*s, x-36*s, y+14*s, x-32*s, y+28*s,
                             fill="#F06292", outline="", smooth=True)
        # 右翅膀
        canvas.create_polygon(
            x+22*s, y+20*s, x+38*s, y+8*s, x+42*s, y+12*s, x+36*s, y+32*s, x+24*s, y+35*s,
            fill="#EC407A", outline="#D81B60", width=2, smooth=True
        )
        canvas.create_polygon(x+26*s, y+22*s, x+36*s, y+14*s, x+32*s, y+28*s,
                             fill="#F06292", outline="", smooth=True)
        
        # ========== 项圈 ==========
        canvas.create_rectangle(x-18*s, y+5*s, x+18*s, y+15*s, fill="#EC407A", outline="#D81B60", width=2)
        canvas.create_line(x-16*s, y+8*s, x+16*s, y+8*s, fill="#F06292", width=2)
        canvas.create_oval(x-5*s, y+6*s, x+5*s, y+14*s, fill="#FFD700", outline="#FFA000", width=2)
        
        # ========== 头部（多层渐变）==========
        canvas.create_oval(x-26*s, y-35*s, x+26*s, y+18*s, fill="#C4A574", outline="")
        canvas.create_oval(x-24*s, y-33*s, x+24*s, y+16*s, fill="#DEB887", outline="")
        canvas.create_oval(x-22*s, y-31*s, x+22*s, y+14*s, fill="#F5DEB3", outline="")
        
        # ========== 耳朵（长长的卷毛耳朵）==========
        # 左耳
        canvas.create_oval(x-40*s, y-26*s, x-10*s, y+22*s, fill="#C4A574", outline="#B8956A", width=2)
        canvas.create_oval(x-38*s, y-22*s, x-14*s, y+18*s, fill="#DEB887", outline="")
        canvas.create_oval(x-36*s, y-18*s, x-18*s, y+12*s, fill="#E8D4B8", outline="")
        # 耳朵毛发纹理
        for i in range(-32, -18, 4):
            canvas.create_line(x+i*s, y-10*s, x+(i-2)*s, y+8*s, fill="#C4A574", width=1)
        # 右耳
        canvas.create_oval(x+10*s, y-26*s, x+40*s, y+22*s, fill="#C4A574", outline="#B8956A", width=2)
        canvas.create_oval(x+14*s, y-22*s, x+38*s, y+18*s, fill="#DEB887", outline="")
        canvas.create_oval(x+18*s, y-18*s, x+36*s, y+12*s, fill="#E8D4B8", outline="")
        for i in range(18, 32, 4):
            canvas.create_line(x+i*s, y-10*s, x+(i+2)*s, y+8*s, fill="#C4A574", width=1)
        
        # ========== 眼睛（大而有神，带睫毛）==========
        # 眼眶
        canvas.create_oval(x-18*s, y-20*s, x-4*s, y-2*s, fill="#DEB887", outline="")
        canvas.create_oval(x+4*s, y-20*s, x+18*s, y-2*s, fill="#DEB887", outline="")
        # 眼白
        canvas.create_oval(x-17*s, y-19*s, x-5*s, y-3*s, fill="white", outline="#333", width=1)
        canvas.create_oval(x+5*s, y-19*s, x+17*s, y-3*s, fill="white", outline="#333", width=1)
        # 虹膜
        canvas.create_oval(x-15*s, y-17*s, x-7*s, y-5*s, fill="#8B4513", outline="")
        canvas.create_oval(x+7*s, y-17*s, x+15*s, y-5*s, fill="#8B4513", outline="")
        # 瞳孔
        canvas.create_oval(x-13*s, y-15*s, x-9*s, y-8*s, fill="#1a1a1a", outline="")
        canvas.create_oval(x+9*s, y-15*s, x+13*s, y-8*s, fill="#1a1a1a", outline="")
        # 高光
        canvas.create_oval(x-14*s, y-16*s, x-11*s, y-13*s, fill="white", outline="")
        canvas.create_oval(x+10*s, y-16*s, x+13*s, y-13*s, fill="white", outline="")
        canvas.create_oval(x-10*s, y-9*s, x-8*s, y-7*s, fill="#EEEEEE", outline="")
        canvas.create_oval(x+8*s, y-9*s, x+10*s, y-7*s, fill="#EEEEEE", outline="")
        # 睫毛（更精细）
        for dx, angle in [(-16, 120), (-13, 100), (-10, 80)]:
            rad = math.radians(angle)
            canvas.create_line(x+dx*s, y-19*s, x+dx*s+6*s*math.cos(rad), y-19*s-6*s*math.sin(rad), 
                              fill="#333", width=int(1.5*s)+1)
        for dx, angle in [(10, 100), (13, 80), (16, 60)]:
            rad = math.radians(angle)
            canvas.create_line(x+dx*s, y-19*s, x+dx*s+6*s*math.cos(rad), y-19*s-6*s*math.sin(rad), 
                              fill="#333", width=int(1.5*s)+1)
        
        # ========== 鼻子 ==========
        canvas.create_polygon(x-4*s, y-4*s, x+4*s, y-4*s, x+6*s, y+4*s, x-6*s, y+4*s,
                             fill="#F5DEB3", outline="", smooth=True)
        canvas.create_oval(x-8*s, y+2*s, x+8*s, y+14*s, fill="#1a1a1a", outline="#111", width=1)
        canvas.create_oval(x-5*s, y+4*s, x-1*s, y+8*s, fill="#444", outline="")
        canvas.create_oval(x-3*s, y+5*s, x-1*s, y+7*s, fill="#666", outline="")
        
        # ========== 嘴巴 ==========
        canvas.create_oval(x-12*s, y+8*s, x-2*s, y+20*s, fill="#F5DEB3", outline="")
        canvas.create_oval(x+2*s, y+8*s, x+12*s, y+20*s, fill="#F5DEB3", outline="")
        canvas.create_line(x, y+14*s, x, y+18*s, fill="#333", width=int(2*s)+1)
        canvas.create_arc(x-10*s, y+12*s, x, y+22*s, start=270, extent=70, style="arc", outline="#333", width=int(2*s)+1)
        canvas.create_arc(x, y+12*s, x+10*s, y+22*s, start=200, extent=70, style="arc", outline="#333", width=int(2*s)+1)
        
        # ========== 飞行帽和护目镜 ==========
        # 帽子
        canvas.create_arc(x-28*s, y-48*s, x+28*s, y-22*s, start=0, extent=180, fill="#EC407A", outline="#D81B60", width=2)
        canvas.create_arc(x-24*s, y-44*s, x+24*s, y-28*s, start=20, extent=140, style="arc", outline="#F06292", width=2)
        # 护目镜带
        canvas.create_rectangle(x-30*s, y-34*s, x+30*s, y-28*s, fill="#AD1457", outline="#880E4F", width=1)
        canvas.create_line(x-28*s, y-31*s, x+28*s, y-31*s, fill="#C2185B", width=2)
        # 护目镜
        canvas.create_oval(x-24*s, y-42*s, x-6*s, y-26*s, fill="#4FC3F7", outline="#0288D1", width=2)
        canvas.create_oval(x+6*s, y-42*s, x+24*s, y-26*s, fill="#4FC3F7", outline="#0288D1", width=2)
        # 镜片高光
        canvas.create_arc(x-22*s, y-40*s, x-10*s, y-30*s, start=45, extent=90, style="arc", outline="white", width=2)
        canvas.create_arc(x+10*s, y-40*s, x+22*s, y-30*s, start=45, extent=90, style="arc", outline="white", width=2)
        canvas.create_oval(x-20*s, y-38*s, x-16*s, y-34*s, fill="#B3E5FC", outline="")
        canvas.create_oval(x+16*s, y-38*s, x+20*s, y-34*s, fill="#B3E5FC", outline="")
        
        # 脸颊腮红
        canvas.create_oval(x-20*s, y-2*s, x-12*s, y+6*s, fill="#FFCDD2", outline="")
        canvas.create_oval(x+12*s, y-2*s, x+20*s, y+6*s, fill="#FFCDD2", outline="")
    
    @staticmethod
    def draw_puppy_rubble(canvas, x, y, scale=1.0):
        """小砾 - 英国斗牛犬工程师 - 超精细版本
        特点：矮胖身材、宽脸皱纹、黄色工程装备
        """
        s = scale
        
        # ========== 尾巴（短小卷曲）==========
        canvas.create_oval(x+22*s, y+42*s, x+34*s, y+52*s, fill="#D4A056", outline="#C49346", width=1)
        canvas.create_oval(x+24*s, y+44*s, x+32*s, y+50*s, fill="#E8B86D", outline="")
        
        # ========== 后腿（粗短）==========
        canvas.create_oval(x-32*s, y+42*s, x-12*s, y+72*s, fill="#E8B86D", outline="")
        canvas.create_oval(x-34*s, y+62*s, x-14*s, y+76*s, fill="#D4A056", outline="")
        canvas.create_oval(x+12*s, y+42*s, x+32*s, y+72*s, fill="#E8B86D", outline="")
        canvas.create_oval(x+14*s, y+62*s, x+34*s, y+76*s, fill="#D4A056", outline="")
        
        # ========== 身体（矮胖多层）==========
        canvas.create_oval(x-34*s, y+2*s, x+34*s, y+58*s, fill="#D4A056", outline="")
        canvas.create_oval(x-32*s, y+5*s, x+32*s, y+55*s, fill="#E8B86D", outline="")
        canvas.create_oval(x-30*s, y+8*s, x+30*s, y+52*s, fill="#F5DEB3", outline="")
        
        # 胸前浅色
        canvas.create_oval(x-18*s, y+12*s, x+18*s, y+42*s, fill="#FFF8DC", outline="")
        # 毛发纹理
        for i in range(-12, 13, 6):
            canvas.create_line(x+i*s, y+16*s, x+i*s, y+38*s, fill="#F5DEB3", width=1)
        
        # ========== 前腿（粗短）==========
        canvas.create_polygon(x-28*s, y+38*s, x-14*s, y+38*s, x-12*s, y+66*s, x-30*s, y+66*s,
                             fill="#E8B86D", outline="#D4A056", width=1)
        canvas.create_line(x-22*s, y+40*s, x-20*s, y+60*s, fill="#F5DEB3", width=2)
        canvas.create_oval(x-32*s, y+62*s, x-10*s, y+76*s, fill="#D4A056", outline="#C49346", width=1)
        
        canvas.create_polygon(x+14*s, y+38*s, x+28*s, y+38*s, x+30*s, y+66*s, x+12*s, y+66*s,
                             fill="#E8B86D", outline="#D4A056", width=1)
        canvas.create_line(x+22*s, y+40*s, x+20*s, y+60*s, fill="#F5DEB3", width=2)
        canvas.create_oval(x+10*s, y+62*s, x+32*s, y+76*s, fill="#D4A056", outline="#C49346", width=1)
        
        # ========== 项圈 ==========
        canvas.create_rectangle(x-24*s, y+0*s, x+24*s, y+12*s, fill="#FFC107", outline="#FFA000", width=2)
        canvas.create_line(x-22*s, y+3*s, x+22*s, y+3*s, fill="#FFCA28", width=2)
        canvas.create_line(x-22*s, y+9*s, x+22*s, y+9*s, fill="#FF8F00", width=1)
        canvas.create_oval(x-5*s, y+1*s, x+5*s, y+11*s, fill="#FF6F00", outline="#E65100", width=2)
        
        # ========== 头部（宽脸多层）==========
        canvas.create_oval(x-32*s, y-38*s, x+32*s, y+20*s, fill="#D4A056", outline="")
        canvas.create_oval(x-30*s, y-36*s, x+30*s, y+18*s, fill="#E8B86D", outline="")
        canvas.create_oval(x-28*s, y-34*s, x+28*s, y+16*s, fill="#F5DEB3", outline="")
        
        # 脸颊肉（斗牛犬特征）
        canvas.create_oval(x-34*s, y-8*s, x-14*s, y+18*s, fill="#F5DEB3", outline="")
        canvas.create_oval(x+14*s, y-8*s, x+34*s, y+18*s, fill="#F5DEB3", outline="")
        # 脸颊皱纹
        canvas.create_arc(x-32*s, y-2*s, x-18*s, y+12*s, start=300, extent=120, style="arc", outline="#D4A056", width=1)
        canvas.create_arc(x+18*s, y-2*s, x+32*s, y+12*s, start=220, extent=120, style="arc", outline="#D4A056", width=1)
        
        # ========== 耳朵（小而圆）==========
        canvas.create_oval(x-34*s, y-34*s, x-18*s, y-14*s, fill="#D4A056", outline="#C49346", width=2)
        canvas.create_oval(x-32*s, y-32*s, x-20*s, y-16*s, fill="#E8B86D", outline="")
        canvas.create_oval(x-30*s, y-28*s, x-22*s, y-20*s, fill="#FFB6C1", outline="")
        
        canvas.create_oval(x+18*s, y-34*s, x+34*s, y-14*s, fill="#D4A056", outline="#C49346", width=2)
        canvas.create_oval(x+20*s, y-32*s, x+32*s, y-16*s, fill="#E8B86D", outline="")
        canvas.create_oval(x+22*s, y-28*s, x+30*s, y-20*s, fill="#FFB6C1", outline="")
        
        # ========== 眼睛 ==========
        canvas.create_oval(x-18*s, y-18*s, x-5*s, y-2*s, fill="#E8B86D", outline="")
        canvas.create_oval(x+5*s, y-18*s, x+18*s, y-2*s, fill="#E8B86D", outline="")
        canvas.create_oval(x-17*s, y-17*s, x-6*s, y-3*s, fill="white", outline="#333", width=1)
        canvas.create_oval(x+6*s, y-17*s, x+17*s, y-3*s, fill="white", outline="#333", width=1)
        canvas.create_oval(x-14*s, y-14*s, x-8*s, y-6*s, fill="#5D4037", outline="")
        canvas.create_oval(x+8*s, y-14*s, x+14*s, y-6*s, fill="#5D4037", outline="")
        canvas.create_oval(x-12*s, y-12*s, x-10*s, y-8*s, fill="#1a1a1a", outline="")
        canvas.create_oval(x+10*s, y-12*s, x+12*s, y-8*s, fill="#1a1a1a", outline="")
        canvas.create_oval(x-13*s, y-13*s, x-11*s, y-11*s, fill="white", outline="")
        canvas.create_oval(x+11*s, y-13*s, x+13*s, y-11*s, fill="white", outline="")
        
        # ========== 鼻子（大而扁）==========
        canvas.create_polygon(x-8*s, y-6*s, x+8*s, y-6*s, x+10*s, y+6*s, x-10*s, y+6*s,
                             fill="#F5DEB3", outline="", smooth=True)
        canvas.create_oval(x-12*s, y+2*s, x+12*s, y+18*s, fill="#1a1a1a", outline="#111", width=1)
        canvas.create_oval(x-8*s, y+4*s, x-2*s, y+10*s, fill="#444", outline="")
        canvas.create_oval(x-6*s, y+5*s, x-3*s, y+8*s, fill="#666", outline="")
        canvas.create_oval(x-7*s, y+11*s, x-2*s, y+16*s, fill="#000", outline="")
        canvas.create_oval(x+2*s, y+11*s, x+7*s, y+16*s, fill="#000", outline="")
        
        # ========== 嘴巴（下垂的嘴角）==========
        canvas.create_oval(x-18*s, y+10*s, x-4*s, y+26*s, fill="#F5DEB3", outline="")
        canvas.create_oval(x+4*s, y+10*s, x+18*s, y+26*s, fill="#F5DEB3", outline="")
        canvas.create_line(x, y+18*s, x, y+24*s, fill="#4A3728", width=int(2*s)+1)
        canvas.create_arc(x-14*s, y+16*s, x, y+30*s, start=270, extent=70, style="arc", outline="#4A3728", width=int(2*s)+1)
        canvas.create_arc(x, y+16*s, x+14*s, y+30*s, start=200, extent=70, style="arc", outline="#4A3728", width=int(2*s)+1)
        # 下巴褶皱
        canvas.create_arc(x-12*s, y+22*s, x+12*s, y+34*s, start=200, extent=140, style="arc", outline="#D4A056", width=1)
        
        # ========== 工程帽 ==========
        # 帽檐
        canvas.create_rectangle(x-36*s, y-44*s, x+36*s, y-36*s, fill="#FF8F00", outline="")
        canvas.create_rectangle(x-34*s, y-42*s, x+34*s, y-34*s, fill="#FFC107", outline="#FFA000", width=2)
        canvas.create_line(x-32*s, y-40*s, x+32*s, y-40*s, fill="#FFCA28", width=2)
        # 帽身
        canvas.create_arc(x-30*s, y-66*s, x+30*s, y-34*s, start=0, extent=180, fill="#FFCA28", outline="#FFC107", width=2)
        canvas.create_arc(x-26*s, y-62*s, x+26*s, y-40*s, start=20, extent=140, style="arc", outline="#FFD54F", width=2)
        # 帽子条纹
        canvas.create_rectangle(x-27*s, y-56*s, x+27*s, y-50*s, fill="#FF8F00", outline="")
        canvas.create_line(x-25*s, y-53*s, x+25*s, y-53*s, fill="#FF6F00", width=2)
        
        # 脸颊腮红
        canvas.create_oval(x-26*s, y-2*s, x-18*s, y+6*s, fill="#FFCDD2", outline="")
        canvas.create_oval(x+18*s, y-2*s, x+26*s, y+6*s, fill="#FFCDD2", outline="")
    
    @staticmethod
    def draw_puppy_rocky(canvas, x, y, scale=1.0):
        """灰灰(Rocky) - 混种犬环保员 - 超精细版本
        特点：灰色毛发、半竖立耳朵、绿色环保装备
        """
        s = scale
        
        # ========== 尾巴 ==========
        canvas.create_polygon(
            x+18*s, y+42*s, x+30*s, y+28*s, x+36*s, y+26*s,
            x+34*s, y+34*s, x+24*s, y+46*s,
            fill="#78909C", outline="#546E7A", width=1, smooth=True
        )
        
        # ========== 后腿 ==========
        canvas.create_oval(x-28*s, y+40*s, x-10*s, y+68*s, fill="#78909C", outline="")
        canvas.create_oval(x-30*s, y+60*s, x-12*s, y+74*s, fill="#546E7A", outline="")
        canvas.create_oval(x+10*s, y+40*s, x+28*s, y+68*s, fill="#78909C", outline="")
        canvas.create_oval(x+12*s, y+60*s, x+30*s, y+74*s, fill="#546E7A", outline="")
        
        # ========== 身体（多层渐变）==========
        canvas.create_oval(x-28*s, y+5*s, x+28*s, y+55*s, fill="#546E7A", outline="")
        canvas.create_oval(x-26*s, y+8*s, x+26*s, y+52*s, fill="#78909C", outline="")
        canvas.create_oval(x-24*s, y+10*s, x+24*s, y+50*s, fill="#90A4AE", outline="")
        
        # 胸前浅色
        canvas.create_oval(x-14*s, y+14*s, x+14*s, y+42*s, fill="#B0BEC5", outline="")
        for i in range(-10, 11, 5):
            canvas.create_line(x+i*s, y+18*s, x+i*s, y+38*s, fill="#90A4AE", width=1)
        
        # ========== 前腿 ==========
        canvas.create_polygon(x-22*s, y+38*s, x-10*s, y+38*s, x-8*s, y+66*s, x-24*s, y+66*s,
                             fill="#78909C", outline="#546E7A", width=1)
        canvas.create_line(x-16*s, y+40*s, x-15*s, y+60*s, fill="#90A4AE", width=2)
        canvas.create_oval(x-26*s, y+62*s, x-6*s, y+74*s, fill="#546E7A", outline="#455A64", width=1)
        
        canvas.create_polygon(x+10*s, y+38*s, x+22*s, y+38*s, x+24*s, y+66*s, x+8*s, y+66*s,
                             fill="#78909C", outline="#546E7A", width=1)
        canvas.create_line(x+16*s, y+40*s, x+15*s, y+60*s, fill="#90A4AE", width=2)
        canvas.create_oval(x+6*s, y+62*s, x+26*s, y+74*s, fill="#546E7A", outline="#455A64", width=1)
        
        # ========== 项圈 ==========
        canvas.create_rectangle(x-20*s, y+2*s, x+20*s, y+12*s, fill="#4CAF50", outline="#388E3C", width=2)
        canvas.create_line(x-18*s, y+5*s, x+18*s, y+5*s, fill="#66BB6A", width=2)
        canvas.create_oval(x-5*s, y+3*s, x+5*s, y+11*s, fill="#8BC34A", outline="#689F38", width=2)
        
        # ========== 头部（多层渐变）==========
        canvas.create_oval(x-26*s, y-35*s, x+26*s, y+18*s, fill="#546E7A", outline="")
        canvas.create_oval(x-24*s, y-33*s, x+24*s, y+16*s, fill="#78909C", outline="")
        canvas.create_oval(x-22*s, y-31*s, x+22*s, y+14*s, fill="#90A4AE", outline="")
        
        # 脸部深色区域
        canvas.create_polygon(
            x, y-28*s, x-16*s, y-10*s, x-12*s, y+8*s,
            x, y+12*s, x+12*s, y+8*s, x+16*s, y-10*s,
            fill="#78909C", outline="", smooth=True
        )
        
        # ========== 耳朵（半竖立）==========
        canvas.create_polygon(x-20*s, y-20*s, x-30*s, y-52*s, x-24*s, y-54*s, x-10*s, y-22*s,
                             fill="#78909C", outline="#546E7A", width=2, smooth=True)
        canvas.create_polygon(x-18*s, y-22*s, x-26*s, y-46*s, x-22*s, y-48*s, x-12*s, y-24*s,
                             fill="#90A4AE", outline="", smooth=True)
        canvas.create_polygon(x-16*s, y-24*s, x-22*s, y-40*s, x-19*s, y-42*s, x-14*s, y-26*s,
                             fill="#FFB6C1", outline="", smooth=True)
        
        canvas.create_polygon(x+20*s, y-20*s, x+30*s, y-52*s, x+24*s, y-54*s, x+10*s, y-22*s,
                             fill="#78909C", outline="#546E7A", width=2, smooth=True)
        canvas.create_polygon(x+18*s, y-22*s, x+26*s, y-46*s, x+22*s, y-48*s, x+12*s, y-24*s,
                             fill="#90A4AE", outline="", smooth=True)
        canvas.create_polygon(x+16*s, y-24*s, x+22*s, y-40*s, x+19*s, y-42*s, x+14*s, y-26*s,
                             fill="#FFB6C1", outline="", smooth=True)
        
        # ========== 眼睛 ==========
        canvas.create_oval(x-16*s, y-18*s, x-4*s, y-3*s, fill="#78909C", outline="")
        canvas.create_oval(x+4*s, y-18*s, x+16*s, y-3*s, fill="#78909C", outline="")
        canvas.create_oval(x-15*s, y-17*s, x-5*s, y-4*s, fill="white", outline="#333", width=1)
        canvas.create_oval(x+5*s, y-17*s, x+15*s, y-4*s, fill="white", outline="#333", width=1)
        canvas.create_oval(x-13*s, y-15*s, x-7*s, y-6*s, fill="#4E342E", outline="")
        canvas.create_oval(x+7*s, y-15*s, x+13*s, y-6*s, fill="#4E342E", outline="")
        canvas.create_oval(x-11*s, y-13*s, x-9*s, y-9*s, fill="#1a1a1a", outline="")
        canvas.create_oval(x+9*s, y-13*s, x+11*s, y-9*s, fill="#1a1a1a", outline="")
        canvas.create_oval(x-12*s, y-14*s, x-10*s, y-12*s, fill="white", outline="")
        canvas.create_oval(x+10*s, y-14*s, x+12*s, y-12*s, fill="white", outline="")
        
        # ========== 鼻子 ==========
        canvas.create_polygon(x-5*s, y-4*s, x+5*s, y-4*s, x+6*s, y+4*s, x-6*s, y+4*s,
                             fill="#90A4AE", outline="", smooth=True)
        canvas.create_oval(x-8*s, y+2*s, x+8*s, y+14*s, fill="#1a1a1a", outline="#111", width=1)
        canvas.create_oval(x-5*s, y+4*s, x-1*s, y+8*s, fill="#444", outline="")
        
        # ========== 嘴巴 ==========
        canvas.create_oval(x-12*s, y+8*s, x-2*s, y+20*s, fill="#90A4AE", outline="")
        canvas.create_oval(x+2*s, y+8*s, x+12*s, y+20*s, fill="#90A4AE", outline="")
        canvas.create_line(x, y+14*s, x, y+18*s, fill="#333", width=int(2*s)+1)
        canvas.create_arc(x-10*s, y+12*s, x, y+22*s, start=270, extent=70, style="arc", outline="#333", width=int(2*s)+1)
        canvas.create_arc(x, y+12*s, x+10*s, y+22*s, start=200, extent=70, style="arc", outline="#333", width=int(2*s)+1)
        
        # ========== 环保帽（绿色鸭舌帽）==========
        canvas.create_oval(x-30*s, y-38*s, x+30*s, y-26*s, fill="#388E3C", outline="")
        canvas.create_oval(x-28*s, y-36*s, x+28*s, y-24*s, fill="#4CAF50", outline="#388E3C", width=2)
        canvas.create_arc(x-26*s, y-52*s, x+26*s, y-24*s, start=0, extent=180, fill="#66BB6A", outline="#4CAF50", width=2)
        canvas.create_arc(x-22*s, y-48*s, x+22*s, y-30*s, start=20, extent=140, style="arc", outline="#81C784", width=2)
        # 回收标志
        canvas.create_oval(x-8*s, y-46*s, x+8*s, y-32*s, fill="#388E3C", outline="#2E7D32", width=1)
        canvas.create_text(x, y-39*s, text="♻", font=("Segoe UI Emoji", int(9*s)), fill="#C8E6C9")
        
        # 脸颊腮红
        canvas.create_oval(x-20*s, y-2*s, x-12*s, y+6*s, fill="#FFCDD2", outline="")
        canvas.create_oval(x+12*s, y-2*s, x+20*s, y+6*s, fill="#FFCDD2", outline="")
    
    @staticmethod
    def draw_puppy_zuma(canvas, x, y, scale=1.0):
        """路马(Zuma) - 拉布拉多水上救援犬，巧克力棕色，超精细版"""
        s = scale
        
        # === 尾巴（拉布拉多的水獭尾）===
        canvas.create_polygon(
            x+22*s, y+35*s, x+38*s, y+20*s, x+42*s, y+18*s, x+40*s, y+25*s, x+25*s, y+40*s,
            fill="#6D4C41", outline="#5D4037", width=1, smooth=True
        )
        canvas.create_polygon(
            x+25*s, y+36*s, x+36*s, y+22*s, x+38*s, y+24*s, x+28*s, y+38*s,
            fill="#8D6E63", outline="", smooth=True
        )
        
        # === 身体（巧克力棕色多层渐变）===
        canvas.create_oval(x-28*s, y+6*s, x+28*s, y+55*s, fill="#5D4037", outline="#4E342E", width=2)
        canvas.create_oval(x-26*s, y+8*s, x+26*s, y+52*s, fill="#6D4C41", outline="")
        canvas.create_oval(x-22*s, y+12*s, x+22*s, y+48*s, fill="#795548", outline="")
        canvas.create_oval(x-15*s, y+18*s, x+15*s, y+42*s, fill="#8D6E63", outline="")
        # 胸前浅色毛
        canvas.create_oval(x-10*s, y+22*s, x+10*s, y+40*s, fill="#A1887F", outline="")
        
        # === 前腿（肌肉感）===
        canvas.create_polygon(
            x-22*s, y+38*s, x-24*s, y+50*s, x-22*s, y+62*s, x-8*s, y+62*s, x-8*s, y+50*s, x-10*s, y+38*s,
            fill="#6D4C41", outline="#5D4037", width=1, smooth=True
        )
        canvas.create_polygon(
            x+10*s, y+38*s, x+8*s, y+50*s, x+8*s, y+62*s, x+22*s, y+62*s, x+24*s, y+50*s, x+22*s, y+38*s,
            fill="#6D4C41", outline="#5D4037", width=1, smooth=True
        )
        # 腿部高光
        canvas.create_line(x-16*s, y+42*s, x-16*s, y+55*s, fill="#8D6E63", width=2)
        canvas.create_line(x+16*s, y+42*s, x+16*s, y+55*s, fill="#8D6E63", width=2)
        # 爪子
        canvas.create_oval(x-24*s, y+58*s, x-8*s, y+70*s, fill="#5D4037", outline="#4E342E", width=1)
        canvas.create_oval(x+8*s, y+58*s, x+24*s, y+70*s, fill="#5D4037", outline="#4E342E", width=1)
        # 爪垫
        canvas.create_oval(x-20*s, y+62*s, x-12*s, y+68*s, fill="#3E2723", outline="")
        canvas.create_oval(x+12*s, y+62*s, x+20*s, y+68*s, fill="#3E2723", outline="")
        
        # === 头部（拉布拉多宽脸）===
        canvas.create_oval(x-26*s, y-34*s, x+26*s, y+18*s, fill="#6D4C41", outline="#5D4037", width=2)
        canvas.create_oval(x-24*s, y-32*s, x+24*s, y+15*s, fill="#795548", outline="")
        canvas.create_oval(x-20*s, y-28*s, x+20*s, y+12*s, fill="#8D6E63", outline="")
        # 脸部浅色区域
        canvas.create_oval(x-15*s, y-10*s, x+15*s, y+15*s, fill="#A1887F", outline="")
        
        # === 耳朵（下垂的拉布拉多耳朵，带纹理）===
        canvas.create_oval(x-34*s, y-22*s, x-10*s, y+12*s, fill="#5D4037", outline="#4E342E", width=2)
        canvas.create_oval(x+10*s, y-22*s, x+34*s, y+12*s, fill="#5D4037", outline="#4E342E", width=2)
        # 耳朵内层
        canvas.create_oval(x-30*s, y-18*s, x-14*s, y+6*s, fill="#6D4C41", outline="")
        canvas.create_oval(x+14*s, y-18*s, x+30*s, y+6*s, fill="#6D4C41", outline="")
        # 耳朵内侧粉色
        canvas.create_oval(x-26*s, y-12*s, x-18*s, y+0*s, fill="#FFAB91", outline="")
        canvas.create_oval(x+18*s, y-12*s, x+26*s, y+0*s, fill="#FFAB91", outline="")
        
        # === 眉毛区域 ===
        canvas.create_arc(x-16*s, y-22*s, x-4*s, y-14*s, start=0, extent=180, fill="#A1887F", outline="")
        canvas.create_arc(x+4*s, y-22*s, x+16*s, y-14*s, start=0, extent=180, fill="#A1887F", outline="")
        
        # === 眼睛（大而有神）===
        canvas.create_oval(x-15*s, y-17*s, x-3*s, y-3*s, fill="white", outline="#333", width=2)
        canvas.create_oval(x+3*s, y-17*s, x+15*s, y-3*s, fill="white", outline="#333", width=2)
        # 虹膜（温暖的棕色）
        canvas.create_oval(x-12*s, y-14*s, x-5*s, y-5*s, fill="#5D4037", outline="#4E342E", width=1)
        canvas.create_oval(x+5*s, y-14*s, x+12*s, y-5*s, fill="#5D4037", outline="#4E342E", width=1)
        # 瞳孔
        canvas.create_oval(x-10*s, y-12*s, x-7*s, y-8*s, fill="#1a1a1a", outline="")
        canvas.create_oval(x+7*s, y-12*s, x+10*s, y-8*s, fill="#1a1a1a", outline="")
        # 眼睛高光（双高光）
        canvas.create_oval(x-11*s, y-13*s, x-9*s, y-11*s, fill="white", outline="")
        canvas.create_oval(x+8*s, y-13*s, x+10*s, y-11*s, fill="white", outline="")
        canvas.create_oval(x-8*s, y-9*s, x-7*s, y-8*s, fill="white", outline="")
        canvas.create_oval(x+9*s, y-9*s, x+10*s, y-8*s, fill="white", outline="")
        
        # === 鼻子（湿润的大鼻子）===
        canvas.create_oval(x-9*s, y-2*s, x+9*s, y+12*s, fill="#1a1a1a", outline="#0d0d0d", width=1)
        canvas.create_oval(x-7*s, y+0*s, x+7*s, y+10*s, fill="#2d2d2d", outline="")
        # 鼻孔
        canvas.create_oval(x-5*s, y+3*s, x-2*s, y+7*s, fill="#0d0d0d", outline="")
        canvas.create_oval(x+2*s, y+3*s, x+5*s, y+7*s, fill="#0d0d0d", outline="")
        # 鼻子高光
        canvas.create_arc(x-5*s, y+0*s, x+2*s, y+5*s, start=30, extent=120, style="arc", outline="#555", width=2)
        
        # === 嘴巴（开心的笑）===
        canvas.create_arc(x-12*s, y+6*s, x+12*s, y+24*s, start=200, extent=140, style="arc", outline="#333", width=2)
        # 舌头
        canvas.create_oval(x-6*s, y+12*s, x+6*s, y+22*s, fill="#FF6B6B", outline="#E53935", width=1)
        canvas.create_line(x, y+14*s, x, y+20*s, fill="#E53935", width=1)
        
        # === 脸颊腮红 ===
        canvas.create_oval(x-22*s, y-4*s, x-14*s, y+4*s, fill="#FFCCBC", outline="")
        canvas.create_oval(x+14*s, y-4*s, x+22*s, y+4*s, fill="#FFCCBC", outline="")
        
        # === 潜水头盔（橙色，更精细）===
        # 头盔主体
        canvas.create_arc(x-28*s, y-52*s, x+28*s, y-16*s, start=0, extent=180, fill="#F57C00", outline="#E65100", width=2)
        canvas.create_arc(x-26*s, y-50*s, x+26*s, y-18*s, start=0, extent=180, fill="#FF9800", outline="")
        # 头盔边缘
        canvas.create_rectangle(x-26*s, y-34*s, x+26*s, y-26*s, fill="#FF9800", outline="#F57C00", width=1)
        canvas.create_line(x-26*s, y-30*s, x+26*s, y-30*s, fill="#FFB74D", width=2)
        # 护目镜框
        canvas.create_oval(x-20*s, y-46*s, x-2*s, y-28*s, fill="#333", outline="#222", width=2)
        canvas.create_oval(x+2*s, y-46*s, x+20*s, y-28*s, fill="#333", outline="#222", width=2)
        # 护目镜玻璃
        canvas.create_oval(x-18*s, y-44*s, x-4*s, y-30*s, fill="#81D4FA", outline="#29B6F6", width=1)
        canvas.create_oval(x+4*s, y-44*s, x+18*s, y-30*s, fill="#81D4FA", outline="#29B6F6", width=1)
        # 镜片高光
        canvas.create_arc(x-16*s, y-42*s, x-8*s, y-34*s, start=45, extent=90, style="arc", outline="white", width=2)
        canvas.create_arc(x+8*s, y-42*s, x+16*s, y-34*s, start=45, extent=90, style="arc", outline="white", width=2)
        # 护目镜连接带
        canvas.create_rectangle(x-2*s, y-40*s, x+2*s, y-34*s, fill="#333", outline="")
        
        # === 项圈（橙色水上救援）===
        canvas.create_rectangle(x-20*s, y+4*s, x+20*s, y+14*s, fill="#F57C00", outline="#E65100", width=2)
        canvas.create_rectangle(x-18*s, y+6*s, x+18*s, y+12*s, fill="#FF9800", outline="")
        # 项圈徽章（锚标志）
        canvas.create_oval(x-8*s, y+5*s, x+8*s, y+15*s, fill="#FFB74D", outline="#FFA726", width=1)
        canvas.create_text(x, y+10*s, text="⚓", font=("Segoe UI Emoji", int(6*s)), fill="#E65100")
    
    @staticmethod
    def draw_puppy_everest(canvas, x, y, scale=1.0):
        """珠珠(Everest) - 哈士奇雪山救援犬，紫色主题，超精细版"""
        s = scale
        
        # === 尾巴（哈士奇蓬松卷尾）===
        canvas.create_polygon(
            x+20*s, y+30*s, x+35*s, y+15*s, x+42*s, y+8*s, x+40*s, y+18*s, x+30*s, y+28*s, x+25*s, y+35*s,
            fill="#CE93D8", outline="#BA68C8", width=1, smooth=True
        )
        canvas.create_polygon(
            x+22*s, y+28*s, x+32*s, y+16*s, x+36*s, y+14*s, x+34*s, y+20*s, x+26*s, y+32*s,
            fill="white", outline="", smooth=True
        )
        
        # === 身体（紫白渐变）===
        canvas.create_oval(x-28*s, y+6*s, x+28*s, y+55*s, fill="#BA68C8", outline="#AB47BC", width=2)
        canvas.create_oval(x-26*s, y+8*s, x+26*s, y+52*s, fill="#CE93D8", outline="")
        canvas.create_oval(x-22*s, y+12*s, x+22*s, y+48*s, fill="#E1BEE7", outline="")
        # 胸前白毛
        canvas.create_oval(x-15*s, y+18*s, x+15*s, y+45*s, fill="white", outline="")
        canvas.create_oval(x-10*s, y+22*s, x+10*s, y+40*s, fill="#FAFAFA", outline="")
        
        # === 前腿 ===
        canvas.create_polygon(
            x-22*s, y+38*s, x-24*s, y+50*s, x-22*s, y+62*s, x-8*s, y+62*s, x-8*s, y+50*s, x-10*s, y+38*s,
            fill="#CE93D8", outline="#BA68C8", width=1, smooth=True
        )
        canvas.create_polygon(
            x+10*s, y+38*s, x+8*s, y+50*s, x+8*s, y+62*s, x+22*s, y+62*s, x+24*s, y+50*s, x+22*s, y+38*s,
            fill="#CE93D8", outline="#BA68C8", width=1, smooth=True
        )
        # 腿部白色
        canvas.create_line(x-16*s, y+45*s, x-16*s, y+58*s, fill="white", width=3)
        canvas.create_line(x+16*s, y+45*s, x+16*s, y+58*s, fill="white", width=3)
        # 爪子（白色）
        canvas.create_oval(x-24*s, y+58*s, x-8*s, y+70*s, fill="white", outline="#E0E0E0", width=1)
        canvas.create_oval(x+8*s, y+58*s, x+24*s, y+70*s, fill="white", outline="#E0E0E0", width=1)
        # 爪垫
        canvas.create_oval(x-20*s, y+62*s, x-12*s, y+68*s, fill="#FFCDD2", outline="")
        canvas.create_oval(x+12*s, y+62*s, x+20*s, y+68*s, fill="#FFCDD2", outline="")
        
        # === 头部（哈士奇特征脸型）===
        canvas.create_oval(x-26*s, y-34*s, x+26*s, y+18*s, fill="#E1BEE7", outline="#CE93D8", width=2)
        canvas.create_oval(x-24*s, y-32*s, x+24*s, y+15*s, fill="white", outline="")
        # 哈士奇脸部花纹（淡紫色倒三角）
        canvas.create_polygon(
            x, y-30*s, x-14*s, y-8*s, x-10*s, y+10*s, x, y+5*s, x+10*s, y+10*s, x+14*s, y-8*s,
            fill="#CE93D8", outline="", smooth=True
        )
        # 额头花纹
        canvas.create_polygon(
            x, y-28*s, x-8*s, y-15*s, x, y-10*s, x+8*s, y-15*s,
            fill="#BA68C8", outline="", smooth=True
        )
        
        # === 耳朵（竖立的三角形哈士奇耳）===
        canvas.create_polygon(x-24*s, y-22*s, x-28*s, y-55*s, x-8*s, y-18*s, fill="#CE93D8", outline="#BA68C8", width=2)
        canvas.create_polygon(x+24*s, y-22*s, x+28*s, y-55*s, x+8*s, y-18*s, fill="#CE93D8", outline="#BA68C8", width=2)
        # 耳朵内层
        canvas.create_polygon(x-22*s, y-24*s, x-24*s, y-48*s, x-12*s, y-20*s, fill="#E1BEE7", outline="")
        canvas.create_polygon(x+22*s, y-24*s, x+24*s, y-48*s, x+12*s, y-20*s, fill="#E1BEE7", outline="")
        # 耳朵内侧粉色
        canvas.create_polygon(x-20*s, y-26*s, x-21*s, y-42*s, x-14*s, y-22*s, fill="#FFB6C1", outline="")
        canvas.create_polygon(x+20*s, y-26*s, x+21*s, y-42*s, x+14*s, y-22*s, fill="#FFB6C1", outline="")
        
        # === 眼睛（哈士奇标志性蓝眼睛）===
        canvas.create_oval(x-16*s, y-18*s, x-3*s, y-3*s, fill="white", outline="#333", width=2)
        canvas.create_oval(x+3*s, y-18*s, x+16*s, y-3*s, fill="white", outline="#333", width=2)
        # 虹膜（冰蓝色）
        canvas.create_oval(x-13*s, y-15*s, x-5*s, y-5*s, fill="#03A9F4", outline="#0288D1", width=1)
        canvas.create_oval(x+5*s, y-15*s, x+13*s, y-5*s, fill="#03A9F4", outline="#0288D1", width=1)
        # 虹膜渐变
        canvas.create_arc(x-12*s, y-14*s, x-6*s, y-6*s, start=45, extent=180, fill="#29B6F6", outline="")
        canvas.create_arc(x+6*s, y-14*s, x+12*s, y-6*s, start=45, extent=180, fill="#29B6F6", outline="")
        # 瞳孔
        canvas.create_oval(x-11*s, y-13*s, x-8*s, y-9*s, fill="#1a1a1a", outline="")
        canvas.create_oval(x+8*s, y-13*s, x+11*s, y-9*s, fill="#1a1a1a", outline="")
        # 眼睛高光（双高光）
        canvas.create_oval(x-12*s, y-14*s, x-10*s, y-12*s, fill="white", outline="")
        canvas.create_oval(x+9*s, y-14*s, x+11*s, y-12*s, fill="white", outline="")
        canvas.create_oval(x-9*s, y-9*s, x-8*s, y-8*s, fill="white", outline="")
        canvas.create_oval(x+10*s, y-9*s, x+11*s, y-8*s, fill="white", outline="")
        # 睫毛（女孩特征）
        for dx in [-14, -10, -6]:
            canvas.create_line(x+dx*s, y-18*s, x+(dx-2)*s, y-22*s, fill="#333", width=1)
        for dx in [6, 10, 14]:
            canvas.create_line(x+dx*s, y-18*s, x+(dx+2)*s, y-22*s, fill="#333", width=1)
        
        # === 鼻子（小巧的黑鼻子）===
        canvas.create_oval(x-8*s, y-1*s, x+8*s, y+11*s, fill="#1a1a1a", outline="#0d0d0d", width=1)
        canvas.create_oval(x-6*s, y+1*s, x+6*s, y+9*s, fill="#2d2d2d", outline="")
        # 鼻孔
        canvas.create_oval(x-4*s, y+3*s, x-1*s, y+6*s, fill="#0d0d0d", outline="")
        canvas.create_oval(x+1*s, y+3*s, x+4*s, y+6*s, fill="#0d0d0d", outline="")
        # 鼻子高光
        canvas.create_arc(x-4*s, y+1*s, x+2*s, y+5*s, start=30, extent=120, style="arc", outline="#555", width=2)
        
        # === 嘴巴（甜美微笑）===
        canvas.create_arc(x-10*s, y+6*s, x+10*s, y+22*s, start=200, extent=140, style="arc", outline="#333", width=2)
        # 小舌头
        canvas.create_oval(x-4*s, y+12*s, x+4*s, y+18*s, fill="#FF8A80", outline="#FF5252")
        
        # === 脸颊腮红（更明显）===
        canvas.create_oval(x-22*s, y-4*s, x-13*s, y+5*s, fill="#F8BBD9", outline="")
        canvas.create_oval(x+13*s, y-4*s, x+22*s, y+5*s, fill="#F8BBD9", outline="")
        
        # === 雪山帽（青绿色毛线帽，更精细）===
        # 帽子主体
        canvas.create_arc(x-30*s, y-56*s, x+30*s, y-20*s, start=0, extent=180, fill="#00ACC1", outline="#00838F", width=2)
        canvas.create_arc(x-28*s, y-54*s, x+28*s, y-22*s, start=0, extent=180, fill="#26C6DA", outline="")
        # 帽子花纹条纹
        canvas.create_arc(x-26*s, y-48*s, x+26*s, y-28*s, start=0, extent=180, fill="#4DD0E1", outline="")
        canvas.create_line(x-24*s, y-38*s, x+24*s, y-38*s, fill="#00ACC1", width=2)
        canvas.create_line(x-22*s, y-34*s, x+22*s, y-34*s, fill="#00ACC1", width=1)
        # 帽子边缘（毛绒感）
        canvas.create_arc(x-28*s, y-28*s, x+28*s, y-18*s, start=0, extent=180, fill="#80DEEA", outline="#4DD0E1", width=1)
        # 帽子绒球
        canvas.create_oval(x-12*s, y-70*s, x+12*s, y-52*s, fill="#4DD0E1", outline="#26C6DA", width=2)
        canvas.create_oval(x-8*s, y-66*s, x+8*s, y-56*s, fill="#80DEEA", outline="")
        # 绒球高光
        canvas.create_oval(x-4*s, y-64*s, x+2*s, y-60*s, fill="#B2EBF2", outline="")
        
        # === 项圈（青绿色雪山救援）===
        canvas.create_rectangle(x-20*s, y+4*s, x+20*s, y+14*s, fill="#00ACC1", outline="#00838F", width=2)
        canvas.create_rectangle(x-18*s, y+6*s, x+18*s, y+12*s, fill="#26C6DA", outline="")
        # 项圈徽章（雪花）
        canvas.create_oval(x-8*s, y+5*s, x+8*s, y+15*s, fill="#80DEEA", outline="#4DD0E1", width=1)
        canvas.create_text(x, y+10*s, text="❄", font=("Segoe UI Emoji", int(6*s)), fill="#00838F")
    
    @staticmethod
    def draw_puppy_tracker(canvas, x, y, scale=1.0):
        """阿克(Tracker) - 吉娃娃丛林救援犬，棕色，超精细版"""
        s = scale * 0.95
        
        # === 尾巴（吉娃娃卷尾）===
        canvas.create_polygon(
            x+18*s, y+32*s, x+28*s, y+20*s, x+32*s, y+12*s, x+30*s, y+18*s, x+22*s, y+30*s,
            fill="#D2691E", outline="#A0522D", width=1, smooth=True
        )
        canvas.create_polygon(
            x+20*s, y+30*s, x+26*s, y+22*s, x+28*s, y+18*s, x+26*s, y+24*s, x+22*s, y+32*s,
            fill="#DEB887", outline="", smooth=True
        )
        
        # === 身体（小巧的吉娃娃身体）===
        canvas.create_oval(x-24*s, y+8*s, x+24*s, y+50*s, fill="#A0522D", outline="#8B4513", width=2)
        canvas.create_oval(x-22*s, y+10*s, x+22*s, y+48*s, fill="#CD853F", outline="")
        canvas.create_oval(x-18*s, y+14*s, x+18*s, y+44*s, fill="#D2691E", outline="")
        # 胸前浅色毛
        canvas.create_oval(x-12*s, y+18*s, x+12*s, y+40*s, fill="#DEB887", outline="")
        canvas.create_oval(x-8*s, y+22*s, x+8*s, y+36*s, fill="#F5DEB3", outline="")
        
        # === 前腿（细小的吉娃娃腿）===
        canvas.create_polygon(
            x-18*s, y+36*s, x-20*s, y+48*s, x-18*s, y+58*s, x-6*s, y+58*s, x-6*s, y+48*s, x-8*s, y+36*s,
            fill="#D2691E", outline="#A0522D", width=1, smooth=True
        )
        canvas.create_polygon(
            x+8*s, y+36*s, x+6*s, y+48*s, x+6*s, y+58*s, x+18*s, y+58*s, x+20*s, y+48*s, x+18*s, y+36*s,
            fill="#D2691E", outline="#A0522D", width=1, smooth=True
        )
        # 腿部高光
        canvas.create_line(x-12*s, y+40*s, x-12*s, y+52*s, fill="#DEB887", width=2)
        canvas.create_line(x+12*s, y+40*s, x+12*s, y+52*s, fill="#DEB887", width=2)
        # 爪子
        canvas.create_oval(x-20*s, y+54*s, x-6*s, y+64*s, fill="#A0522D", outline="#8B4513", width=1)
        canvas.create_oval(x+6*s, y+54*s, x+20*s, y+64*s, fill="#A0522D", outline="#8B4513", width=1)
        # 爪垫
        canvas.create_oval(x-16*s, y+57*s, x-10*s, y+62*s, fill="#5D4037", outline="")
        canvas.create_oval(x+10*s, y+57*s, x+16*s, y+62*s, fill="#5D4037", outline="")
        
        # === 头部（吉娃娃的苹果头）===
        canvas.create_oval(x-24*s, y-38*s, x+24*s, y+14*s, fill="#CD853F", outline="#A0522D", width=2)
        canvas.create_oval(x-22*s, y-36*s, x+22*s, y+12*s, fill="#D2691E", outline="")
        canvas.create_oval(x-18*s, y-32*s, x+18*s, y+8*s, fill="#DEB887", outline="")
        # 脸部浅色区域
        canvas.create_oval(x-14*s, y-15*s, x+14*s, y+10*s, fill="#F5DEB3", outline="")
        
        # === 耳朵（超大的吉娃娃蝙蝠耳）===
        # 左耳
        canvas.create_polygon(
            x-18*s, y-25*s, x-38*s, y-55*s, x-42*s, y-45*s, x-35*s, y-20*s, x-20*s, y-10*s,
            fill="#D2691E", outline="#A0522D", width=2, smooth=True
        )
        # 右耳
        canvas.create_polygon(
            x+18*s, y-25*s, x+38*s, y-55*s, x+42*s, y-45*s, x+35*s, y-20*s, x+20*s, y-10*s,
            fill="#D2691E", outline="#A0522D", width=2, smooth=True
        )
        # 耳朵内层
        canvas.create_polygon(
            x-20*s, y-22*s, x-34*s, y-48*s, x-36*s, y-42*s, x-30*s, y-20*s, x-22*s, y-12*s,
            fill="#DEB887", outline="", smooth=True
        )
        canvas.create_polygon(
            x+20*s, y-22*s, x+34*s, y-48*s, x+36*s, y-42*s, x+30*s, y-20*s, x+22*s, y-12*s,
            fill="#DEB887", outline="", smooth=True
        )
        # 耳朵内侧粉色
        canvas.create_polygon(
            x-22*s, y-20*s, x-30*s, y-42*s, x-32*s, y-38*s, x-26*s, y-18*s,
            fill="#FFB6C1", outline="", smooth=True
        )
        canvas.create_polygon(
            x+22*s, y-20*s, x+30*s, y-42*s, x+32*s, y-38*s, x+26*s, y-18*s,
            fill="#FFB6C1", outline="", smooth=True
        )
        
        # === 眼睛（吉娃娃的大圆眼）===
        canvas.create_oval(x-15*s, y-18*s, x-3*s, y-4*s, fill="white", outline="#333", width=2)
        canvas.create_oval(x+3*s, y-18*s, x+15*s, y-4*s, fill="white", outline="#333", width=2)
        # 虹膜（深棕色）
        canvas.create_oval(x-12*s, y-15*s, x-5*s, y-6*s, fill="#5D4037", outline="#4E342E", width=1)
        canvas.create_oval(x+5*s, y-15*s, x+12*s, y-6*s, fill="#5D4037", outline="#4E342E", width=1)
        # 瞳孔
        canvas.create_oval(x-10*s, y-13*s, x-7*s, y-9*s, fill="#1a1a1a", outline="")
        canvas.create_oval(x+7*s, y-13*s, x+10*s, y-9*s, fill="#1a1a1a", outline="")
        # 眼睛高光（双高光）
        canvas.create_oval(x-11*s, y-14*s, x-9*s, y-12*s, fill="white", outline="")
        canvas.create_oval(x+8*s, y-14*s, x+10*s, y-12*s, fill="white", outline="")
        canvas.create_oval(x-8*s, y-9*s, x-7*s, y-8*s, fill="white", outline="")
        canvas.create_oval(x+9*s, y-9*s, x+10*s, y-8*s, fill="white", outline="")
        
        # === 眉毛（可爱的小眉毛）===
        canvas.create_arc(x-14*s, y-22*s, x-4*s, y-16*s, start=0, extent=180, fill="#A0522D", outline="")
        canvas.create_arc(x+4*s, y-22*s, x+14*s, y-16*s, start=0, extent=180, fill="#A0522D", outline="")
        
        # === 鼻子（小巧的黑鼻子）===
        canvas.create_oval(x-6*s, y-1*s, x+6*s, y+9*s, fill="#1a1a1a", outline="#0d0d0d", width=1)
        canvas.create_oval(x-4*s, y+1*s, x+4*s, y+7*s, fill="#2d2d2d", outline="")
        # 鼻孔
        canvas.create_oval(x-3*s, y+2*s, x-1*s, y+5*s, fill="#0d0d0d", outline="")
        canvas.create_oval(x+1*s, y+2*s, x+3*s, y+5*s, fill="#0d0d0d", outline="")
        # 鼻子高光
        canvas.create_arc(x-3*s, y+1*s, x+2*s, y+4*s, start=30, extent=120, style="arc", outline="#555", width=1)
        
        # === 嘴巴（开心的笑）===
        canvas.create_arc(x-8*s, y+5*s, x+8*s, y+18*s, start=200, extent=140, style="arc", outline="#333", width=2)
        # 小舌头
        canvas.create_oval(x-3*s, y+10*s, x+3*s, y+16*s, fill="#FF6B6B", outline="#E53935")
        
        # === 脸颊腮红 ===
        canvas.create_oval(x-20*s, y-6*s, x-12*s, y+2*s, fill="#FFCCBC", outline="")
        canvas.create_oval(x+12*s, y-6*s, x+20*s, y+2*s, fill="#FFCCBC", outline="")
        
        # === 丛林帽（绿色探险帽，更精细）===
        # 帽檐
        canvas.create_oval(x-32*s, y-35*s, x+32*s, y-22*s, fill="#2E7D32", outline="#1B5E20", width=2)
        canvas.create_oval(x-30*s, y-33*s, x+30*s, y-24*s, fill="#388E3C", outline="")
        # 帽顶
        canvas.create_arc(x-24*s, y-52*s, x+24*s, y-28*s, start=0, extent=180, fill="#388E3C", outline="#2E7D32", width=2)
        canvas.create_arc(x-22*s, y-50*s, x+22*s, y-30*s, start=0, extent=180, fill="#4CAF50", outline="")
        # 帽子装饰带
        canvas.create_rectangle(x-22*s, y-38*s, x+22*s, y-34*s, fill="#8BC34A", outline="#689F38", width=1)
        # 帽子徽章（树叶）
        canvas.create_oval(x-6*s, y-48*s, x+6*s, y-38*s, fill="#8BC34A", outline="#689F38", width=1)
        canvas.create_text(x, y-43*s, text="🌿", font=("Segoe UI Emoji", int(5*s)), fill="#1B5E20")
        
        # === 项圈（绿色丛林救援）===
        canvas.create_rectangle(x-18*s, y+6*s, x+18*s, y+16*s, fill="#388E3C", outline="#2E7D32", width=2)
        canvas.create_rectangle(x-16*s, y+8*s, x+16*s, y+14*s, fill="#4CAF50", outline="")
        # 项圈徽章
        canvas.create_oval(x-6*s, y+7*s, x+6*s, y+17*s, fill="#8BC34A", outline="#689F38", width=1)
        canvas.create_text(x, y+12*s, text="🐾", font=("Segoe UI Emoji", int(5*s)), fill="#1B5E20")
    
    @staticmethod
    def draw_puppy_rex(canvas, x, y, scale=1.0):
        """小克(Rex) - 恐龙救援犬，棕白色伯恩山犬，超精细版"""
        s = scale
        
        # === 尾巴（伯恩山犬蓬松尾巴）===
        canvas.create_polygon(
            x+22*s, y+35*s, x+38*s, y+22*s, x+45*s, y+15*s, x+42*s, y+25*s, x+28*s, y+40*s,
            fill="#5D4037", outline="#4E342E", width=1, smooth=True
        )
        canvas.create_polygon(
            x+25*s, y+36*s, x+36*s, y+25*s, x+40*s, y+20*s, x+38*s, y+28*s, x+28*s, y+38*s,
            fill="#8D6E63", outline="", smooth=True
        )
        # 尾巴白色尖端
        canvas.create_polygon(
            x+38*s, y+18*s, x+44*s, y+14*s, x+42*s, y+20*s,
            fill="white", outline="", smooth=True
        )
        
        # === 身体（伯恩山犬三色）===
        canvas.create_oval(x-30*s, y+6*s, x+30*s, y+58*s, fill="#4E342E", outline="#3E2723", width=2)
        canvas.create_oval(x-28*s, y+8*s, x+28*s, y+55*s, fill="#5D4037", outline="")
        canvas.create_oval(x-24*s, y+12*s, x+24*s, y+50*s, fill="#6D4C41", outline="")
        # 胸前白毛（伯恩山犬特征）
        canvas.create_oval(x-15*s, y+18*s, x+15*s, y+48*s, fill="#8D6E63", outline="")
        canvas.create_oval(x-12*s, y+22*s, x+12*s, y+44*s, fill="white", outline="")
        canvas.create_oval(x-8*s, y+26*s, x+8*s, y+40*s, fill="#FAFAFA", outline="")
        
        # === 前腿（粗壮的伯恩山犬腿）===
        canvas.create_polygon(
            x-24*s, y+40*s, x-26*s, y+52*s, x-24*s, y+66*s, x-10*s, y+66*s, x-10*s, y+52*s, x-12*s, y+40*s,
            fill="#5D4037", outline="#4E342E", width=1, smooth=True
        )
        canvas.create_polygon(
            x+12*s, y+40*s, x+10*s, y+52*s, x+10*s, y+66*s, x+24*s, y+66*s, x+26*s, y+52*s, x+24*s, y+40*s,
            fill="#5D4037", outline="#4E342E", width=1, smooth=True
        )
        # 腿部高光
        canvas.create_line(x-18*s, y+44*s, x-18*s, y+58*s, fill="#8D6E63", width=2)
        canvas.create_line(x+18*s, y+44*s, x+18*s, y+58*s, fill="#8D6E63", width=2)
        # 爪子（白色袜子）
        canvas.create_oval(x-26*s, y+62*s, x-10*s, y+74*s, fill="white", outline="#E0E0E0", width=1)
        canvas.create_oval(x+10*s, y+62*s, x+26*s, y+74*s, fill="white", outline="#E0E0E0", width=1)
        # 爪垫
        canvas.create_oval(x-22*s, y+66*s, x-14*s, y+72*s, fill="#5D4037", outline="")
        canvas.create_oval(x+14*s, y+66*s, x+22*s, y+72*s, fill="#5D4037", outline="")
        
        # === 头部（伯恩山犬宽脸）===
        canvas.create_oval(x-28*s, y-38*s, x+28*s, y+20*s, fill="#5D4037", outline="#4E342E", width=2)
        canvas.create_oval(x-26*s, y-36*s, x+26*s, y+18*s, fill="#6D4C41", outline="")
        # 脸部花纹（伯恩山犬特征）
        canvas.create_oval(x-20*s, y-18*s, x+20*s, y+16*s, fill="#8D6E63", outline="")
        # 白色倒三角
        canvas.create_polygon(x, y-28*s, x-10*s, y-8*s, x+10*s, y-8*s, fill="white", outline="")
        canvas.create_polygon(x, y-25*s, x-6*s, y-10*s, x+6*s, y-10*s, fill="#FAFAFA", outline="")
        # 鼻梁白线
        canvas.create_polygon(x-4*s, y-8*s, x, y+5*s, x+4*s, y-8*s, fill="white", outline="", smooth=True)
        
        # === 耳朵（下垂的三角耳）===
        canvas.create_polygon(
            x-26*s, y-20*s, x-38*s, y-8*s, x-32*s, y+18*s, x-18*s, y+8*s,
            fill="#5D4037", outline="#4E342E", width=2, smooth=True
        )
        canvas.create_polygon(
            x+26*s, y-20*s, x+38*s, y-8*s, x+32*s, y+18*s, x+18*s, y+8*s,
            fill="#5D4037", outline="#4E342E", width=2, smooth=True
        )
        # 耳朵内层
        canvas.create_polygon(
            x-24*s, y-16*s, x-32*s, y-4*s, x-28*s, y+12*s, x-20*s, y+4*s,
            fill="#6D4C41", outline="", smooth=True
        )
        canvas.create_polygon(
            x+24*s, y-16*s, x+32*s, y-4*s, x+28*s, y+12*s, x+20*s, y+4*s,
            fill="#6D4C41", outline="", smooth=True
        )
        # 耳朵内侧粉色
        canvas.create_polygon(
            x-22*s, y-10*s, x-28*s, y+0*s, x-26*s, y+8*s, x-20*s, y+2*s,
            fill="#FFAB91", outline="", smooth=True
        )
        canvas.create_polygon(
            x+22*s, y-10*s, x+28*s, y+0*s, x+26*s, y+8*s, x+20*s, y+2*s,
            fill="#FFAB91", outline="", smooth=True
        )
        
        # === 眼睛（温柔的大眼睛）===
        canvas.create_oval(x-16*s, y-17*s, x-4*s, y-3*s, fill="white", outline="#333", width=2)
        canvas.create_oval(x+4*s, y-17*s, x+16*s, y-3*s, fill="white", outline="#333", width=2)
        # 虹膜（深棕色）
        canvas.create_oval(x-13*s, y-14*s, x-6*s, y-5*s, fill="#4E342E", outline="#3E2723", width=1)
        canvas.create_oval(x+6*s, y-14*s, x+13*s, y-5*s, fill="#4E342E", outline="#3E2723", width=1)
        # 瞳孔
        canvas.create_oval(x-11*s, y-12*s, x-8*s, y-8*s, fill="#1a1a1a", outline="")
        canvas.create_oval(x+8*s, y-12*s, x+11*s, y-8*s, fill="#1a1a1a", outline="")
        # 眼睛高光（双高光）
        canvas.create_oval(x-12*s, y-13*s, x-10*s, y-11*s, fill="white", outline="")
        canvas.create_oval(x+9*s, y-13*s, x+11*s, y-11*s, fill="white", outline="")
        canvas.create_oval(x-9*s, y-8*s, x-8*s, y-7*s, fill="white", outline="")
        canvas.create_oval(x+10*s, y-8*s, x+11*s, y-7*s, fill="white", outline="")
        
        # === 眉毛（棕色眉毛斑点）===
        canvas.create_oval(x-15*s, y-22*s, x-6*s, y-16*s, fill="#A1887F", outline="")
        canvas.create_oval(x+6*s, y-22*s, x+15*s, y-16*s, fill="#A1887F", outline="")
        
        # === 鼻子（大黑鼻子）===
        canvas.create_oval(x-9*s, y-2*s, x+9*s, y+12*s, fill="#1a1a1a", outline="#0d0d0d", width=1)
        canvas.create_oval(x-7*s, y+0*s, x+7*s, y+10*s, fill="#2d2d2d", outline="")
        # 鼻孔
        canvas.create_oval(x-5*s, y+3*s, x-2*s, y+7*s, fill="#0d0d0d", outline="")
        canvas.create_oval(x+2*s, y+3*s, x+5*s, y+7*s, fill="#0d0d0d", outline="")
        # 鼻子高光
        canvas.create_arc(x-5*s, y+0*s, x+2*s, y+5*s, start=30, extent=120, style="arc", outline="#555", width=2)
        
        # === 嘴巴（友善的笑）===
        canvas.create_arc(x-12*s, y+6*s, x+12*s, y+24*s, start=200, extent=140, style="arc", outline="#333", width=2)
        # 舌头
        canvas.create_oval(x-5*s, y+12*s, x+5*s, y+20*s, fill="#FF6B6B", outline="#E53935", width=1)
        canvas.create_line(x, y+14*s, x, y+18*s, fill="#E53935", width=1)
        
        # === 脸颊腮红 ===
        canvas.create_oval(x-24*s, y-4*s, x-15*s, y+5*s, fill="#FFCCBC", outline="")
        canvas.create_oval(x+15*s, y-4*s, x+24*s, y+5*s, fill="#FFCCBC", outline="")
        
        # === 恐龙头盔（绿色圆顶+小角，更精细）===
        # 头盔主体
        canvas.create_arc(x-30*s, y-54*s, x+30*s, y-18*s, start=0, extent=180, fill="#558B2F", outline="#33691E", width=2)
        canvas.create_arc(x-28*s, y-52*s, x+28*s, y-20*s, start=0, extent=180, fill="#7CB342", outline="")
        # 头盔高光
        canvas.create_arc(x-24*s, y-48*s, x+24*s, y-28*s, start=20, extent=140, fill="#8BC34A", outline="")
        # 恐龙小角（三个圆润的角）
        canvas.create_oval(x-20*s, y-62*s, x-8*s, y-48*s, fill="#8BC34A", outline="#7CB342", width=2)
        canvas.create_oval(x-6*s, y-68*s, x+6*s, y-52*s, fill="#9CCC65", outline="#8BC34A", width=2)
        canvas.create_oval(x+8*s, y-62*s, x+20*s, y-48*s, fill="#8BC34A", outline="#7CB342", width=2)
        # 角的高光
        canvas.create_oval(x-16*s, y-58*s, x-12*s, y-52*s, fill="#C5E1A5", outline="")
        canvas.create_oval(x-2*s, y-64*s, x+2*s, y-58*s, fill="#DCEDC8", outline="")
        canvas.create_oval(x+12*s, y-58*s, x+16*s, y-52*s, fill="#C5E1A5", outline="")
        # 头盔边缘
        canvas.create_rectangle(x-28*s, y-26*s, x+28*s, y-20*s, fill="#689F38", outline="#558B2F", width=1)
        
        # === 项圈（绿色恐龙救援）===
        canvas.create_rectangle(x-22*s, y+4*s, x+22*s, y+16*s, fill="#689F38", outline="#558B2F", width=2)
        canvas.create_rectangle(x-20*s, y+6*s, x+20*s, y+14*s, fill="#7CB342", outline="")
        # 项圈徽章（恐龙脚印）
        canvas.create_oval(x-8*s, y+5*s, x+8*s, y+17*s, fill="#AED581", outline="#9CCC65", width=1)
        canvas.create_text(x, y+11*s, text="🦖", font=("Segoe UI Emoji", int(6*s)), fill="#33691E")
    
    @staticmethod
    def draw_puppy_liberty(canvas, x, y, scale=1.0):
        """乐乐(Liberty) - 腊肠犬城市救援犬，紫色主题，超精细版"""
        s = scale
        
        # === 尾巴（腊肠犬细长尾巴）===
        canvas.create_polygon(
            x+26*s, y+32*s, x+38*s, y+25*s, x+45*s, y+20*s, x+42*s, y+28*s, x+30*s, y+36*s,
            fill="#8D6E63", outline="#6D4C41", width=1, smooth=True
        )
        canvas.create_polygon(
            x+28*s, y+32*s, x+36*s, y+26*s, x+40*s, y+24*s, x+38*s, y+30*s, x+32*s, y+35*s,
            fill="#A1887F", outline="", smooth=True
        )
        
        # === 身体（腊肠犬身体长）===
        canvas.create_oval(x-32*s, y+8*s, x+32*s, y+52*s, fill="#6D4C41", outline="#5D4037", width=2)
        canvas.create_oval(x-30*s, y+10*s, x+30*s, y+50*s, fill="#8D6E63", outline="")
        canvas.create_oval(x-26*s, y+14*s, x+26*s, y+46*s, fill="#A1887F", outline="")
        # 胸前浅色毛
        canvas.create_oval(x-18*s, y+20*s, x+18*s, y+44*s, fill="#BCAAA4", outline="")
        canvas.create_oval(x-12*s, y+24*s, x+12*s, y+40*s, fill="#D7CCC8", outline="")
        
        # === 前腿（短腿腊肠犬特征）===
        canvas.create_polygon(
            x-24*s, y+38*s, x-26*s, y+50*s, x-24*s, y+62*s, x-12*s, y+62*s, x-12*s, y+50*s, x-14*s, y+38*s,
            fill="#8D6E63", outline="#6D4C41", width=1, smooth=True
        )
        canvas.create_polygon(
            x+14*s, y+38*s, x+12*s, y+50*s, x+12*s, y+62*s, x+24*s, y+62*s, x+26*s, y+50*s, x+24*s, y+38*s,
            fill="#8D6E63", outline="#6D4C41", width=1, smooth=True
        )
        # 腿部高光
        canvas.create_line(x-18*s, y+42*s, x-18*s, y+56*s, fill="#A1887F", width=2)
        canvas.create_line(x+18*s, y+42*s, x+18*s, y+56*s, fill="#A1887F", width=2)
        # 爪子
        canvas.create_oval(x-26*s, y+58*s, x-12*s, y+68*s, fill="#6D4C41", outline="#5D4037", width=1)
        canvas.create_oval(x+12*s, y+58*s, x+26*s, y+68*s, fill="#6D4C41", outline="#5D4037", width=1)
        # 爪垫
        canvas.create_oval(x-22*s, y+61*s, x-16*s, y+66*s, fill="#4E342E", outline="")
        canvas.create_oval(x+16*s, y+61*s, x+22*s, y+66*s, fill="#4E342E", outline="")
        
        # === 头部（腊肠犬长脸）===
        canvas.create_oval(x-24*s, y-35*s, x+24*s, y+18*s, fill="#8D6E63", outline="#6D4C41", width=2)
        canvas.create_oval(x-22*s, y-33*s, x+22*s, y+15*s, fill="#A1887F", outline="")
        canvas.create_oval(x-18*s, y-28*s, x+18*s, y+12*s, fill="#BCAAA4", outline="")
        # 脸部浅色区域
        canvas.create_oval(x-14*s, y-15*s, x+14*s, y+10*s, fill="#D7CCC8", outline="")
        
        # === 耳朵（长长的下垂耳朵，腊肠犬特征）===
        canvas.create_oval(x-34*s, y-24*s, x-8*s, y+18*s, fill="#6D4C41", outline="#5D4037", width=2)
        canvas.create_oval(x+8*s, y-24*s, x+34*s, y+18*s, fill="#6D4C41", outline="#5D4037", width=2)
        # 耳朵内层
        canvas.create_oval(x-30*s, y-20*s, x-12*s, y+12*s, fill="#8D6E63", outline="")
        canvas.create_oval(x+12*s, y-20*s, x+30*s, y+12*s, fill="#8D6E63", outline="")
        # 耳朵内侧粉色
        canvas.create_oval(x-26*s, y-14*s, x-16*s, y+4*s, fill="#FFAB91", outline="")
        canvas.create_oval(x+16*s, y-14*s, x+26*s, y+4*s, fill="#FFAB91", outline="")
        # 耳朵纹理
        canvas.create_arc(x-28*s, y-16*s, x-14*s, y+6*s, start=45, extent=90, style="arc", outline="#A1887F", width=1)
        canvas.create_arc(x+14*s, y-16*s, x+28*s, y+6*s, start=45, extent=90, style="arc", outline="#A1887F", width=1)
        
        # === 眼睛（大而有神的女孩眼睛）===
        canvas.create_oval(x-16*s, y-20*s, x-4*s, y-6*s, fill="white", outline="#333", width=2)
        canvas.create_oval(x+4*s, y-20*s, x+16*s, y-6*s, fill="white", outline="#333", width=2)
        # 虹膜（深棕色）
        canvas.create_oval(x-13*s, y-17*s, x-6*s, y-8*s, fill="#5D4037", outline="#4E342E", width=1)
        canvas.create_oval(x+6*s, y-17*s, x+13*s, y-8*s, fill="#5D4037", outline="#4E342E", width=1)
        # 瞳孔
        canvas.create_oval(x-11*s, y-15*s, x-8*s, y-11*s, fill="#1a1a1a", outline="")
        canvas.create_oval(x+8*s, y-15*s, x+11*s, y-11*s, fill="#1a1a1a", outline="")
        # 眼睛高光（双高光）
        canvas.create_oval(x-12*s, y-16*s, x-10*s, y-14*s, fill="white", outline="")
        canvas.create_oval(x+9*s, y-16*s, x+11*s, y-14*s, fill="white", outline="")
        canvas.create_oval(x-9*s, y-11*s, x-8*s, y-10*s, fill="white", outline="")
        canvas.create_oval(x+10*s, y-11*s, x+11*s, y-10*s, fill="white", outline="")
        # 睫毛（女孩特征，更精细）
        for dx in [-14, -11, -8]:
            canvas.create_line(x+dx*s, y-20*s, x+(dx-2)*s, y-25*s, fill="#333", width=1)
            canvas.create_line(x+dx*s, y-20*s, x+(dx-1)*s, y-24*s, fill="#333", width=1)
        for dx in [8, 11, 14]:
            canvas.create_line(x+dx*s, y-20*s, x+(dx+2)*s, y-25*s, fill="#333", width=1)
            canvas.create_line(x+dx*s, y-20*s, x+(dx+1)*s, y-24*s, fill="#333", width=1)
        
        # === 眉毛（可爱的小眉毛）===
        canvas.create_arc(x-15*s, y-25*s, x-5*s, y-19*s, start=0, extent=180, fill="#8D6E63", outline="")
        canvas.create_arc(x+5*s, y-25*s, x+15*s, y-19*s, start=0, extent=180, fill="#8D6E63", outline="")
        
        # === 鼻子（小巧可爱）===
        canvas.create_oval(x-7*s, y-3*s, x+7*s, y+9*s, fill="#1a1a1a", outline="#0d0d0d", width=1)
        canvas.create_oval(x-5*s, y-1*s, x+5*s, y+7*s, fill="#2d2d2d", outline="")
        # 鼻孔
        canvas.create_oval(x-4*s, y+1*s, x-1*s, y+4*s, fill="#0d0d0d", outline="")
        canvas.create_oval(x+1*s, y+1*s, x+4*s, y+4*s, fill="#0d0d0d", outline="")
        # 鼻子高光
        canvas.create_arc(x-4*s, y-1*s, x+2*s, y+3*s, start=30, extent=120, style="arc", outline="#555", width=2)
        
        # === 嘴巴（甜美微笑）===
        canvas.create_arc(x-10*s, y+4*s, x+10*s, y+18*s, start=200, extent=140, style="arc", outline="#333", width=2)
        # 小舌头
        canvas.create_oval(x-4*s, y+10*s, x+4*s, y+16*s, fill="#FF8A80", outline="#FF5252")
        
        # === 脸颊腮红（更明显的粉色）===
        canvas.create_oval(x-22*s, y-6*s, x-13*s, y+3*s, fill="#F8BBD9", outline="")
        canvas.create_oval(x+13*s, y-6*s, x+22*s, y+3*s, fill="#F8BBD9", outline="")
        
        # === 紫色头巾/帽子（城市风格，更精细）===
        # 帽子主体
        canvas.create_arc(x-26*s, y-50*s, x+26*s, y-16*s, start=0, extent=180, fill="#7B1FA2", outline="#6A1B9A", width=2)
        canvas.create_arc(x-24*s, y-48*s, x+24*s, y-18*s, start=0, extent=180, fill="#9C27B0", outline="")
        # 帽子高光
        canvas.create_arc(x-20*s, y-44*s, x+20*s, y-24*s, start=20, extent=140, fill="#AB47BC", outline="")
        # 帽子装饰带
        canvas.create_rectangle(x-22*s, y-28*s, x+22*s, y-22*s, fill="#CE93D8", outline="#BA68C8", width=1)
        # 城市图案装饰
        canvas.create_oval(x-10*s, y-46*s, x+10*s, y-32*s, fill="#BA68C8", outline="#9C27B0", width=1)
        # 城市天际线
        canvas.create_rectangle(x-7*s, y-44*s, x-4*s, y-35*s, fill="#E1BEE7", outline="")
        canvas.create_rectangle(x-2*s, y-42*s, x+1*s, y-35*s, fill="#E1BEE7", outline="")
        canvas.create_rectangle(x+3*s, y-44*s, x+6*s, y-35*s, fill="#E1BEE7", outline="")
        # 小窗户
        canvas.create_rectangle(x-6*s, y-42*s, x-5*s, y-40*s, fill="#F3E5F5", outline="")
        canvas.create_rectangle(x-1*s, y-40*s, x+0*s, y-38*s, fill="#F3E5F5", outline="")
        canvas.create_rectangle(x+4*s, y-42*s, x+5*s, y-40*s, fill="#F3E5F5", outline="")
        
        # === 项圈（紫色城市救援）===
        canvas.create_rectangle(x-20*s, y+4*s, x+20*s, y+14*s, fill="#7B1FA2", outline="#6A1B9A", width=2)
        canvas.create_rectangle(x-18*s, y+6*s, x+18*s, y+12*s, fill="#9C27B0", outline="")
        # 项圈徽章（城市标志）
        canvas.create_oval(x-8*s, y+5*s, x+8*s, y+15*s, fill="#CE93D8", outline="#BA68C8", width=1)
        canvas.create_text(x, y+10*s, text="🏙", font=("Segoe UI Emoji", int(5*s)), fill="#4A148C")
    
    @staticmethod
    def draw_ryder(canvas, x, y, scale=1.0):
        """莱德 - 汪汪队队长，10岁男孩"""
        s = scale
        
        # === 身体（蓝色背心）===
        canvas.create_oval(x-20*s, y+18*s, x+20*s, y+58*s, fill="#1976D2", outline="#1565C0", width=2)
        # 背心V领
        canvas.create_polygon(
            x-8*s, y+18*s, x, y+35*s, x+8*s, y+18*s,
            fill="white", outline=""
        )
        
        # === 腿 ===
        canvas.create_rectangle(x-10*s, y+52*s, x-3*s, y+75*s, fill="#5D4037", outline="#4E342E")
        canvas.create_rectangle(x+3*s, y+52*s, x+10*s, y+75*s, fill="#5D4037", outline="#4E342E")
        # 鞋子
        canvas.create_oval(x-13*s, y+70*s, x-1*s, y+80*s, fill="#333", outline="")
        canvas.create_oval(x+1*s, y+70*s, x+13*s, y+80*s, fill="#333", outline="")
        
        # === 手臂 ===
        canvas.create_line(x-20*s, y+28*s, x-28*s, y+45*s, fill="#1976D2", width=int(8*s))
        canvas.create_line(x+20*s, y+28*s, x+28*s, y+45*s, fill="#1976D2", width=int(8*s))
        # 手
        canvas.create_oval(x-32*s, y+42*s, x-24*s, y+52*s, fill="#FFCC80", outline="#FFB74D")
        canvas.create_oval(x+24*s, y+42*s, x+32*s, y+52*s, fill="#FFCC80", outline="#FFB74D")
        
        # === 头部 ===
        canvas.create_oval(x-18*s, y-30*s, x+18*s, y+15*s, fill="#FFCC80", outline="#FFB74D", width=2)
        
        # === 头发（棕色，蓬松）===
        canvas.create_arc(x-20*s, y-42*s, x+20*s, y-8*s, start=0, extent=180, fill="#5D4037", outline="#4E342E", width=2)
        # 刘海
        canvas.create_oval(x-15*s, y-38*s, x-2*s, y-22*s, fill="#5D4037", outline="")
        canvas.create_oval(x-8*s, y-40*s, x+8*s, y-25*s, fill="#5D4037", outline="")
        canvas.create_oval(x+2*s, y-36*s, x+15*s, y-22*s, fill="#5D4037", outline="")

        # === 眼睛 ===
        canvas.create_oval(x-12*s, y-15*s, x-4*s, y-5*s, fill="white", outline="#333", width=1)
        canvas.create_oval(x+4*s, y-15*s, x+12*s, y-5*s, fill="white", outline="#333", width=1)
        canvas.create_oval(x-10*s, y-13*s, x-6*s, y-7*s, fill="#5D4037", outline="")
        canvas.create_oval(x+6*s, y-13*s, x+10*s, y-7*s, fill="#5D4037", outline="")
        canvas.create_oval(x-9*s, y-12*s, x-8*s, y-10*s, fill="white", outline="")
        canvas.create_oval(x+7*s, y-12*s, x+8*s, y-10*s, fill="white", outline="")
        
        # === 眉毛 ===
        canvas.create_line(x-12*s, y-18*s, x-5*s, y-17*s, fill="#4E342E", width=2)
        canvas.create_line(x+5*s, y-17*s, x+12*s, y-18*s, fill="#4E342E", width=2)
        
        # === 鼻子 ===
        canvas.create_oval(x-3*s, y-4*s, x+3*s, y+2*s, fill="#FFB74D", outline="")
        
        # === 嘴巴（自信的微笑）===
        canvas.create_arc(x-8*s, y-2*s, x+8*s, y+10*s, start=200, extent=140, style="arc", outline="#333", width=2)
        
        # === 耳朵 ===
        canvas.create_oval(x-22*s, y-12*s, x-16*s, y+2*s, fill="#FFCC80", outline="#FFB74D")
        canvas.create_oval(x+16*s, y-12*s, x+22*s, y+2*s, fill="#FFCC80", outline="#FFB74D")
        
        # === Pup Pad 通讯器 ===
        canvas.create_rectangle(x-12*s, y+15*s, x+12*s, y+22*s, fill="#1565C0", outline="#0D47A1", width=2)
        canvas.create_rectangle(x-6*s, y+16*s, x+6*s, y+21*s, fill="#4CAF50", outline="")
    
    # ==================== 场景元素 ====================
    
    @staticmethod
    def draw_lookout_tower(canvas, x, y, scale=1.0):
        """瞭望塔 - 更精细版"""
        s = scale
        
        # === 塔基 ===
        canvas.create_polygon(
            x-50*s, y+120*s, x-35*s, y+30*s, x+35*s, y+30*s, x+50*s, y+120*s,
            fill="#90CAF9", outline="#64B5F6", width=2
        )
        # 塔身窗户
        for wy in [50, 80]:
            for wx in [-15, 15]:
                canvas.create_oval(x+wx*s-8*s, y+wy*s-8*s, x+wx*s+8*s, y+wy*s+8*s,
                                  fill="#E3F2FD", outline="#64B5F6", width=2)
        
        # === 观察台 ===
        canvas.create_oval(x-55*s, y-5*s, x+55*s, y+40*s, fill="#1976D2", outline="#1565C0", width=3)
        # 玻璃窗
        canvas.create_arc(x-45*s, y+5*s, x+45*s, y+35*s, start=0, extent=180,
                         fill="#E3F2FD", outline="#90CAF9", width=2)
        
        # === 圆顶 ===
        canvas.create_arc(x-45*s, y-55*s, x+45*s, y+10*s, start=0, extent=180,
                         fill="#F44336", outline="#D32F2F", width=3)
        # 顶部装饰
        canvas.create_oval(x-8*s, y-55*s, x+8*s, y-45*s, fill="#FFEB3B", outline="#FBC02D", width=2)
        
        # === 旗杆和旗帜 ===
        canvas.create_line(x, y-55*s, x, y-95*s, fill="#5D4037", width=3)
        # 旗帜
        canvas.create_polygon(
            x, y-95*s, x+30*s, y-85*s, x, y-75*s,
            fill="#F44336", outline="#D32F2F", width=2
        )
        # 爪印图案
        ThemeDrawings._draw_mini_paw(canvas, x+15*s, y-85*s, 8*s)
        
        # === 门 ===
        canvas.create_arc(x-15*s, y+90*s, x+15*s, y+120*s, start=0, extent=180,
                         fill="#5D4037", outline="#4E342E", width=2)

    @staticmethod
    def draw_paw_badge(canvas, x, y, size=60):
        """汪汪队徽章"""
        s = size / 60
        
        # 外圈
        canvas.create_oval(x-30*s, y-30*s, x+30*s, y+30*s, fill="#1976D2", outline="#1565C0", width=3)
        # 内圈
        canvas.create_oval(x-25*s, y-25*s, x+25*s, y+25*s, fill="#2196F3", outline="")
        
        # 爪印
        # 主掌
        canvas.create_oval(x-14*s, y-3*s, x+14*s, y+22*s, fill="white", outline="")
        # 四个脚趾
        positions = [(-14, -12), (-5, -20), (5, -20), (14, -12)]
        for dx, dy in positions:
            canvas.create_oval(x+dx*s-7*s, y+dy*s-7*s, x+dx*s+7*s, y+dy*s+7*s, fill="white", outline="")
    
    @staticmethod
    def draw_bone(canvas, x, y, size=50):
        """骨头"""
        s = size / 50
        
        # 骨头主体
        canvas.create_rectangle(x-18*s, y-6*s, x+18*s, y+6*s, fill="#FFF8E1", outline="#FFE082", width=2)
        
        # 两端的圆球
        for dx in [-18, 18]:
            canvas.create_oval(x+dx*s-10*s, y-10*s, x+dx*s+10*s, y+10*s, fill="#FFF8E1", outline="#FFE082", width=2)
        
        # 高光
        canvas.create_line(x-10*s, y-3*s, x+10*s, y-3*s, fill="white", width=2)
    
    @staticmethod
    def draw_star(canvas, x, y, size=35, color="#FFD700"):
        """星星"""
        s = size / 35
        points = []
        for i in range(5):
            angle = math.radians(90 + i * 72)
            points.extend([x + 17*s * math.cos(angle), y - 17*s * math.sin(angle)])
            angle = math.radians(90 + i * 72 + 36)
            points.extend([x + 7*s * math.cos(angle), y - 7*s * math.sin(angle)])
        
        canvas.create_polygon(points, fill=color, outline="#FFA000", width=2)
        # 高光
        canvas.create_polygon(
            x-3*s, y-5*s, x, y-12*s, x+3*s, y-5*s,
            fill="#FFECB3", outline=""
        )
    
    # ==================== 汪汪队载具 ====================
    
    @staticmethod
    def draw_chase_car(canvas, x, y, scale=1.0):
        """阿奇的警车"""
        s = scale
        # 车身
        canvas.create_rectangle(x-40*s, y-10*s, x+40*s, y+20*s, fill="#1976D2", outline="#1565C0", width=2)
        # 车顶
        canvas.create_rectangle(x-25*s, y-30*s, x+25*s, y-10*s, fill="#1976D2", outline="#1565C0", width=2)
        # 车窗
        canvas.create_rectangle(x-22*s, y-27*s, x+22*s, y-12*s, fill="#81D4FA", outline="#29B6F6", width=2)
        # 警灯
        canvas.create_rectangle(x-8*s, y-38*s, x+8*s, y-30*s, fill="#F44336", outline="#D32F2F", width=2)
        canvas.create_oval(x-6*s, y-36*s, x-2*s, y-32*s, fill="#FF8A80", outline="")
        canvas.create_oval(x+2*s, y-36*s, x+6*s, y-32*s, fill="#82B1FF", outline="")
        # 车轮
        canvas.create_oval(x-35*s, y+12*s, x-18*s, y+30*s, fill="#333", outline="#222", width=2)
        canvas.create_oval(x+18*s, y+12*s, x+35*s, y+30*s, fill="#333", outline="#222", width=2)
        canvas.create_oval(x-30*s, y+16*s, x-23*s, y+26*s, fill="#666", outline="")
        canvas.create_oval(x+23*s, y+16*s, x+30*s, y+26*s, fill="#666", outline="")
        # 爪印标志
        ThemeDrawings._draw_mini_paw(canvas, x, y+5*s, 10*s)
    
    @staticmethod
    def draw_marshall_truck(canvas, x, y, scale=1.0):
        """毛毛的消防车"""
        s = scale
        # 车身
        canvas.create_rectangle(x-45*s, y-8*s, x+45*s, y+22*s, fill="#F44336", outline="#D32F2F", width=2)
        # 驾驶室
        canvas.create_rectangle(x+20*s, y-28*s, x+45*s, y-8*s, fill="#F44336", outline="#D32F2F", width=2)
        # 车窗
        canvas.create_rectangle(x+23*s, y-25*s, x+42*s, y-10*s, fill="#81D4FA", outline="#29B6F6", width=2)
        # 梯子
        canvas.create_rectangle(x-40*s, y-20*s, x+15*s, y-15*s, fill="#FFD54F", outline="#FFC107", width=2)
        # 警灯
        canvas.create_oval(x+30*s, y-35*s, x+40*s, y-28*s, fill="#F44336", outline="#D32F2F", width=2)
        # 车轮
        canvas.create_oval(x-38*s, y+14*s, x-20*s, y+32*s, fill="#333", outline="#222", width=2)
        canvas.create_oval(x-5*s, y+14*s, x+13*s, y+32*s, fill="#333", outline="#222", width=2)
        canvas.create_oval(x+25*s, y+14*s, x+43*s, y+32*s, fill="#333", outline="#222", width=2)
        # 119标志
        canvas.create_oval(x-25*s, y-2*s, x-5*s, y+15*s, fill="white", outline="#D32F2F", width=2)
        canvas.create_text(x-15*s, y+6*s, text="119", font=("Arial", int(6*s), "bold"), fill="#D32F2F")
    
    @staticmethod
    def draw_skye_helicopter(canvas, x, y, scale=1.0):
        """天天的直升机"""
        s = scale
        # 机身
        canvas.create_oval(x-30*s, y-10*s, x+25*s, y+25*s, fill="#EC407A", outline="#D81B60", width=2)
        # 机尾
        canvas.create_polygon(x+20*s, y+5*s, x+55*s, y-5*s, x+55*s, y+10*s, x+20*s, y+15*s,
                             fill="#EC407A", outline="#D81B60", width=2)
        # 尾翼
        canvas.create_polygon(x+50*s, y-15*s, x+55*s, y-5*s, x+60*s, y-5*s, x+55*s, y-20*s,
                             fill="#F48FB1", outline="#EC407A", width=2)
        # 驾驶舱玻璃
        canvas.create_oval(x-20*s, y-5*s, x+10*s, y+18*s, fill="#81D4FA", outline="#29B6F6", width=2)
        # 起落架
        canvas.create_line(x-15*s, y+25*s, x-20*s, y+35*s, fill="#333", width=int(3*s))
        canvas.create_line(x+10*s, y+25*s, x+15*s, y+35*s, fill="#333", width=int(3*s))
        canvas.create_line(x-25*s, y+35*s, x+20*s, y+35*s, fill="#333", width=int(3*s))
        # 螺旋桨
        canvas.create_oval(x-5*s, y-18*s, x+5*s, y-12*s, fill="#666", outline="#333", width=2)
        canvas.create_polygon(x-45*s, y-16*s, x, y-14*s, x+45*s, y-16*s, x, y-18*s,
                             fill="#90A4AE", outline="#607D8B", width=1)
    
    @staticmethod
    def draw_rubble_bulldozer(canvas, x, y, scale=1.0):
        """小砾的挖掘机"""
        s = scale
        # 履带
        canvas.create_rectangle(x-40*s, y+10*s, x+40*s, y+30*s, fill="#333", outline="#222", width=2)
        canvas.create_oval(x-42*s, y+8*s, x-30*s, y+32*s, fill="#333", outline="#222", width=2)
        canvas.create_oval(x+30*s, y+8*s, x+42*s, y+32*s, fill="#333", outline="#222", width=2)
        # 车身
        canvas.create_rectangle(x-30*s, y-15*s, x+30*s, y+12*s, fill="#FFC107", outline="#FFA000", width=2)
        # 驾驶室
        canvas.create_rectangle(x-10*s, y-35*s, x+25*s, y-15*s, fill="#FFC107", outline="#FFA000", width=2)
        canvas.create_rectangle(x-7*s, y-32*s, x+22*s, y-17*s, fill="#81D4FA", outline="#29B6F6", width=2)
        # 铲斗臂
        canvas.create_polygon(x-30*s, y-10*s, x-50*s, y-25*s, x-45*s, y-30*s, x-25*s, y-15*s,
                             fill="#FF8F00", outline="#E65100", width=2)
        # 铲斗
        canvas.create_polygon(x-55*s, y-35*s, x-45*s, y-25*s, x-55*s, y-15*s, x-65*s, y-25*s,
                             fill="#FF8F00", outline="#E65100", width=2)
    
    @staticmethod
    def draw_rocky_truck(canvas, x, y, scale=1.0):
        """灰灰的回收车"""
        s = scale
        # 车身
        canvas.create_rectangle(x-40*s, y-5*s, x+40*s, y+22*s, fill="#4CAF50", outline="#388E3C", width=2)
        # 驾驶室
        canvas.create_rectangle(x+15*s, y-25*s, x+40*s, y-5*s, fill="#4CAF50", outline="#388E3C", width=2)
        canvas.create_rectangle(x+18*s, y-22*s, x+37*s, y-7*s, fill="#81D4FA", outline="#29B6F6", width=2)
        # 回收箱
        canvas.create_rectangle(x-38*s, y-30*s, x+12*s, y-5*s, fill="#66BB6A", outline="#4CAF50", width=2)
        # 回收标志
        canvas.create_text(x-13*s, y-17*s, text="♻", font=("Segoe UI Emoji", int(12*s)), fill="white")
        # 机械臂
        canvas.create_rectangle(x-42*s, y-20*s, x-38*s, y+5*s, fill="#78909C", outline="#546E7A", width=2)
        canvas.create_rectangle(x-50*s, y-25*s, x-38*s, y-18*s, fill="#78909C", outline="#546E7A", width=2)
        # 车轮
        canvas.create_oval(x-35*s, y+15*s, x-18*s, y+32*s, fill="#333", outline="#222", width=2)
        canvas.create_oval(x+18*s, y+15*s, x+35*s, y+32*s, fill="#333", outline="#222", width=2)
        canvas.create_oval(x-30*s, y+19*s, x-23*s, y+28*s, fill="#666", outline="")
        canvas.create_oval(x+23*s, y+19*s, x+30*s, y+28*s, fill="#666", outline="")
    
    @staticmethod
    def draw_zuma_hovercraft(canvas, x, y, scale=1.0):
        """路马的气垫船"""
        s = scale
        # 气垫底部
        canvas.create_oval(x-45*s, y+10*s, x+45*s, y+35*s, fill="#FFB74D", outline="#FF9800", width=2)
        canvas.create_oval(x-40*s, y+15*s, x+40*s, y+30*s, fill="#FFA726", outline="")
        # 船身
        canvas.create_oval(x-38*s, y-15*s, x+38*s, y+18*s, fill="#FF9800", outline="#F57C00", width=2)
        # 驾驶舱
        canvas.create_oval(x-20*s, y-25*s, x+20*s, y+5*s, fill="#81D4FA", outline="#29B6F6", width=2)
        # 风扇罩
        canvas.create_oval(x+20*s, y-20*s, x+45*s, y+10*s, fill="#FF9800", outline="#F57C00", width=2)
        # 风扇
        canvas.create_oval(x+25*s, y-15*s, x+40*s, y+5*s, fill="#333", outline="#222", width=2)
        canvas.create_line(x+32*s, y-12*s, x+32*s, y+2*s, fill="#666", width=2)
        canvas.create_line(x+27*s, y-5*s, x+38*s, y-5*s, fill="#666", width=2)
        # 爪印
        ThemeDrawings._draw_mini_paw(canvas, x-5*s, y-5*s, 8*s)
    
    @staticmethod
    def draw_everest_snowcat(canvas, x, y, scale=1.0):
        """珠珠的雪地车"""
        s = scale
        # 履带
        canvas.create_rectangle(x-42*s, y+8*s, x+42*s, y+28*s, fill="#333", outline="#222", width=2)
        canvas.create_oval(x-44*s, y+6*s, x-30*s, y+30*s, fill="#333", outline="#222", width=2)
        canvas.create_oval(x+30*s, y+6*s, x+44*s, y+30*s, fill="#333", outline="#222", width=2)
        # 车身
        canvas.create_rectangle(x-35*s, y-12*s, x+35*s, y+10*s, fill="#26C6DA", outline="#00ACC1", width=2)
        # 驾驶室
        canvas.create_rectangle(x-15*s, y-35*s, x+30*s, y-12*s, fill="#26C6DA", outline="#00ACC1", width=2)
        canvas.create_rectangle(x-12*s, y-32*s, x+27*s, y-14*s, fill="#81D4FA", outline="#29B6F6", width=2)
        # 雪铲
        canvas.create_polygon(x-35*s, y-5*s, x-55*s, y+5*s, x-55*s, y+15*s, x-35*s, y+8*s,
                             fill="#4DD0E1", outline="#00ACC1", width=2)
        # 警灯
        canvas.create_oval(x+5*s, y-42*s, x+15*s, y-35*s, fill="#26C6DA", outline="#00ACC1", width=2)
        # 爪印
        ThemeDrawings._draw_mini_paw(canvas, x+10*s, y-2*s, 8*s)
    
    @staticmethod
    def draw_tracker_jeep(canvas, x, y, scale=1.0):
        """阿克的吉普车"""
        s = scale
        # 车身
        canvas.create_rectangle(x-38*s, y-8*s, x+38*s, y+18*s, fill="#4CAF50", outline="#388E3C", width=2)
        # 车顶框架
        canvas.create_line(x-30*s, y-8*s, x-30*s, y-28*s, fill="#795548", width=int(3*s))
        canvas.create_line(x+30*s, y-8*s, x+30*s, y-28*s, fill="#795548", width=int(3*s))
        canvas.create_line(x-32*s, y-28*s, x+32*s, y-28*s, fill="#795548", width=int(3*s))
        # 帆布顶
        canvas.create_rectangle(x-30*s, y-28*s, x+30*s, y-8*s, fill="#8D6E63", outline="")
        # 挡风玻璃
        canvas.create_rectangle(x-25*s, y-25*s, x+25*s, y-10*s, fill="#81D4FA", outline="#29B6F6", width=2)
        # 前保险杠
        canvas.create_rectangle(x-40*s, y+15*s, x+40*s, y+22*s, fill="#333", outline="#222", width=2)
        # 车轮（大轮子）
        canvas.create_oval(x-38*s, y+12*s, x-18*s, y+32*s, fill="#333", outline="#222", width=2)
        canvas.create_oval(x+18*s, y+12*s, x+38*s, y+32*s, fill="#333", outline="#222", width=2)
        canvas.create_oval(x-32*s, y+17*s, x-24*s, y+27*s, fill="#666", outline="")
        canvas.create_oval(x+24*s, y+17*s, x+32*s, y+27*s, fill="#666", outline="")
        # 前灯
        canvas.create_oval(x-35*s, y+2*s, x-28*s, y+10*s, fill="#FFEB3B", outline="#FBC02D", width=1)
        canvas.create_oval(x+28*s, y+2*s, x+35*s, y+10*s, fill="#FFEB3B", outline="#FBC02D", width=1)
    
    @staticmethod
    def draw_rex_dinosaur_car(canvas, x, y, scale=1.0):
        """小克的恐龙车"""
        s = scale
        # 履带
        canvas.create_rectangle(x-40*s, y+10*s, x+40*s, y+28*s, fill="#333", outline="#222", width=2)
        canvas.create_oval(x-42*s, y+8*s, x-28*s, y+30*s, fill="#333", outline="#222", width=2)
        canvas.create_oval(x+28*s, y+8*s, x+42*s, y+30*s, fill="#333", outline="#222", width=2)
        # 车身（恐龙形状）
        canvas.create_oval(x-30*s, y-15*s, x+25*s, y+15*s, fill="#7CB342", outline="#558B2F", width=2)
        # 恐龙头
        canvas.create_oval(x+15*s, y-30*s, x+50*s, y+0*s, fill="#8BC34A", outline="#689F38", width=2)
        # 恐龙眼睛
        canvas.create_oval(x+35*s, y-25*s, x+45*s, y-15*s, fill="white", outline="#333", width=1)
        canvas.create_oval(x+38*s, y-22*s, x+42*s, y-18*s, fill="#333", outline="")
        # 恐龙嘴
        canvas.create_arc(x+30*s, y-15*s, x+50*s, y+5*s, start=300, extent=60, style="arc", outline="#558B2F", width=2)
        # 恐龙角/背刺
        for dx in [-20, -5, 10]:
            canvas.create_polygon(x+dx*s, y-15*s, x+dx*s+5*s, y-28*s, x+dx*s+10*s, y-15*s,
                                 fill="#9CCC65", outline="#7CB342", width=1)
        # 驾驶舱
        canvas.create_oval(x-20*s, y-20*s, x+10*s, y+5*s, fill="#81D4FA", outline="#29B6F6", width=2)
        # 尾巴
        canvas.create_polygon(x-30*s, y-5*s, x-50*s, y-15*s, x-50*s, y+5*s, x-30*s, y+5*s,
                             fill="#7CB342", outline="#558B2F", width=2)
    
    @staticmethod
    def draw_liberty_motorcycle(canvas, x, y, scale=1.0):
        """乐乐的摩托车"""
        s = scale
        # 车身
        canvas.create_polygon(x-25*s, y-5*s, x+20*s, y-5*s, x+25*s, y+10*s, x-20*s, y+10*s,
                             fill="#9C27B0", outline="#7B1FA2", width=2)
        # 座椅
        canvas.create_oval(x-15*s, y-15*s, x+10*s, y-2*s, fill="#7B1FA2", outline="#6A1B9A", width=2)
        # 车头
        canvas.create_polygon(x+20*s, y-10*s, x+40*s, y-5*s, x+40*s, y+5*s, x+25*s, y+10*s,
                             fill="#9C27B0", outline="#7B1FA2", width=2)
        # 车灯
        canvas.create_oval(x+35*s, y-8*s, x+42*s, y+2*s, fill="#FFEB3B", outline="#FBC02D", width=1)
        # 把手
        canvas.create_line(x+25*s, y-15*s, x+30*s, y-5*s, fill="#333", width=int(3*s))
        canvas.create_line(x+22*s, y-18*s, x+28*s, y-18*s, fill="#333", width=int(3*s))
        # 后视镜
        canvas.create_oval(x+20*s, y-22*s, x+26*s, y-16*s, fill="#81D4FA", outline="#333", width=1)
        # 车轮
        canvas.create_oval(x-30*s, y+5*s, x-10*s, y+25*s, fill="#333", outline="#222", width=2)
        canvas.create_oval(x+15*s, y+5*s, x+35*s, y+25*s, fill="#333", outline="#222", width=2)
        # 轮毂
        canvas.create_oval(x-24*s, y+10*s, x-16*s, y+20*s, fill="#BA68C8", outline="")
        canvas.create_oval(x+21*s, y+10*s, x+29*s, y+20*s, fill="#BA68C8", outline="")
        # 爪印
        ThemeDrawings._draw_mini_paw(canvas, x, y+2*s, 7*s)
    
    # ==================== 汪汪队场景背景 ====================
    
    @staticmethod
    def draw_adventure_bay(canvas, x, y, width, height):
        """冒险湾海滩背景"""
        # 天空渐变
        for i in range(int(height * 0.6)):
            ratio = i / (height * 0.6)
            r = int(135 + ratio * 50)
            g = int(206 + ratio * 30)
            b = 235
            canvas.create_line(x, y + i, x + width, y + i, fill=f"#{r:02x}{g:02x}{b:02x}")
        
        # 大海
        sea_y = y + int(height * 0.6)
        canvas.create_rectangle(x, sea_y, x + width, y + int(height * 0.75), fill="#4FC3F7", outline="")
        # 海浪
        for i in range(0, int(width), 40):
            canvas.create_arc(x + i, sea_y - 5, x + i + 40, sea_y + 15, 
                            start=0, extent=180, fill="#81D4FA", outline="")
        
        # 沙滩
        canvas.create_rectangle(x, y + int(height * 0.75), x + width, y + height, fill="#FFE082", outline="")
    
    @staticmethod
    def draw_snowy_mountain(canvas, x, y, width, height):
        """雪山背景"""
        # 天空
        canvas.create_rectangle(x, y, x + width, y + int(height * 0.5), fill="#B3E5FC", outline="")
        # 雪山
        mountain_y = y + int(height * 0.3)
        canvas.create_polygon(x, mountain_y + 80, x + width * 0.3, mountain_y, 
                             x + width * 0.5, mountain_y + 60, fill="#E0E0E0", outline="")
        canvas.create_polygon(x + width * 0.4, mountain_y + 80, x + width * 0.7, mountain_y - 20,
                             x + width, mountain_y + 50, fill="#ECEFF1", outline="")
        # 雪地
        canvas.create_rectangle(x, y + int(height * 0.6), x + width, y + height, fill="white", outline="")
    
    @staticmethod
    def draw_jungle(canvas, x, y, width, height):
        """丛林背景"""
        # 天空
        canvas.create_rectangle(x, y, x + width, y + int(height * 0.4), fill="#81C784", outline="")
        # 丛林
        canvas.create_rectangle(x, y + int(height * 0.3), x + width, y + height, fill="#4CAF50", outline="")
        # 树木
        for i in range(0, int(width), 80):
            tree_x = x + i + 40
            tree_y = y + int(height * 0.5)
            canvas.create_rectangle(tree_x - 8, tree_y, tree_x + 8, tree_y + 60, fill="#795548", outline="#5D4037", width=2)
            canvas.create_oval(tree_x - 35, tree_y - 50, tree_x + 35, tree_y + 20, fill="#2E7D32", outline="#1B5E20", width=2)
        # 地面
        canvas.create_rectangle(x, y + int(height * 0.85), x + width, y + height, fill="#5D4037", outline="")
    
    # ==================== 汪汪队装饰元素 ====================
    
    @staticmethod
    def draw_dog_bowl(canvas, x, y, scale=1.0):
        """狗粮碗"""
        s = scale
        canvas.create_oval(x-25*s, y-5*s, x+25*s, y+15*s, fill="#1976D2", outline="#1565C0", width=2)
        canvas.create_oval(x-20*s, y-8*s, x+20*s, y+8*s, fill="#2196F3", outline="")
        for dx, dy in [(-8, -2), (0, -4), (8, -2), (-4, 0), (4, 0)]:
            canvas.create_oval(x+dx*s-4*s, y+dy*s-3*s, x+dx*s+4*s, y+dy*s+3*s, fill="#8D6E63", outline="#6D4C41")
    
    @staticmethod
    def draw_dog_house(canvas, x, y, scale=1.0):
        """狗窝"""
        s = scale
        canvas.create_rectangle(x-30*s, y-10*s, x+30*s, y+40*s, fill="#F44336", outline="#D32F2F", width=2)
        canvas.create_polygon(x-35*s, y-10*s, x, y-40*s, x+35*s, y-10*s, fill="#D32F2F", outline="#B71C1C", width=2)
        canvas.create_arc(x-15*s, y+5*s, x+15*s, y+40*s, start=0, extent=180, fill="#5D4037", outline="#4E342E", width=2)
        canvas.create_rectangle(x-15*s, y+22*s, x+15*s, y+40*s, fill="#5D4037", outline="")
        ThemeDrawings._draw_mini_paw(canvas, x, y-20*s, 8*s)
    
    @staticmethod
    def draw_medal(canvas, x, y, scale=1.0):
        """奖牌"""
        s = scale
        canvas.create_polygon(x-15*s, y-30*s, x-5*s, y-30*s, x-10*s, y-5*s, fill="#1976D2", outline="#1565C0", width=1)
        canvas.create_polygon(x+5*s, y-30*s, x+15*s, y-30*s, x+10*s, y-5*s, fill="#1976D2", outline="#1565C0", width=1)
        canvas.create_oval(x-18*s, y-10*s, x+18*s, y+25*s, fill="#FFD700", outline="#FFA000", width=3)
        canvas.create_oval(x-14*s, y-6*s, x+14*s, y+21*s, fill="#FFEB3B", outline="")
        ThemeDrawings._draw_mini_star(canvas, x, y+7*s, 10*s, "#FFA000")
    
    @staticmethod
    def draw_balloon(canvas, x, y, scale=1.0, color="#F44336"):
        """气球"""
        s = scale
        canvas.create_oval(x-15*s, y-35*s, x+15*s, y+5*s, fill=color, outline="")
        canvas.create_oval(x-10*s, y-30*s, x-3*s, y-18*s, fill="white", outline="")
        canvas.create_polygon(x-3*s, y+3*s, x+3*s, y+3*s, x, y+10*s, fill=color, outline="")
        canvas.create_line(x, y+10*s, x+5*s, y+40*s, fill="#666", width=1)
    
    @staticmethod
    def draw_flag(canvas, x, y, scale=1.0):
        """汪汪队旗帜"""
        s = scale
        canvas.create_line(x, y, x, y+60*s, fill="#795548", width=int(4*s))
        canvas.create_polygon(x, y, x+40*s, y+12*s, x, y+24*s, fill="#F44336", outline="#D32F2F", width=2)
        ThemeDrawings._draw_mini_paw(canvas, x+20*s, y+12*s, 8*s)
        canvas.create_oval(x-4*s, y-8*s, x+4*s, y, fill="#FFD700", outline="#FFA000", width=2)
    
    @staticmethod
    def draw_treat(canvas, x, y, scale=1.0):
        """狗狗零食"""
        s = scale
        canvas.create_oval(x-18*s, y-8*s, x-8*s, y+8*s, fill="#D2691E", outline="#A0522D", width=2)
        canvas.create_rectangle(x-13*s, y-5*s, x+13*s, y+5*s, fill="#D2691E", outline="")
        canvas.create_oval(x+8*s, y-8*s, x+18*s, y+8*s, fill="#D2691E", outline="#A0522D", width=2)
    
    @staticmethod
    def draw_pup_tag(canvas, x, y, scale=1.0, color="#1976D2"):
        """狗狗徽章/项圈牌"""
        s = scale
        canvas.create_polygon(x, y-25*s, x-20*s, y, x-12*s, y+20*s, x+12*s, y+20*s, x+20*s, y,
                             fill=color, outline="", smooth=False)
        canvas.create_oval(x-12*s, y-8*s, x+12*s, y+15*s, fill="white", outline="")
        ThemeDrawings._draw_mini_paw(canvas, x, y+3*s, 8*s)


# ==================== 测试函数 ====================

def test_drawings():
    """测试所有汪汪队绘图"""
    import tkinter as tk
    
    root = tk.Tk()
    root.title("🐕 汪汪队主题素材展示")
    root.geometry("1600x1000")
    
    canvas = tk.Canvas(root, width=1600, height=1000, bg="#87CEEB")
    canvas.pack()
    
    # 绘制草地
    canvas.create_rectangle(0, 700, 1500, 1000, fill="#81C784", outline="")
    canvas.create_rectangle(0, 700, 1500, 715, fill="#66BB6A", outline="")
    
    # 标题
    canvas.create_text(750, 35, text="🐕 汪汪队主题素材库", font=("微软雅黑", 24, "bold"), fill="#1565C0")
    
    # === 第一排：6个狗狗 ===
    canvas.create_text(50, 65, text="【狗狗角色】", font=("微软雅黑", 11, "bold"), fill="#333", anchor="w")
    y1 = 170
    spacing = 110
    start_x = 80
    
    ThemeDrawings.draw_puppy_chase(canvas, start_x, y1, 0.85)
    canvas.create_text(start_x, y1+75, text="阿奇", font=("微软雅黑", 9), fill="#1565C0")
    
    ThemeDrawings.draw_puppy_marshall(canvas, start_x + spacing, y1, 0.85)
    canvas.create_text(start_x + spacing, y1+75, text="毛毛", font=("微软雅黑", 9), fill="#D32F2F")
    
    ThemeDrawings.draw_puppy_skye(canvas, start_x + spacing*2, y1, 0.85)
    canvas.create_text(start_x + spacing*2, y1+75, text="天天", font=("微软雅黑", 9), fill="#EC407A")
    
    ThemeDrawings.draw_puppy_rubble(canvas, start_x + spacing*3, y1, 0.85)
    canvas.create_text(start_x + spacing*3, y1+75, text="小砾", font=("微软雅黑", 9), fill="#FFA000")
    
    ThemeDrawings.draw_puppy_rocky(canvas, start_x + spacing*4, y1, 0.85)
    canvas.create_text(start_x + spacing*4, y1+75, text="灰灰", font=("微软雅黑", 9), fill="#546E7A")
    
    ThemeDrawings.draw_puppy_zuma(canvas, start_x + spacing*5, y1, 0.85)
    canvas.create_text(start_x + spacing*5, y1+75, text="路马", font=("微软雅黑", 9), fill="#FF9800")
    
    ThemeDrawings.draw_puppy_everest(canvas, start_x + spacing*6, y1, 0.85)
    canvas.create_text(start_x + spacing*6, y1+75, text="珠珠", font=("微软雅黑", 9), fill="#00BCD4")
    
    ThemeDrawings.draw_puppy_tracker(canvas, start_x + spacing*7, y1, 0.85)
    canvas.create_text(start_x + spacing*7, y1+75, text="阿克", font=("微软雅黑", 9), fill="#4CAF50")
    
    ThemeDrawings.draw_puppy_rex(canvas, start_x + spacing*8, y1, 0.85)
    canvas.create_text(start_x + spacing*8, y1+75, text="小克", font=("微软雅黑", 9), fill="#8BC34A")
    
    ThemeDrawings.draw_puppy_liberty(canvas, start_x + spacing*9, y1, 0.85)
    canvas.create_text(start_x + spacing*9, y1+75, text="乐乐", font=("微软雅黑", 9), fill="#9C27B0")
    
    ThemeDrawings.draw_ryder(canvas, start_x + spacing*10, y1-5, 0.9)
    canvas.create_text(start_x + spacing*10, y1+75, text="莱德", font=("微软雅黑", 9), fill="#1976D2")
    
    # === 第二排：所有载具 ===
    canvas.create_text(50, 260, text="【载具】", font=("微软雅黑", 11, "bold"), fill="#333", anchor="w")
    y2 = 340
    v_spacing = 150
    
    ThemeDrawings.draw_chase_car(canvas, 100, y2, 0.7)
    canvas.create_text(100, y2+45, text="警车", font=("微软雅黑", 9), fill="#666")
    
    ThemeDrawings.draw_marshall_truck(canvas, 100 + v_spacing, y2, 0.65)
    canvas.create_text(100 + v_spacing, y2+45, text="消防车", font=("微软雅黑", 9), fill="#666")
    
    ThemeDrawings.draw_skye_helicopter(canvas, 100 + v_spacing*2, y2-10, 0.65)
    canvas.create_text(100 + v_spacing*2, y2+45, text="直升机", font=("微软雅黑", 9), fill="#666")
    
    ThemeDrawings.draw_rubble_bulldozer(canvas, 100 + v_spacing*3, y2, 0.65)
    canvas.create_text(100 + v_spacing*3, y2+45, text="挖掘机", font=("微软雅黑", 9), fill="#666")
    
    ThemeDrawings.draw_rocky_truck(canvas, 100 + v_spacing*4, y2, 0.65)
    canvas.create_text(100 + v_spacing*4, y2+45, text="回收车", font=("微软雅黑", 9), fill="#666")
    
    ThemeDrawings.draw_zuma_hovercraft(canvas, 100 + v_spacing*5, y2, 0.65)
    canvas.create_text(100 + v_spacing*5, y2+45, text="气垫船", font=("微软雅黑", 9), fill="#666")
    
    ThemeDrawings.draw_everest_snowcat(canvas, 100 + v_spacing*6, y2, 0.65)
    canvas.create_text(100 + v_spacing*6, y2+45, text="雪地车", font=("微软雅黑", 9), fill="#666")
    
    ThemeDrawings.draw_tracker_jeep(canvas, 100 + v_spacing*7, y2, 0.65)
    canvas.create_text(100 + v_spacing*7, y2+45, text="吉普车", font=("微软雅黑", 9), fill="#666")
    
    ThemeDrawings.draw_rex_dinosaur_car(canvas, 100 + v_spacing*8, y2, 0.65)
    canvas.create_text(100 + v_spacing*8, y2+45, text="恐龙车", font=("微软雅黑", 9), fill="#666")
    
    ThemeDrawings.draw_liberty_motorcycle(canvas, 100 + v_spacing*9, y2, 0.7)
    canvas.create_text(100 + v_spacing*9, y2+45, text="摩托车", font=("微软雅黑", 9), fill="#666")
    
    # === 第三排：场景和装饰 ===
    canvas.create_text(50, 410, text="【场景】", font=("微软雅黑", 11, "bold"), fill="#333", anchor="w")
    
    ThemeDrawings.draw_lookout_tower(canvas, 150, 550, 0.65)
    canvas.create_text(150, 670, text="瞭望塔", font=("微软雅黑", 9), fill="#666")
    
    ThemeDrawings.draw_dog_house(canvas, 300, 580, 1.0)
    canvas.create_text(300, 640, text="狗窝", font=("微软雅黑", 9), fill="#666")
    
    # === 装饰元素 ===
    canvas.create_text(400, 410, text="【装饰】", font=("微软雅黑", 11, "bold"), fill="#333", anchor="w")
    
    dec_y = 480
    ThemeDrawings.draw_paw_badge(canvas, 450, dec_y, 45)
    canvas.create_text(450, dec_y+40, text="徽章", font=("微软雅黑", 9), fill="#666")
    
    ThemeDrawings.draw_bone(canvas, 530, dec_y, 40)
    canvas.create_text(530, dec_y+40, text="骨头", font=("微软雅黑", 9), fill="#666")
    
    ThemeDrawings.draw_star(canvas, 610, dec_y-5, 30)
    canvas.create_text(610, dec_y+40, text="星星", font=("微软雅黑", 9), fill="#666")
    
    ThemeDrawings.draw_medal(canvas, 690, dec_y+5, 0.9)
    canvas.create_text(690, dec_y+50, text="奖牌", font=("微软雅黑", 9), fill="#666")
    
    ThemeDrawings.draw_flag(canvas, 770, dec_y-20, 0.7)
    canvas.create_text(770, dec_y+40, text="旗帜", font=("微软雅黑", 9), fill="#666")
    
    ThemeDrawings.draw_balloon(canvas, 830, dec_y+10, 0.9, "#F44336")
    ThemeDrawings.draw_balloon(canvas, 860, dec_y, 0.7, "#2196F3")
    ThemeDrawings.draw_balloon(canvas, 890, dec_y+15, 0.8, "#FFEB3B")
    canvas.create_text(860, dec_y+55, text="气球", font=("微软雅黑", 9), fill="#666")
    
    ThemeDrawings.draw_dog_bowl(canvas, 970, dec_y+10, 0.9)
    canvas.create_text(970, dec_y+45, text="狗粮碗", font=("微软雅黑", 9), fill="#666")
    
    ThemeDrawings.draw_treat(canvas, 1060, dec_y+10, 0.9)
    canvas.create_text(1060, dec_y+45, text="零食", font=("微软雅黑", 9), fill="#666")
    
    ThemeDrawings.draw_pup_tag(canvas, 1150, dec_y+10, 0.9, "#1976D2")
    canvas.create_text(1150, dec_y+55, text="项圈牌", font=("微软雅黑", 9), fill="#666")
    
    # === 场景背景预览 ===
    canvas.create_text(400, 560, text="【背景预览】", font=("微软雅黑", 11, "bold"), fill="#333", anchor="w")
    
    # 冒险湾
    ThemeDrawings.draw_adventure_bay(canvas, 450, 590, 200, 100)
    canvas.create_text(550, 700, text="冒险湾", font=("微软雅黑", 9), fill="#666")
    
    # 雪山
    ThemeDrawings.draw_snowy_mountain(canvas, 680, 590, 200, 100)
    canvas.create_text(780, 700, text="雪山", font=("微软雅黑", 9), fill="#666")
    
    # 丛林
    ThemeDrawings.draw_jungle(canvas, 910, 590, 200, 100)
    canvas.create_text(1010, 700, text="丛林", font=("微软雅黑", 9), fill="#666")
    
    # 底部说明
    canvas.create_text(800, 970, text="汪汪队主题素材库 - 纯Canvas绘制，无需图片资源 | 共11个角色 + 10个载具 + 场景背景 + 装饰元素", 
                      font=("微软雅黑", 10), fill="#666")
    
    root.mainloop()


if __name__ == "__main__":
    test_drawings()


if __name__ == "__main__":
    test_drawings()


if __name__ == "__main__":
    test_drawings()
