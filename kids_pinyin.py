# -*- coding: utf-8 -*-
"""
乐乐的拼音乐园 v2.0
适合3岁幼儿的趣味拼音学习

v2.0 更新：继承 BaseGameModule，减少代码重复
"""

import tkinter as tk
from tkinter import messagebox
import random

# 导入基类模块
from base_module import (
    BaseGameModule, logger, TTS_AVAILABLE,
    UI_CONFIG_AVAILABLE, IS_MOBILE
)

# 导入语音配置
try:
    from voice_config_shared import create_rest_reminder
    VOICE_CONFIG_AVAILABLE = True
except ImportError:
    VOICE_CONFIG_AVAILABLE = False

# 导入主题系统
try:
    from theme_config import ThemeHelper
    from theme_drawings import ThemeDrawings
    THEME_AVAILABLE = True
    theme = ThemeHelper()
except ImportError:
    THEME_AVAILABLE = False
    theme = None


class KidsPinyinApp(BaseGameModule):
    """拼音乐园应用 - 继承自 BaseGameModule"""
    
    MODULE_NAME = "pinyin"
    MODULE_TITLE = "乐乐的拼音乐园"
    MODULE_COLOR = "#FF6B6B"
    
    def __init__(self):
        super().__init__()
        
        self.bg_color = theme.bg_color if THEME_AVAILABLE else "#FFE4E1"
        self.window.configure(bg=self.bg_color)
        
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
        
        self.level = 1
        self.init_data()
    
    def cleanup_on_exit(self):
        """退出时清理"""
        try:
            if hasattr(self, 'rest_reminder') and self.rest_reminder:
                self.rest_reminder.stop()
        except:
            pass
        super().cleanup_on_exit()
    
    def set_level(self, level):
        """设置难度等级"""
        self.level = level
        self.init_data()
        total = len(self.vowels) + len(self.consonants)
        self.speak(f"已切换到等级{level}，共{total}个拼音！")
        self.create_main_menu()

    def init_data(self):
        """根据等级初始化拼音数据"""
        VOWELS_L1 = [
            ("a", "啊", "🍎", "阿姨的阿"),
            ("o", "哦", "⭕", "公鸡喔喔叫"),
            ("e", "鹅", "🦢", "白鹅的鹅"),
            ("i", "衣", "👔", "衣服的衣"),
            ("u", "乌", "🐦", "乌鸦的乌"),
            ("ü", "鱼", "🐟", "小鱼的鱼"),
        ]
        CONSONANTS_L1 = [
            ("b", "玻", "🪟", "玻璃的玻"),
            ("p", "坡", "⛰️", "山坡的坡"),
            ("m", "摸", "✋", "摸一摸"),
            ("f", "佛", "🙏", "大佛的佛"),
            ("d", "得", "✅", "得到的得"),
            ("t", "特", "⭐", "特别的特"),
        ]
        CONSONANTS_L2 = [
            ("n", "呢", "👃", "你呢的呢"),
            ("l", "乐", "😊", "快乐的乐"),
            ("g", "哥", "👦", "哥哥的哥"),
            ("k", "科", "🔬", "科学的科"),
            ("h", "喝", "🥤", "喝水的喝"),
            ("j", "鸡", "🐔", "小鸡的鸡"),
        ]
        CONSONANTS_L3 = [
            ("q", "七", "7️⃣", "七个的七"),
            ("x", "西", "🌅", "西瓜的西"),
            ("zh", "知", "📚", "知道的知"),
            ("ch", "吃", "🍽️", "吃饭的吃"),
            ("sh", "十", "🔟", "十个的十"),
            ("r", "日", "☀️", "日出的日"),
        ]
        
        if self.level == 1:
            self.vowels = VOWELS_L1.copy()
            self.consonants = CONSONANTS_L1.copy()
        elif self.level == 2:
            self.vowels = VOWELS_L1.copy()
            self.consonants = CONSONANTS_L1 + CONSONANTS_L2
        else:
            self.vowels = VOWELS_L1.copy()
            self.consonants = CONSONANTS_L1 + CONSONANTS_L2 + CONSONANTS_L3
    
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
    
    def show_paw_feedback_on_canvas(self, canvas, is_correct):
        """在Canvas上显示狗狗反馈"""
        if not THEME_AVAILABLE:
            return
        canvas.delete("all")
        char_id, char_name, _ = random.choice(self.paw_characters)
        draw_func = self.get_character_draw_func(char_id)
        if draw_func:
            w = int(canvas.cget("width"))
            h = int(canvas.cget("height"))
            draw_func(canvas, w//2, h//2 - 10, 0.6)
            if is_correct:
                text = f"{char_name}：太棒了！"
                color = "#4CAF50"
            else:
                text = f"{char_name}：加油！"
                color = "#FF9800"
            canvas.create_text(w//2, h - 12, text=text, font=("微软雅黑", 9, "bold"), fill=color)

    def create_main_menu(self):
        for widget in self.window.winfo_children():
            widget.destroy()
        self.window.configure(bg="#FFE4E1")
        
        main_frame = tk.Frame(self.window, bg="#FFE4E1")
        main_frame.pack(fill=tk.BOTH, expand=True, padx=20, pady=10)
        
        # 标题区域
        if THEME_AVAILABLE:
            title_canvas = tk.Canvas(main_frame, width=800, height=70, bg="#FFE4E1", highlightthickness=0)
            title_canvas.pack(pady=3)
            ThemeDrawings.draw_paw_badge(title_canvas, 60, 35, 30)
            ThemeDrawings.draw_star(title_canvas, 130, 30, 18, "#FFD700")
            title_canvas.create_text(400, 22, text="🔤 乐乐的拼音乐园 🔤", font=("微软雅黑", 26, "bold"), fill="#FF6B6B")
            title_canvas.create_text(400, 50, text="🐾 汪汪队陪你学拼音！ 🐾", font=("微软雅黑", 10), fill="#666")
            ThemeDrawings.draw_star(title_canvas, 670, 30, 18, "#FFD700")
            ThemeDrawings.draw_paw_badge(title_canvas, 740, 35, 30)
        else:
            tk.Label(main_frame, text="🔤 乐乐的拼音乐园 🔤", font=("微软雅黑", 30, "bold"), bg="#FFE4E1", fg="#FF6B6B").pack(pady=5)
        
        # 信息栏：难度和分数
        info_frame = tk.Frame(main_frame, bg="#FFE4E1")
        info_frame.pack(pady=5)
        
        level_frame = tk.Frame(info_frame, bg="#4ECDC4", relief=tk.RAISED, bd=3)
        level_frame.pack(side=tk.LEFT, padx=10)
        tk.Label(level_frame, text="📊 难度等级", font=("微软雅黑", 10, "bold"), bg="#4ECDC4", fg="white").pack(pady=2)
        level_btn_frame = tk.Frame(level_frame, bg="#4ECDC4")
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
        
        score_frame = tk.Frame(info_frame, bg="#FF6B6B", relief=tk.RAISED, bd=3)
        score_frame.pack(side=tk.LEFT, padx=10)
        tk.Label(score_frame, text=f"⭐ 总分: {self.score} ⭐", font=("微软雅黑", 14, "bold"), bg="#FF6B6B", fg="white", padx=20, pady=5).pack()
        total = len(self.vowels) + len(self.consonants)
        tk.Label(score_frame, text=f"当前拼音: {total}个", font=("微软雅黑", 9), bg="#FF6B6B", fg="white").pack(pady=(0,3))
        
        # ========== 简单游戏区（3岁+）==========
        easy_section = tk.LabelFrame(main_frame, text="🌟 简单模式（3岁+）", 
                                     font=("微软雅黑", 12, "bold"), bg="#E8F5E9", 
                                     fg="#2E7D32", relief=tk.GROOVE, bd=3)
        easy_section.pack(fill=tk.X, pady=8, padx=5)
        
        easy_frame = tk.Frame(easy_section, bg="#E8F5E9")
        easy_frame.pack(pady=8)
        
        easy_modes = [
            ("🔤\n韵母卡片", "#FF6B6B", "学韵母", self.start_vowels),
            ("🔤\n声母卡片", "#4ECDC4", "学声母", self.start_consonants),
            ("👂\n听音选拼音", "#45B7D1", "听声音", self.start_listen),
        ]
        
        for i, (title, color, desc, command) in enumerate(easy_modes):
            card = tk.Frame(easy_frame, bg=color, relief=tk.RAISED, bd=4)
            card.grid(row=0, column=i, padx=20, pady=5)
            btn = tk.Button(card, text=title, font=("微软雅黑", 16, "bold"), bg=color, fg="white", 
                           width=10, height=3, relief=tk.FLAT, cursor="hand2", command=command)
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
            ("🖼️\n看图选拼音", "#96CEB4", "看图片", self.start_picture),
            ("🎯\n拼音配对", "#DDA0DD", "找配对", self.start_match),
            ("🔨\n拼音打地鼠", "#FFD93D", "快反应", self.start_whack),
        ]
        
        for i, (title, color, desc, command) in enumerate(advanced_modes):
            card = tk.Frame(advanced_frame, bg=color, relief=tk.RAISED, bd=4)
            card.grid(row=0, column=i, padx=20, pady=5)
            btn = tk.Button(card, text=title, font=("微软雅黑", 16, "bold"), bg=color, fg="white", 
                           width=10, height=3, relief=tk.FLAT, cursor="hand2", command=command)
            btn.pack(padx=5, pady=5)
            tk.Label(card, text=desc, font=("微软雅黑", 10), bg=color, fg="white").pack(pady=3)
        
        # 底部狗狗装饰
        if THEME_AVAILABLE:
            bottom_canvas = tk.Canvas(main_frame, width=800, height=70, bg="#FFE4E1", highlightthickness=0)
            bottom_canvas.pack(pady=5)
            bottom_canvas.create_rectangle(0, 45, 800, 70, fill="#81C784", outline="")
            ThemeDrawings.draw_puppy_marshall(bottom_canvas, 150, 32, 0.4)
            ThemeDrawings.draw_puppy_rubble(bottom_canvas, 320, 32, 0.4)
            ThemeDrawings.draw_puppy_rocky(bottom_canvas, 490, 32, 0.4)
            ThemeDrawings.draw_puppy_zuma(bottom_canvas, 660, 32, 0.4)
        
        tk.Button(main_frame, text="👋 退出", font=("微软雅黑", 11), bg="#FF6B6B", fg="white", relief=tk.RAISED, bd=3, cursor="hand2", command=self.on_close_window).pack(pady=8)
    
    def clear_game_area(self, bg_color="#FFE4E1"):
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
        tk.Button(nav_frame, text="🏠 返回主菜单", font=("微软雅黑", 11), bg="#96CEB4", fg="white", relief=tk.RAISED, bd=3, cursor="hand2", command=self.create_main_menu).pack(side=tk.LEFT, padx=10)
        tk.Label(nav_frame, text=f"⭐ 总分: {self.score}", font=("微软雅黑", 12, "bold"), bg=bg_color, fg="#FF6B6B").pack(side=tk.RIGHT, padx=10)
        self.game_frame = tk.Frame(self.window, bg=bg_color)
        self.game_frame.pack(fill=tk.BOTH, expand=True, padx=20, pady=10)

    # =====================================================
    # 韵母卡片
    # =====================================================
    def start_vowels(self):
        self.clear_game_area("#FFF8DC")
        self.vowel_index = 0
        tk.Label(self.game_frame, text="🔤 韵母卡片", font=("微软雅黑", 26, "bold"), bg="#FFF8DC", fg="#FF6B6B").pack(pady=5)
        self.vowel_progress = tk.Label(self.game_frame, text="", font=("微软雅黑", 11), bg="#FFF8DC", fg="#666")
        self.vowel_progress.pack(pady=5)
        card = tk.Frame(self.game_frame, bg="white", relief=tk.RAISED, bd=4)
        card.pack(pady=10, padx=80, fill=tk.X)
        self.vowel_pinyin = tk.Label(card, text="", font=("Arial", 100, "bold"), bg="white", fg="#FF6B6B")
        self.vowel_pinyin.pack(pady=15)
        self.vowel_emoji = tk.Label(card, text="", font=("Segoe UI Emoji", 60), bg="white")
        self.vowel_emoji.pack(pady=10)
        self.vowel_desc = tk.Label(card, text="", font=("微软雅黑", 18), bg="white", fg="#666")
        self.vowel_desc.pack(pady=10)
        btn_frame = tk.Frame(self.game_frame, bg="#FFF8DC")
        btn_frame.pack(pady=15)
        tk.Button(btn_frame, text="⬅️ 上一个", font=("微软雅黑", 11), bg="#45B7D1", fg="white", command=self.prev_vowel, width=10).pack(side=tk.LEFT, padx=5)
        tk.Button(btn_frame, text="🔊 读一读", font=("微软雅黑", 11), bg="#FF6B6B", fg="white", command=self.speak_vowel, width=10).pack(side=tk.LEFT, padx=5)
        tk.Button(btn_frame, text="下一个 ➡️", font=("微软雅黑", 11), bg="#45B7D1", fg="white", command=self.next_vowel, width=10).pack(side=tk.LEFT, padx=5)
        self.show_vowel()
    
    def show_vowel(self):
        v = self.vowels[self.vowel_index]
        self.vowel_pinyin.config(text=v[0])
        self.vowel_emoji.config(text=v[2])
        self.vowel_desc.config(text=v[3])
        self.vowel_progress.config(text=f"第 {self.vowel_index + 1} / {len(self.vowels)} 个韵母")
        self.speak(f"{v[0]}，{v[1]}，{v[3]}", "-10%")
    
    def speak_vowel(self):
        v = self.vowels[self.vowel_index]
        self.speak(f"{v[0]}，{v[0]}，{v[3]}", "-10%")
    
    def next_vowel(self):
        self.vowel_index = (self.vowel_index + 1) % len(self.vowels)
        self.show_vowel()
    
    def prev_vowel(self):
        self.vowel_index = (self.vowel_index - 1) % len(self.vowels)
        self.show_vowel()

    # =====================================================
    # 声母卡片
    # =====================================================
    def start_consonants(self):
        self.clear_game_area("#E0FFFF")
        self.cons_index = 0
        tk.Label(self.game_frame, text="🔤 声母卡片", font=("微软雅黑", 26, "bold"), bg="#E0FFFF", fg="#4ECDC4").pack(pady=5)
        self.cons_progress = tk.Label(self.game_frame, text="", font=("微软雅黑", 11), bg="#E0FFFF", fg="#666")
        self.cons_progress.pack(pady=5)
        card = tk.Frame(self.game_frame, bg="white", relief=tk.RAISED, bd=4)
        card.pack(pady=10, padx=80, fill=tk.X)
        self.cons_pinyin = tk.Label(card, text="", font=("Arial", 100, "bold"), bg="white", fg="#4ECDC4")
        self.cons_pinyin.pack(pady=15)
        self.cons_emoji = tk.Label(card, text="", font=("Segoe UI Emoji", 60), bg="white")
        self.cons_emoji.pack(pady=10)
        self.cons_desc = tk.Label(card, text="", font=("微软雅黑", 18), bg="white", fg="#666")
        self.cons_desc.pack(pady=10)
        btn_frame = tk.Frame(self.game_frame, bg="#E0FFFF")
        btn_frame.pack(pady=15)
        tk.Button(btn_frame, text="⬅️ 上一个", font=("微软雅黑", 11), bg="#45B7D1", fg="white", command=self.prev_cons, width=10).pack(side=tk.LEFT, padx=5)
        tk.Button(btn_frame, text="🔊 读一读", font=("微软雅黑", 11), bg="#FF6B6B", fg="white", command=self.speak_cons, width=10).pack(side=tk.LEFT, padx=5)
        tk.Button(btn_frame, text="下一个 ➡️", font=("微软雅黑", 11), bg="#45B7D1", fg="white", command=self.next_cons, width=10).pack(side=tk.LEFT, padx=5)
        self.show_cons()
    
    def show_cons(self):
        c = self.consonants[self.cons_index]
        self.cons_pinyin.config(text=c[0])
        self.cons_emoji.config(text=c[2])
        self.cons_desc.config(text=c[3])
        self.cons_progress.config(text=f"第 {self.cons_index + 1} / {len(self.consonants)} 个声母")
        self.speak(f"{c[0]}，{c[1]}，{c[3]}", "-10%")
    
    def speak_cons(self):
        c = self.consonants[self.cons_index]
        self.speak(f"{c[0]}，{c[0]}，{c[3]}", "-10%")
    
    def next_cons(self):
        self.cons_index = (self.cons_index + 1) % len(self.consonants)
        self.show_cons()
    
    def prev_cons(self):
        self.cons_index = (self.cons_index - 1) % len(self.consonants)
        self.show_cons()

    # =====================================================
    # 听音选拼音
    # =====================================================
    def start_listen(self):
        self.clear_game_area("#FFE4E1")
        self.listen_score = 0
        
        if THEME_AVAILABLE:
            title_canvas = tk.Canvas(self.game_frame, width=600, height=70, bg="#FFE4E1", highlightthickness=0)
            title_canvas.pack(pady=5)
            title_canvas.create_text(300, 22, text="🐾 听音选拼音 🐾", font=("微软雅黑", 24, "bold"), fill="#45B7D1")
            title_canvas.create_text(300, 52, text="听声音，选拼音！", font=("微软雅黑", 11), fill="#666")
            ThemeDrawings.draw_paw_badge(title_canvas, 50, 35, 28)
            ThemeDrawings.draw_paw_badge(title_canvas, 550, 35, 28)
        else:
            tk.Label(self.game_frame, text="👂 听音选拼音", font=("微软雅黑", 26, "bold"), bg="#FFE4E1", fg="#45B7D1").pack(pady=5)
        
        self.listen_score_label = tk.Label(self.game_frame, text="⭐ 得分: 0", font=("微软雅黑", 14), bg="#FFE4E1", fg="#666")
        self.listen_score_label.pack(pady=5)
        tk.Button(self.game_frame, text="🔊 再听一遍", font=("微软雅黑", 12), bg="#FF6B6B", fg="white", command=self.replay_listen).pack(pady=10)
        self.listen_hint = tk.Label(self.game_frame, text="", font=("微软雅黑", 18), bg="#FFE4E1")
        self.listen_hint.pack(pady=5)
        
        self.listen_feedback_canvas = tk.Canvas(self.game_frame, width=180, height=100, bg="#FFE4E1", highlightthickness=0)
        self.listen_feedback_canvas.pack(pady=5)
        
        self.listen_frame = tk.Frame(self.game_frame, bg="#FFE4E1")
        self.listen_frame.pack(pady=20)
        self.listen_buttons = []
        colors = ["#FF6B6B", "#4ECDC4", "#45B7D1", "#96CEB4"]
        for i in range(4):
            btn = tk.Button(self.listen_frame, text="", font=("Arial", 36, "bold"), width=4, height=2, bg=colors[i], fg="white", relief=tk.RAISED, bd=4, cursor="hand2", command=lambda idx=i: self.check_listen(idx))
            btn.grid(row=0, column=i, padx=15)
            self.listen_buttons.append(btn)
        self.new_listen_question()
    
    def new_listen_question(self):
        all_pinyin = self.vowels + self.consonants
        self.listen_target = random.choice(all_pinyin)
        others = random.sample([p for p in all_pinyin if p != self.listen_target], 3)
        self.listen_options = [self.listen_target] + others
        random.shuffle(self.listen_options)
        self.listen_correct_idx = self.listen_options.index(self.listen_target)
        colors = ["#FF6B6B", "#4ECDC4", "#45B7D1", "#96CEB4"]
        for i, btn in enumerate(self.listen_buttons):
            btn.config(text=self.listen_options[i][0], bg=colors[i], state=tk.NORMAL)
        self.listen_hint.config(text="", fg="#666")
        self.speak(f"请选择，{self.listen_target[0]}", "-10%")
    
    def replay_listen(self):
        self.speak(f"{self.listen_target[0]}", "-10%")
    
    def check_listen(self, idx):
        if hasattr(self, 'listen_feedback_canvas'):
            self.listen_feedback_canvas.delete("all")
        
        if idx == self.listen_correct_idx:
            self.listen_score += 10
            self.score += 10
            self.listen_hint.config(text=f"🎉 对啦！是{self.listen_target[0]}！", fg="#32CD32")
            self.listen_buttons[idx].config(bg="#32CD32")
            if THEME_AVAILABLE:
                self.show_paw_feedback_on_canvas(self.listen_feedback_canvas, True)
            self.speak_praise()
        else:
            self.listen_hint.config(text=f"😅 是{self.listen_target[0]}哦！", fg="#FF6B6B")
            self.listen_buttons[idx].config(bg="#808080")
            self.listen_buttons[self.listen_correct_idx].config(bg="#32CD32")
            if THEME_AVAILABLE:
                self.show_paw_feedback_on_canvas(self.listen_feedback_canvas, False)
            self.speak_encourage()
        self.listen_score_label.config(text=f"⭐ 得分: {self.listen_score}")
        for btn in self.listen_buttons:
            btn.config(state=tk.DISABLED)
        self.safe_after(5500, self.new_listen_question)

    # =====================================================
    # 看图选拼音
    # =====================================================
    def start_picture(self):
        self.clear_game_area("#E8F5E9")
        self.pic_score = 0
        
        if THEME_AVAILABLE:
            title_canvas = tk.Canvas(self.game_frame, width=600, height=70, bg="#E8F5E9", highlightthickness=0)
            title_canvas.pack(pady=5)
            title_canvas.create_text(300, 22, text="🐾 看图选拼音 🐾", font=("微软雅黑", 24, "bold"), fill="#96CEB4")
            title_canvas.create_text(300, 52, text="看图片，选拼音！", font=("微软雅黑", 11), fill="#666")
            ThemeDrawings.draw_puppy_skye(title_canvas, 60, 40, 0.4)
            ThemeDrawings.draw_puppy_everest(title_canvas, 540, 40, 0.4)
        else:
            tk.Label(self.game_frame, text="🖼️ 看图选拼音", font=("微软雅黑", 26, "bold"), bg="#E8F5E9", fg="#96CEB4").pack(pady=5)
        
        self.pic_score_label = tk.Label(self.game_frame, text="⭐ 得分: 0", font=("微软雅黑", 14), bg="#E8F5E9", fg="#666")
        self.pic_score_label.pack(pady=5)
        self.pic_emoji = tk.Label(self.game_frame, text="", font=("Segoe UI Emoji", 100), bg="white", relief=tk.RAISED, bd=4, padx=30, pady=15)
        self.pic_emoji.pack(pady=15)
        self.pic_hint = tk.Label(self.game_frame, text="", font=("微软雅黑", 18), bg="#E8F5E9")
        self.pic_hint.pack(pady=5)
        
        self.pic_feedback_canvas = tk.Canvas(self.game_frame, width=180, height=100, bg="#E8F5E9", highlightthickness=0)
        self.pic_feedback_canvas.pack(pady=5)
        
        self.pic_frame = tk.Frame(self.game_frame, bg="#E8F5E9")
        self.pic_frame.pack(pady=20)
        self.pic_buttons = []
        colors = ["#FF6B6B", "#4ECDC4", "#45B7D1", "#96CEB4"]
        for i in range(4):
            btn = tk.Button(self.pic_frame, text="", font=("Arial", 36, "bold"), width=4, height=2, bg=colors[i], fg="white", relief=tk.RAISED, bd=4, cursor="hand2", command=lambda idx=i: self.check_picture(idx))
            btn.grid(row=0, column=i, padx=15)
            self.pic_buttons.append(btn)
        self.new_picture_question()
    
    def new_picture_question(self):
        all_pinyin = self.vowels + self.consonants
        self.pic_target = random.choice(all_pinyin)
        others = random.sample([p for p in all_pinyin if p != self.pic_target], 3)
        self.pic_options = [self.pic_target] + others
        random.shuffle(self.pic_options)
        self.pic_correct_idx = self.pic_options.index(self.pic_target)
        self.pic_emoji.config(text=self.pic_target[2])
        colors = ["#FF6B6B", "#4ECDC4", "#45B7D1", "#96CEB4"]
        for i, btn in enumerate(self.pic_buttons):
            btn.config(text=self.pic_options[i][0], bg=colors[i], state=tk.NORMAL)
        self.pic_hint.config(text="", fg="#666")
        self.speak("看图片，选拼音！", "-10%")
    
    def check_picture(self, idx):
        if hasattr(self, 'pic_feedback_canvas'):
            self.pic_feedback_canvas.delete("all")
        
        if idx == self.pic_correct_idx:
            self.pic_score += 10
            self.score += 10
            self.pic_hint.config(text=f"🎉 对啦！是{self.pic_target[0]}！", fg="#32CD32")
            self.pic_buttons[idx].config(bg="#32CD32")
            if THEME_AVAILABLE:
                self.show_paw_feedback_on_canvas(self.pic_feedback_canvas, True)
            self.speak_praise()
        else:
            self.pic_hint.config(text=f"😅 是{self.pic_target[0]}哦！", fg="#FF6B6B")
            self.pic_buttons[idx].config(bg="#808080")
            self.pic_buttons[self.pic_correct_idx].config(bg="#32CD32")
            if THEME_AVAILABLE:
                self.show_paw_feedback_on_canvas(self.pic_feedback_canvas, False)
            self.speak_encourage()
        self.pic_score_label.config(text=f"⭐ 得分: {self.pic_score}")
        for btn in self.pic_buttons:
            btn.config(state=tk.DISABLED)
        self.safe_after(5500, self.new_picture_question)

    # =====================================================
    # 拼音配对
    # =====================================================
    def start_match(self):
        self.clear_game_area("#FFFACD")
        self.match_score = 0
        self.match_selected = None
        self.match_cards = []
        self.match_card_data = []
        self.match_matched = set()
        
        tk.Label(self.game_frame, text="🎯 拼音找朋友", font=("微软雅黑", 26, "bold"), bg="#FFFACD", fg="#FF6B6B").pack(pady=5)
        self.match_score_label = tk.Label(self.game_frame, text="⭐ 得分: 0", font=("微软雅黑", 14), bg="#FFFACD", fg="#666")
        self.match_score_label.pack(pady=5)
        tk.Label(self.game_frame, text="找到拼音和它的图片朋友！", font=("微软雅黑", 13), bg="#FFFACD", fg="#888").pack(pady=5)
        self.match_hint = tk.Label(self.game_frame, text="", font=("微软雅黑", 16), bg="#FFFACD")
        self.match_hint.pack(pady=5)
        
        cards_frame = tk.Frame(self.game_frame, bg="#FFFACD")
        cards_frame.pack(pady=15)
        
        all_items = self.consonants[:3] + self.vowels[:3]
        selected = random.sample(all_items, min(6, len(all_items)))
        
        for item in selected:
            self.match_card_data.append({"type": "pinyin", "pinyin": item[0], "match_id": item[0]})
            self.match_card_data.append({"type": "emoji", "emoji": item[2], "pinyin": item[0], "match_id": item[0]})
        
        random.shuffle(self.match_card_data)
        
        colors = ["#FFB6C1", "#98FB98", "#87CEEB", "#DDA0DD", "#F0E68C", "#FFA07A",
                  "#B0E0E6", "#FFE4B5", "#E6E6FA", "#FFDAB9", "#D8BFD8", "#F5DEB3"]
        
        for i in range(12):
            row = i // 4
            col = i % 4
            card_data = self.match_card_data[i]
            if card_data["type"] == "pinyin":
                text = card_data["pinyin"]
                font = ("Arial", 32, "bold")
            else:
                text = card_data["emoji"]
                font = ("Segoe UI Emoji", 32)
            
            btn = tk.Button(cards_frame, text="❓", font=("Segoe UI Emoji", 32), width=3, height=1, bg=colors[i], fg="#333", relief=tk.RAISED, bd=4, cursor="hand2", command=lambda idx=i: self.match_click(idx))
            btn.grid(row=row, column=col, padx=10, pady=10)
            btn.card_text = text
            btn.card_font = font
            btn.card_color = colors[i]
            self.match_cards.append(btn)
        
        self.speak("拼音找朋友开始！找到拼音和图片配对！", "+0%")
        self.match_show_all()
    
    def match_show_all(self):
        for btn in self.match_cards:
            btn.config(text=btn.card_text, font=btn.card_font)
        self.match_hint.config(text="👀 记住位置！3秒后翻回去...", fg="#FF8C00")
        self.safe_after(3000, self.match_hide_all)
    
    def match_hide_all(self):
        for i, btn in enumerate(self.match_cards):
            if i not in self.match_matched:
                btn.config(text="❓", font=("Segoe UI Emoji", 32))
        self.match_hint.config(text="点击卡片找朋友！", fg="#666")
    
    def match_click(self, idx):
        if idx in self.match_matched:
            return
        
        btn = self.match_cards[idx]
        btn.config(text=btn.card_text, font=btn.card_font)
        
        if self.match_selected is None:
            self.match_selected = idx
            btn.config(relief=tk.SUNKEN)
        else:
            first_idx = self.match_selected
            first_btn = self.match_cards[first_idx]
            first_data = self.match_card_data[first_idx]
            second_data = self.match_card_data[idx]
            
            if first_data["match_id"] == second_data["match_id"] and first_idx != idx:
                self.match_score += 20
                self.score += 20
                self.match_score_label.config(text=f"⭐ 得分: {self.match_score}")
                self.match_matched.add(first_idx)
                self.match_matched.add(idx)
                first_btn.config(bg="#32CD32", relief=tk.FLAT)
                btn.config(bg="#32CD32", relief=tk.FLAT)
                pinyin = first_data["match_id"]
                self.match_hint.config(text=f"🎉 太棒了！{pinyin} 找到朋友了！", fg="#32CD32")
                self.speak_praise()
                if len(self.match_matched) == 12:
                    self.safe_after(1500, self.match_complete)
            else:
                self.match_hint.config(text="😅 不是朋友，再试试！", fg="#FF6B6B")
                self.speak_encourage()
                self.safe_after(1500, lambda: self.match_flip_back(first_idx, idx))
            
            self.match_selected = None
            first_btn.config(relief=tk.RAISED)
    
    def match_flip_back(self, idx1, idx2):
        if idx1 not in self.match_matched:
            self.match_cards[idx1].config(text="❓", font=("Segoe UI Emoji", 32))
        if idx2 not in self.match_matched:
            self.match_cards[idx2].config(text="❓", font=("Segoe UI Emoji", 32))
    
    def match_complete(self):
        self.match_hint.config(text=f"🏆 太厉害了！全部配对成功！得分：{self.match_score}", fg="#FF6B6B")
        self.speak(f"太棒了！乐乐全部配对成功！", "+0%")
        self.safe_after(5500, self.create_main_menu)

    # =====================================================
    # 拼音打地鼠
    # =====================================================
    def start_whack(self):
        self.clear_game_area("#90EE90")
        self.py_whack_score = 0
        self.py_whack_running = True
        self.py_whack_holes = []
        self.py_whack_states = [None] * 9
        self.py_whack_answered = False
        
        tk.Label(self.game_frame, text="🔨 拼音打地鼠", font=("微软雅黑", 26, "bold"), bg="#90EE90", fg="#228B22").pack(pady=5)
        
        info_frame = tk.Frame(self.game_frame, bg="#90EE90")
        info_frame.pack(pady=8)
        self.py_whack_score_label = tk.Label(info_frame, text="⭐ 得分: 0", font=("微软雅黑", 14, "bold"), bg="#90EE90", fg="#FF6B6B")
        self.py_whack_score_label.pack(side=tk.LEFT, padx=20)
        
        target_frame = tk.Frame(self.game_frame, bg="#FFD700", relief=tk.RAISED, bd=4)
        target_frame.pack(pady=10)
        tk.Label(target_frame, text="🎯 打这个拼音的地鼠：", font=("微软雅黑", 16), bg="#FFD700", fg="#333").pack(side=tk.LEFT, padx=10, pady=10)
        self.py_whack_target_label = tk.Label(target_frame, text="", font=("Arial", 50, "bold"), bg="#FFD700", fg="#DC143C")
        self.py_whack_target_label.pack(side=tk.LEFT, padx=15, pady=10)
        
        self.py_whack_hint = tk.Label(self.game_frame, text="", font=("微软雅黑", 13), bg="#90EE90", fg="#006400")
        self.py_whack_hint.pack(pady=5)
        
        holes_frame = tk.Frame(self.game_frame, bg="#228B22", relief=tk.RIDGE, bd=6)
        holes_frame.pack(pady=10)
        
        for i in range(9):
            row = i // 3
            col = i % 3
            hole_outer = tk.Frame(holes_frame, bg="#8B4513", relief=tk.SUNKEN, bd=4)
            hole_outer.grid(row=row, column=col, padx=12, pady=12)
            btn = tk.Button(hole_outer, text="🕳️", font=("Segoe UI Emoji", 28), width=4, height=2, bg="#3D2914", fg="#333", relief=tk.SUNKEN, bd=3, cursor="hand2", command=lambda idx=i: self.py_whack_click(idx))
            btn.pack(padx=4, pady=4)
            self.py_whack_holes.append(btn)
        
        self.speak("拼音打地鼠开始！打掉正确拼音的地鼠！", "+0%")
        self.safe_after(2000, self.py_whack_new_round)
    
    def py_whack_new_round(self):
        if not self.py_whack_running:
            return
        self.py_whack_answered = False
        for i in range(9):
            self.py_whack_holes[i].config(text="🕳️", bg="#3D2914", state=tk.NORMAL)
            self.py_whack_states[i] = None
        
        all_pinyin = self.consonants + self.vowels
        self.py_whack_target = random.choice(all_pinyin)
        others = random.sample([p for p in all_pinyin if p != self.py_whack_target], 3)
        self.py_whack_options = [self.py_whack_target] + others
        self.py_whack_target_pinyin = self.py_whack_target[0]
        self.py_whack_target_label.config(text=self.py_whack_target_pinyin)
        self.speak(f"打，{self.py_whack_target_pinyin}", "+10%")
        self.safe_after(800, self.py_whack_show_moles)
    
    def py_whack_show_moles(self):
        if not self.py_whack_running or self.py_whack_answered:
            return
        num_moles = random.randint(3, 4)
        positions = random.sample(range(9), num_moles)
        correct_pos = random.choice(positions)
        random.shuffle(self.py_whack_options)
        idx = 0
        for pos in positions:
            if pos == correct_pos:
                pinyin = self.py_whack_target_pinyin
            else:
                pinyin = self.py_whack_options[idx][0] if idx < len(self.py_whack_options) else "a"
                idx += 1
            self.py_whack_holes[pos].config(text=f"🐹\n{pinyin}", bg="#FFE4B5")
            self.py_whack_states[pos] = pinyin
        self.py_whack_hint.config(text=f"快打 {self.py_whack_target_pinyin} 的地鼠！", fg="#006400")
        self.safe_after(4000, self.py_whack_hide)
    
    def py_whack_hide(self):
        if not self.py_whack_running or self.py_whack_answered:
            return
        self.py_whack_hint.config(text="😅 地鼠跑掉了！", fg="#FF6B6B")
        for i in range(9):
            self.py_whack_holes[i].config(text="🕳️", bg="#3D2914")
            self.py_whack_states[i] = None
        self.safe_after(1500, self.py_whack_new_round)
    
    def py_whack_click(self, idx):
        if not self.py_whack_running or self.py_whack_answered:
            return
        state = self.py_whack_states[idx]
        if state is None:
            return
        self.py_whack_answered = True
        if state == self.py_whack_target_pinyin:
            self.py_whack_score += 10
            self.score += 10
            self.py_whack_score_label.config(text=f"⭐ 得分: {self.py_whack_score}")
            self.py_whack_holes[idx].config(text="💥", bg="#32CD32")
            self.py_whack_hint.config(text=f"🎉 打中了！{self.py_whack_target_pinyin}！+10分！", fg="#32CD32")
            self.speak_praise()
            for i in range(9):
                if i != idx:
                    self.py_whack_holes[i].config(text="🕳️", bg="#3D2914")
            self.safe_after(2000, self.py_whack_new_round)
        else:
            self.py_whack_holes[idx].config(text="❌", bg="#808080")
            self.py_whack_hint.config(text=f"😅 打错了！要找 {self.py_whack_target_pinyin}！", fg="#FF6B6B")
            self.speak_encourage()
            for i in range(9):
                if self.py_whack_states[i] == self.py_whack_target_pinyin:
                    self.py_whack_holes[i].config(bg="#32CD32")
            self.safe_after(2500, self.py_whack_new_round)


if __name__ == "__main__":
    app = KidsPinyinApp()
    app.run()
