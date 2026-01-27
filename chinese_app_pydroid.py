# -*- coding: utf-8 -*-
"""
乐乐的识字乐园 - Pydroid 3 单文件版
专为3-5岁儿童设计的汉字学习应用

使用方法：
1. 在平板上安装 Pydroid 3 (Google Play免费)
2. 安装 kivy 库：菜单 → Pip → 搜索 kivy → 安装
3. 打开此文件运行
"""
import random
import time
from dataclasses import dataclass, field
from typing import List, Dict, Any
from enum import Enum

from kivy.app import App
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.gridlayout import GridLayout
from kivy.uix.button import Button
from kivy.uix.label import Label
from kivy.uix.widget import Widget
from kivy.uix.screenmanager import ScreenManager, Screen, FadeTransition
from kivy.graphics import Color, Rectangle, Ellipse, Line
from kivy.utils import get_color_from_hex
from kivy.clock import Clock
from kivy.metrics import dp, sp
from kivy.core.text import LabelBase

# ==================== 字体配置 ====================
FONT_PATHS = [
    '/system/fonts/NotoSansCJK-Regular.ttc',
    '/system/fonts/DroidSansFallback.ttf',
    '/system/fonts/NotoSansHans-Regular.otf',
]
for font_path in FONT_PATHS:
    try:
        LabelBase.register(name='Roboto', fn_regular=font_path)
        break
    except:
        continue

# ==================== 汉字数据 ====================
class ChineseData:
    BASIC_WORDS = [
        ("人", "rén", "人们", "👤"), ("口", "kǒu", "口水", "👄"),
        ("手", "shǒu", "小手", "✋"), ("足", "zú", "足球", "⚽"),
        ("日", "rì", "日出", "☀️"), ("月", "yuè", "月亮", "🌙"),
        ("水", "shuǐ", "喝水", "💧"), ("火", "huǒ", "火焰", "🔥"),
        ("山", "shān", "高山", "⛰️"), ("石", "shí", "石头", "🪨"),
        ("田", "tián", "田地", "🌾"), ("土", "tǔ", "泥土", "🟤"),
    ]
    INTERMEDIATE_WORDS = [
        ("大", "dà", "大小", "📏"), ("小", "xiǎo", "小鸟", "🐦"),
        ("上", "shàng", "上面", "⬆️"), ("下", "xià", "下面", "⬇️"),
        ("左", "zuǒ", "左边", "⬅️"), ("右", "yòu", "右边", "➡️"),
        ("天", "tiān", "天空", "🌤️"), ("地", "dì", "大地", "🌍"),
        ("花", "huā", "鲜花", "🌸"), ("草", "cǎo", "小草", "🌿"),
        ("树", "shù", "大树", "🌳"), ("鸟", "niǎo", "小鸟", "🐦"),
    ]
    ADVANCED_WORDS = [
        ("爸", "bà", "爸爸", "👨"), ("妈", "mā", "妈妈", "👩"),
        ("爷", "yé", "爷爷", "👴"), ("奶", "nǎi", "奶奶", "👵"),
        ("哥", "gē", "哥哥", "👦"), ("姐", "jiě", "姐姐", "👧"),
        ("弟", "dì", "弟弟", "👦"), ("妹", "mèi", "妹妹", "👧"),
        ("吃", "chī", "吃饭", "🍚"), ("喝", "hē", "喝水", "🥤"),
        ("看", "kàn", "看书", "📖"), ("听", "tīng", "听歌", "🎵"),
    ]
    
    @classmethod
    def get_words(cls, level=1):
        if level == 1:
            return cls.BASIC_WORDS.copy()
        elif level == 2:
            return cls.BASIC_WORDS + cls.INTERMEDIATE_WORDS
        else:
            return cls.BASIC_WORDS + cls.INTERMEDIATE_WORDS + cls.ADVANCED_WORDS

# ==================== 游戏逻辑 ====================
class GameType(Enum):
    QUIZ = "quiz"
    MATCH = "match"
    WHACK = "whack"
    CHALLENGE = "challenge"

@dataclass
class GameSession:
    game_type: GameType
    level: int = 1
    score: int = 0
    correct_count: int = 0
    wrong_count: int = 0
    total_questions: int = 0
    current_question: int = 0
    start_time: float = field(default_factory=time.time)
    
    @property
    def accuracy(self) -> float:
        total = self.correct_count + self.wrong_count
        return self.correct_count / total if total > 0 else 0
    
    def add_correct(self, points: int = 10):
        self.correct_count += 1
        self.score += points
        self.current_question += 1
    
    def add_wrong(self):
        self.wrong_count += 1
        self.current_question += 1
    
    def is_complete(self) -> bool:
        return self.current_question >= self.total_questions

class GameLogic:
    def create_session(self, game_type: GameType, level: int = 1, total_questions: int = 10) -> GameSession:
        return GameSession(game_type=game_type, level=level, total_questions=total_questions)
    
    def check_answer(self, session: GameSession, user_answer, correct_answer, points: int = 10) -> bool:
        is_correct = user_answer == correct_answer
        if is_correct:
            session.add_correct(points)
        else:
            session.add_wrong()
        return is_correct
    
    def get_random_options(self, correct, all_items: List, count: int = 4) -> List:
        options = [correct]
        others = [item for item in all_items if item != correct]
        options.extend(random.sample(others, min(count - 1, len(others))))
        random.shuffle(options)
        return options
    
    def get_praise_message(self, accuracy: float) -> str:
        if accuracy >= 0.9: return "太棒了！你是最聪明的小朋友！"
        elif accuracy >= 0.7: return "很好！继续加油！"
        elif accuracy >= 0.5: return "不错哦！再练习一下会更好！"
        else: return "没关系，多练习就会进步的！"
    
    def calculate_stars(self, session: GameSession) -> int:
        if session.accuracy >= 0.9: return 3
        elif session.accuracy >= 0.7: return 2
        elif session.accuracy >= 0.5: return 1
        return 0

