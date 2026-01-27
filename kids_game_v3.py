# -*- coding: utf-8 -*-
"""
宝宝识字乐园 v3.4
使用 edge-tts 微软童声
集成学习数据追踪、难度分级
改进：退出确认、休息提醒、定时器清理
新增：进度可视化、自适应难度、故事模式、动画效果、音效系统
优化：UI配置模块，为平板适配做准备
"""

import tkinter as tk
from tkinter import ttk, messagebox, filedialog, simpledialog
import random
import threading
import asyncio
import os
import tempfile
import uuid
import time
import atexit
import json

# 导入UI配置模块
try:
    from ui_config import (
        UI, Colors, ScreenConfig, get_font, get_font_tuple, get_path, 
        get_data_path, IS_MOBILE, PLATFORM
    )
    UI_CONFIG_AVAILABLE = True
except ImportError:
    UI_CONFIG_AVAILABLE = False
    IS_MOBILE = False
    PLATFORM = "windows"

try:
    import edge_tts
    import pygame
    pygame.mixer.init()
    TTS_AVAILABLE = True
except ImportError:
    TTS_AVAILABLE = False

try:
    from pypinyin import pinyin, Style
    PINYIN_AVAILABLE = True
except ImportError:
    PINYIN_AVAILABLE = False

# 导入学习数据和字库
try:
    from voice_config_shared import (
        record_answer, get_module_level, get_wrong_questions, get_stars, add_to_review,
        create_rest_reminder, get_learning_data
    )
    LEARNING_DATA_AVAILABLE = True
except ImportError:
    LEARNING_DATA_AVAILABLE = False
    get_learning_data = lambda: None

try:
    from word_database import get_characters_by_level, CHAR_EMOJI_MAP, STROKE_DATA, get_stroke_data
    WORD_DB_AVAILABLE = True
except ImportError:
    WORD_DB_AVAILABLE = False
    CHAR_EMOJI_MAP = {}
    STROKE_DATA = {}
    get_stroke_data = lambda x: None

# 导入主题系统
try:
    from theme_config import get_theme, ThemeHelper, get_random_character
    from theme_drawings import ThemeDrawings
    THEME_AVAILABLE = True
    theme = ThemeHelper()
except ImportError:
    THEME_AVAILABLE = False
    theme = None

# =====================================================
# 笔顺数据 - 优先使用word_database的数据
# =====================================================
# 如果word_database没有导入成功，使用本地备份
if not WORD_DB_AVAILABLE or not STROKE_DATA:
    STROKE_DATA = {
        # 基础字备份
        "一": [[(20, 100), (180, 100)]],
        "三": [[(40, 50), (160, 50)], [(30, 100), (170, 100)], [(20, 150), (180, 150)]],
        "日": [[(50, 30), (50, 170)], [(50, 30), (150, 30)], [(150, 30), (150, 170)], [(50, 100), (150, 100)], [(50, 170), (150, 170)]],
        "天": [[(30, 50), (170, 50)], [(100, 50), (100, 90)], [(40, 90), (160, 90)], [(100, 90), (40, 170)], [(100, 90), (160, 170)]],
        "火": [[(70, 60), (50, 100)], [(130, 60), (150, 100)], [(100, 50), (60, 170)], [(100, 50), (140, 170)]],
        "水": [[(100, 30), (100, 170)], [(100, 60), (50, 40)], [(100, 60), (150, 40)], [(100, 110), (40, 170)], [(100, 110), (160, 170)]],
        "木": [[(100, 30), (100, 170)], [(30, 90), (170, 90)], [(100, 90), (40, 170)], [(100, 90), (160, 170)]],
        "土": [[(100, 40), (100, 130)], [(40, 90), (160, 90)], [(30, 160), (170, 160)]],
        "心": [[(50, 100), (60, 80)], [(90, 70), (100, 90)], [(100, 90), (140, 130), (160, 100)], [(150, 70), (160, 90)]],
        "白": [[(60, 30), (100, 50)], [(50, 50), (50, 170)], [(50, 50), (150, 50)], [(150, 50), (150, 170)], [(50, 110), (150, 110)], [(50, 170), (150, 170)]],
        "牛": [[(60, 40), (100, 70)], [(30, 70), (170, 70)], [(100, 40), (100, 170)], [(40, 120), (160, 120)]],
        "羊": [[(60, 40), (100, 60)], [(140, 40), (100, 60)], [(40, 80), (160, 80)], [(50, 120), (150, 120)], [(100, 60), (100, 170)]],
    }

# 如果没有从word_database导入，使用本地备份
if not WORD_DB_AVAILABLE or not CHAR_EMOJI_MAP:
    CHAR_EMOJI_MAP = {
        "日": "☀️", "天": "🌤️", "月": "🌙", "风": "💨",
        "爸": "👨", "妈": "👩", "宝": "👶", "姐": "👧",
        "开": "🔓", "关": "🔒", "地": "🌍", "里": "🏠",
        "他": "👤", "工": "🔧", "儿": "👦", "老": "👴",
        "好": "👍", "饭": "🍚", "看": "👀", "玩": "🎮",
        "叔": "👨", "自": "🙋", "姑": "👩", "娘": "👩",
        "火": "🔥", "土": "🟤", "水": "💧", "电": "⚡",
        "木": "🪵", "比": "⚖️", "图": "🖼️", "树": "🌳",
        "一": "1️⃣", "三": "3️⃣", "四": "4️⃣", "五": "5️⃣",
        "两": "✌️", "可": "👌", "心": "❤️", "说": "💬",
        "白": "⬜", "羊": "🐑", "牛": "🐄", "鼠": "🐭",
    }

# 常用组词库 - 从word_database获取或使用备份
def get_char_words(char):
    """获取汉字组词"""
    # 尝试从字库获取
    if WORD_DB_AVAILABLE:
        try:
            for level in [1, 2, 3]:
                chars = get_characters_by_level(level)
                for c in chars:
                    if c[0] == char:
                        return c[3]  # 返回组词列表
        except:
            pass
    # 备份数据
    backup = {
        "日": ["太阳", "日出", "日子"], "天": ["天空", "今天", "天气"], 
        "月": ["月亮", "月光", "月饼"], "风": ["大风", "风车", "春风"],
        "爸": ["爸爸", "爸妈", "老爸"], "妈": ["妈妈", "爸妈", "妈咪"],
        "宝": ["宝宝", "宝贝", "珍宝"], "姐": ["姐姐", "姐妹", "大姐"],
        "开": ["开门", "开心", "打开"], "关": ["关门", "关灯", "关心"],
        "地": ["地上", "土地", "地方"], "里": ["里面", "家里", "心里"],
        "他": ["他们", "其他", "他人"], "工": ["工人", "工作", "手工"],
        "儿": ["儿子", "儿童", "女儿"], "老": ["老师", "老人", "老虎"],
        "好": ["好人", "你好", "好看"], "饭": ["吃饭", "米饭", "饭菜"],
        "看": ["看书", "看见", "好看"], "玩": ["玩具", "玩耍", "好玩"],
        "叔": ["叔叔", "大叔", "叔父"], "自": ["自己", "自然", "自由"],
        "姑": ["姑姑", "姑娘", "姑妈"], "娘": ["姑娘", "娘亲", "新娘"],
        "火": ["火车", "大火", "火焰"], "土": ["泥土", "土地", "尘土"],
        "水": ["喝水", "水果", "河水"], "电": ["电视", "电话", "闪电"],
        "木": ["木头", "树木", "木材"], "比": ["比赛", "对比", "比较"],
        "图": ["图片", "图画", "地图"], "树": ["大树", "树木", "树叶"],
        "一": ["一个", "第一", "一起"], "三": ["三个", "第三", "三只"],
        "四": ["四个", "四方", "四季"], "五": ["五个", "五颜六色", "五星"],
        "两": ["两个", "两边", "两只"], "可": ["可以", "可爱", "可是"],
        "心": ["心里", "开心", "爱心"], "说": ["说话", "说明", "听说"],
        "白": ["白色", "白云", "白天"], "羊": ["小羊", "山羊", "羊毛"],
        "牛": ["小牛", "牛奶", "水牛"], "鼠": ["老鼠", "松鼠", "鼠标"],
    }
    return backup.get(char, [char + "字", "写" + char])

def get_char_sentence(char):
    """获取汉字造句"""
    # 尝试从字库获取
    if WORD_DB_AVAILABLE:
        try:
            for level in [1, 2, 3]:
                chars = get_characters_by_level(level)
                for c in chars:
                    if c[0] == char:
                        return c[4]  # 返回造句
        except:
            pass
    # 备份数据
    backup = {
        "日": "太阳公公出来了。", "天": "今天天气真好。",
        "月": "月亮弯弯像小船。", "风": "大风吹呀吹。",
        "爸": "爸爸最爱乐乐了。", "妈": "妈妈做的饭真香。",
        "宝": "乐乐是妈妈的宝贝。", "姐": "姐姐带乐乐玩。",
        "开": "乐乐开心地笑。", "关": "睡觉要关灯。",
        "地": "地上有一朵小花。", "里": "家里真温暖。",
        "他": "他是我的好朋友。", "工": "工人叔叔在盖房子。",
        "儿": "乐乐是个好儿子。", "老": "老师教我们学知识。",
        "好": "乐乐是好孩子。", "饭": "乐乐吃饭香香的。",
        "看": "乐乐看书真认真。", "玩": "乐乐爱玩玩具。",
        "叔": "叔叔给乐乐买玩具。", "自": "乐乐自己穿衣服。",
        "姑": "姑姑来看乐乐了。", "娘": "姑娘穿着漂亮的裙子。",
        "火": "火车跑得真快。", "土": "泥土里长出小草。",
        "水": "多喝水身体好。", "电": "闪电一闪一闪的。",
        "木": "木头可以做家具。", "比": "我们来比一比谁跑得快。",
        "图": "乐乐画了一幅图画。", "树": "大树下面好乘凉。",
        "一": "乐乐是第一名。", "三": "三只小猪盖房子。",
        "四": "一年有四季。", "五": "五颗星星亮晶晶。",
        "两": "乐乐有两只小手。", "可": "乐乐真可爱。",
        "心": "乐乐心里很开心。", "说": "乐乐说话真好听。",
        "白": "白云飘在蓝天上。", "羊": "小羊在草地上吃草。",
        "牛": "小牛爱喝牛奶。", "鼠": "小老鼠吱吱叫。",
    }
    words = get_char_words(char)
    return backup.get(char, f"乐乐学会了{words[0]}。")


