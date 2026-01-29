# -*- coding: utf-8 -*-
"""
乐乐数学乐园 - 汪汪队主题
适合4岁小朋友的数学启蒙
"""
import os
import sys

# 确保能找到模块
app_dir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.insert(0, app_dir)
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

# 必须在导入kivy之前配置字体
try:
    import font_config
    print("[math_app] 字体配置模块已加载")
except ImportError as e:
    print(f"[math_app] 字体配置导入失败: {e}")

import random
from kivy.app import App
from kivy.uix.screenmanager import ScreenManager, Screen
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.gridlayout import GridLayout
from kivy.uix.button import Button
from kivy.uix.label import Label
from kivy.uix.widget import Widget
from kivy.graphics import Color, Rectangle, Ellipse, Line, Triangle
from kivy.utils import get_color_from_hex
from kivy.metrics import dp, sp
from kivy.clock import Clock
from kivy.core.window import Window

# 导入音频模块
try:
    from audio_kivy import get_audio
    _audio = None
    def _get_audio():
        global _audio
        if _audio is None:
            _audio = get_audio()
        return _audio
    
    def speak(text):
        audio = _get_audio()
        if audio:
            audio.speak(text)
    
    def play_praise():
        audio = _get_audio()
        if audio:
            audio.play_praise()
    
    def play_encourage():
        audio = _get_audio()
        if audio:
            audio.play_encourage()
except ImportError:
    def get_audio(): return None
    def speak(text): print(f"[speak] {text}")
    def play_praise(): print("[praise]")
    def play_encourage(): print("[encourage]")

# 导入汪汪队装饰
try:
    from paw_patrol_theme import (
        PAW_COLORS, PawBadgeWidget, PawPrintWidget as PawPrint, BoneWidget,
        DogBowlWidget, DogHouseWidget,
        ChaseHeadWidget, MarshallHeadWidget, SkyeHeadWidget,
        RubbleHeadWidget, RockyHeadWidget, ZumaHeadWidget,
        animate_paw_bounce, animate_bone_spin, animate_badge_shine,
        create_paw_trail, create_puppy_celebration
    )
    PAW_PATROL_AVAILABLE = True
except ImportError:
    PAW_PATROL_AVAILABLE = False
    def draw_paw_print(canvas, x, y, size, color): pass

# 导入装饰动画
try:
    from decorations import (
        StarWidget, HeartWidget, SunWidget, CloudWidget, FlowerWidget,
        ButterflyWidget, BalloonWidget, CrownWidget, TrophyWidget, GiftBoxWidget,
        RainbowWidget, BirdWidget, FishWidget, CandyWidget, BeeWidget,
        animate_float, animate_rotate, animate_pulse, animate_heartbeat,
        animate_bounce, animate_twinkle, animate_swing,
        create_confetti_burst, create_star_burst, create_heart_burst,
        create_firework, create_celebration_scene
    )
    DECORATIONS_AVAILABLE = True
except ImportError:
    DECORATIONS_AVAILABLE = False
    def animate_star_burst(widget, x, y): pass


# ============================================================
# 工具函数
# ============================================================
def get_font_size(base_size):
    """根据屏幕大小调整字体"""
    scale = min(Window.width / 1200, Window.height / 800)
    return sp(base_size * max(0.7, min(1.3, scale)))

def get_padding():
    return dp(15)

def get_spacing():
    return dp(10)


# ============================================================
# 答对/答错动画效果
# ============================================================
def show_correct_effect(parent, x=None, y=None):
    """答对时的庆祝效果"""
    if not DECORATIONS_AVAILABLE:
        return
    if x is None:
        x = parent.center_x
    if y is None:
        y = parent.center_y
    # 随机选择一种效果
    effect = random.choice(['stars', 'confetti', 'hearts'])
    if effect == 'stars':
        create_star_burst(parent, x, y, count=8)
    elif effect == 'confetti':
        create_confetti_burst(parent, x, y, count=12)
    else:
        create_heart_burst(parent, x, y, count=6)

def show_firework_effect(parent):
    """烟花效果（用于大成功）"""
    if not DECORATIONS_AVAILABLE:
        return
    for i in range(3):
        x = random.randint(100, int(Window.width - 100))
        y = random.randint(200, int(Window.height - 100))
        Clock.schedule_once(lambda dt, px=x, py=y: create_firework(parent, px, py), i * 0.3)


# ============================================================
# 数学数据
# ============================================================
class MathData:
    """数学数据"""
    
    # 数字 1-20
    NUMBERS = {
        1: '一', 2: '二', 3: '三', 4: '四', 5: '五',
        6: '六', 7: '七', 8: '八', 9: '九', 10: '十',
        11: '十一', 12: '十二', 13: '十三', 14: '十四', 15: '十五',
        16: '十六', 17: '十七', 18: '十八', 19: '十九', 20: '二十'
    }
    
    # 形状
    SHAPES = [
        ('圆形', 'circle', '#FF6B6B'),
        ('三角形', 'triangle', '#4ECDC4'),
        ('正方形', 'square', '#45B7D1'),
        ('长方形', 'rectangle', '#96CEB4'),
        ('五角星', 'star', '#FFD93D'),
    ]
    
    @classmethod
    def get_chinese(cls, num):
        """获取数字的中文"""
        return cls.NUMBERS.get(num, str(num))