# ==================== 语音模块 ====================
audio = None
try:
    from jnius import autoclass
    TTS = autoclass('android.speech.tts.TextToSpeech')
    Activity = autoclass('org.kivy.android.PythonActivity')
    Locale = autoclass('java.util.Locale')
    
    class AndroidTTS:
        def __init__(self):
            self.tts = TTS(Activity.mActivity, None)
            self.tts.setLanguage(Locale.CHINESE)
        def speak(self, text):
            self.tts.speak(text, TTS.QUEUE_FLUSH, None, None)
    
    audio = AndroidTTS()
except:
    pass

def speak(text):
    if audio:
        audio.speak(text)

PRAISES = ["太棒了！", "真聪明！", "做得好！", "你真厉害！", "汪汪队为你骄傲！", "没有困难的工作，只有勇敢的狗狗！"]
ENCOURAGES = ["没关系，再试一次！", "加油，你可以的！", "汪汪队永不放弃！", "勇敢的狗狗不怕困难！"]

def play_praise():
    speak(random.choice(PRAISES))

def play_encourage():
    speak(random.choice(ENCOURAGES))

# ==================== 辅助函数 ====================
def get_font_size(base):
    return sp(base)

def get_padding():
    return dp(15)


# ==================== 绘图画布 ====================
class PictureCanvas(Widget):
    """简单图形绘制"""
    def draw_char(self, char):
        self.canvas.clear()
        cx, cy = self.center_x, self.center_y
        
        with self.canvas:
            if char == '日':
                Color(1, 0.8, 0)
                Ellipse(pos=(cx-60, cy-60), size=(120, 120))
                Color(1, 0.6, 0)
                for i in range(8):
                    import math
                    angle = i * math.pi / 4
                    x1, y1 = cx + 70 * math.cos(angle), cy + 70 * math.sin(angle)
                    x2, y2 = cx + 100 * math.cos(angle), cy + 100 * math.sin(angle)
                    Line(points=[x1, y1, x2, y2], width=3)
            elif char == '月':
                Color(1, 1, 0.6)
                Ellipse(pos=(cx-50, cy-50), size=(100, 100))
                Color(0.2, 0.2, 0.4)
                Ellipse(pos=(cx-20, cy-30), size=(80, 80))
            elif char == '山':
                Color(0.4, 0.6, 0.3)
                from kivy.graphics import Triangle
                Triangle(points=[cx, cy+80, cx-100, cy-60, cx+100, cy-60])
                Color(0.3, 0.5, 0.2)
                Triangle(points=[cx-60, cy+40, cx-120, cy-40, cx, cy-40])
                Triangle(points=[cx+60, cy+40, cx, cy-40, cx+120, cy-40])
            elif char == '水':
                Color(0.2, 0.6, 1)
                Ellipse(pos=(cx-15, cy+20), size=(30, 50))
                Ellipse(pos=(cx-40, cy-30), size=(25, 40))
                Ellipse(pos=(cx+15, cy-30), size=(25, 40))
            elif char == '火':
                Color(1, 0.3, 0)
                Ellipse(pos=(cx-30, cy-20), size=(60, 100))
                Color(1, 0.6, 0)
                Ellipse(pos=(cx-20, cy), size=(40, 60))
                Color(1, 1, 0)
                Ellipse(pos=(cx-10, cy+10), size=(20, 30))
            elif char == '人':
                Color(0.9, 0.7, 0.5)
                Ellipse(pos=(cx-25, cy+30), size=(50, 50))
                Color(0.3, 0.5, 0.8)
                Rectangle(pos=(cx-30, cy-50), size=(60, 80))
            elif char == '口':
                Color(0.9, 0.5, 0.5)
                Ellipse(pos=(cx-40, cy-30), size=(80, 60))
                Color(0.8, 0.2, 0.2)
                Ellipse(pos=(cx-25, cy-15), size=(50, 30))
            elif char == '手':
                Color(0.9, 0.7, 0.5)
                Ellipse(pos=(cx-30, cy-40), size=(60, 80))
                for i in range(5):
                    x = cx - 25 + i * 12
                    Ellipse(pos=(x, cy+40), size=(10, 30))
            elif char == '花':
                Color(0.2, 0.7, 0.2)
                Rectangle(pos=(cx-5, cy-60), size=(10, 60))
                for i in range(5):
                    import math
                    angle = i * 2 * math.pi / 5
                    px = cx + 40 * math.cos(angle)
                    py = cy + 20 + 40 * math.sin(angle)
                    Color(1, 0.4, 0.6)
                    Ellipse(pos=(px-15, py-15), size=(30, 30))
                Color(1, 1, 0)
                Ellipse(pos=(cx-15, cy+5), size=(30, 30))
            elif char == '树':
                Color(0.5, 0.3, 0.1)
                Rectangle(pos=(cx-15, cy-80), size=(30, 100))
                Color(0.2, 0.6, 0.2)
                Ellipse(pos=(cx-60, cy), size=(120, 100))
            elif char == '鸟':
                Color(0.3, 0.6, 0.9)
                Ellipse(pos=(cx-30, cy-20), size=(60, 50))
                Color(1, 0.6, 0)
                from kivy.graphics import Triangle
                Triangle(points=[cx+30, cy+5, cx+50, cy+10, cx+30, cy+15])
                Color(0, 0, 0)
                Ellipse(pos=(cx+10, cy+15), size=(8, 8))
            else:
                Color(0.5, 0.7, 1)
                Ellipse(pos=(cx-50, cy-50), size=(100, 100))
                Color(1, 1, 1)
                from kivy.graphics import Triangle
                Triangle(points=[cx-20, cy+20, cx+20, cy+20, cx, cy-20])

