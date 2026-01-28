# -*- coding: utf-8 -*-
"""更新菜单和App注册"""

with open('ui_kivy/chinese_app.py', 'r', encoding='utf-8') as f:
    content = f.read()

# 1. 更新菜单 - 添加描红写字入口
old_menu = """game_list = [
            ('字', '学汉字', '认识基础汉字', '#FF7043', 'chinese_learn'),
            ('图', '看图选字', '看图片选汉字', '#4ECDC4', 'chinese_picture'),
            ('?', '汉字测验', '考考你学会了吗', '#66BB6A', 'chinese_quiz'),
            ('对', '汉字配对', '找到相同的字', '#42A5F5', 'chinese_match'),
            ('锤', '打地鼠', '快速找汉字', '#FFD93D', 'chinese_whack'),
            ('关', '闯关模式', '一关一关闯', '#9C27B0', 'chinese_challenge'),
        ]"""

new_menu = """game_list = [
            ('字', '学汉字', '认识基础汉字', '#FF7043', 'chinese_learn'),
            ('写', '描红写字', '学写汉字', '#FF9800', 'chinese_write'),
            ('图', '看图选字', '看图片选汉字', '#4ECDC4', 'chinese_picture'),
            ('?', '汉字测验', '考考你学会了吗', '#66BB6A', 'chinese_quiz'),
            ('对', '汉字配对', '找到相同的字', '#42A5F5', 'chinese_match'),
            ('锤', '打地鼠', '快速找汉字', '#FFD93D', 'chinese_whack'),
            ('关', '闯关模式', '一关一关闯', '#9C27B0', 'chinese_challenge'),
        ]"""

content = content.replace(old_menu, new_menu)

# 2. 更新App注册 - 添加新Screen
old_reg = "sm.add_widget(ChineseChallengeScreen(name='chinese_challenge'))"
new_reg = """sm.add_widget(ChineseChallengeScreen(name='chinese_challenge'))
        sm.add_widget(ChineseWriteScreen(name='chinese_write'))"""

content = content.replace(old_reg, new_reg)

with open('ui_kivy/chinese_app.py', 'w', encoding='utf-8') as f:
    f.write(content)

print('菜单和注册更新完成!')
