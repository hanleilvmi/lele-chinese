# -*- coding: utf-8 -*-
"""
乐乐的识字乐园 - Android/鸿蒙平板优化版
专为3-5岁儿童设计的汉字学习应用
v1.3.0 - 修复TTS、优化屏幕适配
"""
import sys
import os

# 确保能找到模块
app_dir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.insert(0, app_dir)
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

# 必须在导入kivy之前配置字体
try:
    import font_config
    print("[chinese_app] 字体配置模块已加载")
except ImportError as e:
    print(f"[chinese_app] 字体配置导入失败: {e}")

from kivy.app import App
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.gridlayout import GridLayout
from kivy.uix.scrollview import ScrollView
from kivy.uix.button import Button
from kivy.uix.label import Label
from kivy.uix.widget import Widget
from kivy.uix.screenmanager import ScreenManager, Screen, FadeTransition
from kivy.graphics import Color, Rectangle, RoundedRectangle, Ellipse, Line, Triangle
from kivy.core.window import Window
from kivy.utils import platform, get_color_from_hex
from kivy.clock import Clock
from kivy.metrics import dp, sp
from kivy.core.text import LabelBase
import random


# ============================================================
# 屏幕适配配置
# ============================================================
class ScreenAdapter:
    """屏幕适配器 - 根据设备自动调整UI"""
    
    # 设计基准（1280x800平板）
    BASE_WIDTH = 1280
    BASE_HEIGHT = 800
    
    # 儿童触摸优化：最小触摸区域（dp）
    MIN_TOUCH_SIZE = 60  # 至少60dp，适合3-5岁儿童
    MIN_BUTTON_HEIGHT = 70  # 按钮最小高度
    
    _instance = None
    
    @classmethod
    def get(cls):
        if cls._instance is None:
            cls._instance = cls()
        return cls._instance
    
    def __init__(self):
        self.update()
    
    def update(self):
        """更新屏幕信息"""
        self.width = Window.width
        self.height = Window.height
        self.ratio = self.width / self.height if self.height > 0 else 1.6
        
        # 计算缩放因子
        self.scale_x = self.width / self.BASE_WIDTH
        self.scale_y = self.height / self.BASE_HEIGHT
        self.scale = min(self.scale_x, self.scale_y)
        
        print(f"[ScreenAdapter] 屏幕: {self.width}x{self.height}, 比例: {self.ratio:.2f}, 缩放: {self.scale:.2f}")
    
    def get_grid_cols(self):
        """根据屏幕宽度决定网格列数"""
        if self.ratio > 1.7:  # 超宽屏 (如2560x1440)
            return 4
        elif self.ratio > 1.4:  # 标准平板 (如1280x800)
            return 4
        else:  # 接近正方形
            return 3
    
    def get_card_cols(self):
        """汉字卡片列数"""
        if self.width >= 1920:
            return 5
        elif self.width >= 1280:
            return 4
        else:
            return 3
    
    def font_size(self, base):
        """自适应字体大小"""
        scaled = base * max(0.8, min(1.3, self.scale))
        return sp(max(12, scaled))  # 最小12sp
    
    def button_height(self):
        """按钮高度（适合儿童触摸）"""
        return dp(max(self.MIN_BUTTON_HEIGHT, 80 * self.scale))
    
    def touch_size(self):
        """最小触摸区域"""
        return dp(max(self.MIN_TOUCH_SIZE, 60 * self.scale))
    
    def padding(self):
        """内边距"""
        return dp(max(10, 15 * self.scale))
    
    def spacing(self):
        """间距"""
        return dp(max(10, 15 * self.scale))
    
    def card_spacing(self):
        """卡片间距（大一点方便点击）"""
        return dp(max(15, 20 * self.scale))


# 全局屏幕适配器
screen_adapter = ScreenAdapter.get()

# 绑定窗口大小变化
def on_window_resize(instance, width, height):
    screen_adapter.update()

Window.bind(size=on_window_resize)


# ============================================================
# 儿童友好的UI组件
# ============================================================
class ChildFriendlyButton(Button):
    """儿童友好按钮 - 大触摸区域、圆角、反馈明显"""
    
    def __init__(self, text='', icon='', color='#4CAF50', **kwargs):
        super().__init__(**kwargs)
        self.background_normal = ''
        self.background_color = get_color_from_hex(color)
        self.markup = True
        self.halign = 'center'
        self.valign = 'middle'
        
        # 设置最小尺寸
        self.size_hint_min = (dp(80), dp(60))
        
        # 构建文本
        if icon and text:
            self.text = f'[size={int(sp(36))}]{icon}[/size]\n[b]{text}[/b]'
        elif icon:
            self.text = f'[size={int(sp(42))}]{icon}[/size]'
        else:
            self.text = f'[b]{text}[/b]'
        
        self.font_size = sp(18)
    
    def on_press(self):
        """按下时的视觉反馈"""
        self.opacity = 0.7
    
    def on_release(self):
        """释放时恢复"""
        self.opacity = 1.0


class BigCharButton(Button):
    """大汉字按钮 - 用于选择题选项"""
    
    def __init__(self, char='', color='#FF6B6B', **kwargs):
        super().__init__(**kwargs)
        self.background_normal = ''
        self.background_color = get_color_from_hex(color)
        self.text = char
        self.font_size = sp(48)  # 大字体
        self.bold = True
        
        # 确保足够大的触摸区域
        self.size_hint_min = (dp(100), dp(100))
    
    def on_press(self):
        self.opacity = 0.7
    
    def on_release(self):
        self.opacity = 1.0


# 全局屏幕适配器
screen_adapter = ScreenAdapter.get()

# 绑定窗口大小变化
def on_window_resize(instance, width, height):
    screen_adapter.update()

Window.bind(size=on_window_resize)


# 配置中文字体（后备方案）
def setup_font():
    """配置中文字体"""
    font_paths = []
    if platform == 'android':
        # Android和鸿蒙系统的字体路径
        font_paths = [
            # 鸿蒙系统字体（优先）
            "/system/fonts/HarmonyOS_Sans_SC_Regular.ttf",
            "/system/fonts/HarmonyOS_Sans_SC.ttf",
            "/system/fonts/HarmonyOSSans-Regular.ttf",
            # 华为设备字体
            "/system/fonts/HwChinese-Regular.ttf",
            # 标准Android字体
            "/system/fonts/NotoSansCJK-Regular.ttc",
            "/system/fonts/DroidSansFallback.ttf",
            "/system/fonts/NotoSansSC-Regular.otf",
            "/system/fonts/DroidSansChinese.ttf",
        ]
    else:
        font_paths = [
            "C:/Windows/Fonts/msyh.ttc",
            "C:/Windows/Fonts/simhei.ttf",
        ]
    
    for path in font_paths:
        if os.path.exists(path):
            try:
                LabelBase.register(name='Roboto', fn_regular=path)
                print(f"[chinese_app] 已加载字体: {path}")
                return True
            except:
                pass
    
    print("[chinese_app] 警告: 未找到中文字体，使用系统默认")
    return False

setup_font()

# 导入数据模块
try:
    from core.data_chinese import ChineseData
    from core.game_logic import GameLogic, GameType
except ImportError:
    # 如果导入失败，使用内置数据
    print("使用内置数据模块")

# 导入绘图模块
try:
    from picture_drawings import PictureCanvas
except ImportError:
    # 如果导入失败，创建一个简单的替代类
    class PictureCanvas(Widget):
        def draw_char(self, char):
            self.canvas.clear()
            with self.canvas:
                Color(0.9, 0.9, 0.9)
                Rectangle(pos=self.pos, size=self.size)

# 导入音频模块
try:
    from audio_kivy import get_audio
    AUDIO_AVAILABLE = True
except ImportError:
    AUDIO_AVAILABLE = False
    def get_audio():
        return None

# 平板适配：根据平台设置窗口大小
if platform != 'android':
    Window.size = (1280, 800)  # 模拟平板尺寸


# 全局音频实例
audio = None

def init_audio():
    """初始化音频"""
    global audio
    if AUDIO_AVAILABLE:
        audio = get_audio()
        return audio
    return None

def speak(text):
    """朗读文字"""
    if audio:
        audio.speak(text)

def play_praise():
    """播放表扬"""
    if audio:
        audio.play_praise()

def play_encourage():
    """播放鼓励"""
    if audio:
        audio.play_encourage()


def get_font_size(base_size):
    """根据屏幕大小动态计算字体大小"""
    return screen_adapter.font_size(base_size)


def get_padding():
    """根据屏幕大小动态计算内边距"""
    return screen_adapter.padding()


def get_spacing():
    """根据屏幕大小动态计算间距"""
    return screen_adapter.spacing()


class ChineseMenuScreen(Screen):
    """识字乐园主菜单 - 儿童触摸优化"""
    
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.build_ui()
    
    def build_ui(self):
        layout = BoxLayout(orientation='vertical', padding=get_padding(), spacing=get_spacing())
        
        with layout.canvas.before:
            Color(*get_color_from_hex('#FFF8E1'))
            self.bg = Rectangle(pos=layout.pos, size=layout.size)
        layout.bind(pos=lambda i,v: setattr(self.bg, 'pos', v),
                   size=lambda i,v: setattr(self.bg, 'size', v))
        
        # 标题区域
        title_box = BoxLayout(size_hint=(1, 0.12))
        title_box.add_widget(Label(
            text='🐕 乐乐的识字乐园 🐕',
            font_size=get_font_size(38),
            color=get_color_from_hex('#E65100'),
            bold=True
        ))
        layout.add_widget(title_box)
        
        # 副标题
        layout.add_widget(Label(
            text='点击下面的游戏开始学习汉字吧！',
            font_size=get_font_size(20),
            color=get_color_from_hex('#666666'),
            size_hint=(1, 0.06)
        ))
        
        # 游戏选择区 - 使用更大的间距
        games = GridLayout(
            cols=screen_adapter.get_grid_cols(), 
            spacing=screen_adapter.card_spacing(), 
            size_hint=(1, 0.70), 
            padding=dp(15)
        )
        
        game_list = [
            ('📖', '学汉字', '认识基础汉字', '#FF7043', 'chinese_learn'),
            ('✏️', '描红写字', '学写汉字', '#FF9800', 'chinese_write'),
            ('📚', '汉字故事', '汉字的由来', '#66BB6A', 'chinese_story'),
            ('🖼️', '看图选字', '看图片选汉字', '#4ECDC4', 'chinese_picture'),
            ('❓', '汉字测验', '考考你学会了吗', '#42A5F5', 'chinese_quiz'),
            ('🎯', '汉字配对', '找到相同的字', '#9C27B0', 'chinese_match'),
            ('🔨', '打地鼠', '快速找汉字', '#FFD93D', 'chinese_whack'),
            ('🏆', '闯关模式', '一关一关闯', '#E91E63', 'chinese_challenge'),
        ]
        
        for icon, title, desc, color, screen in game_list:
            btn = Button(
                background_normal='',
                background_color=get_color_from_hex(color),
                size_hint_min=(dp(120), dp(100))  # 最小尺寸确保可点击
            )
            btn.markup = True
            # 使用更大的字体
            btn.text = f'[size={int(sp(48))}]{icon}[/size]\n[b][size={int(sp(22))}]{title}[/size][/b]\n[size={int(sp(14))}]{desc}[/size]'
            btn.target_screen = screen
            btn.bind(on_press=self.go_screen)
            games.add_widget(btn)
        
        layout.add_widget(games)
        
        # 底部信息
        bottom = BoxLayout(size_hint=(1, 0.08))
        bottom.add_widget(Label(
            text='🐾 适合3-5岁小朋友 🐾',
            font_size=get_font_size(16),
            color=get_color_from_hex('#999999')
        ))
        layout.add_widget(bottom)
        
        self.add_widget(layout)
    
    def go_screen(self, instance):
        if hasattr(instance, 'target_screen'):
            # 播放点击音效
            speak(instance.target_screen.replace('chinese_', '').replace('_', ''))
            self.manager.current = instance.target_screen