# ==================== 主菜单 ====================
class ChineseMenuScreen(Screen):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        layout = BoxLayout(orientation='vertical', padding=get_padding(), spacing=dp(15))
        
        with layout.canvas.before:
            Color(*get_color_from_hex('#FFF8E1'))
            self.bg = Rectangle(pos=layout.pos, size=layout.size)
        layout.bind(pos=lambda i,v: setattr(self.bg, 'pos', v),
                   size=lambda i,v: setattr(self.bg, 'size', v))
        
        layout.add_widget(Label(
            text='🐕 乐乐的识字乐园 🐕',
            font_size=get_font_size(36), color=get_color_from_hex('#E65100'),
            bold=True, size_hint=(1, 0.15)
        ))
        layout.add_widget(Label(
            text='点击下面的游戏开始学习汉字吧！',
            font_size=get_font_size(18), color=get_color_from_hex('#666666'),
            size_hint=(1, 0.08)
        ))
        
        games = GridLayout(cols=3, spacing=dp(15), size_hint=(1, 0.65), padding=dp(20))
        game_list = [
            ('字', '学汉字', '#FF7043', 'learn'),
            ('图', '看图选字', '#4ECDC4', 'picture'),
            ('?', '汉字测验', '#66BB6A', 'quiz'),
            ('对', '汉字配对', '#42A5F5', 'match'),
            ('锤', '打地鼠', '#FFD93D', 'whack'),
            ('时', '限时挑战', '#9C27B0', 'challenge'),
        ]
        
        for icon, title, color, screen in game_list:
            btn = Button(background_normal='', background_color=get_color_from_hex(color))
            btn.markup = True
            btn.text = f'[size={int(sp(42))}]{icon}[/size]\n[b][size={int(sp(20))}]{title}[/size][/b]'
            btn.target_screen = screen
            btn.bind(on_press=self.go_screen)
            games.add_widget(btn)
        
        layout.add_widget(games)
        layout.add_widget(Label(text='适合3-5岁小朋友 ❤️', font_size=get_font_size(14),
                                color=get_color_from_hex('#999999'), size_hint=(1, 0.1)))
        self.add_widget(layout)
    
    def go_screen(self, instance):
        if hasattr(instance, 'target_screen'):
            self.manager.current = instance.target_screen


# ==================== 学汉字界面 ====================
class ChineseLearnScreen(Screen):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.current_level = 1
        self.build_ui()
    
    def build_ui(self):
        layout = BoxLayout(orientation='vertical', padding=get_padding(), spacing=dp(10))
        with layout.canvas.before:
            Color(*get_color_from_hex('#FFF3E0'))
            self.bg = Rectangle(pos=layout.pos, size=layout.size)
        layout.bind(pos=lambda i,v: setattr(self.bg, 'pos', v),
                   size=lambda i,v: setattr(self.bg, 'size', v))
        
        nav = BoxLayout(size_hint=(1, 0.1))
        back_btn = Button(text='< 返回', size_hint=(0.2, 1), font_size=get_font_size(18),
                         background_color=get_color_from_hex('#FF7043'), background_normal='')
        back_btn.bind(on_press=lambda x: setattr(self.manager, 'current', 'menu'))
        nav.add_widget(back_btn)
        nav.add_widget(Label(text='【学汉字】点击卡片学习', font_size=get_font_size(24),
                            color=get_color_from_hex('#E65100'), bold=True, size_hint=(0.8, 1)))
        layout.add_widget(nav)
        
        self.cards_grid = GridLayout(cols=4, spacing=dp(12), padding=dp(10), size_hint=(1, 0.8))
        layout.add_widget(self.cards_grid)
        self.add_widget(layout)
        self.load_cards()
    
    def load_cards(self):
        self.cards_grid.clear_widgets()
        words = ChineseData.get_words(level=self.current_level)
        colors = ['#FF6B6B', '#4ECDC4', '#45B7D1', '#96CEB4', '#DDA0DD', '#FFD93D']
        
        for i, (char, pinyin, word, emoji) in enumerate(words):
            btn = Button(background_normal='', background_color=get_color_from_hex(colors[i % len(colors)]))
            btn.markup = True
            btn.text = f'[size={int(sp(42))}][b]{char}[/b][/size]\n[size={int(sp(14))}]{pinyin}[/size]\n[size={int(sp(12))}]{word}[/size]'
            btn.char_data = (char, pinyin, word)
            btn.bind(on_press=self.on_card_press)
            self.cards_grid.add_widget(btn)
    
    def on_card_press(self, instance):
        if hasattr(instance, 'char_data'):
            char, pinyin, word = instance.char_data
            speak(char)
            detail = self.manager.get_screen('detail')
            detail.show_char(char, pinyin, word)
            self.manager.current = 'detail'

