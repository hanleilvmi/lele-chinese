"""
乐乐的学习乐园 v2.8 - 主程序
全方位幼儿早教软件，适合3岁儿童
集成6大模块：识字、拼音、数学、英语、思维、交通
新增：学习进度追踪、难度分级、奖励系统、错题复习、每日学习计划
改进：退出确认、临时文件清理、休息提醒、数据保存优化、打包支持
"""

import tkinter as tk
from tkinter import messagebox, ttk
import subprocess
import sys
import os
import threading
import asyncio
import tempfile
import uuid
import time
import json
import random
import datetime
import atexit

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

# 导入学习数据管理
try:
    from learning_data import get_learning_data, BADGES
    LEARNING_DATA_AVAILABLE = True
except ImportError:
    LEARNING_DATA_AVAILABLE = False

# 导入基础模块
try:
    from learning_base import temp_file_manager, RestReminder
    BASE_MODULE_AVAILABLE = True
except ImportError:
    BASE_MODULE_AVAILABLE = False

# 导入主题系统
try:
    from theme_config import get_current_theme, ThemeHelper, get_random_character
    from theme_selector import show_theme_selector
    from theme_drawings import ThemeDrawings
    THEME_AVAILABLE = True
    theme_helper = ThemeHelper()
except ImportError:
    THEME_AVAILABLE = False
    theme_helper = None

# 导入子模块（用于打包后直接调用）
try:
    from kids_game_v3 import KidsLiteracyGame
    LITERACY_AVAILABLE = True
except ImportError:
    LITERACY_AVAILABLE = False

try:
    from kids_pinyin import KidsPinyinApp as KidsPinyinGame
    PINYIN_AVAILABLE = True
except ImportError:
    PINYIN_AVAILABLE = False

try:
    from kids_math import KidsMathApp as KidsMathGame
    MATH_AVAILABLE = True
except ImportError:
    MATH_AVAILABLE = False

try:
    from kids_english import KidsEnglishApp as KidsEnglishGame
    ENGLISH_AVAILABLE = True
except ImportError:
    ENGLISH_AVAILABLE = False

try:
    from kids_thinking import KidsThinkingApp as KidsThinkingGame
    THINKING_AVAILABLE = True
except ImportError:
    THINKING_AVAILABLE = False

try:
    from kids_vehicles import KidsVehiclesApp as KidsVehiclesGame
    VEHICLES_AVAILABLE = True
except ImportError:
    VEHICLES_AVAILABLE = False

# 语音风格配置
VOICE_STYLES = {
    "汪汪队风格": {
        "voice": "zh-CN-YunxiNeural",
        "desc": "活泼男童声，汪汪队台词",
        "praises": [
            "汪汪队，出动！答对啦！",
            "没有困难的工作，只有勇敢的狗狗！",
            "太棒了，乐乐是最勇敢的狗狗！",
            "耶！任务完成！",
            "狗狗们，做得好！",
            "乐乐真厉害，给你一个大大的赞！",
            "汪汪汪，你真棒！",
            "莱德队长为你骄傲！",
        ],
        "encourages": [
            "没关系，汪汪队永不放弃！",
            "加油，勇敢的狗狗不怕困难！",
            "再试一次，你一定行！",
            "别担心，汪汪队来帮你！",
            "狗狗们，我们再来一次！",
        ]
    },
    "温柔姐姐": {
        "voice": "zh-CN-XiaoyiNeural",
        "desc": "温柔女声，亲切鼓励",
        "praises": [
            "哇，乐乐真棒！",
            "太厉害了，答对啦！",
            "乐乐好聪明呀！",
            "真棒真棒，给你点赞！",
            "乐乐是最棒的小朋友！",
            "太聪明了，继续加油！",
            "答对了，乐乐真厉害！",
            "好棒呀，姐姐为你骄傲！",
        ],
        "encourages": [
            "没关系，再试一次！",
            "加油，乐乐一定行！",
            "别着急，慢慢来！",
            "没事的，我们再来！",
            "乐乐加油，你可以的！",
        ]
    },
    "活泼哥哥": {
        "voice": "zh-CN-YunjianNeural",
        "desc": "阳光男声，热情活泼",
        "praises": [
            "耶！乐乐太厉害了！",
            "哇塞，答对啦！",
            "乐乐真是小天才！",
            "太棒了，给你比个心！",
            "厉害厉害，乐乐最棒！",
            "答对了，哥哥为你鼓掌！",
            "乐乐好聪明，继续加油！",
            "太强了，乐乐真厉害！",
        ],
        "encourages": [
            "没关系，再来一次！",
            "加油加油，你能行！",
            "别灰心，继续努力！",
            "没事，哥哥相信你！",
            "再试试，乐乐最棒！",
        ]
    },
    "可爱童声": {
        "voice": "zh-CN-XiaoxiaoNeural",
        "desc": "可爱女童声，活泼有趣",
        "praises": [
            "哇，乐乐好棒棒！",
            "太厉害啦，答对了！",
            "乐乐真聪明呀！",
            "棒棒哒，给你小红花！",
            "乐乐是最棒的！",
            "好厉害呀，继续加油！",
            "答对啦，乐乐真棒！",
            "太聪明了，为你鼓掌！",
        ],
        "encourages": [
            "没关系呀，再试一次！",
            "加油加油，你可以的！",
            "别着急，慢慢想！",
            "没事没事，我们再来！",
            "乐乐加油，一定行！",
        ]
    },
}

# 配置文件路径
CONFIG_FILE = os.path.join(os.path.dirname(os.path.abspath(__file__)), "voice_config.json")
PROGRESS_FILE = os.path.join(os.path.dirname(os.path.abspath(__file__)), "learning_progress.json")

def load_voice_config():
    """加载语音配置"""
    try:
        if os.path.exists(CONFIG_FILE):
            with open(CONFIG_FILE, 'r', encoding='utf-8') as f:
                return json.load(f)
    except:
        pass
    return {"style": "汪汪队风格"}

def save_voice_config(config):
    """保存语音配置"""
    try:
        with open(CONFIG_FILE, 'w', encoding='utf-8') as f:
            json.dump(config, f, ensure_ascii=False, indent=2)
    except Exception as e:
        print(f"保存配置失败: {e}")