class ChineseLearnScreen(Screen):
    """学汉字 - 卡片学习模式（分页）- 触摸优化"""
    
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.current_level = 1
        self.current_page = 0
        self.cards_per_page = 12  # 每页12个汉字（3行x4列）
        self.build_ui()
    
    def build_ui(self):
        layout = BoxLayout(orientation='vertical', padding=get_padding(), spacing=get_spacing())
        
        with layout.canvas.before:
            Color(*get_color_from_hex('#FFF3E0'))
            self.bg = Rectangle(pos=layout.pos, size=layout.size)
        layout.bind(pos=lambda i,v: setattr(self.bg, 'pos', v),
                   size=lambda i,v: setattr(self.bg, 'size', v))
        
        # 导航栏 - 更大的返回按钮
        nav = BoxLayout(size_hint=(1, 0.12), spacing=dp(10))
        back_btn = Button(
            text='◀ 返回',
            size_hint=(0.18, 1),
            font_size=get_font_size(20),
            background_color=get_color_from_hex('#FF7043'),
            background_normal=''
        )
        back_btn.bind(on_press=lambda x: setattr(self.manager, 'current', 'chinese_menu'))
        nav.add_widget(back_btn)
        
        nav.add_widget(Label(
            text='📖 学汉字',
            font_size=get_font_size(30),
            color=get_color_from_hex('#E65100'),
            bold=True,
            size_hint=(0.47, 1)
        ))
        
        # 难度选择 - 更大的按钮
        level_box = BoxLayout(size_hint=(0.35, 1), spacing=dp(8))
        for lv, text in [(1, '初级'), (2, '中级'), (3, '高级')]:
            btn = Button(
                text=text,
                font_size=get_font_size(14),
                background_color=get_color_from_hex('#4CAF50' if lv == self.current_level else '#BDBDBD'),
                background_normal=''
            )
            btn.level = lv
            btn.bind(on_press=self.change_level)
            level_box.add_widget(btn)
        nav.add_widget(level_box)
        layout.add_widget(nav)
        
        # 提示
        self.hint = Label(
            text='点击汉字卡片学习！',
            font_size=get_font_size(20),
            color=get_color_from_hex('#666666'),
            size_hint=(1, 0.08)
        )
        layout.add_widget(self.hint)
        
        # 汉字卡片区域 - 分页显示
        self.cards_grid = GridLayout(
            cols=4,
            spacing=dp(12),
            padding=dp(10),
            size_hint=(1, 0.65)
        )
        layout.add_widget(self.cards_grid)
        
        # 分页控制
        page_box = BoxLayout(size_hint=(1, 0.1), spacing=dp(20), padding=[dp(100), 0])
        
        self.prev_btn = Button(
            text='< 上一页',
            font_size=get_font_size(18),
            background_color=get_color_from_hex('#42A5F5'),
            background_normal='',
            size_hint=(0.3, 1)
        )
        self.prev_btn.bind(on_press=self.prev_page)
        page_box.add_widget(self.prev_btn)
        
        self.page_label = Label(
            text='第1页',
            font_size=get_font_size(18),
            color=get_color_from_hex('#666666'),
            size_hint=(0.4, 1)
        )
        page_box.add_widget(self.page_label)
        
        self.next_btn = Button(
            text='下一页 >',
            font_size=get_font_size(18),
            background_color=get_color_from_hex('#42A5F5'),
            background_normal='',
            size_hint=(0.3, 1)
        )
        self.next_btn.bind(on_press=self.next_page)
        page_box.add_widget(self.next_btn)
        
        layout.add_widget(page_box)
        
        self.add_widget(layout)
        self.load_cards()
    
    def change_level(self, instance):
        self.current_level = instance.level
        self.current_page = 0  # 切换等级时重置页码
        # 更新按钮颜色
        for btn in instance.parent.children:
            if hasattr(btn, 'level'):
                btn.background_color = get_color_from_hex(
                    '#4CAF50' if btn.level == self.current_level else '#BDBDBD'
                )
        self.load_cards()
    
    def load_cards(self):
        self.cards_grid.clear_widgets()
        all_words = ChineseData.get_words(level=self.current_level)
        
        # 计算分页
        total_pages = (len(all_words) + self.cards_per_page - 1) // self.cards_per_page
        start_idx = self.current_page * self.cards_per_page
        end_idx = min(start_idx + self.cards_per_page, len(all_words))
        words = all_words[start_idx:end_idx]
        
        colors = ['#FF6B6B', '#4ECDC4', '#45B7D1', '#96CEB4', '#DDA0DD', '#FFD93D',
                  '#FF9800', '#8BC34A', '#E91E63', '#9C27B0', '#00BCD4', '#CDDC39']
        
        for i, (char, pinyin, word, emoji) in enumerate(words):
            btn = Button(
                background_normal='',
                background_color=get_color_from_hex(colors[(start_idx + i) % len(colors)])
            )
            btn.markup = True
            btn.text = f'[size={int(sp(42))}][b]{char}[/b][/size]\n[size={int(sp(16))}]{pinyin}[/size]\n[size={int(sp(12))}]{word}[/size]'
            btn.char_data = (char, pinyin, word)
            btn.bind(on_press=self.on_card_press)
            self.cards_grid.add_widget(btn)
        
        # 补齐空位（保持布局整齐）
        for _ in range(self.cards_per_page - len(words)):
            self.cards_grid.add_widget(Label(text=''))
        
        # 更新分页信息
        self.page_label.text = f'第{self.current_page + 1}/{total_pages}页 (共{len(all_words)}字)'
        self.prev_btn.disabled = self.current_page == 0
        self.next_btn.disabled = self.current_page >= total_pages - 1
    
    def prev_page(self, instance):
        if self.current_page > 0:
            self.current_page -= 1
            self.load_cards()
    
    def next_page(self, instance):
        all_words = ChineseData.get_words(level=self.current_level)
        total_pages = (len(all_words) + self.cards_per_page - 1) // self.cards_per_page
        if self.current_page < total_pages - 1:
            self.current_page += 1
            self.load_cards()
    
    def on_card_press(self, instance):
        if hasattr(instance, 'char_data'):
            char, pinyin, word = instance.char_data
            # 朗读汉字
            speak(char)
            # 跳转到详情页面
            detail_screen = self.manager.get_screen('chinese_detail')
            detail_screen.show_char(char, pinyin, word)
            self.manager.current = 'chinese_detail'
    
    def reset_card_color(self, btn):
        colors = ['#FF6B6B', '#4ECDC4', '#45B7D1', '#96CEB4', '#DDA0DD', '#FFD93D']
        btn.background_color = get_color_from_hex(random.choice(colors))