# ==================== 汉字详情界面 ====================
class ChineseDetailScreen(Screen):
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
        
        nav = BoxLayout(size_hint=(1, 0.1))
        back_btn = Button(text='< 返回', size_hint=(0.2, 1), font_size=get_font_size(18),
                         background_color=get_color_from_hex('#FF7043'), background_normal='')
        back_btn.bind(on_press=lambda x: setattr(self.manager, 'current', 'learn'))
        nav.add_widget(back_btn)
        nav.add_widget(Label(text='点击可朗读', font_size=get_font_size(20),
                            color=get_color_from_hex('#666'), size_hint=(0.8, 1)))
        layout.add_widget(nav)
        
        self.char_btn = Button(text='字', font_size=get_font_size(150),
                              color=get_color_from_hex('#E65100'),
                              background_color=get_color_from_hex('#FFF8E1'),
                              background_normal='', size_hint=(1, 0.4))
        self.char_btn.bind(on_press=lambda x: speak(self.current_char) if self.current_char else None)
        layout.add_widget(self.char_btn)
        
        self.pinyin_label = Label(text='pīnyīn', font_size=get_font_size(32),
                                  color=get_color_from_hex('#666'), size_hint=(1, 0.1))
        layout.add_widget(self.pinyin_label)
        
        self.word_btn = Button(text='词语', font_size=get_font_size(36),
                              background_color=get_color_from_hex('#E8F5E9'),
                              background_normal='', size_hint=(1, 0.15))
        self.word_btn.bind(on_press=lambda x: speak(self.word_btn.text))
        layout.add_widget(self.word_btn)
        
        self.sentence_btn = Button(text='例句', font_size=get_font_size(22),
                                  background_color=get_color_from_hex('#E3F2FD'),
                                  background_normal='', size_hint=(1, 0.15))
        self.sentence_btn.bind(on_press=lambda x: speak(self.sentence_btn.text))
        layout.add_widget(self.sentence_btn)
        
        self.add_widget(layout)
    
    def show_char(self, char, pinyin, word):
        self.current_char = char
        self.char_btn.text = char
        self.pinyin_label.text = pinyin
        self.word_btn.text = word
        
        sentences = {
            '人': '我是一个小人儿。', '口': '我有一张小嘴巴。', '手': '我有两只小手。',
            '足': '我喜欢踢足球。', '日': '太阳公公出来了。', '月': '月亮弯弯像小船。',
            '水': '我要喝水。', '火': '火很烫，不能碰。', '山': '山上有很多树。',
            '石': '石头硬硬的。', '田': '农民伯伯在田里种菜。', '土': '小草从土里长出来。',
            '大': '大象的耳朵大大的。', '小': '小鸟在树上唱歌。', '上': '飞机飞到天上去了。',
            '下': '小雨从天上落下来。', '天': '天空是蓝色的。', '地': '小草在地上生长。',
            '花': '花儿真漂亮。', '草': '小草绿绿的。', '树': '大树高高的。', '鸟': '小鸟会飞。',
        }
        self.sentence_btn.text = sentences.get(char, f'我认识"{char}"这个字。')
        Clock.schedule_once(lambda dt: speak(char), 0.3)


# ==================== 汉字测验界面 ====================
class ChineseQuizScreen(Screen):
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
        
        nav = BoxLayout(size_hint=(1, 0.1))
        back_btn = Button(text='< 返回', size_hint=(0.15, 1), font_size=get_font_size(18),
                         background_color=get_color_from_hex('#66BB6A'), background_normal='')
        back_btn.bind(on_press=lambda x: setattr(self.manager, 'current', 'menu'))
        nav.add_widget(back_btn)
        nav.add_widget(Label(text='【汉字测验】', font_size=get_font_size(28),
                            color=get_color_from_hex('#2E7D32'), bold=True, size_hint=(0.5, 1)))
        self.score_label = Label(text='得分: 0', font_size=get_font_size(20),
                                color=get_color_from_hex('#FF6B6B'), size_hint=(0.2, 1))
        nav.add_widget(self.score_label)
        self.progress_label = Label(text='0/10', font_size=get_font_size(18),
                                   color=get_color_from_hex('#666666'), size_hint=(0.15, 1))
        nav.add_widget(self.progress_label)
        layout.add_widget(nav)
        
        self.question_label = Label(text='找出正确的汉字！', font_size=get_font_size(24),
                                   color=get_color_from_hex('#333333'), size_hint=(1, 0.1))
        layout.add_widget(self.question_label)
        
        self.display_label = Label(text='?', font_size=get_font_size(80),
                                  color=get_color_from_hex('#E65100'), size_hint=(1, 0.35))
        layout.add_widget(self.display_label)
        
        self.feedback_label = Label(text='', font_size=get_font_size(24),
                                   color=get_color_from_hex('#4CAF50'), size_hint=(1, 0.1))
        layout.add_widget(self.feedback_label)
        
        self.answers_layout = GridLayout(cols=2, spacing=dp(15), padding=dp(20), size_hint=(1, 0.25))
        layout.add_widget(self.answers_layout)
        
        self.start_btn = Button(text='开始测验', font_size=get_font_size(24), size_hint=(1, 0.1),
                               background_color=get_color_from_hex('#FF9800'), background_normal='')
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
        
        word_hints = {'人': '小人儿', '口': '门口', '手': '小手', '足': '足球',
                     '日': '太阳', '月': '月亮', '水': '喝水', '火': '火车',
                     '山': '高山', '石': '石头', '田': '田地', '土': '泥土',
                     '大': '大象', '小': '小鸟', '上': '上面', '下': '下面',
                     '天': '天空', '地': '土地', '花': '鲜花', '草': '小草',
                     '树': '大树', '鸟': '小鸟'}
        hint_word = word_hints.get(char, word)
        self.display_label.text = hint_word
        self.question_label.text = f'"{hint_word}" 里面有哪个字？'
        
        self.answers_layout.clear_widgets()
        all_chars = [w[0] for w in words]
        options = self.logic.get_random_options(char, all_chars, count=4)
        
        colors = ['#FF6B6B', '#4ECDC4', '#45B7D1', '#96CEB4']
        for i, opt in enumerate(options):
            btn = Button(text=opt, font_size=get_font_size(56),
                        background_color=get_color_from_hex(colors[i]), background_normal='', bold=True)
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
            play_praise()
        else:
            self.feedback_label.text = f'不对哦，是 "{correct_answer}"'
            self.feedback_label.color = get_color_from_hex('#F44336')
            instance.background_color = get_color_from_hex('#F44336')
            play_encourage()
        
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


