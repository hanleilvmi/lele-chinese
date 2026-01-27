# -*- coding: utf-8 -*-
"""
乐乐的英语乐园 v1.0
适合3岁幼儿的趣味英语学习
"""

import tkinter as tk
from tkinter import messagebox
import random
import threading
import asyncio
import os
import tempfile
import uuid
import time
import atexit

try:
    import edge_tts
    import pygame
    pygame.mixer.init()
    TTS_AVAILABLE = True
except ImportError:
    TTS_AVAILABLE = False

# 导入UI配置模块
try:
    from ui_config import (
        UI, Colors, ScreenConfig, get_font, get_path, 
        get_data_path, IS_MOBILE, PLATFORM
    )
    UI_CONFIG_AVAILABLE = True
except ImportError:
    UI_CONFIG_AVAILABLE = False
    IS_MOBILE = False

try:
    from voice_config_shared import get_voice, get_praises, get_encourages, create_rest_reminder
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


class KidsEnglishApp:
    def __init__(self):
        self.window = tk.Tk()
        self.window.title("🔤 乐乐的英语乐园 🔤")
        
        # 设置窗口大小并居中
        window_width = 1100
        window_height = 850
        screen_width = self.window.winfo_screenwidth()
        screen_height = self.window.winfo_screenheight()
        x = (screen_width - window_width) // 2
        y = (screen_height - window_height) // 2 - 30
        self.window.geometry(f"{window_width}x{window_height}+{x}+{y}")
        
        # 使用主题背景色
        self.bg_color = theme.bg_color if THEME_AVAILABLE else "#E0F7FA"
        self.window.configure(bg=self.bg_color)
        
        # 汪汪队角色列表（用于随机显示）
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
        
        self.tts_lock = threading.Lock()
        if VOICE_CONFIG_AVAILABLE:
            self.cn_voice = get_voice()
            self.praises = get_praises()
            self.encourages = get_encourages()
        else:
            self.cn_voice = "zh-CN-YunxiNeural"
            self.praises = ["太棒了！", "真厉害！", "答对啦！"]
            self.encourages = ["加油！", "再试一次！", "没关系！"]
        self.en_voice = "en-US-AnaNeural"
        self.temp_dir = tempfile.gettempdir()
        
        self.audio_dir = os.path.join(os.path.dirname(os.path.abspath(__file__)), "audio")
        self.praise_audios = self._scan_audio_folder("praise")
        self.encourage_audios = self._scan_audio_folder("encourage")
        
        # 定时器管理
        self.pending_timers = []
        
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
        
        # 设置窗口关闭处理
        self.window.protocol("WM_DELETE_WINDOW", self.on_close_window)
        atexit.register(self.cleanup_on_exit)
        
        # 等级设置
        self.level = 1
        
        self.score = 0
        self.game_frame = None
        self.init_data()
        self.create_main_menu()
    
    def on_close_window(self):
        """窗口关闭处理"""
        result = messagebox.askyesno(
            "👋 确认退出",
            "确定要退出英语乐园吗？",
            icon='question',
            default='yes'
        )
        if result:
            self.cleanup_on_exit()
            self.window.quit()
    
    def cleanup_on_exit(self):
        """退出时清理"""
        try:
            for timer_id in self.pending_timers:
                try:
                    self.window.after_cancel(timer_id)
                except:
                    pass
            self.pending_timers.clear()
            if hasattr(self, 'rest_reminder') and self.rest_reminder:
                self.rest_reminder.stop()
            try:
                pygame.mixer.music.stop()
            except:
                pass
        except Exception as e:
            print(f"清理错误: {e}")
    
    def set_level(self, level):
        """手动设置难度等级"""
        self.level = level
        self.init_data()
        total = len(self.letters) + len(self.animals)
        self.speak(f"已切换到等级{level}！", lang="cn")
        self.create_main_menu()
    
    def init_data(self):
        """根据等级初始化英语数据"""
        # 等级1: A-L (12个字母)
        LETTERS_L1 = [
            ("A", "Apple", "🍎", "苹果"), ("B", "Ball", "⚽", "球"), ("C", "Cat", "🐱", "猫"),
            ("D", "Dog", "🐕", "狗"), ("E", "Elephant", "🐘", "大象"), ("F", "Fish", "🐟", "鱼"),
            ("G", "Grape", "🍇", "葡萄"), ("H", "House", "🏠", "房子"), ("I", "Ice cream", "🍦", "冰淇淋"),
            ("J", "Juice", "🧃", "果汁"), ("K", "Kite", "🪁", "风筝"), ("L", "Lion", "🦁", "狮子"),
        ]
        
        # 等级2: M-R (6个字母)
        LETTERS_L2 = [
            ("M", "Moon", "🌙", "月亮"), ("N", "Nose", "👃", "鼻子"), ("O", "Orange", "🍊", "橙子"),
            ("P", "Pig", "🐷", "猪"), ("Q", "Queen", "👸", "女王"), ("R", "Rabbit", "🐰", "兔子"),
        ]
        
        # 等级3: S-Z (8个字母)
        LETTERS_L3 = [
            ("S", "Sun", "☀️", "太阳"), ("T", "Tree", "🌳", "树"), ("U", "Umbrella", "☂️", "雨伞"),
            ("V", "Violin", "🎻", "小提琴"), ("W", "Water", "💧", "水"), ("X", "X-ray", "🩻", "X光"),
            ("Y", "Yellow", "💛", "黄色"), ("Z", "Zebra", "🦓", "斑马"),
        ]
        
        # 根据等级加载
        if self.level == 1:
            self.letters = LETTERS_L1.copy()
        elif self.level == 2:
            self.letters = LETTERS_L1 + LETTERS_L2
        else:
            self.letters = LETTERS_L1 + LETTERS_L2 + LETTERS_L3
        self.numbers = [
            {"num": 1, "en": "One", "emoji": "1️⃣", "cn": "一"},
            {"num": 2, "en": "Two", "emoji": "2️⃣", "cn": "二"},
            {"num": 3, "en": "Three", "emoji": "3️⃣", "cn": "三"},
            {"num": 4, "en": "Four", "emoji": "4️⃣", "cn": "四"},
            {"num": 5, "en": "Five", "emoji": "5️⃣", "cn": "五"},
            {"num": 6, "en": "Six", "emoji": "6️⃣", "cn": "六"},
            {"num": 7, "en": "Seven", "emoji": "7️⃣", "cn": "七"},
            {"num": 8, "en": "Eight", "emoji": "8️⃣", "cn": "八"},
            {"num": 9, "en": "Nine", "emoji": "9️⃣", "cn": "九"},
            {"num": 10, "en": "Ten", "emoji": "🔟", "cn": "十"},
        ]
        self.colors_data = [
            {"en": "Red", "cn": "红色", "emoji": "🔴", "hex": "#FF0000"},
            {"en": "Blue", "cn": "蓝色", "emoji": "🔵", "hex": "#1E90FF"},
            {"en": "Green", "cn": "绿色", "emoji": "🟢", "hex": "#32CD32"},
            {"en": "Yellow", "cn": "黄色", "emoji": "🟡", "hex": "#FFD700"},
            {"en": "Orange", "cn": "橙色", "emoji": "🟠", "hex": "#FFA500"},
            {"en": "Purple", "cn": "紫色", "emoji": "🟣", "hex": "#9932CC"},
            {"en": "Pink", "cn": "粉色", "emoji": "💗", "hex": "#FF69B4"},
            {"en": "Black", "cn": "黑色", "emoji": "⚫", "hex": "#000000"},
        ]
        self.animals = [
            {"en": "Cat", "cn": "猫", "emoji": "🐱", "sound": "meow"},
            {"en": "Dog", "cn": "狗", "emoji": "🐕", "sound": "woof"},
            {"en": "Bird", "cn": "鸟", "emoji": "🐦", "sound": "tweet"},
            {"en": "Fish", "cn": "鱼", "emoji": "🐟", "sound": "blub"},
            {"en": "Rabbit", "cn": "兔子", "emoji": "🐰", "sound": "hop"},
            {"en": "Bear", "cn": "熊", "emoji": "🐻", "sound": "growl"},
            {"en": "Monkey", "cn": "猴子", "emoji": "🐵", "sound": "ooh ooh"},
            {"en": "Elephant", "cn": "大象", "emoji": "🐘", "sound": "trumpet"},
            {"en": "Lion", "cn": "狮子", "emoji": "🦁", "sound": "roar"},
            {"en": "Pig", "cn": "猪", "emoji": "🐷", "sound": "oink"},
        ]
        self.speech_id = 0
        self.praise_playing = False
    
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
            default_msg = f"{char_name} says: Great job! 🎉"
        else:
            text_color = "#FF9800"
            default_msg = f"{char_name} says: Try again! 💪"
        
        tk.Label(popup, text=message or default_msg, font=("微软雅黑", 12, "bold"),
                bg=bg_color, fg=text_color).pack(pady=5)
        
        popup.after(1800, popup.destroy)
    
    def draw_helper_character(self, canvas, x, y, scale=0.6):
        """在Canvas上绘制一个随机的助手角色"""
        if not THEME_AVAILABLE:
            return None
        char_id, char_name, _ = random.choice(self.paw_characters)
        draw_func = self.get_character_draw_func(char_id)
        if draw_func:
            draw_func(canvas, x, y, scale)
            return char_name
        return None

    def speak(self, text, rate="+0%", lang="cn"):
        if TTS_AVAILABLE:
            if self.praise_playing:
                self.window.after(4000, lambda: self._speak_normal(text, rate, lang))
            else:
                self._speak_normal(text, rate, lang)
    
    def _speak_normal(self, text, rate, lang="cn"):
        if TTS_AVAILABLE:
            self.speech_id += 1
            current_id = self.speech_id
            try:
                pygame.mixer.music.stop()
            except:
                pass
            voice = self.en_voice if lang == "en" else self.cn_voice
            t = threading.Thread(target=self._speak_thread, args=(text, rate, voice, current_id), daemon=True)
            t.start()
    
    def _speak_praise_direct(self, text, rate):
        t = threading.Thread(target=self._speak_thread_direct, args=(text, rate), daemon=True)
        t.start()
    
    def _speak_thread_direct(self, text, rate):
        audio_file = None
        try:
            audio_file = os.path.join(self.temp_dir, f"tts_{uuid.uuid4().hex}.mp3")
            async def generate():
                communicate = edge_tts.Communicate(text, self.cn_voice, rate=rate)
                await communicate.save(audio_file)
            asyncio.run(generate())
            pygame.mixer.music.stop()
            pygame.mixer.music.load(audio_file)
            pygame.mixer.music.play()
            while pygame.mixer.music.get_busy():
                pygame.time.Clock().tick(10)
            time.sleep(0.1)
            try:
                os.remove(audio_file)
            except:
                pass
        except Exception as e:
            print(f"语音错误: {e}")
    
    def _speak_thread(self, text, rate, voice, speech_id):
        audio_file = None
        try:
            if speech_id != self.speech_id:
                return
            audio_file = os.path.join(self.temp_dir, f"tts_{uuid.uuid4().hex}.mp3")
            async def generate():
                communicate = edge_tts.Communicate(text, voice, rate=rate)
                await communicate.save(audio_file)
            asyncio.run(generate())
            if speech_id != self.speech_id:
                try:
                    os.remove(audio_file)
                except:
                    pass
                return
            pygame.mixer.music.stop()
            pygame.mixer.music.load(audio_file)
            pygame.mixer.music.play()
            while pygame.mixer.music.get_busy():
                if speech_id != self.speech_id:
                    pygame.mixer.music.stop()
                    break
                pygame.time.Clock().tick(10)
            time.sleep(0.1)
            try:
                os.remove(audio_file)
            except:
                pass
        except Exception as e:
            print(f"语音错误: {e}")
    
    def speak_en_cn(self, en_text, cn_text):
        self.speech_id += 1
        current_id = self.speech_id
        try:
            pygame.mixer.music.stop()
        except:
            pass
        def speak_both():
            if current_id != self.speech_id:
                return
            self._speak_thread(en_text, "-10%", self.en_voice, current_id)
            if current_id != self.speech_id:
                return
            time.sleep(0.3)
            if current_id != self.speech_id:
                return
            self._speak_thread(cn_text, "+0%", self.cn_voice, current_id)
        t = threading.Thread(target=speak_both, daemon=True)
        t.start()
    
    def _scan_audio_folder(self, folder_name):
        folder_path = os.path.join(self.audio_dir, folder_name)
        if not os.path.exists(folder_path):
            return []
        return [os.path.join(folder_path, f) for f in os.listdir(folder_path) if f.lower().endswith(('.mp3', '.wav', '.ogg'))]
    
    def play_audio_file(self, file_path):
        def _play():
            try:
                pygame.mixer.music.stop()
                pygame.mixer.music.load(file_path)
                pygame.mixer.music.play()
            except Exception as e:
                print(f"播放音频错误: {e}")
        threading.Thread(target=_play, daemon=True).start()
    
    def speak_praise(self):
        self.praise_playing = True
        self.window.after(4000, self._clear_praise_flag)
        if self.praise_audios:
            self.play_audio_file(random.choice(self.praise_audios))
        else:
            self._speak_praise_direct(random.choice(self.praises), "+10%")
    
    def speak_encourage(self):
        self.praise_playing = True
        self.window.after(4000, self._clear_praise_flag)
        if self.encourage_audios:
            self.play_audio_file(random.choice(self.encourage_audios))
        else:
            self._speak_praise_direct(random.choice(self.encourages), "+0%")
    
    def _clear_praise_flag(self):
        self.praise_playing = False

    def create_main_menu(self):
        for widget in self.window.winfo_children():
            widget.destroy()
        self.window.configure(bg=self.bg_color)
        main_frame = tk.Frame(self.window, bg=self.bg_color)
        main_frame.pack(fill=tk.BOTH, expand=True, padx=20, pady=8)
        
        # 汪汪队主题标题
        if THEME_AVAILABLE:
            title_canvas = tk.Canvas(main_frame, width=800, height=70, bg=self.bg_color, highlightthickness=0)
            title_canvas.pack(pady=3)
            ThemeDrawings.draw_paw_badge(title_canvas, 60, 35, 30)
            ThemeDrawings.draw_star(title_canvas, 130, 30, 18, "#FFD700")
            title_canvas.create_text(400, 22, text="🔤 乐乐的英语乐园 🔤", font=("微软雅黑", 26, "bold"), fill=theme.primary)
            title_canvas.create_text(400, 50, text="🐾 Paw Patrol: Happy Learning English! 🐾", font=("Arial", 10), fill="#666")
            ThemeDrawings.draw_star(title_canvas, 670, 30, 18, "#FFD700")
            ThemeDrawings.draw_paw_badge(title_canvas, 740, 35, 30)
        else:
            tk.Label(main_frame, text="🔤 乐乐的英语乐园 🔤", font=("微软雅黑", 30, "bold"), bg=self.bg_color, fg="#45B7D1").pack(pady=5)
        
        # 等级选择和分数显示
        info_frame = tk.Frame(main_frame, bg=self.bg_color)
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
        
        score_frame = tk.Frame(info_frame, bg="#45B7D1", relief=tk.RAISED, bd=3)
        score_frame.pack(side=tk.LEFT, padx=10)
        tk.Label(score_frame, text=f"⭐ 总分: {self.score} ⭐", font=("微软雅黑", 14, "bold"), bg="#45B7D1", fg="white", padx=20, pady=5).pack()
        tk.Label(score_frame, text=f"当前字母: {len(self.letters)}个", font=("微软雅黑", 9), bg="#45B7D1", fg="white").pack(pady=(0,3))
        
        # ========== 简单游戏区（3岁+）==========
        easy_section = tk.LabelFrame(main_frame, text="🌟 简单模式（3岁+）", 
                                     font=("微软雅黑", 12, "bold"), bg="#E8F5E9", 
                                     fg="#2E7D32", relief=tk.GROOVE, bd=3)
        easy_section.pack(fill=tk.X, pady=8, padx=5)
        
        easy_frame = tk.Frame(easy_section, bg="#E8F5E9")
        easy_frame.pack(pady=8)
        
        easy_modes = [
            ("🔤\nABC字母", "#FF6B6B", "学字母", self.start_letter_cards),
            ("🌈\n颜色英语", "#45B7D1", "学颜色", self.start_color_english),
            ("🐾\n动物英语", "#96CEB4", "学动物", self.start_animal_english),
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
            ("🔢\n数字英语", "#4ECDC4", "1-5", self.start_number_english),
            ("👂\n听音选词", "#DDA0DD", "听声音", self.start_listen_english),
            ("🔨\n英语打地鼠", "#FFD93D", "快反应", self.start_english_whack),
        ]
        
        for i, (title, color, desc, command) in enumerate(advanced_modes):
            card = tk.Frame(advanced_frame, bg=color, relief=tk.RAISED, bd=4)
            card.grid(row=0, column=i, padx=20, pady=5)
            btn = tk.Button(card, text=title, font=("微软雅黑", 16, "bold"), bg=color, fg="white", 
                           width=10, height=3, relief=tk.FLAT, cursor="hand2", command=command)
            btn.pack(padx=5, pady=5)
            tk.Label(card, text=desc, font=("微软雅黑", 10), bg=color, fg="white").pack(pady=3)
        
        # 汪汪队底部装饰
        if THEME_AVAILABLE:
            bottom_canvas = tk.Canvas(main_frame, width=800, height=70, bg=self.bg_color, highlightthickness=0)
            bottom_canvas.pack(pady=5)
            bottom_canvas.create_rectangle(0, 45, 800, 70, fill="#81C784", outline="")
            ThemeDrawings.draw_puppy_chase(bottom_canvas, 150, 32, 0.4)
            ThemeDrawings.draw_puppy_skye(bottom_canvas, 320, 32, 0.4)
            ThemeDrawings.draw_puppy_marshall(bottom_canvas, 490, 32, 0.4)
            ThemeDrawings.draw_puppy_rubble(bottom_canvas, 660, 32, 0.4)
        
        tk.Button(main_frame, text="👋 退出", font=("微软雅黑", 11), bg="#FF6B6B", fg="white", relief=tk.RAISED, bd=3, cursor="hand2", command=self.on_close_window).pack(pady=8)
    
    def clear_game_area(self, bg_color="#E0F7FA"):
        # 清理所有待处理的定时器
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
        tk.Label(nav_frame, text=f"⭐ 总分: {self.score}", font=("微软雅黑", 12, "bold"), bg=bg_color, fg="#45B7D1").pack(side=tk.RIGHT, padx=10)
        self.game_frame = tk.Frame(self.window, bg=bg_color)
        self.game_frame.pack(fill=tk.BOTH, expand=True, padx=20, pady=10)
    
    def start_letter_cards(self):
        self.clear_game_area("#FFF8DC")
        self.letter_index = 0
        tk.Label(self.game_frame, text="🔤 ABC字母卡片", font=("微软雅黑", 26, "bold"), bg="#FFF8DC", fg="#FF6B6B").pack(pady=5)
        self.letter_progress = tk.Label(self.game_frame, text="", font=("微软雅黑", 11), bg="#FFF8DC", fg="#666")
        self.letter_progress.pack(pady=5)
        card = tk.Frame(self.game_frame, bg="white", relief=tk.RAISED, bd=4)
        card.pack(pady=10, padx=80, fill=tk.X)
        letter_row = tk.Frame(card, bg="white")
        letter_row.pack(pady=15)
        self.letter_big = tk.Label(letter_row, text="", font=("Arial", 100, "bold"), bg="white", fg="#FF6B6B")
        self.letter_big.pack(side=tk.LEFT, padx=20)
        self.letter_small = tk.Label(letter_row, text="", font=("Arial", 80, "bold"), bg="white", fg="#4ECDC4")
        self.letter_small.pack(side=tk.LEFT, padx=20)
        word_row = tk.Frame(card, bg="white")
        word_row.pack(pady=10)
        self.letter_emoji = tk.Label(word_row, text="", font=("Segoe UI Emoji", 60), bg="white")
        self.letter_emoji.pack(side=tk.LEFT, padx=15)
        self.letter_word = tk.Label(word_row, text="", font=("Arial", 36, "bold"), bg="white", fg="#45B7D1")
        self.letter_word.pack(side=tk.LEFT, padx=15)
        self.letter_chinese = tk.Label(card, text="", font=("微软雅黑", 20), bg="white", fg="#666")
        self.letter_chinese.pack(pady=10)
        btn_frame = tk.Frame(self.game_frame, bg="#FFF8DC")
        btn_frame.pack(pady=15)
        tk.Button(btn_frame, text="⬅️ 上一个", font=("微软雅黑", 11), bg="#45B7D1", fg="white", command=self.prev_letter, width=10).pack(side=tk.LEFT, padx=5)
        tk.Button(btn_frame, text="🔊 读一读", font=("微软雅黑", 11), bg="#FF6B6B", fg="white", command=self.speak_letter, width=10).pack(side=tk.LEFT, padx=5)
        tk.Button(btn_frame, text="下一个 ➡️", font=("微软雅黑", 11), bg="#45B7D1", fg="white", command=self.next_letter, width=10).pack(side=tk.LEFT, padx=5)
        self.show_letter()
    
    def show_letter(self):
        l = self.letters[self.letter_index]
        self.letter_big.config(text=l[0])
        self.letter_small.config(text=l[0].lower())
        self.letter_emoji.config(text=l[2])
        self.letter_word.config(text=l[1])
        self.letter_chinese.config(text=l[3])
        self.letter_progress.config(text=f"第 {self.letter_index + 1} / {len(self.letters)} 个字母")
        self.speak_en_cn(f"{l[0]}, {l[1]}", f"{l[0]}，{l[3]}")
    
    def speak_letter(self):
        l = self.letters[self.letter_index]
        self.speak_en_cn(f"{l[0]}, {l[0]}, {l[1]}", f"{l[3]}")
    
    def next_letter(self):
        self.letter_index = (self.letter_index + 1) % len(self.letters)
        self.show_letter()
    
    def prev_letter(self):
        self.letter_index = (self.letter_index - 1) % len(self.letters)
        self.show_letter()
    
    def start_number_english(self):
        """数字英语学习"""
        self.clear_game_area("#E8F5E9")
        self.num_index = 0
        
        tk.Label(self.game_frame, text="🔢 数字英语", font=("微软雅黑", 26, "bold"),
                 bg="#E8F5E9", fg="#4CAF50").pack(pady=5)
        
        self.num_progress = tk.Label(self.game_frame, text="", font=("微软雅黑", 11),
                                      bg="#E8F5E9", fg="#666")
        self.num_progress.pack(pady=5)
        
        card = tk.Frame(self.game_frame, bg="white", relief=tk.RAISED, bd=4)
        card.pack(pady=15, padx=80, fill=tk.X)
        
        # 数字显示
        num_row = tk.Frame(card, bg="white")
        num_row.pack(pady=20)
        
        self.num_digit = tk.Label(num_row, text="", font=("Arial", 100, "bold"),
                                   bg="white", fg="#4CAF50")
        self.num_digit.pack(side=tk.LEFT, padx=30)
        
        self.num_emoji = tk.Label(num_row, text="", font=("Segoe UI Emoji", 60),
                                   bg="white")
        self.num_emoji.pack(side=tk.LEFT, padx=30)
        
        self.num_english = tk.Label(card, text="", font=("Arial", 48, "bold"),
                                     bg="white", fg="#FF6B6B")
        self.num_english.pack(pady=10)
        
        self.num_chinese = tk.Label(card, text="", font=("微软雅黑", 24),
                                     bg="white", fg="#666")
        self.num_chinese.pack(pady=10)
        
        # 苹果展示
        self.num_apples = tk.Label(card, text="", font=("Segoe UI Emoji", 30),
                                    bg="white", wraplength=400)
        self.num_apples.pack(pady=10)
        
        btn_frame = tk.Frame(self.game_frame, bg="#E8F5E9")
        btn_frame.pack(pady=15)
        
        tk.Button(btn_frame, text="⬅️ 上一个", font=("微软雅黑", 11), bg="#45B7D1", fg="white",
                  command=self.prev_number, width=10).pack(side=tk.LEFT, padx=5)
        tk.Button(btn_frame, text="🔊 读一读", font=("微软雅黑", 11), bg="#FF6B6B", fg="white",
                  command=self.speak_number, width=10).pack(side=tk.LEFT, padx=5)
        tk.Button(btn_frame, text="下一个 ➡️", font=("微软雅黑", 11), bg="#45B7D1", fg="white",
                  command=self.next_number, width=10).pack(side=tk.LEFT, padx=5)
        
        self.show_number()
    
    def show_number(self):
        n = self.numbers[self.num_index]
        self.num_digit.config(text=str(n["num"]))
        self.num_emoji.config(text=n["emoji"])
        self.num_english.config(text=n["en"])
        self.num_chinese.config(text=n["cn"])
        self.num_apples.config(text="🍎" * n["num"])
        self.num_progress.config(text=f"第 {self.num_index + 1} / {len(self.numbers)} 个数字")
        self.speak_en_cn(f"{n['en']}, {n['num']}", f"{n['cn']}")
    
    def speak_number(self):
        n = self.numbers[self.num_index]
        self.speak_en_cn(f"{n['en']}, {n['en']}", f"{n['cn']}")
    
    def next_number(self):
        self.num_index = (self.num_index + 1) % len(self.numbers)
        self.show_number()
    
    def prev_number(self):
        self.num_index = (self.num_index - 1) % len(self.numbers)
        self.show_number()
    
    def start_color_english(self):
        """颜色英语学习"""
        self.clear_game_area("#FFF3E0")
        self.color_index = 0
        
        tk.Label(self.game_frame, text="🌈 颜色英语", font=("微软雅黑", 26, "bold"),
                 bg="#FFF3E0", fg="#FF9800").pack(pady=5)
        
        self.color_progress = tk.Label(self.game_frame, text="", font=("微软雅黑", 11),
                                        bg="#FFF3E0", fg="#666")
        self.color_progress.pack(pady=5)
        
        card = tk.Frame(self.game_frame, bg="white", relief=tk.RAISED, bd=4)
        card.pack(pady=15, padx=80, fill=tk.X)
        
        # 颜色展示 - 使用Canvas绘制真实颜色
        self.color_canvas = tk.Canvas(card, width=200, height=150, bg="white", highlightthickness=0)
        self.color_canvas.pack(pady=20)
        
        self.color_english = tk.Label(card, text="", font=("Arial", 48, "bold"),
                                       bg="white")
        self.color_english.pack(pady=10)
        
        self.color_chinese = tk.Label(card, text="", font=("微软雅黑", 24),
                                       bg="white", fg="#666")
        self.color_chinese.pack(pady=10)
        
        btn_frame = tk.Frame(self.game_frame, bg="#FFF3E0")
        btn_frame.pack(pady=15)
        
        tk.Button(btn_frame, text="⬅️ 上一个", font=("微软雅黑", 11), bg="#45B7D1", fg="white",
                  command=self.prev_color, width=10).pack(side=tk.LEFT, padx=5)
        tk.Button(btn_frame, text="🔊 读一读", font=("微软雅黑", 11), bg="#FF6B6B", fg="white",
                  command=self.speak_color, width=10).pack(side=tk.LEFT, padx=5)
        tk.Button(btn_frame, text="下一个 ➡️", font=("微软雅黑", 11), bg="#45B7D1", fg="white",
                  command=self.next_color, width=10).pack(side=tk.LEFT, padx=5)
        
        self.show_color()
    
    def show_color(self):
        c = self.colors_data[self.color_index]
        # 用Canvas绘制颜色圆形
        self.color_canvas.delete("all")
        self.color_canvas.create_oval(25, 10, 175, 140, fill=c["hex"], outline="#333", width=4)
        # 添加高光效果
        self.color_canvas.create_oval(45, 25, 85, 55, fill="white", outline="", stipple="gray50")
        
        self.color_english.config(text=c["en"], fg=c["hex"])
        self.color_chinese.config(text=c["cn"])
        self.color_progress.config(text=f"第 {self.color_index + 1} / {len(self.colors_data)} 个颜色")
        self.speak_en_cn(f"{c['en']}", f"{c['cn']}")
    
    def speak_color(self):
        c = self.colors_data[self.color_index]
        self.speak_en_cn(f"{c['en']}, {c['en']}", f"{c['cn']}")
    
    def next_color(self):
        self.color_index = (self.color_index + 1) % len(self.colors_data)
        self.show_color()
    
    def prev_color(self):
        self.color_index = (self.color_index - 1) % len(self.colors_data)
        self.show_color()
    
    def start_animal_english(self):
        """动物英语学习"""
        self.clear_game_area("#E3F2FD")
        self.animal_index = 0
        
        tk.Label(self.game_frame, text="🐾 动物英语", font=("微软雅黑", 26, "bold"),
                 bg="#E3F2FD", fg="#2196F3").pack(pady=5)
        
        self.animal_progress = tk.Label(self.game_frame, text="", font=("微软雅黑", 11),
                                         bg="#E3F2FD", fg="#666")
        self.animal_progress.pack(pady=5)
        
        card = tk.Frame(self.game_frame, bg="white", relief=tk.RAISED, bd=4)
        card.pack(pady=15, padx=80, fill=tk.X)
        
        # 动物展示
        self.animal_emoji = tk.Label(card, text="", font=("Segoe UI Emoji", 100),
                                      bg="white")
        self.animal_emoji.pack(pady=20)
        
        self.animal_english = tk.Label(card, text="", font=("Arial", 48, "bold"),
                                        bg="white", fg="#2196F3")
        self.animal_english.pack(pady=10)
        
        self.animal_chinese = tk.Label(card, text="", font=("微软雅黑", 24),
                                        bg="white", fg="#666")
        self.animal_chinese.pack(pady=10)
        
        btn_frame = tk.Frame(self.game_frame, bg="#E3F2FD")
        btn_frame.pack(pady=15)
        
        tk.Button(btn_frame, text="⬅️ 上一个", font=("微软雅黑", 11), bg="#45B7D1", fg="white",
                  command=self.prev_animal, width=10).pack(side=tk.LEFT, padx=5)
        tk.Button(btn_frame, text="🔊 读一读", font=("微软雅黑", 11), bg="#FF6B6B", fg="white",
                  command=self.speak_animal, width=10).pack(side=tk.LEFT, padx=5)
        tk.Button(btn_frame, text="下一个 ➡️", font=("微软雅黑", 11), bg="#45B7D1", fg="white",
                  command=self.next_animal, width=10).pack(side=tk.LEFT, padx=5)
        
        self.show_animal()
    
    def show_animal(self):
        a = self.animals[self.animal_index]
        self.animal_emoji.config(text=a["emoji"])
        self.animal_english.config(text=a["en"])
        self.animal_chinese.config(text=a["cn"])
        self.animal_progress.config(text=f"第 {self.animal_index + 1} / {len(self.animals)} 个动物")
        self.speak_en_cn(f"{a['en']}", f"{a['cn']}")
    
    def speak_animal(self):
        a = self.animals[self.animal_index]
        self.speak_en_cn(f"{a['en']}, {a['en']}", f"{a['cn']}")
    
    def next_animal(self):
        self.animal_index = (self.animal_index + 1) % len(self.animals)
        self.show_animal()
    
    def prev_animal(self):
        self.animal_index = (self.animal_index - 1) % len(self.animals)
        self.show_animal()
    
    def start_listen_english(self):
        """听音选词游戏"""
        self.clear_game_area("#FCE4EC")
        self.listen_score = 0
        
        # 标题带狗狗装饰
        if THEME_AVAILABLE:
            title_canvas = tk.Canvas(self.game_frame, width=600, height=70, bg="#FCE4EC", highlightthickness=0)
            title_canvas.pack(pady=5)
            title_canvas.create_text(300, 22, text="🐾 听音选词 🐾", font=("微软雅黑", 24, "bold"), fill="#E91E63")
            title_canvas.create_text(300, 52, text="Listen and choose the right picture!", font=("Arial", 11), fill="#666")
            ThemeDrawings.draw_paw_badge(title_canvas, 50, 35, 28)
            ThemeDrawings.draw_paw_badge(title_canvas, 550, 35, 28)
        else:
            tk.Label(self.game_frame, text="👂 听音选词", font=("微软雅黑", 26, "bold"),
                     bg="#FCE4EC", fg="#E91E63").pack(pady=5)
        
        self.listen_score_label = tk.Label(self.game_frame, text="⭐ 得分: 0",
                                            font=("微软雅黑", 14), bg="#FCE4EC", fg="#666")
        self.listen_score_label.pack(pady=5)
        
        tk.Button(self.game_frame, text="🔊 再听一遍", font=("微软雅黑", 12),
                  bg="#E91E63", fg="white", command=self.replay_listen).pack(pady=10)
        
        self.listen_hint = tk.Label(self.game_frame, text="听英语，选图片！",
                                     font=("微软雅黑", 14), bg="#FCE4EC", fg="#888")
        self.listen_hint.pack(pady=10)
        
        # 反馈区域（显示狗狗）
        self.listen_feedback_canvas = tk.Canvas(self.game_frame, width=200, height=100, 
                                                bg="#FCE4EC", highlightthickness=0)
        self.listen_feedback_canvas.pack(pady=5)
        
        # 选项按钮
        self.listen_frame = tk.Frame(self.game_frame, bg="#FCE4EC")
        self.listen_frame.pack(pady=20)
        
        self.listen_buttons = []
        colors = ["#FF6B6B", "#4ECDC4", "#45B7D1", "#96CEB4"]
        
        for i in range(4):
            btn = tk.Button(self.listen_frame, text="", font=("Segoe UI Emoji", 50),
                           width=4, height=2, bg=colors[i], fg="white",
                           relief=tk.RAISED, bd=4, cursor="hand2",
                           command=lambda idx=i: self.check_listen(idx))
            btn.grid(row=0, column=i, padx=15)
            self.listen_buttons.append(btn)
        
        self.new_listen_question()
    
    def new_listen_question(self):
        # 随机选择题目类型
        q_type = random.choice(["animal", "color", "letter"])
        
        if q_type == "animal":
            self.listen_target = random.choice(self.animals)
            others = random.sample([a for a in self.animals if a != self.listen_target], 3)
            self.listen_options = [self.listen_target] + others
            self.listen_word = self.listen_target["en"]
            display_key = "emoji"
        elif q_type == "color":
            self.listen_target = random.choice(self.colors_data)
            others = random.sample([c for c in self.colors_data if c != self.listen_target], 3)
            self.listen_options = [self.listen_target] + others
            self.listen_word = self.listen_target["en"]
            display_key = "emoji"
        else:
            self.listen_target = random.choice(self.letters)
            others = random.sample([l for l in self.letters if l != self.listen_target], 3)
            self.listen_options = [{"letter": l[0], "emoji": l[2]} for l in [self.listen_target] + others]
            self.listen_target = {"letter": self.listen_target[0], "emoji": self.listen_target[2]}
            self.listen_word = self.listen_target["letter"]
            display_key = "emoji"
        
        random.shuffle(self.listen_options)
        self.listen_correct_idx = self.listen_options.index(self.listen_target)
        
        colors = ["#FF6B6B", "#4ECDC4", "#45B7D1", "#96CEB4"]
        for i, btn in enumerate(self.listen_buttons):
            btn.config(text=self.listen_options[i][display_key], bg=colors[i], state=tk.NORMAL)
        
        self.listen_hint.config(text="", fg="#888")
        self.speak(self.listen_word, "-10%", "en")
    
    def replay_listen(self):
        self.speak(self.listen_word, "-10%", "en")
    
    def check_listen(self, idx):
        # 清空反馈区域
        if hasattr(self, 'listen_feedback_canvas'):
            self.listen_feedback_canvas.delete("all")
        
        if idx == self.listen_correct_idx:
            self.listen_score += 10
            self.score += 10
            self.listen_hint.config(text=f"🎉 Correct! 是 {self.listen_word}！", fg="#32CD32")
            self.listen_buttons[idx].config(bg="#32CD32")
            
            # 显示庆祝的狗狗
            if THEME_AVAILABLE and hasattr(self, 'listen_feedback_canvas'):
                char_id, char_name, _ = random.choice(self.paw_characters)
                draw_func = self.get_character_draw_func(char_id)
                if draw_func:
                    draw_func(self.listen_feedback_canvas, 100, 50, 0.6)
                    self.listen_feedback_canvas.create_text(100, 95, text=f"{char_name}: Great!", 
                                                           font=("微软雅黑", 10, "bold"), fill="#4CAF50")
            self.speak_praise()
        else:
            self.listen_hint.config(text=f"😅 是 {self.listen_word} 哦！", fg="#FF6B6B")
            self.listen_buttons[idx].config(bg="#808080")
            self.listen_buttons[self.listen_correct_idx].config(bg="#32CD32")
            
            # 显示鼓励的狗狗
            if THEME_AVAILABLE and hasattr(self, 'listen_feedback_canvas'):
                char_id, char_name, _ = random.choice(self.paw_characters)
                draw_func = self.get_character_draw_func(char_id)
                if draw_func:
                    draw_func(self.listen_feedback_canvas, 100, 50, 0.6)
                    self.listen_feedback_canvas.create_text(100, 95, text=f"{char_name}: Try again!", 
                                                           font=("微软雅黑", 10, "bold"), fill="#FF9800")
            self.speak_encourage()
        
        self.listen_score_label.config(text=f"⭐ 得分: {self.listen_score}")
        for btn in self.listen_buttons:
            btn.config(state=tk.DISABLED)
        self.window.after(5500, self.new_listen_question)
    
    def start_english_whack(self):
        """英语打地鼠游戏"""
        self.clear_game_area("#90EE90")
        self.en_whack_score = 0
        self.en_whack_running = True
        self.en_whack_holes = []
        self.en_whack_states = [None] * 9
        self.en_whack_answered = False
        self.en_whack_timer_id = None  # 用于取消定时器
        
        # 标题带狗狗装饰
        if THEME_AVAILABLE:
            title_canvas = tk.Canvas(self.game_frame, width=600, height=70, bg="#90EE90", highlightthickness=0)
            title_canvas.pack(pady=5)
            title_canvas.create_text(300, 22, text="🐾 英语打地鼠 🐾", font=("微软雅黑", 24, "bold"), fill="#228B22")
            title_canvas.create_text(300, 52, text="Find the word quickly!", font=("Arial", 11), fill="#006400")
            ThemeDrawings.draw_puppy_chase(title_canvas, 60, 40, 0.4)
            ThemeDrawings.draw_puppy_skye(title_canvas, 540, 40, 0.4)
        else:
            tk.Label(self.game_frame, text="🔨 英语打地鼠", font=("微软雅黑", 26, "bold"),
                     bg="#90EE90", fg="#228B22").pack(pady=5)
        
        info_frame = tk.Frame(self.game_frame, bg="#90EE90")
        info_frame.pack(pady=8)
        
        self.en_whack_score_label = tk.Label(info_frame, text="⭐ 得分: 0",
                                              font=("微软雅黑", 14, "bold"), bg="#90EE90", fg="#FF6B6B")
        self.en_whack_score_label.pack(side=tk.LEFT, padx=20)
        
        # 目标提示框
        target_frame = tk.Frame(self.game_frame, bg="#FFD700", relief=tk.RAISED, bd=4)
        target_frame.pack(pady=10)
        
        tk.Label(target_frame, text="🎯 Find:", font=("Arial", 18, "bold"),
                 bg="#FFD700", fg="#333").pack(side=tk.LEFT, padx=15, pady=15)
        
        # 目标单词标签
        self.en_whack_target_label = tk.Label(target_frame, text="", font=("Arial", 28, "bold"),
                                               bg="#FFD700", fg="#333", width=12)
        self.en_whack_target_label.pack(side=tk.LEFT, padx=15, pady=15)
        
        self.en_whack_hint = tk.Label(self.game_frame, text="点击正确的单词！",
                                       font=("微软雅黑", 14), bg="#90EE90", fg="#006400")
        self.en_whack_hint.pack(pady=8)
        
        # 反馈区域（显示狗狗）
        self.en_whack_feedback = tk.Canvas(self.game_frame, width=180, height=90, 
                                           bg="#90EE90", highlightthickness=0)
        self.en_whack_feedback.pack(pady=5)
        
        # 地鼠洞
        holes_frame = tk.Frame(self.game_frame, bg="#228B22", relief=tk.RIDGE, bd=6)
        holes_frame.pack(pady=10)
        
        for i in range(9):
            row = i // 3
            col = i % 3
            
            hole_outer = tk.Frame(holes_frame, bg="#8B4513", relief=tk.SUNKEN, bd=4)
            hole_outer.grid(row=row, column=col, padx=10, pady=10)
            
            btn = tk.Button(hole_outer, text="", font=("Arial", 16, "bold"),
                           width=12, height=3, bg="#3D2914", fg="#333",
                           relief=tk.SUNKEN, bd=3, cursor="hand2",
                           command=lambda idx=i: self.en_whack_click(idx))
            btn.pack(padx=4, pady=4)
            self.en_whack_holes.append(btn)
        
        self.speak("Find the correct word!", "-10%", "en")
        self.window.after(1500, self.en_whack_new_round)
    
    def en_whack_new_round(self):
        if not self.en_whack_running:
            return
        
        # 取消之前的定时器
        if self.en_whack_timer_id:
            self.window.after_cancel(self.en_whack_timer_id)
            self.en_whack_timer_id = None
        
        self.en_whack_answered = False
        
        # 重置所有洞
        for i in range(9):
            self.en_whack_holes[i].config(text="", bg="#3D2914", state=tk.NORMAL, fg="#333")
            self.en_whack_states[i] = None
        
        # 随机选择题目类型
        q_type = random.choice(["animal", "color"])
        
        if q_type == "animal":
            self.en_whack_target = random.choice(self.animals)
            others = [a for a in self.animals if a["en"] != self.en_whack_target["en"]]
            others = random.sample(others, min(3, len(others)))
        else:
            self.en_whack_target = random.choice(self.colors_data)
            others = [c for c in self.colors_data if c["en"] != self.en_whack_target["en"]]
            others = random.sample(others, min(3, len(others)))
        
        self.en_whack_word = self.en_whack_target["en"]
        
        # 显示目标
        self.en_whack_target_label.config(text=self.en_whack_word)
        if "hex" in self.en_whack_target:
            self.en_whack_target_label.config(fg=self.en_whack_target["hex"])
        else:
            self.en_whack_target_label.config(fg="#333")
        
        self.en_whack_hint.config(text=f"找到 {self.en_whack_word}！", fg="#006400")
        self.speak(self.en_whack_word, "-10%", "en")
        
        # 延迟显示选项
        self.window.after(1000, lambda: self.en_whack_show_moles(others))
    
    def en_whack_show_moles(self, others):
        if not self.en_whack_running or self.en_whack_answered:
            return
        
        # 随机选择3-4个位置
        num_moles = random.randint(3, 4)
        positions = random.sample(range(9), num_moles)
        
        # 确保正确答案在其中一个位置
        correct_pos = positions[0]
        
        # 准备选项列表：正确答案 + 其他选项
        all_options = [self.en_whack_target] + others[:num_moles-1]
        random.shuffle(all_options)
        
        # 分配选项到位置
        for i, pos in enumerate(positions):
            if i < len(all_options):
                opt = all_options[i]
                word = opt["en"]
                
                # 设置按钮显示
                if "hex" in opt:  # 颜色
                    fg = "white" if opt["en"] in ["Blue", "Black", "Purple"] else "black"
                    self.en_whack_holes[pos].config(text=word, bg=opt["hex"], fg=fg)
                else:  # 动物
                    emoji = opt.get("emoji", "")
                    self.en_whack_holes[pos].config(text=f"{emoji}\n{word}", bg="#FFE4B5", fg="black")
                
                self.en_whack_states[pos] = word
        
        # 设置超时隐藏
        self.en_whack_timer_id = self.window.after(5000, self.en_whack_hide)
    
    def en_whack_hide(self):
        if not self.en_whack_running or self.en_whack_answered:
            return
        
        self.en_whack_hint.config(text="太慢了！再试一次！", fg="#FF6B6B")
        
        for i in range(9):
            self.en_whack_holes[i].config(text="", bg="#3D2914", fg="#333")
            self.en_whack_states[i] = None
        
        self.window.after(1500, self.en_whack_new_round)
    
    def en_whack_click(self, idx):
        if not self.en_whack_running or self.en_whack_answered:
            return
        
        state = self.en_whack_states[idx]
        if state is None:
            return
        
        self.en_whack_answered = True
        
        # 取消超时定时器
        if self.en_whack_timer_id:
            self.window.after_cancel(self.en_whack_timer_id)
            self.en_whack_timer_id = None
        
        # 清空反馈区域
        if hasattr(self, 'en_whack_feedback'):
            self.en_whack_feedback.delete("all")
        
        if state == self.en_whack_word:
            # 正确
            self.en_whack_score += 10
            self.score += 10
            self.en_whack_score_label.config(text=f"⭐ 得分: {self.en_whack_score}")
            self.en_whack_holes[idx].config(text="✓ 正确!", bg="#32CD32", fg="white")
            self.en_whack_hint.config(text=f"太棒了！{self.en_whack_word}！+10分！", fg="#32CD32")
            
            # 显示庆祝的狗狗
            if THEME_AVAILABLE and hasattr(self, 'en_whack_feedback'):
                char_id, char_name, _ = random.choice(self.paw_characters)
                draw_func = self.get_character_draw_func(char_id)
                if draw_func:
                    draw_func(self.en_whack_feedback, 90, 45, 0.55)
                    self.en_whack_feedback.create_text(90, 85, text=f"{char_name}: Excellent!", 
                                                       font=("微软雅黑", 9, "bold"), fill="#4CAF50")
            self.speak_praise()
            
            # 隐藏其他选项
            for i in range(9):
                if i != idx:
                    self.en_whack_holes[i].config(text="", bg="#3D2914", fg="#333")
            
            self.window.after(2500, self.en_whack_new_round)
        else:
            # 错误
            self.en_whack_holes[idx].config(text="✗ 错误", bg="#FF6B6B", fg="white")
            self.en_whack_hint.config(text=f"不对哦！正确答案是 {self.en_whack_word}！", fg="#FF6B6B")
            
            # 显示鼓励的狗狗
            if THEME_AVAILABLE and hasattr(self, 'en_whack_feedback'):
                char_id, char_name, _ = random.choice(self.paw_characters)
                draw_func = self.get_character_draw_func(char_id)
                if draw_func:
                    draw_func(self.en_whack_feedback, 90, 45, 0.55)
                    self.en_whack_feedback.create_text(90, 85, text=f"{char_name}: Keep trying!", 
                                                       font=("微软雅黑", 9, "bold"), fill="#FF9800")
            self.speak_encourage()
            
            # 高亮正确答案
            for i in range(9):
                if self.en_whack_states[i] == self.en_whack_word:
                    self.en_whack_holes[i].config(bg="#32CD32")
            
            self.window.after(3000, self.en_whack_new_round)
    
    def run(self):
        self.window.mainloop()


if __name__ == "__main__":
    app = KidsEnglishApp()
    app.run()
