# -*- coding: utf-8 -*-
"""
汪汪队主题辅助模块
提供角色绘制、反馈显示等通用功能
"""

import tkinter as tk
import random

try:
    from theme_drawings import ThemeDrawings
    from theme_config import THEME, ThemeHelper
    THEME_AVAILABLE = True
except ImportError:
    THEME_AVAILABLE = False

# 汪汪队角色列表
PAW_CHARACTERS = [
    ("chase", "阿奇", "#1976D2", "警察狗"),
    ("marshall", "毛毛", "#F44336", "消防狗"),
    ("skye", "天天", "#EC407A", "飞行狗"),
    ("rubble", "小砾", "#FFC107", "工程狗"),
    ("rocky", "灰灰", "#78909C", "环保狗"),
    ("zuma", "路马", "#FF9800", "水上狗"),
    ("everest", "珠珠", "#00BCD4", "雪山狗"),
    ("tracker", "阿克", "#4CAF50", "丛林狗"),
    ("rex", "小克", "#8BC34A", "恐龙狗"),
    ("liberty", "乐乐", "#9C27B0", "城市狗"),
]

# 角色绘制函数映射
def get_draw_func(char_id):
    """获取角色绘制函数"""
    if not THEME_AVAILABLE:
        return None
    char_map = {
        "chase": ThemeDrawings.draw_puppy_chase,
        "marshall": ThemeDrawings.draw_puppy_marshall,
        "skye": ThemeDrawings.draw_puppy_skye,
        "rubble": ThemeDrawings.draw_puppy_rubble,
        "rocky": ThemeDrawings.draw_puppy_rocky,
        "zuma": ThemeDrawings.draw_puppy_zuma,
        "everest": ThemeDrawings.draw_puppy_everest,
        "tracker": ThemeDrawings.draw_puppy_tracker,
        "rex": ThemeDrawings.draw_puppy_rex,
        "liberty": ThemeDrawings.draw_puppy_liberty,
    }
    return char_map.get(char_id)

def get_random_character():
    """获取随机角色"""
    return random.choice(PAW_CHARACTERS)

def draw_random_character(canvas, x, y, scale=0.7):
    """在Canvas上绘制随机角色，返回角色名"""
    if not THEME_AVAILABLE:
        return None
    char_id, char_name, _, _ = get_random_character()
    draw_func = get_draw_func(char_id)
    if draw_func:
        draw_func(canvas, x, y, scale)
        return char_name
    return None

def draw_character_by_id(canvas, char_id, x, y, scale=0.7):
    """根据ID绘制指定角色"""
    if not THEME_AVAILABLE:
        return False
    draw_func = get_draw_func(char_id)
    if draw_func:
        draw_func(canvas, x, y, scale)
        return True
    return False


class PawFeedback:
    """汪汪队反馈显示类"""
    
    def __init__(self, parent):
        self.parent = parent
        self.popup = None
    
    def show_praise(self, message=None):
        """显示表扬反馈"""
        self._show_feedback(True, message)
    
    def show_encourage(self, message=None):
        """显示鼓励反馈"""
        self._show_feedback(False, message)
    
    def _show_feedback(self, is_correct, message=None):
        """显示反馈弹窗"""
        if not THEME_AVAILABLE:
            return
        
        # 关闭之前的弹窗
        if self.popup:
            try:
                self.popup.destroy()
            except:
                pass
        
        char_id, char_name, char_color, _ = get_random_character()
        draw_func = get_draw_func(char_id)
        if not draw_func:
            return
        
        self.popup = tk.Toplevel(self.parent)
        self.popup.overrideredirect(True)
        self.popup.attributes('-topmost', True)
        
        w, h = 260, 200
        x = self.parent.winfo_x() + (self.parent.winfo_width() - w) // 2
        y = self.parent.winfo_y() + (self.parent.winfo_height() - h) // 2
        self.popup.geometry(f"{w}x{h}+{x}+{y}")
        
        bg_color = "#E8F5E9" if is_correct else "#FFEBEE"
        self.popup.configure(bg=bg_color)
        
        canvas = tk.Canvas(self.popup, width=240, height=130, bg=bg_color, highlightthickness=0)
        canvas.pack(pady=10)
        draw_func(canvas, 120, 65, 0.85)
        
        if is_correct:
            text_color = "#4CAF50"
            default_msg = f"{char_name}说：太棒了！🎉"
        else:
            text_color = "#FF9800"
            default_msg = f"{char_name}说：再试一次！💪"
        
        tk.Label(self.popup, text=message or default_msg, font=("微软雅黑", 11, "bold"),
                bg=bg_color, fg=text_color).pack(pady=5)
        
        self.popup.after(1800, self._close_popup)
    
    def _close_popup(self):
        if self.popup:
            try:
                self.popup.destroy()
            except:
                pass
            self.popup = None