# ==================== 看图选字界面 ====================
class ChinesePictureScreen(Screen):
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
        
        nav = BoxLayout(size_hint=(1, 0.1))
        back_btn = Button(text='< 返回', size_hint=(0.15, 1), font_size=get_font_size(18),
                         background_color=get_color_from_hex('#4ECDC4'), background_normal='')
        back_btn.bind(on_press=lambda x: setattr(self.manager, 'current', 'menu'))
        nav.add_widget(back_btn)
        nav.add_widget(Label(text='【看图选字】', font_size=get_font_size(28),
                            color=get_color_from_hex('#00838F'), bold=True, size_hint=(0.5, 1)))
        self.score_label = Label(text='得分: 0', font_size=get_font_size(20),
                                color=get_color_from_hex('#FF6B6B'), size_hint=(0.2, 1))
        nav.add_widget(self.score_label)
        self.progress_label = Label(text='0/10', font_size=get_font_size(18),
                                   color=get_color_from_hex('#666666'), size_hint=(0.15, 1))
        nav.add_widget(self.progress_label)
        layout.add_widget(nav)
        
        self.hint_label = Label(text='看图片，选出正确的汉字！', font_size=get_font_size(22),
                               color=get_color_from_hex('#333333'), size_hint=(1, 0.08))
        layout.add_widget(self.hint_label)
        
        picture_box = BoxLayout(size_hint=(1, 0.35), padding=dp(20))
        self.picture_container = BoxLayout()
        with self.picture_container.canvas.before:
            Color(1, 1, 1, 1)
            self.pic_bg = Rectangle(pos=self.picture_container.pos, size=self.picture_container.size)
        self.picture_container.bind(pos=lambda i,v: setattr(self.pic_bg, 'pos', v),
                                   size=lambda i,v: setattr(self.pic_bg, 'size', v))
        self.picture_canvas = PictureCanvas()
        self.picture_container.add_widget(self.picture_canvas)
        picture_box.add_widget(self.picture_container)
        layout.add_widget(picture_box)
        
        self.desc_label = Label(text='', font_size=get_font_size(24),
                               color=get_color_from_hex('#666666'), size_hint=(1, 0.08))
        layout.add_widget(self.desc_label)
        
        self.feedback_label = Label(text='', font_size=get_font_size(22),
                                   color=get_color_from_hex('#4CAF50'), size_hint=(1, 0.08))
        layout.add_widget(self.feedback_label)
        
        self.answers_layout = GridLayout(cols=4, spacing=dp(15), padding=dp(20), size_hint=(1, 0.2))
        layout.add_widget(self.answers_layout)
        
        self.start_btn = Button(text='开始游戏', font_size=get_font_size(24), size_hint=(1, 0.1),
                               background_color=get_color_from_hex('#4ECDC4'), background_normal='')
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
        
        self.picture_canvas.draw_char(char)
        
        picture_hints = {'人': '一个人站着', '口': '张开的嘴巴', '手': '五个手指', '足': '踢球的脚',
                        '日': '圆圆的太阳', '月': '弯弯的月亮', '水': '流动的水滴', '火': '燃烧的火焰',
                        '山': '高高的山峰', '石': '硬硬的石头', '田': '方方的田地', '土': '棕色的泥土',
                        '花': '漂亮的鲜花', '草': '绿绿的小草', '树': '高高的大树', '鸟': '飞翔的小鸟'}
        self.desc_label.text = f'提示：{picture_hints.get(char, word)}'
        
        self.answers_layout.clear_widgets()
        all_chars = [w[0] for w in words]
        options = self.logic.get_random_options(char, all_chars, count=4)
        
        colors = ['#FF6B6B', '#4ECDC4', '#45B7D1', '#96CEB4']
        for i, opt in enumerate(options):
            btn = Button(text=opt, font_size=get_font_size(56),
                        background_color=get_color_from_hex(colors[i]), background_normal='', bold=True)
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
            play_praise()
        else:
            self.feedback_label.text = f'错误，正确答案是 "{correct_answer}"'
            self.feedback_label.color = get_color_from_hex('#F44336')
            instance.background_color = get_color_from_hex('#F44336')
            play_encourage()
        
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
        self.desc_label.text = '太棒了!'
        self.feedback_label.text = f'{praise}\n正确率: {self.session.accuracy*100:.0f}%'


