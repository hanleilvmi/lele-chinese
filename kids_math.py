# -*- coding: utf-8 -*-
"""
乐乐的数学乐园 v2.0
适合3岁幼儿的趣味数学学习
包含：数字卡片、数一数、比大小、认形状、简单加法、数字打地鼠

v2.0 更新：继承 BaseGameModule，减少代码重复
"""

import tkinter as tk
from tkinter import messagebox
import random
import math

# 导入基类模块
from base_module import (
    BaseGameModule, logger, TTS_AVAILABLE,
    UI_CONFIG_AVAILABLE, IS_MOBILE
)

# 导入UI配置模块
try:
    from ui_config import UI, Colors, ScreenConfig, get_font, get_path
except ImportError:
    pass

# 导入语音配置
try:
    from voice_config_shared import create_rest_reminder
    VOICE_CONFIG_AVAILABLE = True
except ImportError:
    VOICE_CONFIG_AVAILABLE = False

# 导入主题系统
try:
    from theme_config import get_theme, ThemeHelper, get_random_character
    from theme_drawings import ThemeDrawings
    THEME_AVAILABLE = True
    theme = ThemeHelper()
except ImportError:
    THEME_AVAILABLE = False
    theme = None


class KidsMathApp(BaseGameModule):
    """数学乐园应用 - 继承自 BaseGameModule"""
    
    # 模块配置
    MODULE_NAME = "math"
    MODULE_TITLE = "乐乐的数学乐园"
    MODULE_COLOR = "#45B7D1"
    
    def __init__(self):
        # 调用父类初始化
        super().__init__()
        
        # 使用主题背景色
        self.bg_color = theme.bg_color if THEME_AVAILABLE else "#E8F5E9"
        self.window.configure(bg=self.bg_color)

        # 休息提醒
        if VOICE_CONFIG_AVAILABLE:
            try:
                self.rest_reminder = create_rest_reminder(self.window, 15)
                if self.rest_reminder:
                    self.rest_reminder.start()
            except:
                self.rest_reminder = None
        else:
            self.rest_reminder = None
        
        # 等级设置
        self.level = 1
        
        # 初始化数据
        self.init_data()
    
    def cleanup_on_exit(self):
        """退出时清理（扩展父类方法）"""
        try:
            if hasattr(self, 'rest_reminder') and self.rest_reminder:
                self.rest_reminder.stop()
        except:
            pass
        # 调用父类清理
        super().cleanup_on_exit()
    
    def set_level(self, level):
        """手动设置难度等级"""
        self.level = level
        self.init_data()
        self.speak(f"已切换到等级{level}，数字范围1到{self.max_number}！")
        self.create_main_menu()
    
    def init_data(self):
        """根据等级初始化数学数据"""
        # 根据等级设置数字范围
        if self.level == 1:
            self.max_number = 10
        elif self.level == 2:
            self.max_number = 15
        else:
            self.max_number = 20
        
        # 数字1-max_number
        self.numbers = []
        chinese_nums = ["零","一","二","三","四","五","六","七","八","九","十",
                       "十一","十二","十三","十四","十五","十六","十七","十八","十九","二十"]
        for i in range(1, self.max_number + 1):
            emoji_count = "🍎" * min(i, 10)
            if i > 10:
                emoji_count = "🍎" * 10 + "\n" + "🍎" * (i - 10)
            self.numbers.append({
                "num": i,
                "chinese": chinese_nums[i],
                "emoji": emoji_count,
                "desc": f"{i}个苹果"
            })
        
        # 形状 - 使用Canvas绘制彩色图形
        self.shapes = [
            {"name": "圆形", "desc": "圆圆的，像皮球", "color": "#FF6B6B", "draw": "circle"},
            {"name": "三角形", "desc": "三条边，像小山", "color": "#4ECDC4", "draw": "triangle"},
            {"name": "正方形", "desc": "四条边一样长", "color": "#45B7D1", "draw": "square"},
            {"name": "长方形", "desc": "两条长两条短", "color": "#96CEB4", "draw": "rectangle"},
            {"name": "星形", "desc": "五个角，亮闪闪", "color": "#FFD93D", "draw": "star"},
            {"name": "心形", "desc": "像爱心，代表爱", "color": "#FF69B4", "draw": "heart"},
            {"name": "菱形", "desc": "四个角，像风筝", "color": "#9C27B0", "draw": "diamond"},
            {"name": "五边形", "desc": "五条边，像房子", "color": "#FF9800", "draw": "pentagon"},
        ]
        
        # 水果emoji用于数数
        self.count_emojis = ["🍎", "🍌", "🍊", "🍇", "🍓", "⭐", "🎈", "🌸", "🐱", "🐕"]
        
        # 汪汪队角色列表
        self.paw_characters = [
            ("chase", "阿奇", "#1976D2"),
            ("marshall", "毛毛", "#F44336"),
            ("skye", "天天", "#EC407A"),
            ("rubble", "小砾", "#FFC107"),
            ("rocky", "灰灰", "#78909C"),
            ("zuma", "路马", "#FF9800"),
            ("everest", "珠珠", "#00BCD4"),
            ("tracker", "阿克", "#4CAF50"),
            ("rex", "小克", "#8BC34A"),
            ("liberty", "乐乐", "#9C27B0"),
        ]
    
    # =====================================================
    # 汪汪队角色反馈系统
    # =====================================================
    def get_character_draw_func(self, char_id):
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
    
    def show_paw_feedback(self, parent, is_correct, message=""):
        """显示汪汪队角色反馈弹窗"""
        if not THEME_AVAILABLE:
            return
        
        char_id, char_name, char_color = random.choice(self.paw_characters)
        draw_func = self.get_character_draw_func(char_id)
        if not draw_func:
            return
        
        popup = tk.Toplevel(parent)
        popup.overrideredirect(True)
        popup.attributes('-topmost', True)
        
        w, h = 280, 220
        x = parent.winfo_x() + (parent.winfo_width() - w) // 2
        y = parent.winfo_y() + (parent.winfo_height() - h) // 2
        popup.geometry(f"{w}x{h}+{x}+{y}")
        
        bg_color = "#E8F5E9" if is_correct else "#FFEBEE"
        popup.configure(bg=bg_color)
        
        canvas = tk.Canvas(popup, width=260, height=140, bg=bg_color, highlightthickness=0)
        canvas.pack(pady=10)
        draw_func(canvas, 130, 70, 0.9)
        
        if is_correct:
            text_color = "#4CAF50"
            default_msg = f"{char_name}说：太棒了！🎉"
        else:
            text_color = "#FF9800"
            default_msg = f"{char_name}说：再试一次！💪"
        
        tk.Label(popup, text=message or default_msg, font=("微软雅黑", 12, "bold"),
                bg=bg_color, fg=text_color).pack(pady=5)
        
        popup.after(1800, popup.destroy)

    # =====================================================
    # 形状绘制方法
    # =====================================================
    def draw_shape_on_canvas(self, canvas, shape_name, x, y, size, color=None):
        """在Canvas上绘制彩色形状"""
        if color is None:
            for s in self.shapes:
                if s["name"] == shape_name:
                    color = s["color"]
                    break
            if color is None:
                color = "#FF6B6B"
        
        outline_color = self._darken_color(color)
        
        if shape_name == "圆形":
            canvas.create_oval(x-size, y-size, x+size, y+size, 
                              fill=color, outline=outline_color, width=3)
            canvas.create_oval(x-size*0.5, y-size*0.5, x-size*0.2, y-size*0.2,
                              fill="white", outline="")
        elif shape_name == "三角形":
            h = size * 1.5
            points = [x, y-h*0.6, x-size, y+h*0.4, x+size, y+h*0.4]
            canvas.create_polygon(points, fill=color, outline=outline_color, width=3)
        elif shape_name == "正方形":
            canvas.create_rectangle(x-size, y-size, x+size, y+size,
                                   fill=color, outline=outline_color, width=3)
        elif shape_name == "长方形":
            canvas.create_rectangle(x-size*1.4, y-size*0.8, x+size*1.4, y+size*0.8,
                                   fill=color, outline=outline_color, width=3)
        elif shape_name == "星形":
            outer_r = size
            inner_r = size * 0.4
            coords = []
            for i in range(10):
                angle = math.pi/2 + i * math.pi/5
                r = outer_r if i % 2 == 0 else inner_r
                coords.append(x + r * math.cos(angle))
                coords.append(y - r * math.sin(angle))
            canvas.create_polygon(coords, fill=color, outline=outline_color, width=2)
        elif shape_name == "心形":
            coords = []
            for i in range(100):
                t = i * 2 * math.pi / 100
                hx = 16 * math.sin(t) ** 3
                hy = 13 * math.cos(t) - 5 * math.cos(2*t) - 2 * math.cos(3*t) - math.cos(4*t)
                coords.append(x + hx * size / 18)
                coords.append(y - hy * size / 18)
            canvas.create_polygon(coords, fill=color, outline=outline_color, width=2, smooth=True)
        elif shape_name == "菱形":
            points = [x, y-size*1.2, x+size*0.8, y, x, y+size*1.2, x-size*0.8, y]
            canvas.create_polygon(points, fill=color, outline=outline_color, width=3)
        elif shape_name == "五边形":
            coords = []
            for i in range(5):
                angle = math.pi/2 + i * 2 * math.pi / 5
                coords.append(x + size * math.cos(angle))
                coords.append(y - size * math.sin(angle))
            canvas.create_polygon(coords, fill=color, outline=outline_color, width=3)
    
    def _darken_color(self, hex_color, factor=0.7):
        """将颜色变暗"""
        hex_color = hex_color.lstrip('#')
        r = int(int(hex_color[0:2], 16) * factor)
        g = int(int(hex_color[2:4], 16) * factor)
        b = int(int(hex_color[4:6], 16) * factor)
        return f"#{r:02x}{g:02x}{b:02x}"

    # =====================================================
    # 主菜单
    # =====================================================
    def create_main_menu(self):
        for widget in self.window.winfo_children():
            widget.destroy()
        
        self.window.configure(bg=self.bg_color)
        
        main_frame = tk.Frame(self.window, bg=self.bg_color)
        main_frame.pack(fill=tk.BOTH, expand=True, padx=20, pady=8)
        
        # 汪汪队主题装饰Canvas
        if THEME_AVAILABLE:
            decor_canvas = tk.Canvas(main_frame, width=1060, height=70, bg=self.bg_color, highlightthickness=0)
            decor_canvas.pack(pady=3)
            ThemeDrawings.draw_paw_badge(decor_canvas, 50, 35, 30)
            ThemeDrawings.draw_star(decor_canvas, 120, 30, 18, "#FFD700")
            decor_canvas.create_text(530, 22, text="🔢 乐乐的数学乐园 🔢", 
                                    font=("微软雅黑", 28, "bold"), fill=theme.primary)
            decor_canvas.create_text(530, 52, text="✨ 汪汪队陪你快乐学数学 ✨",
                                    font=("微软雅黑", 10), fill="#666")
            ThemeDrawings.draw_star(decor_canvas, 940, 30, 18, "#FFD700")
            ThemeDrawings.draw_paw_badge(decor_canvas, 1010, 35, 30)
        else:
            tk.Label(main_frame, text="🔢 乐乐的数学乐园 🔢", 
                     font=("微软雅黑", 32, "bold"), bg=self.bg_color, fg="#45B7D1").pack(pady=5)
        
        # 等级选择和分数显示
        info_frame = tk.Frame(main_frame, bg=self.bg_color)
        info_frame.pack(pady=5)
        
        level_frame = tk.Frame(info_frame, bg=theme.primary if THEME_AVAILABLE else "#45B7D1", relief=tk.RAISED, bd=3)
        level_frame.pack(side=tk.LEFT, padx=10)
        tk.Label(level_frame, text="📊 难度等级", font=("微软雅黑", 10, "bold"), 
                bg=theme.primary if THEME_AVAILABLE else "#45B7D1", fg="white").pack(pady=2)
        level_btn_frame = tk.Frame(level_frame, bg=theme.primary if THEME_AVAILABLE else "#45B7D1")
        level_btn_frame.pack(pady=3, padx=8)
        
        level_colors = ["#96CEB4", "#FFD93D", "#FF6B6B"]
        level_texts = ["⭐入门", "⭐⭐进阶", "⭐⭐⭐挑战"]
        for i in range(3):
            lv = i + 1
            bg = level_colors[i] if self.level != lv else "#333"
            btn = tk.Button(level_btn_frame, text=level_texts[i], font=("微软雅黑", 9, "bold"), 
                           bg=bg, fg="white", width=7, relief=tk.RAISED, bd=2, cursor="hand2",
                           command=lambda l=lv: self.set_level(l))
            btn.pack(side=tk.LEFT, padx=2)
        
        score_frame = tk.Frame(info_frame, bg=theme.secondary if THEME_AVAILABLE else "#4ECDC4", relief=tk.RAISED, bd=3)
        score_frame.pack(side=tk.LEFT, padx=10)
        tk.Label(score_frame, text=f"⭐ 总分: {self.score} ⭐", 
                 font=("微软雅黑", 14, "bold"), bg=theme.secondary if THEME_AVAILABLE else "#4ECDC4", fg="white",
                 padx=20, pady=5).pack()
        tk.Label(score_frame, text=f"数字范围: 1-{self.max_number}", font=("微软雅黑", 9), 
                bg=theme.secondary if THEME_AVAILABLE else "#4ECDC4", fg="white").pack(pady=(0,3))
        
        # ========== 简单游戏区（3岁+）==========
        easy_section = tk.LabelFrame(main_frame, text="🌟 简单模式（3岁+）", 
                                     font=("微软雅黑", 12, "bold"), bg="#E8F5E9", 
                                     fg="#2E7D32", relief=tk.GROOVE, bd=3)
        easy_section.pack(fill=tk.X, pady=8, padx=5)
        
        easy_frame = tk.Frame(easy_section, bg="#E8F5E9")
        easy_frame.pack(pady=8)
        
        easy_modes = [
            ("🔢\n数字卡片", "#FF6B6B", "认识数字", self.start_number_cards),
            ("📊\n数一数", "#4ECDC4", "数数有几个", self.start_counting),
            ("🔺\n认形状", "#96CEB4", "学形状", self.start_shapes),
        ]
        
        for i, (title, color, desc, command) in enumerate(easy_modes):
            card = tk.Frame(easy_frame, bg=color, relief=tk.RAISED, bd=4)
            card.grid(row=0, column=i, padx=20, pady=5)
            btn = tk.Button(card, text=title, font=("微软雅黑", 16, "bold"),
                           bg=color, fg="white", width=10, height=3,
                           relief=tk.FLAT, cursor="hand2", command=command)
            btn.pack(padx=5, pady=5)
            tk.Label(card, text=desc, font=("微软雅黑", 10), bg=color, fg="white").pack(pady=3)
        
        # ========== 进阶游戏区（4岁+）==========
        advanced_section = tk.LabelFrame(main_frame, text="🚀 进阶模式（4岁+）", 
                                         font=("微软雅黑", 12, "bold"), bg="#E3F2FD", 
                                         fg="#1565C0", relief=tk.GROOVE, bd=3)
        advanced_section.pack(fill=tk.X, pady=8, padx=5)
        
        advanced_frame = tk.Frame(advanced_section, bg="#E3F2FD")
        advanced_frame.pack(pady=8)
        
        advanced_modes = [
            ("⚖️\n比大小", "#45B7D1", "谁更大", self.start_compare),
            ("➕\n学加法", "#DDA0DD", "简单加法", self.start_addition),
            ("🔨\n打地鼠", "#FFD93D", "快速反应", self.start_whack),
        ]
        
        for i, (title, color, desc, command) in enumerate(advanced_modes):
            card = tk.Frame(advanced_frame, bg=color, relief=tk.RAISED, bd=4)
            card.grid(row=0, column=i, padx=20, pady=5)
            btn = tk.Button(card, text=title, font=("微软雅黑", 16, "bold"),
                           bg=color, fg="white", width=10, height=3,
                           relief=tk.FLAT, cursor="hand2", command=command)
            btn.pack(padx=5, pady=5)
            tk.Label(card, text=desc, font=("微软雅黑", 10), bg=color, fg="white").pack(pady=3)
        
        # 汪汪队底部装饰
        if THEME_AVAILABLE:
            bottom_canvas = tk.Canvas(main_frame, width=1060, height=70, bg=self.bg_color, highlightthickness=0)
            bottom_canvas.pack(pady=5)
            bottom_canvas.create_rectangle(0, 45, 1060, 70, fill="#81C784", outline="")
            ThemeDrawings.draw_puppy_chase(bottom_canvas, 180, 32, 0.4)
            ThemeDrawings.draw_puppy_marshall(bottom_canvas, 380, 32, 0.4)
            ThemeDrawings.draw_puppy_skye(bottom_canvas, 580, 32, 0.4)
            ThemeDrawings.draw_puppy_rubble(bottom_canvas, 780, 32, 0.4)
            ThemeDrawings.draw_puppy_rocky(bottom_canvas, 980, 32, 0.4)
        
        tk.Button(main_frame, text="👋 退出", font=("微软雅黑", 11),
                  bg="#FF6B6B", fg="white", relief=tk.RAISED, bd=3,
                  cursor="hand2", command=self.on_close_window).pack(pady=8)

    def clear_game_area(self, bg_color="#E8F5E9"):
        """清空游戏区域（覆盖父类方法以使用自定义样式）"""
        # 清理定时器
        for timer_id in self.pending_timers:
            try:
                self.window.after_cancel(timer_id)
            except:
                pass
        self.pending_timers.clear()
        
        for widget in self.window.winfo_children():
            widget.destroy()
        
        self.window.configure(bg=bg_color)
        
        nav_frame = tk.Frame(self.window, bg=bg_color)
        nav_frame.pack(fill=tk.X, pady=5)
        
        tk.Button(nav_frame, text="🏠 返回主菜单", font=("微软雅黑", 11),
                  bg="#96CEB4", fg="white", relief=tk.RAISED, bd=3,
                  cursor="hand2", command=self.create_main_menu).pack(side=tk.LEFT, padx=10)
        
        tk.Label(nav_frame, text=f"⭐ 总分: {self.score}",
                 font=("微软雅黑", 12, "bold"), bg=bg_color, fg="#4ECDC4").pack(side=tk.RIGHT, padx=10)
        
        self.game_frame = tk.Frame(self.window, bg=bg_color)
        self.game_frame.pack(fill=tk.BOTH, expand=True, padx=20, pady=10)

    # =====================================================
    # 模式1: 数字卡片（1-20）
    # =====================================================
    def start_number_cards(self):
        self.clear_game_area("#FFF8DC")
        self.num_index = 0
        
        tk.Label(self.game_frame, text="🔢 数字卡片", font=("微软雅黑", 26, "bold"),
                 bg="#FFF8DC", fg="#FF6B6B").pack(pady=5)
        tk.Label(self.game_frame, text="认识数字 1-20", font=("微软雅黑", 12),
                 bg="#FFF8DC", fg="#888").pack()
        
        self.num_progress = tk.Label(self.game_frame, text="", font=("微软雅黑", 11),
                                      bg="#FFF8DC", fg="#666")
        self.num_progress.pack(pady=5)
        
        card = tk.Frame(self.game_frame, bg="white", relief=tk.RAISED, bd=4)
        card.pack(pady=10, padx=80, fill=tk.X)
        
        num_row = tk.Frame(card, bg="white")
        num_row.pack(pady=15)
        
        self.num_digit = tk.Label(num_row, text="", font=("Arial", 100, "bold"), 
                                   bg="white", fg="#FF6B6B")
        self.num_digit.pack(side=tk.LEFT, padx=30)
        
        self.num_chinese = tk.Label(num_row, text="", font=("楷体", 70, "bold"), 
                                     bg="white", fg="#4ECDC4")
        self.num_chinese.pack(side=tk.LEFT, padx=30)
        
        self.num_emoji = tk.Label(card, text="", font=("Segoe UI Emoji", 28), 
                                   bg="white", wraplength=500)
        self.num_emoji.pack(pady=10)
        
        self.num_desc = tk.Label(card, text="", font=("微软雅黑", 18), 
                                  bg="white", fg="#666")
        self.num_desc.pack(pady=10)
        
        btn_frame = tk.Frame(self.game_frame, bg="#FFF8DC")
        btn_frame.pack(pady=15)
        
        buttons = [
            ("⬅️ 上一个", "#45B7D1", self.prev_number),
            ("🔊 读一读", "#FF6B6B", self.speak_number),
            ("下一个 ➡️", "#45B7D1", self.next_number),
        ]
        
        for text, color, cmd in buttons:
            tk.Button(btn_frame, text=text, font=("微软雅黑", 11), bg=color, fg="white",
                      command=cmd, width=10).pack(side=tk.LEFT, padx=5)
        
        self.show_number()
    
    def show_number(self):
        n = self.numbers[self.num_index]
        self.num_digit.config(text=str(n["num"]))
        self.num_chinese.config(text=n["chinese"])
        self.num_emoji.config(text=n["emoji"])
        self.num_desc.config(text=n["desc"])
        self.num_progress.config(text=f"第 {self.num_index + 1} / 20 个数字")
        self.speak(f"这是数字{n['num']}，{n['chinese']}，{n['desc']}", "-10%")
    
    def speak_number(self):
        n = self.numbers[self.num_index]
        self.speak(f"{n['num']}，{n['chinese']}，数一数，{n['desc']}", "-10%")
    
    def next_number(self):
        self.num_index = (self.num_index + 1) % len(self.numbers)
        self.show_number()
    
    def prev_number(self):
        self.num_index = (self.num_index - 1) % len(self.numbers)
        self.show_number()

    # =====================================================
    # 模式2: 数一数（汪汪队版）
    # =====================================================
    def start_counting(self):
        self.clear_game_area("#E0FFFF")
        self.count_score = 0
        
        title_frame = tk.Frame(self.game_frame, bg="#E0FFFF")
        title_frame.pack(pady=5)
        
        if THEME_AVAILABLE:
            title_canvas = tk.Canvas(title_frame, width=500, height=60, bg="#E0FFFF", highlightthickness=0)
            title_canvas.pack()
            title_canvas.create_text(250, 20, text="🐾 数一数 🐾", font=("微软雅黑", 24, "bold"), fill="#4ECDC4")
            title_canvas.create_text(250, 48, text="帮狗狗们数一数有几个！", font=("微软雅黑", 12), fill="#666")
            ThemeDrawings.draw_paw_badge(title_canvas, 40, 30, 25)
            ThemeDrawings.draw_paw_badge(title_canvas, 460, 30, 25)
        else:
            tk.Label(title_frame, text="📊 数一数", font=("微软雅黑", 26, "bold"),
                     bg="#E0FFFF", fg="#4ECDC4").pack()
        
        self.count_score_label = tk.Label(self.game_frame, text="⭐ 得分: 0",
                                           font=("微软雅黑", 14), bg="#E0FFFF", fg="#666")
        self.count_score_label.pack(pady=5)
        
        self.count_canvas = tk.Canvas(self.game_frame, width=600, height=200, bg="white", 
                                      relief=tk.RAISED, bd=4)
        self.count_canvas.pack(pady=15)
        
        self.count_hint = tk.Label(self.game_frame, text="", font=("微软雅黑", 18), bg="#E0FFFF")
        self.count_hint.pack(pady=5)
        
        self.count_feedback_canvas = tk.Canvas(self.game_frame, width=200, height=120, 
                                               bg="#E0FFFF", highlightthickness=0)
        self.count_feedback_canvas.pack(pady=5)
        
        self.count_frame = tk.Frame(self.game_frame, bg="#E0FFFF")
        self.count_frame.pack(pady=15)
        
        self.count_buttons = []
        colors = ["#FF6B6B", "#4ECDC4", "#45B7D1", "#96CEB4", "#DDA0DD", "#FFD93D"]
        
        for i in range(6):
            btn = tk.Button(self.count_frame, text="", font=("Arial", 28, "bold"),
                           width=3, height=1, bg=colors[i], fg="white",
                           relief=tk.RAISED, bd=4, cursor="hand2",
                           command=lambda idx=i: self.check_count(idx))
            btn.grid(row=0, column=i, padx=10, pady=8)
            self.count_buttons.append(btn)
        
        self.new_count_question()
    
    def new_count_question(self):
        self.count_answer = random.randint(2, 8)
        
        self.count_canvas.delete("all")
        self.count_feedback_canvas.delete("all")
        
        if THEME_AVAILABLE:
            char_id, char_name, _ = random.choice(self.paw_characters[:6])
            draw_func = self.get_character_draw_func(char_id)
            
            cols = min(self.count_answer, 4)
            rows = (self.count_answer + 3) // 4
            start_x = 300 - (cols * 70) // 2 + 35
            start_y = 100 - (rows * 50) // 2 + 25
            
            for i in range(self.count_answer):
                row = i // 4
                col = i % 4
                x = start_x + col * 70
                y = start_y + row * 80
                if draw_func:
                    draw_func(self.count_canvas, x, y, 0.45)
            
            self.count_canvas.create_text(300, 185, text=f"数一数，有几只{char_name}？", 
                                         font=("微软雅黑", 12), fill="#666")
        else:
            emoji = random.choice(self.count_emojis)
            display_text = ""
            for i in range(self.count_answer):
                display_text += emoji + " "
                if (i + 1) % 5 == 0:
                    display_text += "\n"
            self.count_canvas.create_text(300, 100, text=display_text, font=("Segoe UI Emoji", 35))
        
        self.count_options = [self.count_answer]
        while len(self.count_options) < 6:
            n = random.randint(1, 10)
            if n not in self.count_options:
                self.count_options.append(n)
        random.shuffle(self.count_options)
        self.count_correct_idx = self.count_options.index(self.count_answer)
        
        colors = ["#FF6B6B", "#4ECDC4", "#45B7D1", "#96CEB4", "#DDA0DD", "#FFD93D"]
        for i, btn in enumerate(self.count_buttons):
            btn.config(text=str(self.count_options[i]), bg=colors[i], state=tk.NORMAL)
        
        self.count_hint.config(text="", fg="#666")
        self.speak("数一数，有几个？", "-10%")
    
    def check_count(self, idx):
        self.count_feedback_canvas.delete("all")
        
        if idx == self.count_correct_idx:
            self.count_score += 10
            self.score += 10
            self.count_hint.config(text=f"🎉 对啦！有 {self.count_answer} 个！", fg="#32CD32")
            self.count_buttons[idx].config(bg="#32CD32")
            
            if THEME_AVAILABLE:
                char_id, char_name, _ = random.choice(self.paw_characters)
                draw_func = self.get_character_draw_func(char_id)
                if draw_func:
                    draw_func(self.count_feedback_canvas, 100, 60, 0.7)
                    self.count_feedback_canvas.create_text(100, 115, text=f"{char_name}：太棒了！", 
                                                          font=("微软雅黑", 10, "bold"), fill="#4CAF50")
            self.speak_praise()
        else:
            self.count_hint.config(text=f"😅 数错啦，有 {self.count_answer} 个哦！", fg="#FF6B6B")
            self.count_buttons[idx].config(bg="#808080")
            self.count_buttons[self.count_correct_idx].config(bg="#32CD32")
            
            if THEME_AVAILABLE:
                char_id, char_name, _ = random.choice(self.paw_characters)
                draw_func = self.get_character_draw_func(char_id)
                if draw_func:
                    draw_func(self.count_feedback_canvas, 100, 60, 0.7)
                    self.count_feedback_canvas.create_text(100, 115, text=f"{char_name}：再试试！", 
                                                          font=("微软雅黑", 10, "bold"), fill="#FF9800")
            self.speak_encourage()
        
        self.count_score_label.config(text=f"⭐ 得分: {self.count_score}")
        
        for btn in self.count_buttons:
            btn.config(state=tk.DISABLED)
        self.safe_after(3500, self.new_count_question)

    # =====================================================
    # 模式3: 比大小（汪汪队版）
    # =====================================================
    def start_compare(self):
        self.clear_game_area("#FFE4E1")
        self.compare_score = 0
        
        if THEME_AVAILABLE:
            title_canvas = tk.Canvas(self.game_frame, width=600, height=70, bg="#FFE4E1", highlightthickness=0)
            title_canvas.pack(pady=5)
            title_canvas.create_text(300, 25, text="🐾 比大小 🐾", font=("微软雅黑", 24, "bold"), fill="#45B7D1")
            title_canvas.create_text(300, 55, text="帮狗狗们比一比谁的骨头多！", font=("微软雅黑", 12), fill="#666")
            ThemeDrawings.draw_bone(title_canvas, 80, 35, 30)
            ThemeDrawings.draw_bone(title_canvas, 520, 35, 30)
        else:
            tk.Label(self.game_frame, text="⚖️ 比大小", font=("微软雅黑", 26, "bold"),
                     bg="#FFE4E1", fg="#45B7D1").pack(pady=5)
        
        self.compare_score_label = tk.Label(self.game_frame, text="⭐ 得分: 0",
                                             font=("微软雅黑", 14), bg="#FFE4E1", fg="#666")
        self.compare_score_label.pack()
        
        self.compare_question = tk.Label(self.game_frame, text="哪个更大？点击大的那个！",
                                          font=("微软雅黑", 16), bg="#FFE4E1", fg="#888")
        self.compare_question.pack(pady=10)
        
        self.compare_canvas = tk.Canvas(self.game_frame, width=700, height=200, bg="#FFE4E1", highlightthickness=0)
        self.compare_canvas.pack(pady=10)
        
        self.compare_feedback = tk.Canvas(self.game_frame, width=200, height=100, bg="#FFE4E1", highlightthickness=0)
        self.compare_feedback.pack(pady=5)
        
        self.compare_hint = tk.Label(self.game_frame, text="", font=("微软雅黑", 18), bg="#FFE4E1")
        self.compare_hint.pack(pady=10)
        
        btn_frame = tk.Frame(self.game_frame, bg="#FFE4E1")
        btn_frame.pack(pady=10)
        
        self.compare_btn1 = tk.Button(btn_frame, text="选左边", font=("微软雅黑", 14, "bold"),
                                       bg="#FF6B6B", fg="white", width=12, height=2,
                                       cursor="hand2", command=lambda: self.check_compare(0))
        self.compare_btn1.pack(side=tk.LEFT, padx=30)
        
        self.compare_btn2 = tk.Button(btn_frame, text="选右边", font=("微软雅黑", 14, "bold"),
                                       bg="#4ECDC4", fg="white", width=12, height=2,
                                       cursor="hand2", command=lambda: self.check_compare(1))
        self.compare_btn2.pack(side=tk.LEFT, padx=30)
        
        self.new_compare_question()
    
    def new_compare_question(self):
        n1 = random.randint(1, 10)
        n2 = random.randint(1, 10)
        while n2 == n1:
            n2 = random.randint(1, 10)
        
        self.compare_n1 = n1
        self.compare_n2 = n2
        self.compare_correct = 0 if n1 > n2 else 1
        
        self.compare_canvas.delete("all")
        self.compare_feedback.delete("all")
        
        if THEME_AVAILABLE:
            char1_id, char1_name, _ = random.choice(self.paw_characters[:5])
            draw1 = self.get_character_draw_func(char1_id)
            if draw1:
                draw1(self.compare_canvas, 120, 100, 0.7)
            self.compare_canvas.create_text(120, 170, text=f"{char1_name}", font=("微软雅黑", 10), fill="#666")
            self.compare_canvas.create_oval(70, 30, 170, 70, fill="#FFD54F", outline="#FFA000", width=2)
            self.compare_canvas.create_text(120, 50, text=str(n1), font=("Arial", 28, "bold"), fill="#5D4037")
            
            self.compare_canvas.create_text(350, 100, text="VS", font=("Arial", 36, "bold"), fill="#DDA0DD")
            
            char2_id, char2_name, _ = random.choice(self.paw_characters[5:])
            draw2 = self.get_character_draw_func(char2_id)
            if draw2:
                draw2(self.compare_canvas, 580, 100, 0.7)
            self.compare_canvas.create_text(580, 170, text=f"{char2_name}", font=("微软雅黑", 10), fill="#666")
            self.compare_canvas.create_oval(530, 30, 630, 70, fill="#FFD54F", outline="#FFA000", width=2)
            self.compare_canvas.create_text(580, 50, text=str(n2), font=("Arial", 28, "bold"), fill="#5D4037")
        else:
            self.compare_canvas.create_text(150, 100, text=str(n1), font=("Arial", 70, "bold"), fill="#FF6B6B")
            self.compare_canvas.create_text(350, 100, text="VS", font=("Arial", 36, "bold"), fill="#DDA0DD")
            self.compare_canvas.create_text(550, 100, text=str(n2), font=("Arial", 70, "bold"), fill="#4ECDC4")
        
        self.compare_question.config(text=f"🔢 {n1} 和 {n2}，哪个更大？")
        self.compare_btn1.config(bg="#FF6B6B", state=tk.NORMAL)
        self.compare_btn2.config(bg="#4ECDC4", state=tk.NORMAL)
        self.compare_hint.config(text="", fg="#666")
        self.speak(f"{n1}和{n2}，哪个更大？", "-10%")
    
    def check_compare(self, idx):
        bigger = self.compare_n1 if self.compare_n1 > self.compare_n2 else self.compare_n2
        symbol = ">" if self.compare_n1 > self.compare_n2 else "<"
        
        self.compare_feedback.delete("all")
        
        if idx == self.compare_correct:
            self.compare_score += 10
            self.score += 10
            self.compare_hint.config(text=f"🎉 对啦！{self.compare_n1} {symbol} {self.compare_n2}，{bigger}更大！", fg="#32CD32")
            if idx == 0:
                self.compare_btn1.config(bg="#32CD32")
            else:
                self.compare_btn2.config(bg="#32CD32")
            
            if THEME_AVAILABLE:
                char_id, char_name, _ = random.choice(self.paw_characters)
                draw_func = self.get_character_draw_func(char_id)
                if draw_func:
                    draw_func(self.compare_feedback, 100, 50, 0.6)
                    self.compare_feedback.create_text(100, 95, text=f"{char_name}：真棒！", 
                                                     font=("微软雅黑", 10, "bold"), fill="#4CAF50")
            self.speak_praise()
        else:
            self.compare_hint.config(text=f"😅 {self.compare_n1} {symbol} {self.compare_n2}，{bigger}更大哦！", fg="#FF6B6B")
            if self.compare_correct == 0:
                self.compare_btn1.config(bg="#32CD32")
                self.compare_btn2.config(bg="#808080")
            else:
                self.compare_btn2.config(bg="#32CD32")
                self.compare_btn1.config(bg="#808080")
            
            if THEME_AVAILABLE:
                char_id, char_name, _ = random.choice(self.paw_characters)
                draw_func = self.get_character_draw_func(char_id)
                if draw_func:
                    draw_func(self.compare_feedback, 100, 50, 0.6)
                    self.compare_feedback.create_text(100, 95, text=f"{char_name}：加油！", 
                                                     font=("微软雅黑", 10, "bold"), fill="#FF9800")
            self.speak_encourage()
        
        self.compare_score_label.config(text=f"⭐ 得分: {self.compare_score}")
        self.compare_btn1.config(state=tk.DISABLED)
        self.compare_btn2.config(state=tk.DISABLED)
        self.safe_after(3500, self.new_compare_question)

    # =====================================================
    # 模式4: 认形状
    # =====================================================
    def start_shapes(self):
        self.clear_game_area("#FFF0F5")
        self.shape_index = 0
        self.shape_mode = "learn"
        
        tk.Label(self.game_frame, text="🔺 认形状", font=("微软雅黑", 26, "bold"),
                 bg="#FFF0F5", fg="#96CEB4").pack(pady=5)
        
        mode_frame = tk.Frame(self.game_frame, bg="#FFF0F5")
        mode_frame.pack(pady=10)
        
        tk.Button(mode_frame, text="📖 学习模式", font=("微软雅黑", 11), 
                  bg="#4ECDC4", fg="white", width=12,
                  command=self.shape_learn_mode).pack(side=tk.LEFT, padx=10)
        tk.Button(mode_frame, text="🎯 答题模式", font=("微软雅黑", 11), 
                  bg="#FF6B6B", fg="white", width=12,
                  command=self.shape_quiz_mode).pack(side=tk.LEFT, padx=10)
        
        self.shape_content = tk.Frame(self.game_frame, bg="#FFF0F5")
        self.shape_content.pack(fill=tk.BOTH, expand=True, pady=10)
        
        self.shape_learn_mode()
    
    def shape_learn_mode(self):
        self.shape_mode = "learn"
        for widget in self.shape_content.winfo_children():
            widget.destroy()
        
        self.shape_canvas = tk.Canvas(self.shape_content, width=300, height=250, 
                                       bg="white", relief=tk.RAISED, bd=4)
        self.shape_canvas.pack(pady=15)
        
        self.shape_name_label = tk.Label(self.shape_content, text="", 
                                          font=("微软雅黑", 36, "bold"), bg="#FFF0F5")
        self.shape_name_label.pack(pady=5)
        
        self.shape_desc = tk.Label(self.shape_content, text="", 
                                    font=("微软雅黑", 18), bg="#FFF0F5", fg="#666")
        self.shape_desc.pack(pady=5)
        
        btn_frame = tk.Frame(self.shape_content, bg="#FFF0F5")
        btn_frame.pack(pady=15)
        
        tk.Button(btn_frame, text="⬅️ 上一个", font=("微软雅黑", 12), bg="#45B7D1", fg="white",
                  command=self.prev_shape, width=10).pack(side=tk.LEFT, padx=10)
        tk.Button(btn_frame, text="🔊 读一读", font=("微软雅黑", 12), bg="#FF6B6B", fg="white",
                  command=self.speak_shape, width=10).pack(side=tk.LEFT, padx=10)
        tk.Button(btn_frame, text="下一个 ➡️", font=("微软雅黑", 12), bg="#45B7D1", fg="white",
                  command=self.next_shape, width=10).pack(side=tk.LEFT, padx=10)
        
        self.show_shape()
    
    def show_shape(self):
        s = self.shapes[self.shape_index]
        self.shape_canvas.delete("all")
        self.draw_shape_on_canvas(self.shape_canvas, s["name"], 150, 125, 70, s["color"])
        self.shape_name_label.config(text=s["name"], fg=s["color"])
        self.shape_desc.config(text=s["desc"])
        self.speak(f"这是{s['name']}，{s['desc']}", "-10%")
    
    def speak_shape(self):
        s = self.shapes[self.shape_index]
        self.speak(f"{s['name']}，{s['desc']}", "-10%")
    
    def next_shape(self):
        self.shape_index = (self.shape_index + 1) % len(self.shapes)
        self.show_shape()
    
    def prev_shape(self):
        self.shape_index = (self.shape_index - 1) % len(self.shapes)
        self.show_shape()
    
    def shape_quiz_mode(self):
        self.shape_mode = "quiz"
        self.shape_quiz_score = 0
        
        for widget in self.shape_content.winfo_children():
            widget.destroy()
        
        self.shape_quiz_score_label = tk.Label(self.shape_content, text="⭐ 得分: 0",
                                                font=("微软雅黑", 14), bg="#FFF0F5", fg="#666")
        self.shape_quiz_score_label.pack()
        
        tk.Label(self.shape_content, text="看图形，选名字！", font=("微软雅黑", 14),
                 bg="#FFF0F5", fg="#888").pack(pady=5)
        
        self.shape_quiz_canvas = tk.Canvas(self.shape_content, width=250, height=200, 
                                            bg="white", relief=tk.RAISED, bd=4)
        self.shape_quiz_canvas.pack(pady=15)
        
        self.shape_hint = tk.Label(self.shape_content, text="", font=("微软雅黑", 16), bg="#FFF0F5")
        self.shape_hint.pack()
        
        self.shape_options_frame = tk.Frame(self.shape_content, bg="#FFF0F5")
        self.shape_options_frame.pack(pady=15)
        
        self.shape_buttons = []
        colors = ["#FF6B6B", "#4ECDC4", "#45B7D1", "#96CEB4"]
        for i in range(4):
            btn = tk.Button(self.shape_options_frame, text="", font=("微软雅黑", 18, "bold"),
                           width=8, height=1, bg=colors[i], fg="white",
                           relief=tk.RAISED, bd=4, cursor="hand2",
                           command=lambda idx=i: self.check_shape_quiz(idx))
            btn.grid(row=0, column=i, padx=10)
            self.shape_buttons.append(btn)
        
        self.new_shape_question()
    
    def new_shape_question(self):
        self.shape_target = random.choice(self.shapes)
        others = random.sample([s for s in self.shapes if s != self.shape_target], 3)
        self.shape_options = [self.shape_target] + others
        random.shuffle(self.shape_options)
        self.shape_correct_idx = self.shape_options.index(self.shape_target)
        
        self.shape_quiz_canvas.delete("all")
        self.draw_shape_on_canvas(self.shape_quiz_canvas, self.shape_target["name"], 
                                   125, 100, 60, self.shape_target["color"])
        
        colors = ["#FF6B6B", "#4ECDC4", "#45B7D1", "#96CEB4"]
        for i, btn in enumerate(self.shape_buttons):
            btn.config(text=self.shape_options[i]["name"], bg=colors[i], state=tk.NORMAL)
        
        self.shape_hint.config(text="", fg="#666")
        self.speak("这是什么形状？", "-10%")
    
    def check_shape_quiz(self, idx):
        if idx == self.shape_correct_idx:
            self.shape_quiz_score += 10
            self.score += 10
            self.shape_hint.config(text=f"🎉 对啦！这是{self.shape_target['name']}！", fg="#32CD32")
            self.shape_buttons[idx].config(bg="#32CD32")
            self.speak_praise()
        else:
            self.shape_hint.config(text=f"😅 这是{self.shape_target['name']}哦！", fg="#FF6B6B")
            self.shape_buttons[idx].config(bg="#808080")
            self.shape_buttons[self.shape_correct_idx].config(bg="#32CD32")
            self.speak_encourage()
        
        self.shape_quiz_score_label.config(text=f"⭐ 得分: {self.shape_quiz_score}")
        for btn in self.shape_buttons:
            btn.config(state=tk.DISABLED)
        self.safe_after(5500, self.new_shape_question)

    # =====================================================
    # 模式5: 学加法
    # =====================================================
    def start_addition(self):
        self.clear_game_area("#E8F5E9")
        self.add_score = 0
        
        tk.Label(self.game_frame, text="➕ 学加法", font=("微软雅黑", 26, "bold"),
                 bg="#E8F5E9", fg="#DDA0DD").pack(pady=5)
        
        self.add_score_label = tk.Label(self.game_frame, text="⭐ 得分: 0",
                                         font=("微软雅黑", 14), bg="#E8F5E9", fg="#666")
        self.add_score_label.pack()
        
        self.add_question = tk.Label(self.game_frame, text="", font=("Arial", 50, "bold"),
                                      bg="#E8F5E9", fg="#45B7D1")
        self.add_question.pack(pady=20)
        
        self.add_visual = tk.Label(self.game_frame, text="", font=("Segoe UI Emoji", 40),
                                    bg="#E8F5E9")
        self.add_visual.pack(pady=10)
        
        self.add_hint = tk.Label(self.game_frame, text="", font=("微软雅黑", 18), bg="#E8F5E9")
        self.add_hint.pack(pady=10)
        
        self.add_frame = tk.Frame(self.game_frame, bg="#E8F5E9")
        self.add_frame.pack(pady=20)
        
        self.add_buttons = []
        colors = ["#FF6B6B", "#4ECDC4", "#45B7D1", "#96CEB4", "#DDA0DD", "#FFD93D"]
        for i in range(6):
            btn = tk.Button(self.add_frame, text="", font=("Arial", 28, "bold"),
                           width=3, height=1, bg=colors[i], fg="white",
                           relief=tk.RAISED, bd=4, cursor="hand2",
                           command=lambda idx=i: self.check_addition(idx))
            btn.grid(row=0, column=i, padx=10)
            self.add_buttons.append(btn)
        
        self.new_addition_question()
    
    def new_addition_question(self):
        self.add_n1 = random.randint(1, 5)
        self.add_n2 = random.randint(1, 5)
        self.add_answer = self.add_n1 + self.add_n2
        
        self.add_question.config(text=f"{self.add_n1} + {self.add_n2} = ?")
        
        emoji = random.choice(["🍎", "⭐", "🎈"])
        visual = emoji * self.add_n1 + " + " + emoji * self.add_n2
        self.add_visual.config(text=visual)
        
        self.add_options = [self.add_answer]
        while len(self.add_options) < 6:
            n = random.randint(2, 10)
            if n not in self.add_options:
                self.add_options.append(n)
        random.shuffle(self.add_options)
        self.add_correct_idx = self.add_options.index(self.add_answer)
        
        colors = ["#FF6B6B", "#4ECDC4", "#45B7D1", "#96CEB4", "#DDA0DD", "#FFD93D"]
        for i, btn in enumerate(self.add_buttons):
            btn.config(text=str(self.add_options[i]), bg=colors[i], state=tk.NORMAL)
        
        self.add_hint.config(text="", fg="#666")
        self.speak(f"{self.add_n1}加{self.add_n2}等于几？", "-10%")
    
    def check_addition(self, idx):
        if idx == self.add_correct_idx:
            self.add_score += 10
            self.score += 10
            self.add_hint.config(text=f"🎉 对啦！{self.add_n1}+{self.add_n2}={self.add_answer}！", fg="#32CD32")
            self.add_buttons[idx].config(bg="#32CD32")
            self.speak_praise()
        else:
            self.add_hint.config(text=f"😅 {self.add_n1}+{self.add_n2}={self.add_answer}哦！", fg="#FF6B6B")
            self.add_buttons[idx].config(bg="#808080")
            self.add_buttons[self.add_correct_idx].config(bg="#32CD32")
            self.speak_encourage()
        
        self.add_score_label.config(text=f"⭐ 得分: {self.add_score}")
        for btn in self.add_buttons:
            btn.config(state=tk.DISABLED)
        self.safe_after(5500, self.new_addition_question)

    # =====================================================
    # 模式6: 打地鼠
    # =====================================================
    def start_whack(self):
        """数字打地鼠 - 打掉带有目标数字的地鼠"""
        self.clear_game_area("#90EE90")
        self.whack_score = 0
        self.whack_running = True
        self.whack_combo = 0
        self.whack_holes = []
        self.whack_hole_states = [None] * 9
        self.whack_target = 0
        self.whack_answered = False
        
        tk.Label(self.game_frame, text="🔨 数字打地鼠", font=("微软雅黑", 26, "bold"),
                 bg="#90EE90", fg="#228B22").pack(pady=5)
        
        info_frame = tk.Frame(self.game_frame, bg="#90EE90")
        info_frame.pack(pady=8)
        
        self.whack_score_label = tk.Label(info_frame, text="⭐ 得分: 0",
                                           font=("微软雅黑", 14, "bold"), bg="#90EE90", fg="#FF6B6B")
        self.whack_score_label.pack(side=tk.LEFT, padx=15)
        
        self.whack_combo_label = tk.Label(info_frame, text="🔥 连击: 0",
                                           font=("微软雅黑", 14, "bold"), bg="#90EE90", fg="#FF8C00")
        self.whack_combo_label.pack(side=tk.LEFT, padx=15)
        
        target_frame = tk.Frame(self.game_frame, bg="#FFD700", relief=tk.RAISED, bd=4)
        target_frame.pack(pady=10)
        
        tk.Label(target_frame, text="🎯 打这个数字的地鼠：", font=("微软雅黑", 16),
                 bg="#FFD700", fg="#333").pack(side=tk.LEFT, padx=10, pady=10)
        
        self.whack_target_label = tk.Label(target_frame, text="", font=("Arial", 55, "bold"),
                                            bg="#FFD700", fg="#DC143C")
        self.whack_target_label.pack(side=tk.LEFT, padx=15, pady=10)
        
        self.whack_hint = tk.Label(self.game_frame, text="🐹 地鼠出现了！快打带有正确数字的地鼠！",
                                    font=("微软雅黑", 13), bg="#90EE90", fg="#006400")
        self.whack_hint.pack(pady=5)
        
        holes_frame = tk.Frame(self.game_frame, bg="#228B22", relief=tk.RIDGE, bd=6)
        holes_frame.pack(pady=10)
        
        for i in range(9):
            row = i // 3
            col = i % 3
            
            hole_outer = tk.Frame(holes_frame, bg="#8B4513", relief=tk.SUNKEN, bd=4)
            hole_outer.grid(row=row, column=col, padx=12, pady=12)
            
            btn = tk.Button(hole_outer, text="🕳️", font=("Segoe UI Emoji", 32),
                           width=4, height=2, bg="#3D2914", fg="#333",
                           relief=tk.SUNKEN, bd=3, cursor="hand2",
                           command=lambda idx=i: self.whack_click(idx))
            btn.pack(padx=4, pady=4)
            self.whack_holes.append(btn)
        
        self.speak("数字打地鼠开始！打掉带有正确数字的地鼠！", "+0%")
        self.safe_after(2000, self.whack_new_round)
    
    def whack_new_round(self):
        if not self.whack_running:
            return
        
        self.whack_answered = False
        
        for i in range(9):
            self.whack_holes[i].config(text="🕳️", bg="#3D2914", state=tk.NORMAL)
            self.whack_hole_states[i] = None
        
        self.whack_target = random.randint(1, 10)
        self.whack_target_label.config(text=str(self.whack_target))
        
        self.speak(f"打，{self.whack_target}", "+10%")
        self.safe_after(800, self.whack_show_moles)
    
    def whack_show_moles(self):
        if not self.whack_running or self.whack_answered:
            return
        
        num_moles = random.randint(3, 4)
        positions = random.sample(range(9), num_moles)
        correct_pos = random.choice(positions)
        
        other_nums = [n for n in range(1, 11) if n != self.whack_target]
        distractors = random.sample(other_nums, num_moles - 1)
        
        distractor_idx = 0
        for pos in positions:
            if pos == correct_pos:
                num = self.whack_target
                self.whack_holes[pos].config(text=f"🐹\n{num}", bg="#FFE4B5")
                self.whack_hole_states[pos] = num
            else:
                num = distractors[distractor_idx]
                self.whack_holes[pos].config(text=f"🐹\n{num}", bg="#FFDAB9")
                self.whack_hole_states[pos] = num
                distractor_idx += 1
        
        self.whack_hint.config(text=f"🔨 快打带有 {self.whack_target} 的地鼠！", fg="#006400")
        self.safe_after(4000, self.whack_moles_hide)
    
    def whack_moles_hide(self):
        if not self.whack_running or self.whack_answered:
            return
        
        self.whack_combo = 0
        self.whack_combo_label.config(text=f"🔥 连击: {self.whack_combo}")
        self.whack_hint.config(text="😅 地鼠跑掉了！下一轮继续！", fg="#FF6B6B")
        
        for i in range(9):
            self.whack_holes[i].config(text="🕳️", bg="#3D2914")
            self.whack_hole_states[i] = None
        
        self.safe_after(1500, self.whack_new_round)
    
    def whack_click(self, idx):
        if not self.whack_running or self.whack_answered:
            return
        
        state = self.whack_hole_states[idx]
        if state is None:
            return
        
        self.whack_answered = True
        
        if state == self.whack_target:
            self.whack_combo += 1
            bonus = min(self.whack_combo * 2, 10)
            points = 10 + bonus
            self.whack_score += points
            self.score += points
            
            self.whack_score_label.config(text=f"⭐ 得分: {self.whack_score}")
            self.whack_combo_label.config(text=f"🔥 连击: {self.whack_combo}")
            
            self.whack_holes[idx].config(text="💥", bg="#32CD32")
            
            if self.whack_combo >= 3:
                self.whack_hint.config(text=f"🎉 太棒了！连击x{self.whack_combo}！+{points}分！", fg="#FF8C00")
            else:
                self.whack_hint.config(text=f"🎉 打中了！{self.whack_target}！+{points}分！", fg="#32CD32")
            
            self.speak_praise()
            
            for i in range(9):
                if i != idx:
                    self.whack_holes[i].config(text="🕳️", bg="#3D2914")
                    self.whack_hole_states[i] = None
            
            self.safe_after(2000, self.whack_new_round)
        else:
            self.whack_combo = 0
            self.whack_combo_label.config(text=f"🔥 连击: {self.whack_combo}")
            
            self.whack_holes[idx].config(text="❌", bg="#808080")
            self.whack_hint.config(text=f"😅 打错了！要找 {self.whack_target} 的地鼠哦！", fg="#FF6B6B")
            self.speak_encourage()
            
            for i in range(9):
                if self.whack_hole_states[i] == self.whack_target:
                    self.whack_holes[i].config(bg="#32CD32")
            
            self.safe_after(2500, self.whack_new_round)


if __name__ == "__main__":
    app = KidsMathApp()
    app.run()