# ============================================================
# 主菜单
# ============================================================
class MathMenuScreen(Screen):
    """数学乐园主菜单"""
    
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.build_ui()
    
    def build_ui(self):
        layout = BoxLayout(orientation='vertical', padding=get_padding(), spacing=get_spacing())
        
        # 蓝色渐变背景
        with layout.canvas.before:
            Color(*get_color_from_hex('#E3F2FD'))
            self.bg = Rectangle(pos=layout.pos, size=layout.size)
        layout.bind(pos=lambda i,v: setattr(self.bg, 'pos', v),
                   size=lambda i,v: setattr(self.bg, 'size', v))
        
        # 标题
        title_box = BoxLayout(size_hint=(1, 0.15))
        self.title_label = Label(
            text='乐乐数学乐园',
            font_size=get_font_size(42),
            color=get_color_from_hex('#1565C0'),
            bold=True
        )
        title_box.add_widget(self.title_label)
        layout.add_widget(title_box)
        
        # 游戏按钮网格
        game_grid = GridLayout(cols=3, spacing=dp(15), size_hint=(1, 0.75), padding=dp(10))
        
        # 游戏列表: (图标, 名称, 描述, 颜色, 屏幕名, 狗狗)
        games = [
            ('1', '认数字', '跟阿奇学', '#1565C0', 'math_numbers', 'chase'),
            ('123', '数一数', '跟毛毛数', '#D32F2F', 'math_counting', 'marshall'),
            ('><', '比大小', '跟小砾比', '#FF8F00', 'math_compare', 'rubble'),
            ('+', '学加法', '跟路马算', '#00897B', 'math_addition', 'zuma'),
            ('○△', '认形状', '跟天天认', '#EC407A', 'math_shapes', 'skye'),
            ('★', '大闯关', '挑战赛', '#7B1FA2', 'math_challenge', 'all'),
        ]
        
        for icon, name, desc, color, screen, dog in games:
            btn = self.create_game_button(icon, name, desc, color, screen)
            game_grid.add_widget(btn)
        
        layout.add_widget(game_grid)
        
        # 底部返回按钮
        bottom = BoxLayout(size_hint=(1, 0.1))
        back_btn = Button(
            text='返回主菜单',
            font_size=get_font_size(20),
            size_hint=(0.3, 0.8),
            pos_hint={'center_x': 0.5},
            background_color=get_color_from_hex('#78909C'),
            background_normal=''
        )
        back_btn.bind(on_press=self.go_back)
        bottom.add_widget(Widget())
        bottom.add_widget(back_btn)
        bottom.add_widget(Widget())
        layout.add_widget(bottom)
        
        self.add_widget(layout)
    
    def create_game_button(self, icon, name, desc, color, screen):
        """创建游戏按钮"""
        btn_layout = BoxLayout(orientation='vertical', spacing=dp(5))
        
        # 按钮背景
        with btn_layout.canvas.before:
            Color(*get_color_from_hex(color))
            btn_layout.bg = Rectangle(pos=btn_layout.pos, size=btn_layout.size)
        btn_layout.bind(
            pos=lambda i,v: setattr(i.bg, 'pos', v),
            size=lambda i,v: setattr(i.bg, 'size', v)
        )
        
        # 图标
        icon_label = Label(
            text=icon,
            font_size=get_font_size(48),
            size_hint=(1, 0.5)
        )
        btn_layout.add_widget(icon_label)
        
        # 名称
        name_label = Label(
            text=name,
            font_size=get_font_size(24),
            bold=True,
            size_hint=(1, 0.3)
        )
        btn_layout.add_widget(name_label)
        
        # 描述
        desc_label = Label(
            text=desc,
            font_size=get_font_size(16),
            size_hint=(1, 0.2)
        )
        btn_layout.add_widget(desc_label)
        
        # 点击事件
        btn_layout.screen_name = screen
        btn_layout.bind(on_touch_down=self.on_game_touch)
        
        return btn_layout
    
    def on_game_touch(self, instance, touch):
        if instance.collide_point(*touch.pos):
            if hasattr(instance, 'screen_name'):
                self.manager.current = instance.screen_name
            return True
        return False
    
    def go_back(self, instance):
        """返回主菜单"""
        # 如果有主应用菜单，返回那里
        if 'main_menu' in self.manager.screen_names:
            self.manager.current = 'main_menu'
    
    def add_decorations(self):
        """添加装饰动画"""
        if not DECORATIONS_AVAILABLE:
            return
        
        self.deco_widgets = []
        self._update_deco_positions()
        
        # 绑定尺寸变化事件
        self.bind(size=self._update_deco_positions, pos=self._update_deco_positions)
    
    def _update_deco_positions(self, *args):
        """更新装饰位置"""
        if not DECORATIONS_AVAILABLE:
            return
        
        # 清除旧装饰
        if hasattr(self, 'deco_widgets'):
            for w in self.deco_widgets:
                try:
                    self.remove_widget(w)
                except:
                    pass
        
        self.deco_widgets = []
        w, h = self.size
        x, y = self.pos
        
        # 左上角太阳
        try:
            sun = SunWidget(size_hint=(None, None), size=(dp(55), dp(55)))
            sun.pos = (x + dp(10), y + h - dp(75))
            sun.opacity = 0.85
            self.add_widget(sun)
            self.deco_widgets.append(sun)
            animate_rotate(sun, duration=20)
        except: pass
        
        # 右上角云朵
        try:
            cloud = CloudWidget(size_hint=(None, None), size=(dp(65), dp(40)))
            cloud.pos = (x + w - dp(85), y + h - dp(65))
            cloud.opacity = 0.8
            self.add_widget(cloud)
            self.deco_widgets.append(cloud)
            animate_float(cloud, amplitude=8, duration=3)
        except: pass
        
        # 底部气球 - 均匀分布
        balloon_colors = [(1, 0.4, 0.4), (0.4, 0.8, 1), (1, 0.9, 0.3), (0.8, 0.5, 1)]
        balloon_spacing = (w - dp(200)) / 4
        for i in range(4):
            try:
                balloon = BalloonWidget(
                    color=balloon_colors[i],
                    size_hint=(None, None),
                    size=(dp(32), dp(42))
                )
                balloon.pos = (x + dp(60) + i * balloon_spacing, y + dp(15))
                balloon.opacity = 0.85
                self.add_widget(balloon)
                self.deco_widgets.append(balloon)
                animate_float(balloon, amplitude=10, duration=2.5 + i * 0.3)
            except: pass
        
        # 星星 - 分布在标题两侧
        star_positions = [
            (x + dp(80), y + h - dp(55)),
            (x + w - dp(100), y + h - dp(55)),
            (x + dp(150), y + h - dp(85)),
        ]
        for i, (sx, sy) in enumerate(star_positions):
            try:
                star = StarWidget(
                    color=(1, 0.9, 0.3),
                    size_hint=(None, None),
                    size=(dp(22), dp(22))
                )
                star.pos = (sx, sy)
                star.opacity = 0.8
                self.add_widget(star)
                self.deco_widgets.append(star)
                animate_twinkle(star, duration=1 + i * 0.3)
                animate_rotate(star, duration=6 + i)
            except: pass
    
    def on_enter(self):
        speak("欢迎来到数学乐园")
        # 添加装饰
        if not hasattr(self, 'deco_widgets') or not self.deco_widgets:
            Clock.schedule_once(lambda dt: self.add_decorations(), 0.3)


# ============================================================
# 认数字 - 阿奇主题
# ============================================================
class MathNumbersScreen(Screen):
    """认数字 - 学习1-20"""
    
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.current_num = 1
        self.max_num = 10  # 初始最大数字
        self.build_ui()
    
    def build_ui(self):
        layout = BoxLayout(orientation='vertical', padding=get_padding(), spacing=get_spacing())
        
        # 阿奇蓝色背景
        with layout.canvas.before:
            Color(*get_color_from_hex('#E3F2FD'))
            self.bg = Rectangle(pos=layout.pos, size=layout.size)
        layout.bind(pos=lambda i,v: setattr(self.bg, 'pos', v),
                   size=lambda i,v: setattr(self.bg, 'size', v))
        
        # 导航栏
        nav = BoxLayout(size_hint=(1, 0.1))
        back_btn = Button(
            text='< 返回',
            size_hint=(0.15, 1),
            font_size=get_font_size(18),
            background_color=get_color_from_hex('#1565C0'),
            background_normal=''
        )
        back_btn.bind(on_press=lambda x: setattr(self.manager, 'current', 'math_menu'))
        nav.add_widget(back_btn)
        
        nav.add_widget(Label(
            text='跟阿奇认数字',
            font_size=get_font_size(28),
            color=get_color_from_hex('#1565C0'),
            bold=True,
            size_hint=(0.55, 1)
        ))
        
        # 难度选择
        self.level_btn = Button(
            text='1-10',
            size_hint=(0.15, 1),
            font_size=get_font_size(16),
            background_color=get_color_from_hex('#42A5F5'),
            background_normal=''
        )
        self.level_btn.bind(on_press=self.change_level)
        nav.add_widget(self.level_btn)
        
        speak_btn = Button(
            text='听',
            size_hint=(0.15, 1),
            font_size=get_font_size(18),
            background_color=get_color_from_hex('#66BB6A'),
            background_normal=''
        )
        speak_btn.bind(on_press=self.speak_number)
        nav.add_widget(speak_btn)
        
        layout.add_widget(nav)
        
        # 数字显示区域
        number_box = BoxLayout(orientation='vertical', size_hint=(1, 0.6))
        
        # 大数字
        self.num_label = Label(
            text='1',
            font_size=get_font_size(180),
            color=get_color_from_hex('#1565C0'),
            bold=True,
            size_hint=(1, 0.7)
        )
        number_box.add_widget(self.num_label)
        
        # 中文读法
        self.chinese_label = Label(
            text='一',
            font_size=get_font_size(48),
            color=get_color_from_hex('#1976D2'),
            size_hint=(1, 0.3)
        )
        number_box.add_widget(self.chinese_label)
        
        layout.add_widget(number_box)
        
        # 数字选择网格
        self.num_grid = GridLayout(cols=10, spacing=dp(5), size_hint=(1, 0.2), padding=dp(5))
        self.update_number_grid()
        layout.add_widget(self.num_grid)
        
        # 上一个/下一个按钮
        nav_btns = BoxLayout(size_hint=(1, 0.1), spacing=dp(20), padding=[dp(50), 0])
        
        prev_btn = Button(
            text='上一个',
            font_size=get_font_size(22),
            background_color=get_color_from_hex('#90CAF9'),
            background_normal=''
        )
        prev_btn.bind(on_press=self.prev_number)
        nav_btns.add_widget(prev_btn)
        
        next_btn = Button(
            text='下一个',
            font_size=get_font_size(22),
            background_color=get_color_from_hex('#42A5F5'),
            background_normal=''
        )
        next_btn.bind(on_press=self.next_number)
        nav_btns.add_widget(next_btn)
        
        layout.add_widget(nav_btns)
        
        self.add_widget(layout)
    
    def update_number_grid(self):
        """更新数字选择网格"""
        self.num_grid.clear_widgets()
        for i in range(1, self.max_num + 1):
            btn = Button(
                text=str(i),
                font_size=get_font_size(20),
                background_color=get_color_from_hex('#1565C0' if i == self.current_num else '#90CAF9'),
                background_normal=''
            )
            btn.num = i
            btn.bind(on_press=self.select_number)
            self.num_grid.add_widget(btn)
    
    def select_number(self, instance):
        """选择数字"""
        self.current_num = instance.num
        self.show_number()
    
    def show_number(self):
        """显示当前数字"""
        self.num_label.text = str(self.current_num)
        self.chinese_label.text = MathData.get_chinese(self.current_num)
        self.update_number_grid()
        speak(MathData.get_chinese(self.current_num))
    
    def prev_number(self, instance):
        """上一个数字"""
        if self.current_num > 1:
            self.current_num -= 1
            self.show_number()
    
    def next_number(self, instance):
        """下一个数字"""
        if self.current_num < self.max_num:
            self.current_num += 1
            self.show_number()
    
    def speak_number(self, instance):
        """朗读数字"""
        speak(str(self.current_num))
        Clock.schedule_once(lambda dt: speak(MathData.get_chinese(self.current_num)), 0.8)
    
    def change_level(self, instance):
        """切换难度"""
        if self.max_num == 10:
            self.max_num = 20
            self.level_btn.text = '1-20'
        else:
            self.max_num = 10
            self.level_btn.text = '1-10'
        if self.current_num > self.max_num:
            self.current_num = self.max_num
        self.update_number_grid()
        self.show_number()
    
    def on_enter(self):
        self.show_number()