class ChineseDetailScreen(Screen):
    """汉字详情页面 - 显示汉字的详细信息"""
    
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.current_char = None
        self.build_ui()
    
    def build_ui(self):
        layout = BoxLayout(orientation='vertical', padding=get_padding(), spacing=dp(10))
        
        with layout.canvas.before:
            Color(*get_color_from_hex('#FFFDE7'))
            self.bg = Rectangle(pos=layout.pos, size=layout.size)
        layout.bind(pos=lambda i,v: setattr(self.bg, 'pos', v),
                   size=lambda i,v: setattr(self.bg, 'size', v))
        
        # 导航栏
        nav = BoxLayout(size_hint=(1, 0.1))
        back_btn = Button(
            text='< 返回',
            size_hint=(0.15, 1),
            font_size=get_font_size(18),
            background_color=get_color_from_hex('#FF7043'),
            background_normal=''
        )
        back_btn.bind(on_press=lambda x: setattr(self.manager, 'current', 'chinese_learn'))
        nav.add_widget(back_btn)
        
        nav.add_widget(Label(
            text='【汉字详情】点击可朗读',
            font_size=get_font_size(24),
            color=get_color_from_hex('#E65100'),
            bold=True,
            size_hint=(0.7, 1)
        ))
        nav.add_widget(Label(text='', size_hint=(0.15, 1)))
        layout.add_widget(nav)
        
        # 主内容区域
        content = BoxLayout(orientation='horizontal', size_hint=(1, 0.8), spacing=dp(20))
        
        # 左侧：大汉字显示（可点击）
        left_box = BoxLayout(orientation='vertical', size_hint=(0.4, 1))
        
        # 汉字按钮（点击朗读）
        self.char_btn = Button(
            text='字',
            font_size=get_font_size(160),
            color=get_color_from_hex('#E65100'),
            background_color=get_color_from_hex('#FFF8E1'),
            background_normal='',
            size_hint=(1, 0.7)
        )
        self.char_btn.bind(on_press=self.speak_char)
        left_box.add_widget(self.char_btn)
        
        self.pinyin_label = Label(
            text='pīnyīn',
            font_size=get_font_size(36),
            color=get_color_from_hex('#666666'),
            size_hint=(1, 0.3)
        )
        left_box.add_widget(self.pinyin_label)
        
        content.add_widget(left_box)
        
        # 右侧：详细信息（都可点击朗读）
        right_box = BoxLayout(orientation='vertical', size_hint=(0.6, 1), spacing=dp(10), padding=dp(10))
        
        # 组词（可点击）
        word_box = BoxLayout(orientation='vertical', size_hint=(1, 0.28))
        word_box.add_widget(Label(
            text='[组词] 点击朗读',
            font_size=get_font_size(16),
            color=get_color_from_hex('#4CAF50'),
            bold=True,
            halign='left',
            size_hint=(1, 0.3)
        ))
        self.word_btn = Button(
            text='词语',
            font_size=get_font_size(36),
            color=get_color_from_hex('#333333'),
            background_color=get_color_from_hex('#E8F5E9'),
            background_normal='',
            size_hint=(1, 0.7)
        )
        self.word_btn.bind(on_press=self.speak_word)
        word_box.add_widget(self.word_btn)
        right_box.add_widget(word_box)
        
        # 造句（可点击）
        sentence_box = BoxLayout(orientation='vertical', size_hint=(1, 0.38))
        sentence_box.add_widget(Label(
            text='[造句] 点击朗读',
            font_size=get_font_size(16),
            color=get_color_from_hex('#2196F3'),
            bold=True,
            halign='left',
            size_hint=(1, 0.2)
        ))
        self.sentence_btn = Button(
            text='例句',
            font_size=get_font_size(22),
            color=get_color_from_hex('#333333'),
            background_color=get_color_from_hex('#E3F2FD'),
            background_normal='',
            size_hint=(1, 0.8),
            halign='center',
            valign='middle'
        )
        self.sentence_btn.bind(on_press=self.speak_sentence)
        self.sentence_btn.bind(size=lambda *x: setattr(self.sentence_btn, 'text_size', (self.sentence_btn.width - dp(20), None)))
        sentence_box.add_widget(self.sentence_btn)
        right_box.add_widget(sentence_box)
        
        # 小提示（可点击）
        tip_box = BoxLayout(orientation='vertical', size_hint=(1, 0.34))
        tip_box.add_widget(Label(
            text='[小提示] 点击朗读',
            font_size=get_font_size(16),
            color=get_color_from_hex('#FF9800'),
            bold=True,
            halign='left',
            size_hint=(1, 0.25)
        ))
        self.tip_btn = Button(
            text='提示内容',
            font_size=get_font_size(20),
            color=get_color_from_hex('#666666'),
            background_color=get_color_from_hex('#FFF3E0'),
            background_normal='',
            size_hint=(1, 0.75),
            halign='center',
            valign='middle'
        )
        self.tip_btn.bind(on_press=self.speak_tip)
        self.tip_btn.bind(size=lambda *x: setattr(self.tip_btn, 'text_size', (self.tip_btn.width - dp(20), None)))
        tip_box.add_widget(self.tip_btn)
        right_box.add_widget(tip_box)
        
        content.add_widget(right_box)
        layout.add_widget(content)
        
        self.add_widget(layout)
    
    def speak_char(self, instance):
        """朗读汉字"""
        if self.current_char:
            speak(self.current_char)
    
    def speak_word(self, instance):
        """朗读词语"""
        speak(self.word_btn.text)
    
    def speak_sentence(self, instance):
        """朗读句子"""
        speak(self.sentence_btn.text)
    
    def speak_tip(self, instance):
        """朗读提示"""
        speak(self.tip_btn.text)
    
    def show_char(self, char, pinyin, word):
        """显示汉字详情"""
        self.current_char = char
        self.char_btn.text = char
        self.pinyin_label.text = pinyin
        self.word_btn.text = word
        
        # 进入页面时自动朗读汉字
        Clock.schedule_once(lambda dt: speak(char), 0.3)
        
        # 根据汉字生成造句和提示
        sentences = {
            '人': '我是一个小人儿。',
            '口': '我有一张小嘴巴。',
            '手': '我有两只小手。',
            '足': '我喜欢踢足球。',
            '日': '太阳公公出来了。',
            '月': '月亮弯弯像小船。',
            '水': '我要喝水。',
            '火': '火很烫，不能碰。',
            '山': '山上有很多树。',
            '石': '石头硬硬的。',
            '田': '农民伯伯在田里种菜。',
            '土': '小草从土里长出来。',
            '大': '大象的耳朵大大的。',
            '小': '小鸟在树上唱歌。',
            '上': '飞机飞到天上去了。',
            '下': '小雨从天上落下来。',
            '左': '我的左手拿着书。',
            '右': '我的右手拿着笔。',
            '天': '天空是蓝色的。',
            '地': '小草在地上生长。',
            '花': '花儿真漂亮。',
            '草': '小草绿绿的。',
            '树': '大树高高的。',
            '鸟': '小鸟会飞。',
            '爸': '爸爸爱我。',
            '妈': '妈妈做饭很好吃。',
            '爷': '爷爷给我讲故事。',
            '奶': '奶奶做的饼干真好吃。',
            '哥': '哥哥带我去玩。',
            '姐': '姐姐教我画画。',
            '弟': '弟弟很可爱。',
            '妹': '妹妹喜欢唱歌。',
            '吃': '我爱吃苹果。',
            '喝': '多喝水身体好。',
            '看': '我喜欢看书。',
            '听': '我在听音乐。',
        }
        
        tips = {
            '人': '人字像一个人站着的样子',
            '口': '口字像张开的嘴巴',
            '手': '手字上面是手指',
            '足': '足字下面像脚',
            '日': '日字像太阳',
            '月': '月字像弯弯的月亮',
            '水': '水字像流动的水',
            '火': '火字像燃烧的火焰',
            '山': '山字像三座山峰',
            '石': '石字像一块石头',
            '田': '田字像田地的样子',
            '土': '土字像土堆',
            '大': '大字像人张开双臂',
            '小': '小字中间一竖两边两点',
            '上': '上字一横在上面',
            '下': '下字一横在下面',
            '左': '左字有个工字',
            '右': '右字有个口字',
            '天': '天字像人头顶着天',
            '地': '地字有个土字旁',
            '花': '花字有个草字头',
            '草': '草字有个草字头',
            '树': '树字有个木字旁',
            '鸟': '鸟字像一只小鸟',
        }
        
        self.sentence_btn.text = sentences.get(char, f'我认识"{char}"这个字。')
        self.tip_btn.text = tips.get(char, f'"{char}"是一个常用字')


class ChineseQuizScreen(Screen):
    """汉字测验 - 选择题模式 - 触摸优化"""
    
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.logic = GameLogic()
        self.session = None
        self.current_word = None
        self.build_ui()
    
    def build_ui(self):
        layout = BoxLayout(orientation='vertical', padding=get_padding(), spacing=get_spacing())
        
        with layout.canvas.before:
            Color(*get_color_from_hex('#E8F5E9'))
            self.bg = Rectangle(pos=layout.pos, size=layout.size)
        layout.bind(pos=lambda i,v: setattr(self.bg, 'pos', v),
                   size=lambda i,v: setattr(self.bg, 'size', v))
        
        # 导航栏 - 更大的按钮
        nav = BoxLayout(size_hint=(1, 0.12), spacing=dp(10))
        back_btn = Button(
            text='◀ 返回',
            size_hint=(0.18, 1),
            font_size=get_font_size(20),
            background_color=get_color_from_hex('#66BB6A'),
            background_normal=''
        )
        back_btn.bind(on_press=lambda x: setattr(self.manager, 'current', 'chinese_menu'))
        nav.add_widget(back_btn)
        
        nav.add_widget(Label(
            text='❓ 汉字测验',
            font_size=get_font_size(30),
            color=get_color_from_hex('#2E7D32'),
            bold=True,
            size_hint=(0.47, 1)
        ))
        
        self.score_label = Label(
            text='⭐ 0',
            font_size=get_font_size(22),
            color=get_color_from_hex('#FF6B6B'),
            size_hint=(0.18, 1)
        )
        nav.add_widget(self.score_label)
        
        self.progress_label = Label(
            text='0/10',
            font_size=get_font_size(20),
            color=get_color_from_hex('#666666'),
            size_hint=(0.17, 1)
        )
        nav.add_widget(self.progress_label)
        layout.add_widget(nav)
        
        # 题目提示
        self.question_label = Label(
            text='听声音，选汉字！',
            font_size=get_font_size(26),
            color=get_color_from_hex('#333333'),
            size_hint=(1, 0.08)
        )
        layout.add_widget(self.question_label)
        
        # 播放按钮 - 更大更明显
        self.play_btn = Button(
            text='🔊 点击听声音',
            font_size=get_font_size(40),
            background_color=get_color_from_hex('#FF9800'),
            background_normal='',
            size_hint=(1, 0.28)
        )
        self.play_btn.bind(on_press=self.play_sound)
        layout.add_widget(self.play_btn)
        
        # 反馈
        self.feedback_label = Label(
            text='',
            font_size=get_font_size(26),
            color=get_color_from_hex('#4CAF50'),
            size_hint=(1, 0.08)
        )
        layout.add_widget(self.feedback_label)
        
        # 答案按钮 - 大按钮便于儿童触摸
        self.answers_layout = GridLayout(
            cols=2,
            spacing=screen_adapter.card_spacing(),  # 更大间距
            padding=dp(15),
            size_hint=(1, 0.32)
        )
        layout.add_widget(self.answers_layout)
        
        # 开始按钮 - 更大
        self.start_btn = Button(
            text='🎮 开始测验',
            font_size=get_font_size(26),
            size_hint=(1, 0.12),
            background_color=get_color_from_hex('#FF9800'),
            background_normal=''
        )
        self.start_btn.bind(on_press=self.start_game)
        layout.add_widget(self.start_btn)
        
        self.add_widget(layout)
    
    def start_game(self, instance):
        self.session = self.logic.create_session(GameType.QUIZ, total_questions=10)
        self.score_label.text = '⭐ 0'
        self.feedback_label.text = ''
        self.start_btn.text = '🔄 重新开始'
        self.next_question()
    
    def play_sound(self, instance):
        """点击播放按钮再听一遍"""
        if self.current_word:
            speak(self.current_word[0])
    
    def next_question(self):
        if self.session.is_complete():
            self.show_result()
            return
        
        words = ChineseData.get_words(level=2)
        self.current_word = random.choice(words)
        char, pinyin, word, emoji = self.current_word
        
        # 听声音选字模式
        self.play_btn.text = '🔊 点击听声音'
        self.question_label.text = '听声音，选出正确的汉字！'
        
        # 自动播放声音
        Clock.schedule_once(lambda dt: speak(char), 0.5)
        
        # 生成汉字选项 - 使用更大的按钮
        self.answers_layout.clear_widgets()
        all_chars = [w[0] for w in words]
        options = self.logic.get_random_options(char, all_chars, count=4)
        
        colors = ['#FF6B6B', '#4ECDC4', '#45B7D1', '#96CEB4']
        for i, opt in enumerate(options):
            btn = Button(
                text=opt,
                font_size=get_font_size(64),  # 更大的字体
                background_color=get_color_from_hex(colors[i]),
                background_normal='',
                bold=True,
                size_hint_min=(dp(120), dp(80))  # 最小尺寸
            )
            btn.bind(on_press=self.on_answer)
            self.answers_layout.add_widget(btn)
        
        self.progress_label.text = f'{self.session.current_question + 1}/10'
    
    def on_answer(self, instance):
        if self.current_word is None:
            return
        
        user_answer = instance.text
        correct_answer = self.current_word[0]
        
        is_correct = self.logic.check_answer(self.session, user_answer, correct_answer)
        
        if is_correct:
            self.feedback_label.text = f'✅ 太棒了！就是 "{correct_answer}"'
            self.feedback_label.color = get_color_from_hex('#4CAF50')
            instance.background_color = get_color_from_hex('#4CAF50')
            play_praise()  # 播放表扬
        else:
            self.feedback_label.text = f'❌ 不对哦，是 "{correct_answer}"'
            self.feedback_label.color = get_color_from_hex('#F44336')
            instance.background_color = get_color_from_hex('#F44336')
            play_encourage()  # 播放鼓励
        
        self.score_label.text = f'⭐ {self.session.score}'
        
        for btn in self.answers_layout.children:
            btn.disabled = True
        
        Clock.schedule_once(lambda dt: self.next_question(), 1.5)
    
    def show_result(self):
        stars = self.logic.calculate_stars(self.session)
        praise = self.logic.get_praise_message(self.session.accuracy)
        star_text = '★' * stars + '☆' * (3 - stars)
        self.question_label.text = f'{star_text} 测验完成！'
        self.play_btn.text = '棒！'
        self.feedback_label.text = f'{praise}\n正确率: {self.session.accuracy*100:.0f}%'


