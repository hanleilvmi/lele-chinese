# -*- coding: utf-8 -*-
"""
音频接口模块 - 定义音频播放的抽象接口
不同平台（Windows/Android）实现不同的具体类
"""
from abc import ABC, abstractmethod
from typing import Optional, List
import random


class AudioInterface(ABC):
    """音频播放抽象接口"""
    
    # 表扬语列表
    PRAISE_MESSAGES = [
        "太棒了！",
        "真聪明！",
        "做得好！",
        "你真厉害！",
        "非常正确！",
        "汪汪队为你骄傲！",
        "没有困难的工作，只有勇敢的狗狗！",
    ]
    
    # 鼓励语列表
    ENCOURAGE_MESSAGES = [
        "没关系，再试一次！",
        "加油，你可以的！",
        "别灰心，继续努力！",
        "汪汪队永不放弃！",
        "勇敢的狗狗不怕困难！",
    ]
    
    @abstractmethod
    def speak(self, text: str, rate: str = "+0%", lang: str = "cn"):
        """
        文字转语音
        :param text: 要朗读的文字
        :param rate: 语速，如 "+10%", "-10%"
        :param lang: 语言，"cn" 或 "en"
        """
        pass
    
    @abstractmethod
    def play_sound(self, sound_path: str):
        """
        播放音效文件
        :param sound_path: 音效文件路径
        """
        pass
    
    @abstractmethod
    def stop(self):
        """停止当前播放"""
        pass
    
    def play_praise(self):
        """播放随机表扬语"""
        message = random.choice(self.PRAISE_MESSAGES)
        self.speak(message, rate="+10%")
    
    def play_encourage(self):
        """播放随机鼓励语"""
        message = random.choice(self.ENCOURAGE_MESSAGES)
        self.speak(message)
    
    def speak_number(self, number: int, lang: str = "cn"):
        """朗读数字"""
        if lang == "cn":
            cn_numbers = ["零", "一", "二", "三", "四", "五", 
                         "六", "七", "八", "九", "十"]
            if 0 <= number <= 10:
                self.speak(cn_numbers[number])
            else:
                self.speak(str(number))
        else:
            self.speak(str(number), lang="en")
    
    def speak_letter(self, letter: str):
        """朗读字母"""
        self.speak(letter, lang="en")


class DummyAudio(AudioInterface):
    """空实现，用于测试或无音频环境"""
    
    def speak(self, text: str, rate: str = "+0%", lang: str = "cn"):
        print(f"[Audio] Speaking: {text} (rate={rate}, lang={lang})")
    
    def play_sound(self, sound_path: str):
        print(f"[Audio] Playing: {sound_path}")
    
    def stop(self):
        print("[Audio] Stopped")


# 平台特定实现将在各自的UI模块中提供
# 例如：
# - ui_tkinter/audio_tkinter.py -> EdgeTTSAudio (使用 edge_tts + pygame)
# - ui_kivy/audio_kivy.py -> KivyAudio (使用 kivy.core.audio 或 android.tts)