# ============================================================
# 数一数 - 毛毛主题
# ============================================================
class MathCountingScreen(Screen):
    """数一数 - 点数物品"""
    
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.target_count = 3
        self.user_count = 0
        self.items = []
        self.build_ui()
    
    def build_ui(self):
        layout = BoxLayout(orientation='vertical', padding=get_padding(), spacing=get_spacing())
        
        # 毛毛红色背景
        with layout.canvas.before:
            Color(*get_color_from_hex('#FFEBEE'))
            self.bg = Rectangle(pos=layout.pos, size=layout.size)
        layout.bind(pos=lambda i,v: setattr(self.bg, 'pos', v),
                   size=lambda i,v: setattr(self.bg, 'size', v))
        
        # 导航栏
        nav = BoxLayout(size_hint=(1, 0.1))
        back_btn = Button(
            text='< 返回',
            size_hint=(0.15, 1),
            font_size=get_font_size(18),
            background_color=get_color_from_hex('#D32F2F'),
            background_normal=''
        )
        back_btn.bind(on_press=lambda x: setattr(self.manager, 'current', 'math_menu'))
        nav.add_widget(back_btn)
        
        nav.add_widget(Label(
            text='跟毛毛数一数',
            font_size=get_font_size(28),
            color=get_color_from_hex('#D32F2F'),
            bold=True,
            size_hint=(0.55, 1)
        ))
        
        self.score_label = Label(
            text='',
            font_size=get_font_size(20),
            color=get_color_from_hex('#4CAF50'),
            size_hint=(0.15, 1)
        )
        nav.add_widget(self.score_label)
        
        new_btn = Button(
            text='换题',
            size_hint=(0.15, 1),
            font_size=get_font_size(18),
            background_color=get_color_from_hex('#FF7043'),
            background_normal=''
        )
        new_btn.bind(on_press=self.new_question)
        nav.add_widget(new_btn)
        
        layout.add_widget(nav)
        
        # 提示
        self.hint_label = Label(
            text='数一数，有几个苹果？',
            font_size=get_font_size(24),
            color=get_color_from_hex('#D32F2F'),
            size_hint=(1, 0.08)
        )
        layout.add_widget(self.hint_label)
        
        # 物品显示区域
        self.items_box = BoxLayout(size_hint=(1, 0.45))
        self.items_widget = CountingItemsWidget()
        self.items_box.add_widget(self.items_widget)
        layout.add_widget(self.items_box)
        
        # 答案选择
        answer_label = Label(
            text='有几个？点击选择：',
            font_size=get_font_size(20),
            color=get_color_from_hex('#666666'),
            size_hint=(1, 0.07)
        )
        layout.add_widget(answer_label)
        
        # 数字按钮
        self.answer_grid = GridLayout(cols=5, spacing=dp(10), size_hint=(1, 0.2), padding=dp(10))
        layout.add_widget(self.answer_grid)
        
        # 结果显示
        self.result_label = Label(
            text='',
            font_size=get_font_size(28),
            color=get_color_from_hex('#4CAF50'),
            size_hint=(1, 0.1)
        )
        layout.add_widget(self.result_label)
        
        self.add_widget(layout)
    
    def new_question(self, instance=None):
        """生成新题目"""
        self.target_count = random.randint(1, 10)
        self.user_count = 0
        self.result_label.text = ''
        self.score_label.text = ''
        
        # 随机选择物品类型
        item_types = ['apple', 'star', 'heart', 'ball']
        item_type = random.choice(item_types)
        
        item_names = {'apple': '苹果', 'star': '星星', 'heart': '爱心', 'ball': '球'}
        self.hint_label.text = f'数一数，有几个{item_names[item_type]}？'
        
        # 更新物品显示
        self.items_widget.set_items(item_type, self.target_count)
        
        # 更新答案按钮
        self.update_answer_buttons()
        
        speak(f"数一数，有几个{item_names[item_type]}")
    
    def update_answer_buttons(self):
        """更新答案按钮"""
        self.answer_grid.clear_widgets()
        
        # 生成选项（包含正确答案和干扰项）
        options = [self.target_count]
        while len(options) < 5:
            opt = random.randint(1, 10)
            if opt not in options:
                options.append(opt)
        random.shuffle(options)
        
        for opt in options:
            btn = Button(
                text=str(opt),
                font_size=get_font_size(32),
                background_color=get_color_from_hex('#EF5350'),
                background_normal=''
            )
            btn.answer = opt
            btn.bind(on_press=self.check_answer)
            self.answer_grid.add_widget(btn)
    
    def check_answer(self, instance):
        """检查答案"""
        if instance.answer == self.target_count:
            self.result_label.text = '答对了！'
            self.result_label.color = get_color_from_hex('#4CAF50')
            self.score_label.text = '棒！'
            play_praise()
            # 显示庆祝效果
            show_correct_effect(self, instance.center_x, instance.center_y)
            # 延迟后出新题
            Clock.schedule_once(lambda dt: self.new_question(), 2.0)
        else:
            self.result_label.text = f'再数数看~'
            self.result_label.color = get_color_from_hex('#FF9800')
            play_encourage()
    
    def on_enter(self):
        self.new_question()