# ==================== 汉字配对界面 ====================
class ChineseMatchScreen(Screen):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
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
        
        nav = BoxLayout(size_hint=(1, 0.1))
        back_btn = Button(text='< 返回', size_hint=(0.15, 1), font_size=get_font_size(18),
                         background_color=get_color_from_hex('#42A5F5'), background_normal='')
        back_btn.bind(on_press=lambda x: setattr(self.manager, 'current', 'menu'))
        nav.add_widget(back_btn)
        nav.add_widget(Label(text='【汉字配对】', font_size=get_font_size(28),
                            color=get_color_from_hex('#1565C0'), bold=True, size_hint=(0.55, 1)))
        self.score_label = Label(text='得分: 0', font_size=get_font_size(20),
                                color=get_color_from_hex('#FF6B6B'), size_hint=(0.15, 1))
        nav.add_widget(self.score_label)
        nav.add_widget(Label(text='', size_hint=(0.15, 1)))
        layout.add_widget(nav)
        
        self.hint_label = Label(text='找到汉字和它的拼音配对！', font_size=get_font_size(20),
                               color=get_color_from_hex('#666666'), size_hint=(1, 0.08))
        layout.add_widget(self.hint_label)
        
        self.feedback_label = Label(text='', font_size=get_font_size(22),
                                   color=get_color_from_hex('#4CAF50'), size_hint=(1, 0.08))
        layout.add_widget(self.feedback_label)
        
        self.cards_layout = GridLayout(cols=4, spacing=dp(12), padding=dp(15), size_hint=(1, 0.54))
        layout.add_widget(self.cards_layout)
        
        self.start_btn = Button(text='开始游戏', font_size=get_font_size(24), size_hint=(1, 0.1),
                               background_color=get_color_from_hex('#42A5F5'), background_normal='')
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
        
        words = ChineseData.get_words(level=2)
        selected = random.sample(words, 6)
        
        for char, pinyin, word, emoji in selected:
            self.card_data.append({'type': 'char', 'value': char, 'match_id': char, 'pinyin': pinyin})
            self.card_data.append({'type': 'pinyin', 'value': pinyin, 'match_id': char})
        
        random.shuffle(self.card_data)
        
        colors = ['#FFB6C1', '#98FB98', '#87CEEB', '#DDA0DD', '#F0E68C', '#FFA07A',
                  '#B0E0E6', '#FFE4B5', '#E6E6FA', '#FFDAB9', '#D8BFD8', '#F5DEB3']
        
        for i in range(12):
            card = self.card_data[i]
            btn = Button(text='?', font_size=get_font_size(36),
                        background_color=get_color_from_hex(colors[i]), background_normal='')
            btn.card_index = i
            btn.card_value = card['value']
            btn.card_type = card['type']
            btn.original_color = get_color_from_hex(colors[i])
            btn.bind(on_press=self.on_card_press)
            self.cards_layout.add_widget(btn)
            self.cards.append(btn)
        
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
                self.score += 20
                self.score_label.text = f'得分: {self.score}'
                self.matched.add(first_idx)
                self.matched.add(idx)
                first_btn.background_color = get_color_from_hex('#4CAF50')
                instance.background_color = get_color_from_hex('#4CAF50')
                self.feedback_label.text = f'太棒了！{first_data["match_id"]} 配对成功！'
                self.feedback_label.color = get_color_from_hex('#4CAF50')
                play_praise()
                
                if len(self.matched) == 12:
                    Clock.schedule_once(lambda dt: self.show_complete(), 1.0)
            else:
                self.feedback_label.text = '不是配对，再试试！'
                self.feedback_label.color = get_color_from_hex('#FF9800')
                play_encourage()
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


