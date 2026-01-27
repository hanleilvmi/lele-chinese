# -*- coding: utf-8 -*-
"""
乐乐的识字乐园 - Android平板优化版
专为3-5岁儿童设计的汉字学习应用
"""
import sys
import os

# 确保能找到模块
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

# 必须在导入kivy之前配置
import font_config

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
import random

from core.data_chinese import ChineseData
from core.game_logic import GameLogic, GameType
from picture_drawings import PictureCanvas

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
    return sp(base_size)


def get_padding():
    """根据屏幕大小动态计算内边距"""
    return dp(15)


class ChineseMenuScreen(Screen):
    """识字乐园主菜单 - 平板优化"""
    
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.build_ui()
    
    def build_ui(self):
        layout = BoxLayout(orientation='vertical', padding=get_padding(), spacing=dp(15))
        
        with layout.canvas.before:
            Color(*get_color_from_hex('#FFF8E1'))
            self.bg = Rectangle(pos=layout.pos, size=layout.size)
        layout.bind(pos=lambda i,v: setattr(self.bg, 'pos', v),
                   size=lambda i,v: setattr(self.bg, 'size', v))
        
        # 标题区域
        title_box = BoxLayout(size_hint=(1, 0.15))
        title_box.add_widget(Label(
            text='乐乐的识字乐园',
            font_size=get_font_size(36),
            color=get_color_from_hex('#E65100'),
            bold=True
        ))
        layout.add_widget(title_box)
        
        # 副标题
        layout.add_widget(Label(
            text='点击下面的游戏开始学习汉字吧！',
            font_size=get_font_size(18),
            color=get_color_from_hex('#666666'),
            size_hint=(1, 0.08)
        ))
        
        # 游戏选择区 - 3列布局更均匀
        games = GridLayout(cols=3, spacing=dp(15), size_hint=(1, 0.65), padding=dp(20))
        
        game_list = [
            ('字', '学汉字', '认识基础汉字', '#FF7043', 'chinese_learn'),
            ('图', '看图选字', '看图片选汉字', '#4ECDC4', 'chinese_picture'),
            ('?', '汉字测验', '考考你学会了吗', '#66BB6A', 'chinese_quiz'),
            ('对', '汉字配对', '找到相同的字', '#42A5F5', 'chinese_match'),
            ('锤', '打地鼠', '快速找汉字', '#FFD93D', 'chinese_whack'),
            ('关', '闯关模式', '一关一关闯', '#9C27B0', 'chinese_challenge'),
        ]
        
        for icon, title, desc, color, screen in game_list:
            btn = Button(
                background_normal='',
                background_color=get_color_from_hex(color)
            )
            btn.markup = True
            btn.text = f'[size={int(sp(42))}]{icon}[/size]\n[b][size={int(sp(20))}]{title}[/size][/b]\n[size={int(sp(12))}]{desc}[/size]'
            btn.target_screen = screen
            btn.bind(on_press=self.go_screen)
            games.add_widget(btn)
        
        layout.add_widget(games)
        
        # 底部信息
        bottom = BoxLayout(size_hint=(1, 0.1))
        bottom.add_widget(Label(
            text='适合3-5岁小朋友',
            font_size=get_font_size(14),
            color=get_color_from_hex('#999999')
        ))
        layout.add_widget(bottom)
        
        self.add_widget(layout)
    
    def go_screen(self, instance):
        if hasattr(instance, 'target_screen'):
            self.manager.current = instance.target_screen