class CountingItemsWidget(Widget):
    """数数物品显示组件"""
    
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.item_type = 'apple'
        self.count = 0
        self.bind(size=self.draw_items, pos=self.draw_items)
    
    def set_items(self, item_type, count):
        """设置物品"""
        self.item_type = item_type
        self.count = count
        self.draw_items()
    
    def draw_items(self, *args):
        """绘制物品"""
        self.canvas.clear()
        if self.count == 0:
            return
        
        # 计算物品位置（网格排列）
        cols = min(5, self.count)
        rows = (self.count + cols - 1) // cols
        
        item_size = min(self.width / (cols + 1), self.height / (rows + 1)) * 0.7
        
        start_x = self.x + (self.width - cols * item_size * 1.3) / 2
        start_y = self.y + (self.height - rows * item_size * 1.3) / 2
        
        with self.canvas:
            for i in range(self.count):
                row = i // cols
                col = i % cols
                x = start_x + col * item_size * 1.3 + item_size * 0.15
                y = start_y + row * item_size * 1.3 + item_size * 0.15
                
                self.draw_item(x, y, item_size)
    
    def draw_item(self, x, y, size):
        """绘制单个物品"""
        with self.canvas:
            if self.item_type == 'apple':
                # 红色苹果
                Color(0.9, 0.2, 0.2, 1)
                Ellipse(pos=(x, y), size=(size, size))
                # 苹果柄
                Color(0.4, 0.25, 0.1, 1)
                Line(points=[x + size/2, y + size, x + size/2, y + size + size*0.15], width=dp(2))
            elif self.item_type == 'star':
                # 黄色星星
                Color(1, 0.85, 0.2, 1)
                self.draw_star(x + size/2, y + size/2, size/2)
            elif self.item_type == 'heart':
                # 粉色爱心
                Color(1, 0.4, 0.6, 1)
                self.draw_heart(x, y, size)
            elif self.item_type == 'ball':
                # 蓝色球
                Color(0.2, 0.6, 1, 1)
                Ellipse(pos=(x, y), size=(size, size))
    
    def draw_star(self, cx, cy, r):
        """绘制五角星"""
        import math
        points = []
        for i in range(5):
            # 外顶点
            angle = math.radians(90 + i * 72)
            points.extend([cx + r * math.cos(angle), cy + r * math.sin(angle)])
            # 内顶点
            angle = math.radians(90 + i * 72 + 36)
            points.extend([cx + r * 0.4 * math.cos(angle), cy + r * 0.4 * math.sin(angle)])
        points.extend(points[:2])  # 闭合
        Line(points=points, width=dp(2), close=True)
    
    def draw_heart(self, x, y, size):
        """绘制爱心"""
        # 用两个圆和一个三角形近似
        r = size * 0.3
        Ellipse(pos=(x + size*0.1, y + size*0.4), size=(r*2, r*2))
        Ellipse(pos=(x + size*0.5 - r, y + size*0.4), size=(r*2, r*2))
        # 下半部分用三角形
        Triangle(points=[x, y + size*0.5, x + size, y + size*0.5, x + size/2, y])


# ============================================================
# 比大小 - 小砾主题
# ============================================================
class MathCompareScreen(Screen):
    """比大小 - 比较两个数"""
    
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.num1 = 0
        self.num2 = 0
        self.correct_answer = ''
        self.score = 0
        self.total = 0
        self.build_ui()
    
    def build_ui(self):
        layout = BoxLayout(orientation='vertical', padding=get_padding(), spacing=get_spacing())
        
        # 小砾黄色背景
        with layout.canvas.before:
            Color(*get_color_from_hex('#FFF8E1'))
            self.bg = Rectangle(pos=layout.pos, size=layout.size)
        layout.bind(pos=lambda i,v: setattr(self.bg, 'pos', v),
                   size=lambda i,v: setattr(self.bg, 'size', v))
        
        # 导航栏
        nav = BoxLayout(size_hint=(1, 0.1))
        back_btn = Button(
            text='< 返回',
            size_hint=(0.15, 1),
            font_size=get_font_size(18),
            background_color=get_color_from_hex('#FF8F00'),
            background_normal=''
        )
        back_btn.bind(on_press=lambda x: setattr(self.manager, 'current', 'math_menu'))
        nav.add_widget(back_btn)
        
        nav.add_widget(Label(
            text='跟小砾比大小',
            font_size=get_font_size(28),
            color=get_color_from_hex('#FF8F00'),
            bold=True,
            size_hint=(0.55, 1)
        ))
        
        self.score_label = Label(
            text='0/0',
            font_size=get_font_size(20),
            color=get_color_from_hex('#4CAF50'),
            size_hint=(0.15, 1)
        )
        nav.add_widget(self.score_label)
        
        new_btn = Button(
            text='换题',
            size_hint=(0.15, 1),
            font_size=get_font_size(18),
            background_color=get_color_from_hex('#FFB300'),
            background_normal=''
        )
        new_btn.bind(on_press=self.new_question)
        nav.add_widget(new_btn)
        
        layout.add_widget(nav)
        
        # 提示
        self.hint_label = Label(
            text='哪个数更大？点击中间的符号',
            font_size=get_font_size(22),
            color=get_color_from_hex('#FF8F00'),
            size_hint=(1, 0.08)
        )
        layout.add_widget(self.hint_label)
        
        # 比较区域
        compare_box = BoxLayout(size_hint=(1, 0.45), spacing=dp(10))
        
        # 左边数字
        self.left_label = Label(
            text='5',
            font_size=get_font_size(120),
            color=get_color_from_hex('#1565C0'),
            bold=True
        )
        compare_box.add_widget(self.left_label)
        
        # 中间符号区域
        symbol_box = BoxLayout(orientation='vertical', size_hint=(0.3, 1))
        self.symbol_label = Label(
            text='?',
            font_size=get_font_size(80),
            color=get_color_from_hex('#FF8F00'),
            bold=True
        )
        symbol_box.add_widget(self.symbol_label)
        compare_box.add_widget(symbol_box)
        
        # 右边数字
        self.right_label = Label(
            text='3',
            font_size=get_font_size(120),
            color=get_color_from_hex('#D32F2F'),
            bold=True
        )
        compare_box.add_widget(self.right_label)
        
        layout.add_widget(compare_box)
        
        # 选择按钮
        btn_box = BoxLayout(size_hint=(1, 0.2), spacing=dp(30), padding=[dp(50), dp(10)])
        
        self.gt_btn = Button(
            text='>',
            font_size=get_font_size(60),
            background_color=get_color_from_hex('#4CAF50'),
            background_normal=''
        )
        self.gt_btn.bind(on_press=lambda x: self.check_answer('>'))
        btn_box.add_widget(self.gt_btn)
        
        self.eq_btn = Button(
            text='=',
            font_size=get_font_size(60),
            background_color=get_color_from_hex('#2196F3'),
            background_normal=''
        )
        self.eq_btn.bind(on_press=lambda x: self.check_answer('='))
        btn_box.add_widget(self.eq_btn)
        
        self.lt_btn = Button(
            text='<',
            font_size=get_font_size(60),
            background_color=get_color_from_hex('#FF9800'),
            background_normal=''
        )
        self.lt_btn.bind(on_press=lambda x: self.check_answer('<'))
        btn_box.add_widget(self.lt_btn)
        
        layout.add_widget(btn_box)
        
        # 结果显示
        self.result_label = Label(
            text='',
            font_size=get_font_size(28),
            color=get_color_from_hex('#4CAF50'),
            size_hint=(1, 0.12)
        )
        layout.add_widget(self.result_label)
        
        self.add_widget(layout)
    
    def new_question(self, instance=None):
        """生成新题目"""
        self.num1 = random.randint(1, 10)
        self.num2 = random.randint(1, 10)
        
        if self.num1 > self.num2:
            self.correct_answer = '>'
        elif self.num1 < self.num2:
            self.correct_answer = '<'
        else:
            self.correct_answer = '='
        
        self.left_label.text = str(self.num1)
        self.right_label.text = str(self.num2)
        self.symbol_label.text = '?'
        self.result_label.text = ''
        
        speak(f"{self.num1} 和 {self.num2}，哪个大")
    
    def check_answer(self, answer):
        """检查答案"""
        self.total += 1
        self.symbol_label.text = answer
        
        if answer == self.correct_answer:
            self.score += 1
            self.result_label.text = '答对了！'
            self.result_label.color = get_color_from_hex('#4CAF50')
            play_praise()
            # 显示庆祝效果
            show_correct_effect(self, self.center_x, self.center_y)
            Clock.schedule_once(lambda dt: self.new_question(), 1.5)
        else:
            self.result_label.text = f'再想想~ 答案是 {self.correct_answer}'
            self.result_label.color = get_color_from_hex('#FF9800')
            self.symbol_label.text = self.correct_answer
            play_encourage()
        
        self.score_label.text = f'{self.score}/{self.total}'
    
    def on_enter(self):
        self.score = 0
        self.total = 0
        self.score_label.text = '0/0'
        self.new_question()