# ==================== 打地鼠界面 ====================
class ChineseWhackScreen(Screen):
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
        
        nav = BoxLayout(size_hint=(1, 0.08))
        back_btn = Button(text='< 返回', size_hint=(0.15, 1), font_size=get_font_size(18),
                         background_color=get_color_from_hex('#228B22'), background_normal='')
        back_btn.bind(on_press=self.go_back)
        nav.add_widget(back_btn)
        nav.add_widget(Label(text='【汉字打地鼠】', font_size=get_font_size(26),
                            color=get_color_from_hex('#006400'), bold=True, size_hint=(0.55, 1)))
        self.score_label = Label(text='得分: 0', font_size=get_font_size(20),
                                color=get_color_from_hex('#FF6B6B'), size_hint=(0.15, 1))
        nav.add_widget(self.score_label)
        self.round_label = Label(text='0/10', font_size=get_font_size(18),
                                color=get_color_from_hex('#333333'), size_hint=(0.15, 1))
        nav.add_widget(self.round_label)
        layout.add_widget(nav)
        
        target_box = BoxLayout(size_hint=(1, 0.12), padding=[dp(50), dp(5)])
        target_bg = Button(text='', background_color=get_color_from_hex('#FFD700'),
                          background_normal='', size_hint=(1, 1))
        target_box.add_widget(target_bg)
        layout.add_widget(target_box)
        
        self.target_label = Label(text='点击开始游戏！', font_size=get_font_size(32),
                                 color=get_color_from_hex('#DC143C'), size_hint=(1, 0.01))
        layout.add_widget(self.target_label)
        
        self.feedback_label = Label(text='', font_size=get_font_size(22),
                                   color=get_color_from_hex('#4CAF50'), size_hint=(1, 0.08))
        layout.add_widget(self.feedback_label)
        
        self.holes_layout = GridLayout(cols=3, spacing=dp(15), padding=dp(20), size_hint=(1, 0.52))
        for i in range(9):
            hole_btn = Button(text='', font_size=get_font_size(52),
                             background_color=get_color_from_hex('#8B4513'), background_normal='',
                             color=get_color_from_hex('#000000'))
            hole_btn.hole_index = i
            hole_btn.bind(on_press=self.on_hole_press)
            self.holes_layout.add_widget(hole_btn)
            self.holes.append(hole_btn)
        layout.add_widget(self.holes_layout)
        
        self.start_btn = Button(text='开始游戏', font_size=get_font_size(24), size_hint=(1, 0.1),
                               background_color=get_color_from_hex('#FF9800'), background_normal='')
        self.start_btn.bind(on_press=self.start_game)
        layout.add_widget(self.start_btn)
        self.add_widget(layout)
    
    def go_back(self, instance):
        self.stop_game()
        self.manager.current = 'menu'
    
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
        
        for i, hole in enumerate(self.holes):
            hole.text = ''
            hole.background_color = get_color_from_hex('#8B4513')
            self.hole_states[i] = None
        
        words = ChineseData.get_words(level=2)
        target_word = random.choice(words)
        self.target_char = target_word[0]
        self.target_label.text = f'快找 {self.target_char}！'
        speak(f"快找{self.target_char}")
        
        num_moles = random.randint(3, 4)
        mole_positions = random.sample(range(9), num_moles)
        
        others = random.sample([w for w in words if w[0] != self.target_char], num_moles - 1)
        char_list = [self.target_char] + [w[0] for w in others]
        random.shuffle(char_list)
        
        for i, pos in enumerate(mole_positions):
            hole = self.holes[pos]
            char = char_list[i]
            hole.text = char
            hole.background_color = get_color_from_hex('#FFEB3B')
            hole.color = get_color_from_hex('#000000')
            self.hole_states[pos] = char
        
        self.round_label.text = f'{self.session.current_question + 1}/10'
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
        
        if self.spawn_event:
            self.spawn_event.cancel()
        
        if char == self.target_char:
            self.session.add_correct(10)
            self.score_label.text = f'得分: {self.session.score}'
            self.feedback_label.text = f'太棒了！打中 {self.target_char}！'
            self.feedback_label.color = get_color_from_hex('#4CAF50')
            instance.background_color = get_color_from_hex('#4CAF50')
            instance.text = '棒!'
            play_praise()
        else:
            self.session.add_wrong()
            self.feedback_label.text = f'打错了！要找 {self.target_char}'
            self.feedback_label.color = get_color_from_hex('#F44336')
            instance.background_color = get_color_from_hex('#F44336')
            instance.text = 'X'
            play_encourage()
        
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


