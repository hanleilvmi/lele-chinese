# -*- coding: utf-8 -*-
"""添加功能2: 汉字故事"""

NEW_CODE = '''

class ChineseWriteScreen(Screen):
    """描红写字 - 让小朋友用手指描写汉字"""
    
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
            size_hint=(0.15, 1),
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
            size_hint=(0.5, 1)
        ))
        
        clear_btn = Button(
            text='清除',
            size_hint=(0.15, 1),
            font_size=get_font_size(18),
            background_color=get_color_from_hex('#F44336'),
            background_normal=''
        )
        clear_btn.bind(on_press=self.clear_canvas)
        nav.add_widget(clear_btn)
        
        next_btn = Button(
            text='换字',
            size_hint=(0.15, 1),
            font_size=get_font_size(18),
            background_color=get_color_from_hex('#4CAF50'),
            background_normal=''
        )
        next_btn.bind(on_press=self.next_char)
        nav.add_widget(next_btn)
        layout.add_widget(nav)
        
        self.hint_label = Label(
            text='用手指描写下面的汉字吧！',
            font_size=get_font_size(20),
            color=get_color_from_hex('#666666'),
            size_hint=(1, 0.08)
        )
        layout.add_widget(self.hint_label)
        
        # 写字区域
        write_box = BoxLayout(size_hint=(1, 0.65), padding=dp(10))
        
        # 左侧示范字
        left_box = BoxLayout(orientation='vertical', size_hint=(0.3, 1))
        left_box.add_widget(Label(text='示范', font_size=get_font_size(18), color=get_color_from_hex('#999999'), size_hint=(1, 0.15)))
        self.demo_label = Label(text='人', font_size=get_font_size(120), color=get_color_from_hex('#CCCCCC'), size_hint=(1, 0.85))
        left_box.add_widget(self.demo_label)
        write_box.add_widget(left_box)
        
        # 右侧写字画布
        right_box = BoxLayout(orientation='vertical', size_hint=(0.7, 1))
        right_box.add_widget(Label(text='在这里写字', font_size=get_font_size(18), color=get_color_from_hex('#999999'), size_hint=(1, 0.1)))
        canvas_container = BoxLayout(size_hint=(1, 0.9), padding=dp(5))
        self.write_canvas = WriteCanvas()
        canvas_container.add_widget(self.write_canvas)
        right_box.add_widget(canvas_container)
        write_box.add_widget(right_box)
        layout.add_widget(write_box)
        
        # 底部汉字选择
        char_box = BoxLayout(size_hint=(1, 0.15), spacing=dp(10), padding=dp(10))
        words = ChineseData.get_words(level=1)[:8]
        for char, pinyin, word, emoji in words:
            btn = Button(text=char, font_size=get_font_size(32), background_color=get_color_from_hex('#FFB74D'), background_normal='')
            btn.bind(on_press=self.select_char)
            char_box.add_widget(btn)
        layout.add_widget(char_box)
        
        self.add_widget(layout)
        self.select_char_by_name('人')
    
    def select_char(self, instance):
        self.select_char_by_name(instance.text)
    
    def select_char_by_name(self, char):
        self.current_char = char
        self.demo_label.text = char
        self.write_canvas.set_guide_char(char)
        self.clear_canvas(None)
        speak(char)
    
    def clear_canvas(self, instance):
        self.write_canvas.clear_drawing()
    
    def next_char(self, instance):
        words = ChineseData.get_words(level=2)
        char = random.choice(words)[0]
        self.select_char_by_name(char)
        play_praise()


class WriteCanvas(Widget):
    """写字画布 - 支持触摸绘制"""
    
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.guide_char = '人'
        self.lines = []
        self.current_line = []
        self.bind(size=self.redraw, pos=self.redraw)
        Clock.schedule_once(lambda dt: self.redraw(), 0.1)
    
    def set_guide_char(self, char):
        self.guide_char = char
        self.redraw()
    
    def redraw(self, *args):
        self.canvas.clear()
        with self.canvas:
            Color(1, 1, 1, 1)
            Rectangle(pos=self.pos, size=self.size)
            Color(0.9, 0.9, 0.9, 1)
            cx, cy = self.center_x, self.center_y
            w, h = self.width, self.height
            Line(points=[self.x, cy, self.x + w, cy], width=1)
            Line(points=[cx, self.y, cx, self.y + h], width=1)
            Line(points=[self.x, self.y, self.x + w, self.y + h], width=1)
            Line(points=[self.x, self.y + h, self.x + w, self.y], width=1)
            Color(0.8, 0.8, 0.8, 1)
            Line(rectangle=(self.x, self.y, w, h), width=2)
        self.redraw_lines()
    
    def redraw_lines(self):
        with self.canvas:
            Color(0.2, 0.2, 0.8, 1)
            for line in self.lines:
                if len(line) >= 4:
                    Line(points=line, width=dp(4))
    
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
            self.redraw()
            with self.canvas:
                Color(0.2, 0.2, 0.8, 1)
                if len(self.current_line) >= 4:
                    Line(points=self.current_line, width=dp(4))
            return True
        return super().on_touch_move(touch)
    
    def on_touch_up(self, touch):
        if touch.grab_current is self:
            touch.ungrab(self)
            if len(self.current_line) >= 4:
                self.lines.append(self.current_line[:])
            self.current_line = []
            return True
        return super().on_touch_up(touch)

'''

# 读取原文件
with open('ui_kivy/chinese_app.py', 'r', encoding='utf-8') as f:
    content = f.read()

# 在 ChineseLearnApp 之前插入
marker = 'class ChineseLearnApp(App):'
pos = content.find(marker)

if pos != -1:
    new_content = content[:pos] + NEW_CODE + '\n\n' + content[pos:]
    with open('ui_kivy/chinese_app.py', 'w', encoding='utf-8') as f:
        f.write(new_content)
    print('成功添加描红写字功能!')
else:
    print('ERROR')