# ============================================================
# 学加法 - 路马主题
# ============================================================
class MathAdditionScreen(Screen):
    """学加法 - 5以内加法"""
    
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.num1 = 0
        self.num2 = 0
        self.answer = 0
        self.max_sum = 5  # 最大和
        self.score = 0
        self.total = 0
        self.build_ui()
    
    def build_ui(self):
        layout = BoxLayout(orientation='vertical', padding=get_padding(), spacing=get_spacing())
        
        # 路马青色背景
        with layout.canvas.before:
            Color(*get_color_from_hex('#E0F2F1'))
            self.bg = Rectangle(pos=layout.pos, size=layout.size)
        layout.bind(pos=lambda i,v: setattr(self.bg, 'pos', v),
                   size=lambda i,v: setattr(self.bg, 'size', v))
        
        # 导航栏
        nav = BoxLayout(size_hint=(1, 0.1))
        back_btn = Button(
            text='< 返回',
            size_hint=(0.12, 1),
            font_size=get_font_size(18),
            background_color=get_color_from_hex('#00897B'),
            background_normal=''
        )
        back_btn.bind(on_press=lambda x: setattr(self.manager, 'current', 'math_menu'))
        nav.add_widget(back_btn)
        
        nav.add_widget(Label(
            text='跟路马学加法',
            font_size=get_font_size(28),
            color=get_color_from_hex('#00897B'),
            bold=True,
            size_hint=(0.46, 1)
        ))
        
        # 难度选择
        self.level_btn = Button(
            text='5以内',
            size_hint=(0.14, 1),
            font_size=get_font_size(16),
            background_color=get_color_from_hex('#26A69A'),
            background_normal=''
        )
        self.level_btn.bind(on_press=self.change_level)
        nav.add_widget(self.level_btn)
        
        self.score_label = Label(
            text='0/0',
            font_size=get_font_size(18),
            color=get_color_from_hex('#4CAF50'),
            size_hint=(0.14, 1)
        )
        nav.add_widget(self.score_label)
        
        new_btn = Button(
            text='换题',
            size_hint=(0.14, 1),
            font_size=get_font_size(18),
            background_color=get_color_from_hex('#4DB6AC'),
            background_normal=''
        )
        new_btn.bind(on_press=self.new_question)
        nav.add_widget(new_btn)
        
        layout.add_widget(nav)
        
        # 算式显示
        formula_box = BoxLayout(size_hint=(1, 0.25))
        
        self.formula_label = Label(
            text='2 + 3 = ?',
            font_size=get_font_size(72),
            color=get_color_from_hex('#00695C'),
            bold=True
        )
        formula_box.add_widget(self.formula_label)
        
        layout.add_widget(formula_box)
        
        # 图形辅助显示
        self.visual_box = BoxLayout(size_hint=(1, 0.25))
        self.visual_widget = AdditionVisualWidget()
        self.visual_box.add_widget(self.visual_widget)
        layout.add_widget(self.visual_box)
        
        # 答案选择
        answer_label = Label(
            text='答案是几？',
            font_size=get_font_size(22),
            color=get_color_from_hex('#00897B'),
            size_hint=(1, 0.07)
        )
        layout.add_widget(answer_label)
        
        # 数字按钮
        self.answer_grid = GridLayout(cols=5, spacing=dp(10), size_hint=(1, 0.18), padding=dp(10))
        layout.add_widget(self.answer_grid)
        
        # 结果显示
        self.result_label = Label(
            text='',
            font_size=get_font_size(28),
            color=get_color_from_hex('#4CAF50'),
            size_hint=(1, 0.1)
        )
        layout.add_widget(self.result_label)
        
        self.add_widget(layout)
    
    def new_question(self, instance=None):
        """生成新题目"""
        # 确保和不超过max_sum
        self.num1 = random.randint(0, self.max_sum)
        self.num2 = random.randint(0, self.max_sum - self.num1)
        self.answer = self.num1 + self.num2
        
        self.formula_label.text = f'{self.num1} + {self.num2} = ?'
        self.result_label.text = ''
        
        # 更新图形显示
        self.visual_widget.set_numbers(self.num1, self.num2)
        
        # 更新答案按钮
        self.update_answer_buttons()
        
        speak(f"{self.num1} 加 {self.num2} 等于几")
    
    def update_answer_buttons(self):
        """更新答案按钮"""
        self.answer_grid.clear_widgets()
        
        # 生成选项
        options = [self.answer]
        while len(options) < 5:
            opt = random.randint(0, self.max_sum + 2)
            if opt not in options:
                options.append(opt)
        random.shuffle(options)
        
        for opt in options:
            btn = Button(
                text=str(opt),
                font_size=get_font_size(32),
                background_color=get_color_from_hex('#26A69A'),
                background_normal=''
            )
            btn.answer = opt
            btn.bind(on_press=self.check_answer)
            self.answer_grid.add_widget(btn)
    
    def check_answer(self, instance):
        """检查答案"""
        self.total += 1
        
        if instance.answer == self.answer:
            self.score += 1
            self.formula_label.text = f'{self.num1} + {self.num2} = {self.answer}'
            self.result_label.text = '答对了！'
            self.result_label.color = get_color_from_hex('#4CAF50')
            play_praise()
            # 显示庆祝效果
            show_correct_effect(self, instance.center_x, instance.center_y)
            Clock.schedule_once(lambda dt: self.new_question(), 1.5)
        else:
            self.result_label.text = '再算算~'
            self.result_label.color = get_color_from_hex('#FF9800')
            play_encourage()
        
        self.score_label.text = f'{self.score}/{self.total}'
    
    def change_level(self, instance):
        """切换难度"""
        if self.max_sum == 5:
            self.max_sum = 10
            self.level_btn.text = '10以内'
        else:
            self.max_sum = 5
            self.level_btn.text = '5以内'
        self.new_question()
    
    def on_enter(self):
        self.score = 0
        self.total = 0
        self.score_label.text = '0/0'
        self.new_question()


class AdditionVisualWidget(Widget):
    """加法图形辅助显示"""
    
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.num1 = 0
        self.num2 = 0
        self.bind(size=self.draw, pos=self.draw)
    
    def set_numbers(self, num1, num2):
        self.num1 = num1
        self.num2 = num2
        self.draw()
    
    def draw(self, *args):
        self.canvas.clear()
        
        total = self.num1 + self.num2
        if total == 0:
            return
        
        # 计算圆的大小
        max_per_row = 5
        circle_size = min(self.width / (max_per_row + 2), self.height / 3) * 0.8
        
        with self.canvas:
            # 画第一组（蓝色）
            Color(0.2, 0.5, 0.9, 1)
            for i in range(self.num1):
                x = self.x + 20 + (i % max_per_row) * (circle_size + 10)
                y = self.center_y + (circle_size + 10) * (0.5 if i < max_per_row else -0.5)
                Ellipse(pos=(x, y), size=(circle_size, circle_size))
            
            # 加号
            if self.num1 > 0 and self.num2 > 0:
                Color(0.3, 0.3, 0.3, 1)
                plus_x = self.x + 20 + max(self.num1, 1) * (circle_size + 10) + 10
                Line(points=[plus_x, self.center_y - 15, plus_x, self.center_y + 15], width=dp(3))
                Line(points=[plus_x - 15, self.center_y, plus_x + 15, self.center_y], width=dp(3))
            
            # 画第二组（红色）
            Color(0.9, 0.3, 0.3, 1)
            start_x = self.x + 20 + max(self.num1, 0) * (circle_size + 10) + (50 if self.num1 > 0 else 0)
            for i in range(self.num2):
                x = start_x + (i % max_per_row) * (circle_size + 10)
                y = self.center_y + (circle_size + 10) * (0.5 if i < max_per_row else -0.5)
                Ellipse(pos=(x, y), size=(circle_size, circle_size))