class ChineseLearnScreen(Screen):
    """学汉字 - 卡片学习模式（分页）"""
    
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.current_level = 1
        self.current_page = 0
        self.cards_per_page = 12  # 每页12个汉字（3行x4列）
        self.build_ui()
    
    def build_ui(self):
        layout = BoxLayout(orientation='vertical', padding=get_padding(), spacing=dp(10))
        
        with layout.canvas.before:
            Color(*get_color_from_hex('#FFF3E0'))
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
        back_btn.bind(on_press=lambda x: setattr(self.manager, 'current', 'chinese_menu'))
        nav.add_widget(back_btn)
        
        nav.add_widget(Label(
            text='【学汉字】',
            font_size=get_font_size(28),
            color=get_color_from_hex('#E65100'),
            bold=True,
            size_hint=(0.5, 1)
        ))
        
        # 难度选择
        level_box = BoxLayout(size_hint=(0.35, 1), spacing=dp(5))
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
            text='🔊 组词（点击朗读）',
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
            text='🔊 造句（点击朗读）',
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
            text='🔊 小提示（点击朗读）',
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
    """汉字测验 - 选择题模式"""
    
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.logic = GameLogic()
        self.session = None
        self.current_word = None
        self.build_ui()
    
    def build_ui(self):
        layout = BoxLayout(orientation='vertical', padding=get_padding(), spacing=dp(15))
        
        with layout.canvas.before:
            Color(*get_color_from_hex('#E8F5E9'))
            self.bg = Rectangle(pos=layout.pos, size=layout.size)
        layout.bind(pos=lambda i,v: setattr(self.bg, 'pos', v),
                   size=lambda i,v: setattr(self.bg, 'size', v))
        
        # 导航栏
        nav = BoxLayout(size_hint=(1, 0.1))
        back_btn = Button(
            text='< 返回',
            size_hint=(0.15, 1),
            font_size=get_font_size(18),
            background_color=get_color_from_hex('#66BB6A'),
            background_normal=''
        )
        back_btn.bind(on_press=lambda x: setattr(self.manager, 'current', 'chinese_menu'))
        nav.add_widget(back_btn)
        
        nav.add_widget(Label(
            text='【汉字测验】',
            font_size=get_font_size(28),
            color=get_color_from_hex('#2E7D32'),
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
        
        # 题目提示
        self.question_label = Label(
            text='听声音，选汉字！',
            font_size=get_font_size(24),
            color=get_color_from_hex('#333333'),
            size_hint=(1, 0.1)
        )
        layout.add_widget(self.question_label)
        
        # 播放按钮（替代词组显示）
        self.play_btn = Button(
            text='🔊 点击听声音',
            font_size=get_font_size(36),
            background_color=get_color_from_hex('#FF9800'),
            background_normal='',
            size_hint=(1, 0.35)
        )
        self.play_btn.bind(on_press=self.play_sound)
        layout.add_widget(self.play_btn)
        
        # 反馈
        self.feedback_label = Label(
            text='',
            font_size=get_font_size(24),
            color=get_color_from_hex('#4CAF50'),
            size_hint=(1, 0.1)
        )
        layout.add_widget(self.feedback_label)
        
        # 答案按钮 - 大按钮便于触摸
        self.answers_layout = GridLayout(
            cols=2,
            spacing=dp(15),
            padding=dp(20),
            size_hint=(1, 0.25)
        )
        layout.add_widget(self.answers_layout)
        
        # 开始按钮
        self.start_btn = Button(
            text='开始测验',
            font_size=get_font_size(24),
            size_hint=(1, 0.1),
            background_color=get_color_from_hex('#FF9800'),
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
        
        # 生成汉字选项
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
            self.feedback_label.text = f'太棒了！就是 "{correct_answer}"'
            self.feedback_label.color = get_color_from_hex('#4CAF50')
            instance.background_color = get_color_from_hex('#4CAF50')
            play_praise()  # 播放表扬
        else:
            self.feedback_label.text = f'不对哦，是 "{correct_answer}"'
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
        self.question_label.text = f'{star_text} 测验完成！'
        self.display_label.text = '棒！'
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
            self.char_label.text = '🔊'
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
            text=f'🎉 第{level}关 过关！🎉',
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
        self.hint_label.text = f'🎉 过关啦！🎉'
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


class ChineseLearnApp(App):
    """乐乐的识字乐园 - Android平板版"""
    
    def build(self):
        self.title = '乐乐的识字乐园'
        
        # 初始化音频
        init_audio()
        # 延迟播放欢迎语，等待TTS初始化
        Clock.schedule_once(lambda dt: speak("欢迎来到乐乐的识字乐园"), 1.5)
        
        sm = ScreenManager(transition=FadeTransition())
        sm.add_widget(ChineseMenuScreen(name='chinese_menu'))
        sm.add_widget(ChineseLearnScreen(name='chinese_learn'))
        sm.add_widget(ChineseDetailScreen(name='chinese_detail'))
        sm.add_widget(ChineseQuizScreen(name='chinese_quiz'))
        sm.add_widget(ChineseMatchScreen(name='chinese_match'))
        sm.add_widget(ChineseWhackScreen(name='chinese_whack'))
        sm.add_widget(ChinesePictureScreen(name='chinese_picture'))
        sm.add_widget(ChineseChallengeScreen(name='chinese_challenge'))
        
        return sm
    
    def on_pause(self):
        """Android暂停时调用"""
        return True
    
    def on_resume(self):
        """Android恢复时调用"""
        pass


if __name__ == '__main__':
    ChineseLearnApp().run()