class ChineseMatchScreen(Screen):
    """汉字配对游戏"""
    
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.logic = GameLogic()
        self.cards = []
        self.card_data = []
        self.selected = None
        self.matched = set()
        self.score = 0
        self.build_ui()
    
    def build_ui(self):
        layout = BoxLayout(orientation='vertical', padding=get_padding(), spacing=dp(10))
        
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
            background_color=get_color_from_hex('#42A5F5'),
            background_normal=''
        )
        back_btn.bind(on_press=lambda x: setattr(self.manager, 'current', 'chinese_menu'))
        nav.add_widget(back_btn)
        
        nav.add_widget(Label(
            text='【汉字配对】',
            font_size=get_font_size(28),
            color=get_color_from_hex('#1565C0'),
            bold=True,
            size_hint=(0.55, 1)
        ))
        
        self.score_label = Label(
            text='得分: 0',
            font_size=get_font_size(20),
            color=get_color_from_hex('#FF6B6B'),
            size_hint=(0.15, 1)
        )
        nav.add_widget(self.score_label)
        nav.add_widget(Label(text='', size_hint=(0.15, 1)))
        layout.add_widget(nav)
        
        # 提示
        self.hint_label = Label(
            text='找到汉字和图片配对！',
            font_size=get_font_size(20),
            color=get_color_from_hex('#666666'),
            size_hint=(1, 0.08)
        )
        layout.add_widget(self.hint_label)
        
        # 反馈
        self.feedback_label = Label(
            text='',
            font_size=get_font_size(22),
            color=get_color_from_hex('#4CAF50'),
            size_hint=(1, 0.08)
        )
        layout.add_widget(self.feedback_label)
        
        # 卡片区域
        self.cards_layout = GridLayout(
            cols=4,
            spacing=dp(12),
            padding=dp(15),
            size_hint=(1, 0.54)
        )
        layout.add_widget(self.cards_layout)
        
        # 开始按钮
        self.start_btn = Button(
            text='开始游戏',
            font_size=get_font_size(24),
            size_hint=(1, 0.1),
            background_color=get_color_from_hex('#42A5F5'),
            background_normal=''
        )
        self.start_btn.bind(on_press=self.start_game)
        layout.add_widget(self.start_btn)
        
        self.add_widget(layout)
    
    def start_game(self, instance):
        self.cards = []
        self.card_data = []
        self.selected = None
        self.matched = set()
        self.score = 0
        self.score_label.text = '得分: 0'
        self.feedback_label.text = ''
        self.start_btn.text = '重新开始'
        
        self.cards_layout.clear_widgets()
        
        # 选择有明确图片的汉字
        words = ChineseData.get_words(level=2)
        picture_chars = ['日', '月', '山', '水', '火', '人', '口', '手', '花', '树', '鸟', '草']
        available = [w for w in words if w[0] in picture_chars]
        selected = random.sample(available, min(6, len(available)))
        
        # 汉字对应的图片描述（用中文代替emoji）
        char_pics = {
            '日': '太阳', '月': '月亮', '山': '高山', '水': '水滴', '火': '火焰',
            '人': '小人', '口': '嘴巴', '手': '小手', '足': '脚丫', '花': '鲜花',
            '树': '大树', '鸟': '小鸟', '草': '小草', '石': '石头', '田': '田地',
            '大': '大的', '小': '小的', '天': '天空', '地': '大地'
        }
        
        # 创建配对数据：汉字 + 图片描述
        for char, pinyin, word, emoji in selected:
            self.card_data.append({'type': 'char', 'value': char, 'match_id': char})
            pic = char_pics.get(char, '?')
            self.card_data.append({'type': 'picture', 'value': pic, 'match_id': char})
        
        random.shuffle(self.card_data)
        
        colors = ['#FFB6C1', '#98FB98', '#87CEEB', '#DDA0DD', '#F0E68C', '#FFA07A',
                  '#B0E0E6', '#FFE4B5', '#E6E6FA', '#FFDAB9', '#D8BFD8', '#F5DEB3']
        
        for i in range(12):
            card = self.card_data[i]
            btn = Button(
                text='?',
                font_size=get_font_size(36),
                background_color=get_color_from_hex(colors[i]),
                background_normal=''
            )
            btn.card_index = i
            btn.card_value = card['value']
            btn.card_type = card['type']
            btn.original_color = get_color_from_hex(colors[i])
            btn.bind(on_press=self.on_card_press)
            self.cards_layout.add_widget(btn)
            self.cards.append(btn)
        
        # 先显示所有卡片3秒
        self.show_all_cards()
        Clock.schedule_once(lambda dt: self.hide_all_cards(), 3.0)
    
    def show_all_cards(self):
        for i, btn in enumerate(self.cards):
            btn.text = self.card_data[i]['value']
        self.hint_label.text = '记住位置！3秒后翻回去...'
    
    def hide_all_cards(self):
        for i, btn in enumerate(self.cards):
            if i not in self.matched:
                btn.text = '?'
        self.hint_label.text = '点击卡片找配对！'
    
    def on_card_press(self, instance):
        idx = instance.card_index
        if idx in self.matched:
            return
        
        instance.text = self.card_data[idx]['value']
        
        if self.selected is None:
            self.selected = idx
            instance.background_color = get_color_from_hex('#FFEB3B')
        else:
            first_idx = self.selected
            first_btn = self.cards[first_idx]
            first_data = self.card_data[first_idx]
            second_data = self.card_data[idx]
            
            if (first_data['match_id'] == second_data['match_id'] and 
                first_data['type'] != second_data['type'] and first_idx != idx):
                # 配对成功
                self.score += 20
                self.score_label.text = f'得分: {self.score}'
                self.matched.add(first_idx)
                self.matched.add(idx)
                first_btn.background_color = get_color_from_hex('#4CAF50')
                instance.background_color = get_color_from_hex('#4CAF50')
                self.feedback_label.text = f'太棒了！{first_data["match_id"]} 配对成功！'
                self.feedback_label.color = get_color_from_hex('#4CAF50')
                play_praise()  # 播放表扬
                
                if len(self.matched) == 12:
                    Clock.schedule_once(lambda dt: self.show_complete(), 1.0)
            else:
                self.feedback_label.text = '不是配对，再试试！'
                self.feedback_label.color = get_color_from_hex('#FF9800')
                play_encourage()  # 播放鼓励
                Clock.schedule_once(lambda dt: self.flip_back(first_idx, idx), 1.0)
            
            self.selected = None
    
    def flip_back(self, idx1, idx2):
        if idx1 not in self.matched:
            self.cards[idx1].text = '?'
            self.cards[idx1].background_color = self.cards[idx1].original_color
        if idx2 not in self.matched:
            self.cards[idx2].text = '?'
            self.cards[idx2].background_color = self.cards[idx2].original_color
    
    def show_complete(self):
        self.hint_label.text = '★★★ 太厉害了！全部配对成功！★★★'
        self.feedback_label.text = f'总得分: {self.score}'
        self.feedback_label.color = get_color_from_hex('#FF6B6B')


class ChineseWhackScreen(Screen):
    """汉字打地鼠游戏"""
    
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.logic = GameLogic()
        self.session = None
        self.target_char = None
        self.holes = []
        self.hole_states = [None] * 9
        self.game_active = False
        self.spawn_event = None
        self.build_ui()
    
    def build_ui(self):
        layout = BoxLayout(orientation='vertical', padding=get_padding(), spacing=dp(10))
        
        with layout.canvas.before:
            Color(*get_color_from_hex('#90EE90'))
            self.bg = Rectangle(pos=layout.pos, size=layout.size)
        layout.bind(pos=lambda i,v: setattr(self.bg, 'pos', v),
                   size=lambda i,v: setattr(self.bg, 'size', v))
        
        # 导航栏
        nav = BoxLayout(size_hint=(1, 0.08))
        back_btn = Button(
            text='< 返回',
            size_hint=(0.15, 1),
            font_size=get_font_size(18),
            background_color=get_color_from_hex('#228B22'),
            background_normal=''
        )
        back_btn.bind(on_press=self.go_back)
        nav.add_widget(back_btn)
        
        nav.add_widget(Label(
            text='【汉字打地鼠】',
            font_size=get_font_size(26),
            color=get_color_from_hex('#006400'),
            bold=True,
            size_hint=(0.55, 1)
        ))
        
        self.score_label = Label(
            text='得分: 0',
            font_size=get_font_size(20),
            color=get_color_from_hex('#FF6B6B'),
            size_hint=(0.15, 1)
        )
        nav.add_widget(self.score_label)
        
        self.round_label = Label(
            text='0/10',
            font_size=get_font_size(18),
            color=get_color_from_hex('#333333'),
            size_hint=(0.15, 1)
        )
        nav.add_widget(self.round_label)
        layout.add_widget(nav)
        
        # 目标提示 - 大字体显眼
        target_box = BoxLayout(size_hint=(1, 0.12), padding=[dp(50), dp(5)])
        target_bg = Button(
            text='',
            background_color=get_color_from_hex('#FFD700'),
            background_normal='',
            size_hint=(1, 1)
        )
        target_box.add_widget(target_bg)
        layout.add_widget(target_box)
        
        self.target_label = Label(
            text='点击开始游戏！',
            font_size=get_font_size(32),
            color=get_color_from_hex('#DC143C'),
            size_hint=(1, 0.01)
        )
        layout.add_widget(self.target_label)
        
        # 反馈
        self.feedback_label = Label(
            text='',
            font_size=get_font_size(22),
            color=get_color_from_hex('#4CAF50'),
            size_hint=(1, 0.08)
        )
        layout.add_widget(self.feedback_label)
        
        # 地鼠洞网格 3x3 - 大按钮便于触摸
        self.holes_layout = GridLayout(
            cols=3,
            spacing=dp(15),
            padding=dp(20),
            size_hint=(1, 0.52)
        )
        
        hole_colors = ['#8B4513', '#A0522D', '#8B4513', '#A0522D', '#8B4513', '#A0522D',
                       '#8B4513', '#A0522D', '#8B4513']
        
        for i in range(9):
            hole_btn = Button(
                text='',
                font_size=get_font_size(52),
                background_color=get_color_from_hex(hole_colors[i]),
                background_normal='',
                color=get_color_from_hex('#000000')  # 黑色文字
            )
            hole_btn.hole_index = i
            hole_btn.bind(on_press=self.on_hole_press)
            self.holes_layout.add_widget(hole_btn)
            self.holes.append(hole_btn)
        
        layout.add_widget(self.holes_layout)
        
        # 开始按钮
        self.start_btn = Button(
            text='开始游戏',
            font_size=get_font_size(24),
            size_hint=(1, 0.1),
            background_color=get_color_from_hex('#FF9800'),
            background_normal=''
        )
        self.start_btn.bind(on_press=self.start_game)
        layout.add_widget(self.start_btn)
        
        self.add_widget(layout)
    
    def go_back(self, instance):
        self.stop_game()
        self.manager.current = 'chinese_menu'
    
    def start_game(self, instance):
        self.session = self.logic.create_session(GameType.WHACK, total_questions=10)
        self.score_label.text = '得分: 0'
        self.feedback_label.text = ''
        self.start_btn.text = '重新开始'
        self.game_active = True
        self.spawn_moles()
    
    def stop_game(self):
        self.game_active = False
        if self.spawn_event:
            self.spawn_event.cancel()
            self.spawn_event = None
        for hole in self.holes:
            hole.text = ''
            hole.background_color = get_color_from_hex('#8B4513')
        self.hole_states = [None] * 9
    
    def spawn_moles(self):
        if not self.game_active:
            return
        
        if self.session.current_question >= self.session.total_questions:
            self.show_result()
            return
        
        # 清空所有洞
        for i, hole in enumerate(self.holes):
            hole.text = ''
            hole.background_color = get_color_from_hex('#8B4513')
            self.hole_states[i] = None
        
        # 选择目标汉字
        words = ChineseData.get_words(level=2)
        target_word = random.choice(words)
        self.target_char = target_word[0]
        self.target_label.text = f'快找 {self.target_char}！'
        speak(f"快找{self.target_char}")
        
        # 随机选择3-4个洞放地鼠
        num_moles = random.randint(3, 4)
        mole_positions = random.sample(range(9), num_moles)
        
        # 确保目标汉字在其中
        others = random.sample([w for w in words if w[0] != self.target_char], num_moles - 1)
        char_list = [self.target_char] + [w[0] for w in others]
        random.shuffle(char_list)
        
        # 放置地鼠
        for i, pos in enumerate(mole_positions):
            hole = self.holes[pos]
            char = char_list[i]
            hole.text = char
            hole.background_color = get_color_from_hex('#FFEB3B')  # 亮黄色背景
            hole.color = get_color_from_hex('#000000')  # 黑色文字
            self.hole_states[pos] = char
        
        self.round_label.text = f'{self.session.current_question + 1}/10'
        
        # 3秒后地鼠消失
        self.spawn_event = Clock.schedule_once(self.moles_hide, 3.0)
    
    def moles_hide(self, dt):
        if not self.game_active:
            return
        
        self.feedback_label.text = f'错过了！目标是 {self.target_char}'
        self.feedback_label.color = get_color_from_hex('#FF9800')
        self.session.add_wrong()
        
        Clock.schedule_once(lambda dt: self.spawn_moles(), 1.0)
    
    def on_hole_press(self, instance):
        if not self.game_active:
            return
        
        idx = instance.hole_index
        char = self.hole_states[idx]
        
        if char is None:
            return
        
        # 取消自动隐藏
        if self.spawn_event:
            self.spawn_event.cancel()
        
        if char == self.target_char:
            # 打中目标
            self.session.add_correct(10)
            self.score_label.text = f'得分: {self.session.score}'
            self.feedback_label.text = f'太棒了！打中 {self.target_char}！'
            self.feedback_label.color = get_color_from_hex('#4CAF50')
            instance.background_color = get_color_from_hex('#4CAF50')
            instance.text = '棒!'
            play_praise()  # 播放表扬
        else:
            # 打错了
            self.session.add_wrong()
            self.feedback_label.text = f'打错了！要找 {self.target_char}'
            self.feedback_label.color = get_color_from_hex('#F44336')
            instance.background_color = get_color_from_hex('#F44336')
            instance.text = 'X'
            play_encourage()  # 播放鼓励
        
        self.hole_states[idx] = None
        Clock.schedule_once(lambda dt: self.spawn_moles(), 1.0)
    
    def show_result(self):
        self.game_active = False
        stars = self.logic.calculate_stars(self.session)
        praise = self.logic.get_praise_message(self.session.accuracy)
        star_text = '★' * stars + '☆' * (3 - stars)
        self.target_label.text = f'{star_text} 游戏完成！'
        self.feedback_label.text = f'{praise}\n正确率: {self.session.accuracy*100:.0f}%'
        self.feedback_label.color = get_color_from_hex('#FF9800')
        
        for hole in self.holes:
            hole.text = '棒'
            hole.background_color = get_color_from_hex('#4CAF50')