def create_title_with_paw(parent, title, subtitle="", bg_color="#E3F2FD"):
    """创建带汪汪队装饰的标题"""
    if not THEME_AVAILABLE:
        frame = tk.Frame(parent, bg=bg_color)
        tk.Label(frame, text=title, font=("微软雅黑", 24, "bold"), bg=bg_color, fg="#1565C0").pack()
        if subtitle:
            tk.Label(frame, text=subtitle, font=("微软雅黑", 11), bg=bg_color, fg="#666").pack()
        return frame
    
    frame = tk.Frame(parent, bg=bg_color)
    canvas = tk.Canvas(frame, width=600, height=70, bg=bg_color, highlightthickness=0)
    canvas.pack()
    
    # 左侧装饰
    ThemeDrawings.draw_paw_badge(canvas, 50, 35, 30)
    
    # 标题
    canvas.create_text(300, 25, text=f"🐾 {title} 🐾", font=("微软雅黑", 22, "bold"), fill="#1565C0")
    if subtitle:
        canvas.create_text(300, 55, text=subtitle, font=("微软雅黑", 11), fill="#666")
    
    # 右侧装饰
    ThemeDrawings.draw_paw_badge(canvas, 550, 35, 30)
    
    return frame


def create_feedback_canvas(parent, width=200, height=120, bg_color="#E3F2FD"):
    """创建反馈Canvas"""
    return tk.Canvas(parent, width=width, height=height, bg=bg_color, highlightthickness=0)


def show_character_feedback(canvas, is_correct, char_id=None):
    """在Canvas上显示角色反馈"""
    if not THEME_AVAILABLE:
        return
    
    canvas.delete("all")
    
    if char_id is None:
        char_id, char_name, _, _ = get_random_character()
    else:
        char_name = next((c[1] for c in PAW_CHARACTERS if c[0] == char_id), "狗狗")
    
    draw_func = get_draw_func(char_id)
    if draw_func:
        w = int(canvas.cget("width"))
        h = int(canvas.cget("height"))
        draw_func(canvas, w//2, h//2 - 10, 0.65)
        
        if is_correct:
            text = f"{char_name}：太棒了！"
            color = "#4CAF50"
        else:
            text = f"{char_name}：加油！"
            color = "#FF9800"
        
        canvas.create_text(w//2, h - 15, text=text, font=("微软雅黑", 10, "bold"), fill=color)


def draw_decorations(canvas, width, height):
    """在Canvas上绘制装饰元素"""
    if not THEME_AVAILABLE:
        return
    
    # 角落装饰
    ThemeDrawings.draw_star(canvas, 30, 30, 18, "#FFD700")
    ThemeDrawings.draw_star(canvas, width - 30, 30, 18, "#FFD700")
    ThemeDrawings.draw_bone(canvas, width // 2, height - 20, 25)


def draw_grass_ground(canvas, width, height, grass_height=40):
    """绘制草地背景"""
    y = height - grass_height
    canvas.create_rectangle(0, y, width, height, fill="#81C784", outline="")
    canvas.create_rectangle(0, y, width, y + 8, fill="#66BB6A", outline="")