# ============================================================
# 认形状 - 天天主题
# ============================================================
class MathShapesScreen(Screen):
    """认形状 - 学习基本形状"""
    
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.current_shape_idx = 0
        self.score = 0
        self.total = 0
        self.mode = 'learn'  # learn 或 quiz
        self.build_ui()
    
    def build_ui(self):
        layout = BoxLayout(orientation='vertical', padding=get_padding(), spacing=get_spacing())
        
        # 天天粉色背景
        with layout.canvas.before:
            Color(*get_color_from_hex('#FCE4EC'))
            self.bg = Rectangle(pos=layout.pos, size=layout.size)
        layout.bind(pos=lambda i,v: setattr(self.bg, 'pos', v),
                   size=lambda i,v: setattr(self.bg, 'size', v))
        
        # 导航栏
        nav = BoxLayout(size_hint=(1, 0.1))
        back_btn = Button(
            text='< 返回',
            size_hint=(0.12, 1),
            font_size=get_font_size(18),
            background_color=get_color_from_hex('#EC407A'),
            background_normal=''
        )
        back_btn.bind(on_press=lambda x: setattr(self.manager, 'current', 'math_menu'))
        nav.add_widget(back_btn)
        
        nav.add_widget(Label(
            text='跟天天认形状',
            font_size=get_font_size(28),
            color=get_color_from_hex('#EC407A'),
            bold=True,
            size_hint=(0.46, 1)
        ))
        
        # 模式切换
        self.mode_btn = Button(
            text='学习',
            size_hint=(0.14, 1),
            font_size=get_font_size(16),
            background_color=get_color_from_hex('#F06292'),
            background_normal=''
        )
        self.mode_btn.bind(on_press=self.toggle_mode)
        nav.add_widget(self.mode_btn)
        
        self.score_label = Label(
            text='',
            font_size=get_font_size(18),
            color=get_color_from_hex('#4CAF50'),
            size_hint=(0.14, 1)
        )
        nav.add_widget(self.score_label)
        
        next_btn = Button(
            text='下一个',
            size_hint=(0.14, 1),
            font_size=get_font_size(18),
            background_color=get_color_from_hex('#F48FB1'),
            background_normal=''
        )
        next_btn.bind(on_press=self.next_shape)
        nav.add_widget(next_btn)
        
        layout.add_widget(nav)
        
        # 形状名称
        self.shape_name_label = Label(
            text='圆形',
            font_size=get_font_size(42),
            color=get_color_from_hex('#EC407A'),
            bold=True,
            size_hint=(1, 0.12)
        )
        layout.add_widget(self.shape_name_label)
        
        # 形状显示区域
        self.shape_box = BoxLayout(size_hint=(1, 0.45))
        self.shape_widget = ShapeDisplayWidget()
        self.shape_box.add_widget(self.shape_widget)
        layout.add_widget(self.shape_box)
        
        # 形状选择按钮（学习模式）/ 答案按钮（测验模式）
        self.buttons_box = GridLayout(cols=5, spacing=dp(10), size_hint=(1, 0.2), padding=dp(10))
        layout.add_widget(self.buttons_box)
        
        # 结果显示
        self.result_label = Label(
            text='',
            font_size=get_font_size(28),
            color=get_color_from_hex('#4CAF50'),
            size_hint=(1, 0.1)
        )
        layout.add_widget(self.result_label)
        
        self.add_widget(layout)
    
    def toggle_mode(self, instance):
        """切换学习/测验模式"""
        if self.mode == 'learn':
            self.mode = 'quiz'
            self.mode_btn.text = '测验'
            self.score = 0
            self.total = 0
            self.score_label.text = '0/0'
            self.new_quiz()
        else:
            self.mode = 'learn'
            self.mode_btn.text = '学习'
            self.score_label.text = ''
            self.show_shape()
    
    def show_shape(self):
        """显示当前形状（学习模式）"""
        shape = MathData.SHAPES[self.current_shape_idx]
        name, shape_type, color = shape
        
        self.shape_name_label.text = name
        self.shape_widget.set_shape(shape_type, color)
        self.result_label.text = ''
        
        # 更新形状选择按钮
        self.buttons_box.clear_widgets()
        for i, (s_name, s_type, s_color) in enumerate(MathData.SHAPES):
            btn = Button(
                text=s_name,
                font_size=get_font_size(20),
                background_color=get_color_from_hex(s_color if i == self.current_shape_idx else '#BDBDBD'),
                background_normal=''
            )
            btn.shape_idx = i
            btn.bind(on_press=self.select_shape)
            self.buttons_box.add_widget(btn)
        
        speak(name)
    
    def select_shape(self, instance):
        """选择形状"""
        self.current_shape_idx = instance.shape_idx
        self.show_shape()
    
    def next_shape(self, instance):
        """下一个形状"""
        if self.mode == 'learn':
            self.current_shape_idx = (self.current_shape_idx + 1) % len(MathData.SHAPES)
            self.show_shape()
        else:
            self.new_quiz()
    
    def new_quiz(self):
        """生成测验题目"""
        # 随机选择一个形状
        self.current_shape_idx = random.randint(0, len(MathData.SHAPES) - 1)
        shape = MathData.SHAPES[self.current_shape_idx]
        name, shape_type, color = shape
        
        self.shape_name_label.text = '这是什么形状？'
        self.shape_widget.set_shape(shape_type, color)
        self.result_label.text = ''
        
        # 生成答案选项
        self.buttons_box.clear_widgets()
        options = list(range(len(MathData.SHAPES)))
        random.shuffle(options)
        
        for idx in options:
            s_name, s_type, s_color = MathData.SHAPES[idx]
            btn = Button(
                text=s_name,
                font_size=get_font_size(20),
                background_color=get_color_from_hex(s_color),
                background_normal=''
            )
            btn.shape_idx = idx
            btn.bind(on_press=self.check_quiz_answer)
            self.buttons_box.add_widget(btn)
        
        speak("这是什么形状")
    
    def check_quiz_answer(self, instance):
        """检查测验答案"""
        self.total += 1
        
        if instance.shape_idx == self.current_shape_idx:
            self.score += 1
            name = MathData.SHAPES[self.current_shape_idx][0]
            self.shape_name_label.text = name
            self.result_label.text = '答对了！'
            self.result_label.color = get_color_from_hex('#4CAF50')
            play_praise()
            # 显示庆祝效果
            show_correct_effect(self, instance.center_x, instance.center_y)
            Clock.schedule_once(lambda dt: self.new_quiz(), 1.5)
        else:
            self.result_label.text = '再看看~'
            self.result_label.color = get_color_from_hex('#FF9800')
            play_encourage()
        
        self.score_label.text = f'{self.score}/{self.total}'
    
    def on_enter(self):
        if self.mode == 'learn':
            self.show_shape()
        else:
            self.new_quiz()