class ChinesePictureScreen(Screen):
    """看图选字游戏 - 根据图片/emoji选择正确的汉字"""
    
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.logic = GameLogic()
        self.session = None
        self.current_word = None
        self.build_ui()
    
    def build_ui(self):
        layout = BoxLayout(orientation='vertical', padding=get_padding(), spacing=dp(10))
        
        with layout.canvas.before:
            Color(*get_color_from_hex('#E1F5FE'))
            self.bg = Rectangle(pos=layout.pos, size=layout.size)
        layout.bind(pos=lambda i,v: setattr(self.bg, 'pos', v),
                   size=lambda i,v: setattr(self.bg, 'size', v))
        
        # 导航栏
        nav = BoxLayout(size_hint=(1, 0.1))
        back_btn = Button(
            text='< 返回',
            size_hint=(0.15, 1),
            font_size=get_font_size(18),
            background_color=get_color_from_hex('#4ECDC4'),
            background_normal=''
        )
        back_btn.bind(on_press=lambda x: setattr(self.manager, 'current', 'chinese_menu'))
        nav.add_widget(back_btn)
        
        nav.add_widget(Label(
            text='【看图选字】',
            font_size=get_font_size(28),
            color=get_color_from_hex('#00838F'),
            bold=True,
            size_hint=(0.5, 1)
        ))
        
        self.score_label = Label(
            text='得分: 0',
            font_size=get_font_size(20),
            color=get_color_from_hex('#FF6B6B'),
            size_hint=(0.2, 1)
        )
        nav.add_widget(self.score_label)
        
        self.progress_label = Label(
            text='0/10',
            font_size=get_font_size(18),
            color=get_color_from_hex('#666666'),
            size_hint=(0.15, 1)
        )
        nav.add_widget(self.progress_label)
        layout.add_widget(nav)
        
        # 提示
        self.hint_label = Label(
            text='看图片，选出正确的汉字！',
            font_size=get_font_size(22),
            color=get_color_from_hex('#333333'),
            size_hint=(1, 0.08)
        )
        layout.add_widget(self.hint_label)
        
        # 图片显示区 - 使用Canvas绘图
        picture_box = BoxLayout(size_hint=(1, 0.35), padding=dp(20))
        
        # 白色背景容器
        self.picture_container = BoxLayout()
        with self.picture_container.canvas.before:
            Color(1, 1, 1, 1)
            self.pic_bg = Rectangle(pos=self.picture_container.pos, size=self.picture_container.size)
        self.picture_container.bind(
            pos=lambda i,v: setattr(self.pic_bg, 'pos', v),
            size=lambda i,v: setattr(self.pic_bg, 'size', v)
        )
        
        # 绘图画布
        self.picture_canvas = PictureCanvas()
        self.picture_container.add_widget(self.picture_canvas)
        picture_box.add_widget(self.picture_container)
        layout.add_widget(picture_box)
        
        # 图片描述
        self.desc_label = Label(
            text='',
            font_size=get_font_size(24),
            color=get_color_from_hex('#666666'),
            size_hint=(1, 0.08)
        )
        layout.add_widget(self.desc_label)
        
        # 反馈
        self.feedback_label = Label(
            text='',
            font_size=get_font_size(22),
            color=get_color_from_hex('#4CAF50'),
            size_hint=(1, 0.08)
        )
        layout.add_widget(self.feedback_label)
        
        # 答案选项 - 4个大按钮
        self.answers_layout = GridLayout(
            cols=4,
            spacing=dp(15),
            padding=dp(20),
            size_hint=(1, 0.2)
        )
        layout.add_widget(self.answers_layout)
        
        # 开始按钮
        self.start_btn = Button(
            text='开始游戏',
            font_size=get_font_size(24),
            size_hint=(1, 0.1),
            background_color=get_color_from_hex('#4ECDC4'),
            background_normal=''
        )
        self.start_btn.bind(on_press=self.start_game)
        layout.add_widget(self.start_btn)
        
        self.add_widget(layout)
    
    def start_game(self, instance):
        self.session = self.logic.create_session(GameType.QUIZ, total_questions=10)
        self.score_label.text = '得分: 0'
        self.feedback_label.text = ''
        self.start_btn.text = '重新开始'
        self.next_question()
    
    def next_question(self):
        if self.session.is_complete():
            self.show_result()
            return
        
        words = ChineseData.get_words(level=2)
        self.current_word = random.choice(words)
        char, pinyin, word, emoji = self.current_word
        
        # 使用Canvas绘制图形
        self.picture_canvas.draw_char(char)
        
        # 显示提示文字
        picture_hints = {
            '人': '一个人站着', '口': '张开的嘴巴', '手': '五个手指', '足': '踢球的脚',
            '日': '圆圆的太阳', '月': '弯弯的月亮', '水': '流动的水滴', '火': '燃烧的火焰',
            '山': '高高的山峰', '石': '硬硬的石头', '田': '方方的田地', '土': '棕色的泥土',
            '大': '很大很大', '小': '很小很小', '上': '在上面', '下': '在下面',
            '天': '蓝蓝的天空', '地': '脚下的大地', '花': '漂亮的鲜花', '草': '绿绿的小草',
            '树': '高高的大树', '鸟': '飞翔的小鸟', '爸': '爸爸', '妈': '妈妈',
            '爷': '爷爷', '奶': '奶奶', '哥': '哥哥', '姐': '姐姐',
            '弟': '弟弟', '妹': '妹妹', '吃': '吃东西', '喝': '喝水',
            '看': '用眼睛看', '听': '用耳朵听', '左': '左边', '右': '右边',
        }
        hint_text = picture_hints.get(char, word)
        self.desc_label.text = f'提示：{hint_text}'
        
        # 生成选项
        self.answers_layout.clear_widgets()
        all_chars = [w[0] for w in words]
        options = self.logic.get_random_options(char, all_chars, count=4)
        
        colors = ['#FF6B6B', '#4ECDC4', '#45B7D1', '#96CEB4']
        for i, opt in enumerate(options):
            btn = Button(
                text=opt,
                font_size=get_font_size(56),
                background_color=get_color_from_hex(colors[i]),
                background_normal='',
                bold=True
            )
            btn.bind(on_press=self.on_answer)
            self.answers_layout.add_widget(btn)
        
        self.progress_label.text = f'{self.session.current_question + 1}/10'
    
    def on_answer(self, instance):
        if self.current_word is None:
            return
        
        user_answer = instance.text
        correct_answer = self.current_word[0]
        
        is_correct = self.logic.check_answer(self.session, user_answer, correct_answer)
        
        if is_correct:
            self.feedback_label.text = f'正确！这是 "{correct_answer}"'
            self.feedback_label.color = get_color_from_hex('#4CAF50')
            instance.background_color = get_color_from_hex('#4CAF50')
            play_praise()  # 播放表扬
        else:
            self.feedback_label.text = f'错误，正确答案是 "{correct_answer}"'
            self.feedback_label.color = get_color_from_hex('#F44336')
            instance.background_color = get_color_from_hex('#F44336')
            play_encourage()  # 播放鼓励
        
        self.score_label.text = f'得分: {self.session.score}'
        
        for btn in self.answers_layout.children:
            btn.disabled = True
        
        Clock.schedule_once(lambda dt: self.next_question(), 1.5)
    
    def show_result(self):
        stars = self.logic.calculate_stars(self.session)
        praise = self.logic.get_praise_message(self.session.accuracy)
        star_text = '★' * stars + '☆' * (3 - stars)
        self.hint_label.text = f'{star_text} 游戏完成！'
        self.picture_canvas.canvas.clear()
        with self.picture_canvas.canvas:
            Color(0.3, 0.7, 0.3)
            from kivy.graphics import Ellipse as E
            cx, cy = self.picture_canvas.center_x, self.picture_canvas.center_y
            E(pos=(cx-50, cy-50), size=(100, 100))
        self.desc_label.text = '太棒了!'
        self.feedback_label.text = f'{praise}\n正确率: {self.session.accuracy*100:.0f}%'


