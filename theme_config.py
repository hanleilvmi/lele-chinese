# -*- coding: utf-8 -*-
"""
乐乐学习乐园 - 汪汪队主题系统
"""

import json
import os
import random

CONFIG_FILE = os.path.join(os.path.dirname(os.path.abspath(__file__)), "theme_settings.json")

# 汪汪队主题配置
THEME = {
    "name": "汪汪队",
    "icon": "🐕",
    "voice": "zh-CN-YunxiNeural",
    "colors": {
        "bg": "#E3F2FD",           # 浅蓝背景
        "primary": "#1976D2",       # 主色（蓝色）
        "secondary": "#FF9800",     # 次色（橙色）
        "accent": "#4CAF50",        # 强调色（绿色）
        "success": "#4CAF50",       # 成功（绿色）
        "error": "#F44336",         # 错误（红色）
        "warning": "#FF9800",       # 警告（橙色）
        "card_bg": "#BBDEFB",       # 卡片背景
        "text": "#1565C0",          # 文字颜色
        "text_light": "#666666",    # 浅色文字
    },
    "praises": [
        "汪汪队，出动！答对啦！",
        "没有困难的工作，只有勇敢的狗狗！",
        "太棒了，你是最勇敢的小队员！",
        "耶！任务完成！",
        "狗狗们为你骄傲！",
        "莱德队长说你真厉害！",
        "阿奇说：干得漂亮！",
        "毛毛为你鼓掌！",
        "天天说你飞得真高！",
        "小砾说：挖到宝藏啦！",
    ],
    "encourages": [
        "没关系，汪汪队永不放弃！",
        "加油，勇敢的狗狗不怕困难！",
        "再试一次，你一定行！",
        "别担心，狗狗们相信你！",
        "莱德说：我们再来一次！",
    ],
    "welcome": "汪汪队，准备出动！",
    "goodbye": "汪汪队，任务完成！下次再见！",
    "decor": "🐾",
    # 角色列表（用于随机显示）
    "characters": [
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
}


def load_settings():
    """加载设置"""
    try:
        if os.path.exists(CONFIG_FILE):
            with open(CONFIG_FILE, 'r', encoding='utf-8') as f:
                return json.load(f)
    except:
        pass
    return {}


def save_settings(settings):
    """保存设置"""
    try:
        with open(CONFIG_FILE, 'w', encoding='utf-8') as f:
            json.dump(settings, f, ensure_ascii=False, indent=2)
    except:
        pass


def get_current_theme():
    """获取当前主题"""
    return THEME


def get_theme():
    """获取主题（兼容旧接口）"""
    return THEME


# 便捷函数
def get_voice():
    """获取语音"""
    return THEME["voice"]


def get_praise():
    """获取随机表扬语"""
    return random.choice(THEME["praises"])


def get_encourage():
    """获取随机鼓励语"""
    return random.choice(THEME["encourages"])


def get_colors():
    """获取颜色配置"""
    return THEME["colors"]


def get_welcome():
    """获取欢迎语"""
    return THEME["welcome"]


def get_random_character():
    """获取随机角色"""
    return random.choice(THEME["characters"])


class ThemeHelper:
    """主题辅助类 - 提供便捷的主题访问"""
    
    def __init__(self):
        self.theme = THEME
    
    @property
    def bg_color(self):
        return self.theme["colors"]["bg"]
    
    @property
    def primary(self):
        return self.theme["colors"]["primary"]
    
    @property
    def secondary(self):
        return self.theme["colors"]["secondary"]
    
    @property
    def accent(self):
        return self.theme["colors"]["accent"]
    
    @property
    def success(self):
        return self.theme["colors"]["success"]
    
    @property
    def error(self):
        return self.theme["colors"]["error"]
    
    @property
    def card_bg(self):
        return self.theme["colors"]["card_bg"]
    
    @property
    def text_color(self):
        return self.theme["colors"]["text"]
    
    @property
    def voice(self):
        return self.theme["voice"]
    
    @property
    def decor(self):
        return self.theme["decor"]
    
    @property
    def icon(self):
        return self.theme["icon"]
    
    def get_praise(self):
        return random.choice(self.theme["praises"])
    
    def get_encourage(self):
        return random.choice(self.theme["encourages"])
    
    def get_random_character(self):
        """获取随机角色 (id, name, color)"""
        return random.choice(self.theme["characters"])
    
    def get_character_by_name(self, name):
        """根据名字获取角色"""
        for char in self.theme["characters"]:
            if char[1] == name:
                return char
        return None


# 创建全局实例
theme_helper = ThemeHelper()