class ShapeDisplayWidget(Widget):
    """形状显示组件"""
    
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.shape_type = 'circle'
        self.shape_color = '#FF6B6B'
        self.bind(size=self.draw, pos=self.draw)
    
    def set_shape(self, shape_type, color):
        self.shape_type = shape_type
        self.shape_color = color
        self.draw()
    
    def draw(self, *args):
        self.canvas.clear()
        
        # 计算形状大小和位置
        size = min(self.width, self.height) * 0.6
        cx = self.center_x
        cy = self.center_y
        
        with self.canvas:
            Color(*get_color_from_hex(self.shape_color))
            
            if self.shape_type == 'circle':
                Ellipse(pos=(cx - size/2, cy - size/2), size=(size, size))
            
            elif self.shape_type == 'square':
                Rectangle(pos=(cx - size/2, cy - size/2), size=(size, size))
            
            elif self.shape_type == 'rectangle':
                w = size
                h = size * 0.6
                Rectangle(pos=(cx - w/2, cy - h/2), size=(w, h))
            
            elif self.shape_type == 'triangle':
                Triangle(points=[
                    cx, cy + size/2,  # 顶点
                    cx - size/2, cy - size/2,  # 左下
                    cx + size/2, cy - size/2   # 右下
                ])
            
            elif self.shape_type == 'star':
                self.draw_star(cx, cy, size/2)
    
    def draw_star(self, cx, cy, r):
        """绘制五角星"""
        import math
        points = []
        for i in range(5):
            # 外顶点
            angle = math.radians(90 + i * 72)
            points.extend([cx + r * math.cos(angle), cy + r * math.sin(angle)])
            # 内顶点
            angle = math.radians(90 + i * 72 + 36)
            points.extend([cx + r * 0.4 * math.cos(angle), cy + r * 0.4 * math.sin(angle)])
        
        # 使用三角形填充五角星
        with self.canvas:
            for i in range(5):
                idx = i * 2
                next_idx = (idx + 2) % 10
                Triangle(points=[
                    cx, cy,  # 中心
                    points[idx * 2], points[idx * 2 + 1],  # 外顶点
                    points[next_idx * 2], points[next_idx * 2 + 1]  # 下一个外顶点
                ])