class ChineseChallengeScreen(Screen):
    """闯关模式 - 无时间压力，一关一关闯，解锁汪汪队狗狗"""
    
    # 每关解锁的狗狗
    LEVEL_PUPPIES = {
        1: ('阿奇', '警犬阿奇加入你的队伍！'),
        2: ('毛毛', '消防犬毛毛来帮忙啦！'),
        3: ('天天', '飞行犬天天飞来了！'),
        4: ('灰灰', '环保犬灰灰报到！'),
        5: ('路马', '水上救援路马来了！'),
        6: ('小砾', '工程犬小砾准备好了！'),
        7: ('珠珠', '雪地救援珠珠加入！'),
        8: ('小克', '丛林犬小克出动！'),
        9: ('莱德', '队长莱德为你骄傲！'),
        10: ('多个狗狗', '汪汪队全员集合！'),
    }
    
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.logic = GameLogic()
        self.current_word = None
        self.current_level = 1  # 当前关卡
        self.level_progress = 0  # 当前关卡进度 (0-4)
        self.level_correct = 0  # 当前关卡答对数
        self.total_score = 0
        self.unlocked_puppies = []  # 已解锁的狗狗
        self.popup = None  # 弹窗
        self.build_ui()
    
    def build_ui(self):
        layout = BoxLayout(orientation='vertical', padding=get_padding(), spacing=dp(10))
        
        with layout.canvas.before:
            Color(*get_color_from_hex('#F3E5F5'))
            self.bg = Rectangle(pos=layout.pos, size=layout.size)
        layout.bind(pos=lambda i,v: setattr(self.bg, 'pos', v),
                   size=lambda i,v: setattr(self.bg, 'size', v))
        
        # 导航栏
        nav = BoxLayout(size_hint=(1, 0.1))
        back_btn = Button(
            text='< 返回',
            size_hint=(0.15, 1),
            font_size=get_font_size(18),
            background_color=get_color_from_hex('#9C27B0'),
            background_normal=''
        )
        back_btn.bind(on_press=lambda x: setattr(self.manager, 'current', 'chinese_menu'))
        nav.add_widget(back_btn)
        
        nav.add_widget(Label(
            text='【闯关模式】',
            font_size=get_font_size(28),
            color=get_color_from_hex('#7B1FA2'),
            bold=True,
            size_hint=(0.4, 1)
        ))
        
        # 关卡显示
        self.level_label = Label(
            text='第1关',
            font_size=get_font_size(24),
            color=get_color_from_hex('#FF9800'),
            bold=True,
            size_hint=(0.15, 1)
        )
        nav.add_widget(self.level_label)
        
        self.score_label = Label(
            text='得分: 0',
            font_size=get_font_size(20),
            color=get_color_from_hex('#FF6B6B'),
            size_hint=(0.15, 1)
        )
        nav.add_widget(self.score_label)
        
        self.progress_label = Label(
            text='0/5',
            font_size=get_font_size(18),
            color=get_color_from_hex('#666666'),
            size_hint=(0.15, 1)
        )
        nav.add_widget(self.progress_label)
        layout.add_widget(nav)
        
        # 提示
        self.hint_label = Label(
            text='每关答对3题即可过关！',
            font_size=get_font_size(20),
            color=get_color_from_hex('#333333'),
            size_hint=(1, 0.08)
        )
        layout.add_widget(self.hint_label)
        
        # 星星进度显示
        self.stars_label = Label(
            text='☆ ☆ ☆',
            font_size=get_font_size(36),
            color=get_color_from_hex('#FFD700'),
            size_hint=(1, 0.08)
        )
        layout.add_widget(self.stars_label)
        
        # 汉字/词语显示
        self.char_label = Label(
            text='准备闯关',
            font_size=get_font_size(100),
            color=get_color_from_hex('#7B1FA2'),
            size_hint=(1, 0.25)
        )
        layout.add_widget(self.char_label)
        
        # 问题提示
        self.question_label = Label(
            text='点击开始，一起闯关吧！',
            font_size=get_font_size(22),
            color=get_color_from_hex('#666666'),
            size_hint=(1, 0.08)
        )
        layout.add_widget(self.question_label)
        
        # 反馈
        self.feedback_label = Label(
            text='',
            font_size=get_font_size(24),
            color=get_color_from_hex('#4CAF50'),
            size_hint=(1, 0.08)
        )
        layout.add_widget(self.feedback_label)
        
        # 答案按钮
        self.answers_layout = GridLayout(
            cols=4,
            spacing=dp(10),
            padding=dp(15),
            size_hint=(1, 0.22)
        )
        layout.add_widget(self.answers_layout)
        
        # 开始按钮
        self.start_btn = Button(
            text='开始闯关！',
            font_size=get_font_size(24),
            size_hint=(1, 0.1),
            background_color=get_color_from_hex('#9C27B0'),
            background_normal=''
        )
        self.start_btn.bind(on_press=self.start_game)
        layout.add_widget(self.start_btn)
        
        self.add_widget(layout)
    
    def start_game(self, instance):
        self.current_level = 1
        self.level_progress = 0
        self.level_correct = 0
        self.total_score = 0
        self.unlocked_puppies = []
        self.score_label.text = '得分: 0'
        self.level_label.text = '第1关'
        self.feedback_label.text = ''
        self.start_btn.text = '重新开始'
        self.update_stars()
        self.next_question()
    
    def update_stars(self):
        """更新星星显示"""
        filled = self.level_correct
        empty = 3 - filled
        self.stars_label.text = '★ ' * filled + '☆ ' * empty
    
    def next_question(self):
        # 检查是否过关
        if self.level_correct >= 3:
            self.level_complete()
            return
        
        # 检查是否本关失败（答了5题但没答对3题）
        if self.level_progress >= 5:
            self.level_failed()
            return
        
        words = ChineseData.get_words(level=2)
        self.current_word = random.choice(words)
        char, pinyin, word, emoji = self.current_word
        
        # 根据关卡调整难度
        if self.current_level <= 3:
            # 前3关：显示词语，选汉字（词语必须包含目标字）
            word_hints = {
                '人': '人们', '口': '门口', '手': '小手', '足': '足球',
                '日': '日出', '月': '月亮', '水': '喝水', '火': '火车',
                '山': '高山', '石': '石头', '田': '田地', '土': '泥土',
                '大': '大小', '小': '大小', '上': '上面', '下': '下面',
                '天': '天空', '地': '地上', '花': '花朵', '草': '小草',
                '树': '大树', '鸟': '小鸟', '爸': '爸爸', '妈': '妈妈',
                '爷': '爷爷', '奶': '奶奶', '哥': '哥哥', '姐': '姐姐',
                '弟': '弟弟', '妹': '妹妹', '吃': '吃饭', '喝': '喝水',
                '看': '看书', '听': '听歌', '左': '左边', '右': '右边',
            }
            hint_word = word_hints.get(char, word)
            # 确保提示词包含目标字
            if char not in hint_word:
                hint_word = word  # 用默认词组
            self.char_label.text = hint_word
            self.question_label.text = '找出里面的字！'
        else:
            # 4关以后：听声音选字
            self.char_label.text = '听'
            self.question_label.text = '听声音，选汉字！'
            Clock.schedule_once(lambda dt: speak(char), 0.3)
        
        # 生成汉字选项
        self.answers_layout.clear_widgets()
        all_chars = [w[0] for w in words]
        options = self.logic.get_random_options(char, all_chars, count=4)
        
        colors = ['#FF6B6B', '#4ECDC4', '#45B7D1', '#96CEB4']
        for i, opt in enumerate(options):
            btn = Button(
                text=opt,
                font_size=get_font_size(52),
                background_color=get_color_from_hex(colors[i]),
                background_normal='',
                bold=True
            )
            btn.bind(on_press=self.on_answer)
            self.answers_layout.add_widget(btn)
        
        self.progress_label.text = f'{self.level_progress + 1}/5'
    
    def on_answer(self, instance):
        if self.current_word is None:
            return
        
        user_answer = instance.text
        correct_answer = self.current_word[0]
        is_correct = user_answer == correct_answer
        
        self.level_progress += 1
        
        if is_correct:
            self.level_correct += 1
            self.total_score += 10 * self.current_level  # 关卡越高分数越多
            self.score_label.text = f'得分: {self.total_score}'
            self.feedback_label.text = '答对了！太棒了！'
            self.feedback_label.color = get_color_from_hex('#4CAF50')
            instance.background_color = get_color_from_hex('#4CAF50')
            play_praise()
        else:
            self.feedback_label.text = f'答案是 {correct_answer}，没关系继续！'
            self.feedback_label.color = get_color_from_hex('#FF9800')
            instance.background_color = get_color_from_hex('#FF9800')
            play_encourage()
        
        self.update_stars()
        
        for btn in self.answers_layout.children:
            btn.disabled = True
        
        Clock.schedule_once(lambda dt: self.next_question(), 1.2)
    
    def level_complete(self):
        """过关成功 - 显示解锁的狗狗"""
        completed_level = self.current_level
        
        # 获取解锁的狗狗
        if completed_level in self.LEVEL_PUPPIES:
            puppy_name, puppy_msg = self.LEVEL_PUPPIES[completed_level]
            self.unlocked_puppies.append(puppy_name)
            # 显示狗狗解锁弹窗
            self.show_puppy_unlock(puppy_name, puppy_msg, completed_level)
        else:
            # 没有狗狗解锁，直接进入下一关
            self._continue_after_unlock()
    
    def show_puppy_unlock(self, puppy_name, puppy_msg, level):
        """显示狗狗解锁弹窗"""
        from kivy.uix.modalview import ModalView
        from kivy.uix.image import Image
        
        # 创建弹窗
        popup = ModalView(size_hint=(0.8, 0.8), auto_dismiss=False)
        
        content = BoxLayout(orientation='vertical', padding=dp(20), spacing=dp(15))
        
        # 背景
        with content.canvas.before:
            Color(*get_color_from_hex('#FFF8E1'))
            self.popup_bg = Rectangle(pos=content.pos, size=content.size)
        content.bind(pos=lambda i,v: setattr(self.popup_bg, 'pos', v),
                    size=lambda i,v: setattr(self.popup_bg, 'size', v))
        
        # 标题
        content.add_widget(Label(
            text=f'第{level}关 过关！',
            font_size=get_font_size(32),
            color=get_color_from_hex('#FF6B00'),
            bold=True,
            size_hint=(1, 0.12)
        ))
        
        # 解锁提示
        content.add_widget(Label(
            text='解锁新队员！',
            font_size=get_font_size(24),
            color=get_color_from_hex('#4CAF50'),
            size_hint=(1, 0.08)
        ))
        
        # 狗狗图片
        import os
        img_path = os.path.join('汪汪队图片', f'{puppy_name}.jpg')
        if os.path.exists(img_path):
            img = Image(source=img_path, size_hint=(1, 0.5), allow_stretch=True)
            content.add_widget(img)
        else:
            content.add_widget(Label(
                text=puppy_name,
                font_size=get_font_size(60),
                color=get_color_from_hex('#FF6B00'),
                size_hint=(1, 0.5)
            ))
        
        # 狗狗消息
        content.add_widget(Label(
            text=puppy_msg,
            font_size=get_font_size(22),
            color=get_color_from_hex('#333333'),
            size_hint=(1, 0.1)
        ))
        
        # 继续按钮
        continue_btn = Button(
            text='继续闯关！',
            font_size=get_font_size(24),
            size_hint=(1, 0.12),
            background_color=get_color_from_hex('#4CAF50'),
            background_normal=''
        )
        continue_btn.bind(on_press=lambda x: self.close_popup_and_continue(popup))
        content.add_widget(continue_btn)
        
        popup.add_widget(content)
        popup.open()
        self.popup = popup
        
        # 播放语音
        speak(puppy_msg)
    
    def close_popup_and_continue(self, popup):
        """关闭弹窗并继续"""
        popup.dismiss()
        self._continue_after_unlock()
    
    def _continue_after_unlock(self):
        """解锁后继续游戏"""
        self.hint_label.text = f'过关啦！'
        self.char_label.text = '棒！'
        self.question_label.text = ''
        self.feedback_label.text = ''
        self.stars_label.text = '★ ★ ★'
        
        # 进入下一关
        self.current_level += 1
        self.level_progress = 0
        self.level_correct = 0
        
        if self.current_level > 10:
            # 通关了！
            Clock.schedule_once(lambda dt: self.game_complete(), 0.5)
        else:
            self.level_label.text = f'第{self.current_level}关'
            Clock.schedule_once(lambda dt: self.start_new_level(), 0.5)
    
    def start_new_level(self):
        self.hint_label.text = f'第{self.current_level}关开始！答对3题过关！'
        self.update_stars()
        self.next_question()
    
    def level_failed(self):
        """本关失败，可以重试"""
        self.hint_label.text = f'第{self.current_level}关 差一点点！'
        self.char_label.text = '加油'
        self.question_label.text = ''
        self.feedback_label.text = '点击重试本关'
        self.feedback_label.color = get_color_from_hex('#FF9800')
        self.answers_layout.clear_widgets()
        
        retry_btn = Button(
            text='重试本关',
            font_size=get_font_size(28),
            background_color=get_color_from_hex('#FF9800'),
            background_normal=''
        )
        retry_btn.bind(on_press=self.retry_level)
        self.answers_layout.add_widget(retry_btn)
    
    def retry_level(self, instance):
        self.level_progress = 0
        self.level_correct = 0
        self.hint_label.text = f'第{self.current_level}关 再来一次！'
        self.update_stars()
        self.next_question()
    
    def game_complete(self):
        """全部通关 - 显示收集的所有狗狗"""
        self.hint_label.text = '🏆 恭喜通关！你太厉害了！🏆'
        self.char_label.text = '冠军'
        self.stars_label.text = '🌟 🌟 🌟'
        self.question_label.text = f'总得分: {self.total_score}'
        self.feedback_label.text = f'收集了 {len(self.unlocked_puppies)} 只狗狗！'
        self.feedback_label.color = get_color_from_hex('#FFD700')
        self.answers_layout.clear_widgets()
        self.level_label.text = '通关！'
        speak("恭喜你，全部通关了，汪汪队全员为你骄傲！")




