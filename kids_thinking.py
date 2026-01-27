# -*- coding: utf-8 -*-
"""
乐乐的思维乐园 v1.0
适合3岁幼儿的趣味思维训练
包含：找不同、记忆翻牌、图形规律、分类游戏、迷宫寻路、拼图游戏
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

import math

# edge-tts 语音
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

# 导入语音配置
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


class KidsThinkingApp:
    def __init__(self):
        self.window = tk.Tk()
        self.window.title("🧠 乐乐的思维乐园 🧠")
        
        # 设置窗口大小并居中
        window_width = 1100
        window_height = 850
        screen_width = self.window.winfo_screenwidth()
        screen_height = self.window.winfo_screenheight()
        x = (screen_width - window_width) // 2
        y = (screen_height - window_height) // 2 - 30
        self.window.geometry(f"{window_width}x{window_height}+{x}+{y}")
        
        # 使用主题背景色
        self.bg_color = theme.bg_color if THEME_AVAILABLE else "#F3E5F5"
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
        
        # 语音设置 - 从配置加载
        self.tts_lock = threading.Lock()
        if VOICE_CONFIG_AVAILABLE:
            self.voice = get_voice()
            self.praises = get_praises()
            self.encourages = get_encourages()
        else:
            self.voice = "zh-CN-YunxiNeural"
            self.praises = ["太棒了！", "真厉害！", "答对啦！"]
            self.encourages = ["加油！", "再试一次！", "没关系！"]
        self.temp_dir = tempfile.gettempdir()
        
        # 自定义音频文件夹
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
        
        # 总分
        self.score = 0
        self.game_frame = None
        
        # 初始化数据
        self.init_data()
        self.create_main_menu()
    
    def on_close_window(self):
        """窗口关闭处理"""
        result = messagebox.askyesno(
            "👋 确认退出",
            "确定要退出思维乐园吗？",
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
        self.speak(f"已切换到等级{level}！")
        self.create_main_menu()
    
    def init_data(self):
        """初始化思维数据"""
        # 找不同用的emoji组
        self.diff_groups = [
            (["🍎", "🍎", "🍎", "🍊"], "🍊"),
            (["🐱", "🐱", "🐶", "🐱"], "🐶"),
            (["⭐", "⭐", "⭐", "🌙"], "🌙"),
            (["🔴", "🔴", "🔵", "🔴"], "🔵"),
            (["🌸", "🌸", "🌸", "🌺"], "🌺"),
            (["🎈", "🎈", "🎁", "🎈"], "🎁"),
        ]
        
        # 记忆翻牌用的emoji
        self.memory_emojis = ["🍎", "🍌", "🍊", "🍇", "🐱", "🐶", "⭐", "🌙"]
        
        # 图形规律 - 使用彩色形状
        self.pattern_shapes = [
            (["circle_red", "circle_blue", "circle_red", "circle_blue"], "circle_red"),
            (["star_yellow", "star_yellow", "heart_pink", "star_yellow", "star_yellow"], "heart_pink"),
            (["square_green", "triangle_orange", "square_green", "triangle_orange"], "square_green"),
            (["circle_red", "circle_red", "circle_blue", "circle_red", "circle_red"], "circle_blue"),
        ]
        
        # 形状颜色映射
        self.shape_colors = {
            "circle_red": ("#FF6B6B", "圆形"),
            "circle_blue": ("#4ECDC4", "圆形"),
            "star_yellow": ("#FFD93D", "星形"),
            "heart_pink": ("#FF69B4", "心形"),
            "square_green": ("#45B7D1", "正方形"),
            "triangle_orange": ("#FF9800", "三角形"),
        }
        
        # 分类数据
        self.category_data = {
            "水果": ["🍎", "🍌", "🍊", "🍇", "🍓"],
            "动物": ["🐱", "🐶", "🐰", "🐻", "🐵"],
            "交通": ["🚗", "🚌", "🚲", "✈️", "🚢"],
        }
        
        # 语音版本号
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

    # =====================================================
    # 语音系统
    # =====================================================
    def speak(self, text, rate="+0%"):
        if TTS_AVAILABLE:
            if self.praise_playing:
                self.window.after(4000, lambda: self._speak_normal(text, rate))
            else:
                self._speak_normal(text, rate)
    
    def _speak_normal(self, text, rate):
        if TTS_AVAILABLE:
            self.speech_id += 1
            current_id = self.speech_id
            try:
                pygame.mixer.music.stop()
            except:
                pass
            t = threading.Thread(target=self._speak_thread, args=(text, rate, current_id), daemon=True)
            t.start()
    
    def _speak_praise_direct(self, text, rate):
        t = threading.Thread(target=self._speak_thread_direct, args=(text, rate), daemon=True)
        t.start()
    
    def _speak_thread_direct(self, text, rate):
        audio_file = None
        try:
            audio_file = os.path.join(self.temp_dir, f"tts_{uuid.uuid4().hex}.mp3")
            async def generate():
                communicate = edge_tts.Communicate(text, self.voice, rate=rate)
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
            if audio_file:
                try:
                    os.remove(audio_file)
                except:
                    pass
    
    def _speak_thread(self, text, rate, speech_id):
        audio_file = None
        try:
            if speech_id != self.speech_id:
                return
            audio_file = os.path.join(self.temp_dir, f"tts_{uuid.uuid4().hex}.mp3")
            async def generate():
                communicate = edge_tts.Communicate(text, self.voice, rate=rate)
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
            if audio_file:
                try:
                    os.remove(audio_file)
                except:
                    pass
    
    def _scan_audio_folder(self, folder_name):
        folder_path = os.path.join(self.audio_dir, folder_name)
        if not os.path.exists(folder_path):
            return []
        audio_files = []
        for f in os.listdir(folder_path):
            if f.lower().endswith(('.mp3', '.wav', '.ogg')):
                audio_files.append(os.path.join(folder_path, f))
        return audio_files
    
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

    # =====================================================
    # 形状绘制方法
    # =====================================================
    def draw_pattern_shape(self, canvas, shape_key, x, y, size):
        """绘制图案形状"""
        if shape_key not in self.shape_colors:
            return
        
        color, shape_type = self.shape_colors[shape_key]
        outline = self._darken_color(color)
        
        if shape_type == "圆形":
            canvas.create_oval(x-size, y-size, x+size, y+size, 
                              fill=color, outline=outline, width=2)
        elif shape_type == "星形":
            coords = []
            for i in range(10):
                angle = math.pi/2 + i * math.pi/5
                r = size if i % 2 == 0 else size * 0.4
                coords.append(x + r * math.cos(angle))
                coords.append(y - r * math.sin(angle))
            canvas.create_polygon(coords, fill=color, outline=outline, width=2)
        elif shape_type == "心形":
            coords = []
            for i in range(50):
                t = i * 2 * math.pi / 50
                hx = 16 * math.sin(t) ** 3
                hy = 13 * math.cos(t) - 5 * math.cos(2*t) - 2 * math.cos(3*t) - math.cos(4*t)
                coords.append(x + hx * size / 18)
                coords.append(y - hy * size / 18)
            canvas.create_polygon(coords, fill=color, outline=outline, width=2, smooth=True)
        elif shape_type == "正方形":
            canvas.create_rectangle(x-size, y-size, x+size, y+size,
                                   fill=color, outline=outline, width=2)
        elif shape_type == "三角形":
            h = size * 1.5
            points = [x, y-h*0.6, x-size, y+h*0.4, x+size, y+h*0.4]
            canvas.create_polygon(points, fill=color, outline=outline, width=2)
    
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
        
        self.window.configure(bg="#F3E5F5")
        
        main_frame = tk.Frame(self.window, bg="#F3E5F5")
        main_frame.pack(fill=tk.BOTH, expand=True, padx=20, pady=8)
        
        # 汪汪队主题标题
        if THEME_AVAILABLE:
            title_canvas = tk.Canvas(main_frame, width=800, height=70, bg="#F3E5F5", highlightthickness=0)
            title_canvas.pack(pady=3)
            ThemeDrawings.draw_paw_badge(title_canvas, 60, 35, 30)
            ThemeDrawings.draw_star(title_canvas, 130, 30, 18, "#FFD700")
            title_canvas.create_text(400, 22, text="🧠 乐乐的思维乐园 🧠", font=("微软雅黑", 26, "bold"), fill="#9C27B0")
            title_canvas.create_text(400, 50, text="🐾 汪汪队陪你动脑筋！ 🐾", font=("微软雅黑", 10), fill="#666")
            ThemeDrawings.draw_star(title_canvas, 670, 30, 18, "#FFD700")
            ThemeDrawings.draw_paw_badge(title_canvas, 740, 35, 30)
        else:
            tk.Label(main_frame, text="🧠 乐乐的思维乐园 🧠", 
                     font=("微软雅黑", 30, "bold"), bg="#F3E5F5", fg="#9C27B0").pack(pady=5)
        
        # 等级选择和分数显示
        info_frame = tk.Frame(main_frame, bg="#F3E5F5")
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
        
        score_frame = tk.Frame(info_frame, bg="#9C27B0", relief=tk.RAISED, bd=3)
        score_frame.pack(side=tk.LEFT, padx=10)
        tk.Label(score_frame, text=f"⭐ 总分: {self.score} ⭐", 
                 font=("微软雅黑", 14, "bold"), bg="#9C27B0", fg="white",
                 padx=20, pady=5).pack()
        level_desc = ["简单", "中等", "困难"]
        tk.Label(score_frame, text=f"当前难度: {level_desc[self.level-1]}", font=("微软雅黑", 9), bg="#9C27B0", fg="white").pack(pady=(0,3))
        
        # ========== 简单游戏区（3岁+）==========
        easy_section = tk.LabelFrame(main_frame, text="🌟 简单模式（3岁+）", 
                                     font=("微软雅黑", 12, "bold"), bg="#E8F5E9", 
                                     fg="#2E7D32", relief=tk.GROOVE, bd=3)
        easy_section.pack(fill=tk.X, pady=8, padx=5)
        
        easy_frame = tk.Frame(easy_section, bg="#E8F5E9")
        easy_frame.pack(pady=8)
        
        easy_modes = [
            ("🔍\n找不同", "#FF6B6B", "找出不同", self.start_find_diff),
            ("📦\n分类游戏", "#96CEB4", "学分类", self.start_category),
            ("🧩\n配对游戏", "#FFD93D", "找相同", self.start_matching),
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
            ("🎴\n记忆翻牌", "#4ECDC4", "记住位置", self.start_memory),
            ("📐\n图形规律", "#45B7D1", "找规律", self.start_pattern),
            ("🎯\n反应测试", "#DDA0DD", "快反应", self.start_reaction),
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
            bottom_canvas = tk.Canvas(main_frame, width=800, height=70, bg="#F3E5F5", highlightthickness=0)
            bottom_canvas.pack(pady=5)
            bottom_canvas.create_rectangle(0, 45, 800, 70, fill="#81C784", outline="")
            ThemeDrawings.draw_puppy_chase(bottom_canvas, 150, 32, 0.4)
            ThemeDrawings.draw_puppy_liberty(bottom_canvas, 320, 32, 0.4)
            ThemeDrawings.draw_puppy_tracker(bottom_canvas, 490, 32, 0.4)
            ThemeDrawings.draw_puppy_rex(bottom_canvas, 660, 32, 0.4)
        
        tk.Button(main_frame, text="👋 退出", font=("微软雅黑", 11),
                  bg="#FF6B6B", fg="white", relief=tk.RAISED, bd=3,
                  cursor="hand2", command=self.on_close_window).pack(pady=8)
    
    def clear_game_area(self, bg_color="#F3E5F5"):
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
        
        tk.Button(nav_frame, text="🏠 返回主菜单", font=("微软雅黑", 11),
                  bg="#96CEB4", fg="white", relief=tk.RAISED, bd=3,
                  cursor="hand2", command=self.create_main_menu).pack(side=tk.LEFT, padx=10)
        
        tk.Label(nav_frame, text=f"⭐ 总分: {self.score}",
                 font=("微软雅黑", 12, "bold"), bg=bg_color, fg="#9C27B0").pack(side=tk.RIGHT, padx=10)
        
        self.game_frame = tk.Frame(self.window, bg=bg_color)
        self.game_frame.pack(fill=tk.BOTH, expand=True, padx=20, pady=10)

    # =====================================================
    # 模式1: 找不同
    # =====================================================
    def start_find_diff(self):
        self.clear_game_area("#FFF8DC")
        self.diff_score = 0
        
        # 标题带狗狗装饰
        if THEME_AVAILABLE:
            title_canvas = tk.Canvas(self.game_frame, width=600, height=70, bg="#FFF8DC", highlightthickness=0)
            title_canvas.pack(pady=5)
            title_canvas.create_text(300, 22, text="🐾 找不同 🐾", font=("微软雅黑", 24, "bold"), fill="#FF6B6B")
            title_canvas.create_text(300, 52, text="找出不一样的那个！", font=("微软雅黑", 11), fill="#666")
            ThemeDrawings.draw_puppy_chase(title_canvas, 60, 40, 0.4)
            ThemeDrawings.draw_puppy_marshall(title_canvas, 540, 40, 0.4)
        else:
            tk.Label(self.game_frame, text="🔍 找不同", font=("微软雅黑", 26, "bold"),
                     bg="#FFF8DC", fg="#FF6B6B").pack(pady=5)
        
        self.diff_score_label = tk.Label(self.game_frame, text="⭐ 得分: 0",
                                          font=("微软雅黑", 14), bg="#FFF8DC", fg="#666")
        self.diff_score_label.pack(pady=5)
        
        tk.Label(self.game_frame, text="找出不一样的那个！", font=("微软雅黑", 16),
                 bg="#FFF8DC", fg="#888").pack(pady=10)
        
        self.diff_hint = tk.Label(self.game_frame, text="", font=("微软雅黑", 18), bg="#FFF8DC")
        self.diff_hint.pack(pady=5)
        
        # 反馈区域（显示狗狗）
        self.diff_feedback_canvas = tk.Canvas(self.game_frame, width=180, height=100, 
                                              bg="#FFF8DC", highlightthickness=0)
        self.diff_feedback_canvas.pack(pady=5)
        
        # 选项按钮
        self.diff_frame = tk.Frame(self.game_frame, bg="#FFF8DC")
        self.diff_frame.pack(pady=20)
        
        self.diff_buttons = []
        for i in range(4):
            btn = tk.Button(self.diff_frame, text="", font=("Segoe UI Emoji", 60),
                           width=3, height=1, bg="white",
                           relief=tk.RAISED, bd=4, cursor="hand2",
                           command=lambda idx=i: self.check_diff(idx))
            btn.grid(row=0, column=i, padx=15, pady=10)
            self.diff_buttons.append(btn)
        
        self.new_diff_question()
    
    def new_diff_question(self):
        group = random.choice(self.diff_groups)
        self.diff_items = group[0].copy()
        self.diff_answer = group[1]
        random.shuffle(self.diff_items)
        self.diff_correct_idx = self.diff_items.index(self.diff_answer)
        
        for i, btn in enumerate(self.diff_buttons):
            btn.config(text=self.diff_items[i], bg="white", state=tk.NORMAL)
        
        self.diff_hint.config(text="", fg="#666")
        self.speak("找出不一样的那个！", "-10%")
    
    def check_diff(self, idx):
        # 清空反馈区域
        if hasattr(self, 'diff_feedback_canvas'):
            self.diff_feedback_canvas.delete("all")
        
        if idx == self.diff_correct_idx:
            self.diff_score += 10
            self.score += 10
            self.diff_hint.config(text=f"🎉 对啦！{self.diff_answer}是不一样的！", fg="#32CD32")
            self.diff_buttons[idx].config(bg="#32CD32")
            
            # 显示庆祝的狗狗
            if THEME_AVAILABLE and hasattr(self, 'diff_feedback_canvas'):
                self.show_paw_feedback_on_canvas(self.diff_feedback_canvas, True)
            self.speak_praise()
        else:
            self.diff_hint.config(text=f"😅 {self.diff_answer}才是不一样的哦！", fg="#FF6B6B")
            self.diff_buttons[idx].config(bg="#808080")
            self.diff_buttons[self.diff_correct_idx].config(bg="#32CD32")
            
            # 显示鼓励的狗狗
            if THEME_AVAILABLE and hasattr(self, 'diff_feedback_canvas'):
                self.show_paw_feedback_on_canvas(self.diff_feedback_canvas, False)
            self.speak_encourage()
        
        self.diff_score_label.config(text=f"⭐ 得分: {self.diff_score}")
        for btn in self.diff_buttons:
            btn.config(state=tk.DISABLED)
        self.window.after(5500, self.new_diff_question)
    
    # =====================================================
    # 模式2: 记忆翻牌
    # =====================================================
    def start_memory(self):
        self.clear_game_area("#E0FFFF")
        self.memory_score = 0
        self.memory_flipped = []
        self.memory_matched = []
        
        # 标题带狗狗装饰
        if THEME_AVAILABLE:
            title_canvas = tk.Canvas(self.game_frame, width=600, height=70, bg="#E0FFFF", highlightthickness=0)
            title_canvas.pack(pady=5)
            title_canvas.create_text(300, 22, text="🐾 记忆翻牌 🐾", font=("微软雅黑", 24, "bold"), fill="#4ECDC4")
            title_canvas.create_text(300, 52, text="翻开两张相同的卡片！", font=("微软雅黑", 11), fill="#666")
            ThemeDrawings.draw_puppy_skye(title_canvas, 60, 40, 0.4)
            ThemeDrawings.draw_puppy_everest(title_canvas, 540, 40, 0.4)
        else:
            tk.Label(self.game_frame, text="🎴 记忆翻牌", font=("微软雅黑", 26, "bold"),
                     bg="#E0FFFF", fg="#4ECDC4").pack(pady=5)
        
        self.memory_score_label = tk.Label(self.game_frame, text="⭐ 得分: 0",
                                            font=("微软雅黑", 14), bg="#E0FFFF", fg="#666")
        self.memory_score_label.pack(pady=5)
        
        tk.Label(self.game_frame, text="翻开两张相同的卡片！", font=("微软雅黑", 16),
                 bg="#E0FFFF", fg="#888").pack(pady=10)
        
        self.memory_hint = tk.Label(self.game_frame, text="", font=("微软雅黑", 18), bg="#E0FFFF")
        self.memory_hint.pack(pady=5)
        
        # 反馈区域（显示狗狗）
        self.memory_feedback_canvas = tk.Canvas(self.game_frame, width=180, height=100, 
                                                bg="#E0FFFF", highlightthickness=0)
        self.memory_feedback_canvas.pack(pady=5)
        
        # 卡片网格
        self.memory_frame = tk.Frame(self.game_frame, bg="#E0FFFF")
        self.memory_frame.pack(pady=20)
        
        self.setup_memory_game()
    
    def setup_memory_game(self):
        # 清空
        for widget in self.memory_frame.winfo_children():
            widget.destroy()
        
        self.memory_flipped = []
        self.memory_matched = []
        
        # 选4对emoji
        selected = random.sample(self.memory_emojis, 4)
        self.memory_cards = selected * 2
        random.shuffle(self.memory_cards)
        
        self.memory_buttons = []
        for i in range(8):
            btn = tk.Button(self.memory_frame, text="❓", font=("Segoe UI Emoji", 40),
                           width=3, height=1, bg="#9C27B0", fg="white",
                           relief=tk.RAISED, bd=4, cursor="hand2",
                           command=lambda idx=i: self.flip_card(idx))
            btn.grid(row=i//4, column=i%4, padx=10, pady=10)
            self.memory_buttons.append(btn)
        
        self.speak("翻开两张相同的卡片！", "-10%")
    
    def flip_card(self, idx):
        if idx in self.memory_flipped or idx in self.memory_matched:
            return
        if len(self.memory_flipped) >= 2:
            return
        
        # 翻开卡片 - 显示emoji
        emoji = self.memory_cards[idx]
        self.memory_buttons[idx].config(text=emoji, bg="#FFFACD", fg="black")
        self.memory_flipped.append(idx)
        
        if len(self.memory_flipped) == 2:
            self.window.after(1000, self.check_memory_match)
    
    def check_memory_match(self):
        idx1, idx2 = self.memory_flipped
        
        # 清空反馈区域
        if hasattr(self, 'memory_feedback_canvas'):
            self.memory_feedback_canvas.delete("all")
        
        if self.memory_cards[idx1] == self.memory_cards[idx2]:
            # 匹配成功
            self.memory_matched.extend([idx1, idx2])
            self.memory_score += 10
            self.score += 10
            self.memory_score_label.config(text=f"⭐ 得分: {self.memory_score}")
            self.memory_buttons[idx1].config(bg="#32CD32")
            self.memory_buttons[idx2].config(bg="#32CD32")
            self.memory_hint.config(text="🎉 配对成功！", fg="#32CD32")
            
            # 显示庆祝的狗狗
            if THEME_AVAILABLE and hasattr(self, 'memory_feedback_canvas'):
                self.show_paw_feedback_on_canvas(self.memory_feedback_canvas, True)
            
            if len(self.memory_matched) == 8:
                self.speak_praise()
                self.memory_hint.config(text="🎉 太棒了！全部配对成功！")
                self.window.after(3000, self.setup_memory_game)
        else:
            # 匹配失败
            self.memory_buttons[idx1].config(text="❓", bg="#9C27B0")
            self.memory_buttons[idx2].config(text="❓", bg="#9C27B0")
            self.memory_hint.config(text="😅 不一样，再试试！", fg="#FF6B6B")
            
            # 显示鼓励的狗狗
            if THEME_AVAILABLE and hasattr(self, 'memory_feedback_canvas'):
                self.show_paw_feedback_on_canvas(self.memory_feedback_canvas, False)
        
        self.memory_flipped = []

    # =====================================================
    # 模式3: 图形规律
    # =====================================================
    def start_pattern(self):
        self.clear_game_area("#FFE4E1")
        self.pattern_score = 0
        
        tk.Label(self.game_frame, text="📐 图形规律", font=("微软雅黑", 26, "bold"),
                 bg="#FFE4E1", fg="#45B7D1").pack(pady=5)
        
        self.pattern_score_label = tk.Label(self.game_frame, text="⭐ 得分: 0",
                                             font=("微软雅黑", 14), bg="#FFE4E1", fg="#666")
        self.pattern_score_label.pack(pady=5)
        
        tk.Label(self.game_frame, text="找出规律，选择下一个！", font=("微软雅黑", 16),
                 bg="#FFE4E1", fg="#888").pack(pady=10)
        
        # 规律展示画布
        self.pattern_canvas = tk.Canvas(self.game_frame, width=700, height=120, 
                                         bg="white", relief=tk.RAISED, bd=4)
        self.pattern_canvas.pack(pady=15)
        
        self.pattern_hint = tk.Label(self.game_frame, text="", font=("微软雅黑", 18), bg="#FFE4E1")
        self.pattern_hint.pack(pady=5)
        
        # 选项画布
        self.pattern_options_frame = tk.Frame(self.game_frame, bg="#FFE4E1")
        self.pattern_options_frame.pack(pady=20)
        
        self.pattern_option_canvases = []
        for i in range(3):
            canvas = tk.Canvas(self.pattern_options_frame, width=100, height=100, 
                              bg="white", relief=tk.RAISED, bd=3, cursor="hand2")
            canvas.grid(row=0, column=i, padx=20)
            canvas.bind("<Button-1>", lambda e, idx=i: self.check_pattern(idx))
            self.pattern_option_canvases.append(canvas)
        
        self.new_pattern_question()
    
    def new_pattern_question(self):
        pattern_set = random.choice(self.pattern_shapes)
        self.pattern_sequence = pattern_set[0]
        self.pattern_answer = pattern_set[1]
        
        # 在画布上绘制规律序列
        self.pattern_canvas.delete("all")
        spacing = 100
        start_x = 80
        for i, shape_key in enumerate(self.pattern_sequence):
            self.draw_pattern_shape(self.pattern_canvas, shape_key, start_x + i * spacing, 60, 30)
        
        # 绘制问号
        self.pattern_canvas.create_text(start_x + len(self.pattern_sequence) * spacing, 60, 
                                        text="❓", font=("Segoe UI Emoji", 40))
        
        # 生成选项
        all_shapes = list(self.shape_colors.keys())
        others = [s for s in all_shapes if s != self.pattern_answer]
        self.pattern_options = [self.pattern_answer] + random.sample(others, 2)
        random.shuffle(self.pattern_options)
        self.pattern_correct_idx = self.pattern_options.index(self.pattern_answer)
        
        # 在选项画布上绘制
        for i, canvas in enumerate(self.pattern_option_canvases):
            canvas.delete("all")
            canvas.config(bg="white")
            self.draw_pattern_shape(canvas, self.pattern_options[i], 50, 50, 30)
        
        self.pattern_hint.config(text="", fg="#666")
        self.speak("找出规律，下一个是什么？", "-10%")
    
    def check_pattern(self, idx):
        # 禁用所有选项
        for canvas in self.pattern_option_canvases:
            canvas.unbind("<Button-1>")
        
        if idx == self.pattern_correct_idx:
            self.pattern_score += 10
            self.score += 10
            self.pattern_hint.config(text="🎉 对啦！你找到规律了！", fg="#32CD32")
            self.pattern_option_canvases[idx].config(bg="#90EE90")
            self.speak_praise()
        else:
            self.pattern_hint.config(text="😅 再仔细看看规律哦！", fg="#FF6B6B")
            self.pattern_option_canvases[idx].config(bg="#D3D3D3")
            self.pattern_option_canvases[self.pattern_correct_idx].config(bg="#90EE90")
            self.speak_encourage()
        
        self.pattern_score_label.config(text=f"⭐ 得分: {self.pattern_score}")
        
        def next_q():
            for i, canvas in enumerate(self.pattern_option_canvases):
                canvas.bind("<Button-1>", lambda e, idx=i: self.check_pattern(idx))
            self.new_pattern_question()
        
        self.window.after(4000, next_q)
    
    # =====================================================
    # 模式4: 分类游戏
    # =====================================================
    def start_category(self):
        self.clear_game_area("#E8F5E9")
        self.cat_score = 0
        
        tk.Label(self.game_frame, text="📦 分类游戏", font=("微软雅黑", 26, "bold"),
                 bg="#E8F5E9", fg="#96CEB4").pack(pady=5)
        
        self.cat_score_label = tk.Label(self.game_frame, text="⭐ 得分: 0",
                                         font=("微软雅黑", 14), bg="#E8F5E9", fg="#666")
        self.cat_score_label.pack(pady=5)
        
        self.cat_question = tk.Label(self.game_frame, text="", font=("微软雅黑", 18),
                                      bg="#E8F5E9", fg="#45B7D1")
        self.cat_question.pack(pady=10)
        
        # 物品展示
        self.cat_item = tk.Label(self.game_frame, text="", font=("Segoe UI Emoji", 80),
                                  bg="white", relief=tk.RAISED, bd=4, padx=30, pady=15)
        self.cat_item.pack(pady=15)
        
        self.cat_hint = tk.Label(self.game_frame, text="", font=("微软雅黑", 18), bg="#E8F5E9")
        self.cat_hint.pack(pady=5)
        
        # 分类选项
        self.cat_frame = tk.Frame(self.game_frame, bg="#E8F5E9")
        self.cat_frame.pack(pady=20)
        
        self.cat_buttons = []
        colors = ["#FF6B6B", "#4ECDC4", "#45B7D1"]
        categories = list(self.category_data.keys())
        for i, cat in enumerate(categories):
            btn = tk.Button(self.cat_frame, text=cat, font=("微软雅黑", 18, "bold"),
                           width=8, height=2, bg=colors[i], fg="white",
                           relief=tk.RAISED, bd=4, cursor="hand2",
                           command=lambda c=cat: self.check_category(c))
            btn.grid(row=0, column=i, padx=15)
            self.cat_buttons.append(btn)
        
        self.new_category_question()
    
    def new_category_question(self):
        # 随机选一个类别和物品
        self.cat_correct = random.choice(list(self.category_data.keys()))
        self.cat_current_item = random.choice(self.category_data[self.cat_correct])
        
        self.cat_item.config(text=self.cat_current_item)
        self.cat_question.config(text=f"这个{self.cat_current_item}属于哪一类？")
        
        colors = ["#FF6B6B", "#4ECDC4", "#45B7D1"]
        for i, btn in enumerate(self.cat_buttons):
            btn.config(bg=colors[i], state=tk.NORMAL)
        
        self.cat_hint.config(text="", fg="#666")
        self.speak(f"这个属于哪一类？", "-10%")
    
    def check_category(self, selected):
        if selected == self.cat_correct:
            self.cat_score += 10
            self.score += 10
            self.cat_hint.config(text=f"🎉 对啦！{self.cat_current_item}是{self.cat_correct}！", fg="#32CD32")
            self.speak_praise()
        else:
            self.cat_hint.config(text=f"😅 {self.cat_current_item}是{self.cat_correct}哦！", fg="#FF6B6B")
            self.speak_encourage()
        
        self.cat_score_label.config(text=f"⭐ 得分: {self.cat_score}")
        for btn in self.cat_buttons:
            btn.config(state=tk.DISABLED)
        self.window.after(5500, self.new_category_question)

    # =====================================================
    # 模式5: 反应测试
    # =====================================================
    def start_reaction(self):
        self.clear_game_area("#FFF0F5")
        self.react_score = 0
        self.react_running = False
        
        tk.Label(self.game_frame, text="🎯 反应测试", font=("微软雅黑", 26, "bold"),
                 bg="#FFF0F5", fg="#DDA0DD").pack(pady=5)
        
        self.react_score_label = tk.Label(self.game_frame, text="⭐ 得分: 0",
                                           font=("微软雅黑", 14), bg="#FFF0F5", fg="#666")
        self.react_score_label.pack(pady=5)
        
        tk.Label(self.game_frame, text="看到⭐就快速点击！", font=("微软雅黑", 16),
                 bg="#FFF0F5", fg="#888").pack(pady=10)
        
        self.react_hint = tk.Label(self.game_frame, text="", font=("微软雅黑", 18), bg="#FFF0F5")
        self.react_hint.pack(pady=5)
        
        # 反应按钮
        self.react_btn = tk.Button(self.game_frame, text="🔴", font=("Segoe UI Emoji", 100),
                                    width=4, height=2, bg="white",
                                    relief=tk.RAISED, bd=4, cursor="hand2",
                                    command=self.react_click)
        self.react_btn.pack(pady=30)
        
        # 开始按钮
        self.react_start_btn = tk.Button(self.game_frame, text="🎮 开始游戏", 
                                          font=("微软雅黑", 14, "bold"),
                                          bg="#4CAF50", fg="white", relief=tk.RAISED, bd=3,
                                          cursor="hand2", command=self.start_reaction_game)
        self.react_start_btn.pack(pady=15)
        
        self.speak("看到星星就快速点击！", "-10%")
    
    def start_reaction_game(self):
        self.react_score = 0
        self.react_count = 0
        self.react_running = True
        self.react_is_star = False
        self.react_start_btn.config(state=tk.DISABLED)
        self.react_score_label.config(text="⭐ 得分: 0")
        self.react_hint.config(text="准备...", fg="#666")
        self.window.after(1000, self.show_react_symbol)
    
    def show_react_symbol(self):
        if not self.react_running:
            return
        
        self.react_count += 1
        if self.react_count > 10:
            self.end_reaction_game()
            return
        
        # 随机显示星星或其他
        if random.random() > 0.4:  # 60%概率显示星星
            self.react_btn.config(text="⭐", bg="#FFD700")
            self.react_is_star = True
            self.react_hint.config(text="快点击！", fg="#32CD32")
        else:
            symbols = ["🔴", "🔵", "🟢", "🟡"]
            self.react_btn.config(text=random.choice(symbols), bg="white")
            self.react_is_star = False
            self.react_hint.config(text="等待星星...", fg="#666")
        
        # 2秒后换下一个
        self.window.after(2000, self.show_react_symbol)
    
    def react_click(self):
        if not self.react_running:
            return
        
        if self.react_is_star:
            self.react_score += 10
            self.score += 10
            self.react_score_label.config(text=f"⭐ 得分: {self.react_score}")
            self.react_btn.config(bg="#32CD32")
        else:
            self.react_hint.config(text="😅 不是星星哦！", fg="#FF6B6B")
    
    def end_reaction_game(self):
        self.react_running = False
        self.react_start_btn.config(state=tk.NORMAL)
        self.react_btn.config(text="🎉", bg="white")
        self.react_hint.config(text=f"游戏结束！得分: {self.react_score}", fg="#9C27B0")
        
        if self.react_score >= 50:
            self.speak_praise()
        else:
            self.speak_encourage()
    
    # =====================================================
    # 模式6: 配对游戏
    # =====================================================
    def start_matching(self):
        self.clear_game_area("#E0F7FA")
        self.match_score = 0
        
        tk.Label(self.game_frame, text="🧩 配对游戏", font=("微软雅黑", 26, "bold"),
                 bg="#E0F7FA", fg="#FFD93D").pack(pady=5)
        
        self.match_score_label = tk.Label(self.game_frame, text="⭐ 得分: 0",
                                           font=("微软雅黑", 14), bg="#E0F7FA", fg="#666")
        self.match_score_label.pack(pady=5)
        
        tk.Label(self.game_frame, text="找出和左边一样的！", font=("微软雅黑", 16),
                 bg="#E0F7FA", fg="#888").pack(pady=10)
        
        # 目标展示
        self.match_target = tk.Label(self.game_frame, text="", font=("Segoe UI Emoji", 80),
                                      bg="white", relief=tk.RAISED, bd=4, padx=30, pady=15)
        self.match_target.pack(pady=15)
        
        self.match_hint = tk.Label(self.game_frame, text="", font=("微软雅黑", 18), bg="#E0F7FA")
        self.match_hint.pack(pady=5)
        
        # 选项
        self.match_frame = tk.Frame(self.game_frame, bg="#E0F7FA")
        self.match_frame.pack(pady=20)
        
        self.match_buttons = []
        colors = ["#FF6B6B", "#4ECDC4", "#45B7D1", "#96CEB4"]
        for i in range(4):
            btn = tk.Button(self.match_frame, text="", font=("Segoe UI Emoji", 50),
                           width=3, height=1, bg=colors[i], fg="white",
                           relief=tk.RAISED, bd=4, cursor="hand2",
                           command=lambda idx=i: self.check_matching(idx))
            btn.grid(row=0, column=i, padx=15)
            self.match_buttons.append(btn)
        
        self.new_matching_question()
    
    def new_matching_question(self):
        all_emojis = ["🍎", "🍌", "🍊", "🍇", "🐱", "🐶", "⭐", "🌙", "🎈", "🎁"]
        self.match_answer = random.choice(all_emojis)
        others = random.sample([e for e in all_emojis if e != self.match_answer], 3)
        
        self.match_options = [self.match_answer] + others
        random.shuffle(self.match_options)
        self.match_correct_idx = self.match_options.index(self.match_answer)
        
        self.match_target.config(text=self.match_answer)
        
        colors = ["#FF6B6B", "#4ECDC4", "#45B7D1", "#96CEB4"]
        for i, btn in enumerate(self.match_buttons):
            btn.config(text=self.match_options[i], bg=colors[i], state=tk.NORMAL)
        
        self.match_hint.config(text="", fg="#666")
        self.speak("找出一样的！", "-10%")
    
    def check_matching(self, idx):
        if idx == self.match_correct_idx:
            self.match_score += 10
            self.score += 10
            self.match_hint.config(text=f"🎉 对啦！找到了{self.match_answer}！", fg="#32CD32")
            self.match_buttons[idx].config(bg="#32CD32")
            self.speak_praise()
        else:
            self.match_hint.config(text=f"😅 不对哦，是{self.match_answer}！", fg="#FF6B6B")
            self.match_buttons[idx].config(bg="#808080")
            self.match_buttons[self.match_correct_idx].config(bg="#32CD32")
            self.speak_encourage()
        
        self.match_score_label.config(text=f"⭐ 得分: {self.match_score}")
        for btn in self.match_buttons:
            btn.config(state=tk.DISABLED)
        self.window.after(5500, self.new_matching_question)
    
    def run(self):
        self.window.mainloop()


if __name__ == "__main__":
    app = KidsThinkingApp()
    app.run()