# ============================================================
# 大闯关 - 综合挑战模式
# ============================================================
class MathChallengeScreen(Screen):
    """大闯关 - 综合数学挑战"""
    
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.level = 1
        self.score = 0
        self.lives = 3
        self.question_type = 'count'
        self.correct_answer = None
        self.build_ui()
    
    def build_ui(self):
        layout = BoxLayout(orientation='vertical', padding=get_padding(), spacing=get_spacing())
        
        # 紫色背景
        with layout.canvas.before:
            Color(*get_color_from_hex('#EDE7F6'))
            self.bg = Rectangle(pos=layout.pos, size=layout.size)
        layout.bind(pos=lambda i,v: setattr(self.bg, 'pos', v),
                   size=lambda i,v: setattr(self.bg, 'size', v))

        # 导航栏
        nav = BoxLayout(size_hint=(1, 0.1))
        back_btn = Button(
            text='< 返回',
            size_hint=(0.12, 1),
            font_size=get_font_size(18),
            background_color=get_color_from_hex('#7B1FA2'),
            background_normal=''
        )
        back_btn.bind(on_press=lambda x: setattr(self.manager, 'current', 'math_menu'))
        nav.add_widget(back_btn)
        
        nav.add_widget(Label(
            text='数学大闯关',
            font_size=get_font_size(28),
            color=get_color_from_hex('#7B1FA2'),
            bold=True,
            size_hint=(0.36, 1)
        ))

        self.level_label = Label(
            text='第1关',
            font_size=get_font_size(20),
            color=get_color_from_hex('#9C27B0'),
            size_hint=(0.14, 1)
        )
        nav.add_widget(self.level_label)
        
        self.score_label = Label(
            text='0分',
            font_size=get_font_size(18),
            color=get_color_from_hex('#4CAF50'),
            size_hint=(0.14, 1)
        )
        nav.add_widget(self.score_label)
        
        self.lives_label = Label(
            text='❤❤❤',
            font_size=get_font_size(20),
            color=get_color_from_hex('#F44336'),
            size_hint=(0.14, 1)
        )
        nav.add_widget(self.lives_label)

        restart_btn = Button(
            text='重新开始',
            size_hint=(0.14, 1),
            font_size=get_font_size(14),
            background_color=get_color_from_hex('#AB47BC'),
            background_normal=''
        )
        restart_btn.bind(on_press=self.restart_game)
        nav.add_widget(restart_btn)
        
        layout.add_widget(nav)
        
        # 题目显示
        self.question_label = Label(
            text='准备开始！',
            font_size=get_font_size(32),
            color=get_color_from_hex('#7B1FA2'),
            size_hint=(1, 0.15)
        )
        layout.add_widget(self.question_label)

        # 内容显示区域
        self.content_box = BoxLayout(size_hint=(1, 0.4))
        self.content_widget = ChallengeContentWidget()
        self.content_box.add_widget(self.content_widget)
        layout.add_widget(self.content_box)
        
        # 答案按钮
        self.answer_grid = GridLayout(cols=4, spacing=dp(15), size_hint=(1, 0.22), padding=dp(15))
        layout.add_widget(self.answer_grid)
        
        # 结果显示
        self.result_label = Label(
            text='',
            font_size=get_font_size(32),
            color=get_color_from_hex('#4CAF50'),
            size_hint=(1, 0.1)
        )
        layout.add_widget(self.result_label)
        
        self.add_widget(layout)

    def restart_game(self, instance=None):
        """重新开始游戏"""
        self.level = 1
        self.score = 0
        self.lives = 3
        self.update_status()
        self.new_question()
    
    def update_status(self):
        """更新状态显示"""
        self.level_label.text = f'第{self.level}关'
        self.score_label.text = f'{self.score}分'
        hearts = '❤' * self.lives + '♡' * (3 - self.lives)
        self.lives_label.text = hearts

    def new_question(self):
        """生成新题目"""
        if self.lives <= 0:
            self.game_over()
            return
        
        # 根据关卡选择题目类型
        if self.level <= 3:
            types = ['count']
        elif self.level <= 6:
            types = ['count', 'compare']
        else:
            types = ['count', 'compare', 'addition']
        
        self.question_type = random.choice(types)
        self.result_label.text = ''

        if self.question_type == 'count':
            self.generate_count_question()
        elif self.question_type == 'compare':
            self.generate_compare_question()
        else:
            self.generate_addition_question()
    
    def generate_count_question(self):
        """生成数数题目"""
        max_count = min(5 + self.level, 10)
        count = random.randint(1, max_count)
        self.correct_answer = count
        
        self.question_label.text = '数一数，有几个？'
        self.content_widget.show_counting(count)
        self.generate_options(count, 1, max_count + 2)
        speak("数一数，有几个")

    def generate_compare_question(self):
        """生成比大小题目"""
        max_num = min(5 + self.level, 15)
        num1 = random.randint(1, max_num)
        num2 = random.randint(1, max_num)
        
        if num1 > num2:
            self.correct_answer = '>'
        elif num1 < num2:
            self.correct_answer = '<'
        else:
            self.correct_answer = '='
        
        self.question_label.text = f'{num1} ○ {num2}，填什么符号？'
        self.content_widget.show_compare(num1, num2)
        self.generate_symbol_options()
        speak(f"{num1}和{num2}，比大小")

    def generate_addition_question(self):
        """生成加法题目"""
        max_sum = min(5 + self.level // 2, 10)
        num1 = random.randint(0, max_sum)
        num2 = random.randint(0, max_sum - num1)
        self.correct_answer = num1 + num2
        
        self.question_label.text = f'{num1} + {num2} = ?'
        self.content_widget.show_addition(num1, num2)
        self.generate_options(self.correct_answer, 0, max_sum + 2)
        speak(f"{num1}加{num2}等于几")

    def generate_options(self, correct, min_val, max_val):
        """生成数字选项"""
        self.answer_grid.clear_widgets()
        options = [correct]
        while len(options) < 4:
            opt = random.randint(min_val, max_val)
            if opt not in options:
                options.append(opt)
        random.shuffle(options)
        
        colors = ['#9C27B0', '#7B1FA2', '#AB47BC', '#BA68C8']
        for i, opt in enumerate(options):
            btn = Button(
                text=str(opt),
                font_size=get_font_size(36),
                background_color=get_color_from_hex(colors[i]),
                background_normal=''
            )
            btn.answer = opt
            btn.bind(on_press=self.check_answer)
            self.answer_grid.add_widget(btn)

    def generate_symbol_options(self):
        """生成符号选项"""
        self.answer_grid.clear_widgets()
        symbols = ['>', '<', '=', '?']
        colors = ['#4CAF50', '#FF9800', '#2196F3', '#9E9E9E']
        
        for i, sym in enumerate(symbols[:3]):
            btn = Button(
                text=sym,
                font_size=get_font_size(48),
                background_color=get_color_from_hex(colors[i]),
                background_normal=''
            )
            btn.answer = sym
            btn.bind(on_press=self.check_answer)
            self.answer_grid.add_widget(btn)
        # 添加空白占位
        self.answer_grid.add_widget(Label(text=''))

    def check_answer(self, instance):
        """检查答案"""
        if instance.answer == self.correct_answer:
            self.score += 10 * self.level
            self.result_label.text = '答对了！+' + str(10 * self.level) + '分'
            self.result_label.color = get_color_from_hex('#4CAF50')
            play_praise()
            
            # 显示庆祝效果
            show_correct_effect(self, instance.center_x, instance.center_y)
            
            # 每答对3题升一级，升级时放烟花
            old_level = self.level
            if self.score >= self.level * 30:
                self.level += 1
                if self.level > old_level:
                    show_firework_effect(self)
            
            self.update_status()
            Clock.schedule_once(lambda dt: self.new_question(), 1.2)
        else:
            self.lives -= 1
            self.result_label.text = '答错了，再想想~'
            self.result_label.color = get_color_from_hex('#F44336')
            play_encourage()
            self.update_status()
            
            if self.lives <= 0:
                Clock.schedule_once(lambda dt: self.game_over(), 1.0)

    def game_over(self):
        """游戏结束"""
        self.question_label.text = '游戏结束！'
        self.result_label.text = f'最终得分：{self.score}分，闯到第{self.level}关'
        self.result_label.color = get_color_from_hex('#7B1FA2')
        self.content_widget.show_game_over()
        self.answer_grid.clear_widgets()
        # 显示庆祝烟花
        show_firework_effect(self)
        speak(f"游戏结束，你得了{self.score}分")
    
    def on_enter(self):
        self.restart_game()


class ChallengeContentWidget(Widget):
    """闯关内容显示组件"""
    
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.mode = 'empty'
        self.data = {}
        self.bind(size=self.draw, pos=self.draw)
    
    def show_counting(self, count):
        self.mode = 'count'
        self.data = {'count': count}
        self.draw()
    
    def show_compare(self, num1, num2):
        self.mode = 'compare'
        self.data = {'num1': num1, 'num2': num2}
        self.draw()
    
    def show_addition(self, num1, num2):
        self.mode = 'addition'
        self.data = {'num1': num1, 'num2': num2}
        self.draw()
    
    def show_game_over(self):
        self.mode = 'gameover'
        self.draw()

    def draw(self, *args):
        self.canvas.clear()
        
        if self.mode == 'count':
            self.draw_counting()
        elif self.mode == 'compare':
            self.draw_compare()
        elif self.mode == 'addition':
            self.draw_addition()
        elif self.mode == 'gameover':
            self.draw_game_over()

    def draw_counting(self):
        count = self.data.get('count', 0)
        if count == 0:
            return
        
        cols = min(5, count)
        rows = (count + cols - 1) // cols
        size = min(self.width / (cols + 1), self.height / (rows + 1)) * 0.7
        
        start_x = self.x + (self.width - cols * size * 1.3) / 2
        start_y = self.y + (self.height - rows * size * 1.3) / 2
        
        with self.canvas:
            Color(0.6, 0.2, 0.8, 1)  # 紫色
            for i in range(count):
                row = i // cols
                col = i % cols
                x = start_x + col * size * 1.3
                y = start_y + row * size * 1.3
                Ellipse(pos=(x, y), size=(size, size))

    def draw_compare(self):
        num1 = self.data.get('num1', 0)
        num2 = self.data.get('num2', 0)
        
        size = min(self.width / 12, self.height / 3) * 0.8
        
        with self.canvas:
            # 左边数字的点
            Color(0.2, 0.5, 0.9, 1)
            for i in range(num1):
                x = self.x + 20 + (i % 5) * (size + 5)
                y = self.center_y + (size + 5) * (0.3 if i < 5 else -0.7)
                Ellipse(pos=(x, y), size=(size, size))
            
            # 右边数字的点
            Color(0.9, 0.3, 0.3, 1)
            start_x = self.center_x + 20
            for i in range(num2):
                x = start_x + (i % 5) * (size + 5)
                y = self.center_y + (size + 5) * (0.3 if i < 5 else -0.7)
                Ellipse(pos=(x, y), size=(size, size))

    def draw_addition(self):
        num1 = self.data.get('num1', 0)
        num2 = self.data.get('num2', 0)
        
        size = min(self.width / 14, self.height / 3) * 0.7
        
        with self.canvas:
            # 第一组
            Color(0.2, 0.6, 0.9, 1)
            for i in range(num1):
                x = self.x + 20 + (i % 5) * (size + 5)
                y = self.center_y + (size + 5) * (0.3 if i < 5 else -0.7)
                Ellipse(pos=(x, y), size=(size, size))
            
            # 加号
            if num1 > 0 or num2 > 0:
                Color(0.3, 0.3, 0.3, 1)
                plus_x = self.x + 20 + max(num1, 1) * (size + 5) + 15
                Line(points=[plus_x, self.center_y - 12, plus_x, self.center_y + 12], width=dp(2))
                Line(points=[plus_x - 12, self.center_y, plus_x + 12, self.center_y], width=dp(2))
            
            # 第二组
            Color(0.9, 0.4, 0.3, 1)
            start_x = self.x + 20 + max(num1, 0) * (size + 5) + 45
            for i in range(num2):
                x = start_x + (i % 5) * (size + 5)
                y = self.center_y + (size + 5) * (0.3 if i < 5 else -0.7)
                Ellipse(pos=(x, y), size=(size, size))

    def draw_game_over(self):
        # 画一个大奖杯
        with self.canvas:
            cx = self.center_x
            cy = self.center_y
            
            # 奖杯身体（金色）
            Color(1, 0.84, 0, 1)
            Rectangle(pos=(cx - 40, cy - 30), size=(80, 60))
            
            # 奖杯顶部
            Ellipse(pos=(cx - 50, cy + 20), size=(100, 30))
            
            # 奖杯底座
            Color(0.6, 0.4, 0.2, 1)
            Rectangle(pos=(cx - 30, cy - 50), size=(60, 20))
            Rectangle(pos=(cx - 40, cy - 60), size=(80, 15))


# ============================================================
# 主应用
# ============================================================
class MathApp(App):
    """数学乐园主应用"""
    
    def build(self):
        # 初始化音频
        try:
            get_audio()  # 确保音频模块初始化
        except:
            pass
        
        # 创建屏幕管理器
        sm = ScreenManager()
        
        # 添加所有屏幕
        sm.add_widget(MathMenuScreen(name='math_menu'))
        sm.add_widget(MathNumbersScreen(name='math_numbers'))
        sm.add_widget(MathCountingScreen(name='math_counting'))
        sm.add_widget(MathCompareScreen(name='math_compare'))
        sm.add_widget(MathAdditionScreen(name='math_addition'))
        sm.add_widget(MathShapesScreen(name='math_shapes'))
        sm.add_widget(MathChallengeScreen(name='math_challenge'))
        
        return sm


# ============================================================
# 启动入口
# ============================================================
if __name__ == '__main__':
    MathApp().run()