class KidsLiteracyGame:
    def __init__(self):
        self.window = tk.Tk()
        self.window.title("🎈 乐乐的识字小课堂 🎈")
        
        # 使用UI配置设置窗口大小
        if UI_CONFIG_AVAILABLE:
            w, h = ScreenConfig.get_window_size()
            if w and h:
                window_width, window_height = w, h
            else:
                # 移动端全屏
                window_width = self.window.winfo_screenwidth()
                window_height = self.window.winfo_screenheight()
        else:
            window_width = 1050
            window_height = 800
        
        screen_width = self.window.winfo_screenwidth()
        screen_height = self.window.winfo_screenheight()
        x = (screen_width - window_width) // 2
        y = (screen_height - window_height) // 2 - 30
        self.window.geometry(f"{window_width}x{window_height}+{x}+{y}")
        
        # 保存窗口尺寸供后续使用
        self.window_width = window_width
        self.window_height = window_height
        
        # =====================================================
        # 汉字掌握度追踪系统
        # =====================================================
        # 掌握度等级: 0=生疏(红), 1=学习中(橙), 2=熟悉(黄), 3=掌握(绿)
        self.char_mastery = {}  # {字: {"level": 0-3, "correct": 0, "wrong": 0, "last_seen": ""}}
        self.load_mastery_data()
        
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
        
        # 定时器管理
        self.pending_timers = []
        
        # 休息提醒
        if LEARNING_DATA_AVAILABLE:
            self.rest_reminder = create_rest_reminder(self.window, 15)
            if self.rest_reminder:
                self.rest_reminder.start()
        
        # 设置窗口关闭处理
        self.window.protocol("WM_DELETE_WINDOW", self.on_close_window)
        atexit.register(self.cleanup_on_exit)
        
        self.tts_lock = threading.Lock()
        try:
            from voice_config_shared import get_voice, get_praises, get_encourages
            self.voice = get_voice()
            self.praises = get_praises()
            self.encourages = get_encourages()
        except ImportError:
            self.voice = "zh-CN-YunxiNeural"
            self.praises = ["太棒了！", "真厉害！", "答对啦！"]
            self.encourages = ["加油！", "再试一次！", "没关系！"]
        self.temp_dir = tempfile.gettempdir()
        
        self.audio_dir = os.path.join(os.path.dirname(os.path.abspath(__file__)), "audio")
        self.praise_audios = self._scan_audio_folder("praise")
        self.encourage_audios = self._scan_audio_folder("encourage")
        
        # 初始化音效系统
        self.init_sound_system()
        
        # 获取难度等级和对应字库
        self.level = get_module_level("literacy") if LEARNING_DATA_AVAILABLE else 1
        self.load_words_by_level()
        
        self.score = 0
        self.current_mode = None
        self.game_frame = None
        self.speech_id = 0
        self.praise_playing = False
        self.custom_words = []  # 自定义字库
        
        self.create_main_menu()
    
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
    
    def on_close_window(self):
        """窗口关闭处理"""
        result = messagebox.askyesno(
            "👋 确认退出",
            "确定要退出识字乐园吗？",
            icon='question',
            default='yes'
        )
        if result:
            self.cleanup_on_exit()
            self.window.quit()
    
    def cleanup_on_exit(self):
        """退出时清理"""
        try:
            # 保存掌握度数据
            self.save_mastery_data()
            
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
    
    # =====================================================
    # 掌握度数据管理
    # =====================================================
    def load_mastery_data(self):
        """加载汉字掌握度数据"""
        try:
            if UI_CONFIG_AVAILABLE:
                mastery_file = get_data_path("char_mastery.json")
            else:
                mastery_file = os.path.join(os.path.dirname(os.path.abspath(__file__)), "char_mastery.json")
            if os.path.exists(mastery_file):
                with open(mastery_file, 'r', encoding='utf-8') as f:
                    self.char_mastery = json.load(f)
        except Exception as e:
            print(f"加载掌握度数据失败: {e}")
            self.char_mastery = {}
    
    def save_mastery_data(self):
        """保存汉字掌握度数据"""
        try:
            if UI_CONFIG_AVAILABLE:
                mastery_file = get_data_path("char_mastery.json")
            else:
                mastery_file = os.path.join(os.path.dirname(os.path.abspath(__file__)), "char_mastery.json")
            with open(mastery_file, 'w', encoding='utf-8') as f:
                json.dump(self.char_mastery, f, ensure_ascii=False, indent=2)
        except Exception as e:
            print(f"保存掌握度数据失败: {e}")
    
    def update_char_mastery(self, char, is_correct):
        """更新汉字掌握度
        
        掌握度计算规则：
        - 答对+1分，答错-1分
        - 0-2分: 生疏(level 0)
        - 3-5分: 学习中(level 1)  
        - 6-8分: 熟悉(level 2)
        - 9+分: 掌握(level 3)
        """
        from datetime import date
        today = date.today().isoformat()
        
        if char not in self.char_mastery:
            self.char_mastery[char] = {
                "level": 0,
                "score": 0,
                "correct": 0,
                "wrong": 0,
                "last_seen": today,
                "first_seen": today
            }
        
        data = self.char_mastery[char]
        data["last_seen"] = today
        
        if is_correct:
            data["correct"] += 1
            data["score"] = min(12, data["score"] + 1)  # 最高12分
        else:
            data["wrong"] += 1
            data["score"] = max(0, data["score"] - 1)  # 最低0分
        
        # 计算掌握度等级
        score = data["score"]
        if score >= 9:
            data["level"] = 3  # 掌握
        elif score >= 6:
            data["level"] = 2  # 熟悉
        elif score >= 3:
            data["level"] = 1  # 学习中
        else:
            data["level"] = 0  # 生疏
        
        # 定期保存
        if (data["correct"] + data["wrong"]) % 5 == 0:
            self.save_mastery_data()
    
    def get_mastery_stats(self):
        """获取掌握度统计"""
        total = len(self.words)
        stats = {
            "total": total,
            "mastered": 0,      # 掌握 (level 3)
            "familiar": 0,      # 熟悉 (level 2)
            "learning": 0,      # 学习中 (level 1)
            "new": 0,           # 生疏/未学 (level 0)
            "total_correct": 0,
            "total_wrong": 0
        }
        
        learned_chars = set()
        for char, data in self.char_mastery.items():
            learned_chars.add(char)
            if data["level"] == 3:
                stats["mastered"] += 1
            elif data["level"] == 2:
                stats["familiar"] += 1
            elif data["level"] == 1:
                stats["learning"] += 1
            else:
                stats["new"] += 1
            stats["total_correct"] += data.get("correct", 0)
            stats["total_wrong"] += data.get("wrong", 0)
        
        # 计算未学习的字
        for w in self.words:
            if w[0] not in learned_chars:
                stats["new"] += 1
        
        return stats
    
    def get_char_mastery_level(self, char):
        """获取单个汉字的掌握度等级"""
        if char in self.char_mastery:
            return self.char_mastery[char]["level"]
        return 0  # 未学习
    
    def get_mastery_color(self, level):
        """获取掌握度对应的颜色"""
        colors = {
            0: "#FF6B6B",  # 生疏 - 红色
            1: "#FF9800",  # 学习中 - 橙色
            2: "#FFD700",  # 熟悉 - 黄色
            3: "#4CAF50"   # 掌握 - 绿色
        }
        return colors.get(level, "#E0E0E0")
    
    def get_mastery_text(self, level):
        """获取掌握度对应的文字"""
        texts = {
            0: "生疏",
            1: "学习中",
            2: "熟悉",
            3: "掌握"
        }
        return texts.get(level, "未学")
    
    # =====================================================
    # 动画效果系统
    # =====================================================
    def create_celebration_canvas(self, parent, width=200, height=150):
        """创建庆祝动画画布"""
        canvas = tk.Canvas(parent, width=width, height=height, bg=parent.cget("bg"), 
                          highlightthickness=0)
        return canvas
    
    def play_star_animation(self, canvas, duration=2000):
        """播放星星飞舞动画"""
        canvas.delete("celebration")
        
        stars = []
        colors = ["#FFD700", "#FFA500", "#FF6B6B", "#4ECDC4", "#9C27B0"]
        
        # 创建多个星星
        for _ in range(12):
            x = random.randint(20, int(canvas.cget("width")) - 20)
            y = int(canvas.cget("height")) + 10
            color = random.choice(colors)
            size = random.randint(8, 16)
            speed = random.uniform(2, 5)
            
            # 绘制星星
            star_id = self.draw_star_shape(canvas, x, y, size, color)
            stars.append({"id": star_id, "x": x, "y": y, "speed": speed, "wobble": random.uniform(-2, 2)})
        
        # 动画更新
        def animate_stars(frame=0):
            if frame > duration // 50:
                canvas.delete("celebration")
                return
            
            for star in stars:
                star["y"] -= star["speed"]
                star["x"] += star["wobble"]
                canvas.move(star["id"], star["wobble"], -star["speed"])
                
                # 添加闪烁效果
                if frame % 4 == 0:
                    canvas.itemconfig(star["id"], state=tk.HIDDEN if frame % 8 == 0 else tk.NORMAL)
            
            canvas.after(50, lambda: animate_stars(frame + 1))
        
        animate_stars()
    
    def draw_star_shape(self, canvas, x, y, size, color):
        """绘制五角星形状"""
        import math
        points = []
        for i in range(5):
            # 外顶点
            angle = math.radians(i * 72 - 90)
            points.extend([x + size * math.cos(angle), y + size * math.sin(angle)])
            # 内顶点
            angle = math.radians(i * 72 - 90 + 36)
            points.extend([x + size * 0.4 * math.cos(angle), y + size * 0.4 * math.sin(angle)])
        
        return canvas.create_polygon(points, fill=color, outline="white", width=1, tags="celebration")
    
    def play_firework_animation(self, canvas, x=None, y=None, duration=1500):
        """播放烟花动画"""
        canvas.delete("celebration")
        
        w = int(canvas.cget("width"))
        h = int(canvas.cget("height"))
        
        if x is None:
            x = w // 2
        if y is None:
            y = h // 2
        
        colors = ["#FF6B6B", "#FFD700", "#4ECDC4", "#9C27B0", "#FF9800", "#E91E63"]
        particles = []
        
        # 创建粒子
        import math
        for i in range(20):
            angle = math.radians(i * 18)
            speed = random.uniform(3, 6)
            color = random.choice(colors)
            size = random.randint(4, 8)
            
            particle = {
                "x": x,
                "y": y,
                "vx": speed * math.cos(angle),
                "vy": speed * math.sin(angle),
                "color": color,
                "size": size,
                "id": None
            }
            particle["id"] = canvas.create_oval(x - size//2, y - size//2, x + size//2, y + size//2,
                                                 fill=color, outline="", tags="celebration")
            particles.append(particle)
        
        def animate_firework(frame=0):
            if frame > duration // 40:
                canvas.delete("celebration")
                return
            
            for p in particles:
                p["x"] += p["vx"]
                p["y"] += p["vy"]
                p["vy"] += 0.2  # 重力
                p["size"] = max(1, p["size"] - 0.2)  # 逐渐变小
                
                canvas.coords(p["id"], p["x"] - p["size"]//2, p["y"] - p["size"]//2,
                             p["x"] + p["size"]//2, p["y"] + p["size"]//2)
                
                # 淡出效果
                if frame > duration // 80:
                    canvas.itemconfig(p["id"], state=tk.HIDDEN if frame % 3 == 0 else tk.NORMAL)
            
            canvas.after(40, lambda: animate_firework(frame + 1))
        
        animate_firework()
    
    def play_bounce_text(self, canvas, text, x, y, color="#4CAF50", duration=1000):
        """播放弹跳文字动画"""
        canvas.delete("celebration")
        
        text_id = canvas.create_text(x, y, text=text, font=("微软雅黑", 20, "bold"),
                                      fill=color, tags="celebration")
        
        def animate_bounce(frame=0, direction=1):
            if frame > duration // 50:
                canvas.delete("celebration")
                return
            
            # 弹跳效果
            offset = direction * 3 * (1 - frame / (duration // 50))
            canvas.move(text_id, 0, offset)
            
            # 缩放效果（通过改变字体大小模拟）
            scale = 1 + 0.2 * (1 - frame / (duration // 50))
            size = int(20 * scale)
            canvas.itemconfig(text_id, font=("微软雅黑", size, "bold"))
            
            new_direction = -direction if frame % 4 == 0 else direction
            canvas.after(50, lambda: animate_bounce(frame + 1, new_direction))
        
        animate_bounce()
    
    def play_correct_animation(self, canvas):
        """播放答对动画（组合效果）"""
        # 随机选择动画类型
        anim_type = random.choice(["stars", "firework", "bounce"])
        
        w = int(canvas.cget("width"))
        h = int(canvas.cget("height"))
        
        if anim_type == "stars":
            self.play_star_animation(canvas)
        elif anim_type == "firework":
            self.play_firework_animation(canvas, w // 2, h // 2)
        else:
            texts = ["太棒了！", "真厉害！", "答对啦！", "好聪明！", "真棒！"]
            self.play_bounce_text(canvas, random.choice(texts), w // 2, h // 2)
    
    def play_encourage_animation(self, canvas):
        """播放鼓励动画"""
        w = int(canvas.cget("width"))
        h = int(canvas.cget("height"))
        
        texts = ["加油！", "再试试！", "没关系！", "继续努力！"]
        text = random.choice(texts)
        
        canvas.delete("celebration")
        text_id = canvas.create_text(w // 2, h // 2, text=text, font=("微软雅黑", 16, "bold"),
                                      fill="#FF9800", tags="celebration")
        
        def fade_out(alpha=10):
            if alpha <= 0:
                canvas.delete("celebration")
                return
            # 模拟淡出（通过移动实现）
            canvas.move(text_id, 0, -1)
            canvas.after(100, lambda: fade_out(alpha - 1))
        
        canvas.after(500, lambda: fade_out())
    
    # =====================================================
    # 音效系统
    # =====================================================
    def init_sound_system(self):
        """初始化音效系统"""
        self.sound_enabled = True
        self.music_enabled = False
        self.sound_effects = {}
        
        # 音效文件路径
        effects_dir = os.path.join(self.audio_dir, "effects")
        
        # 预定义音效（如果文件存在则加载）
        effect_files = {
            "click": "click.mp3",
            "correct": "correct.mp3",
            "wrong": "wrong.mp3",
            "levelup": "levelup.mp3",
            "star": "star.mp3"
        }
        
        for name, filename in effect_files.items():
            filepath = os.path.join(effects_dir, filename)
            if os.path.exists(filepath):
                try:
                    self.sound_effects[name] = pygame.mixer.Sound(filepath)
                except:
                    pass
        
        # 加载设置
        self.load_sound_settings()
    
    def load_sound_settings(self):
        """加载音效设置"""
        try:
            if UI_CONFIG_AVAILABLE:
                settings_file = get_data_path("sound_settings.json")
            else:
                settings_file = os.path.join(os.path.dirname(os.path.abspath(__file__)), "sound_settings.json")
            if os.path.exists(settings_file):
                with open(settings_file, 'r', encoding='utf-8') as f:
                    settings = json.load(f)
                    self.sound_enabled = settings.get("sound_enabled", True)
                    self.music_enabled = settings.get("music_enabled", False)
        except:
            pass
    
    def save_sound_settings(self):
        """保存音效设置"""
        try:
            if UI_CONFIG_AVAILABLE:
                settings_file = get_data_path("sound_settings.json")
            else:
                settings_file = os.path.join(os.path.dirname(os.path.abspath(__file__)), "sound_settings.json")
            with open(settings_file, 'w', encoding='utf-8') as f:
                json.dump({
                    "sound_enabled": self.sound_enabled,
                    "music_enabled": self.music_enabled
                }, f)
        except:
            pass
    
    def play_sound(self, sound_name):
        """播放音效"""
        if not self.sound_enabled:
            return
        
        if sound_name in self.sound_effects:
            try:
                self.sound_effects[sound_name].play()
            except:
                pass
    
    def play_click_sound(self):
        """播放点击音效"""
        self.play_sound("click")
    
    def play_correct_sound(self):
        """播放答对音效"""
        self.play_sound("correct")
    
    def play_wrong_sound(self):
        """播放答错音效"""
        self.play_sound("wrong")
    
    def toggle_sound(self):
        """切换音效开关"""
        self.sound_enabled = not self.sound_enabled
        self.save_sound_settings()
        return self.sound_enabled
    
    def toggle_music(self):
        """切换背景音乐开关"""
        self.music_enabled = not self.music_enabled
        self.save_sound_settings()
        
        if self.music_enabled:
            self.start_background_music()
        else:
            self.stop_background_music()
        
        return self.music_enabled
    
    def start_background_music(self):
        """开始播放背景音乐"""
        if not self.music_enabled:
            return
        
        music_file = os.path.join(self.audio_dir, "background.mp3")
        if os.path.exists(music_file):
            try:
                pygame.mixer.music.load(music_file)
                pygame.mixer.music.set_volume(0.3)  # 背景音乐音量较低
                pygame.mixer.music.play(-1)  # 循环播放
            except:
                pass
    
    def stop_background_music(self):
        """停止背景音乐"""
        try:
            pygame.mixer.music.stop()
        except:
            pass
    
    def create_sound_control_button(self, parent, bg_color):
        """创建音效控制按钮"""
        control_frame = tk.Frame(parent, bg=bg_color)
        
        # 音效开关
        sound_text = "🔊" if self.sound_enabled else "🔇"
        self.sound_btn = tk.Button(control_frame, text=sound_text, font=("Segoe UI Emoji", 14),
                                    bg=bg_color, fg="#666", relief=tk.FLAT, cursor="hand2",
                                    command=self.on_sound_toggle)
        self.sound_btn.pack(side=tk.LEFT, padx=2)
        
        # 音乐开关
        music_text = "🎵" if self.music_enabled else "🎶"
        self.music_btn = tk.Button(control_frame, text=music_text, font=("Segoe UI Emoji", 14),
                                    bg=bg_color, fg="#666" if self.music_enabled else "#CCC", 
                                    relief=tk.FLAT, cursor="hand2",
                                    command=self.on_music_toggle)
        self.music_btn.pack(side=tk.LEFT, padx=2)
        
        return control_frame
    
    def on_sound_toggle(self):
        """音效开关点击"""
        enabled = self.toggle_sound()
        self.sound_btn.config(text="🔊" if enabled else "🔇")
    
    def on_music_toggle(self):
        """音乐开关点击"""
        enabled = self.toggle_music()
        self.music_btn.config(text="🎵" if enabled else "🎶",
                              fg="#666" if enabled else "#CCC")
    
    # =====================================================
    # 自适应难度系统
    # =====================================================
    def get_adaptive_word(self, exclude_chars=None):
        """智能选择下一个要学习的汉字
        
        优先级：
        1. 生疏的字(level 0) - 50%概率
        2. 学习中的字(level 1) - 30%概率
        3. 熟悉的字(level 2) - 15%概率
        4. 掌握的字(level 3) - 5%概率
        
        Args:
            exclude_chars: 要排除的字符列表（避免连续出同一个字）
        """
        if exclude_chars is None:
            exclude_chars = []
        
        # 按掌握度分组
        groups = {0: [], 1: [], 2: [], 3: []}
        
        for w in self.words:
            char = w[0]
            if char in exclude_chars:
                continue
            level = self.get_char_mastery_level(char)
            groups[level].append(w)
        
        # 权重选择
        weights = {0: 50, 1: 30, 2: 15, 3: 5}
        
        # 构建加权列表
        weighted_pool = []
        for level, words in groups.items():
            if words:
                weight = weights[level]
                weighted_pool.extend([(w, weight) for w in words])
        
        if not weighted_pool:
            # 如果所有字都被排除了，从全部字库随机选
            available = [w for w in self.words if w[0] not in exclude_chars]
            return random.choice(available) if available else random.choice(self.words)
        
        # 加权随机选择
        total_weight = sum(w[1] for w in weighted_pool)
        r = random.uniform(0, total_weight)
        
        cumulative = 0
        for word, weight in weighted_pool:
            cumulative += weight
            if r <= cumulative:
                return word
        
        return weighted_pool[-1][0]
    
    def get_adaptive_options(self, target_word, num_options=4):
        """智能生成选项，确保难度适中
        
        策略：
        - 干扰项优先选择与目标字掌握度相近的字
        - 避免选择太简单或太难的干扰项
        """
        target_char = target_word[0]
        target_level = self.get_char_mastery_level(target_char)
        
        # 获取其他字
        other_words = [w for w in self.words if w[0] != target_char]
        
        if len(other_words) < num_options - 1:
            # 字库太小，直接随机
            options = [target_word] + random.sample(other_words, min(len(other_words), num_options - 1))
            random.shuffle(options)
            return options
        
        # 按掌握度分组
        same_level = []
        near_level = []
        other_level = []
        
        for w in other_words:
            level = self.get_char_mastery_level(w[0])
            if level == target_level:
                same_level.append(w)
            elif abs(level - target_level) == 1:
                near_level.append(w)
            else:
                other_level.append(w)
        
        # 优先选择同级别或相近级别的字作为干扰项
        distractors = []
        needed = num_options - 1
        
        # 先从同级别选
        if same_level:
            take = min(len(same_level), needed)
            distractors.extend(random.sample(same_level, take))
            needed -= take
        
        # 再从相近级别选
        if needed > 0 and near_level:
            take = min(len(near_level), needed)
            distractors.extend(random.sample(near_level, take))
            needed -= take
        
        # 最后从其他级别选
        if needed > 0 and other_level:
            take = min(len(other_level), needed)
            distractors.extend(random.sample(other_level, take))
        
        options = [target_word] + distractors
        random.shuffle(options)
        return options
    
    def should_review_char(self, char):
        """判断是否应该复习某个字
        
        复习条件：
        - 掌握度下降
        - 长时间未见
        - 错误率高
        """
        if char not in self.char_mastery:
            return False
        
        data = self.char_mastery[char]
        
        # 如果错误次数较多，需要复习
        if data.get("wrong", 0) > data.get("correct", 0):
            return True
        
        # 如果掌握度较低，需要复习
        if data.get("level", 0) <= 1:
            return True
        
        return False
    
    def get_review_words(self, count=5):
        """获取需要复习的字
        
        Returns:
            需要复习的字列表
        """
        review_list = []
        
        for w in self.words:
            char = w[0]
            if self.should_review_char(char):
                review_list.append(w)
        
        # 按掌握度排序（低的优先）
        review_list.sort(key=lambda w: self.char_mastery.get(w[0], {}).get("score", 0))
        
        return review_list[:count]
    
    def set_level(self, level):
        """手动设置难度等级"""
        self.level = level
        self.load_words_by_level()
        self.speak(f"已切换到等级{level}，共{len(self.words)}个字！")
        self.create_main_menu()
    
    def load_words_by_level(self):
        """根据难度等级加载字库 - 优先使用word_database"""
        if WORD_DB_AVAILABLE:
            try:
                self.words = get_characters_by_level(self.level)
                if self.words and len(self.words) > 0:
                    return
            except Exception as e:
                print(f"从word_database加载字库失败: {e}")
        
        # 备份字库（如果word_database不可用）
        LEVEL_1 = [
            ("日", "rì", "☀️", ["太阳", "日出", "日子"], "太阳公公出来了。"),
            ("天", "tiān", "🌤️", ["天空", "今天", "天气"], "今天天气真好。"),
            ("月", "yuè", "🌙", ["月亮", "月光", "月饼"], "月亮弯弯像小船。"),
            ("风", "fēng", "💨", ["大风", "风车", "春风"], "大风吹呀吹。"),
            ("一", "yī", "1️⃣", ["一个", "第一", "一起"], "乐乐是第一名。"),
            ("三", "sān", "3️⃣", ["三个", "第三", "三只"], "三只小猪盖房子。"),
            ("四", "sì", "4️⃣", ["四个", "四方", "四季"], "一年有四季。"),
            ("五", "wǔ", "5️⃣", ["五个", "五颜六色", "五星"], "五颗星星亮晶晶。"),
            ("火", "huǒ", "🔥", ["火车", "大火", "火焰"], "火车跑得真快。"),
            ("水", "shuǐ", "💧", ["喝水", "水果", "河水"], "多喝水身体好。"),
            ("土", "tǔ", "🟤", ["泥土", "土地", "尘土"], "泥土里长出小草。"),
            ("木", "mù", "🪵", ["木头", "树木", "木材"], "木头可以做家具。"),
        ]
        
        LEVEL_2 = [
            ("爸", "bà", "👨", ["爸爸", "爸妈", "老爸"], "爸爸最爱乐乐了。"),
            ("妈", "mā", "👩", ["妈妈", "爸妈", "妈咪"], "妈妈做的饭真香。"),
            ("宝", "bǎo", "👶", ["宝宝", "宝贝", "珍宝"], "乐乐是妈妈的宝贝。"),
            ("姐", "jiě", "👧", ["姐姐", "姐妹", "大姐"], "姐姐带乐乐玩。"),
            ("开", "kāi", "🔓", ["开门", "开心", "打开"], "乐乐开心地笑。"),
            ("关", "guān", "🔒", ["关门", "关灯", "关心"], "睡觉要关灯。"),
            ("地", "dì", "🌍", ["地上", "土地", "地方"], "地上有一朵小花。"),
            ("里", "lǐ", "🏠", ["里面", "家里", "心里"], "家里真温暖。"),
            ("好", "hǎo", "👍", ["好人", "你好", "好看"], "乐乐是好孩子。"),
            ("看", "kàn", "👀", ["看书", "看见", "好看"], "乐乐看书真认真。"),
            ("玩", "wán", "🎮", ["玩具", "玩耍", "好玩"], "乐乐爱玩玩具。"),
            ("饭", "fàn", "🍚", ["吃饭", "米饭", "饭菜"], "乐乐吃饭香香的。"),
        ]
        
        LEVEL_3 = [
            ("他", "tā", "👤", ["他们", "其他", "他人"], "他是我的好朋友。"),
            ("工", "gōng", "🔧", ["工人", "工作", "手工"], "工人叔叔在盖房子。"),
            ("儿", "ér", "👦", ["儿子", "儿童", "女儿"], "乐乐是个好儿子。"),
            ("老", "lǎo", "👴", ["老师", "老人", "老虎"], "老师教我们学知识。"),
            ("叔", "shū", "👨", ["叔叔", "大叔", "叔父"], "叔叔给乐乐买玩具。"),
            ("自", "zì", "🙋", ["自己", "自然", "自由"], "乐乐自己穿衣服。"),
            ("姑", "gū", "👩", ["姑姑", "姑娘", "姑妈"], "姑姑来看乐乐了。"),
            ("娘", "niáng", "👩", ["姑娘", "娘亲", "新娘"], "姑娘穿着漂亮的裙子。"),
            ("电", "diàn", "⚡", ["电视", "电话", "闪电"], "闪电一闪一闪的。"),
            ("比", "bǐ", "⚖️", ["比赛", "对比", "比较"], "我们来比一比谁跑得快。"),
            ("图", "tú", "🖼️", ["图片", "图画", "地图"], "乐乐画了一幅图画。"),
            ("树", "shù", "🌳", ["大树", "树木", "树叶"], "大树下面好乘凉。"),
        ]
        
        if self.level == 1:
            self.words = LEVEL_1.copy()
        elif self.level == 2:
            self.words = LEVEL_1 + LEVEL_2
        else:
            self.words = LEVEL_1 + LEVEL_2 + LEVEL_3
    
    def record_result(self, is_correct, question_data=None):
        """记录答题结果"""
        points = 10 if is_correct else 0
        
        # 更新汉字掌握度
        if question_data:
            # 从question_data中提取汉字
            question = question_data.get("question", "")
            answer = question_data.get("answer", "")
            # 优先使用answer（单个汉字），否则尝试从question提取
            char = answer if len(answer) == 1 else ""
            if not char and ":" in question:
                # 格式如 "看图选字:🌙" 或 "听音选字:月"
                char = question_data.get("answer", "")
            if char and len(char) == 1:
                self.update_char_mastery(char, is_correct)
        
        if LEARNING_DATA_AVAILABLE:
            result = record_answer("literacy", points, is_correct, question_data)
            
            # 答对时将内容加入复习列表
            if is_correct and question_data:
                char = question_data.get("answer", "")
                if char:
                    add_to_review("literacy", char, char)
            
            # 处理返回结果（兼容旧格式）
            if isinstance(result, dict):
                new_badges = result.get("badges", [])
                level_change = result.get("level_change")
                new_level = result.get("new_level", 1)
                
                # 难度变化提示
                if level_change == "up":
                    self.level = new_level
                    self.load_words_by_level()
                    self.window.after(500, lambda: messagebox.showinfo(
                        "🎉 难度升级！", 
                        f"太棒了！你已经升到 {'⭐'*new_level} 难度了！\n题目会更有挑战性哦！"
                    ))
                elif level_change == "down":
                    self.level = new_level
                    self.load_words_by_level()
            else:
                new_badges = result if result else []
            
            if new_badges:
                # 显示新徽章提示
                for badge in new_badges:
                    self.window.after(500, lambda b=badge: messagebox.showinfo(
                        "🎉 获得新徽章！", 
                        f"{b['emoji']} {b['name']}\n{b['desc']}"
                    ))
    
    def get_pinyin(self, char):
        """获取汉字拼音"""
        if PINYIN_AVAILABLE:
            try:
                py = pinyin(char, style=Style.TONE)
                if py and py[0]:
                    return py[0][0]
            except:
                pass
        return "?"
    
    def get_emoji(self, char):
        """获取汉字对应的emoji"""
        return CHAR_EMOJI_MAP.get(char, "📝")
    
    def get_words(self, char):
        """获取汉字组词"""
        return get_char_words(char)
    
    def get_sentence(self, char):
        """获取汉字造句"""
        return get_char_sentence(char)
    
    def parse_word_line(self, line):
        """解析字库文件的一行"""
        line = line.strip()
        if not line or line.startswith('#'):
            return []
        
        # 检查是否是完整格式：汉字,拼音,emoji,组词1|组词2,造句
        if ',' in line:
            parts = line.split(',')
            if len(parts) >= 5:
                char = parts[0].strip()
                py = parts[1].strip()
                emoji = parts[2].strip()
                words = [w.strip() for w in parts[3].split('|')]
                sentence = parts[4].strip()
                return [(char, py, emoji, words, sentence)]
        
        # 简单格式：每个汉字自动生成信息
        result = []
        for char in line:
            if '\u4e00' <= char <= '\u9fff':  # 是汉字
                py = self.get_pinyin(char)
                emoji = self.get_emoji(char)
                words = self.get_words(char)
                sentence = self.get_sentence(char)
                result.append((char, py, emoji, words, sentence))
        return result
    
    def import_word_library(self):
        """导入自定义字库"""
        file_path = filedialog.askopenfilename(
            title="选择字库文件",
            filetypes=[("文本文件", "*.txt"), ("所有文件", "*.*")],
            initialdir=os.path.dirname(os.path.abspath(__file__))
        )
        if not file_path:
            return
        
        try:
            with open(file_path, 'r', encoding='utf-8') as f:
                content = f.read()
            
            new_words = []
            for line in content.split('\n'):
                parsed = self.parse_word_line(line)
                new_words.extend(parsed)
            
            if new_words:
                # 去重
                existing_chars = {w[0] for w in self.words}
                added = 0
                for word in new_words:
                    if word[0] not in existing_chars:
                        self.words.append(word)
                        self.custom_words.append(word)
                        existing_chars.add(word[0])
                        added += 1
                
                messagebox.showinfo("导入成功", f"成功导入 {added} 个新汉字！\n当前字库共 {len(self.words)} 个字。")
                self.speak(f"太棒了！导入了{added}个新汉字！", "+0%")
            else:
                messagebox.showwarning("提示", "没有找到有效的汉字。")
        except Exception as e:
            messagebox.showerror("错误", f"导入失败：{str(e)}")
    
    def clear_custom_library(self):
        """清空自定义字库"""
        if not self.custom_words:
            messagebox.showinfo("提示", "没有自定义字库可清空。")
            return
        
        if messagebox.askyesno("确认", f"确定要清空 {len(self.custom_words)} 个自定义汉字吗？"):
            for word in self.custom_words:
                if word in self.words:
                    self.words.remove(word)
            self.custom_words.clear()
            messagebox.showinfo("完成", "自定义字库已清空。")
    
    def show_library_info(self):
        """显示字库信息"""
        default_count = len(self.words) - len(self.custom_words)
        custom_count = len(self.custom_words)
        
        info = f"📚 字库信息\n\n"
        info += f"默认字库：{default_count} 个字\n"
        info += f"自定义字库：{custom_count} 个字\n"
        info += f"总计：{len(self.words)} 个字\n\n"
        
        if self.custom_words:
            chars = ''.join([w[0] for w in self.custom_words[:30]])
            info += f"自定义汉字：{chars}"
            if len(self.custom_words) > 30:
                info += f"...等{len(self.custom_words)}个"
        
        messagebox.showinfo("字库信息", info)

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
        self.window.after(6000, self._clear_praise_flag)
        if self.praise_audios:
            self.play_audio_file(random.choice(self.praise_audios))
        else:
            self._speak_praise_direct(random.choice(self.praises), "+10%")
    
    def speak_encourage(self):
        self.praise_playing = True
        self.window.after(6000, self._clear_praise_flag)
        if self.encourage_audios:
            self.play_audio_file(random.choice(self.encourage_audios))
        else:
            self._speak_praise_direct(random.choice(self.encourages), "+0%")
    
    def _clear_praise_flag(self):
        self.praise_playing = False

    def create_main_menu(self):
        for widget in self.window.winfo_children():
            widget.destroy()
        self.window.configure(bg="#FFF8E1")
        main_frame = tk.Frame(self.window, bg="#FFF8E1")
        main_frame.pack(fill=tk.BOTH, expand=True, padx=15, pady=8)
        
        # 汪汪队主题标题
        if THEME_AVAILABLE:
            title_canvas = tk.Canvas(main_frame, width=800, height=65, bg="#FFF8E1", highlightthickness=0)
            title_canvas.pack(pady=3)
            ThemeDrawings.draw_paw_badge(title_canvas, 60, 32, 28)
            ThemeDrawings.draw_star(title_canvas, 125, 28, 16, "#FFD700")
            title_canvas.create_text(400, 20, text="🎈 乐乐的识字小课堂 🎈", font=("微软雅黑", 24, "bold"), fill="#FF6B6B")
            title_canvas.create_text(400, 48, text="🐾 汪汪队陪你学汉字！ 🐾", font=("微软雅黑", 10), fill="#666")
            ThemeDrawings.draw_star(title_canvas, 675, 28, 16, "#FFD700")
            ThemeDrawings.draw_paw_badge(title_canvas, 740, 32, 28)
        else:
            tk.Label(main_frame, text="🎈 乐乐的识字小课堂 🎈", font=("微软雅黑", 28, "bold"), bg="#FFF8E1", fg="#FF6B6B").pack(pady=5)
        
        # 等级选择和分数显示
        info_frame = tk.Frame(main_frame, bg="#FFF8E1")
        info_frame.pack(pady=5)
        
        # 等级选择
        level_frame = tk.Frame(info_frame, bg="#4ECDC4", relief=tk.RAISED, bd=2)
        level_frame.pack(side=tk.LEFT, padx=8)
        tk.Label(level_frame, text="📊 难度", font=("微软雅黑", 9, "bold"), bg="#4ECDC4", fg="white").pack(pady=2)
        level_btn_frame = tk.Frame(level_frame, bg="#4ECDC4")
        level_btn_frame.pack(pady=3, padx=5)
        
        level_colors = ["#96CEB4", "#FFD93D", "#FF6B6B"]
        level_texts = ["⭐入门", "⭐⭐进阶", "⭐⭐⭐挑战"]
        for i in range(3):
            lv = i + 1
            bg = level_colors[i] if self.level != lv else "#333"
            btn = tk.Button(level_btn_frame, text=level_texts[i], font=("微软雅黑", 8, "bold"), 
                           bg=bg, fg="white", width=6, relief=tk.RAISED, bd=2, cursor="hand2",
                           command=lambda l=lv: self.set_level(l))
            btn.pack(side=tk.LEFT, padx=2)
        
        # 学习进度
        progress_frame = tk.Frame(info_frame, bg="#9C27B0", relief=tk.RAISED, bd=2)
        progress_frame.pack(side=tk.LEFT, padx=8)
        stats = self.get_mastery_stats()
        tk.Label(progress_frame, text=f"📈 掌握{stats['mastered']} | 熟悉{stats['familiar']} | 学习{stats['learning']}", 
                 font=("微软雅黑", 9), bg="#9C27B0", fg="white", padx=8, pady=5).pack()
        tk.Button(progress_frame, text="📋详情", font=("微软雅黑", 8), bg="#7B1FA2", fg="white",
                  relief=tk.FLAT, cursor="hand2", command=self.show_progress_panel).pack(pady=2)
        
        # 分数显示
        score_frame = tk.Frame(info_frame, bg="#FF6B6B", relief=tk.RAISED, bd=2)
        score_frame.pack(side=tk.LEFT, padx=8)
        stars = get_stars() if LEARNING_DATA_AVAILABLE else 0
        tk.Label(score_frame, text=f"⭐{self.score} | 🌟{stars} | 📚{len(self.words)}字", 
                 font=("微软雅黑", 10, "bold"), bg="#FF6B6B", fg="white", padx=10, pady=8).pack()
        
        # ========== 简单游戏区（3岁+）==========
        easy_section = tk.LabelFrame(main_frame, text="🌟 简单模式（3岁+）", 
                                     font=("微软雅黑", 11, "bold"), bg="#E8F5E9", 
                                     fg="#2E7D32", relief=tk.GROOVE, bd=3)
        easy_section.pack(fill=tk.X, pady=6, padx=5)
        
        easy_frame = tk.Frame(easy_section, bg="#E8F5E9")
        easy_frame.pack(pady=6)
        
        easy_modes = [
            ("📚\n认字卡片", "#FF6B6B", "学汉字", self.start_flashcard),
            ("🖼️\n看图选字", "#4ECDC4", "看图片", self.start_picture),
            ("👂\n听音选字", "#45B7D1", "听声音", self.start_audio),
            ("✏️\n笔顺动画", "#FF9800", "学写字", self.start_stroke),
        ]
        
        for i, (title, color, desc, command) in enumerate(easy_modes):
            card = tk.Frame(easy_frame, bg=color, relief=tk.RAISED, bd=3)
            card.grid(row=0, column=i, padx=12, pady=3)
            btn = tk.Button(card, text=title, font=("微软雅黑", 13, "bold"), bg=color, fg="white", 
                           width=9, height=2, relief=tk.FLAT, cursor="hand2", command=command)
            btn.pack(padx=4, pady=4)
            tk.Label(card, text=desc, font=("微软雅黑", 9), bg=color, fg="white").pack(pady=2)
        
        # ========== 进阶游戏区（4岁+）==========
        advanced_section = tk.LabelFrame(main_frame, text="🚀 进阶模式（4岁+）", 
                                         font=("微软雅黑", 11, "bold"), bg="#E3F2FD", 
                                         fg="#1565C0", relief=tk.GROOVE, bd=3)
        advanced_section.pack(fill=tk.X, pady=6, padx=5)
        
        advanced_frame = tk.Frame(advanced_section, bg="#E3F2FD")
        advanced_frame.pack(pady=6)
        
        advanced_modes = [
            ("🎯\n找朋友", "#96CEB4", "找配对", self.start_match),
            ("🔨\n打地鼠", "#DDA0DD", "快反应", self.start_whack),
            ("⏱️\n限时挑战", "#FFD93D", "计时赛", self.start_challenge),
            ("📖\n故事模式", "#8BC34A", "听故事", self.start_story_mode),
            ("👨‍👩‍👧\n亲子互动", "#E91E63", "家长出题", self.start_parent_mode),
        ]
        
        for i, (title, color, desc, command) in enumerate(advanced_modes):
            card = tk.Frame(advanced_frame, bg=color, relief=tk.RAISED, bd=3)
            card.grid(row=0, column=i, padx=10, pady=3)
            btn = tk.Button(card, text=title, font=("微软雅黑", 13, "bold"), bg=color, fg="white", 
                           width=9, height=2, relief=tk.FLAT, cursor="hand2", command=command)
            btn.pack(padx=4, pady=4)
            tk.Label(card, text=desc, font=("微软雅黑", 9), bg=color, fg="white").pack(pady=2)
        
        # 汪汪队底部装饰
        if THEME_AVAILABLE:
            bottom_canvas = tk.Canvas(main_frame, width=800, height=60, bg="#FFF8E1", highlightthickness=0)
            bottom_canvas.pack(pady=5)
            bottom_canvas.create_rectangle(0, 40, 800, 60, fill="#81C784", outline="")
            ThemeDrawings.draw_puppy_chase(bottom_canvas, 150, 28, 0.35)
            ThemeDrawings.draw_puppy_marshall(bottom_canvas, 320, 28, 0.35)
            ThemeDrawings.draw_puppy_skye(bottom_canvas, 490, 28, 0.35)
            ThemeDrawings.draw_puppy_liberty(bottom_canvas, 660, 28, 0.35)
        
        # 字库管理按钮区
        lib_frame = tk.Frame(main_frame, bg="#FFF8E1")
        lib_frame.pack(pady=3)
        lib_frame.pack(pady=5)
        tk.Button(lib_frame, text="📥 导入字库", font=("微软雅黑", 10), bg="#4ECDC4", fg="white", relief=tk.RAISED, bd=2, cursor="hand2", command=self.import_word_library).pack(side=tk.LEFT, padx=5)
        tk.Button(lib_frame, text="📊 字库信息", font=("微软雅黑", 10), bg="#45B7D1", fg="white", relief=tk.RAISED, bd=2, cursor="hand2", command=self.show_library_info).pack(side=tk.LEFT, padx=5)
        tk.Button(lib_frame, text="🗑️ 清空自定义", font=("微软雅黑", 10), bg="#DDA0DD", fg="white", relief=tk.RAISED, bd=2, cursor="hand2", command=self.clear_custom_library).pack(side=tk.LEFT, padx=5)
        
        # 底部控制区
        bottom_frame = tk.Frame(main_frame, bg="#FFF8E1")
        bottom_frame.pack(pady=10)
        
        # 音效控制
        sound_control = self.create_sound_control_button(bottom_frame, "#FFF8E1")
        sound_control.pack(side=tk.LEFT, padx=20)
        
        tk.Button(bottom_frame, text="👋 退出", font=("微软雅黑", 12), bg="#FF6B6B", fg="white", relief=tk.RAISED, bd=3, cursor="hand2", command=self.on_close_window).pack(side=tk.LEFT, padx=20)
    
    def show_progress_panel(self):
        """显示学习进度详情面板"""
        # 创建弹窗
        panel = tk.Toplevel(self.window)
        panel.title("📈 学习进度详情")
        panel.geometry("700x550")
        panel.configure(bg="#FFF8E1")
        panel.transient(self.window)
        panel.grab_set()
        
        # 居中显示
        panel.update_idletasks()
        x = (panel.winfo_screenwidth() - 700) // 2
        y = (panel.winfo_screenheight() - 550) // 2
        panel.geometry(f"+{x}+{y}")
        
        # 标题
        tk.Label(panel, text="📈 乐乐的学习进度", font=("微软雅黑", 20, "bold"),
                 bg="#FFF8E1", fg="#9C27B0").pack(pady=10)
        
        # 统计概览
        stats = self.get_mastery_stats()
        overview_frame = tk.Frame(panel, bg="white", relief=tk.RAISED, bd=2)
        overview_frame.pack(pady=10, padx=20, fill=tk.X)
        
        # 统计卡片
        cards_frame = tk.Frame(overview_frame, bg="white")
        cards_frame.pack(pady=10)
        
        stat_items = [
            ("🟢 掌握", stats["mastered"], "#4CAF50"),
            ("🟡 熟悉", stats["familiar"], "#FFD700"),
            ("🟠 学习中", stats["learning"], "#FF9800"),
            ("🔴 生疏", stats["new"], "#FF6B6B"),
        ]
        
        for text, count, color in stat_items:
            card = tk.Frame(cards_frame, bg=color, relief=tk.RAISED, bd=2)
            card.pack(side=tk.LEFT, padx=10, pady=5)
            tk.Label(card, text=text, font=("微软雅黑", 10), bg=color, fg="white").pack(padx=15, pady=2)
            tk.Label(card, text=f"{count}字", font=("微软雅黑", 16, "bold"), bg=color, fg="white").pack(padx=15, pady=2)
        
        # 正确率
        total_answers = stats["total_correct"] + stats["total_wrong"]
        accuracy = int(stats["total_correct"] / total_answers * 100) if total_answers > 0 else 0
        tk.Label(overview_frame, text=f"📊 总答题: {total_answers}次 | 正确率: {accuracy}%",
                 font=("微软雅黑", 11), bg="white", fg="#666").pack(pady=5)
        
        # 图例说明
        legend_frame = tk.Frame(panel, bg="#FFF8E1")
        legend_frame.pack(pady=5)
        tk.Label(legend_frame, text="掌握度说明：", font=("微软雅黑", 10), bg="#FFF8E1", fg="#666").pack(side=tk.LEFT)
        tk.Label(legend_frame, text="🟢掌握(9+分)", font=("微软雅黑", 9), bg="#FFF8E1", fg="#4CAF50").pack(side=tk.LEFT, padx=5)
        tk.Label(legend_frame, text="🟡熟悉(6-8分)", font=("微软雅黑", 9), bg="#FFF8E1", fg="#FFD700").pack(side=tk.LEFT, padx=5)
        tk.Label(legend_frame, text="🟠学习中(3-5分)", font=("微软雅黑", 9), bg="#FFF8E1", fg="#FF9800").pack(side=tk.LEFT, padx=5)
        tk.Label(legend_frame, text="🔴生疏(0-2分)", font=("微软雅黑", 9), bg="#FFF8E1", fg="#FF6B6B").pack(side=tk.LEFT, padx=5)
        
        # 汉字详情区域（带滚动）
        tk.Label(panel, text="📚 各汉字掌握情况", font=("微软雅黑", 12, "bold"),
                 bg="#FFF8E1", fg="#333").pack(pady=5)
        
        # 创建滚动区域
        canvas_frame = tk.Frame(panel, bg="#FFF8E1")
        canvas_frame.pack(fill=tk.BOTH, expand=True, padx=20, pady=5)
        
        canvas = tk.Canvas(canvas_frame, bg="white", highlightthickness=1, highlightbackground="#DDD")
        scrollbar = ttk.Scrollbar(canvas_frame, orient="vertical", command=canvas.yview)
        scrollable_frame = tk.Frame(canvas, bg="white")
        
        scrollable_frame.bind(
            "<Configure>",
            lambda e: canvas.configure(scrollregion=canvas.bbox("all"))
        )
        
        canvas.create_window((0, 0), window=scrollable_frame, anchor="nw")
        canvas.configure(yscrollcommand=scrollbar.set)
        
        canvas.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)
        scrollbar.pack(side=tk.RIGHT, fill=tk.Y)
        
        # 显示每个汉字的掌握情况
        chars_per_row = 8
        for i, w in enumerate(self.words):
            char = w[0]
            row = i // chars_per_row
            col = i % chars_per_row
            
            level = self.get_char_mastery_level(char)
            color = self.get_mastery_color(level)
            
            # 获取详细数据
            data = self.char_mastery.get(char, {"correct": 0, "wrong": 0, "score": 0})
            
            char_frame = tk.Frame(scrollable_frame, bg=color, relief=tk.RAISED, bd=2)
            char_frame.grid(row=row, column=col, padx=5, pady=5)
            
            tk.Label(char_frame, text=char, font=("楷体", 24, "bold"),
                     bg=color, fg="white", width=2).pack(padx=5, pady=2)
            tk.Label(char_frame, text=f"✓{data.get('correct',0)} ✗{data.get('wrong',0)}",
                     font=("微软雅黑", 8), bg=color, fg="white").pack()
        
        # 关闭按钮
        tk.Button(panel, text="关闭", font=("微软雅黑", 11), bg="#9C27B0", fg="white",
                  padx=30, command=panel.destroy).pack(pady=10)
    
    def clear_game_area(self, bg_color="#FFF8E1"):
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
        tk.Label(nav_frame, text=f"⭐ 总分: {self.score}", font=("微软雅黑", 12, "bold"), bg=bg_color, fg="#FF6B6B").pack(side=tk.RIGHT, padx=10)
        self.game_frame = tk.Frame(self.window, bg=bg_color)
        self.game_frame.pack(fill=tk.BOTH, expand=True, padx=20, pady=10)

    def start_flashcard(self):
        self.clear_game_area("#FFF8DC")
        self.card_index = 0
        
        # 使用居中容器
        center_frame = tk.Frame(self.game_frame, bg="#FFF8DC")
        center_frame.pack(expand=True)
        
        tk.Label(center_frame, text="📚 认字卡片", font=("微软雅黑", 28, "bold"), bg="#FFF8DC", fg="#FF6B6B").pack(pady=8)
        self.card_progress = tk.Label(center_frame, text="", font=("微软雅黑", 12), bg="#FFF8DC", fg="#666")
        self.card_progress.pack(pady=5)
        
        card = tk.Frame(center_frame, bg="white", relief=tk.RAISED, bd=4)
        card.pack(pady=15, padx=60, ipadx=80)
        
        self.card_char = tk.Label(card, text="", font=("楷体", 140, "bold"), bg="white", fg="#FF6B6B")
        self.card_char.pack(pady=20)
        self.card_pinyin = tk.Label(card, text="", font=("Arial", 28), bg="white", fg="#4ECDC4")
        self.card_pinyin.pack(pady=8)
        self.card_emoji = tk.Label(card, text="", font=("Segoe UI Emoji", 55), bg="white")
        self.card_emoji.pack(pady=12)
        self.card_words = tk.Label(card, text="", font=("微软雅黑", 18), bg="white", fg="#666")
        self.card_words.pack(pady=8)
        self.card_sentence = tk.Label(card, text="", font=("微软雅黑", 16), bg="white", fg="#888")
        self.card_sentence.pack(pady=15)
        
        btn_frame = tk.Frame(center_frame, bg="#FFF8DC")
        btn_frame.pack(pady=20)
        tk.Button(btn_frame, text="⬅️ 上一个", font=("微软雅黑", 12), bg="#45B7D1", fg="white", command=self.prev_card, width=10, height=2).pack(side=tk.LEFT, padx=8)
        tk.Button(btn_frame, text="🔊 读一读", font=("微软雅黑", 12), bg="#FF6B6B", fg="white", command=self.speak_card, width=10, height=2).pack(side=tk.LEFT, padx=8)
        tk.Button(btn_frame, text="下一个 ➡️", font=("微软雅黑", 12), bg="#45B7D1", fg="white", command=self.next_card, width=10, height=2).pack(side=tk.LEFT, padx=8)
        self.show_card()
    
    def show_card(self):
        w = self.words[self.card_index]
        self.card_char.config(text=w[0])
        self.card_pinyin.config(text=w[1])
        self.card_emoji.config(text=w[2])
        self.card_words.config(text="组词：" + "、".join(w[3]))
        self.card_sentence.config(text="造句：" + w[4])
        self.card_progress.config(text=f"第 {self.card_index + 1} / {len(self.words)} 个字")
        self.speak(f"这个字念，{w[0]}，{w[0]}，{w[4]}", "-10%")
    
    def speak_card(self):
        w = self.words[self.card_index]
        self.speak(f"{w[0]}，{w[0]}，组词，{'，'.join(w[3])}，造句，{w[4]}", "-10%")
    
    def next_card(self):
        self.card_index = (self.card_index + 1) % len(self.words)
        self.show_card()
    
    def prev_card(self):
        self.card_index = (self.card_index - 1) % len(self.words)
        self.show_card()
    
    def start_picture(self):
        self.clear_game_area("#E0FFFF")
        self.pic_score = 0
        
        # 标题带狗狗装饰
        if THEME_AVAILABLE:
            title_canvas = tk.Canvas(self.game_frame, width=600, height=70, bg="#E0FFFF", highlightthickness=0)
            title_canvas.pack(pady=5)
            title_canvas.create_text(300, 22, text="🐾 看图选字 🐾", font=("微软雅黑", 24, "bold"), fill="#4ECDC4")
            title_canvas.create_text(300, 52, text="看图片，选汉字！", font=("微软雅黑", 11), fill="#666")
            ThemeDrawings.draw_puppy_chase(title_canvas, 60, 40, 0.4)
            ThemeDrawings.draw_puppy_skye(title_canvas, 540, 40, 0.4)
        else:
            tk.Label(self.game_frame, text="🖼️ 看图选字", font=("微软雅黑", 26, "bold"), bg="#E0FFFF", fg="#4ECDC4").pack(pady=5)
        
        self.pic_score_label = tk.Label(self.game_frame, text="⭐ 得分: 0", font=("微软雅黑", 14), bg="#E0FFFF", fg="#666")
        self.pic_score_label.pack(pady=5)
        self.pic_emoji = tk.Label(self.game_frame, text="", font=("Segoe UI Emoji", 100), bg="white", relief=tk.RAISED, bd=4, padx=30, pady=15)
        self.pic_emoji.pack(pady=15)
        self.pic_hint = tk.Label(self.game_frame, text="", font=("微软雅黑", 18), bg="#E0FFFF")
        self.pic_hint.pack(pady=5)
        
        # 反馈区域（显示狗狗）
        self.pic_feedback_canvas = tk.Canvas(self.game_frame, width=180, height=100, 
                                             bg="#E0FFFF", highlightthickness=0)
        self.pic_feedback_canvas.pack(pady=5)
        
        self.pic_frame = tk.Frame(self.game_frame, bg="#E0FFFF")
        self.pic_frame.pack(pady=20)
        self.pic_buttons = []
        colors = ["#FF6B6B", "#4ECDC4", "#45B7D1", "#96CEB4"]
        for i in range(4):
            btn = tk.Button(self.pic_frame, text="", font=("楷体", 50, "bold"), width=3, height=1, bg=colors[i], fg="white", relief=tk.RAISED, bd=4, cursor="hand2", command=lambda idx=i: self.check_picture(idx))
            btn.grid(row=0, column=i, padx=15)
            self.pic_buttons.append(btn)
        self.new_picture_question()
    
    def new_picture_question(self):
        # 使用自适应难度选择目标字
        self.pic_target = self.get_adaptive_word()
        
        # 使用智能选项生成
        self.pic_options = self.get_adaptive_options(self.pic_target, 4)
        self.pic_correct_idx = self.pic_options.index(self.pic_target)
        
        self.pic_emoji.config(text=self.pic_target[2])
        colors = ["#FF6B6B", "#4ECDC4", "#45B7D1", "#96CEB4"]
        for i, btn in enumerate(self.pic_buttons):
            btn.config(text=self.pic_options[i][0], bg=colors[i], state=tk.NORMAL)
        self.pic_hint.config(text="", fg="#666")
        self.speak("看图片，选汉字！", "-10%")
    
    def check_picture(self, idx):
        # 清空反馈区域
        if hasattr(self, 'pic_feedback_canvas'):
            self.pic_feedback_canvas.delete("all")
        
        if idx == self.pic_correct_idx:
            self.pic_score += 10
            self.score += 10
            self.pic_hint.config(text=f"🎉 对啦！是{self.pic_target[0]}！", fg="#32CD32")
            self.pic_buttons[idx].config(bg="#32CD32")
            self.record_result(True, {"question": f"看图选字:{self.pic_target[2]}", "answer": self.pic_target[0]})
            
            # 播放庆祝动画
            if hasattr(self, 'pic_feedback_canvas'):
                self.play_correct_animation(self.pic_feedback_canvas)
            
            # 显示庆祝的狗狗
            if THEME_AVAILABLE and hasattr(self, 'pic_feedback_canvas'):
                self.window.after(500, lambda: self.show_paw_feedback_on_canvas(self.pic_feedback_canvas, True))
            self.speak_praise()
        else:
            self.pic_hint.config(text=f"😅 是{self.pic_target[0]}哦！", fg="#FF6B6B")
            self.pic_buttons[idx].config(bg="#808080")
            self.pic_buttons[self.pic_correct_idx].config(bg="#32CD32")
            self.record_result(False, {"question": f"看图选字:{self.pic_target[2]}", "answer": self.pic_target[0]})
            
            # 播放鼓励动画
            if hasattr(self, 'pic_feedback_canvas'):
                self.play_encourage_animation(self.pic_feedback_canvas)
            
            # 显示鼓励的狗狗
            if THEME_AVAILABLE and hasattr(self, 'pic_feedback_canvas'):
                self.window.after(500, lambda: self.show_paw_feedback_on_canvas(self.pic_feedback_canvas, False))
            self.speak_encourage()
        self.pic_score_label.config(text=f"⭐ 得分: {self.pic_score}")
        for btn in self.pic_buttons:
            btn.config(state=tk.DISABLED)
        self.window.after(5500, self.new_picture_question)
    
    def start_audio(self):
        self.clear_game_area("#FFE4E1")
        self.audio_score = 0
        
        # 标题带狗狗装饰
        if THEME_AVAILABLE:
            title_canvas = tk.Canvas(self.game_frame, width=600, height=70, bg="#FFE4E1", highlightthickness=0)
            title_canvas.pack(pady=5)
            title_canvas.create_text(300, 22, text="🐾 听音选字 🐾", font=("微软雅黑", 24, "bold"), fill="#45B7D1")
            title_canvas.create_text(300, 52, text="听声音，选汉字！", font=("微软雅黑", 11), fill="#666")
            ThemeDrawings.draw_puppy_marshall(title_canvas, 60, 40, 0.4)
            ThemeDrawings.draw_puppy_rubble(title_canvas, 540, 40, 0.4)
        else:
            tk.Label(self.game_frame, text="👂 听音选字", font=("微软雅黑", 26, "bold"), bg="#FFE4E1", fg="#45B7D1").pack(pady=5)
        
        self.audio_score_label = tk.Label(self.game_frame, text="⭐ 得分: 0", font=("微软雅黑", 14), bg="#FFE4E1", fg="#666")
        self.audio_score_label.pack(pady=5)
        tk.Button(self.game_frame, text="🔊 再听一遍", font=("微软雅黑", 12), bg="#FF6B6B", fg="white", command=self.replay_audio).pack(pady=10)
        self.audio_hint = tk.Label(self.game_frame, text="", font=("微软雅黑", 18), bg="#FFE4E1")
        self.audio_hint.pack(pady=5)
        
        # 反馈区域（显示狗狗）
        self.audio_feedback_canvas = tk.Canvas(self.game_frame, width=180, height=100, 
                                               bg="#FFE4E1", highlightthickness=0)
        self.audio_feedback_canvas.pack(pady=5)
        
        self.audio_frame = tk.Frame(self.game_frame, bg="#FFE4E1")
        self.audio_frame.pack(pady=20)
        self.audio_buttons = []
        colors = ["#FF6B6B", "#4ECDC4", "#45B7D1", "#96CEB4"]
        for i in range(4):
            btn = tk.Button(self.audio_frame, text="", font=("楷体", 50, "bold"), width=3, height=1, bg=colors[i], fg="white", relief=tk.RAISED, bd=4, cursor="hand2", command=lambda idx=i: self.check_audio(idx))
            btn.grid(row=0, column=i, padx=15)
            self.audio_buttons.append(btn)
        self.new_audio_question()
    
    def new_audio_question(self):
        # 使用自适应难度选择目标字
        self.audio_target = self.get_adaptive_word()
        
        # 使用智能选项生成
        self.audio_options = self.get_adaptive_options(self.audio_target, 4)
        self.audio_correct_idx = self.audio_options.index(self.audio_target)
        
        colors = ["#FF6B6B", "#4ECDC4", "#45B7D1", "#96CEB4"]
        for i, btn in enumerate(self.audio_buttons):
            btn.config(text=self.audio_options[i][0], bg=colors[i], state=tk.NORMAL)
        self.audio_hint.config(text="", fg="#666")
        self.speak(f"请选择，{self.audio_target[0]}", "-10%")
    
    def replay_audio(self):
        self.speak(f"{self.audio_target[0]}", "-10%")
    
    def check_audio(self, idx):
        # 清空反馈区域
        if hasattr(self, 'audio_feedback_canvas'):
            self.audio_feedback_canvas.delete("all")
        
        if idx == self.audio_correct_idx:
            self.audio_score += 10
            self.score += 10
            self.audio_hint.config(text=f"🎉 对啦！是{self.audio_target[0]}！", fg="#32CD32")
            self.audio_buttons[idx].config(bg="#32CD32")
            self.record_result(True, {"question": f"听音选字:{self.audio_target[0]}", "answer": self.audio_target[0]})
            
            # 播放庆祝动画
            if hasattr(self, 'audio_feedback_canvas'):
                self.play_correct_animation(self.audio_feedback_canvas)
            
            # 显示庆祝的狗狗
            if THEME_AVAILABLE and hasattr(self, 'audio_feedback_canvas'):
                self.window.after(500, lambda: self.show_paw_feedback_on_canvas(self.audio_feedback_canvas, True))
            self.speak_praise()
        else:
            self.audio_hint.config(text=f"😅 是{self.audio_target[0]}哦！", fg="#FF6B6B")
            self.audio_buttons[idx].config(bg="#808080")
            self.audio_buttons[self.audio_correct_idx].config(bg="#32CD32")
            self.record_result(False, {"question": f"听音选字:{self.audio_target[0]}", "answer": self.audio_target[0]})
            
            # 播放鼓励动画
            if hasattr(self, 'audio_feedback_canvas'):
                self.play_encourage_animation(self.audio_feedback_canvas)
            
            # 显示鼓励的狗狗
            if THEME_AVAILABLE and hasattr(self, 'audio_feedback_canvas'):
                self.window.after(500, lambda: self.show_paw_feedback_on_canvas(self.audio_feedback_canvas, False))
            self.speak_encourage()
        self.audio_score_label.config(text=f"⭐ 得分: {self.audio_score}")
        for btn in self.audio_buttons:
            btn.config(state=tk.DISABLED)
        self.window.after(5500, self.new_audio_question)
    
    def start_match(self):
        """找朋友游戏 - 汉字和图片/拼音配对"""
        self.clear_game_area("#FFFACD")
        self.match_score = 0
        self.match_selected = None  # 当前选中的卡片索引
        self.match_cards = []
        self.match_card_data = []
        self.match_matched = set()  # 已配对的索引
        
        tk.Label(self.game_frame, text="🎯 找朋友", font=("微软雅黑", 26, "bold"),
                 bg="#FFFACD", fg="#FF6B6B").pack(pady=5)
        
        self.match_score_label = tk.Label(self.game_frame, text="⭐ 得分: 0",
                                           font=("微软雅黑", 14), bg="#FFFACD", fg="#666")
        self.match_score_label.pack(pady=5)
        
        tk.Label(self.game_frame, text="点击两张卡片，找到汉字和它的图片朋友！",
                 font=("微软雅黑", 13), bg="#FFFACD", fg="#888").pack(pady=5)
        
        self.match_hint = tk.Label(self.game_frame, text="", font=("微软雅黑", 16), bg="#FFFACD")
        self.match_hint.pack(pady=5)
        
        # 卡片区域 (4x3)
        cards_frame = tk.Frame(self.game_frame, bg="#FFFACD")
        cards_frame.pack(pady=15)
        
        # 选择6对卡片（汉字+emoji）
        selected_words = random.sample(self.words, min(6, len(self.words)))
        
        # 创建卡片数据：每个汉字对应一个emoji
        for w in selected_words:
            self.match_card_data.append({"type": "char", "char": w[0], "match_id": w[0]})
            self.match_card_data.append({"type": "emoji", "emoji": w[2], "char": w[0], "match_id": w[0]})
        
        # 打乱顺序
        random.shuffle(self.match_card_data)
        
        # 创建卡片按钮
        colors = ["#FFB6C1", "#98FB98", "#87CEEB", "#DDA0DD", "#F0E68C", "#FFA07A",
                  "#B0E0E6", "#FFE4B5", "#E6E6FA", "#FFDAB9", "#D8BFD8", "#F5DEB3"]
        
        for i in range(12):
            row = i // 4
            col = i % 4
            
            card_data = self.match_card_data[i]
            if card_data["type"] == "char":
                text = card_data["char"]
                font = ("楷体", 36, "bold")
            else:
                text = card_data["emoji"]
                font = ("Segoe UI Emoji", 36)
            
            btn = tk.Button(cards_frame, text="❓", font=("Segoe UI Emoji", 36),
                           width=3, height=1, bg=colors[i], fg="#333",
                           relief=tk.RAISED, bd=4, cursor="hand2",
                           command=lambda idx=i: self.match_click(idx))
            btn.grid(row=row, column=col, padx=10, pady=10)
            btn.card_text = text
            btn.card_font = font
            btn.card_color = colors[i]
            self.match_cards.append(btn)
        
        self.speak("找朋友游戏开始！找到汉字和图片配对！", "+0%")
        
        # 先展示所有卡片3秒
        self.match_show_all()
    
    def match_show_all(self):
        """展示所有卡片让玩家记忆"""
        for i, btn in enumerate(self.match_cards):
            btn.config(text=btn.card_text, font=btn.card_font)
        self.match_hint.config(text="👀 记住卡片位置！3秒后翻回去...", fg="#FF8C00")
        self.window.after(3000, self.match_hide_all)
    
    def match_hide_all(self):
        """隐藏所有卡片"""
        for i, btn in enumerate(self.match_cards):
            if i not in self.match_matched:
                btn.config(text="❓", font=("Segoe UI Emoji", 36))
        self.match_hint.config(text="点击卡片找朋友！", fg="#666")
    
    def match_click(self, idx):
        """点击卡片"""
        if idx in self.match_matched:
            return
        
        btn = self.match_cards[idx]
        
        # 翻开卡片
        btn.config(text=btn.card_text, font=btn.card_font)
        
        if self.match_selected is None:
            # 第一张卡片
            self.match_selected = idx
            btn.config(relief=tk.SUNKEN)
        else:
            # 第二张卡片
            first_idx = self.match_selected
            first_btn = self.match_cards[first_idx]
            
            first_data = self.match_card_data[first_idx]
            second_data = self.match_card_data[idx]
            
            if first_data["match_id"] == second_data["match_id"] and first_idx != idx:
                # 配对成功！
                self.match_score += 20
                self.score += 20
                self.match_score_label.config(text=f"⭐ 得分: {self.match_score}")
                
                self.match_matched.add(first_idx)
                self.match_matched.add(idx)
                
                first_btn.config(bg="#32CD32", relief=tk.FLAT)
                btn.config(bg="#32CD32", relief=tk.FLAT)
                
                char = first_data["match_id"]
                self.match_hint.config(text=f"🎉 太棒了！{char} 找到朋友了！", fg="#32CD32")
                self.speak_praise()
                
                # 检查是否全部配对完成
                if len(self.match_matched) == 12:
                    self.window.after(1500, self.match_complete)
            else:
                # 配对失败
                self.match_hint.config(text="😅 不是朋友，再试试！", fg="#FF6B6B")
                self.speak_encourage()
                
                # 1.5秒后翻回去
                self.window.after(1500, lambda: self.match_flip_back(first_idx, idx))
            
            self.match_selected = None
            first_btn.config(relief=tk.RAISED)
    
    def match_flip_back(self, idx1, idx2):
        """翻回卡片"""
        if idx1 not in self.match_matched:
            self.match_cards[idx1].config(text="❓", font=("Segoe UI Emoji", 36))
        if idx2 not in self.match_matched:
            self.match_cards[idx2].config(text="❓", font=("Segoe UI Emoji", 36))
    
    def match_complete(self):
        """配对完成"""
        self.match_hint.config(text=f"🏆 太厉害了！全部找到朋友了！得分：{self.match_score}", fg="#FF6B6B")
        self.speak(f"太棒了！乐乐全部配对成功，得了{self.match_score}分！", "+0%")
        self.window.after(5500, self.create_main_menu)
    
    def start_whack(self):
        """打地鼠游戏 - 打掉带有目标汉字的地鼠"""
        self.clear_game_area("#90EE90")  # 草地绿色背景
        self.whack_score = 0
        self.whack_running = True
        self.whack_combo = 0  # 连击数
        self.whack_holes = []
        self.whack_hole_states = [None] * 9  # 每个洞的状态：None=空, 字符=地鼠
        self.whack_target_char = None
        self.whack_can_click = False  # 是否可以点击
        self.whack_round = 0  # 当前轮次
        self.whack_correct_pos = -1  # 正确答案位置
        
        tk.Label(self.game_frame, text="🔨 打地鼠识字", font=("微软雅黑", 26, "bold"),
                 bg="#90EE90", fg="#228B22").pack(pady=5)
        
        # 信息栏
        info_frame = tk.Frame(self.game_frame, bg="#90EE90")
        info_frame.pack(pady=8)
        
        self.whack_score_label = tk.Label(info_frame, text="⭐ 得分: 0",
                                           font=("微软雅黑", 14, "bold"), bg="#90EE90", fg="#FF6B6B")
        self.whack_score_label.pack(side=tk.LEFT, padx=15)
        
        self.whack_combo_label = tk.Label(info_frame, text="🔥 连击: 0",
                                           font=("微软雅黑", 14, "bold"), bg="#90EE90", fg="#FF8C00")
        self.whack_combo_label.pack(side=tk.LEFT, padx=15)
        
        self.whack_round_label = tk.Label(info_frame, text="📍 第1轮",
                                           font=("微软雅黑", 14), bg="#90EE90", fg="#666")
        self.whack_round_label.pack(side=tk.LEFT, padx=15)
        
        # 目标提示区 - 显示要找的汉字
        target_frame = tk.Frame(self.game_frame, bg="#FFD700", relief=tk.RAISED, bd=4)
        target_frame.pack(pady=10)
        
        tk.Label(target_frame, text="🎯 打这个字：", font=("微软雅黑", 18),
                 bg="#FFD700", fg="#333").pack(side=tk.LEFT, padx=15, pady=12)
        
        self.whack_target_label = tk.Label(target_frame, text="", font=("楷体", 60, "bold"),
                                            bg="#FFD700", fg="#DC143C")
        self.whack_target_label.pack(side=tk.LEFT, padx=20, pady=12)
        
        # 提示文字
        self.whack_hint = tk.Label(self.game_frame, text="准备开始...", 
                                    font=("微软雅黑", 15), bg="#90EE90", fg="#006400")
        self.whack_hint.pack(pady=8)
        
        # 地鼠洞区域 (3x3) - 草地风格
        holes_frame = tk.Frame(self.game_frame, bg="#228B22", relief=tk.RIDGE, bd=6)
        holes_frame.pack(pady=10)
        
        for i in range(9):
            row = i // 3
            col = i % 3
            
            # 洞的外框 - 土色
            hole_outer = tk.Frame(holes_frame, bg="#8B4513", relief=tk.SUNKEN, bd=4)
            hole_outer.grid(row=row, column=col, padx=12, pady=12)
            
            # 按钮 - 初始显示空洞
            btn = tk.Button(hole_outer, text="🕳️", font=("Segoe UI Emoji", 32),
                           width=4, height=2, bg="#3D2914", fg="#333",
                           relief=tk.SUNKEN, bd=3, cursor="hand2",
                           activebackground="#5D4934",
                           command=lambda idx=i: self.whack_click(idx))
            btn.pack(padx=4, pady=4)
            self.whack_holes.append(btn)
        
        # 开始游戏
        self.speak("打地鼠游戏开始！看到目标汉字就快打它！", "+0%")
        self.window.after(2500, self.whack_new_round)
    
    def whack_new_round(self):
        """新一轮 - 选择目标汉字并让地鼠出现"""
        if not self.whack_running:
            return
        
        self.whack_round += 1
        self.whack_can_click = False
        self.whack_correct_pos = -1
        
        # 重置所有洞为空
        for i in range(9):
            self.whack_holes[i].config(text="🕳️", bg="#3D2914", state=tk.NORMAL)
            self.whack_hole_states[i] = None
        
        # 选择目标汉字
        self.whack_target_word = random.choice(self.words)
        self.whack_target_char = self.whack_target_word[0]
        self.whack_target_label.config(text=self.whack_target_char)
        self.whack_round_label.config(text=f"📍 第{self.whack_round}轮")
        
        self.whack_hint.config(text=f"🎯 准备！找 [{self.whack_target_char}]", fg="#006400")
        
        # 语音提示
        self.speak(f"找，{self.whack_target_char}", "+0%")
        
        # 1.5秒后让地鼠出现
        self.window.after(1500, self.whack_show_moles)
    
    def whack_show_moles(self):
        """让地鼠从洞里冒出来"""
        if not self.whack_running:
            return
        
        self.whack_can_click = True
        
        # 确保字库足够
        if len(self.words) < 4:
            # 字库太少，添加默认字
            default_chars = [
                ("猫", "māo", "🐱", ["小猫", "猫咪"], "小猫咪在晒太阳。"),
                ("狗", "gǒu", "🐕", ["小狗", "狗狗"], "小狗汪汪叫。"),
                ("鸟", "niǎo", "🐦", ["小鸟", "鸟儿"], "小鸟在天上飞。"),
                ("鱼", "yú", "🐟", ["小鱼", "金鱼"], "鱼儿在水里游。"),
            ]
            for c in default_chars:
                if c not in self.words:
                    self.words.append(c)
        
        # 根据轮次调整难度
        if self.whack_round <= 3:
            num_moles = 3  # 前3轮只有3个地鼠
        elif self.whack_round <= 6:
            num_moles = 4
        else:
            num_moles = random.randint(4, 5)
        
        # 确保地鼠数量不超过可用字数
        num_moles = min(num_moles, len(self.words))
        
        positions = random.sample(range(9), num_moles)
        
        # 随机选择正确答案的位置
        self.whack_correct_pos = random.choice(positions)
        
        # 选择干扰汉字
        other_words = [w for w in self.words if w[0] != self.whack_target_char]
        num_distractors = min(len(other_words), num_moles - 1)
        distractors = random.sample(other_words, num_distractors) if num_distractors > 0 else []
        
        # 放置地鼠
        distractor_idx = 0
        for pos in positions:
            if pos == self.whack_correct_pos:
                # 正确答案的地鼠 - 绿色背景更醒目
                char = self.whack_target_char
                self.whack_holes[pos].config(text=f"🐹\n{char}", bg="#98FB98")
                self.whack_hole_states[pos] = char
            else:
                # 干扰地鼠 - 橙色背景
                if distractor_idx < len(distractors):
                    char = distractors[distractor_idx][0]
                    self.whack_holes[pos].config(text=f"🐹\n{char}", bg="#FFDAB9")
                    self.whack_hole_states[pos] = char
                    distractor_idx += 1
        
        self.whack_hint.config(text=f"🔨 快打 [{self.whack_target_char}] ！", fg="#DC143C")
        
        # 5秒后地鼠缩回去（给小朋友足够时间）
        self.window.after(5000, self.whack_timeout)
    
    def whack_timeout(self):
        """超时 - 地鼠跑掉了"""
        if not self.whack_running or not self.whack_can_click:
            return
        
        self.whack_can_click = False
        self.whack_combo = 0
        self.whack_combo_label.config(text=f"🔥 连击: 0")
        
        # 高亮显示正确答案
        if self.whack_correct_pos >= 0:
            self.whack_holes[self.whack_correct_pos].config(bg="#32CD32")
        
        self.whack_hint.config(text=f"⏰ 时间到！正确答案是 [{self.whack_target_char}]", fg="#FF6B6B")
        self.speak_encourage()
        
        # 2秒后隐藏地鼠，进入下一轮
        self.window.after(2000, self.whack_hide_and_next)
    
    def whack_hide_and_next(self):
        """隐藏地鼠并进入下一轮"""
        if not self.whack_running:
            return
        
        # 隐藏所有地鼠
        for i in range(9):
            self.whack_holes[i].config(text="🕳️", bg="#3D2914")
            self.whack_hole_states[i] = None
        
        # 1秒后下一轮
        self.window.after(1000, self.whack_new_round)
    
    def whack_click(self, idx):
        """点击地鼠洞"""
        if not self.whack_running or not self.whack_can_click:
            return
        
        state = self.whack_hole_states[idx]
        
        if state is None:
            # 点击空洞 - 无反应
            return
        
        self.whack_can_click = False  # 防止重复点击
        
        if state == self.whack_target_char:
            # 打中正确的地鼠！
            self.whack_combo += 1
            bonus = min(self.whack_combo * 2, 10)  # 连击奖励，最多+10
            points = 10 + bonus
            self.whack_score += points
            self.score += points
            
            self.whack_score_label.config(text=f"⭐ 得分: {self.whack_score}")
            self.whack_combo_label.config(text=f"🔥 连击: {self.whack_combo}")
            
            # 显示打中效果
            self.whack_holes[idx].config(text="💥\n✓", bg="#32CD32")
            
            if self.whack_combo >= 3:
                self.whack_hint.config(text=f"🎉 太棒了！连击x{self.whack_combo}！+{points}分！", fg="#FF8C00")
            else:
                self.whack_hint.config(text=f"🎉 打中了！[{self.whack_target_char}] +{points}分！", fg="#32CD32")
            
            self.speak_praise()
            
            # 隐藏其他地鼠
            for i in range(9):
                if i != idx:
                    self.whack_holes[i].config(text="🕳️", bg="#3D2914")
                    self.whack_hole_states[i] = None
            
            # 2秒后下一轮
            self.window.after(2000, self.whack_hide_and_next)
        else:
            # 打错了
            self.whack_combo = 0
            self.whack_combo_label.config(text=f"🔥 连击: 0")
            
            # 显示错误
            self.whack_holes[idx].config(text="❌", bg="#808080")
            
            # 高亮正确答案
            if self.whack_correct_pos >= 0:
                self.whack_holes[self.whack_correct_pos].config(bg="#32CD32")
            
            self.whack_hint.config(text=f"😅 打错了！正确的是 [{self.whack_target_char}]", fg="#FF6B6B")
            self.speak_encourage()
            
            # 2.5秒后下一轮（让玩家看清正确答案）
            self.window.after(2500, self.whack_hide_and_next)
    
    def start_challenge(self):
        """限时挑战 - 60秒内答对尽可能多的题"""
        self.clear_game_area("#FFE4E1")
        self.challenge_score = 0
        self.challenge_correct = 0
        self.challenge_wrong = 0
        self.challenge_time = 60
        self.challenge_running = True
        
        tk.Label(self.game_frame, text="⏱️ 限时挑战", font=("微软雅黑", 26, "bold"),
                 bg="#FFE4E1", fg="#DC143C").pack(pady=5)
        
        # 信息栏
        info_frame = tk.Frame(self.game_frame, bg="#FFE4E1")
        info_frame.pack(pady=10)
        
        self.challenge_time_label = tk.Label(info_frame, text="⏱️ 60秒",
                                              font=("微软雅黑", 18, "bold"), bg="#FFE4E1", fg="#DC143C")
        self.challenge_time_label.pack(side=tk.LEFT, padx=20)
        
        self.challenge_score_label = tk.Label(info_frame, text="⭐ 0分",
                                               font=("微软雅黑", 16, "bold"), bg="#FFE4E1", fg="#FF6B6B")
        self.challenge_score_label.pack(side=tk.LEFT, padx=20)
        
        self.challenge_stats_label = tk.Label(info_frame, text="✅0 ❌0",
                                               font=("微软雅黑", 14), bg="#FFE4E1", fg="#666")
        self.challenge_stats_label.pack(side=tk.LEFT, padx=20)
        
        # 题目区域
        self.challenge_question = tk.Label(self.game_frame, text="", font=("Segoe UI Emoji", 80),
                                            bg="white", relief=tk.RAISED, bd=4, padx=30, pady=15)
        self.challenge_question.pack(pady=15)
        
        self.challenge_hint = tk.Label(self.game_frame, text="看图片，选汉字！越快越好！",
                                        font=("微软雅黑", 14), bg="#FFE4E1", fg="#888")
        self.challenge_hint.pack(pady=5)
        
        # 选项按钮
        self.challenge_frame = tk.Frame(self.game_frame, bg="#FFE4E1")
        self.challenge_frame.pack(pady=15)
        
        self.challenge_buttons = []
        colors = ["#FF6B6B", "#4ECDC4", "#45B7D1", "#96CEB4"]
        
        for i in range(4):
            btn = tk.Button(self.challenge_frame, text="", font=("楷体", 45, "bold"),
                           width=3, height=1, bg=colors[i], fg="white",
                           relief=tk.RAISED, bd=4, cursor="hand2",
                           command=lambda idx=i: self.challenge_answer(idx))
            btn.grid(row=0, column=i, padx=12)
            self.challenge_buttons.append(btn)
        
        self.speak("限时挑战开始！60秒内答对越多越好！", "+0%")
        self.window.after(1500, self.challenge_new_question)
        self.window.after(1000, self.challenge_tick)
    
    def challenge_tick(self):
        """倒计时"""
        if not self.challenge_running:
            return
        
        self.challenge_time -= 1
        self.challenge_time_label.config(text=f"⏱️ {self.challenge_time}秒")
        
        if self.challenge_time <= 10:
            self.challenge_time_label.config(fg="#FF0000")
        
        if self.challenge_time <= 0:
            self.challenge_end()
        else:
            self.window.after(1000, self.challenge_tick)
    
    def challenge_new_question(self):
        """新题目"""
        if not self.challenge_running:
            return
        
        # 使用自适应难度选择目标字
        self.challenge_target = self.get_adaptive_word()
        
        # 使用智能选项生成
        self.challenge_options = self.get_adaptive_options(self.challenge_target, 4)
        self.challenge_correct_idx = self.challenge_options.index(self.challenge_target)
        
        # 显示图片
        self.challenge_question.config(text=self.challenge_target[2])
        
        # 更新选项
        colors = ["#FF6B6B", "#4ECDC4", "#45B7D1", "#96CEB4"]
        for i, btn in enumerate(self.challenge_buttons):
            btn.config(text=self.challenge_options[i][0], bg=colors[i], state=tk.NORMAL)
        
        self.challenge_hint.config(text="快选！", fg="#888")
    
    def challenge_answer(self, idx):
        """回答问题"""
        if not self.challenge_running:
            return
        
        # 禁用按钮
        for btn in self.challenge_buttons:
            btn.config(state=tk.DISABLED)
        
        if idx == self.challenge_correct_idx:
            # 答对
            self.challenge_correct += 1
            self.challenge_score += 10
            self.score += 10
            self.challenge_buttons[idx].config(bg="#32CD32")
            self.challenge_hint.config(text="✅ 对！", fg="#32CD32")
        else:
            # 答错
            self.challenge_wrong += 1
            self.challenge_buttons[idx].config(bg="#808080")
            self.challenge_buttons[self.challenge_correct_idx].config(bg="#32CD32")
            self.challenge_hint.config(text="❌ 错！", fg="#FF6B6B")
        
        self.challenge_score_label.config(text=f"⭐ {self.challenge_score}分")
        self.challenge_stats_label.config(text=f"✅{self.challenge_correct} ❌{self.challenge_wrong}")
        
        # 0.8秒后下一题（快节奏）
        self.window.after(800, self.challenge_new_question)
    
    def challenge_end(self):
        """挑战结束"""
        self.challenge_running = False
        
        for btn in self.challenge_buttons:
            btn.config(state=tk.DISABLED)
        
        total = self.challenge_correct + self.challenge_wrong
        accuracy = int(self.challenge_correct / total * 100) if total > 0 else 0
        
        if self.challenge_score >= 100:
            result = "🏆 超级厉害！识字小天才！"
        elif self.challenge_score >= 70:
            result = "🌟 真棒！乐乐很厉害！"
        elif self.challenge_score >= 40:
            result = "👍 不错哦！继续加油！"
        else:
            result = "💪 下次会更好！"
        
        self.challenge_hint.config(
            text=f"⏰ 时间到！答对{self.challenge_correct}题，正确率{accuracy}%，得分{self.challenge_score}！{result}",
            fg="#DC143C")
        self.speak(f"时间到！乐乐答对了{self.challenge_correct}题，得了{self.challenge_score}分！{result}", "+0%")
        
        self.window.after(5000, self.create_main_menu)
    
    # =====================================================
    # 笔顺动画模式
    # =====================================================
    def start_stroke(self):
        """笔顺动画 - 学习汉字书写"""
        self.clear_game_area("#FFF8DC")
        self.stroke_index = 0
        self.stroke_current_stroke = 0
        self.stroke_animating = False
        
        # 标题
        tk.Label(self.game_frame, text="✏️ 笔顺动画", font=("微软雅黑", 26, "bold"),
                 bg="#FFF8DC", fg="#FF9800").pack(pady=5)
        tk.Label(self.game_frame, text="看动画学写字，跟着笔顺一起写！",
                 font=("微软雅黑", 12), bg="#FFF8DC", fg="#666").pack(pady=5)
        
        # 进度显示
        self.stroke_progress = tk.Label(self.game_frame, text="", font=("微软雅黑", 12),
                                         bg="#FFF8DC", fg="#666")
        self.stroke_progress.pack(pady=5)
        
        # 主显示区域
        display_frame = tk.Frame(self.game_frame, bg="#FFF8DC")
        display_frame.pack(pady=10)
        
        # 左侧：汉字信息
        info_frame = tk.Frame(display_frame, bg="white", relief=tk.RAISED, bd=3)
        info_frame.pack(side=tk.LEFT, padx=20)
        
        self.stroke_char_label = tk.Label(info_frame, text="", font=("楷体", 80, "bold"),
                                           bg="white", fg="#FF6B6B", width=3, height=2)
        self.stroke_char_label.pack(pady=10, padx=20)
        
        self.stroke_pinyin_label = tk.Label(info_frame, text="", font=("Arial", 20),
                                             bg="white", fg="#4ECDC4")
        self.stroke_pinyin_label.pack(pady=5)
        
        self.stroke_emoji_label = tk.Label(info_frame, text="", font=("Segoe UI Emoji", 40),
                                            bg="white")
        self.stroke_emoji_label.pack(pady=5)
        
        # 右侧：笔顺画布
        canvas_frame = tk.Frame(display_frame, bg="#8B4513", relief=tk.RAISED, bd=4)
        canvas_frame.pack(side=tk.LEFT, padx=20)
        
        self.stroke_canvas = tk.Canvas(canvas_frame, width=200, height=200, bg="#FFFACD",
                                        highlightthickness=0)
        self.stroke_canvas.pack(padx=5, pady=5)
        
        # 笔画信息
        self.stroke_info = tk.Label(self.game_frame, text="", font=("微软雅黑", 14),
                                     bg="#FFF8DC", fg="#333")
        self.stroke_info.pack(pady=10)
        
        # 控制按钮
        btn_frame = tk.Frame(self.game_frame, bg="#FFF8DC")
        btn_frame.pack(pady=15)
        
        tk.Button(btn_frame, text="⬅️ 上一个", font=("微软雅黑", 11), bg="#45B7D1", fg="white",
                  width=10, height=2, command=self.stroke_prev).pack(side=tk.LEFT, padx=8)
        tk.Button(btn_frame, text="▶️ 播放笔顺", font=("微软雅黑", 11), bg="#4CAF50", fg="white",
                  width=10, height=2, command=self.stroke_play).pack(side=tk.LEFT, padx=8)
        tk.Button(btn_frame, text="🔄 重播", font=("微软雅黑", 11), bg="#FF9800", fg="white",
                  width=10, height=2, command=self.stroke_replay).pack(side=tk.LEFT, padx=8)
        tk.Button(btn_frame, text="下一个 ➡️", font=("微软雅黑", 11), bg="#45B7D1", fg="white",
                  width=10, height=2, command=self.stroke_next).pack(side=tk.LEFT, padx=8)
        
        # 提示
        tk.Label(self.game_frame, text="💡 提示：有笔顺数据的字会显示动画，其他字显示田字格",
                 font=("微软雅黑", 10), bg="#FFF8DC", fg="#999").pack(pady=10)
        
        self.stroke_show_char()
        self.speak("笔顺动画开始！看动画学写字！", "+0%")
    
    def stroke_show_char(self):
        """显示当前汉字"""
        w = self.words[self.stroke_index]
        char = w[0]
        
        self.stroke_char_label.config(text=char)
        self.stroke_pinyin_label.config(text=w[1])
        self.stroke_emoji_label.config(text=w[2])
        self.stroke_progress.config(text=f"第 {self.stroke_index + 1} / {len(self.words)} 个字")
        
        # 清空画布并绘制田字格
        self.stroke_draw_grid()
        
        # 检查是否有笔顺数据
        if char in STROKE_DATA:
            strokes = STROKE_DATA[char]
            self.stroke_info.config(text=f'📝 "{char}" 共 {len(strokes)} 笔，点击播放看笔顺！')
        else:
            self.stroke_info.config(text=f'📝 "{char}" 暂无笔顺数据，请在田字格中练习！')
            # 在画布中央显示汉字轮廓
            self.stroke_canvas.create_text(100, 100, text=char, font=("楷体", 100),
                                            fill="#DDD", tags="char_outline")
        
        self.speak(f"这个字是，{char}，{w[4]}", "-10%")
    
    def stroke_draw_grid(self):
        """绘制田字格"""
        self.stroke_canvas.delete("all")
        
        # 外框
        self.stroke_canvas.create_rectangle(10, 10, 190, 190, outline="#8B4513", width=3)
        
        # 中间十字虚线
        self.stroke_canvas.create_line(100, 10, 100, 190, fill="#DEB887", dash=(5, 3))
        self.stroke_canvas.create_line(10, 100, 190, 100, fill="#DEB887", dash=(5, 3))
        
        # 对角虚线
        self.stroke_canvas.create_line(10, 10, 190, 190, fill="#DEB887", dash=(5, 3))
        self.stroke_canvas.create_line(190, 10, 10, 190, fill="#DEB887", dash=(5, 3))
    
    def stroke_play(self):
        """播放笔顺动画"""
        if self.stroke_animating:
            return
        
        w = self.words[self.stroke_index]
        char = w[0]
        
        if char not in STROKE_DATA:
            self.speak("这个字暂时没有笔顺动画，请在田字格中练习！", "+0%")
            return
        
        self.stroke_animating = True
        self.stroke_current_stroke = 0
        self.stroke_draw_grid()
        self.stroke_animate_next()
    
    def stroke_animate_next(self):
        """动画绘制下一笔"""
        w = self.words[self.stroke_index]
        char = w[0]
        
        if char not in STROKE_DATA:
            self.stroke_animating = False
            return
        
        strokes = STROKE_DATA[char]
        
        if self.stroke_current_stroke >= len(strokes):
            self.stroke_animating = False
            self.stroke_info.config(text=f'✅ "{char}" 写完了！共 {len(strokes)} 笔')
            self.speak(f"写完了！{char}，共{len(strokes)}笔", "+0%")
            return
        
        # 获取当前笔画
        stroke = strokes[self.stroke_current_stroke]
        
        # 动画绘制笔画
        self.stroke_animate_stroke(stroke, 0)
    
    def stroke_animate_stroke(self, stroke, point_idx):
        """动画绘制单个笔画"""
        if not self.stroke_animating:
            return
        
        if point_idx >= len(stroke) - 1:
            # 当前笔画完成，进入下一笔
            self.stroke_current_stroke += 1
            self.stroke_info.config(text=f"📝 第 {self.stroke_current_stroke} 笔完成...")
            self.window.after(500, self.stroke_animate_next)
            return
        
        # 绘制线段
        x1, y1 = stroke[point_idx]
        x2, y2 = stroke[point_idx + 1]
        
        # 使用红色绘制当前笔画
        self.stroke_canvas.create_line(x1, y1, x2, y2, fill="#DC143C", width=8,
                                        capstyle=tk.ROUND, tags="stroke")
        
        # 继续绘制
        self.window.after(100, lambda: self.stroke_animate_stroke(stroke, point_idx + 1))
    
    def stroke_replay(self):
        """重播笔顺"""
        self.stroke_animating = False
        self.window.after(100, self.stroke_play)
    
    def stroke_next(self):
        """下一个字"""
        self.stroke_animating = False
        self.stroke_index = (self.stroke_index + 1) % len(self.words)
        self.stroke_show_char()
    
    def stroke_prev(self):
        """上一个字"""
        self.stroke_animating = False
        self.stroke_index = (self.stroke_index - 1) % len(self.words)
        self.stroke_show_char()
    
    # =====================================================
    # 故事模式 - 边听故事边认字
    # =====================================================
    def start_story_mode(self):
        """故事模式 - 用学过的字编成小故事"""
        self.clear_game_area("#FFF3E0")
        self.story_score = 0
        self.story_index = 0
        self.story_char_index = 0
        self.story_playing = False
        
        # 预设故事模板（使用字库中的字）
        self.stories = self.generate_stories()
        
        # 标题
        if THEME_AVAILABLE:
            title_canvas = tk.Canvas(self.game_frame, width=700, height=70, bg="#FFF3E0", highlightthickness=0)
            title_canvas.pack(pady=5)
            title_canvas.create_text(350, 22, text="📖 故事小课堂 📖", font=("微软雅黑", 24, "bold"), fill="#8BC34A")
            title_canvas.create_text(350, 52, text="听故事，认汉字，快乐学习！", font=("微软雅黑", 11), fill="#666")
            ThemeDrawings.draw_puppy_skye(title_canvas, 80, 40, 0.4)
            ThemeDrawings.draw_puppy_everest(title_canvas, 620, 40, 0.4)
        else:
            tk.Label(self.game_frame, text="📖 故事小课堂", font=("微软雅黑", 26, "bold"),
                     bg="#FFF3E0", fg="#8BC34A").pack(pady=5)
        
        self.story_score_label = tk.Label(self.game_frame, text="⭐ 得分: 0",
                                           font=("微软雅黑", 14), bg="#FFF3E0", fg="#666")
        self.story_score_label.pack(pady=5)
        
        # 故事选择区
        select_frame = tk.Frame(self.game_frame, bg="#FFF3E0")
        select_frame.pack(pady=10)
        
        tk.Label(select_frame, text="选择故事：", font=("微软雅黑", 12),
                 bg="#FFF3E0").pack(side=tk.LEFT, padx=5)
        
        self.story_var = tk.StringVar(value="0")
        for i, story in enumerate(self.stories[:4]):  # 最多显示4个故事
            tk.Radiobutton(select_frame, text=story["title"], variable=self.story_var,
                          value=str(i), font=("微软雅黑", 11), bg="#FFF3E0",
                          command=self.story_select).pack(side=tk.LEFT, padx=10)
        
        # 故事显示区
        story_frame = tk.Frame(self.game_frame, bg="white", relief=tk.RAISED, bd=3)
        story_frame.pack(pady=15, padx=30, fill=tk.X)
        
        self.story_title_label = tk.Label(story_frame, text="", font=("微软雅黑", 18, "bold"),
                                           bg="white", fg="#8BC34A")
        self.story_title_label.pack(pady=10)
        
        # 故事内容（带高亮汉字）
        self.story_text_frame = tk.Frame(story_frame, bg="white")
        self.story_text_frame.pack(pady=10, padx=20)
        
        self.story_content_label = tk.Label(self.story_text_frame, text="", font=("微软雅黑", 16),
                                             bg="white", fg="#333", wraplength=600, justify=tk.LEFT)
        self.story_content_label.pack()
        
        # 当前学习的字
        highlight_frame = tk.Frame(story_frame, bg="#E8F5E9", relief=tk.GROOVE, bd=2)
        highlight_frame.pack(pady=10, padx=20, fill=tk.X)
        
        tk.Label(highlight_frame, text="📝 当前学习：", font=("微软雅黑", 11),
                 bg="#E8F5E9", fg="#666").pack(side=tk.LEFT, padx=10, pady=8)
        
        self.story_char_label = tk.Label(highlight_frame, text="", font=("楷体", 50, "bold"),
                                          bg="#E8F5E9", fg="#FF6B6B")
        self.story_char_label.pack(side=tk.LEFT, padx=10)
        
        self.story_pinyin_label = tk.Label(highlight_frame, text="", font=("Arial", 16),
                                            bg="#E8F5E9", fg="#4ECDC4")
        self.story_pinyin_label.pack(side=tk.LEFT, padx=10)
        
        self.story_emoji_label = tk.Label(highlight_frame, text="", font=("Segoe UI Emoji", 30),
                                           bg="#E8F5E9")
        self.story_emoji_label.pack(side=tk.LEFT, padx=10)
        
        # 控制按钮
        btn_frame = tk.Frame(self.game_frame, bg="#FFF3E0")
        btn_frame.pack(pady=15)
        
        tk.Button(btn_frame, text="▶️ 播放故事", font=("微软雅黑", 12), bg="#4CAF50", fg="white",
                  width=12, height=2, command=self.story_play).pack(side=tk.LEFT, padx=8)
        tk.Button(btn_frame, text="⏸️ 暂停", font=("微软雅黑", 12), bg="#FF9800", fg="white",
                  width=10, height=2, command=self.story_pause).pack(side=tk.LEFT, padx=8)
        tk.Button(btn_frame, text="🔊 读当前字", font=("微软雅黑", 12), bg="#2196F3", fg="white",
                  width=10, height=2, command=self.story_speak_char).pack(side=tk.LEFT, padx=8)
        tk.Button(btn_frame, text="➡️ 下一个字", font=("微软雅黑", 12), bg="#9C27B0", fg="white",
                  width=10, height=2, command=self.story_next_char).pack(side=tk.LEFT, padx=8)
        
        # 答题区
        quiz_frame = tk.Frame(self.game_frame, bg="#FFF3E0")
        quiz_frame.pack(pady=10)
        
        tk.Label(quiz_frame, text="🎯 小测验：这个字念什么？", font=("微软雅黑", 12),
                 bg="#FFF3E0", fg="#666").pack(pady=5)
        
        self.story_quiz_frame = tk.Frame(quiz_frame, bg="#FFF3E0")
        self.story_quiz_frame.pack(pady=5)
        
        self.story_quiz_buttons = []
        colors = ["#FF6B6B", "#4ECDC4", "#45B7D1", "#96CEB4"]
        for i in range(4):
            btn = tk.Button(self.story_quiz_frame, text="", font=("微软雅黑", 12),
                           width=10, height=1, bg=colors[i], fg="white",
                           relief=tk.RAISED, bd=3, cursor="hand2",
                           command=lambda idx=i: self.story_check_answer(idx))
            btn.pack(side=tk.LEFT, padx=8)
            self.story_quiz_buttons.append(btn)
        
        self.story_quiz_hint = tk.Label(quiz_frame, text="", font=("微软雅黑", 12),
                                         bg="#FFF3E0")
        self.story_quiz_hint.pack(pady=5)
        
        # 初始化显示
        self.story_select()
        self.speak("故事模式开始！选一个故事，边听边学汉字！", "+0%")
    
    def generate_stories(self):
        """根据字库生成故事"""
        # 获取字库中的字
        char_dict = {w[0]: w for w in self.words}
        
        # 预设故事模板
        stories = [
            {
                "title": "🌞 美好的一天",
                "template": "今{天}天气真好，{日}出东方，金色的阳光照在大地上。小鸟在{天}空飞翔，{风}儿轻轻吹。乐乐和{爸}{爸}、{妈}{妈}一起去公园{玩}。",
                "chars": ["天", "日", "天", "风", "爸", "爸", "妈", "妈", "玩"]
            },
            {
                "title": "🏠 温暖的家",
                "template": "乐乐的家{里}真温暖。{爸}{爸}在{看}书，{妈}{妈}在做{饭}。乐乐是个{好}孩子，{自}己收拾玩具。{姐}{姐}说：你真棒！",
                "chars": ["里", "爸", "爸", "看", "妈", "妈", "饭", "好", "自", "姐", "姐"]
            },
            {
                "title": "🌳 大自然",
                "template": "{木}头可以做家具，{树}上有小鸟。{水}里有小鱼，{火}车跑得快。{土}{地}上长着小草，{电}闪雷鸣真壮观！",
                "chars": ["木", "树", "水", "火", "土", "地", "电"]
            },
            {
                "title": "🔢 数字歌",
                "template": "{一}二{三}{四}{五}，上山打老虎。老虎不在家，打到小松鼠。松鼠有几只？让我数{一}数。{一}{三}{五}，真有趣！",
                "chars": ["一", "三", "四", "五", "一", "一", "三", "五"]
            },
            {
                "title": "👨‍👩‍👧 我的家人",
                "template": "我有一个幸福的家。{爸}{爸}很高大，{妈}{妈}很温柔。{姐}{姐}带我{玩}，{叔}{叔}给我买玩具。{姑}{姑}来{看}我，大家都爱乐乐！",
                "chars": ["爸", "爸", "妈", "妈", "姐", "姐", "玩", "叔", "叔", "姑", "姑", "看"]
            },
        ]
        
        # 过滤出字库中有的字
        valid_stories = []
        for story in stories:
            valid_chars = [c for c in story["chars"] if c in char_dict]
            if len(valid_chars) >= 3:  # 至少有3个有效字
                story["valid_chars"] = valid_chars
                story["char_data"] = [char_dict[c] for c in valid_chars if c in char_dict]
                valid_stories.append(story)
        
        return valid_stories if valid_stories else [stories[0]]  # 至少返回一个故事
    
    def story_select(self):
        """选择故事"""
        idx = int(self.story_var.get())
        if idx < len(self.stories):
            self.story_index = idx
            self.story_char_index = 0
            story = self.stories[idx]
            
            self.story_title_label.config(text=story["title"])
            
            # 处理故事文本，高亮显示汉字
            text = story["template"]
            # 移除标记符号显示纯文本
            display_text = text.replace("{", "").replace("}", "")
            self.story_content_label.config(text=display_text)
            
            # 显示第一个字
            self.story_show_char()
    
    def story_show_char(self):
        """显示当前学习的字"""
        story = self.stories[self.story_index]
        chars = story.get("char_data", [])
        
        if not chars or self.story_char_index >= len(chars):
            self.story_char_label.config(text="✓")
            self.story_pinyin_label.config(text="学完了！")
            self.story_emoji_label.config(text="🎉")
            for btn in self.story_quiz_buttons:
                btn.config(state=tk.DISABLED)
            return
        
        w = chars[self.story_char_index]
        self.story_current_word = w
        
        self.story_char_label.config(text=w[0])
        self.story_pinyin_label.config(text=w[1])
        self.story_emoji_label.config(text=w[2])
        
        # 更新测验选项
        self.story_update_quiz()
    
    def story_update_quiz(self):
        """更新测验选项"""
        if not hasattr(self, 'story_current_word'):
            return
        
        w = self.story_current_word
        
        # 生成选项（正确拼音 + 3个干扰项）
        correct_pinyin = w[1]
        
        # 获取其他字的拼音作为干扰项
        other_pinyins = [word[1] for word in self.words if word[1] != correct_pinyin]
        other_pinyins = list(set(other_pinyins))  # 去重
        
        if len(other_pinyins) >= 3:
            distractors = random.sample(other_pinyins, 3)
        else:
            distractors = other_pinyins + ["?"] * (3 - len(other_pinyins))
        
        options = [correct_pinyin] + distractors
        random.shuffle(options)
        self.story_correct_idx = options.index(correct_pinyin)
        
        colors = ["#FF6B6B", "#4ECDC4", "#45B7D1", "#96CEB4"]
        for i, btn in enumerate(self.story_quiz_buttons):
            btn.config(text=options[i], bg=colors[i], state=tk.NORMAL)
        
        self.story_quiz_hint.config(text="", fg="#666")
    
    def story_check_answer(self, idx):
        """检查答案"""
        if idx == self.story_correct_idx:
            self.story_score += 10
            self.score += 10
            self.story_score_label.config(text=f"⭐ 得分: {self.story_score}")
            self.story_quiz_hint.config(text="🎉 答对了！", fg="#4CAF50")
            self.story_quiz_buttons[idx].config(bg="#4CAF50")
            
            # 记录结果
            self.record_result(True, {"question": f"故事模式:{self.story_current_word[0]}", 
                                      "answer": self.story_current_word[0]})
            self.speak_praise()
            
            # 自动进入下一个字
            self.window.after(2000, self.story_next_char)
        else:
            self.story_quiz_hint.config(text=f"😅 是 {self.story_current_word[1]} 哦！", fg="#FF6B6B")
            self.story_quiz_buttons[idx].config(bg="#808080")
            self.story_quiz_buttons[self.story_correct_idx].config(bg="#4CAF50")
            
            self.record_result(False, {"question": f"故事模式:{self.story_current_word[0]}", 
                                       "answer": self.story_current_word[0]})
            self.speak_encourage()
        
        for btn in self.story_quiz_buttons:
            btn.config(state=tk.DISABLED)
    
    def story_play(self):
        """播放故事"""
        story = self.stories[self.story_index]
        text = story["template"].replace("{", "").replace("}", "")
        self.speak(text, "-20%")
    
    def story_pause(self):
        """暂停播放"""
        try:
            pygame.mixer.music.stop()
        except:
            pass
    
    def story_speak_char(self):
        """朗读当前字"""
        if hasattr(self, 'story_current_word'):
            w = self.story_current_word
            self.speak(f"{w[0]}，{w[0]}，{w[4]}", "-10%")
    
    def story_next_char(self):
        """下一个字"""
        story = self.stories[self.story_index]
        chars = story.get("char_data", [])
        
        self.story_char_index += 1
        if self.story_char_index >= len(chars):
            # 故事学完了
            self.story_char_label.config(text="🎉")
            self.story_pinyin_label.config(text="太棒了！")
            self.story_emoji_label.config(text="")
            self.story_quiz_hint.config(text=f"🏆 故事学完了！得分：{self.story_score}", fg="#8BC34A")
            self.speak(f"太棒了！故事学完了，乐乐得了{self.story_score}分！", "+0%")
            for btn in self.story_quiz_buttons:
                btn.config(state=tk.DISABLED)
        else:
            self.story_show_char()
            self.story_speak_char()
    
    # =====================================================
    # 亲子互动模式
    # =====================================================
    def start_parent_mode(self):
        """亲子互动模式 - 家长出题，孩子答题"""
        self.clear_game_area("#E8F5E9")
        self.parent_score = 0
        self.parent_questions = []
        self.parent_current_q = 0
        self.parent_mode = "setup"  # setup, quiz, result
        
        # 标题
        tk.Label(self.game_frame, text="👨‍👩‍👧 亲子互动", font=("微软雅黑", 26, "bold"),
                 bg="#E8F5E9", fg="#E91E63").pack(pady=5)
        
        self.parent_subtitle = tk.Label(self.game_frame, text="家长出题，宝宝答题，一起学习！",
                                         font=("微软雅黑", 12), bg="#E8F5E9", fg="#666")
        self.parent_subtitle.pack(pady=5)
        
        # 主内容区
        self.parent_content = tk.Frame(self.game_frame, bg="#E8F5E9")
        self.parent_content.pack(fill=tk.BOTH, expand=True, pady=10)
        
        self.parent_show_setup()
    
    def parent_show_setup(self):
        """显示出题设置界面"""
        for widget in self.parent_content.winfo_children():
            widget.destroy()
        
        self.parent_mode = "setup"
        self.parent_subtitle.config(text="👨‍👩‍👧 家长选择要考的汉字")
        
        # 说明
        tk.Label(self.parent_content, text="📝 请家长选择要考宝宝的汉字（点击选中/取消）",
                 font=("微软雅黑", 13), bg="#E8F5E9", fg="#333").pack(pady=10)
        
        # 汉字选择区
        select_frame = tk.Frame(self.parent_content, bg="white", relief=tk.RAISED, bd=2)
        select_frame.pack(pady=10, padx=20)
        
        self.parent_selected = set()
        self.parent_char_buttons = {}
        
        # 显示所有汉字供选择
        chars_per_row = 8
        for i, w in enumerate(self.words):
            row = i // chars_per_row
            col = i % chars_per_row
            
            char = w[0]
            btn = tk.Button(select_frame, text=char, font=("楷体", 24, "bold"),
                           width=3, height=1, bg="#E0E0E0", fg="#333",
                           relief=tk.RAISED, bd=2, cursor="hand2",
                           command=lambda c=char: self.parent_toggle_char(c))
            btn.grid(row=row, column=col, padx=5, pady=5)
            self.parent_char_buttons[char] = btn
        
        # 快捷选择按钮
        quick_frame = tk.Frame(self.parent_content, bg="#E8F5E9")
        quick_frame.pack(pady=10)
        
        tk.Button(quick_frame, text="全选", font=("微软雅黑", 10), bg="#4CAF50", fg="white",
                  command=self.parent_select_all).pack(side=tk.LEFT, padx=5)
        tk.Button(quick_frame, text="清空", font=("微软雅黑", 10), bg="#FF5722", fg="white",
                  command=self.parent_clear_all).pack(side=tk.LEFT, padx=5)
        tk.Button(quick_frame, text="随机5个", font=("微软雅黑", 10), bg="#2196F3", fg="white",
                  command=lambda: self.parent_random_select(5)).pack(side=tk.LEFT, padx=5)
        tk.Button(quick_frame, text="随机10个", font=("微软雅黑", 10), bg="#9C27B0", fg="white",
                  command=lambda: self.parent_random_select(10)).pack(side=tk.LEFT, padx=5)
        
        # 已选数量
        self.parent_count_label = tk.Label(self.parent_content, text="已选择: 0 个字",
                                            font=("微软雅黑", 12), bg="#E8F5E9", fg="#666")
        self.parent_count_label.pack(pady=5)
        
        # 题目类型选择
        type_frame = tk.Frame(self.parent_content, bg="#E8F5E9")
        type_frame.pack(pady=10)
        
        tk.Label(type_frame, text="题目类型：", font=("微软雅黑", 11),
                 bg="#E8F5E9").pack(side=tk.LEFT)
        
        self.parent_quiz_type = tk.StringVar(value="picture")
        tk.Radiobutton(type_frame, text="🖼️ 看图选字", variable=self.parent_quiz_type,
                       value="picture", font=("微软雅黑", 10), bg="#E8F5E9").pack(side=tk.LEFT, padx=10)
        tk.Radiobutton(type_frame, text="👂 听音选字", variable=self.parent_quiz_type,
                       value="audio", font=("微软雅黑", 10), bg="#E8F5E9").pack(side=tk.LEFT, padx=10)
        tk.Radiobutton(type_frame, text="🔀 混合模式", variable=self.parent_quiz_type,
                       value="mixed", font=("微软雅黑", 10), bg="#E8F5E9").pack(side=tk.LEFT, padx=10)
        
        # 开始按钮
        tk.Button(self.parent_content, text="🎮 开始答题", font=("微软雅黑", 14, "bold"),
                  bg="#E91E63", fg="white", padx=30, pady=10,
                  command=self.parent_start_quiz).pack(pady=15)
        
        self.speak("亲子互动模式！请家长选择要考的汉字！", "+0%")
    
    def parent_toggle_char(self, char):
        """切换汉字选中状态"""
        btn = self.parent_char_buttons[char]
        if char in self.parent_selected:
            self.parent_selected.remove(char)
            btn.config(bg="#E0E0E0", fg="#333")
        else:
            self.parent_selected.add(char)
            btn.config(bg="#4CAF50", fg="white")
        
        self.parent_count_label.config(text=f"已选择: {len(self.parent_selected)} 个字")
    
    def parent_select_all(self):
        """全选"""
        for w in self.words:
            char = w[0]
            self.parent_selected.add(char)
            self.parent_char_buttons[char].config(bg="#4CAF50", fg="white")
        self.parent_count_label.config(text=f"已选择: {len(self.parent_selected)} 个字")
    
    def parent_clear_all(self):
        """清空选择"""
        for char in list(self.parent_selected):
            self.parent_char_buttons[char].config(bg="#E0E0E0", fg="#333")
        self.parent_selected.clear()
        self.parent_count_label.config(text="已选择: 0 个字")
    
    def parent_random_select(self, count):
        """随机选择"""
        self.parent_clear_all()
        chars = [w[0] for w in self.words]
        selected = random.sample(chars, min(count, len(chars)))
        for char in selected:
            self.parent_selected.add(char)
            self.parent_char_buttons[char].config(bg="#4CAF50", fg="white")
        self.parent_count_label.config(text=f"已选择: {len(self.parent_selected)} 个字")
    
    def parent_start_quiz(self):
        """开始答题"""
        if len(self.parent_selected) < 2:
            messagebox.showwarning("提示", "请至少选择2个汉字！")
            return
        
        # 准备题目
        self.parent_questions = []
        for w in self.words:
            if w[0] in self.parent_selected:
                self.parent_questions.append(w)
        
        random.shuffle(self.parent_questions)
        self.parent_current_q = 0
        self.parent_score = 0
        self.parent_correct = 0
        self.parent_wrong = 0
        
        self.parent_show_question()
    
    def parent_show_question(self):
        """显示题目"""
        for widget in self.parent_content.winfo_children():
            widget.destroy()
        
        self.parent_mode = "quiz"
        
        if self.parent_current_q >= len(self.parent_questions):
            self.parent_show_result()
            return
        
        q = self.parent_questions[self.parent_current_q]
        quiz_type = self.parent_quiz_type.get()
        
        if quiz_type == "mixed":
            quiz_type = random.choice(["picture", "audio"])
        
        # 进度
        self.parent_subtitle.config(
            text=f"第 {self.parent_current_q + 1} / {len(self.parent_questions)} 题  |  ⭐ {self.parent_score}分")
        
        if quiz_type == "picture":
            # 看图选字
            tk.Label(self.parent_content, text="🖼️ 看图片，选汉字！",
                     font=("微软雅黑", 16), bg="#E8F5E9", fg="#333").pack(pady=10)
            
            tk.Label(self.parent_content, text=q[2], font=("Segoe UI Emoji", 80),
                     bg="white", relief=tk.RAISED, bd=4, padx=30, pady=15).pack(pady=15)
        else:
            # 听音选字
            tk.Label(self.parent_content, text="👂 听声音，选汉字！",
                     font=("微软雅黑", 16), bg="#E8F5E9", fg="#333").pack(pady=10)
            
            tk.Button(self.parent_content, text="🔊 再听一遍", font=("微软雅黑", 12),
                      bg="#FF6B6B", fg="white",
                      command=lambda: self.speak(q[0], "-10%")).pack(pady=15)
            
            self.speak(f"请选择，{q[0]}", "-10%")
        
        # 选项
        others = random.sample([w for w in self.words if w != q], min(3, len(self.words) - 1))
        options = [q] + others
        random.shuffle(options)
        correct_idx = options.index(q)
        
        self.parent_hint = tk.Label(self.parent_content, text="", font=("微软雅黑", 16),
                                     bg="#E8F5E9")
        self.parent_hint.pack(pady=10)
        
        btn_frame = tk.Frame(self.parent_content, bg="#E8F5E9")
        btn_frame.pack(pady=15)
        
        self.parent_option_btns = []
        colors = ["#FF6B6B", "#4ECDC4", "#45B7D1", "#96CEB4"]
        
        for i, opt in enumerate(options):
            btn = tk.Button(btn_frame, text=opt[0], font=("楷体", 45, "bold"),
                           width=3, height=1, bg=colors[i], fg="white",
                           relief=tk.RAISED, bd=4, cursor="hand2",
                           command=lambda idx=i, ci=correct_idx, qw=q: self.parent_check_answer(idx, ci, qw))
            btn.grid(row=0, column=i, padx=12)
            self.parent_option_btns.append(btn)
    
    def parent_check_answer(self, idx, correct_idx, q):
        """检查答案"""
        for btn in self.parent_option_btns:
            btn.config(state=tk.DISABLED)
        
        if idx == correct_idx:
            self.parent_score += 10
            self.parent_correct += 1
            self.parent_option_btns[idx].config(bg="#32CD32")
            self.parent_hint.config(text=f"🎉 太棒了！是 {q[0]}！", fg="#32CD32")
            self.record_result(True, {"question": f"亲子互动:{q[0]}", "answer": q[0]})
            self.speak_praise()
        else:
            self.parent_wrong += 1
            self.parent_option_btns[idx].config(bg="#808080")
            self.parent_option_btns[correct_idx].config(bg="#32CD32")
            self.parent_hint.config(text=f"😅 是 {q[0]} 哦！", fg="#FF6B6B")
            self.record_result(False, {"question": f"亲子互动:{q[0]}", "answer": q[0]})
            self.speak_encourage()
        
        self.parent_current_q += 1
        self.window.after(3000, self.parent_show_question)
    
    def parent_show_result(self):
        """显示结果"""
        for widget in self.parent_content.winfo_children():
            widget.destroy()
        
        self.parent_mode = "result"
        self.parent_subtitle.config(text="🎉 答题完成！")
        
        total = self.parent_correct + self.parent_wrong
        accuracy = int(self.parent_correct / total * 100) if total > 0 else 0
        
        # 结果卡片
        result_frame = tk.Frame(self.parent_content, bg="white", relief=tk.RAISED, bd=4)
        result_frame.pack(pady=20, padx=50)
        
        if accuracy >= 90:
            emoji = "🏆"
            comment = "太厉害了！满分小天才！"
        elif accuracy >= 70:
            emoji = "🌟"
            comment = "真棒！继续加油！"
        elif accuracy >= 50:
            emoji = "👍"
            comment = "不错哦！再练练会更好！"
        else:
            emoji = "💪"
            comment = "加油！多练习就会进步！"
        
        tk.Label(result_frame, text=emoji, font=("Segoe UI Emoji", 60),
                 bg="white").pack(pady=15)
        tk.Label(result_frame, text=comment, font=("微软雅黑", 18, "bold"),
                 bg="white", fg="#E91E63").pack(pady=5)
        
        tk.Label(result_frame, text=f"答对: {self.parent_correct} 题  |  答错: {self.parent_wrong} 题",
                 font=("微软雅黑", 14), bg="white", fg="#666").pack(pady=5)
        tk.Label(result_frame, text=f"正确率: {accuracy}%  |  得分: {self.parent_score}",
                 font=("微软雅黑", 14), bg="white", fg="#666").pack(pady=5, padx=30)
        
        # 按钮
        btn_frame = tk.Frame(self.parent_content, bg="#E8F5E9")
        btn_frame.pack(pady=20)
        
        tk.Button(btn_frame, text="🔄 再来一次", font=("微软雅黑", 12), bg="#4CAF50", fg="white",
                  padx=20, command=self.parent_show_setup).pack(side=tk.LEFT, padx=10)
        tk.Button(btn_frame, text="🏠 返回主菜单", font=("微软雅黑", 12), bg="#2196F3", fg="white",
                  padx=20, command=self.create_main_menu).pack(side=tk.LEFT, padx=10)
        
        self.speak(f"答题完成！乐乐答对了{self.parent_correct}题，得了{self.parent_score}分！{comment}", "+0%")
    
    def run(self):
        self.window.mainloop()


if __name__ == "__main__":
    app = KidsLiteracyGame()
    app.run()