class ChineseWriteScreen(Screen):
    """描红写字 - 让小朋友直接在汉字上描写"""
    
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.current_char = None
        self.build_ui()
    
    def build_ui(self):
        layout = BoxLayout(orientation='vertical', padding=get_padding(), spacing=dp(10))
        
        with layout.canvas.before:
            Color(*get_color_from_hex('#FFF8E1'))
            self.bg = Rectangle(pos=layout.pos, size=layout.size)
        layout.bind(pos=lambda i,v: setattr(self.bg, 'pos', v),
                   size=lambda i,v: setattr(self.bg, 'size', v))
        
        # 导航栏
        nav = BoxLayout(size_hint=(1, 0.1))
        back_btn = Button(
            text='< 返回',
            size_hint=(0.12, 1),
            font_size=get_font_size(18),
            background_color=get_color_from_hex('#FF9800'),
            background_normal=''
        )
        back_btn.bind(on_press=lambda x: setattr(self.manager, 'current', 'chinese_menu'))
        nav.add_widget(back_btn)
        
        nav.add_widget(Label(
            text='【描红写字】',
            font_size=get_font_size(28),
            color=get_color_from_hex('#E65100'),
            bold=True,
            size_hint=(0.4, 1)
        ))
        
        # 朗读按钮
        speak_btn = Button(
            text='听',
            size_hint=(0.12, 1),
            font_size=get_font_size(18),
            background_color=get_color_from_hex('#2196F3'),
            background_normal=''
        )
        speak_btn.bind(on_press=self.speak_char)
        nav.add_widget(speak_btn)
        
        clear_btn = Button(
            text='清除',
            size_hint=(0.12, 1),
            font_size=get_font_size(18),
            background_color=get_color_from_hex('#F44336'),
            background_normal=''
        )
        clear_btn.bind(on_press=self.clear_canvas)
        nav.add_widget(clear_btn)
        
        next_btn = Button(
            text='换字',
            size_hint=(0.12, 1),
            font_size=get_font_size(18),
            background_color=get_color_from_hex('#4CAF50'),
            background_normal=''
        )
        next_btn.bind(on_press=self.next_char)
        nav.add_widget(next_btn)
        
        # 棒按钮（表扬）
        praise_btn = Button(
            text='棒!',
            size_hint=(0.12, 1),
            font_size=get_font_size(18),
            background_color=get_color_from_hex('#FF5722'),
            background_normal=''
        )
        praise_btn.bind(on_press=lambda x: play_praise())
        nav.add_widget(praise_btn)
        
        layout.add_widget(nav)
        
        self.hint_label = Label(
            text='用手指沿着红色的字描写吧！',
            font_size=get_font_size(22),
            color=get_color_from_hex('#666666'),
            size_hint=(1, 0.06)
        )
        layout.add_widget(self.hint_label)
        
        # 写字区域 - 大画布居中
        write_box = BoxLayout(size_hint=(1, 0.68), padding=dp(20))
        self.write_canvas = WriteCanvas()
        write_box.add_widget(self.write_canvas)
        layout.add_widget(write_box)
        
        # 底部汉字选择 - 两行
        char_container = BoxLayout(orientation='vertical', size_hint=(1, 0.16), spacing=dp(5))
        
        # 第一行
        char_box1 = BoxLayout(size_hint=(1, 0.5), spacing=dp(8), padding=[dp(5), 0])
        words1 = ChineseData.get_words(level=1)[:6]
        for char, pinyin, word, emoji in words1:
            btn = Button(text=char, font_size=get_font_size(28), background_color=get_color_from_hex('#FFB74D'), background_normal='')
            btn.bind(on_press=self.select_char)
            char_box1.add_widget(btn)
        char_container.add_widget(char_box1)
        
        # 第二行
        char_box2 = BoxLayout(size_hint=(1, 0.5), spacing=dp(8), padding=[dp(5), 0])
        words2 = ChineseData.get_words(level=1)[6:12]
        for char, pinyin, word, emoji in words2:
            btn = Button(text=char, font_size=get_font_size(28), background_color=get_color_from_hex('#81D4FA'), background_normal='')
            btn.bind(on_press=self.select_char)
            char_box2.add_widget(btn)
        char_container.add_widget(char_box2)
        
        layout.add_widget(char_container)
        
        self.add_widget(layout)
        self.select_char_by_name('人')
    
    def select_char(self, instance):
        self.select_char_by_name(instance.text)
    
    def select_char_by_name(self, char):
        self.current_char = char
        self.write_canvas.set_guide_char(char)
        self.clear_canvas(None)
        speak(char)
    
    def speak_char(self, instance):
        if self.current_char:
            speak(self.current_char)
    
    def clear_canvas(self, instance):
        self.write_canvas.clear_drawing()
    
    def next_char(self, instance):
        words = ChineseData.get_words(level=2)
        char = random.choice(words)[0]
        self.select_char_by_name(char)
        play_praise()


class WriteCanvas(Widget):
    """写字画布 - 汉字显示在中央，小朋友直接在上面描写"""
    
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.guide_char = '人'
        self.lines = []
        self.current_line = []
        # 创建用于显示汉字的Label
        self.char_label = Label(
            text='人',
            font_size=sp(200),
            color=(1, 0.8, 0.8, 0.6),  # 浅红色半透明
            halign='center',
            valign='middle'
        )
        self.add_widget(self.char_label)
        self.bind(size=self.on_resize, pos=self.on_resize)
        Clock.schedule_once(lambda dt: self.redraw(), 0.1)
    
    def on_resize(self, *args):
        # 让汉字Label填满画布
        self.char_label.size = self.size
        self.char_label.pos = self.pos
        self.char_label.text_size = self.size
        self.redraw()
    
    def set_guide_char(self, char):
        self.guide_char = char
        self.char_label.text = char
        self.redraw()
    
    def redraw(self, *args):
        self.canvas.before.clear()
        with self.canvas.before:
            # 白色背景
            Color(1, 1, 1, 1)
            Rectangle(pos=self.pos, size=self.size)
            
            # 米字格（浅灰色）
            Color(0.85, 0.85, 0.85, 1)
            cx, cy = self.center_x, self.center_y
            w, h = self.width, self.height
            # 横线
            Line(points=[self.x, cy, self.x + w, cy], width=1.5)
            # 竖线
            Line(points=[cx, self.y, cx, self.y + h], width=1.5)
            # 对角线
            Line(points=[self.x, self.y, self.x + w, self.y + h], width=1)
            Line(points=[self.x, self.y + h, self.x + w, self.y], width=1)
            
            # 边框（深一点）
            Color(0.7, 0.7, 0.7, 1)
            Line(rectangle=(self.x + 2, self.y + 2, w - 4, h - 4), width=3)
        
        # 重绘用户笔迹
        self.redraw_lines()
    
    def redraw_lines(self):
        self.canvas.after.clear()
        with self.canvas.after:
            # 用户笔迹用深蓝色粗线
            Color(0.1, 0.2, 0.7, 1)
            for line in self.lines:
                if len(line) >= 4:
                    Line(points=line, width=dp(6), cap='round', joint='round')
    
    def clear_drawing(self):
        self.lines = []
        self.current_line = []
        self.redraw()
    
    def on_touch_down(self, touch):
        if self.collide_point(*touch.pos):
            self.current_line = [touch.x, touch.y]
            touch.grab(self)
            return True
        return super().on_touch_down(touch)
    
    def on_touch_move(self, touch):
        if touch.grab_current is self:
            self.current_line.extend([touch.x, touch.y])
            # 实时绘制当前笔画
            self.canvas.after.clear()
            with self.canvas.after:
                Color(0.1, 0.2, 0.7, 1)
                for line in self.lines:
                    if len(line) >= 4:
                        Line(points=line, width=dp(6), cap='round', joint='round')
                if len(self.current_line) >= 4:
                    Line(points=self.current_line, width=dp(6), cap='round', joint='round')
            return True
        return super().on_touch_move(touch)
    
    def on_touch_up(self, touch):
        if touch.grab_current is self:
            touch.ungrab(self)
            if len(self.current_line) >= 4:
                self.lines.append(self.current_line[:])
            self.current_line = []
            self.redraw_lines()
            return True
        return super().on_touch_up(touch)
        return super().on_touch_move(touch)
    
    def on_touch_up(self, touch):
        if touch.grab_current is self:
            touch.ungrab(self)
            if len(self.current_line) >= 4:
                self.lines.append(self.current_line[:])
            self.current_line = []
            return True
        return super().on_touch_up(touch)





