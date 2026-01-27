# -*- coding: utf-8 -*-
"""
安全更新所有模块，添加：
1. 退出确认对话框
2. 休息提醒
3. 定时器管理
4. 等级选择功能
"""

import re

def update_pinyin_module():
    """更新拼音模块"""
    with open('kids_pinyin.py', 'r', encoding='utf-8') as f:
        content = f.read()
    
    # 1. 添加导入 - 在 voice_config_shared 导入后添加 create_rest_reminder
    old_import = '''try:
    from voice_config_shared import get_voice, get_praises, get_encourages
    VOICE_CONFIG_AVAILABLE = True
except ImportError:
    VOICE_CONFIG_AVAILABLE = False'''
    
    new_import = '''try:
    from voice_config_shared import get_voice, get_praises, get_encourages, create_rest_reminder
    VOICE_CONFIG_AVAILABLE = True
except ImportError:
    VOICE_CONFIG_AVAILABLE = False'''
    
    content = content.replace(old_import, new_import)
    
    # 2. 添加 atexit 导入
    if 'import atexit' not in content:
        content = content.replace('import time', 'import time\nimport atexit')
    
    # 3. 更新 __init__ 方法 - 添加定时器管理、休息提醒、窗口关闭处理
    old_init_end = '''        self.score = 0
        self.game_frame = None
        self.init_data()
        self.create_main_menu()'''
    
    new_init_end = '''        # 定时器管理
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
            "确定要退出拼音乐园吗？",
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
        total = len(self.vowels) + len(self.consonants)
        self.speak(f"已切换到等级{level}，共{total}个拼音！")
        self.create_main_menu()'''
    
    content = content.replace(old_init_end, new_init_end)

    # 4. 更新 init_data 方法 - 添加等级支持
    old_init_data = '''    def init_data(self):
        self.vowels = [
            ("a", "啊", "🍎", "阿姨的阿"),
            ("o", "哦", "⭕", "公鸡喔喔叫"),
            ("e", "鹅", "🦢", "白鹅的鹅"),
            ("i", "衣", "👔", "衣服的衣"),
            ("u", "乌", "🐦", "乌鸦的乌"),
            ("ü", "鱼", "🐟", "小鱼的鱼"),
        ]
        self.consonants = [
            ("b", "玻", "🪟", "玻璃的玻"),
            ("p", "坡", "⛰️", "山坡的坡"),
            ("m", "摸", "✋", "摸一摸"),
            ("f", "佛", "🙏", "大佛的佛"),
            ("d", "得", "✅", "得到的得"),
            ("t", "特", "⭐", "特别的特"),
        ]
        self.speech_id = 0
        self.praise_playing = False'''
    
    new_init_data = '''    def init_data(self):
        """根据等级初始化拼音数据"""
        # 等级1: 6个韵母 + 6个声母
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
        
        # 等级2: 增加更多声母
        CONSONANTS_L2 = [
            ("n", "呢", "👃", "你呢的呢"),
            ("l", "乐", "😊", "快乐的乐"),
            ("g", "哥", "👦", "哥哥的哥"),
            ("k", "科", "🔬", "科学的科"),
            ("h", "喝", "🥤", "喝水的喝"),
            ("j", "鸡", "🐔", "小鸡的鸡"),
        ]
        
        # 等级3: 增加更多声母和复韵母
        CONSONANTS_L3 = [
            ("q", "七", "7️⃣", "七个的七"),
            ("x", "西", "🌅", "西瓜的西"),
            ("zh", "知", "📚", "知道的知"),
            ("ch", "吃", "🍽️", "吃饭的吃"),
            ("sh", "十", "🔟", "十个的十"),
            ("r", "日", "☀️", "日出的日"),
        ]
        
        # 根据等级加载
        if self.level == 1:
            self.vowels = VOWELS_L1.copy()
            self.consonants = CONSONANTS_L1.copy()
        elif self.level == 2:
            self.vowels = VOWELS_L1.copy()
            self.consonants = CONSONANTS_L1 + CONSONANTS_L2
        else:
            self.vowels = VOWELS_L1.copy()
            self.consonants = CONSONANTS_L1 + CONSONANTS_L2 + CONSONANTS_L3
        
        self.speech_id = 0
        self.praise_playing = False'''
    
    content = content.replace(old_init_data, new_init_data)

    # 5. 更新主菜单 - 添加等级选择按钮
    old_menu = '''        score_frame = tk.Frame(main_frame, bg="#FF6B6B", relief=tk.RAISED, bd=3)
        score_frame.pack(pady=15)
        tk.Label(score_frame, text=f"⭐ 总分: {self.score} ⭐", font=("微软雅黑", 16, "bold"), bg="#FF6B6B", fg="white", padx=30, pady=8).pack()
        
        modes_frame = tk.Frame(main_frame, bg="#FFE4E1")'''
    
    new_menu = '''        # 等级选择和分数显示
        info_frame = tk.Frame(main_frame, bg="#FFE4E1")
        info_frame.pack(pady=10)
        
        # 等级选择
        level_frame = tk.Frame(info_frame, bg="#4ECDC4", relief=tk.RAISED, bd=3)
        level_frame.pack(side=tk.LEFT, padx=10)
        tk.Label(level_frame, text="📊 难度等级", font=("微软雅黑", 11, "bold"), bg="#4ECDC4", fg="white").pack(pady=3)
        level_btn_frame = tk.Frame(level_frame, bg="#4ECDC4")
        level_btn_frame.pack(pady=5, padx=10)
        
        level_colors = ["#96CEB4", "#FFD93D", "#FF6B6B"]
        level_texts = ["⭐ 入门\\n12个", "⭐⭐ 进阶\\n18个", "⭐⭐⭐ 挑战\\n24个"]
        for i in range(3):
            lv = i + 1
            bg = level_colors[i] if self.level != lv else "#333"
            fg = "white"
            btn = tk.Button(level_btn_frame, text=level_texts[i], font=("微软雅黑", 9, "bold"), 
                           bg=bg, fg=fg, width=8, height=2, relief=tk.RAISED, bd=2, cursor="hand2",
                           command=lambda l=lv: self.set_level(l))
            btn.pack(side=tk.LEFT, padx=3)
        
        # 分数显示
        score_frame = tk.Frame(info_frame, bg="#FF6B6B", relief=tk.RAISED, bd=3)
        score_frame.pack(side=tk.LEFT, padx=10)
        tk.Label(score_frame, text=f"⭐ 总分: {self.score} ⭐", font=("微软雅黑", 16, "bold"), bg="#FF6B6B", fg="white", padx=30, pady=8).pack()
        total = len(self.vowels) + len(self.consonants)
        tk.Label(score_frame, text=f"当前拼音: {total}个", font=("微软雅黑", 10), bg="#FF6B6B", fg="white").pack(pady=(0,5))
        
        modes_frame = tk.Frame(main_frame, bg="#FFE4E1")'''
    
    content = content.replace(old_menu, new_menu)
    
    # 6. 更新退出按钮
    old_exit = '''tk.Button(main_frame, text="👋 退出", font=("微软雅黑", 12), bg="#FF6B6B", fg="white", relief=tk.RAISED, bd=3, cursor="hand2", command=self.window.quit).pack(pady=10)'''
    new_exit = '''tk.Button(main_frame, text="👋 退出", font=("微软雅黑", 12), bg="#FF6B6B", fg="white", relief=tk.RAISED, bd=3, cursor="hand2", command=self.on_close_window).pack(pady=10)'''
    content = content.replace(old_exit, new_exit)
    
    # 7. 更新 clear_game_area - 添加定时器清理
    old_clear = '''    def clear_game_area(self, bg_color="#FFE4E1"):
        for widget in self.window.winfo_children():
            widget.destroy()'''
    
    new_clear = '''    def clear_game_area(self, bg_color="#FFE4E1"):
        # 清理所有待处理的定时器
        for timer_id in self.pending_timers:
            try:
                self.window.after_cancel(timer_id)
            except:
                pass
        self.pending_timers.clear()
        
        for widget in self.window.winfo_children():
            widget.destroy()'''
    
    content = content.replace(old_clear, new_clear)
    
    # 保存文件
    with open('kids_pinyin.py', 'w', encoding='utf-8') as f:
        f.write(content)
    
    print("✅ kids_pinyin.py 更新完成")