# ==================== 限时挑战界面 ====================
class ChineseChallengeScreen(Screen):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.logic = GameLogic()
        self.session = None
        self.current_word = None
        self.time_left = 60
        self.timer_event = None
        self.combo = 0
        self.build_ui()
    
    def build_ui(self):
        layout = BoxLayout(orientation='vertical', padding=get_padding(), spacing=dp(10))
        with layout.canvas.before:
            Color(*get_color_from_hex('#F3E5F5'))
            self.bg = Rectangle(pos=layout.pos, size=layout.size)
        layout.bind(pos=lambda i,v: setattr(self.bg, 'pos', v),
                   size=lambda i,v: setattr(self.bg, 'size', v))
        
        nav = BoxLayout(size_hint=(1, 0.1))
        back_btn = Button(text='< 返回', size_hint=(0.15, 1), font_size=get_font_size(18),
                         background_color=get_color_from_hex('#9C27B0'), background_normal='')
        back_btn.bind(on_press=self.go_back)
        nav.add_widget(back_btn)
        nav.add_widget(Label(text='【限时挑战】', font_size=get_font_size(28),
                            color=get_color_from_hex('#7B1FA2'), bold=True, size_hint=(0.4, 1)))
        self.timer_label = Label(text='60秒', font_size=get_font_size(28),
                                color=get_color_from_hex('#F44336'), bold=True, size_hint=(0.15, 1))
        nav.add_widget(self.timer_label)
        self.score_label = Label(text='得分: 0', font_size=get_font_size(20),
                                color=get_color_from_hex('#FF6B6B'), size_hint=(0.15, 1))
        nav.add_widget(self.score_label)
        self.combo_label = Label(text='', font_size=get_font_size(16),
                                color=get_color_from_hex('#FF9800'), size_hint=(0.15, 1))
        nav.add_widget(self.combo_label)
        layout.add_widget(nav)
        
        self.hint_label = Label(text='60秒内答对越多越好！', font_size=get_font_size(20),
                               color=get_color_from_hex('#333333'), size_hint=(1, 0.08))
        layout.add_widget(self.hint_label)
        
        self.char_label = Label(text='准备', font_size=get_font_size(120),
                               color=get_color_from_hex('#7B1FA2'), size_hint=(1, 0.3))
        layout.add_widget(self.char_label)
        
        self.question_label = Label(text='', font_size=get_font_size(22),
                                   color=get_color_from_hex('#666666'), size_hint=(1, 0.08))
        layout.add_widget(self.question_label)
        
        self.feedback_label = Label(text='', font_size=get_font_size(24),
                                   color=get_color_from_hex('#4CAF50'), size_hint=(1, 0.08))
        layout.add_widget(self.feedback_label)
        
        self.answers_layout = GridLayout(cols=4, spacing=dp(10), padding=dp(15), size_hint=(1, 0.22))
        layout.add_widget(self.answers_layout)
        
        self.start_btn = Button(text='开始挑战！', font_size=get_font_size(24), size_hint=(1, 0.1),
                               background_color=get_color_from_hex('#9C27B0'), background_normal='')
        self.start_btn.bind(on_press=self.start_game)
        layout.add_widget(self.start_btn)
        self.add_widget(layout)
    
    def go_back(self, instance):
        self.stop_timer()
        self.manager.current = 'menu'
    
    def stop_timer(self):
        if self.timer_event:
            self.timer_event.cancel()
            self.timer_event = None
    
    def start_game(self, instance):
        self.session = self.logic.create_session(GameType.CHALLENGE, total_questions=100)
        self.time_left = 60
        self.combo = 0
        self.score_label.text = '得分: 0'
        self.combo_label.text = ''
        self.feedback_label.text = ''
        self.start_btn.text = '重新开始'
        self.start_btn.disabled = True
        self.timer_event = Clock.schedule_interval(self.update_timer, 1)
        self.next_question()
    
    def update_timer(self, dt):
        self.time_left -= 1
        self.timer_label.text = f'{self.time_left}秒'
        if self.time_left <= 10:
            self.timer_label.color = get_color_from_hex('#F44336')
        elif self.time_left <= 30:
            self.timer_label.color = get_color_from_hex('#FF9800')
        if self.time_left <= 0:
            self.stop_timer()
            self.show_result()
    
    def next_question(self):
        words = ChineseData.get_words(level=2)
        self.current_word = random.choice(words)
        char, pinyin, word, emoji = self.current_word
        
        word_hints = {'人': '小人儿', '口': '门口', '手': '小手', '足': '足球',
                     '日': '太阳', '月': '月亮', '水': '喝水', '火': '火车',
                     '山': '高山', '石': '石头', '田': '田地', '土': '泥土',
                     '大': '大象', '小': '小鸟', '上': '上面', '下': '下面',
                     '天': '天空', '地': '土地', '花': '鲜花', '草': '小草',
                     '树': '大树', '鸟': '小鸟'}
        hint_word = word_hints.get(char, word)
        self.char_label.text = hint_word
        self.question_label.text = '找出里面的字！'
        
        self.answers_layout.clear_widgets()
        all_chars = [w[0] for w in words]
        options = self.logic.get_random_options(char, all_chars, count=4)
        
        colors = ['#FF6B6B', '#4ECDC4', '#45B7D1', '#96CEB4']
        for i, opt in enumerate(options):
            btn = Button(text=opt, font_size=get_font_size(52),
                        background_color=get_color_from_hex(colors[i]), background_normal='', bold=True)
            btn.disabled = False
            btn.bind(on_press=self.on_answer)
            self.answers_layout.add_widget(btn)
    
    def on_answer(self, instance):
        if self.current_word is None or self.time_left <= 0:
            return
        
        user_answer = instance.text
        correct_answer = self.current_word[0]
        is_correct = user_answer == correct_answer
        
        if is_correct:
            self.combo += 1
            bonus = min(self.combo, 5)
            points = 10 * bonus
            self.session.add_correct(points)
            self.feedback_label.text = f'正确！+{points}分'
            self.feedback_label.color = get_color_from_hex('#4CAF50')
            if self.combo >= 3:
                self.combo_label.text = f'{self.combo}连击!'
                self.combo_label.color = get_color_from_hex('#FF9800')
        else:
            self.combo = 0
            self.combo_label.text = ''
            self.session.add_wrong()
            self.feedback_label.text = f'错误！答案是 {correct_answer}'
            self.feedback_label.color = get_color_from_hex('#F44336')
        
        self.score_label.text = f'得分: {self.session.score}'
        Clock.schedule_once(lambda dt: self.next_question(), 0.5)
    
    def show_result(self):
        self.start_btn.disabled = False
        total = self.session.correct_count + self.session.wrong_count
        score = self.session.score
        
        if score >= 300:
            rank, stars = '超级天才！', '★★★'
        elif score >= 200:
            rank, stars = '非常棒！', '★★☆'
        elif score >= 100:
            rank, stars = '继续加油！', '★☆☆'
        else:
            rank, stars = '多多练习！', '☆☆☆'
        
        self.char_label.text = stars
        self.question_label.text = rank
        self.hint_label.text = '挑战结束！'
        self.feedback_label.text = f'答对{self.session.correct_count}题，得分{score}分'
        self.timer_label.text = '完成'
        self.timer_label.color = get_color_from_hex('#4CAF50')
        self.answers_layout.clear_widgets()

# ==================== 主应用 ====================
class ChineseLearnApp(App):
    def build(self):
        self.title = '乐乐的识字乐园'
        Clock.schedule_once(lambda dt: speak("欢迎来到乐乐的识字乐园"), 1.5)
        
        sm = ScreenManager(transition=FadeTransition())
        sm.add_widget(ChineseMenuScreen(name='menu'))
        sm.add_widget(ChineseLearnScreen(name='learn'))
        sm.add_widget(ChineseDetailScreen(name='detail'))
        sm.add_widget(ChineseQuizScreen(name='quiz'))
        sm.add_widget(ChinesePictureScreen(name='picture'))
        sm.add_widget(ChineseMatchScreen(name='match'))
        sm.add_widget(ChineseWhackScreen(name='whack'))
        sm.add_widget(ChineseChallengeScreen(name='challenge'))
        return sm
    
    def on_pause(self):
        return True
    
    def on_resume(self):
        pass

if __name__ == '__main__':
    ChineseLearnApp().run()