class ChineseStoryScreen(Screen):
    CHAR_STORIES = {
        '人': {
            'story': '很久很久以前，有一个聪明的古人想画一个人。他看到人站着的样子，两条腿稳稳地站在地上，身体微微弯曲。于是他画了一撇一捺，就像一个人侧着身子站立。从此，这个简单的符号就代表了人，一直用到今天！',
            'origin': '象形字，像人侧立的样子'
        },
        '口': {
            'story': '小朋友，你张开嘴巴看看镜子，嘴巴是不是方方的？古时候的人也发现了这个秘密！他们画了一个方方的框框，就像张开的嘴巴一样。吃饭要用口，说话要用口，唱歌也要用口，口字真重要！',
            'origin': '象形字，像张开的嘴巴'
        },
        '日': {
            'story': '每天早上，太阳公公从东边升起来，圆圆的，亮亮的，照得大地暖洋洋。古人抬头看太阳，画了一个圆圈，中间加一点表示光芒。后来圆圈变成了方框，就成了我们现在写的日字。日就是太阳！',
            'origin': '象形字，像圆圆的太阳'
        },
        '月': {
            'story': '晚上，月亮婆婆出来了。有时候月亮圆圆的像大饼，有时候弯弯的像小船。古人最喜欢弯弯的月牙，他们把月牙的样子画下来，就成了月字。月亮弯弯挂天上，照着小朋友做美梦！',
            'origin': '象形字，像弯弯的月牙'
        },
        '山': {
            'story': '远远望去，大山高高的，一座连着一座。中间的山峰最高，两边的矮一些。古人用三个尖尖的笔画，画出了山的样子。中间高，两边低，这就是山字！爬山虽然累，但是山顶的风景最美！',
            'origin': '象形字，像三座山峰'
        },
        '水': {
            'story': '小河里的水哗啦啦地流，溅起一朵朵小水花。古人蹲在河边看水流，看到水一弯一弯地往前跑。他们画出水流动的样子，弯弯曲曲的，就成了水字。水能喝，水能洗澡，水是生命之源！',
            'origin': '象形字，像流动的水波'
        },
        '火': {
            'story': '古时候，人们学会了生火。火苗跳啊跳，一会儿高一会儿低，上面尖尖的，下面宽宽的，还会噼里啪啦响。古人把火苗的样子画下来，就成了火字。火能取暖，火能做饭，但是小朋友不能玩火哦！',
            'origin': '象形字，像跳动的火苗'
        },
        '手': {
            'story': '伸出你的小手看一看，有手掌，有五个手指头。古人画手的时候，画出手腕和五个手指，就像一只张开的手。手可以拿东西，可以写字画画，可以拥抱爸爸妈妈，小手真能干！',
            'origin': '象形字，像张开的手掌'
        },
        '足': {
            'story': '低头看看你的小脚丫，有脚后跟，有脚趾头。古人画脚的时候，画出脚的形状，上面是小腿，下面是脚掌。足就是脚的意思。用足可以走路，可以跑步，可以踢足球！',
            'origin': '象形字，像脚的形状'
        },
        '鸟': {
            'story': '树上有只小鸟，它有尖尖的嘴巴，圆圆的眼睛，身上有漂亮的羽毛，还有一条长长的尾巴。古人把小鸟的样子画下来，头、身子、尾巴都有，就成了鸟字。小鸟会飞，会唱歌，真可爱！',
            'origin': '象形字，像一只小鸟'
        },
        '田': {
            'story': '农民伯伯的田地，方方正正的，中间有小路把田分成一块一块的。从高处往下看，田地就像一个井字格。古人画出田地的样子，外面一个大框，里面有十字，就成了田字。田里种庄稼，养活我们！',
            'origin': '象形字，像方正的田地'
        },
        '石': {
            'story': '山脚下有一块大石头，硬硬的，沉沉的，搬都搬不动。古人画石头的时候，上面画一个山崖，下面画一块石头。石头可以盖房子，可以铺路，石头真有用！',
            'origin': '象形字，像山崖下的石头'
        },
    }
    
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.current_char = None
        self.current_index = 0
        self.char_list = list(self.CHAR_STORIES.keys())
        self.build_ui()
    
    def build_ui(self):
        layout = BoxLayout(orientation='vertical', padding=get_padding(), spacing=dp(10))
        with layout.canvas.before:
            Color(*get_color_from_hex('#E8F5E9'))
            self.bg = Rectangle(pos=layout.pos, size=layout.size)
        layout.bind(pos=lambda i,v: setattr(self.bg, 'pos', v), size=lambda i,v: setattr(self.bg, 'size', v))
        
        nav = BoxLayout(size_hint=(1, 0.1))
        back_btn = Button(text='< 返回', size_hint=(0.15, 1), font_size=get_font_size(18), background_color=get_color_from_hex('#66BB6A'), background_normal='')
        back_btn.bind(on_press=lambda x: setattr(self.manager, 'current', 'chinese_menu'))
        nav.add_widget(back_btn)
        nav.add_widget(Label(text='【汉字故事】', font_size=get_font_size(28), color=get_color_from_hex('#2E7D32'), bold=True, size_hint=(0.4, 1)))
        prev_btn = Button(text='<', size_hint=(0.1, 1), font_size=get_font_size(24), background_color=get_color_from_hex('#81C784'), background_normal='')
        prev_btn.bind(on_press=self.prev_char)
        nav.add_widget(prev_btn)
        next_btn = Button(text='>', size_hint=(0.1, 1), font_size=get_font_size(24), background_color=get_color_from_hex('#81C784'), background_normal='')
        next_btn.bind(on_press=self.next_char)
        nav.add_widget(next_btn)
        listen_btn = Button(text='听故事', size_hint=(0.15, 1), font_size=get_font_size(18), background_color=get_color_from_hex('#FF9800'), background_normal='')
        listen_btn.bind(on_press=self.speak_story)
        nav.add_widget(listen_btn)
        layout.add_widget(nav)
        
        content = BoxLayout(orientation='horizontal', size_hint=(1, 0.75), spacing=dp(20), padding=dp(10))
        left_box = BoxLayout(orientation='vertical', size_hint=(0.35, 1))
        self.char_label = Label(text='人', font_size=get_font_size(180), color=get_color_from_hex('#2E7D32'), bold=True, size_hint=(1, 0.7))
        left_box.add_widget(self.char_label)
        self.origin_label = Label(text='象形字', font_size=get_font_size(18), color=get_color_from_hex('#666666'), size_hint=(1, 0.3))
        left_box.add_widget(self.origin_label)
        content.add_widget(left_box)
        
        right_box = BoxLayout(orientation='vertical', size_hint=(0.65, 1), padding=dp(10))
        self.title_label = Label(text='人 的故事', font_size=get_font_size(28), color=get_color_from_hex('#FF6B00'), bold=True, size_hint=(1, 0.15))
        right_box.add_widget(self.title_label)
        self.story_btn = Button(text='点击听故事...', font_size=get_font_size(24), background_color=get_color_from_hex('#FFF8E1'), background_normal='', color=get_color_from_hex('#333333'), size_hint=(1, 0.85), halign='center', valign='middle')
        self.story_btn.bind(on_press=self.speak_story)
        self.story_btn.bind(size=lambda *x: setattr(self.story_btn, 'text_size', (self.story_btn.width - dp(20), None)))
        right_box.add_widget(self.story_btn)
        content.add_widget(right_box)
        layout.add_widget(content)
        
        char_box = BoxLayout(size_hint=(1, 0.13), spacing=dp(8), padding=dp(5))
        for char in self.char_list:
            btn = Button(text=char, font_size=get_font_size(28), background_color=get_color_from_hex('#A5D6A7'), background_normal='')
            btn.bind(on_press=self.select_char)
            char_box.add_widget(btn)
        layout.add_widget(char_box)
        self.add_widget(layout)
        self.show_story('人')
    
    def select_char(self, instance):
        self.show_story(instance.text)
    
    def show_story(self, char):
        if char not in self.CHAR_STORIES:
            return
        self.current_char = char
        self.current_index = self.char_list.index(char) if char in self.char_list else 0
        data = self.CHAR_STORIES[char]
        self.char_label.text = char
        self.title_label.text = f'{char} 的故事'
        self.story_btn.text = data['story']
        self.origin_label.text = data['origin']
        speak(char)
    
    def speak_story(self, instance):
        if self.current_char and self.current_char in self.CHAR_STORIES:
            speak(self.CHAR_STORIES[self.current_char]['story'])
    
    def prev_char(self, instance):
        self.current_index = (self.current_index - 1) % len(self.char_list)
        self.show_story(self.char_list[self.current_index])
    
    def next_char(self, instance):
        self.current_index = (self.current_index + 1) % len(self.char_list)
        self.show_story(self.char_list[self.current_index])



class ChineseLearnApp(App):
    """乐乐的识字乐园 - Android/鸿蒙平板版"""
    
    def build(self):
        self.title = '乐乐的识字乐园'
        
        print("[App] 开始构建应用...")
        
        # 初始化音频（关键！）
        print("[App] 初始化音频模块...")
        audio_instance = init_audio()
        if audio_instance:
            print("[App] 音频模块初始化成功")
        else:
            print("[App] 警告：音频模块初始化失败")
        
        # 延迟播放欢迎语，等待TTS完全初始化（增加延迟时间）
        Clock.schedule_once(lambda dt: self._play_welcome(), 3.0)
        
        sm = ScreenManager(transition=FadeTransition())
        sm.add_widget(ChineseMenuScreen(name='chinese_menu'))
        sm.add_widget(ChineseLearnScreen(name='chinese_learn'))
        sm.add_widget(ChineseDetailScreen(name='chinese_detail'))
        sm.add_widget(ChineseQuizScreen(name='chinese_quiz'))
        sm.add_widget(ChineseMatchScreen(name='chinese_match'))
        sm.add_widget(ChineseWhackScreen(name='chinese_whack'))
        sm.add_widget(ChinesePictureScreen(name='chinese_picture'))
        sm.add_widget(ChineseChallengeScreen(name='chinese_challenge'))
        sm.add_widget(ChineseWriteScreen(name='chinese_write'))
        sm.add_widget(ChineseStoryScreen(name='chinese_story'))
        
        print("[App] 应用构建完成")
        return sm
    
    def _play_welcome(self):
        """播放欢迎语"""
        print("[App] 尝试播放欢迎语...")
        speak("欢迎来到乐乐的识字乐园")
    
    def on_pause(self):
        """Android/鸿蒙暂停时调用"""
        print("[App] 应用暂停")
        return True
    
    def on_resume(self):
        """Android/鸿蒙恢复时调用"""
        print("[App] 应用恢复")
        pass
    
    def on_stop(self):
        """应用停止时清理资源"""
        print("[App] 应用停止")
        if audio:
            try:
                audio.cleanup()
            except:
                pass


if __name__ == '__main__':
    ChineseLearnApp().run()