def update_math_module():
    """更新数学模块"""
    with open('kids_math.py', 'r', encoding='utf-8') as f:
        content = f.read()
    
    # 1. 添加导入
    old_import = '''try:
    from voice_config_shared import get_voice, get_praises, get_encourages
    VOICE_CONFIG_AVAILABLE = True
except ImportError:
    VOICE_CONFIG_AVAILABLE = False'''
    
    new_import = '''try:
    from voice_config_shared import get_voice, get_praises, get_encourages, create_rest_reminder
    VOICE_CONFIG_AVAILABLE = True
except ImportError:
    VOICE_CONFIG_AVAILABLE = False'''
    
    content = content.replace(old_import, new_import)
    
    # 2. 添加 atexit 导入
    if 'import atexit' not in content:
        content = content.replace('import time', 'import time\nimport atexit')
    
    # 3. 更新 __init__ 方法
    old_init_end = '''        # 总分
        self.score = 0
        self.game_frame = None
        
        # 初始化数据
        self.init_data()
        self.create_main_menu()'''
    
    new_init_end = '''        # 定时器管理
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
            "确定要退出数学乐园吗？",
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
        self.speak(f"已切换到等级{level}，数字范围1到{self.max_number}！")
        self.create_main_menu()'''
    
    content = content.replace(old_init_end, new_init_end)

    # 4. 更新 init_data 方法 - 添加等级支持
    old_init_data_start = '''    def init_data(self):
        """初始化数学数据"""
        # 数字1-20
        self.numbers = []
        chinese_nums = ["零","一","二","三","四","五","六","七","八","九","十",
                       "十一","十二","十三","十四","十五","十六","十七","十八","十九","二十"]
        for i in range(1, 21):'''
    
    new_init_data_start = '''    def init_data(self):
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
        for i in range(1, self.max_number + 1):'''
    
    content = content.replace(old_init_data_start, new_init_data_start)
    
    # 5. 更新主菜单 - 添加等级选择
    old_menu = '''        # 总分
        score_frame = tk.Frame(main_frame, bg="#4ECDC4", relief=tk.RAISED, bd=3)
        score_frame.pack(pady=15)
        tk.Label(score_frame, text=f"⭐ 总分: {self.score} ⭐", 
                 font=("微软雅黑", 16, "bold"), bg="#4ECDC4", fg="white",
                 padx=30, pady=8).pack()
        
        # 游戏模式
        modes_frame = tk.Frame(main_frame, bg="#E8F5E9")'''
    
    new_menu = '''        # 等级选择和分数显示
        info_frame = tk.Frame(main_frame, bg="#E8F5E9")
        info_frame.pack(pady=10)
        
        # 等级选择
        level_frame = tk.Frame(info_frame, bg="#45B7D1", relief=tk.RAISED, bd=3)
        level_frame.pack(side=tk.LEFT, padx=10)
        tk.Label(level_frame, text="📊 难度等级", font=("微软雅黑", 11, "bold"), bg="#45B7D1", fg="white").pack(pady=3)
        level_btn_frame = tk.Frame(level_frame, bg="#45B7D1")
        level_btn_frame.pack(pady=5, padx=10)
        
        level_colors = ["#96CEB4", "#FFD93D", "#FF6B6B"]
        level_texts = ["⭐ 入门\\n1-10", "⭐⭐ 进阶\\n1-15", "⭐⭐⭐ 挑战\\n1-20"]
        for i in range(3):
            lv = i + 1
            bg = level_colors[i] if self.level != lv else "#333"
            fg = "white"
            btn = tk.Button(level_btn_frame, text=level_texts[i], font=("微软雅黑", 9, "bold"), 
                           bg=bg, fg=fg, width=8, height=2, relief=tk.RAISED, bd=2, cursor="hand2",
                           command=lambda l=lv: self.set_level(l))
            btn.pack(side=tk.LEFT, padx=3)
        
        # 分数显示
        score_frame = tk.Frame(info_frame, bg="#4ECDC4", relief=tk.RAISED, bd=3)
        score_frame.pack(side=tk.LEFT, padx=10)
        tk.Label(score_frame, text=f"⭐ 总分: {self.score} ⭐", 
                 font=("微软雅黑", 16, "bold"), bg="#4ECDC4", fg="white",
                 padx=30, pady=8).pack()
        tk.Label(score_frame, text=f"数字范围: 1-{self.max_number}", font=("微软雅黑", 10), bg="#4ECDC4", fg="white").pack(pady=(0,5))
        
        # 游戏模式
        modes_frame = tk.Frame(main_frame, bg="#E8F5E9")'''
    
    content = content.replace(old_menu, new_menu)
    
    # 6. 更新退出按钮
    old_exit = '''tk.Button(main_frame, text="👋 退出", font=("微软雅黑", 12),
                  bg="#FF6B6B", fg="white", relief=tk.RAISED, bd=3,
                  cursor="hand2", command=self.window.quit).pack(pady=10)'''
    new_exit = '''tk.Button(main_frame, text="👋 退出", font=("微软雅黑", 12),
                  bg="#FF6B6B", fg="white", relief=tk.RAISED, bd=3,
                  cursor="hand2", command=self.on_close_window).pack(pady=10)'''
    content = content.replace(old_exit, new_exit)
    
    # 7. 更新 clear_game_area
    old_clear = '''    def clear_game_area(self, bg_color="#E8F5E9"):
        for widget in self.window.winfo_children():
            widget.destroy()'''
    
    new_clear = '''    def clear_game_area(self, bg_color="#E8F5E9"):
        # 清理所有待处理的定时器
        for timer_id in self.pending_timers:
            try:
                self.window.after_cancel(timer_id)
            except:
                pass
        self.pending_timers.clear()
        
        for widget in self.window.winfo_children():
            widget.destroy()'''
    
    content = content.replace(old_clear, new_clear)
    
    # 保存文件
    with open('kids_math.py', 'w', encoding='utf-8') as f:
        f.write(content)
    
    print("✅ kids_math.py 更新完成")