class KidsLearningMain:
    def __init__(self):
        self.window = tk.Tk()
        self.window.title("🌟 乐乐的学习乐园 🌟")
        
        # 设置窗口大小并居中
        window_width = 1050
        window_height = 850
        screen_width = self.window.winfo_screenwidth()
        screen_height = self.window.winfo_screenheight()
        x = (screen_width - window_width) // 2
        y = (screen_height - window_height) // 2 - 30
        self.window.geometry(f"{window_width}x{window_height}+{x}+{y}")
        self.window.configure(bg="#E8F5E9")
        
        # 加载语音配置
        self.voice_config = load_voice_config()
        self.current_style = self.voice_config.get("style", "汪汪队风格")
        
        # 加载学习数据
        if LEARNING_DATA_AVAILABLE:
            self.learning_data = get_learning_data()
            self.learning_data.check_daily_login()
        else:
            self.learning_data = None
        
        # 语音设置
        self.tts_lock = threading.Lock()
        self.voice = VOICE_STYLES[self.current_style]["voice"]
        self.temp_dir = tempfile.gettempdir()
        self.speech_id = 0
        
        self.create_main_menu()
    
    def speak(self, text, rate="+0%"):
        if TTS_AVAILABLE:
            self.speech_id += 1
            current_id = self.speech_id
            try:
                pygame.mixer.music.stop()
            except:
                pass
            t = threading.Thread(target=self._speak_thread, args=(text, rate, current_id), daemon=True)
            t.start()
    
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

    def create_main_menu(self):
        for widget in self.window.winfo_children():
            widget.destroy()
        
        # 使用主题背景色
        bg_color = theme_helper.bg_color if THEME_AVAILABLE else "#E8F5E9"
        self.window.configure(bg=bg_color)
        
        main_frame = tk.Frame(self.window, bg=bg_color)
        main_frame.pack(fill=tk.BOTH, expand=True, padx=20, pady=10)
        
        # 顶部区域 - 汪汪队主题装饰
        top_frame = tk.Frame(main_frame, bg=bg_color)
        top_frame.pack(fill=tk.X, pady=5)
        
        # 汪汪队主题标题Canvas
        if THEME_AVAILABLE:
            title_canvas = tk.Canvas(top_frame, width=700, height=90, bg=bg_color, highlightthickness=0)
            title_canvas.pack(side=tk.LEFT, expand=True)
            # 绘制装饰
            ThemeDrawings.draw_paw_badge(title_canvas, 50, 45, 40)
            ThemeDrawings.draw_star(title_canvas, 120, 40, 25, "#FFD700")
            # 标题
            title_canvas.create_text(380, 30, text="🌟 乐乐的学习乐园 🌟", 
                                    font=("微软雅黑", 32, "bold"), fill=theme_helper.primary)
            title_canvas.create_text(380, 65, text="🐕 汪汪队，准备出动！快乐学习，聪明成长 🐾",
                                    font=("微软雅黑", 11), fill="#666")
            # 右侧装饰
            ThemeDrawings.draw_star(title_canvas, 620, 40, 25, "#FFD700")
            ThemeDrawings.draw_bone(title_canvas, 680, 45, 35)
        else:
            # 标题
            title_frame = tk.Frame(top_frame, bg=bg_color)
            title_frame.pack(side=tk.LEFT, expand=True)
            tk.Label(title_frame, text="🌈 ⭐ 🎈 ⭐ 🌈", font=("Segoe UI Emoji", 18), bg=bg_color).pack()
            tk.Label(title_frame, text="🌟 乐乐的学习乐园 🌟", font=("微软雅黑", 36, "bold"), bg=bg_color, fg="#4CAF50").pack()
            tk.Label(title_frame, text="✨ 快乐学习，聪明成长 ✨", font=("微软雅黑", 12), bg=bg_color, fg="#888").pack()
        
        # 进度卡片 - 使用新的学习数据
        if self.learning_data:
            stats = self.learning_data.get_stats()
            daily_plan = self.learning_data.get_daily_plan()
            
            # 右侧卡片容器
            right_cards = tk.Frame(top_frame, bg=bg_color)
            right_cards.pack(side=tk.RIGHT, padx=10)
            
            # 每日计划卡片
            card_bg = theme_helper.card_bg if THEME_AVAILABLE else "#81D4FA"
            plan_card = tk.Frame(right_cards, bg=card_bg, relief=tk.RAISED, bd=3)
            plan_card.pack(pady=3)
            tk.Label(plan_card, text="📅 今日计划", font=("微软雅黑", 11, "bold"), bg=card_bg, fg="#01579B").pack(pady=3, padx=12)
            
            # 进度条
            progress_frame = tk.Frame(plan_card, bg=card_bg)
            progress_frame.pack(padx=12, pady=2)
            progress_pct = daily_plan["question_progress"]
            tk.Label(progress_frame, text=f"答题: {daily_plan['today_questions']}/{daily_plan['target_questions']}", 
                    font=("微软雅黑", 9), bg=card_bg, fg="#01579B").pack(side=tk.LEFT)
            
            # 简单进度条
            bar_frame = tk.Frame(progress_frame, bg="#B3E5FC", width=80, height=10, relief=tk.SUNKEN, bd=1)
            bar_frame.pack(side=tk.LEFT, padx=5)
            bar_frame.pack_propagate(False)
            fill_width = int(80 * progress_pct / 100)
            if fill_width > 0:
                fill_bar = tk.Frame(bar_frame, bg="#4CAF50" if progress_pct >= 100 else "#2196F3", width=fill_width, height=10)
                fill_bar.pack(side=tk.LEFT)
            
            # 学习时长
            self.time_label = tk.Label(plan_card, text=f"⏱️ 已学习: {daily_plan['session_minutes']}分钟", 
                    font=("微软雅黑", 9), bg=card_bg, fg="#01579B")
            self.time_label.pack(pady=(0,3))
            
            # 目标完成提示
            if daily_plan["goal_completed"]:
                tk.Label(plan_card, text="🎉 今日目标已完成！", font=("微软雅黑", 9, "bold"), 
                        bg=card_bg, fg="#4CAF50").pack(pady=(0,3))
            
            # 总进度卡片
            progress_card = tk.Frame(right_cards, bg="#FFD54F", relief=tk.RAISED, bd=3)
            progress_card.pack(pady=3)
            tk.Label(progress_card, text="📊 学习进度", font=("微软雅黑", 11, "bold"), bg="#FFD54F", fg="#5D4037").pack(pady=3, padx=12)
            tk.Label(progress_card, text=f"⭐ 星星: {stats['stars']} | 🏅 徽章: {stats['badges']}", font=("微软雅黑", 9), bg="#FFD54F", fg="#5D4037").pack(padx=12)
            tk.Label(progress_card, text=f"📚 学习天数: {stats['days']} 天", font=("微软雅黑", 9), bg="#FFD54F", fg="#5D4037").pack(padx=12)
            accuracy_text = f"正确率: {stats['accuracy']}%" if stats['total'] > 0 else "开始学习吧！"
            tk.Label(progress_card, text=accuracy_text, font=("微软雅黑", 9), bg="#FFD54F", fg="#5D4037").pack(padx=12, pady=(0,3))
        
        # 欢迎语 - 汪汪队风格
        hour = datetime.datetime.now().hour
        time_greeting = "早上好！" if hour < 12 else ("下午好！" if hour < 18 else "晚上好！")
        paw_greetings = ["汪汪队，出动！", "没有困难的工作，只有勇敢的狗狗！", "乐乐最棒了！", "每天进步一点点！"]
        
        welcome_frame = tk.Frame(main_frame, bg=theme_helper.accent if THEME_AVAILABLE else "#81C784", relief=tk.RAISED, bd=3)
        welcome_frame.pack(pady=10)
        tk.Label(welcome_frame, text=f"🐕 {time_greeting}欢迎乐乐来学习！{random.choice(paw_greetings)} 🐾", 
                 font=("微软雅黑", 13), bg=theme_helper.accent if THEME_AVAILABLE else "#81C784", fg="white", padx=15, pady=8).pack()
        
        # 模块选择 - 2行3列
        modules_frame = tk.Frame(main_frame, bg=bg_color)
        modules_frame.pack(pady=15)
        
        modules = [
            ("📚\n识字乐园", "#FF6B6B", "学汉字 认字游戏\n看图识字 听音选字", "kids_game_v3.py", "学认字，变聪明！", "literacy"),
            ("🔤\n拼音乐园", "#FF9800", "学拼音 声母韵母\n听音辨音 拼读练习", "kids_pinyin.py", "学拼音，读得准！", "pinyin"),
            ("🔢\n数学乐园", "#4CAF50", "学数学 数字形状\n数数比大小 简单加法", "kids_math.py", "学数学，算得快！", "math"),
            ("🌍\n英语乐园", "#2196F3", "学英语 ABC单词\n颜色动物 听音选词", "kids_english.py", "学英语，说得好！", "english"),
            ("🧠\n思维乐园", "#9C27B0", "练思维 动脑筋\n找不同 记忆配对", "kids_thinking.py", "动脑筋，变聪明！", "thinking"),
            ("🚗\n交通乐园", "#00BCD4", "认车车 大冒险\n开挖掘机 赛车飞机", "kids_vehicles.py", "认车车，去冒险！", "vehicles"),
        ]
        
        for i, (title, color, desc, script, voice_text, module_key) in enumerate(modules):
            row, col = i // 3, i % 3
            card = tk.Frame(modules_frame, bg=color, relief=tk.RAISED, bd=4)
            card.grid(row=row, column=col, padx=12, pady=12)
            
            btn = tk.Button(card, text=title, font=("微软雅黑", 18, "bold"), bg=color, fg="white", 
                           width=10, height=3, relief=tk.FLAT, cursor="hand2",
                           activebackground=color, activeforeground="white",
                           command=lambda s=script, v=voice_text: self.launch_module(s, v))
            btn.pack(padx=6, pady=6)
            
            # 显示模块等级
            if self.learning_data:
                level = self.learning_data.get_level(module_key)
                level_text = "⭐" * level
                tk.Label(card, text=f"难度: {level_text}", font=("微软雅黑", 9), bg=color, fg="white").pack()
            
            tk.Label(card, text=desc, font=("微软雅黑", 9), bg=color, fg="white", justify=tk.CENTER).pack(pady=3)
        
        # 提示 - 汪汪队风格
        paw_tips = ["🐕 汪汪队，出动！每个乐园都有6种趣味玩法！", "🐾 答对3题获得1颗星星！", "🏅 收集徽章，成为汪汪队小队员！", "📊 点击学习报告查看进度！"]
        tip_frame = tk.Frame(main_frame, bg=theme_helper.card_bg if THEME_AVAILABLE else "#C8E6C9", relief=tk.GROOVE, bd=2)
        tip_frame.pack(pady=10, fill=tk.X, padx=30)
        tk.Label(tip_frame, text=random.choice(paw_tips), font=("微软雅黑", 11), 
                bg=theme_helper.card_bg if THEME_AVAILABLE else "#C8E6C9", fg="#2E7D32", pady=8).pack()
        
        # 汪汪队底部装饰
        if THEME_AVAILABLE:
            bottom_canvas = tk.Canvas(main_frame, width=1000, height=80, bg=bg_color, highlightthickness=0)
            bottom_canvas.pack(pady=5)
            # 绘制草地
            bottom_canvas.create_rectangle(0, 50, 1000, 80, fill="#81C784", outline="")
            # 绘制狗狗角色
            ThemeDrawings.draw_puppy_chase(bottom_canvas, 100, 35, 0.45)
            ThemeDrawings.draw_puppy_marshall(bottom_canvas, 250, 35, 0.45)
            ThemeDrawings.draw_puppy_skye(bottom_canvas, 400, 35, 0.45)
            ThemeDrawings.draw_puppy_rubble(bottom_canvas, 550, 35, 0.45)
            ThemeDrawings.draw_puppy_rocky(bottom_canvas, 700, 35, 0.45)
            ThemeDrawings.draw_puppy_zuma(bottom_canvas, 850, 35, 0.45)
            # 绘制装饰
            ThemeDrawings.draw_bone(bottom_canvas, 175, 65, 25)
            ThemeDrawings.draw_star(bottom_canvas, 325, 65, 15, "#FFD700")
            ThemeDrawings.draw_bone(bottom_canvas, 475, 65, 25)
            ThemeDrawings.draw_star(bottom_canvas, 625, 65, 15, "#FFD700")
            ThemeDrawings.draw_bone(bottom_canvas, 775, 65, 25)
        else:
            tk.Label(main_frame, text="🎈 🎀 🌸 🎁 🎊 🌟 🎈 🎀 🌸 🎁 🎊 🌟", font=("Segoe UI Emoji", 14), bg=bg_color, fg="#A5D6A7").pack(pady=5)
        
        # 底部按钮 - 第一行
        bottom_frame = tk.Frame(main_frame, bg=bg_color)
        bottom_frame.pack(pady=5)
        
        tk.Button(bottom_frame, text="📊 学习报告", font=("微软雅黑", 10), bg="#FF9800", fg="white", 
                  relief=tk.RAISED, bd=3, cursor="hand2", padx=8, pady=2, command=self.show_learning_report).pack(side=tk.LEFT, padx=4)
        tk.Button(bottom_frame, text="🏅 我的徽章", font=("微软雅黑", 10), bg="#E91E63", fg="white", 
                  relief=tk.RAISED, bd=3, cursor="hand2", padx=8, pady=2, command=self.show_badges).pack(side=tk.LEFT, padx=4)
        tk.Button(bottom_frame, text="🎯 每日挑战", font=("微软雅黑", 10), bg="#F44336", fg="white", 
                  relief=tk.RAISED, bd=3, cursor="hand2", padx=8, pady=2, command=self.show_daily_challenges).pack(side=tk.LEFT, padx=4)
        tk.Button(bottom_frame, text="📝 错题复习", font=("微软雅黑", 10), bg="#2196F3", fg="white", 
                  relief=tk.RAISED, bd=3, cursor="hand2", padx=8, pady=2, command=self.show_wrong_questions).pack(side=tk.LEFT, padx=4)
        tk.Button(bottom_frame, text="🧠 智能复习", font=("微软雅黑", 10), bg="#673AB7", fg="white", 
                  relief=tk.RAISED, bd=3, cursor="hand2", padx=8, pady=2, command=self.show_smart_review).pack(side=tk.LEFT, padx=4)
        
        # 底部按钮 - 第二行
        bottom_frame2 = tk.Frame(main_frame, bg=bg_color)
        bottom_frame2.pack(pady=5)
        
        tk.Button(bottom_frame2, text="📅 每日计划", font=("微软雅黑", 10), bg="#00BCD4", fg="white", 
                  relief=tk.RAISED, bd=3, cursor="hand2", padx=10, pady=2, command=self.show_daily_plan_settings).pack(side=tk.LEFT, padx=5)
        tk.Button(bottom_frame2, text="🎨 主题风格", font=("微软雅黑", 10), bg="#E91E63", fg="white", 
                  relief=tk.RAISED, bd=3, cursor="hand2", padx=10, pady=2, command=self.show_theme_settings).pack(side=tk.LEFT, padx=5)
        tk.Button(bottom_frame2, text="⚙️ 语音设置", font=("微软雅黑", 10), bg="#9C27B0", fg="white", 
                  relief=tk.RAISED, bd=3, cursor="hand2", padx=10, pady=2, command=self.show_voice_settings).pack(side=tk.LEFT, padx=5)
        tk.Button(bottom_frame2, text="家长", font=("微软雅黑", 10), bg="#607D8B", fg="white", 
                  relief=tk.RAISED, bd=3, cursor="hand2", padx=10, pady=2, command=self.show_parent_panel).pack(side=tk.LEFT, padx=5)
        tk.Button(bottom_frame2, text="👋 退出", font=("微软雅黑", 10), bg="#FF5722", fg="white", 
                  relief=tk.RAISED, bd=3, cursor="hand2", padx=10, pady=2, command=self.confirm_and_exit).pack(side=tk.LEFT, padx=5)
        
        tk.Label(main_frame, text="v2.8 | 适合3-5岁宝宝 | 改进：退出确认、休息提醒、数据优化", font=("微软雅黑", 9), bg="#E8F5E9", fg="#AAA").pack(pady=5)
        
        self.window.after(500, lambda: self.speak("欢迎乐乐来学习！选择一个乐园开始吧！"))
        
        # 启动休息提醒检查
        self.start_rest_reminder_check()
        
        # 启动学习时间刷新（每30秒刷新一次）
        self.start_time_refresh()
        
        # 设置窗口关闭处理
        self.window.protocol("WM_DELETE_WINDOW", self.on_close_window)
    
    def on_close_window(self):
        """窗口关闭按钮处理"""
        self.confirm_and_exit()
    
    def confirm_and_exit(self):
        """确认退出"""
        result = messagebox.askyesno(
            "👋 确认退出",
            "确定要退出学习乐园吗？\n\n学习进度会自动保存哦！",
            icon='question',
            default='yes'
        )
        if result:
            self.on_exit()
    
    def on_exit(self):
        """退出时保存数据并清理"""
        try:
            # 保存学习数据
            if self.learning_data:
                self.learning_data.end_session()
            
            # 清理临时文件
            if BASE_MODULE_AVAILABLE:
                temp_file_manager.cleanup_all()
            
            # 停止pygame
            try:
                pygame.mixer.music.stop()
                pygame.mixer.quit()
            except:
                pass
        except Exception as e:
            print(f"退出清理错误: {e}")
        finally:
            self.window.quit()
    
    def show_learning_report(self):
        """显示学习报告"""
        if not self.learning_data:
            messagebox.showinfo("提示", "学习数据模块未加载")
            return
        
        report_win = tk.Toplevel(self.window)
        report_win.title("📊 学习报告")
        report_win.geometry("600x550")
        report_win.configure(bg="#E3F2FD")
        report_win.transient(self.window)
        report_win.grab_set()
        
        x = (report_win.winfo_screenwidth() - 600) // 2
        y = (report_win.winfo_screenheight() - 550) // 2
        report_win.geometry(f"+{x}+{y}")
        
        tk.Label(report_win, text="📊 乐乐的学习报告", font=("微软雅黑", 22, "bold"), bg="#E3F2FD", fg="#1565C0").pack(pady=15)
        
        # 总体统计
        stats = self.learning_data.get_stats()
        overall_frame = tk.Frame(report_win, bg="#BBDEFB", relief=tk.RAISED, bd=2)
        overall_frame.pack(fill=tk.X, padx=20, pady=10)
        
        tk.Label(overall_frame, text="📈 总体统计", font=("微软雅黑", 14, "bold"), bg="#BBDEFB", fg="#1565C0").pack(pady=8)
        
        stats_text = f"⭐ 星星: {stats['stars']}    🏅 徽章: {stats['badges']}    📅 学习天数: {stats['days']}\n"
        stats_text += f"✅ 答对: {stats['correct']}    ❌ 答错: {stats['wrong']}    📊 正确率: {stats['accuracy']}%"
        tk.Label(overall_frame, text=stats_text, font=("微软雅黑", 12), bg="#BBDEFB", fg="#333").pack(pady=8)
        
        # 各模块统计
        modules_frame = tk.Frame(report_win, bg="#E3F2FD")
        modules_frame.pack(fill=tk.BOTH, expand=True, padx=20, pady=10)
        
        tk.Label(modules_frame, text="📚 各模块学习情况", font=("微软雅黑", 14, "bold"), bg="#E3F2FD", fg="#1565C0").pack(pady=8)
        
        module_names = {
            "literacy": ("📚 识字", "#FF6B6B"),
            "pinyin": ("🔤 拼音", "#FF9800"),
            "math": ("🔢 数学", "#4CAF50"),
            "english": ("🌍 英语", "#2196F3"),
            "thinking": ("🧠 思维", "#9C27B0"),
            "vehicles": ("🚗 交通", "#00BCD4")
        }
        
        grid_frame = tk.Frame(modules_frame, bg="#E3F2FD")
        grid_frame.pack()
        
        for i, (key, (name, color)) in enumerate(module_names.items()):
            m_stats = self.learning_data.get_stats(key)
            
            card = tk.Frame(grid_frame, bg=color, relief=tk.RAISED, bd=2)
            card.grid(row=i//3, column=i%3, padx=8, pady=8)
            
            tk.Label(card, text=name, font=("微软雅黑", 11, "bold"), bg=color, fg="white").pack(pady=5, padx=15)
            tk.Label(card, text=f"难度: {'⭐'*m_stats['level']}", font=("微软雅黑", 9), bg=color, fg="white").pack()
            tk.Label(card, text=f"正确率: {m_stats['accuracy']}%", font=("微软雅黑", 9), bg=color, fg="white").pack()
            tk.Label(card, text=f"答题: {m_stats['total']}次", font=("微软雅黑", 9), bg=color, fg="white").pack(pady=(0,5))
        
        tk.Button(report_win, text="关闭", font=("微软雅黑", 12), bg="#4CAF50", fg="white", 
                 relief=tk.RAISED, bd=3, cursor="hand2", padx=30, command=report_win.destroy).pack(pady=15)
    
    def show_badges(self):
        """显示徽章收集"""
        if not self.learning_data:
            messagebox.showinfo("提示", "学习数据模块未加载")
            return
        
        badges_win = tk.Toplevel(self.window)
        badges_win.title("🏅 我的徽章")
        badges_win.geometry("650x500")
        badges_win.configure(bg="#FFF3E0")
        badges_win.transient(self.window)
        badges_win.grab_set()
        
        x = (badges_win.winfo_screenwidth() - 650) // 2
        y = (badges_win.winfo_screenheight() - 500) // 2
        badges_win.geometry(f"+{x}+{y}")
        
        tk.Label(badges_win, text="🏅 乐乐的徽章收集", font=("微软雅黑", 22, "bold"), bg="#FFF3E0", fg="#E65100").pack(pady=15)
        
        # 星星数量
        stars = self.learning_data.get_stars()
        tk.Label(badges_win, text=f"⭐ 我的星星: {stars} 颗", font=("微软雅黑", 16), bg="#FFF3E0", fg="#FF9800").pack(pady=5)
        
        # 徽章展示
        badges_frame = tk.Frame(badges_win, bg="#FFF3E0")
        badges_frame.pack(fill=tk.BOTH, expand=True, padx=20, pady=10)
        
        all_badges = self.learning_data.get_all_badges()
        
        for i, badge in enumerate(all_badges):
            row, col = i // 4, i % 4
            
            if badge["unlocked"]:
                bg_color = "#FFD54F"
                fg_color = "#5D4037"
                emoji = badge["emoji"]
            else:
                bg_color = "#E0E0E0"
                fg_color = "#9E9E9E"
                emoji = "🔒"
            
            card = tk.Frame(badges_frame, bg=bg_color, relief=tk.RAISED, bd=2)
            card.grid(row=row, column=col, padx=8, pady=8)
            
            tk.Label(card, text=emoji, font=("Segoe UI Emoji", 28), bg=bg_color).pack(pady=5, padx=15)
            tk.Label(card, text=badge["name"], font=("微软雅黑", 10, "bold"), bg=bg_color, fg=fg_color).pack()
            tk.Label(card, text=badge["desc"], font=("微软雅黑", 8), bg=bg_color, fg=fg_color, wraplength=100).pack(pady=(0,5))
        
        unlocked_count = len([b for b in all_badges if b["unlocked"]])
        tk.Label(badges_win, text=f"已解锁: {unlocked_count}/{len(all_badges)}", font=("微软雅黑", 12), bg="#FFF3E0", fg="#666").pack(pady=5)
        
        tk.Button(badges_win, text="关闭", font=("微软雅黑", 12), bg="#FF9800", fg="white", 
                 relief=tk.RAISED, bd=3, cursor="hand2", padx=30, command=badges_win.destroy).pack(pady=10)

    def show_help(self):
        help_win = tk.Toplevel(self.window)
        help_win.title("❓ 使用帮助")
        help_win.geometry("550x500")
        help_win.configure(bg="#E3F2FD")
        help_win.transient(self.window)
        help_win.grab_set()
        
        x = (help_win.winfo_screenwidth() - 550) // 2
        y = (help_win.winfo_screenheight() - 500) // 2
        help_win.geometry(f"+{x}+{y}")
        
        tk.Label(help_win, text="📖 使用帮助", font=("微软雅黑", 20, "bold"), bg="#E3F2FD", fg="#1565C0").pack(pady=15)
        
        help_text = """
🎮 基本操作：
• 鼠标点击按钮选择答案
• 方向键控制游戏中的角色移动
• 空格键在游戏中执行动作（如挖土、喷水）

🔊 语音功能：
• 自动朗读题目和反馈
• 可在"语音设置"中更换语音风格

📚 学习模块：
• 识字乐园：学习常用汉字，看图识字
• 拼音乐园：学习声母韵母，听音辨音
• 数学乐园：认识数字形状，学习加法
• 英语乐园：学习ABC字母和简单单词
• 思维乐园：训练记忆力和逻辑思维
• 交通乐园：认识交通工具，趣味游戏

💡 小贴士：
• 答对会有表扬，答错也有鼓励
• 每个模块有6种不同玩法
• 建议每次学习15-20分钟
        """
        
        text_frame = tk.Frame(help_win, bg="white", relief=tk.SUNKEN, bd=2)
        text_frame.pack(fill=tk.BOTH, expand=True, padx=20, pady=10)
        tk.Label(text_frame, text=help_text, font=("微软雅黑", 11), bg="white", fg="#333", 
                justify=tk.LEFT, anchor="nw").pack(fill=tk.BOTH, expand=True, padx=15, pady=10)
        tk.Button(help_win, text="知道了", font=("微软雅黑", 12), bg="#4CAF50", fg="white", 
                 relief=tk.RAISED, bd=3, cursor="hand2", padx=30, command=help_win.destroy).pack(pady=15)
    
    def launch_module(self, script, voice_text):
        self.speak(voice_text)
        
        # 模块映射
        module_map = {
            "kids_game_v3.py": (LITERACY_AVAILABLE, KidsLiteracyGame if LITERACY_AVAILABLE else None, "识字乐园"),
            "kids_pinyin.py": (PINYIN_AVAILABLE, KidsPinyinGame if PINYIN_AVAILABLE else None, "拼音乐园"),
            "kids_math.py": (MATH_AVAILABLE, KidsMathGame if MATH_AVAILABLE else None, "数学乐园"),
            "kids_english.py": (ENGLISH_AVAILABLE, KidsEnglishGame if ENGLISH_AVAILABLE else None, "英语乐园"),
            "kids_thinking.py": (THINKING_AVAILABLE, KidsThinkingGame if THINKING_AVAILABLE else None, "思维乐园"),
            "kids_vehicles.py": (VEHICLES_AVAILABLE, KidsVehiclesGame if VEHICLES_AVAILABLE else None, "交通乐园"),
        }
        
        if script in module_map:
            available, game_class, name = module_map[script]
            if available and game_class:
                try:
                    # 在新线程中启动模块窗口
                    def run_module():
                        try:
                            game = game_class()
                            game.run()
                        except Exception as e:
                            print(f"模块运行错误: {e}")
                    
                    # 直接在新窗口中运行（不阻塞主窗口）
                    threading.Thread(target=run_module, daemon=True).start()
                except Exception as e:
                    messagebox.showerror("错误", f"启动{name}失败：{e}")
            else:
                messagebox.showerror("错误", f"{name}模块未加载")
        else:
            # 回退到subprocess方式（开发模式）
            script_path = os.path.join(os.path.dirname(os.path.abspath(__file__)), script)
            if not os.path.exists(script_path):
                messagebox.showerror("错误", f"找不到模块文件：{script}")
                return
            
            try:
                subprocess.Popen([sys.executable, script_path], 
                               creationflags=subprocess.CREATE_NEW_CONSOLE if os.name == 'nt' else 0)
            except Exception as e:
                messagebox.showerror("错误", f"启动模块失败：{e}")
    
    def show_theme_settings(self):
        """显示主题选择"""
        if not THEME_AVAILABLE:
            messagebox.showinfo("提示", "主题系统未加载")
            return
        
        def on_theme_change(theme_id):
            from theme_config import THEMES
            theme = THEMES.get(theme_id, {})
            msg = f"已切换到：{theme.get('icon', '')} {theme.get('name', '')}主题"
            msg += "\n\n重新打开各模块后生效！"
            messagebox.showinfo("🎨 主题已更换", msg)
        
        show_theme_selector(self.window, on_theme_change)
    
    def show_voice_settings(self):
        settings_win = tk.Toplevel(self.window)
        settings_win.title("⚙️ 语音设置")
        settings_win.geometry("500x450")
        settings_win.configure(bg="#F3E5F5")
        settings_win.transient(self.window)
        settings_win.grab_set()
        
        x = (settings_win.winfo_screenwidth() - 500) // 2
        y = (settings_win.winfo_screenheight() - 450) // 2
        settings_win.geometry(f"+{x}+{y}")
        
        tk.Label(settings_win, text="🎤 选择语音风格", font=("微软雅黑", 20, "bold"), 
                bg="#F3E5F5", fg="#7B1FA2").pack(pady=15)
        tk.Label(settings_win, text=f"当前风格：{self.current_style}", 
                font=("微软雅黑", 12), bg="#F3E5F5", fg="#666").pack(pady=5)
        
        style_var = tk.StringVar(value=self.current_style)
        styles_frame = tk.Frame(settings_win, bg="#F3E5F5")
        styles_frame.pack(pady=15, fill=tk.X, padx=30)
        
        colors = ["#FF6B6B", "#4ECDC4", "#45B7D1", "#96CEB4"]
        for i, (style_name, style_data) in enumerate(VOICE_STYLES.items()):
            frame = tk.Frame(styles_frame, bg=colors[i % len(colors)], relief=tk.RAISED, bd=2)
            frame.pack(fill=tk.X, pady=5)
            rb = tk.Radiobutton(frame, text=f"  {style_name}", variable=style_var, value=style_name, 
                               font=("微软雅黑", 14, "bold"), bg=colors[i % len(colors)], fg="white",
                               selectcolor=colors[i % len(colors)], activebackground=colors[i % len(colors)],
                               command=lambda s=style_name: self.preview_voice(s))
            rb.pack(side=tk.LEFT, padx=10, pady=8)
            tk.Label(frame, text=style_data["desc"], font=("微软雅黑", 10), 
                    bg=colors[i % len(colors)], fg="white").pack(side=tk.RIGHT, padx=10)
        
        self.preview_label = tk.Label(settings_win, text="💡 点击选项可试听语音效果", 
                                      font=("微软雅黑", 11), bg="#F3E5F5", fg="#888")
        self.preview_label.pack(pady=10)
        
        btn_frame = tk.Frame(settings_win, bg="#F3E5F5")
        btn_frame.pack(pady=20)
        
        def save_and_close():
            selected = style_var.get()
            self.current_style = selected
            self.voice = VOICE_STYLES[selected]["voice"]
            self.voice_config["style"] = selected
            save_voice_config(self.voice_config)
            messagebox.showinfo("成功", f"语音风格已设置为：{selected}\n\n重新打开各模块后生效！")
            settings_win.destroy()
        
        tk.Button(btn_frame, text="✅ 保存设置", font=("微软雅黑", 12), bg="#4CAF50", fg="white", 
                 relief=tk.RAISED, bd=3, cursor="hand2", padx=20, command=save_and_close).pack(side=tk.LEFT, padx=10)
        tk.Button(btn_frame, text="❌ 取消", font=("微软雅黑", 12), bg="#9E9E9E", fg="white", 
                 relief=tk.RAISED, bd=3, cursor="hand2", padx=20, command=settings_win.destroy).pack(side=tk.LEFT, padx=10)
    
    def preview_voice(self, style_name):
        style = VOICE_STYLES[style_name]
        text = random.choice(style["praises"])
        self.preview_label.config(text=f"🔊 正在试听：{style_name}")
        self.voice = style["voice"]
        self.speak(text, "+10%")
    
    def show_wrong_questions(self):
        """显示错题复习"""
        if not self.learning_data:
            messagebox.showinfo("提示", "学习数据模块未加载")
            return
        
        wrong_win = tk.Toplevel(self.window)
        wrong_win.title("📝 错题复习")
        wrong_win.geometry("700x600")
        wrong_win.configure(bg="#FFF3E0")
        wrong_win.transient(self.window)
        wrong_win.grab_set()
        
        x = (wrong_win.winfo_screenwidth() - 700) // 2
        y = (wrong_win.winfo_screenheight() - 600) // 2
        wrong_win.geometry(f"+{x}+{y}")
        
        tk.Label(wrong_win, text="📝 错题复习", font=("微软雅黑", 22, "bold"), bg="#FFF3E0", fg="#E65100").pack(pady=15)
        
        # 各模块错题统计
        module_names = {
            "literacy": ("📚 识字", "#FF6B6B"),
            "pinyin": ("🔤 拼音", "#FF9800"),
            "math": ("🔢 数学", "#4CAF50"),
            "english": ("🌍 英语", "#2196F3"),
        }
        
        # 创建滚动区域
        canvas = tk.Canvas(wrong_win, bg="#FFF3E0", highlightthickness=0)
        scrollbar = tk.Scrollbar(wrong_win, orient="vertical", command=canvas.yview)
        scrollable_frame = tk.Frame(canvas, bg="#FFF3E0")
        
        scrollable_frame.bind(
            "<Configure>",
            lambda e: canvas.configure(scrollregion=canvas.bbox("all"))
        )
        
        canvas.create_window((0, 0), window=scrollable_frame, anchor="nw")
        canvas.configure(yscrollcommand=scrollbar.set)
        
        total_wrong = 0
        
        for module_key, (module_name, color) in module_names.items():
            wrong_list = self.learning_data.get_wrong_questions(module_key)
            total_wrong += len(wrong_list)
            
            # 模块标题
            module_frame = tk.Frame(scrollable_frame, bg=color, relief=tk.RAISED, bd=2)
            module_frame.pack(fill=tk.X, padx=20, pady=8)
            
            tk.Label(module_frame, text=f"{module_name} - 错题: {len(wrong_list)}道", 
                    font=("微软雅黑", 12, "bold"), bg=color, fg="white").pack(pady=8, padx=15)
            
            if wrong_list:
                # 显示错题列表
                for i, q in enumerate(wrong_list[:10]):  # 最多显示10道
                    q_frame = tk.Frame(scrollable_frame, bg="white", relief=tk.GROOVE, bd=1)
                    q_frame.pack(fill=tk.X, padx=30, pady=3)
                    
                    question = q.get("question", "未知题目")
                    answer = q.get("answer", "")
                    wrong_count = q.get("wrong_count", 1)
                    
                    tk.Label(q_frame, text=f"❌ {question}", font=("微软雅黑", 10), 
                            bg="white", fg="#333", anchor="w").pack(side=tk.LEFT, padx=10, pady=5)
                    tk.Label(q_frame, text=f"答案: {answer} | 错{wrong_count}次", 
                            font=("微软雅黑", 9), bg="white", fg="#888").pack(side=tk.RIGHT, padx=10, pady=5)
                
                if len(wrong_list) > 10:
                    tk.Label(scrollable_frame, text=f"... 还有 {len(wrong_list)-10} 道错题", 
                            font=("微软雅黑", 9), bg="#FFF3E0", fg="#888").pack(pady=3)
            else:
                tk.Label(scrollable_frame, text="✅ 太棒了！没有错题！", 
                        font=("微软雅黑", 10), bg="#FFF3E0", fg="#4CAF50").pack(pady=5)
        
        canvas.pack(side="left", fill="both", expand=True, padx=10, pady=10)
        scrollbar.pack(side="right", fill="y")
        
        # 底部统计
        bottom_frame = tk.Frame(wrong_win, bg="#FFF3E0")
        bottom_frame.pack(fill=tk.X, pady=10)
        
        if total_wrong > 0:
            tk.Label(bottom_frame, text=f"📊 共有 {total_wrong} 道错题需要复习", 
                    font=("微软雅黑", 12), bg="#FFF3E0", fg="#E65100").pack(pady=5)
            tk.Label(bottom_frame, text="💡 多练习这些题目，下次一定能答对！", 
                    font=("微软雅黑", 10), bg="#FFF3E0", fg="#888").pack()
        else:
            tk.Label(bottom_frame, text="🎉 太棒了！没有错题！继续保持！", 
                    font=("微软雅黑", 14, "bold"), bg="#FFF3E0", fg="#4CAF50").pack(pady=10)
        
        tk.Button(wrong_win, text="关闭", font=("微软雅黑", 12), bg="#FF9800", fg="white", 
                 relief=tk.RAISED, bd=3, cursor="hand2", padx=30, command=wrong_win.destroy).pack(pady=10)
    
    def show_daily_plan_settings(self):
        """显示每日计划设置界面"""
        if not self.learning_data:
            messagebox.showinfo("提示", "学习数据模块未加载")
            return
        
        plan_win = tk.Toplevel(self.window)
        plan_win.title("📅 每日学习计划")
        plan_win.geometry("500x520")
        plan_win.configure(bg="#E1F5FE")
        plan_win.transient(self.window)
        plan_win.grab_set()
        
        x = (plan_win.winfo_screenwidth() - 500) // 2
        y = (plan_win.winfo_screenheight() - 520) // 2
        plan_win.geometry(f"+{x}+{y}")
        
        tk.Label(plan_win, text="📅 每日学习计划", font=("微软雅黑", 22, "bold"), 
                bg="#E1F5FE", fg="#0277BD").pack(pady=15)
        
        # 获取当前计划
        current_plan = self.learning_data.get_daily_plan()
        
        # 今日进度卡片
        progress_card = tk.Frame(plan_win, bg="#81D4FA", relief=tk.RAISED, bd=3)
        progress_card.pack(fill=tk.X, padx=30, pady=10)
        
        tk.Label(progress_card, text="📊 今日学习进度", font=("微软雅黑", 14, "bold"), 
                bg="#81D4FA", fg="#01579B").pack(pady=8)
        
        progress_text = f"✅ 已答题: {current_plan['today_questions']}/{current_plan['target_questions']} 题\n"
        progress_text += f"🎯 正确率: {int(current_plan['today_correct']/current_plan['today_questions']*100) if current_plan['today_questions'] > 0 else 0}%\n"
        progress_text += f"⏱️ 学习时长: {current_plan['today_minutes']} 分钟"
        
        tk.Label(progress_card, text=progress_text, font=("微软雅黑", 11), 
                bg="#81D4FA", fg="#01579B", justify=tk.LEFT).pack(pady=5, padx=15)
        
        if current_plan["goal_completed"]:
            tk.Label(progress_card, text="🎉 今日目标已完成！太棒了！", font=("微软雅黑", 12, "bold"), 
                    bg="#81D4FA", fg="#4CAF50").pack(pady=5)
        else:
            remaining = current_plan['target_questions'] - current_plan['today_questions']
            tk.Label(progress_card, text=f"💪 还差 {remaining} 题完成目标，加油！", font=("微软雅黑", 11), 
                    bg="#81D4FA", fg="#E65100").pack(pady=5)
        
        # 设置区域
        settings_frame = tk.Frame(plan_win, bg="#E1F5FE")
        settings_frame.pack(fill=tk.X, padx=30, pady=15)
        
        tk.Label(settings_frame, text="⚙️ 目标设置", font=("微软雅黑", 14, "bold"), 
                bg="#E1F5FE", fg="#0277BD").pack(pady=8)
        
        # 每日目标答题数
        q_frame = tk.Frame(settings_frame, bg="#E1F5FE")
        q_frame.pack(fill=tk.X, pady=8)
        tk.Label(q_frame, text="📝 每日目标答题数:", font=("微软雅黑", 11), 
                bg="#E1F5FE", fg="#333").pack(side=tk.LEFT, padx=10)
        
        target_q_var = tk.IntVar(value=current_plan['target_questions'])
        q_options = [10, 20, 30, 50, 100]
        for val in q_options:
            tk.Radiobutton(q_frame, text=str(val), variable=target_q_var, value=val,
                          font=("微软雅黑", 10), bg="#E1F5FE", fg="#333",
                          selectcolor="#81D4FA").pack(side=tk.LEFT, padx=5)
        
        # 每日目标学习时长
        t_frame = tk.Frame(settings_frame, bg="#E1F5FE")
        t_frame.pack(fill=tk.X, pady=8)
        tk.Label(t_frame, text="⏰ 每日目标时长:", font=("微软雅黑", 11), 
                bg="#E1F5FE", fg="#333").pack(side=tk.LEFT, padx=10)
        
        target_t_var = tk.IntVar(value=self.learning_data.data["daily_plan"]["target_minutes"])
        t_options = [10, 15, 20, 30, 45]
        for val in t_options:
            tk.Radiobutton(t_frame, text=f"{val}分钟", variable=target_t_var, value=val,
                          font=("微软雅黑", 10), bg="#E1F5FE", fg="#333",
                          selectcolor="#81D4FA").pack(side=tk.LEFT, padx=3)
        
        # 休息提醒间隔
        r_frame = tk.Frame(settings_frame, bg="#E1F5FE")
        r_frame.pack(fill=tk.X, pady=8)
        tk.Label(r_frame, text="😴 休息提醒间隔:", font=("微软雅黑", 11), 
                bg="#E1F5FE", fg="#333").pack(side=tk.LEFT, padx=10)
        
        rest_var = tk.IntVar(value=self.learning_data.data["daily_plan"]["rest_reminder"])
        r_options = [(0, "关闭"), (10, "10分钟"), (15, "15分钟"), (20, "20分钟"), (30, "30分钟")]
        for val, text in r_options:
            tk.Radiobutton(r_frame, text=text, variable=rest_var, value=val,
                          font=("微软雅黑", 10), bg="#E1F5FE", fg="#333",
                          selectcolor="#81D4FA").pack(side=tk.LEFT, padx=3)
        
        # 提示
        tip_frame = tk.Frame(plan_win, bg="#B3E5FC", relief=tk.GROOVE, bd=2)
        tip_frame.pack(fill=tk.X, padx=30, pady=10)
        tk.Label(tip_frame, text="💡 小贴士：建议每次学习15-20分钟，保护眼睛哦！", 
                font=("微软雅黑", 10), bg="#B3E5FC", fg="#01579B", pady=8).pack()
        
        # 按钮
        btn_frame = tk.Frame(plan_win, bg="#E1F5FE")
        btn_frame.pack(pady=15)
        
        def save_settings():
            self.learning_data.set_daily_targets(
                target_questions=target_q_var.get(),
                target_minutes=target_t_var.get(),
                rest_reminder=rest_var.get()
            )
            self.speak("设置已保存！")
            messagebox.showinfo("成功", "每日计划设置已保存！")
            plan_win.destroy()
            # 刷新主界面
            self.create_main_menu()
        
        tk.Button(btn_frame, text="✅ 保存设置", font=("微软雅黑", 12), bg="#4CAF50", fg="white", 
                 relief=tk.RAISED, bd=3, cursor="hand2", padx=20, command=save_settings).pack(side=tk.LEFT, padx=10)
        tk.Button(btn_frame, text="❌ 取消", font=("微软雅黑", 12), bg="#9E9E9E", fg="white", 
                 relief=tk.RAISED, bd=3, cursor="hand2", padx=20, command=plan_win.destroy).pack(side=tk.LEFT, padx=10)
    
    def start_rest_reminder_check(self):
        """启动休息提醒定时检查"""
        def check_rest():
            if not self.learning_data:
                return
            
            if self.learning_data.should_show_rest_reminder():
                self.show_rest_reminder()
            
            # 每分钟检查一次
            self.window.after(60000, check_rest)
        
        # 延迟1分钟后开始检查
        self.window.after(60000, check_rest)
    
    def start_time_refresh(self):
        """启动学习时间定时刷新"""
        def refresh_time():
            if not self.learning_data:
                return
            
            # 更新时间标签（如果存在）
            if hasattr(self, 'time_label') and self.time_label.winfo_exists():
                session_minutes = self.learning_data.get_session_minutes()
                self.time_label.config(text=f"⏱️ 已学习: {session_minutes}分钟")
            
            # 每30秒刷新一次
            self.window.after(30000, refresh_time)
        
        # 延迟30秒后开始刷新
        self.window.after(30000, refresh_time)
    
    def show_rest_reminder(self):
        """显示休息提醒弹窗"""
        session_minutes = self.learning_data.get_session_minutes()
        
        rest_win = tk.Toplevel(self.window)
        rest_win.title("😴 休息一下")
        rest_win.geometry("400x350")
        rest_win.configure(bg="#E8F5E9")
        rest_win.transient(self.window)
        rest_win.grab_set()
        
        x = (rest_win.winfo_screenwidth() - 400) // 2
        y = (rest_win.winfo_screenheight() - 350) // 2
        rest_win.geometry(f"+{x}+{y}")
        
        # 可爱的提醒界面
        tk.Label(rest_win, text="😴", font=("Segoe UI Emoji", 60), bg="#E8F5E9").pack(pady=15)
        tk.Label(rest_win, text="乐乐，休息一下吧！", font=("微软雅黑", 20, "bold"), 
                bg="#E8F5E9", fg="#2E7D32").pack(pady=5)
        
        tk.Label(rest_win, text=f"你已经学习了 {session_minutes} 分钟啦！", 
                font=("微软雅黑", 14), bg="#E8F5E9", fg="#666").pack(pady=5)
        
        # 休息建议
        tips = [
            "👀 闭上眼睛休息一会儿",
            "🚶 站起来走一走",
            "💧 喝点水补充水分",
            "🌳 看看窗外的绿色植物",
            "🤸 做做伸展运动"
        ]
        
        tip_frame = tk.Frame(rest_win, bg="#C8E6C9", relief=tk.GROOVE, bd=2)
        tip_frame.pack(fill=tk.X, padx=30, pady=15)
        tk.Label(tip_frame, text="💡 休息小建议：", font=("微软雅黑", 11, "bold"), 
                bg="#C8E6C9", fg="#2E7D32").pack(pady=5)
        
        import random
        selected_tips = random.sample(tips, 3)
        for tip in selected_tips:
            tk.Label(tip_frame, text=tip, font=("微软雅黑", 10), 
                    bg="#C8E6C9", fg="#333").pack(pady=2)
        
        tk.Button(rest_win, text="好的，我休息一下！", font=("微软雅黑", 12), 
                 bg="#4CAF50", fg="white", relief=tk.RAISED, bd=3, cursor="hand2", 
                 padx=20, pady=5, command=rest_win.destroy).pack(pady=15)
        
        # 语音提醒
        self.speak("乐乐，你已经学习很久了，休息一下眼睛吧！")
    
    def show_smart_review(self):
        """显示智能复习界面（艾宾浩斯记忆曲线）"""
        if not self.learning_data:
            messagebox.showinfo("提示", "学习数据模块未加载")
            return
        
        review_win = tk.Toplevel(self.window)
        review_win.title("🧠 智能复习")
        review_win.geometry("650x600")
        review_win.configure(bg="#EDE7F6")
        review_win.transient(self.window)
        review_win.grab_set()
        
        x = (review_win.winfo_screenwidth() - 650) // 2
        y = (review_win.winfo_screenheight() - 600) // 2
        review_win.geometry(f"+{x}+{y}")
        
        tk.Label(review_win, text="🧠 智能复习", font=("微软雅黑", 22, "bold"), 
                bg="#EDE7F6", fg="#4527A0").pack(pady=15)
        tk.Label(review_win, text="基于艾宾浩斯遗忘曲线，科学安排复习时间", 
                font=("微软雅黑", 10), bg="#EDE7F6", fg="#666").pack()
        
        # 获取复习统计
        stats = self.learning_data.get_review_stats()
        due_items = self.learning_data.get_due_reviews()
        
        # 统计卡片
        stats_frame = tk.Frame(review_win, bg="#D1C4E9", relief=tk.RAISED, bd=3)
        stats_frame.pack(fill=tk.X, padx=30, pady=15)
        
        tk.Label(stats_frame, text="📊 复习统计", font=("微软雅黑", 14, "bold"), 
                bg="#D1C4E9", fg="#4527A0").pack(pady=8)
        
        stats_text = f"📚 总学习内容: {stats['total']} 项  |  "
        stats_text += f"⏰ 今日待复习: {stats['due_today']} 项  |  "
        stats_text += f"✅ 已掌握: {stats['mastered']} 项"
        tk.Label(stats_frame, text=stats_text, font=("微软雅黑", 11), 
                bg="#D1C4E9", fg="#333").pack(pady=5)
        
        # 各类别统计
        category_names = {"literacy": "📚识字", "pinyin": "🔤拼音", "english": "🌍英语", "math": "🔢数学"}
        cat_frame = tk.Frame(stats_frame, bg="#D1C4E9")
        cat_frame.pack(pady=5)
        
        for cat, name in category_names.items():
            cat_stats = stats["by_category"].get(cat, {"total": 0, "due": 0})
            tk.Label(cat_frame, text=f"{name}: {cat_stats['total']}项({cat_stats['due']}待复习)", 
                    font=("微软雅黑", 9), bg="#D1C4E9", fg="#555").pack(side=tk.LEFT, padx=8)
        
        # 今日待复习列表
        list_frame = tk.Frame(review_win, bg="#EDE7F6")
        list_frame.pack(fill=tk.BOTH, expand=True, padx=30, pady=10)
        
        tk.Label(list_frame, text="⏰ 今日待复习内容", font=("微软雅黑", 14, "bold"), 
                bg="#EDE7F6", fg="#4527A0").pack(pady=8)
        
        if due_items:
            # 创建滚动区域
            canvas = tk.Canvas(list_frame, bg="#EDE7F6", highlightthickness=0, height=200)
            scrollbar = tk.Scrollbar(list_frame, orient="vertical", command=canvas.yview)
            scrollable = tk.Frame(canvas, bg="#EDE7F6")
            
            scrollable.bind("<Configure>", lambda e: canvas.configure(scrollregion=canvas.bbox("all")))
            canvas.create_window((0, 0), window=scrollable, anchor="nw")
            canvas.configure(yscrollcommand=scrollbar.set)
            
            for item in due_items[:20]:  # 最多显示20项
                item_frame = tk.Frame(scrollable, bg="white", relief=tk.GROOVE, bd=1)
                item_frame.pack(fill=tk.X, pady=3, padx=5)
                
                cat_emoji = {"literacy": "📚", "pinyin": "🔤", "english": "🌍", "math": "🔢"}.get(item["category"], "📖")
                display = item.get("display_name", item["item"])
                review_count = item.get("review_count", 0)
                
                tk.Label(item_frame, text=f"{cat_emoji} {display}", font=("微软雅黑", 11), 
                        bg="white", fg="#333").pack(side=tk.LEFT, padx=10, pady=5)
                tk.Label(item_frame, text=f"已复习{review_count}次", font=("微软雅黑", 9), 
                        bg="white", fg="#888").pack(side=tk.RIGHT, padx=10, pady=5)
            
            canvas.pack(side="left", fill="both", expand=True)
            scrollbar.pack(side="right", fill="y")
            
            # 开始复习按钮
            tk.Button(review_win, text="🚀 开始今日复习", font=("微软雅黑", 14, "bold"), 
                     bg="#673AB7", fg="white", relief=tk.RAISED, bd=3, cursor="hand2", 
                     padx=30, pady=8, command=lambda: self.start_review_session(review_win, due_items)).pack(pady=15)
        else:
            # 没有待复习内容
            tk.Label(list_frame, text="🎉", font=("Segoe UI Emoji", 50), bg="#EDE7F6").pack(pady=10)
            tk.Label(list_frame, text="太棒了！今天没有需要复习的内容！", 
                    font=("微软雅黑", 14), bg="#EDE7F6", fg="#4CAF50").pack()
            tk.Label(list_frame, text="继续学习新内容，系统会自动安排复习计划", 
                    font=("微软雅黑", 10), bg="#EDE7F6", fg="#888").pack(pady=5)
        
        # 复习日历预览
        calendar = self.learning_data.get_review_calendar(7)
        cal_frame = tk.Frame(review_win, bg="#B39DDB", relief=tk.GROOVE, bd=2)
        cal_frame.pack(fill=tk.X, padx=30, pady=10)
        
        tk.Label(cal_frame, text="📅 未来7天复习计划", font=("微软雅黑", 11, "bold"), 
                bg="#B39DDB", fg="#4527A0").pack(pady=5)
        
        days_frame = tk.Frame(cal_frame, bg="#B39DDB")
        days_frame.pack(pady=5)
        
        from datetime import datetime, timedelta
        today = datetime.now().date()
        day_names = ["今天", "明天", "后天"]
        
        for i, (date_str, count) in enumerate(calendar.items()):
            day_label = day_names[i] if i < 3 else f"{i+1}天后"
            color = "#4CAF50" if count == 0 else ("#FF9800" if count < 5 else "#F44336")
            
            day_card = tk.Frame(days_frame, bg=color, relief=tk.RAISED, bd=1)
            day_card.pack(side=tk.LEFT, padx=3)
            tk.Label(day_card, text=day_label, font=("微软雅黑", 8), bg=color, fg="white").pack(padx=8, pady=2)
            tk.Label(day_card, text=f"{count}项", font=("微软雅黑", 9, "bold"), bg=color, fg="white").pack(padx=8, pady=2)
        
        tk.Button(review_win, text="关闭", font=("微软雅黑", 11), bg="#9E9E9E", fg="white", 
                 relief=tk.RAISED, bd=3, cursor="hand2", padx=20, command=review_win.destroy).pack(pady=10)
    
    def start_review_session(self, parent_win, items):
        """开始复习会话"""
        if not items:
            return
        
        parent_win.destroy()
        
        # 创建复习窗口
        self.review_items = items.copy()
        self.review_index = 0
        self.review_correct = 0
        
        self.review_win = tk.Toplevel(self.window)
        self.review_win.title("🧠 复习中...")
        self.review_win.geometry("600x500")
        self.review_win.configure(bg="#EDE7F6")
        self.review_win.transient(self.window)
        self.review_win.grab_set()
        
        x = (self.review_win.winfo_screenwidth() - 600) // 2
        y = (self.review_win.winfo_screenheight() - 500) // 2
        self.review_win.geometry(f"+{x}+{y}")
        
        self.show_review_question()
    
    def show_review_question(self):
        """显示复习题目"""
        if self.review_index >= len(self.review_items):
            self.finish_review_session()
            return
        
        # 清空窗口
        for widget in self.review_win.winfo_children():
            widget.destroy()
        
        item = self.review_items[self.review_index]
        total = len(self.review_items)
        
        # 进度
        tk.Label(self.review_win, text=f"复习进度: {self.review_index + 1}/{total}", 
                font=("微软雅黑", 12), bg="#EDE7F6", fg="#666").pack(pady=10)
        
        # 进度条
        progress_frame = tk.Frame(self.review_win, bg="#D1C4E9", height=10, relief=tk.SUNKEN, bd=1)
        progress_frame.pack(fill=tk.X, padx=50, pady=5)
        progress_frame.pack_propagate(False)
        progress_pct = (self.review_index + 1) / total
        fill = tk.Frame(progress_frame, bg="#673AB7", width=int(500 * progress_pct), height=10)
        fill.pack(side=tk.LEFT)
        
        # 题目内容
        cat_emoji = {"literacy": "📚", "pinyin": "🔤", "english": "🌍", "math": "🔢"}.get(item["category"], "📖")
        cat_name = {"literacy": "识字", "pinyin": "拼音", "english": "英语", "math": "数学"}.get(item["category"], "")
        
        tk.Label(self.review_win, text=f"{cat_emoji} {cat_name}复习", font=("微软雅黑", 14), 
                bg="#EDE7F6", fg="#4527A0").pack(pady=15)
        
        display = item.get("display_name", item["item"])
        tk.Label(self.review_win, text=display, font=("微软雅黑", 48, "bold"), 
                bg="#EDE7F6", fg="#333").pack(pady=30)
        
        # 朗读按钮
        tk.Button(self.review_win, text="🔊 听一听", font=("微软雅黑", 12), bg="#2196F3", fg="white", 
                 relief=tk.RAISED, bd=3, cursor="hand2", padx=15, 
                 command=lambda: self.speak(display)).pack(pady=10)
        
        # 自评按钮
        tk.Label(self.review_win, text="你记住了吗？", font=("微软雅黑", 14), 
                bg="#EDE7F6", fg="#666").pack(pady=20)
        
        btn_frame = tk.Frame(self.review_win, bg="#EDE7F6")
        btn_frame.pack(pady=10)
        
        tk.Button(btn_frame, text="😊 记住了！", font=("微软雅黑", 14), bg="#4CAF50", fg="white", 
                 relief=tk.RAISED, bd=3, cursor="hand2", padx=25, pady=8,
                 command=lambda: self.review_answer(item, True)).pack(side=tk.LEFT, padx=15)
        tk.Button(btn_frame, text="😅 忘记了...", font=("微软雅黑", 14), bg="#FF9800", fg="white", 
                 relief=tk.RAISED, bd=3, cursor="hand2", padx=25, pady=8,
                 command=lambda: self.review_answer(item, False)).pack(side=tk.LEFT, padx=15)
        
        # 朗读题目
        self.speak(f"复习{cat_name}，{display}")
    
    def review_answer(self, item, is_correct):
        """处理复习答案"""
        # 更新复习记录
        self.learning_data.update_review_item(item["category"], item["item"], is_correct)
        
        if is_correct:
            self.review_correct += 1
            self.speak(random.choice(["太棒了！", "记得真好！", "真厉害！"]))
        else:
            self.speak(random.choice(["没关系，多复习几次就记住了！", "加油，下次一定能记住！"]))
        
        self.review_index += 1
        self.review_win.after(1500, self.show_review_question)
    
    def finish_review_session(self):
        """完成复习会话"""
        for widget in self.review_win.winfo_children():
            widget.destroy()
        
        total = len(self.review_items)
        accuracy = int(self.review_correct / total * 100) if total > 0 else 0
        
        tk.Label(self.review_win, text="🎉", font=("Segoe UI Emoji", 60), bg="#EDE7F6").pack(pady=20)
        tk.Label(self.review_win, text="复习完成！", font=("微软雅黑", 24, "bold"), 
                bg="#EDE7F6", fg="#4527A0").pack(pady=10)
        
        result_text = f"共复习 {total} 项内容\n记住了 {self.review_correct} 项\n正确率: {accuracy}%"
        tk.Label(self.review_win, text=result_text, font=("微软雅黑", 14), 
                bg="#EDE7F6", fg="#333").pack(pady=15)
        
        if accuracy >= 80:
            msg = "太棒了！记忆力超强！"
            self.speak("太棒了，乐乐记忆力超强！")
        elif accuracy >= 60:
            msg = "不错哦，继续加油！"
            self.speak("不错哦，继续加油！")
        else:
            msg = "多复习几次就能记住啦！"
            self.speak("多复习几次就能记住啦！")
        
        tk.Label(self.review_win, text=msg, font=("微软雅黑", 16), 
                bg="#EDE7F6", fg="#4CAF50").pack(pady=10)
        
        tk.Button(self.review_win, text="完成", font=("微软雅黑", 14), bg="#673AB7", fg="white", 
                 relief=tk.RAISED, bd=3, cursor="hand2", padx=30, pady=5,
                 command=self.review_win.destroy).pack(pady=20)
    
    def show_parent_panel(self):
        """显示家长控制面板（需要密码验证）"""
        if not self.learning_data:
            messagebox.showinfo("提示", "学习数据模块未加载")
            return
        
        settings = self.learning_data.get_parent_settings()
        
        # 如果设置了密码，需要验证
        if settings.get("password"):
            self.show_password_dialog()
        else:
            self.open_parent_panel()
    
    def show_password_dialog(self):
        """显示密码输入对话框"""
        pwd_win = tk.Toplevel(self.window)
        pwd_win.title("🔐 家长验证")
        pwd_win.geometry("350x200")
        pwd_win.configure(bg="#ECEFF1")
        pwd_win.transient(self.window)
        pwd_win.grab_set()
        
        x = (pwd_win.winfo_screenwidth() - 350) // 2
        y = (pwd_win.winfo_screenheight() - 200) // 2
        pwd_win.geometry(f"+{x}+{y}")
        
        tk.Label(pwd_win, text="🔐 请输入家长密码", font=("微软雅黑", 16, "bold"), 
                bg="#ECEFF1", fg="#37474F").pack(pady=20)
        
        pwd_entry = tk.Entry(pwd_win, font=("微软雅黑", 14), show="*", width=20)
        pwd_entry.pack(pady=10)
        pwd_entry.focus()
        
        def verify():
            if self.learning_data.verify_parent_password(pwd_entry.get()):
                pwd_win.destroy()
                self.open_parent_panel()
            else:
                messagebox.showerror("错误", "密码错误！")
                pwd_entry.delete(0, tk.END)
        
        pwd_entry.bind("<Return>", lambda e: verify())
        
        btn_frame = tk.Frame(pwd_win, bg="#ECEFF1")
        btn_frame.pack(pady=15)
        tk.Button(btn_frame, text="确定", font=("微软雅黑", 11), bg="#4CAF50", fg="white", 
                 relief=tk.RAISED, bd=3, padx=20, command=verify).pack(side=tk.LEFT, padx=10)
        tk.Button(btn_frame, text="取消", font=("微软雅黑", 11), bg="#9E9E9E", fg="white", 
                 relief=tk.RAISED, bd=3, padx=20, command=pwd_win.destroy).pack(side=tk.LEFT, padx=10)
    
    def open_parent_panel(self):
        """打开家长控制面板"""
        parent_win = tk.Toplevel(self.window)
        parent_win.title("👨‍👩‍👧 家长控制面板")
        parent_win.geometry("750x650")
        parent_win.configure(bg="#ECEFF1")
        parent_win.transient(self.window)
        parent_win.grab_set()
        
        x = (parent_win.winfo_screenwidth() - 750) // 2
        y = (parent_win.winfo_screenheight() - 650) // 2
        parent_win.geometry(f"+{x}+{y}")
        
        tk.Label(parent_win, text="👨‍👩‍👧 家长控制面板", font=("微软雅黑", 20, "bold"), 
                bg="#ECEFF1", fg="#37474F").pack(pady=15)
        
        # 创建选项卡
        notebook = ttk.Notebook(parent_win)
        notebook.pack(fill=tk.BOTH, expand=True, padx=20, pady=10)
        
        # 选项卡1：学习报告
        report_frame = tk.Frame(notebook, bg="#FAFAFA")
        notebook.add(report_frame, text="📊 学习报告")
        self.create_report_tab(report_frame)
        
        # 选项卡2：时间控制
        time_frame = tk.Frame(notebook, bg="#FAFAFA")
        notebook.add(time_frame, text="⏰ 时间控制")
        self.create_time_control_tab(time_frame)
        
        # 选项卡3：安全设置
        security_frame = tk.Frame(notebook, bg="#FAFAFA")
        notebook.add(security_frame, text="🔐 安全设置")
        self.create_security_tab(security_frame)
        
        # 选项卡4：数据管理
        data_frame = tk.Frame(notebook, bg="#FAFAFA")
        notebook.add(data_frame, text="💾 数据管理")
        self.create_data_tab(data_frame)
        
        tk.Button(parent_win, text="关闭", font=("微软雅黑", 12), bg="#607D8B", fg="white", 
                 relief=tk.RAISED, bd=3, cursor="hand2", padx=30, command=parent_win.destroy).pack(pady=15)
    
    def create_report_tab(self, parent):
        """创建学习报告选项卡"""
        report = self.learning_data.get_weekly_report()
        stats = self.learning_data.get_stats()
        
        # 总体统计
        summary_frame = tk.Frame(parent, bg="#E3F2FD", relief=tk.RAISED, bd=2)
        summary_frame.pack(fill=tk.X, padx=15, pady=10)
        
        tk.Label(summary_frame, text="📈 总体学习情况", font=("微软雅黑", 14, "bold"), 
                bg="#E3F2FD", fg="#1565C0").pack(pady=8)
        
        summary_text = f"累计学习天数: {stats['days']} 天  |  总答题: {stats['total']} 题  |  "
        summary_text += f"正确率: {stats['accuracy']}%  |  星星: {stats['stars']} ⭐"
        tk.Label(summary_frame, text=summary_text, font=("微软雅黑", 11), 
                bg="#E3F2FD", fg="#333").pack(pady=5)
        
        # 本周学习时长图表（简易柱状图）
        week_frame = tk.Frame(parent, bg="#FFF3E0", relief=tk.RAISED, bd=2)
        week_frame.pack(fill=tk.X, padx=15, pady=10)
        
        tk.Label(week_frame, text="📅 本周学习时长", font=("微软雅黑", 14, "bold"), 
                bg="#FFF3E0", fg="#E65100").pack(pady=8)
        
        chart_frame = tk.Frame(week_frame, bg="#FFF3E0")
        chart_frame.pack(pady=10)
        
        max_minutes = max([d["minutes"] for d in report["daily_data"]] + [1])
        
        for day_data in report["daily_data"]:
            day_frame = tk.Frame(chart_frame, bg="#FFF3E0")
            day_frame.pack(side=tk.LEFT, padx=8)
            
            # 柱状图
            bar_height = int(80 * day_data["minutes"] / max_minutes) if max_minutes > 0 else 0
            bar_container = tk.Frame(day_frame, bg="#FFF3E0", height=80, width=30)
            bar_container.pack()
            bar_container.pack_propagate(False)
            
            spacer = tk.Frame(bar_container, bg="#FFF3E0", height=80-bar_height)
            spacer.pack()
            
            if bar_height > 0:
                bar = tk.Frame(bar_container, bg="#FF9800", height=bar_height, width=30)
                bar.pack()
            
            tk.Label(day_frame, text=f"{day_data['minutes']}分", font=("微软雅黑", 8), 
                    bg="#FFF3E0", fg="#666").pack()
            tk.Label(day_frame, text=day_data["weekday"], font=("微软雅黑", 9), 
                    bg="#FFF3E0", fg="#333").pack()
        
        tk.Label(week_frame, text=f"本周总学习时长: {report['total_minutes']} 分钟", 
                font=("微软雅黑", 11), bg="#FFF3E0", fg="#E65100").pack(pady=5)
        
        # 各模块统计
        module_frame = tk.Frame(parent, bg="#E8F5E9", relief=tk.RAISED, bd=2)
        module_frame.pack(fill=tk.X, padx=15, pady=10)
        
        tk.Label(module_frame, text="📚 各模块学习情况", font=("微软雅黑", 14, "bold"), 
                bg="#E8F5E9", fg="#2E7D32").pack(pady=8)
        
        modules_grid = tk.Frame(module_frame, bg="#E8F5E9")
        modules_grid.pack(pady=5)
        
        module_names = {"literacy": "识字", "pinyin": "拼音", "math": "数学", 
                       "english": "英语", "thinking": "思维", "vehicles": "交通"}
        
        for i, (key, name) in enumerate(module_names.items()):
            m_stats = report["module_stats"].get(key, {"correct": 0, "wrong": 0, "level": 1})
            total = m_stats["correct"] + m_stats["wrong"]
            accuracy = int(m_stats["correct"] / total * 100) if total > 0 else 0
            
            card = tk.Frame(modules_grid, bg="white", relief=tk.GROOVE, bd=1)
            card.grid(row=i//3, column=i%3, padx=8, pady=5)
            
            tk.Label(card, text=name, font=("微软雅黑", 10, "bold"), bg="white", fg="#333").pack(pady=3, padx=15)
            tk.Label(card, text=f"答题: {total}  正确率: {accuracy}%", font=("微软雅黑", 9), 
                    bg="white", fg="#666").pack(pady=2)
            tk.Label(card, text=f"难度: {'⭐'*m_stats['level']}", font=("微软雅黑", 9), 
                    bg="white", fg="#FF9800").pack(pady=2)
    
    def create_time_control_tab(self, parent):
        """创建时间控制选项卡"""
        settings = self.learning_data.get_parent_settings()
        
        tk.Label(parent, text="⏰ 学习时间控制", font=("微软雅黑", 14, "bold"), 
                bg="#FAFAFA", fg="#333").pack(pady=15)
        
        # 每日时间限制
        daily_frame = tk.Frame(parent, bg="#E3F2FD", relief=tk.RAISED, bd=2)
        daily_frame.pack(fill=tk.X, padx=20, pady=8)
        
        tk.Label(daily_frame, text="📅 每日学习时间限制（分钟，0表示不限制）:", 
                font=("微软雅黑", 11), bg="#E3F2FD", fg="#333").pack(side=tk.LEFT, padx=15, pady=10)
        
        daily_var = tk.IntVar(value=settings.get("daily_time_limit", 60))
        daily_spin = tk.Spinbox(daily_frame, from_=0, to=180, increment=15, width=8,
                               textvariable=daily_var, font=("微软雅黑", 11))
        daily_spin.pack(side=tk.LEFT, padx=10)
        
        # 单次时间限制
        session_frame = tk.Frame(parent, bg="#FFF3E0", relief=tk.RAISED, bd=2)
        session_frame.pack(fill=tk.X, padx=20, pady=8)
        
        tk.Label(session_frame, text="⏱️ 单次学习时间限制（分钟，0表示不限制）:", 
                font=("微软雅黑", 11), bg="#FFF3E0", fg="#333").pack(side=tk.LEFT, padx=15, pady=10)
        
        session_var = tk.IntVar(value=settings.get("session_time_limit", 30))
        session_spin = tk.Spinbox(session_frame, from_=0, to=60, increment=5, width=8,
                                 textvariable=session_var, font=("微软雅黑", 11))
        session_spin.pack(side=tk.LEFT, padx=10)
        
        # 允许学习时间段
        hours_frame = tk.Frame(parent, bg="#E8F5E9", relief=tk.RAISED, bd=2)
        hours_frame.pack(fill=tk.X, padx=20, pady=8)
        
        tk.Label(hours_frame, text="🕐 允许学习时间段:", font=("微软雅黑", 11), 
                bg="#E8F5E9", fg="#333").pack(side=tk.LEFT, padx=15, pady=10)
        
        start_var = tk.IntVar(value=settings.get("allowed_hours_start", 8))
        tk.Spinbox(hours_frame, from_=0, to=23, width=4, textvariable=start_var, 
                  font=("微软雅黑", 11)).pack(side=tk.LEFT)
        tk.Label(hours_frame, text="点 到", font=("微软雅黑", 11), bg="#E8F5E9").pack(side=tk.LEFT, padx=5)
        
        end_var = tk.IntVar(value=settings.get("allowed_hours_end", 21))
        tk.Spinbox(hours_frame, from_=0, to=23, width=4, textvariable=end_var, 
                  font=("微软雅黑", 11)).pack(side=tk.LEFT)
        tk.Label(hours_frame, text="点", font=("微软雅黑", 11), bg="#E8F5E9").pack(side=tk.LEFT, padx=5)
        
        # 周末额外时间
        weekend_frame = tk.Frame(parent, bg="#F3E5F5", relief=tk.RAISED, bd=2)
        weekend_frame.pack(fill=tk.X, padx=20, pady=8)
        
        tk.Label(weekend_frame, text="🎉 周末额外学习时间（分钟）:", font=("微软雅黑", 11), 
                bg="#F3E5F5", fg="#333").pack(side=tk.LEFT, padx=15, pady=10)
        
        weekend_var = tk.IntVar(value=settings.get("weekend_extra_time", 15))
        tk.Spinbox(weekend_frame, from_=0, to=60, increment=5, width=8,
                  textvariable=weekend_var, font=("微软雅黑", 11)).pack(side=tk.LEFT, padx=10)
        
        # 保存按钮
        def save_time_settings():
            self.learning_data.update_parent_settings(
                daily_time_limit=daily_var.get(),
                session_time_limit=session_var.get(),
                allowed_hours_start=start_var.get(),
                allowed_hours_end=end_var.get(),
                weekend_extra_time=weekend_var.get()
            )
            messagebox.showinfo("成功", "时间控制设置已保存！")
        
        tk.Button(parent, text="💾 保存设置", font=("微软雅黑", 12), bg="#4CAF50", fg="white", 
                 relief=tk.RAISED, bd=3, cursor="hand2", padx=25, command=save_time_settings).pack(pady=20)
    
    def create_security_tab(self, parent):
        """创建安全设置选项卡"""
        settings = self.learning_data.get_parent_settings()
        
        tk.Label(parent, text="🔐 安全设置", font=("微软雅黑", 14, "bold"), 
                bg="#FAFAFA", fg="#333").pack(pady=15)
        
        # 密码设置
        pwd_frame = tk.Frame(parent, bg="#FFEBEE", relief=tk.RAISED, bd=2)
        pwd_frame.pack(fill=tk.X, padx=20, pady=10)
        
        tk.Label(pwd_frame, text="🔑 家长密码设置", font=("微软雅黑", 12, "bold"), 
                bg="#FFEBEE", fg="#C62828").pack(pady=8)
        
        pwd_input_frame = tk.Frame(pwd_frame, bg="#FFEBEE")
        pwd_input_frame.pack(pady=5)
        
        tk.Label(pwd_input_frame, text="新密码:", font=("微软雅黑", 10), bg="#FFEBEE").pack(side=tk.LEFT, padx=5)
        new_pwd = tk.Entry(pwd_input_frame, font=("微软雅黑", 11), show="*", width=15)
        new_pwd.pack(side=tk.LEFT, padx=5)
        
        tk.Label(pwd_input_frame, text="确认:", font=("微软雅黑", 10), bg="#FFEBEE").pack(side=tk.LEFT, padx=5)
        confirm_pwd = tk.Entry(pwd_input_frame, font=("微软雅黑", 11), show="*", width=15)
        confirm_pwd.pack(side=tk.LEFT, padx=5)
        
        def set_password():
            if new_pwd.get() != confirm_pwd.get():
                messagebox.showerror("错误", "两次输入的密码不一致！")
                return
            self.learning_data.set_parent_password(new_pwd.get())
            messagebox.showinfo("成功", "密码已设置！" if new_pwd.get() else "密码已清除！")
            new_pwd.delete(0, tk.END)
            confirm_pwd.delete(0, tk.END)
        
        tk.Button(pwd_frame, text="设置密码", font=("微软雅黑", 10), bg="#C62828", fg="white", 
                 relief=tk.RAISED, bd=2, padx=15, command=set_password).pack(pady=8)
        
        tk.Label(pwd_frame, text="💡 留空并点击设置可清除密码", font=("微软雅黑", 9), 
                bg="#FFEBEE", fg="#888").pack(pady=3)
        
        # 其他安全选项
        options_frame = tk.Frame(parent, bg="#E8F5E9", relief=tk.RAISED, bd=2)
        options_frame.pack(fill=tk.X, padx=20, pady=10)
        
        tk.Label(options_frame, text="⚙️ 其他选项", font=("微软雅黑", 12, "bold"), 
                bg="#E8F5E9", fg="#2E7D32").pack(pady=8)
        
        lock_var = tk.BooleanVar(value=settings.get("lock_after_limit", False))
        tk.Checkbutton(options_frame, text="达到时间限制后锁定程序", variable=lock_var,
                      font=("微软雅黑", 10), bg="#E8F5E9").pack(anchor=tk.W, padx=20, pady=3)
        
        diff_lock_var = tk.BooleanVar(value=settings.get("difficulty_lock", False))
        tk.Checkbutton(options_frame, text="锁定难度设置（防止孩子调整）", variable=diff_lock_var,
                      font=("微软雅黑", 10), bg="#E8F5E9").pack(anchor=tk.W, padx=20, pady=3)
        
        show_ans_var = tk.BooleanVar(value=settings.get("show_answers", True))
        tk.Checkbutton(options_frame, text="显示答案提示", variable=show_ans_var,
                      font=("微软雅黑", 10), bg="#E8F5E9").pack(anchor=tk.W, padx=20, pady=3)
        
        def save_security():
            self.learning_data.update_parent_settings(
                lock_after_limit=lock_var.get(),
                difficulty_lock=diff_lock_var.get(),
                show_answers=show_ans_var.get()
            )
            messagebox.showinfo("成功", "安全设置已保存！")
        
        tk.Button(options_frame, text="💾 保存", font=("微软雅黑", 10), bg="#4CAF50", fg="white", 
                 relief=tk.RAISED, bd=2, padx=20, command=save_security).pack(pady=10)
    
    def create_data_tab(self, parent):
        """创建数据管理选项卡"""
        tk.Label(parent, text="💾 数据管理", font=("微软雅黑", 14, "bold"), 
                bg="#FAFAFA", fg="#333").pack(pady=10)
        
        # 数据统计
        stats = self.learning_data.get_stats()
        review_stats = self.learning_data.get_review_stats()
        
        stats_frame = tk.Frame(parent, bg="#E3F2FD", relief=tk.RAISED, bd=2)
        stats_frame.pack(fill=tk.X, padx=20, pady=8)
        
        tk.Label(stats_frame, text="📊 数据统计", font=("微软雅黑", 12, "bold"), 
                bg="#E3F2FD", fg="#1565C0").pack(pady=5)
        
        stats_text = f"总答题数: {stats['total']}  |  星星: {stats['stars']}  |  徽章: {stats['badges']}\n"
        stats_text += f"复习项目: {review_stats['total']}  |  已掌握: {review_stats['mastered']}"
        tk.Label(stats_frame, text=stats_text, font=("微软雅黑", 10), 
                bg="#E3F2FD", fg="#333").pack(pady=5)
        
        # 字库管理
        word_frame = tk.Frame(parent, bg="#E8F5E9", relief=tk.RAISED, bd=2)
        word_frame.pack(fill=tk.X, padx=20, pady=8)
        
        tk.Label(word_frame, text="📚 字库管理", font=("微软雅黑", 12, "bold"), 
                bg="#E8F5E9", fg="#2E7D32").pack(pady=5)
        
        # 显示当前字库数量
        try:
            from word_database import get_characters_by_level
            word_count = len(get_characters_by_level(3))
            tk.Label(word_frame, text=f"当前字库: {word_count} 个汉字", 
                    font=("微软雅黑", 10), bg="#E8F5E9", fg="#333").pack(pady=3)
        except:
            tk.Label(word_frame, text="字库模块未加载", 
                    font=("微软雅黑", 10), bg="#E8F5E9", fg="#888").pack(pady=3)
        
        word_btn_frame = tk.Frame(word_frame, bg="#E8F5E9")
        word_btn_frame.pack(pady=8)
        
        tk.Button(word_btn_frame, text="➕ 添加新字", font=("微软雅黑", 10), bg="#4CAF50", fg="white", 
                 relief=tk.RAISED, bd=2, padx=12, command=self.show_add_words_dialog).pack(side=tk.LEFT, padx=5)
        tk.Button(word_btn_frame, text="📖 查看字库", font=("微软雅黑", 10), bg="#2196F3", fg="white", 
                 relief=tk.RAISED, bd=2, padx=12, command=self.show_word_library).pack(side=tk.LEFT, padx=5)
        
        # 重置选项
        reset_frame = tk.Frame(parent, bg="#FFEBEE", relief=tk.RAISED, bd=2)
        reset_frame.pack(fill=tk.X, padx=20, pady=8)
        
        tk.Label(reset_frame, text="⚠️ 重置数据（谨慎操作）", font=("微软雅黑", 12, "bold"), 
                bg="#FFEBEE", fg="#C62828").pack(pady=5)
        
        btn_frame = tk.Frame(reset_frame, bg="#FFEBEE")
        btn_frame.pack(pady=8)
        
        modules = [("识字", "literacy"), ("拼音", "pinyin"), ("数学", "math"), 
                  ("英语", "english"), ("思维", "thinking"), ("交通", "vehicles")]
        
        for name, key in modules:
            tk.Button(btn_frame, text=f"重置{name}", font=("微软雅黑", 9), bg="#FF9800", fg="white", 
                     relief=tk.RAISED, bd=2, padx=8,
                     command=lambda k=key, n=name: self.confirm_reset(k, n)).pack(side=tk.LEFT, padx=3)
        
        tk.Button(reset_frame, text="🗑️ 重置所有数据", font=("微软雅黑", 10), bg="#F44336", fg="white", 
                 relief=tk.RAISED, bd=3, padx=15, command=lambda: self.confirm_reset(None, "所有")).pack(pady=8)
        
        tk.Label(reset_frame, text="⚠️ 重置后数据无法恢复，请谨慎操作！", font=("微软雅黑", 9), 
                bg="#FFEBEE", fg="#C62828").pack(pady=3)
    
    def show_add_words_dialog(self):
        """显示添加新字对话框"""
        add_win = tk.Toplevel(self.window)
        add_win.title("➕ 添加新汉字")
        add_win.geometry("500x450")
        add_win.configure(bg="#E8F5E9")
        add_win.transient(self.window)
        add_win.grab_set()
        
        x = (add_win.winfo_screenwidth() - 500) // 2
        y = (add_win.winfo_screenheight() - 450) // 2
        add_win.geometry(f"+{x}+{y}")
        
        tk.Label(add_win, text="➕ 添加新汉字到字库", font=("微软雅黑", 18, "bold"), 
                bg="#E8F5E9", fg="#2E7D32").pack(pady=15)
        
        tk.Label(add_win, text="输入要添加的汉字（可以一次输入多个）:", 
                font=("微软雅黑", 11), bg="#E8F5E9", fg="#333").pack(pady=5)
        
        # 输入框
        input_frame = tk.Frame(add_win, bg="#E8F5E9")
        input_frame.pack(pady=10)
        
        char_entry = tk.Entry(input_frame, font=("楷体", 24), width=20)
        char_entry.pack(pady=5)
        char_entry.focus()
        
        tk.Label(add_win, text="例如: 花草鸟鱼 或 春夏秋冬", 
                font=("微软雅黑", 10), bg="#E8F5E9", fg="#888").pack()
        
        # 结果显示区
        result_frame = tk.Frame(add_win, bg="white", relief=tk.SUNKEN, bd=2)
        result_frame.pack(fill=tk.BOTH, expand=True, padx=20, pady=10)
        
        result_text = tk.Text(result_frame, font=("微软雅黑", 10), height=10, wrap=tk.WORD)
        result_text.pack(fill=tk.BOTH, expand=True, padx=5, pady=5)
        result_text.config(state=tk.DISABLED)
        
        def add_words():
            chars = char_entry.get().strip()
            if not chars:
                messagebox.showwarning("提示", "请输入要添加的汉字！")
                return
            
            result_text.config(state=tk.NORMAL)
            result_text.delete(1.0, tk.END)
            
            try:
                # 导入添加工具
                from add_words import add_words_to_database, get_pinyin, get_emoji
                from word_database import get_characters_by_level
                
                # 获取现有字符
                existing = set(c[0] for c in get_characters_by_level(3))
                
                added = []
                skipped = []
                
                for char in chars:
                    if not ('\u4e00' <= char <= '\u9fff'):
                        continue
                    if char in existing:
                        skipped.append(char)
                    else:
                        py = get_pinyin(char)
                        emoji = get_emoji(char)
                        added.append(f"{char} ({py}) {emoji}")
                
                if added:
                    # 执行添加
                    add_words_to_database(chars)
                    result_text.insert(tk.END, f"✅ 成功添加 {len(added)} 个新字:\n")
                    for item in added:
                        result_text.insert(tk.END, f"  • {item}\n")
                else:
                    result_text.insert(tk.END, "没有新字需要添加\n")
                
                if skipped:
                    result_text.insert(tk.END, f"\n⏭️ 跳过 {len(skipped)} 个已存在的字:\n")
                    result_text.insert(tk.END, f"  {' '.join(skipped)}\n")
                
                result_text.insert(tk.END, "\n💡 提示: 重新打开识字乐园即可使用新字")
                
            except ImportError as e:
                result_text.insert(tk.END, f"❌ 错误: 缺少必要模块\n{str(e)}")
            except Exception as e:
                result_text.insert(tk.END, f"❌ 添加失败: {str(e)}")
            
            result_text.config(state=tk.DISABLED)
            char_entry.delete(0, tk.END)
        
        # 按钮
        btn_frame = tk.Frame(add_win, bg="#E8F5E9")
        btn_frame.pack(pady=10)
        
        tk.Button(btn_frame, text="➕ 添加", font=("微软雅黑", 12), bg="#4CAF50", fg="white", 
                 relief=tk.RAISED, bd=3, padx=25, command=add_words).pack(side=tk.LEFT, padx=10)
        tk.Button(btn_frame, text="关闭", font=("微软雅黑", 12), bg="#9E9E9E", fg="white", 
                 relief=tk.RAISED, bd=3, padx=25, command=add_win.destroy).pack(side=tk.LEFT, padx=10)
    
    def show_word_library(self):
        """显示字库内容"""
        lib_win = tk.Toplevel(self.window)
        lib_win.title("📖 字库内容")
        lib_win.geometry("700x550")
        lib_win.configure(bg="#FFF8E1")
        lib_win.transient(self.window)
        lib_win.grab_set()
        
        x = (lib_win.winfo_screenwidth() - 700) // 2
        y = (lib_win.winfo_screenheight() - 550) // 2
        lib_win.geometry(f"+{x}+{y}")
        
        tk.Label(lib_win, text="📖 字库内容", font=("微软雅黑", 18, "bold"), 
                bg="#FFF8E1", fg="#FF6B6B").pack(pady=10)
        
        try:
            from word_database import CHARACTERS_LEVEL_1, CHARACTERS_LEVEL_2, CHARACTERS_LEVEL_3
            
            # 创建滚动区域
            canvas = tk.Canvas(lib_win, bg="#FFF8E1", highlightthickness=0)
            scrollbar = tk.Scrollbar(lib_win, orient="vertical", command=canvas.yview)
            scrollable_frame = tk.Frame(canvas, bg="#FFF8E1")
            
            scrollable_frame.bind("<Configure>", lambda e: canvas.configure(scrollregion=canvas.bbox("all")))
            canvas.create_window((0, 0), window=scrollable_frame, anchor="nw")
            canvas.configure(yscrollcommand=scrollbar.set)
            
            levels = [
                ("⭐ 等级1 - 基础字", CHARACTERS_LEVEL_1, "#FF6B6B"),
                ("⭐⭐ 等级2 - 进阶字", CHARACTERS_LEVEL_2, "#4ECDC4"),
                ("⭐⭐⭐ 等级3 - 挑战字", CHARACTERS_LEVEL_3, "#9C27B0"),
            ]
            
            for level_name, chars, color in levels:
                # 等级标题
                level_frame = tk.Frame(scrollable_frame, bg=color)
                level_frame.pack(fill=tk.X, padx=10, pady=8)
                tk.Label(level_frame, text=f"{level_name} ({len(chars)}字)", 
                        font=("微软雅黑", 12, "bold"), bg=color, fg="white").pack(pady=5)
                
                # 汉字网格
                chars_frame = tk.Frame(scrollable_frame, bg="#FFF8E1")
                chars_frame.pack(fill=tk.X, padx=20, pady=5)
                
                for i, char_data in enumerate(chars):
                    char, py, emoji = char_data[0], char_data[1], char_data[2]
                    
                    card = tk.Frame(chars_frame, bg="white", relief=tk.RAISED, bd=1)
                    card.grid(row=i//8, column=i%8, padx=4, pady=4)
                    
                    tk.Label(card, text=char, font=("楷体", 20, "bold"), 
                            bg="white", fg="#333").pack(padx=8, pady=2)
                    tk.Label(card, text=f"{emoji}", font=("Segoe UI Emoji", 12), 
                            bg="white").pack()
                    tk.Label(card, text=py, font=("Arial", 8), 
                            bg="white", fg="#888").pack(pady=2)
            
            canvas.pack(side="left", fill="both", expand=True, padx=10, pady=5)
            scrollbar.pack(side="right", fill="y")
            
            # 绑定鼠标滚轮
            def on_mousewheel(event):
                canvas.yview_scroll(int(-1*(event.delta/120)), "units")
            canvas.bind_all("<MouseWheel>", on_mousewheel)
            
            total = len(CHARACTERS_LEVEL_1) + len(CHARACTERS_LEVEL_2) + len(CHARACTERS_LEVEL_3)
            tk.Label(lib_win, text=f"共 {total} 个汉字", font=("微软雅黑", 11), 
                    bg="#FFF8E1", fg="#666").pack(pady=5)
            
        except ImportError:
            tk.Label(lib_win, text="❌ 无法加载字库模块", font=("微软雅黑", 14), 
                    bg="#FFF8E1", fg="#F44336").pack(pady=50)
        
        tk.Button(lib_win, text="关闭", font=("微软雅黑", 12), bg="#FF6B6B", fg="white", 
                 relief=tk.RAISED, bd=3, padx=30, command=lib_win.destroy).pack(pady=10)
    
    def confirm_reset(self, module, name):
        """确认重置数据"""
        if messagebox.askyesno("确认重置", f"确定要重置{name}数据吗？\n此操作无法撤销！"):
            self.learning_data.reset_progress(module)
            messagebox.showinfo("完成", f"{name}数据已重置！")
    
    def show_daily_challenges(self):
        """显示每日挑战界面"""
        if not self.learning_data:
            messagebox.showinfo("提示", "学习数据模块未加载")
            return
        
        challenge_win = tk.Toplevel(self.window)
        challenge_win.title("🎯 每日挑战")
        challenge_win.geometry("550x550")
        challenge_win.configure(bg="#FFEBEE")
        challenge_win.transient(self.window)
        challenge_win.grab_set()
        
        x = (challenge_win.winfo_screenwidth() - 550) // 2
        y = (challenge_win.winfo_screenheight() - 550) // 2
        challenge_win.geometry(f"+{x}+{y}")
        
        tk.Label(challenge_win, text="🎯 每日挑战", font=("微软雅黑", 24, "bold"), 
                bg="#FFEBEE", fg="#C62828").pack(pady=15)
        
        # 获取挑战数据
        challenges = self.learning_data.get_daily_challenges()
        stats = self.learning_data.get_challenge_stats()
        
        # 统计卡片
        stats_frame = tk.Frame(challenge_win, bg="#FFCDD2", relief=tk.RAISED, bd=3)
        stats_frame.pack(fill=tk.X, padx=30, pady=10)
        
        tk.Label(stats_frame, text="🏆 挑战统计", font=("微软雅黑", 12, "bold"), 
                bg="#FFCDD2", fg="#C62828").pack(pady=8)
        
        stats_text = f"🔥 连续完成: {stats['streak']} 天  |  "
        stats_text += f"📊 累计完成: {stats['total_completed']} 个  |  "
        stats_text += f"✅ 今日: {stats['today_completed']}/{stats['today_total']}"
        tk.Label(stats_frame, text=stats_text, font=("微软雅黑", 11), 
                bg="#FFCDD2", fg="#333").pack(pady=5)
        
        # 今日挑战列表
        tk.Label(challenge_win, text="📋 今日挑战任务", font=("微软雅黑", 14, "bold"), 
                bg="#FFEBEE", fg="#C62828").pack(pady=10)
        
        for challenge in challenges:
            c_frame = tk.Frame(challenge_win, bg="white", relief=tk.RAISED, bd=2)
            c_frame.pack(fill=tk.X, padx=30, pady=8)
            
            # 左侧emoji和名称
            left_frame = tk.Frame(c_frame, bg="white")
            left_frame.pack(side=tk.LEFT, padx=15, pady=10)
            
            emoji = challenge.get("emoji", "🎯")
            tk.Label(left_frame, text=emoji, font=("Segoe UI Emoji", 28), bg="white").pack(side=tk.LEFT)
            
            info_frame = tk.Frame(left_frame, bg="white")
            info_frame.pack(side=tk.LEFT, padx=10)
            
            tk.Label(info_frame, text=challenge["name"], font=("微软雅黑", 12, "bold"), 
                    bg="white", fg="#333").pack(anchor=tk.W)
            tk.Label(info_frame, text=challenge["desc"], font=("微软雅黑", 10), 
                    bg="white", fg="#666").pack(anchor=tk.W)
            
            # 右侧进度和奖励
            right_frame = tk.Frame(c_frame, bg="white")
            right_frame.pack(side=tk.RIGHT, padx=15, pady=10)
            
            if challenge["completed"]:
                tk.Label(right_frame, text="✅ 已完成", font=("微软雅黑", 11, "bold"), 
                        bg="white", fg="#4CAF50").pack()
            else:
                progress = challenge["progress"]
                target = challenge["target"]
                progress_text = f"{progress}/{target}"
                
                # 进度条
                bar_frame = tk.Frame(right_frame, bg="#E0E0E0", width=80, height=12, relief=tk.SUNKEN, bd=1)
                bar_frame.pack()
                bar_frame.pack_propagate(False)
                
                fill_width = int(80 * min(progress, target) / target) if target > 0 else 0
                if fill_width > 0:
                    fill = tk.Frame(bar_frame, bg="#F44336", width=fill_width, height=12)
                    fill.pack(side=tk.LEFT)
                
                tk.Label(right_frame, text=progress_text, font=("微软雅黑", 9), 
                        bg="white", fg="#666").pack()
            
            # 奖励星星
            reward = challenge.get("reward_stars", 1)
            tk.Label(right_frame, text=f"⭐×{reward}", font=("微软雅黑", 10), 
                    bg="white", fg="#FF9800").pack()
        
        # 提示
        tip_frame = tk.Frame(challenge_win, bg="#FFCDD2", relief=tk.GROOVE, bd=2)
        tip_frame.pack(fill=tk.X, padx=30, pady=15)
        tk.Label(tip_frame, text="💡 完成挑战可获得额外星星奖励！每天都有新挑战哦！", 
                font=("微软雅黑", 10), bg="#FFCDD2", fg="#C62828", pady=8).pack()
        
        # 刷新按钮
        btn_frame = tk.Frame(challenge_win, bg="#FFEBEE")
        btn_frame.pack(pady=10)
        
        def refresh_challenges():
            # 检查挑战完成状态
            newly_completed = self.learning_data.check_challenge_completion()
            if newly_completed:
                for c in newly_completed:
                    self.speak(f"太棒了！完成了{c['name']}挑战！")
                    messagebox.showinfo("🎉 挑战完成！", 
                        f"恭喜完成挑战：{c['name']}\n获得 {c.get('reward_stars', 1)} 颗星星！")
            challenge_win.destroy()
            self.show_daily_challenges()
        
        tk.Button(btn_frame, text="🔄 刷新进度", font=("微软雅黑", 11), bg="#2196F3", fg="white", 
                 relief=tk.RAISED, bd=3, cursor="hand2", padx=15, command=refresh_challenges).pack(side=tk.LEFT, padx=10)
        tk.Button(btn_frame, text="关闭", font=("微软雅黑", 11), bg="#9E9E9E", fg="white", 
                 relief=tk.RAISED, bd=3, cursor="hand2", padx=15, command=challenge_win.destroy).pack(side=tk.LEFT, padx=10)
        
        # 语音提示
        completed_count = stats['today_completed']
        total_count = stats['today_total']
        if completed_count == total_count and total_count > 0:
            self.speak("太棒了！今天的挑战全部完成了！")
        elif completed_count > 0:
            self.speak(f"已经完成{completed_count}个挑战了，继续加油！")
        else:
            self.speak("今天有新的挑战任务，快来完成吧！")
    
    def run(self):
        self.window.mainloop()


if __name__ == "__main__":
    app = KidsLearningMain()
    app.run()

