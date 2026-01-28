# -*- coding: utf-8 -*-
# 添加汉字故事功能

story_code = '''

class ChineseStoryScreen(Screen):
    CHAR_STORIES = {
        '人': {'story': '很久以前，人们画了一个侧面站立的人形。这就是人字！', 'origin': '象形字，像人侧立'},
        '口': {'story': '张开嘴巴，方方正正。古人用方框表示嘴巴！', 'origin': '象形字，像张开的嘴'},
        '日': {'story': '太阳圆圆的，中间有光芒。古人画圆圈加一点，成了日字！', 'origin': '象形字，像太阳'},
        '月': {'story': '月亮弯弯像小船。古人看着月牙，画出了月字！', 'origin': '象形字，像月亮'},
        '山': {'story': '山峰一座连一座，中间高两边低。三个尖尖变成山字！', 'origin': '象形字，像山峰'},
        '水': {'story': '小河流水哗啦啦。古人画出水纹，成了水字！', 'origin': '象形字，像流水'},
        '火': {'story': '火苗跳动，上尖下宽。古人画出火焰，成了火字！', 'origin': '象形字，像火焰'},
        '手': {'story': '伸出小手数一数，五个手指真灵活！', 'origin': '象形字，像手形'},
        '足': {'story': '小脚丫踩地上，留下脚印。这就是足字！', 'origin': '象形字，像脚形'},
        '鸟': {'story': '小鸟有尖嘴巴，圆眼睛，漂亮羽毛！', 'origin': '象形字，像小鸟'},
        '田': {'story': '田地方方正正，中间有小路分开！', 'origin': '象形字，像田地'},
        '石': {'story': '山脚下有块大石头，硬硬的！', 'origin': '象形字，像石头'},
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

'''

with open('ui_kivy/chinese_app.py', 'r', encoding='utf-8') as f:
    content = f.read()

marker = 'class ChineseLearnApp(App):'
pos = content.find(marker)
if pos != -1:
    new_content = content[:pos] + story_code + '\n\n' + content[pos:]
    with open('ui_kivy/chinese_app.py', 'w', encoding='utf-8') as f:
        f.write(new_content)
    print('OK')
else:
    print('ERROR')