def update_english_module():
    """更新英语模块"""
    with open('kids_english.py', 'r', encoding='utf-8') as f:
        content = f.read()
    
    # 1. 添加导入
    old_import = '''try:
    from voice_config_shared import get_voice, get_praises, get_encourages
    VOICE_CONFIG_AVAILABLE = True
except ImportError:
    VOICE_CONFIG_AVAILABLE = False'''
    
    new_import = '''try:
    from voice_config_shared import get_voice, get_praises, get_encourages, create_rest_reminder
    VOICE_CONFIG_AVAILABLE = True
except ImportError:
    VOICE_CONFIG_AVAILABLE = False'''
    
    content = content.replace(old_import, new_import)
    
    # 2. 添加 atexit 导入
    if 'import atexit' not in content:
        content = content.replace('import time', 'import time\nimport atexit')
    
    # 3. 更新 __init__ 方法
    old_init_end = '''        self.score = 0
        self.game_frame = None
        self.init_data()
        self.create_main_menu()'''
    
    new_init_end = '''        # 定时器管理
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
        self.create_main_menu()'''
    
    content = content.replace(old_init_end, new_init_end)

    # 4. 更新 init_data 方法 - 添加等级支持
    old_init_data = '''    def init_data(self):
        self.letters = [
            ("A", "Apple", "🍎", "苹果"), ("B", "Ball", "⚽", "球"), ("C", "Cat", "🐱", "猫"),
            ("D", "Dog", "🐕", "狗"), ("E", "Elephant", "🐘", "大象"), ("F", "Fish", "🐟", "鱼"),
            ("G", "Grape", "🍇", "葡萄"), ("H", "House", "🏠", "房子"), ("I", "Ice cream", "🍦", "冰淇淋"),
            ("J", "Juice", "🧃", "果汁"), ("K", "Kite", "🪁", "风筝"), ("L", "Lion", "🦁", "狮子"),
        ]'''
    
    new_init_data = '''    def init_data(self):
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
            self.letters = LETTERS_L1 + LETTERS_L2 + LETTERS_L3'''
    
    content = content.replace(old_init_data, new_init_data)
    
    # 5. 更新主菜单 - 添加等级选择
    old_menu = '''        score_frame = tk.Frame(main_frame, bg="#45B7D1", relief=tk.RAISED, bd=3)
        score_frame.pack(pady=15)
        tk.Label(score_frame, text=f"⭐ 总分: {self.score} ⭐", font=("微软雅黑", 16, "bold"), bg="#45B7D1", fg="white", padx=30, pady=8).pack()
        modes_frame = tk.Frame(main_frame, bg="#E0F7FA")'''
    
    new_menu = '''        # 等级选择和分数显示
        info_frame = tk.Frame(main_frame, bg="#E0F7FA")
        info_frame.pack(pady=10)
        
        # 等级选择
        level_frame = tk.Frame(info_frame, bg="#4ECDC4", relief=tk.RAISED, bd=3)
        level_frame.pack(side=tk.LEFT, padx=10)
        tk.Label(level_frame, text="📊 难度等级", font=("微软雅黑", 11, "bold"), bg="#4ECDC4", fg="white").pack(pady=3)
        level_btn_frame = tk.Frame(level_frame, bg="#4ECDC4")
        level_btn_frame.pack(pady=5, padx=10)
        
        level_colors = ["#96CEB4", "#FFD93D", "#FF6B6B"]
        level_texts = ["⭐ 入门\\nA-L", "⭐⭐ 进阶\\nA-R", "⭐⭐⭐ 挑战\\nA-Z"]
        for i in range(3):
            lv = i + 1
            bg = level_colors[i] if self.level != lv else "#333"
            fg = "white"
            btn = tk.Button(level_btn_frame, text=level_texts[i], font=("微软雅黑", 9, "bold"), 
                           bg=bg, fg=fg, width=8, height=2, relief=tk.RAISED, bd=2, cursor="hand2",
                           command=lambda l=lv: self.set_level(l))
            btn.pack(side=tk.LEFT, padx=3)
        
        # 分数显示
        score_frame = tk.Frame(info_frame, bg="#45B7D1", relief=tk.RAISED, bd=3)
        score_frame.pack(side=tk.LEFT, padx=10)
        tk.Label(score_frame, text=f"⭐ 总分: {self.score} ⭐", font=("微软雅黑", 16, "bold"), bg="#45B7D1", fg="white", padx=30, pady=8).pack()
        tk.Label(score_frame, text=f"当前字母: {len(self.letters)}个", font=("微软雅黑", 10), bg="#45B7D1", fg="white").pack(pady=(0,5))
        
        modes_frame = tk.Frame(main_frame, bg="#E0F7FA")'''
    
    content = content.replace(old_menu, new_menu)
    
    # 6. 更新退出按钮
    old_exit = '''tk.Button(main_frame, text="👋 退出", font=("微软雅黑", 12), bg="#FF6B6B", fg="white", relief=tk.RAISED, bd=3, cursor="hand2", command=self.window.quit).pack(pady=10)'''
    new_exit = '''tk.Button(main_frame, text="👋 退出", font=("微软雅黑", 12), bg="#FF6B6B", fg="white", relief=tk.RAISED, bd=3, cursor="hand2", command=self.on_close_window).pack(pady=10)'''
    content = content.replace(old_exit, new_exit)
    
    # 7. 更新 clear_game_area
    old_clear = '''    def clear_game_area(self, bg_color="#E0F7FA"):
        for widget in self.window.winfo_children():
            widget.destroy()'''
    
    new_clear = '''    def clear_game_area(self, bg_color="#E0F7FA"):
        # 清理所有待处理的定时器
        for timer_id in self.pending_timers:
            try:
                self.window.after_cancel(timer_id)
            except:
                pass
        self.pending_timers.clear()
        
        for widget in self.window.winfo_children():
            widget.destroy()'''
    
    content = content.replace(old_clear, new_clear)
    
    # 保存文件
    with open('kids_english.py', 'w', encoding='utf-8') as f:
        f.write(content)
    
    print("✅ kids_english.py 更新完成")


def update_thinking_module():
    """更新思维模块"""
    with open('kids_thinking.py', 'r', encoding='utf-8') as f:
        content = f.read()
    
    # 1. 添加导入
    old_import = '''try:
    from voice_config_shared import get_voice, get_praises, get_encourages
    VOICE_CONFIG_AVAILABLE = True
except ImportError:
    VOICE_CONFIG_AVAILABLE = False'''
    
    new_import = '''try:
    from voice_config_shared import get_voice, get_praises, get_encourages, create_rest_reminder
    VOICE_CONFIG_AVAILABLE = True
except ImportError:
    VOICE_CONFIG_AVAILABLE = False'''
    
    content = content.replace(old_import, new_import)
    
    # 2. 添加 atexit 导入
    if 'import atexit' not in content:
        content = content.replace('import time', 'import time\nimport atexit')
    
    # 3. 更新 __init__ 方法
    old_init_end = '''        # 总分
        self.score = 0
        self.game_frame = None
        
        # 初始化数据
        self.init_data()
        self.create_main_menu()'''
    
    new_init_end = '''        # 定时器管理
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
        self.create_main_menu()'''
    
    content = content.replace(old_init_end, new_init_end)

    # 4. 更新主菜单 - 添加等级选择
    old_menu = '''        # 总分
        score_frame = tk.Frame(main_frame, bg="#9C27B0", relief=tk.RAISED, bd=3)
        score_frame.pack(pady=15)
        tk.Label(score_frame, text=f"⭐ 总分: {self.score} ⭐", 
                 font=("微软雅黑", 16, "bold"), bg="#9C27B0", fg="white",
                 padx=30, pady=8).pack()
        
        # 游戏模式
        modes_frame = tk.Frame(main_frame, bg="#F3E5F5")'''
    
    new_menu = '''        # 等级选择和分数显示
        info_frame = tk.Frame(main_frame, bg="#F3E5F5")
        info_frame.pack(pady=10)
        
        # 等级选择
        level_frame = tk.Frame(info_frame, bg="#4ECDC4", relief=tk.RAISED, bd=3)
        level_frame.pack(side=tk.LEFT, padx=10)
        tk.Label(level_frame, text="📊 难度等级", font=("微软雅黑", 11, "bold"), bg="#4ECDC4", fg="white").pack(pady=3)
        level_btn_frame = tk.Frame(level_frame, bg="#4ECDC4")
        level_btn_frame.pack(pady=5, padx=10)
        
        level_colors = ["#96CEB4", "#FFD93D", "#FF6B6B"]
        level_texts = ["⭐ 入门\\n简单", "⭐⭐ 进阶\\n中等", "⭐⭐⭐ 挑战\\n困难"]
        for i in range(3):
            lv = i + 1
            bg = level_colors[i] if self.level != lv else "#333"
            fg = "white"
            btn = tk.Button(level_btn_frame, text=level_texts[i], font=("微软雅黑", 9, "bold"), 
                           bg=bg, fg=fg, width=8, height=2, relief=tk.RAISED, bd=2, cursor="hand2",
                           command=lambda l=lv: self.set_level(l))
            btn.pack(side=tk.LEFT, padx=3)
        
        # 分数显示
        score_frame = tk.Frame(info_frame, bg="#9C27B0", relief=tk.RAISED, bd=3)
        score_frame.pack(side=tk.LEFT, padx=10)
        tk.Label(score_frame, text=f"⭐ 总分: {self.score} ⭐", 
                 font=("微软雅黑", 16, "bold"), bg="#9C27B0", fg="white",
                 padx=30, pady=8).pack()
        level_desc = ["简单", "中等", "困难"]
        tk.Label(score_frame, text=f"当前难度: {level_desc[self.level-1]}", font=("微软雅黑", 10), bg="#9C27B0", fg="white").pack(pady=(0,5))
        
        # 游戏模式
        modes_frame = tk.Frame(main_frame, bg="#F3E5F5")'''
    
    content = content.replace(old_menu, new_menu)
    
    # 5. 更新退出按钮
    old_exit = '''tk.Button(main_frame, text="👋 退出", font=("微软雅黑", 12),
                  bg="#FF6B6B", fg="white", relief=tk.RAISED, bd=3,
                  cursor="hand2", command=self.window.quit).pack(pady=10)'''
    new_exit = '''tk.Button(main_frame, text="👋 退出", font=("微软雅黑", 12),
                  bg="#FF6B6B", fg="white", relief=tk.RAISED, bd=3,
                  cursor="hand2", command=self.on_close_window).pack(pady=10)'''
    content = content.replace(old_exit, new_exit)
    
    # 6. 更新 clear_game_area
    old_clear = '''    def clear_game_area(self, bg_color="#F3E5F5"):
        for widget in self.window.winfo_children():
            widget.destroy()'''
    
    new_clear = '''    def clear_game_area(self, bg_color="#F3E5F5"):
        # 清理所有待处理的定时器
        for timer_id in self.pending_timers:
            try:
                self.window.after_cancel(timer_id)
            except:
                pass
        self.pending_timers.clear()
        
        for widget in self.window.winfo_children():
            widget.destroy()'''
    
    content = content.replace(old_clear, new_clear)
    
    # 保存文件
    with open('kids_thinking.py', 'w', encoding='utf-8') as f:
        f.write(content)
    
    print("✅ kids_thinking.py 更新完成")


if __name__ == "__main__":
    print("开始更新所有模块...")
    print()
    
    try:
        update_pinyin_module()
    except Exception as e:
        print(f"❌ 更新拼音模块失败: {e}")
    
    try:
        update_math_module()
    except Exception as e:
        print(f"❌ 更新数学模块失败: {e}")
    
    try:
        update_english_module()
    except Exception as e:
        print(f"❌ 更新英语模块失败: {e}")
    
    try:
        update_thinking_module()
    except Exception as e:
        print(f"❌ 更新思维模块失败: {e}")
    
    print()
    print("🎉 所有模块更新完成！")
