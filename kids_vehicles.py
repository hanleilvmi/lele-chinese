# -*- coding: utf-8 -*-
"""
乐乐的交通乐园 v3.0 - 汪汪队主题版
汪汪队，准备出动！每个游戏由一位狗狗队员带领！
使用Canvas绘制彩色卡通图形
"""

import tkinter as tk
from tkinter import messagebox
import random
import threading
import asyncio
import os
import tempfile
import uuid
import time
import math

try:
    import edge_tts
    import pygame
    pygame.mixer.init()
    TTS_AVAILABLE = True
except ImportError:
    TTS_AVAILABLE = False

# 导入UI配置模块
try:
    from ui_config import (
        UI, Colors, ScreenConfig, get_font, get_path, 
        get_data_path, IS_MOBILE, PLATFORM
    )
    UI_CONFIG_AVAILABLE = True
except ImportError:
    UI_CONFIG_AVAILABLE = False
    IS_MOBILE = False

try:
    from voice_config_shared import get_voice, get_praises, get_encourages
    VOICE_CONFIG_AVAILABLE = True
except ImportError:
    VOICE_CONFIG_AVAILABLE = False

# 导入主题系统
try:
    from theme_config import get_theme, ThemeHelper, get_random_character
    from theme_drawings import ThemeDrawings
    THEME_AVAILABLE = True
    theme = ThemeHelper()
except ImportError:
    THEME_AVAILABLE = False
    theme = None


class KidsVehiclesApp:
    """汪汪队交通乐园 - 每个游戏由一位狗狗队员带领"""
    
    # 汪汪队角色与游戏对应关系
    PAW_PATROL_GAMES = {
        "rubble": {
            "name": "小砾", "color": "#FFC107", "role": "工程犬",
            "game": "挖掘机", "icon": "🏗️", "vehicle": "挖掘机",
            "intro": "小砾来啦！让我们一起开挖掘机挖宝藏！",
            "praise": "小砾说：挖得太棒了！",
        },
        "chase": {
            "name": "阿奇", "color": "#1976D2", "role": "警犬",
            "game": "赛车", "icon": "🏎️", "vehicle": "警车",
            "intro": "阿奇出动！跟我一起飙车吧！",
            "praise": "阿奇说：开得真快！",
        },
        "skye": {
            "name": "天天", "color": "#EC407A", "role": "飞行犬",
            "game": "飞机", "icon": "✈️", "vehicle": "直升机",
            "intro": "天天准备起飞！让我们翱翔天空！",
            "praise": "天天说：飞得真高！",
        },
        "marshall": {
            "name": "毛毛", "color": "#F44336", "role": "消防犬",
            "game": "消防车", "icon": "🚒", "vehicle": "消防车",
            "intro": "毛毛出动！火警响起，快去救火！",
            "praise": "毛毛说：救火成功！",
        },
        "rocky": {
            "name": "灰灰", "color": "#4CAF50", "role": "环保犬",
            "game": "火箭", "icon": "🚀", "vehicle": "回收车",
            "intro": "灰灰说：让我们发射火箭探索太空！",
            "praise": "灰灰说：发射成功！",
        },
        "zuma": {
            "name": "路马", "color": "#FF9800", "role": "水上救援犬",
            "game": "火车", "icon": "🚂", "vehicle": "气垫船",
            "intro": "路马来啦！让我们开火车运货！",
            "praise": "路马说：运送成功！",
        },
        "tracker": {
            "name": "阿克", "color": "#8BC34A", "role": "丛林犬",
            "game": "停车场", "icon": "🅿️", "vehicle": "吉普车",
            "intro": "阿克出动！把车停进车位！",
            "praise": "阿克说：停得真准！",
        },
        "everest": {
            "name": "珠珠", "color": "#00BCD4", "role": "雪山救援犬",
            "game": "红绿灯", "icon": "🚦", "vehicle": "雪地车",
            "intro": "珠珠提醒你：红灯停，绿灯行！",
            "praise": "珠珠说：交通规则记得牢！",
        },
        "liberty": {
            "name": "乐乐", "color": "#9C27B0", "role": "城市犬",
            "game": "小达人", "icon": "🎓", "vehicle": "摩托车",
            "intro": "乐乐来考考你！认识交通工具吗？",
            "praise": "乐乐说：你真聪明！",
        },
        "rex": {
            "name": "小克", "color": "#795548", "role": "恐龙犬",
            "game": "拼图", "icon": "🧩", "vehicle": "恐龙车",
            "intro": "小克说：来拼拼图吧！",
            "praise": "小克说：拼得真好！",
        },
    }
    
    def __init__(self):
        self.window = tk.Tk()
        self.window.title("🐾 汪汪队交通乐园 🐾")
        
        # 设置窗口大小并居中
        window_width = 1100
        window_height = 900
        screen_width = self.window.winfo_screenwidth()
        screen_height = self.window.winfo_screenheight()
        x = (screen_width - window_width) // 2
        y = (screen_height - window_height) // 2 - 30
        self.window.geometry(f"{window_width}x{window_height}+{x}+{y}")
        
        # 汪汪队主题背景色
        self.bg_color = "#E3F2FD"  # 汪汪队蓝色背景
        self.window.configure(bg=self.bg_color)
        
        # 保存画布尺寸
        self.canvas_width = 900
        self.canvas_height = 550
        
        # 语音系统
        self.tts_lock = threading.Lock()
        if VOICE_CONFIG_AVAILABLE:
            self.voice = get_voice()
            self.praises = get_praises()
            self.encourages = get_encourages()
        else:
            self.voice = "zh-CN-YunxiNeural"
            self.praises = [
                "汪汪队，任务完成！",
                "没有困难的工作，只有勇敢的狗狗！",
                "太棒了，你是最勇敢的小队员！",
            ]
            self.encourages = [
                "没关系，汪汪队永不放弃！",
                "加油，勇敢的狗狗不怕困难！",
                "再试一次，你一定行！",
            ]
        self.temp_dir = tempfile.gettempdir()
        
        self.audio_dir = os.path.join(os.path.dirname(os.path.abspath(__file__)), "audio")
        self.praise_audios = self._scan_audio_folder("praise")
        self.encourage_audios = self._scan_audio_folder("encourage")
        
        self.score = 0
        self.game_frame = None
        self.speech_id = 0
        self.praise_playing = False
        self.game_running = False
        self.current_pup = None  # 当前游戏的狗狗
        
        self.create_main_menu()

    # =====================================================
    # 语音系统
    # =====================================================
    def speak(self, text, rate="+0%"):
        if TTS_AVAILABLE:
            if self.praise_playing:
                self.window.after(4000, lambda: self._speak_normal(text, rate))
            else:
                self._speak_normal(text, rate)
    
    def _speak_normal(self, text, rate):
        if TTS_AVAILABLE:
            self.speech_id += 1
            current_id = self.speech_id
            try:
                pygame.mixer.music.stop()
            except:
                pass
            t = threading.Thread(target=self._speak_thread, args=(text, rate, current_id), daemon=True)
            t.start()
    
    def _speak_praise_direct(self, text, rate):
        t = threading.Thread(target=self._speak_thread_direct, args=(text, rate), daemon=True)
        t.start()
    
    def _speak_thread_direct(self, text, rate):
        audio_file = None
        try:
            audio_file = os.path.join(self.temp_dir, f"tts_{uuid.uuid4().hex}.mp3")
            async def generate():
                communicate = edge_tts.Communicate(text, self.voice, rate=rate)
                await communicate.save(audio_file)
            asyncio.run(generate())
            pygame.mixer.music.stop()
            pygame.mixer.music.load(audio_file)
            pygame.mixer.music.play()
            while pygame.mixer.music.get_busy():
                pygame.time.Clock().tick(10)
            time.sleep(0.1)
            try:
                os.remove(audio_file)
            except:
                pass
        except Exception as e:
            print(f"语音错误: {e}")
    
    def _speak_thread(self, text, rate, speech_id):
        audio_file = None
        try:
            if speech_id != self.speech_id:
                return
            audio_file = os.path.join(self.temp_dir, f"tts_{uuid.uuid4().hex}.mp3")
            async def generate():
                communicate = edge_tts.Communicate(text, self.voice, rate=rate)
                await communicate.save(audio_file)
            asyncio.run(generate())
            if speech_id != self.speech_id:
                try:
                    os.remove(audio_file)
                except:
                    pass
                return
            pygame.mixer.music.stop()
            pygame.mixer.music.load(audio_file)
            pygame.mixer.music.play()
            while pygame.mixer.music.get_busy():
                if speech_id != self.speech_id:
                    pygame.mixer.music.stop()
                    break
                pygame.time.Clock().tick(10)
            time.sleep(0.1)
            try:
                os.remove(audio_file)
            except:
                pass
        except Exception as e:
            print(f"语音错误: {e}")
    
    def _scan_audio_folder(self, folder_name):
        folder_path = os.path.join(self.audio_dir, folder_name)
        if not os.path.exists(folder_path):
            return []
        return [os.path.join(folder_path, f) for f in os.listdir(folder_path) 
                if f.lower().endswith(('.mp3', '.wav', '.ogg'))]
    
    def play_audio_file(self, file_path):
        def _play():
            try:
                pygame.mixer.music.stop()
                pygame.mixer.music.load(file_path)
                pygame.mixer.music.play()
            except Exception as e:
                print(f"播放音频错误: {e}")
        threading.Thread(target=_play, daemon=True).start()
    
    def speak_praise(self):
        self.praise_playing = True
        self.window.after(4000, self._clear_praise_flag)
        if self.praise_audios:
            self.play_audio_file(random.choice(self.praise_audios))
        else:
            self._speak_praise_direct(random.choice(self.praises), "+10%")
    
    def speak_encourage(self):
        self.praise_playing = True
        self.window.after(4000, self._clear_praise_flag)
        if self.encourage_audios:
            self.play_audio_file(random.choice(self.encourage_audios))
        else:
            self._speak_praise_direct(random.choice(self.encourages), "+0%")
    
    def _clear_praise_flag(self):
        self.praise_playing = False

    # =====================================================
    # 绘图工具 - 水果绘制
    # =====================================================
    def draw_apple(self, canvas, x, y, size=40):
        """绘制真实的苹果"""
        s = size / 40
        # 苹果主体
        canvas.create_oval(x-18*s, y-15*s, x+18*s, y+20*s, fill="#DC143C", outline="#8B0000", width=2)
        # 苹果高光
        canvas.create_oval(x-12*s, y-10*s, x-4*s, y+2*s, fill="#FF6B6B", outline="")
        # 苹果凹陷（顶部）
        canvas.create_arc(x-8*s, y-18*s, x+8*s, y-8*s, start=0, extent=180, fill="#B22222", outline="")
        # 苹果茎
        canvas.create_rectangle(x-2*s, y-22*s, x+2*s, y-15*s, fill="#8B4513", outline="#654321")
        # 叶子
        canvas.create_oval(x+2*s, y-25*s, x+15*s, y-18*s, fill="#228B22", outline="#006400")
    
    def draw_banana(self, canvas, x, y, size=40):
        """绘制真实的香蕉"""
        s = size / 40
        # 香蕉主体（弯曲形状）
        canvas.create_polygon(
            x-20*s, y+5*s,
            x-15*s, y-15*s,
            x-5*s, y-20*s,
            x+10*s, y-18*s,
            x+20*s, y-10*s,
            x+18*s, y+0*s,
            x+10*s, y+5*s,
            x-5*s, y+8*s,
            x-15*s, y+10*s,
            fill="#FFD700", outline="#DAA520", width=2, smooth=True
        )
        # 香蕉顶端
        canvas.create_oval(x-22*s, y+3*s, x-16*s, y+12*s, fill="#8B7355", outline="#6B5344")
        # 香蕉底端
        canvas.create_polygon(x+18*s, y-8*s, x+22*s, y-5*s, x+20*s, y+0*s, fill="#8B7355", outline="")
        # 香蕉条纹
        canvas.create_arc(x-10*s, y-15*s, x+15*s, y+5*s, start=30, extent=120, style="arc", outline="#BBA520", width=1)
    
    def draw_watermelon(self, canvas, x, y, size=40):
        """绘制真实的西瓜（切片）"""
        s = size / 40
        # 西瓜皮（外层绿色）
        canvas.create_arc(x-22*s, y-15*s, x+22*s, y+25*s, start=0, extent=180, fill="#228B22", outline="#006400", width=2)
        # 西瓜皮（白色层）
        canvas.create_arc(x-18*s, y-11*s, x+18*s, y+21*s, start=0, extent=180, fill="#98FB98", outline="")
        # 西瓜肉（红色）
        canvas.create_arc(x-15*s, y-8*s, x+15*s, y+18*s, start=0, extent=180, fill="#FF6B6B", outline="")
        # 西瓜籽
        for sx, sy in [(-8, 0), (0, 3), (8, 0), (-4, -5), (4, -5)]:
            canvas.create_oval(x+sx*s-2*s, y+sy*s-3*s, x+sx*s+2*s, y+sy*s+3*s, fill="#1a1a1a", outline="")
    
    def draw_grape(self, canvas, x, y, size=40):
        """绘制真实的葡萄串"""
        s = size / 40
        # 葡萄茎
        canvas.create_line(x, y-22*s, x, y-12*s, fill="#8B4513", width=int(3*s))
        canvas.create_oval(x-8*s, y-28*s, x+8*s, y-20*s, fill="#228B22", outline="#006400")
        # 葡萄粒（从上到下，从少到多）
        grape_positions = [
            [(0, -10)],
            [(-7, -2), (7, -2)],
            [(-10, 8), (0, 6), (10, 8)],
            [(-7, 16), (7, 16)],
        ]
        for row in grape_positions:
            for gx, gy in row:
                # 葡萄粒
                canvas.create_oval(x+gx*s-8*s, y+gy*s-8*s, x+gx*s+8*s, y+gy*s+8*s, 
                                  fill="#8B008B", outline="#4B0082", width=1)
                # 高光
                canvas.create_oval(x+gx*s-5*s, y+gy*s-6*s, x+gx*s-1*s, y+gy*s-2*s, 
                                  fill="#DA70D6", outline="")
    
    def draw_fruit(self, canvas, fruit_type, x, y, size=40):
        """根据类型绘制水果"""
        if fruit_type == "🍎" or fruit_type == "apple":
            self.draw_apple(canvas, x, y, size)
        elif fruit_type == "🍌" or fruit_type == "banana":
            self.draw_banana(canvas, x, y, size)
        elif fruit_type == "🍉" or fruit_type == "watermelon":
            self.draw_watermelon(canvas, x, y, size)
        elif fruit_type == "🍇" or fruit_type == "grape":
            self.draw_grape(canvas, x, y, size)
        else:
            # 默认用emoji
            canvas.create_text(x, y, text=fruit_type, font=("Segoe UI Emoji", int(size*0.6)))

    # =====================================================
    # 绘图工具 - 彩色卡通交通工具
    # =====================================================
    def draw_excavator(self, canvas, x, y, scale=1.0, arm_angle=30, tag=""):
        """绘制更真实的挖掘机"""
        s = scale
        
        # === 履带系统 ===
        # 履带外框
        canvas.create_polygon(
            x-45*s, y+25*s, x-50*s, y+32*s, x-50*s, y+42*s, x-45*s, y+48*s,
            x+55*s, y+48*s, x+60*s, y+42*s, x+60*s, y+32*s, x+55*s, y+25*s,
            fill="#2F2F2F", outline="#1a1a1a", width=2, tags=tag
        )
        # 履带纹理
        for i in range(-45, 56, 10):
            canvas.create_line(x+i*s, y+26*s, x+i*s, y+47*s, fill="#1a1a1a", width=2, tags=tag)
        # 履带轮子
        canvas.create_oval(x-42*s, y+28*s, x-28*s, y+45*s, fill="#444444", outline="#333333", width=2, tags=tag)
        canvas.create_oval(x-36*s, y+32*s, x-34*s, y+41*s, fill="#666666", tags=tag)
        canvas.create_oval(x+38*s, y+28*s, x+52*s, y+45*s, fill="#444444", outline="#333333", width=2, tags=tag)
        canvas.create_oval(x+42*s, y+32*s, x+48*s, y+41*s, fill="#666666", tags=tag)
        # 中间小轮
        for wx in [-15, 5, 25]:
            canvas.create_oval(x+wx*s-5*s, y+35*s, x+wx*s+5*s, y+45*s, fill="#444444", outline="#333333", tags=tag)
        
        # === 转台底座 ===
        canvas.create_oval(x-25*s, y+15*s, x+25*s, y+30*s, fill="#333333", outline="#222222", width=2, tags=tag)
        
        # === 车身主体 ===
        # 发动机舱
        canvas.create_rectangle(x-35*s, y-15*s, x+35*s, y+18*s, fill="#FFB800", outline="#CC9500", width=2, tags=tag)
        # 发动机舱细节
        canvas.create_rectangle(x+20*s, y-10*s, x+32*s, y+5*s, fill="#333333", outline="#222222", tags=tag)  # 散热格栅
        for gy in range(-8, 4, 4):
            canvas.create_line(x+22*s, y+gy*s, x+30*s, y+gy*s, fill="#555555", tags=tag)
        # 配重块
        canvas.create_rectangle(x+25*s, y+5*s, x+38*s, y+18*s, fill="#444444", outline="#333333", width=2, tags=tag)
        
        # === 驾驶室 ===
        # 驾驶室主体
        canvas.create_rectangle(x-30*s, y-55*s, x+15*s, y-15*s, fill="#FFB800", outline="#CC9500", width=2, tags=tag)
        # 驾驶室顶棚
        canvas.create_rectangle(x-32*s, y-60*s, x+17*s, y-55*s, fill="#CC9500", outline="#AA7700", width=2, tags=tag)
        # 前窗
        canvas.create_polygon(
            x-28*s, y-52*s, x+12*s, y-52*s, x+12*s, y-25*s, x-28*s, y-20*s,
            fill="#87CEEB", outline="#4682B4", width=2, tags=tag
        )
        # 窗框
        canvas.create_line(x-8*s, y-52*s, x-8*s, y-22*s, fill="#4682B4", width=2, tags=tag)
        canvas.create_line(x-28*s, y-38*s, x+12*s, y-38*s, fill="#4682B4", width=2, tags=tag)
        # 侧窗
        canvas.create_rectangle(x-30*s, y-50*s, x-28*s, y-25*s, fill="#87CEEB", outline="#4682B4", tags=tag)
        # 门把手
        canvas.create_rectangle(x+8*s, y-35*s, x+12*s, y-32*s, fill="#333333", tags=tag)
        
        # === 机械臂 ===
        arm_rad = math.radians(arm_angle)
        
        # 大臂基座
        canvas.create_oval(x+10*s, y-25*s, x+25*s, y-10*s, fill="#FFB800", outline="#CC9500", width=2, tags=tag)
        
        # 大臂
        arm_len = 70 * s
        arm_end_x = x + 17*s + arm_len * math.cos(arm_rad)
        arm_end_y = y - 17*s - arm_len * math.sin(arm_rad)
        # 大臂主体（梯形截面效果）
        canvas.create_polygon(
            x+12*s, y-22*s, x+22*s, y-22*s,
            arm_end_x+5*s, arm_end_y, arm_end_x-5*s, arm_end_y,
            fill="#FFB800", outline="#CC9500", width=2, tags=tag
        )
        # 液压缸
        canvas.create_line(x+5*s, y-30*s, arm_end_x-15*s, arm_end_y+10*s, fill="#888888", width=int(6*s), tags=tag)
        canvas.create_line(x+5*s, y-30*s, arm_end_x-15*s, arm_end_y+10*s, fill="#AAAAAA", width=int(3*s), tags=tag)
        
        # 小臂
        small_arm_angle = arm_angle - 40
        small_arm_rad = math.radians(small_arm_angle)
        small_arm_len = 50 * s
        bucket_x = arm_end_x + small_arm_len * math.cos(small_arm_rad)
        bucket_y = arm_end_y - small_arm_len * math.sin(small_arm_rad)
        canvas.create_polygon(
            arm_end_x-4*s, arm_end_y, arm_end_x+4*s, arm_end_y,
            bucket_x+3*s, bucket_y, bucket_x-3*s, bucket_y,
            fill="#FFB800", outline="#CC9500", width=2, tags=tag
        )
        # 小臂液压缸
        canvas.create_line(arm_end_x+10*s, arm_end_y-15*s, bucket_x, bucket_y-10*s, fill="#888888", width=int(4*s), tags=tag)
        
        # === 铲斗 ===
        bucket_angle = small_arm_angle - 30
        canvas.create_polygon(
            bucket_x-8*s, bucket_y,
            bucket_x+8*s, bucket_y,
            bucket_x+20*s, bucket_y+25*s,
            bucket_x+15*s, bucket_y+35*s,
            bucket_x-15*s, bucket_y+35*s,
            bucket_x-20*s, bucket_y+25*s,
            fill="#666666", outline="#444444", width=2, tags=tag
        )
        # 铲斗齿
        for tx in [-12, -4, 4, 12]:
            canvas.create_polygon(
                bucket_x+tx*s, bucket_y+35*s,
                bucket_x+(tx-3)*s, bucket_y+42*s,
                bucket_x+(tx+3)*s, bucket_y+42*s,
                fill="#444444", outline="#333333", tags=tag
            )
        
        return bucket_x, bucket_y + 35*s  # 返回铲斗位置

    def draw_race_car(self, canvas, x, y, scale=1.0, color="#FF0000"):
        """绘制更真实的赛车 - 车头朝右（用于主菜单预览）"""
        s = scale
        
        # === 车身底盘 ===
        canvas.create_polygon(
            x-55*s, y+8*s, x-50*s, y+15*s, x+50*s, y+15*s, x+55*s, y+8*s,
            x+55*s, y+5*s, x-55*s, y+5*s,
            fill="#222222", outline="#111111", width=1
        )
        
        # === 车身主体 ===
        # 后部
        canvas.create_polygon(
            x-50*s, y+5*s, x-45*s, y-5*s, x-40*s, y-10*s,
            x-35*s, y-10*s, x-35*s, y+5*s,
            fill=color, outline="", smooth=False
        )
        # 中部（座舱前）
        canvas.create_polygon(
            x-35*s, y+5*s, x-35*s, y-10*s, x-15*s, y-18*s,
            x+5*s, y-18*s, x+5*s, y+5*s,
            fill=color, outline=""
        )
        # 前部（引擎盖）
        canvas.create_polygon(
            x+5*s, y+5*s, x+5*s, y-15*s, x+25*s, y-12*s,
            x+45*s, y-5*s, x+55*s, y+5*s,
            fill=color, outline=""
        )
        # 车身轮廓
        canvas.create_line(x-50*s, y+5*s, x-45*s, y-5*s, x-40*s, y-10*s, x-15*s, y-18*s, 
                          x+5*s, y-18*s, x+25*s, y-12*s, x+45*s, y-5*s, x+55*s, y+5*s,
                          fill="#8B0000", width=2, smooth=True)
        
        # === 座舱 ===
        canvas.create_polygon(
            x-12*s, y-15*s, x-5*s, y-22*s, x+3*s, y-22*s, x+5*s, y-15*s,
            fill="#1a1a1a", outline="#333333", width=1
        )
        # 挡风玻璃
        canvas.create_polygon(
            x-10*s, y-15*s, x-5*s, y-20*s, x+2*s, y-20*s, x+4*s, y-15*s,
            fill="#87CEEB", outline="#4682B4", width=1
        )
        
        # === 尾翼 ===
        canvas.create_rectangle(x-52*s, y-18*s, x-48*s, y-10*s, fill="#222222", outline="#111111")
        canvas.create_rectangle(x-58*s, y-22*s, x-42*s, y-18*s, fill=color, outline="#8B0000", width=1)
        
        # === 前轮 ===
        canvas.create_oval(x+30*s, y+2*s, x+48*s, y+20*s, fill="#1a1a1a", outline="#111111", width=2)
        canvas.create_oval(x+34*s, y+6*s, x+44*s, y+16*s, fill="#333333", outline="")
        canvas.create_oval(x+37*s, y+9*s, x+41*s, y+13*s, fill="#666666", outline="")
        
        # === 后轮 ===
        canvas.create_oval(x-48*s, y+2*s, x-30*s, y+20*s, fill="#1a1a1a", outline="#111111", width=2)
        canvas.create_oval(x-44*s, y+6*s, x-34*s, y+16*s, fill="#333333", outline="")
        canvas.create_oval(x-41*s, y+9*s, x-37*s, y+13*s, fill="#666666", outline="")
        
        # === 装饰 ===
        # 赛车编号
        canvas.create_oval(x-5*s, y-8*s, x+8*s, y+5*s, fill="white", outline="#DDD")
        canvas.create_text(x+1.5*s, y-1.5*s, text="1", font=("Arial", int(10*s), "bold"), fill=color)
        # 进气口
        canvas.create_rectangle(x+35*s, y-8*s, x+45*s, y-3*s, fill="#222222", outline="#111111")
        
        # 前轮
        canvas.create_oval(x-35*s, y+5*s, x-15*s, y+25*s, fill="#222222", outline="#111111", width=2)
        canvas.create_oval(x-30*s, y+10*s, x-20*s, y+20*s, fill="#666666", outline="#444444")
        
        # 后轮
        canvas.create_oval(x+15*s, y+5*s, x+35*s, y+25*s, fill="#222222", outline="#111111", width=2)
        canvas.create_oval(x+20*s, y+10*s, x+30*s, y+20*s, fill="#666666", outline="#444444")
        
        # 赛车编号
        canvas.create_oval(x-5*s, y-12*s, x+10*s, y+2*s, fill="white", outline="#DDD")
        canvas.create_text(x+2*s, y-5*s, text="1", font=("Arial", int(10*s), "bold"), fill=color)

    def draw_race_car_up(self, canvas, x, y, scale=1.0, color="#FF0000"):
        """绘制彩色赛车 - 车头朝上（用于赛车游戏）"""
        s = scale
        # 车身 - 流线型，车头朝上
        canvas.create_polygon(
            x-15*s, y+50*s,    # 左后
            x-20*s, y+20*s,    # 左侧
            x-15*s, y-30*s,    # 左前
            x, y-50*s,         # 车头尖端
            x+15*s, y-30*s,    # 右前
            x+20*s, y+20*s,    # 右侧
            x+15*s, y+50*s,    # 右后
            fill=color, outline="#8B0000", width=2, smooth=True
        )
        
        # 车窗 - 浅蓝色
        canvas.create_polygon(
            x-10*s, y-10*s,
            x, y-25*s,
            x+10*s, y-10*s,
            x+8*s, y+10*s,
            x-8*s, y+10*s,
            fill="#87CEEB", outline="#4682B4", width=1
        )
        
        # 左轮
        canvas.create_oval(x-25*s, y+10*s, x-15*s, y+35*s, fill="#222222", outline="#111111", width=2)
        canvas.create_oval(x-23*s, y+15*s, x-17*s, y+30*s, fill="#666666")
        
        # 右轮
        canvas.create_oval(x+15*s, y+10*s, x+25*s, y+35*s, fill="#222222", outline="#111111", width=2)
        canvas.create_oval(x+17*s, y+15*s, x+23*s, y+30*s, fill="#666666")
        
        # 赛车编号
        canvas.create_oval(x-8*s, y+15*s, x+8*s, y+35*s, fill="white", outline="#DDD")
        canvas.create_text(x, y+25*s, text="1", font=("Arial", int(12*s), "bold"), fill=color)

    def draw_airplane(self, canvas, x, y, scale=1.0, color="#4169E1"):
        """绘制更真实的客机"""
        s = scale
        
        # === 机身 ===
        # 机身主体（流线型）
        canvas.create_polygon(
            x-65*s, y,           # 尾部
            x-60*s, y-8*s,
            x-40*s, y-12*s,
            x+20*s, y-12*s,
            x+50*s, y-8*s,
            x+70*s, y,           # 机头
            x+50*s, y+8*s,
            x+20*s, y+12*s,
            x-40*s, y+12*s,
            x-60*s, y+8*s,
            fill="white", outline="#CCCCCC", width=2, smooth=True
        )
        # 机身蓝色条纹
        canvas.create_polygon(
            x-55*s, y-3*s, x+55*s, y-3*s, x+55*s, y+3*s, x-55*s, y+3*s,
            fill=color, outline=""
        )
        # 机身窗户
        for wx in range(-40, 40, 12):
            canvas.create_oval(x+wx*s-3*s, y-8*s, x+wx*s+3*s, y-2*s, fill="#87CEEB", outline="#4682B4", width=1)
        
        # === 机头 ===
        canvas.create_polygon(
            x+55*s, y-6*s, x+75*s, y, x+55*s, y+6*s,
            fill="#333333", outline="#222222", width=1, smooth=True
        )
        # 驾驶舱窗户
        canvas.create_polygon(
            x+45*s, y-7*s, x+60*s, y-4*s, x+65*s, y, x+60*s, y+4*s, x+45*s, y+7*s,
            fill="#1a3a5c", outline="#0f2840", width=1
        )
        canvas.create_polygon(
            x+48*s, y-5*s, x+58*s, y-3*s, x+62*s, y, x+58*s, y+3*s, x+48*s, y+5*s,
            fill="#87CEEB", outline=""
        )
        
        # === 主机翼 ===
        # 上机翼
        canvas.create_polygon(
            x-15*s, y-10*s,      # 机身连接点
            x+15*s, y-10*s,
            x+25*s, y-50*s,      # 翼尖
            x+20*s, y-52*s,
            x-5*s, y-52*s,
            x-25*s, y-12*s,
            fill="#E8E8E8", outline="#AAAAAA", width=2
        )
        # 下机翼
        canvas.create_polygon(
            x-15*s, y+10*s,
            x+15*s, y+10*s,
            x+25*s, y+50*s,
            x+20*s, y+52*s,
            x-5*s, y+52*s,
            x-25*s, y+12*s,
            fill="#E8E8E8", outline="#AAAAAA", width=2
        )
        # 机翼蓝色标记
        canvas.create_polygon(x+5*s, y-48*s, x+18*s, y-48*s, x+20*s, y-50*s, x+8*s, y-50*s, fill=color, outline="")
        canvas.create_polygon(x+5*s, y+48*s, x+18*s, y+48*s, x+20*s, y+50*s, x+8*s, y+50*s, fill=color, outline="")
        
        # === 引擎 ===
        # 上引擎
        canvas.create_oval(x-5*s, y-48*s, x+8*s, y-38*s, fill="#444444", outline="#333333", width=2)
        canvas.create_oval(x-3*s, y-46*s, x+6*s, y-40*s, fill="#222222", outline="")
        # 下引擎
        canvas.create_oval(x-5*s, y+38*s, x+8*s, y+48*s, fill="#444444", outline="#333333", width=2)
        canvas.create_oval(x-3*s, y+40*s, x+6*s, y+46*s, fill="#222222", outline="")
        
        # === 尾翼 ===
        # 垂直尾翼
        canvas.create_polygon(
            x-55*s, y-8*s,
            x-45*s, y-8*s,
            x-40*s, y-35*s,
            x-50*s, y-38*s,
            x-60*s, y-35*s,
            fill=color, outline="#1E3A8A", width=2
        )
        # 尾翼标志
        canvas.create_polygon(x-52*s, y-32*s, x-45*s, y-30*s, x-45*s, y-25*s, x-52*s, y-27*s, fill="white", outline="")
        
        # 水平尾翼
        canvas.create_polygon(
            x-55*s, y-5*s, x-45*s, y-5*s, x-40*s, y-18*s, x-55*s, y-18*s,
            fill="#E8E8E8", outline="#AAAAAA", width=1
        )
        canvas.create_polygon(
            x-55*s, y+5*s, x-45*s, y+5*s, x-40*s, y+18*s, x-55*s, y+18*s,
            fill="#E8E8E8", outline="#AAAAAA", width=1
        )

    def draw_fire_truck(self, canvas, x, y, scale=1.0):
        """绘制更真实的消防车"""
        s = scale
        
        # === 底盘 ===
        canvas.create_rectangle(x-55*s, y+15*s, x+60*s, y+22*s, fill="#222222", outline="#111111", width=1)
        
        # === 车身主体 ===
        # 后部储物箱
        canvas.create_rectangle(x-55*s, y-15*s, x-10*s, y+15*s, fill="#CC0000", outline="#8B0000", width=2)
        # 储物箱门
        for dx in [-45, -30]:
            canvas.create_rectangle(x+dx*s, y-12*s, x+(dx+12)*s, y+12*s, fill="#AA0000", outline="#880000", width=1)
            canvas.create_oval(x+(dx+10)*s, y-2*s, x+(dx+12)*s, y+2*s, fill="#C0C0C0", outline="")
        
        # 中部水箱
        canvas.create_rectangle(x-10*s, y-20*s, x+25*s, y+15*s, fill="#CC0000", outline="#8B0000", width=2)
        # 水箱细节
        canvas.create_rectangle(x-5*s, y-15*s, x+20*s, y-5*s, fill="#AA0000", outline="#880000", width=1)
        canvas.create_text(x+7*s, y-10*s, text="WATER", font=("Arial", int(6*s), "bold"), fill="white")
        
        # === 驾驶室 ===
        canvas.create_polygon(
            x+25*s, y+15*s, x+25*s, y-25*s, x+30*s, y-35*s,
            x+60*s, y-35*s, x+65*s, y-25*s, x+65*s, y+15*s,
            fill="#CC0000", outline="#8B0000", width=2
        )
        # 前挡风玻璃
        canvas.create_polygon(
            x+30*s, y-32*s, x+58*s, y-32*s, x+62*s, y-20*s, x+28*s, y-20*s,
            fill="#87CEEB", outline="#4682B4", width=2
        )
        # 侧窗
        canvas.create_rectangle(x+28*s, y-18*s, x+40*s, y-5*s, fill="#87CEEB", outline="#4682B4", width=1)
        canvas.create_rectangle(x+45*s, y-18*s, x+62*s, y-5*s, fill="#87CEEB", outline="#4682B4", width=1)
        
        # === 警灯 ===
        canvas.create_rectangle(x+35*s, y-42*s, x+55*s, y-35*s, fill="#333333", outline="#222222", width=1)
        canvas.create_oval(x+36*s, y-41*s, x+44*s, y-36*s, fill="#FF0000", outline="#CC0000")
        canvas.create_oval(x+46*s, y-41*s, x+54*s, y-36*s, fill="#0066FF", outline="#0044CC")
        
        # === 云梯 ===
        # 云梯底座
        canvas.create_rectangle(x-45*s, y-25*s, x+15*s, y-18*s, fill="#444444", outline="#333333", width=1)
        # 云梯主体
        canvas.create_polygon(
            x-42*s, y-28*s, x+12*s, y-28*s, x+12*s, y-32*s, x-42*s, y-32*s,
            fill="#C0C0C0", outline="#808080", width=1
        )
        # 云梯横杆
        for lx in range(-40, 12, 12):
            canvas.create_line(x+lx*s, y-28*s, x+lx*s, y-32*s, fill="#808080", width=2)
        
        # === 轮子 ===
        # 后轮（双轮）
        for wy in [0, 8]:
            canvas.create_oval(x-48*s, y+12*s+wy*s, x-30*s, y+30*s+wy*s, fill="#1a1a1a", outline="#111111", width=2)
        canvas.create_oval(x-44*s, y+18*s, x-34*s, y+28*s, fill="#333333", outline="")
        canvas.create_oval(x-41*s, y+21*s, x-37*s, y+25*s, fill="#666666", outline="")
        
        # 前轮
        canvas.create_oval(x+40*s, y+12*s, x+58*s, y+30*s, fill="#1a1a1a", outline="#111111", width=2)
        canvas.create_oval(x+44*s, y+16*s, x+54*s, y+26*s, fill="#333333", outline="")
        canvas.create_oval(x+47*s, y+19*s, x+51*s, y+23*s, fill="#666666", outline="")
        
        # === 装饰 ===
        # 119标志
        canvas.create_rectangle(x-8*s, y+0*s, x+22*s, y+12*s, fill="white", outline="#DDD")
        canvas.create_text(x+7*s, y+6*s, text="119", font=("Arial", int(10*s), "bold"), fill="#CC0000")
        # 前灯
        canvas.create_oval(x+62*s, y-8*s, x+68*s, y-2*s, fill="#FFFF00", outline="#FFD700", width=1)
        canvas.create_oval(x+62*s, y+2*s, x+68*s, y+8*s, fill="#FFFF00", outline="#FFD700", width=1)

    def draw_rocket(self, canvas, x, y, scale=1.0, flame=False):
        """绘制更真实的火箭"""
        s = scale
        
        # === 火箭头（整流罩）===
        canvas.create_polygon(
            x, y-90*s,
            x-8*s, y-70*s,
            x-15*s, y-50*s,
            x-18*s, y-40*s,
            x+18*s, y-40*s,
            x+15*s, y-50*s,
            x+8*s, y-70*s,
            fill="#CC0000", outline="#8B0000", width=2, smooth=True
        )
        # 头部高光
        canvas.create_arc(x-5*s, y-85*s, x+5*s, y-70*s, start=45, extent=90, fill="#FF3333", outline="")
        
        # === 火箭身（第一级）===
        canvas.create_rectangle(x-18*s, y-40*s, x+18*s, y+25*s, fill="#F5F5F5", outline="#CCCCCC", width=2)
        # 火箭身条纹
        canvas.create_rectangle(x-18*s, y-35*s, x+18*s, y-30*s, fill="#CC0000", outline="")
        canvas.create_rectangle(x-18*s, y+15*s, x+18*s, y+20*s, fill="#CC0000", outline="")
        # 国旗/标志区域
        canvas.create_rectangle(x-12*s, y-20*s, x+12*s, y+5*s, fill="#CC0000", outline="#8B0000", width=1)
        canvas.create_text(x, y-7*s, text="CN", font=("Arial", int(12*s), "bold"), fill="#FFD700")
        
        # === 舷窗 ===
        canvas.create_oval(x-8*s, y-28*s, x+8*s, y-12*s, fill="#1a1a1a", outline="#333333", width=2)
        canvas.create_oval(x-6*s, y-26*s, x+6*s, y-14*s, fill="#87CEEB", outline="")
        canvas.create_arc(x-5*s, y-25*s, x+3*s, y-17*s, start=45, extent=90, fill="#AADDFF", outline="")
        
        # === 尾翼（4个）===
        # 左尾翼
        canvas.create_polygon(
            x-18*s, y+5*s, x-35*s, y+35*s, x-35*s, y+40*s, x-18*s, y+25*s,
            fill="#333333", outline="#222222", width=1
        )
        # 右尾翼
        canvas.create_polygon(
            x+18*s, y+5*s, x+35*s, y+35*s, x+35*s, y+40*s, x+18*s, y+25*s,
            fill="#333333", outline="#222222", width=1
        )
        # 前后尾翼（较小）
        canvas.create_polygon(
            x-5*s, y+15*s, x-5*s, y+35*s, x-12*s, y+40*s, x-12*s, y+25*s,
            fill="#444444", outline="#333333", width=1
        )
        canvas.create_polygon(
            x+5*s, y+15*s, x+5*s, y+35*s, x+12*s, y+40*s, x+12*s, y+25*s,
            fill="#444444", outline="#333333", width=1
        )
        
        # === 发动机喷口 ===
        canvas.create_polygon(
            x-15*s, y+25*s, x+15*s, y+25*s, x+12*s, y+35*s, x-12*s, y+35*s,
            fill="#555555", outline="#333333", width=1
        )
        canvas.create_oval(x-10*s, y+30*s, x+10*s, y+40*s, fill="#333333", outline="#222222", width=1)
        
        # === 火焰 ===
        if flame:
            import random
            # 主火焰
            for i in range(5):
                flame_h = random.randint(40, 70) * s
                flame_w = random.randint(5, 12) * s
                offset_x = random.randint(-5, 5) * s
                colors = ["#FF4500", "#FF6600", "#FFCC00", "#FFFF00", "#FFFFFF"]
                canvas.create_polygon(
                    x + offset_x, y + 35*s + flame_h,
                    x + offset_x - flame_w, y + 35*s,
                    x + offset_x + flame_w, y + 35*s,
                    fill=random.choice(colors), outline=""
                )
            # 烟雾
            for i in range(3):
                smoke_y = y + 50*s + i * 20*s
                smoke_size = (8 + i * 4) * s
                alpha = 150 - i * 40
                smoke_color = f"#{alpha:02x}{alpha:02x}{alpha:02x}"
                canvas.create_oval(x-smoke_size, smoke_y-smoke_size/2, x+smoke_size, smoke_y+smoke_size/2,
                                  fill=smoke_color, outline="")

    def draw_train(self, canvas, x, y, scale=1.0, color="#228B22"):
        """绘制更真实的蒸汽火车头"""
        s = scale
        
        # === 锅炉（圆柱形车身）===
        # 锅炉主体 - 深绿色圆角矩形
        canvas.create_oval(x-50*s, y-25*s, x-30*s, y+10*s, fill=color, outline="#004400", width=2)  # 前端圆形
        canvas.create_rectangle(x-40*s, y-25*s, x+20*s, y+10*s, fill=color, outline="")  # 主体
        canvas.create_oval(x+10*s, y-25*s, x+30*s, y+10*s, fill=color, outline="#004400", width=2)  # 后端
        # 锅炉顶部高光
        canvas.create_arc(x-40*s, y-30*s, x+20*s, y-10*s, start=0, extent=180, fill="#2E8B2E", outline="")
        # 锅炉环带
        for bx in [-30, -10, 10]:
            canvas.create_rectangle(x+bx*s-2*s, y-25*s, x+bx*s+2*s, y+10*s, fill="#004400", outline="")
        
        # === 驾驶室 ===
        # 驾驶室主体
        canvas.create_rectangle(x+20*s, y-50*s, x+55*s, y+10*s, fill=color, outline="#004400", width=2)
        # 驾驶室顶棚
        canvas.create_rectangle(x+15*s, y-55*s, x+60*s, y-50*s, fill="#8B4513", outline="#654321", width=2)
        # 驾驶室窗户
        canvas.create_rectangle(x+25*s, y-45*s, x+38*s, y-25*s, fill="#87CEEB", outline="#4682B4", width=2)
        canvas.create_rectangle(x+42*s, y-45*s, x+52*s, y-25*s, fill="#87CEEB", outline="#4682B4", width=2)
        # 窗户十字框
        canvas.create_line(x+31.5*s, y-45*s, x+31.5*s, y-25*s, fill="#4682B4", width=1)
        canvas.create_line(x+25*s, y-35*s, x+38*s, y-35*s, fill="#4682B4", width=1)
        
        # === 烟囱 ===
        # 烟囱底座
        canvas.create_rectangle(x-35*s, y-35*s, x-25*s, y-25*s, fill="#222222", outline="#111111", width=2)
        # 烟囱主体（锥形）
        canvas.create_polygon(x-38*s, y-35*s, x-22*s, y-35*s, x-25*s, y-55*s, x-35*s, y-55*s, 
                             fill="#333333", outline="#222222", width=2)
        # 烟囱顶部
        canvas.create_oval(x-40*s, y-60*s, x-20*s, y-52*s, fill="#444444", outline="#333333", width=2)
        # 烟雾
        for i, (dx, dy, size) in enumerate([(-30, -70, 8), (-35, -80, 10), (-28, -90, 12)]):
            alpha = 200 - i * 50
            smoke_color = f"#{alpha:02x}{alpha:02x}{alpha:02x}"
            canvas.create_oval(x+dx*s-size*s, y+dy*s-size*s, x+dx*s+size*s, y+dy*s+size*s, 
                              fill=smoke_color, outline="")
        
        # === 蒸汽圆顶 ===
        canvas.create_oval(x-10*s, y-40*s, x+5*s, y-25*s, fill="#DAA520", outline="#B8860B", width=2)
        
        # === 前灯 ===
        canvas.create_oval(x-55*s, y-15*s, x-45*s, y+0*s, fill="#FFFF00", outline="#FFD700", width=2)
        # 灯光效果
        canvas.create_oval(x-53*s, y-12*s, x-47*s, y-3*s, fill="#FFFFAA", outline="")
        
        # === 排障器（牛栏）===
        canvas.create_polygon(x-55*s, y+15*s, x-65*s, y+25*s, x-55*s, y+25*s, fill="#333333", outline="#222222")
        canvas.create_line(x-63*s, y+20*s, x-55*s, y+20*s, fill="#555555", width=2)
        canvas.create_line(x-60*s, y+17*s, x-55*s, y+23*s, fill="#555555", width=2)
        
        # === 底盘 ===
        canvas.create_rectangle(x-50*s, y+10*s, x+55*s, y+18*s, fill="#333333", outline="#222222", width=2)
        
        # === 大轮子（驱动轮）===
        for wx in [-25, 10]:
            # 轮子外圈
            canvas.create_oval(x+wx*s-18*s, y+12*s, x+wx*s+18*s, y+48*s, fill="#222222", outline="#111111", width=3)
            # 轮子内圈
            canvas.create_oval(x+wx*s-14*s, y+16*s, x+wx*s+14*s, y+44*s, fill="#333333", outline="#222222", width=2)
            # 轮毂
            canvas.create_oval(x+wx*s-6*s, y+24*s, x+wx*s+6*s, y+36*s, fill="#8B0000", outline="#660000", width=2)
            # 轮辐
            for angle in [0, 45, 90, 135]:
                import math
                rad = math.radians(angle)
                x1 = x + wx*s + 6*s * math.cos(rad)
                y1 = y + 30*s + 6*s * math.sin(rad)
                x2 = x + wx*s + 14*s * math.cos(rad)
                y2 = y + 30*s + 14*s * math.sin(rad)
                canvas.create_line(x1, y1, x2, y2, fill="#666666", width=2)
        
        # === 小轮子（导轮）===
        canvas.create_oval(x+40*s-10*s, y+20*s, x+40*s+10*s, y+40*s, fill="#222222", outline="#111111", width=2)
        canvas.create_oval(x+40*s-5*s, y+25*s, x+40*s+5*s, y+35*s, fill="#444444", outline="")
        
        # === 连杆 ===
        canvas.create_line(x-25*s, y+30*s, x+10*s, y+30*s, fill="#8B4513", width=int(5*s))
        canvas.create_oval(x-27*s, y+27*s, x-23*s, y+33*s, fill="#CD853F", outline="#8B4513")
        canvas.create_oval(x+8*s, y+27*s, x+12*s, y+33*s, fill="#CD853F", outline="#8B4513")
        
        # === 汽缸 ===
        canvas.create_rectangle(x-45*s, y+5*s, x-35*s, y+18*s, fill="#555555", outline="#333333", width=2)

    # =====================================================
    # 成就系统
    # =====================================================
    def init_achievements(self):
        """初始化成就系统"""
        if not hasattr(self, 'achievements'):
            self.achievements = {
                "first_drive": {"name": "小队员", "desc": "完成第一次任务", "icon": "�", "unlocked": False, "pup": "chase"},
                "speed_demon": {"name": "飞车阿奇", "desc": "赛车得分超过100", "icon": "🏎️", "unlocked": False, "pup": "chase"},
                "fire_hero": {"name": "消防毛毛", "desc": "消防车救火成功5次", "icon": "🚒", "unlocked": False, "pup": "marshall"},
                "pilot": {"name": "飞行天天", "desc": "飞机收集50颗星星", "icon": "✈️", "unlocked": False, "pup": "skye"},
                "astronaut": {"name": "太空灰灰", "desc": "成功发射火箭3次", "icon": "🚀", "unlocked": False, "pup": "rocky"},
                "parking_master": {"name": "停车阿克", "desc": "完美停车5次", "icon": "🅿️", "unlocked": False, "pup": "tracker"},
                "traffic_expert": {"name": "安全珠珠", "desc": "红绿灯答对10题", "icon": "", "unlocked": False, "pup": "everest"},
                "collector": {"name": "收藏家", "desc": "总分超过500", "icon": "⭐", "unlocked": False},
                "explorer": {"name": "探险家", "desc": "玩过所有游戏", "icon": "🗺️", "unlocked": False},
            }
            self.games_played = set()
            self.fire_rescues = 0
            self.stars_collected = 0
            self.rockets_launched = 0
            self.perfect_parks = 0
            self.traffic_correct = 0
    
    def check_achievement(self, achievement_id):
        """检查并解锁成就"""
        if not hasattr(self, 'achievements'):
            self.init_achievements()
        
        if achievement_id in self.achievements and not self.achievements[achievement_id]["unlocked"]:
            self.achievements[achievement_id]["unlocked"] = True
            self.show_achievement_popup(achievement_id)
    
    def show_achievement_popup(self, achievement_id):
        """显示成就解锁弹窗 - 汪汪队主题"""
        ach = self.achievements[achievement_id]
        pup_id = ach.get("pup", "chase")
        pup = self.PAW_PATROL_GAMES.get(pup_id, self.PAW_PATROL_GAMES["chase"])
        
        popup = tk.Toplevel(self.window)
        popup.overrideredirect(True)
        popup.attributes('-topmost', True)
        
        w, h = 350, 220
        x = self.window.winfo_x() + (self.window.winfo_width() - w) // 2
        y = self.window.winfo_y() + 100
        popup.geometry(f"{w}x{h}+{x}+{y}")
        popup.configure(bg=pup["color"])
        
        tk.Label(popup, text="🏆 汪汪队成就解锁！🏆", font=("微软雅黑", 16, "bold"),
                bg=pup["color"], fg="white").pack(pady=8)
        
        # 狗狗头像
        avatar_canvas = tk.Canvas(popup, width=70, height=70, bg=pup["color"], highlightthickness=0)
        avatar_canvas.pack()
        draw_func = self.get_pup_draw_func(pup_id)
        if draw_func:
            draw_func(avatar_canvas, 35, 40, 0.5)
        
        tk.Label(popup, text=f"{ach['icon']} {ach['name']}", font=("微软雅黑", 18, "bold"),
                bg=pup["color"], fg="white").pack(pady=3)
        tk.Label(popup, text=ach['desc'], font=("微软雅黑", 11),
                bg=pup["color"], fg="white").pack(pady=3)
        
        self.speak(f"汪汪队恭喜你！解锁成就：{ach['name']}！")
        popup.after(3500, popup.destroy)
    
    def show_achievements(self):
        """显示成就页面 - 汪汪队主题"""
        if not hasattr(self, 'achievements'):
            self.init_achievements()
        
        for widget in self.window.winfo_children():
            widget.destroy()
        self.window.configure(bg="#1a1a2e")
        
        main_frame = tk.Frame(self.window, bg="#1a1a2e")
        main_frame.pack(fill=tk.BOTH, expand=True, padx=20, pady=10)
        
        tk.Button(main_frame, text="🏠 返回", font=("微软雅黑", 11),
                  bg="#96CEB4", fg="white", command=self.create_main_menu).pack(anchor=tk.W, pady=5)
        
        tk.Label(main_frame, text="🏆 我的成就 🏆", font=("微软雅黑", 28, "bold"),
                bg="#1a1a2e", fg="#FFD700").pack(pady=15)
        
        # 统计
        unlocked = sum(1 for a in self.achievements.values() if a["unlocked"])
        total = len(self.achievements)
        tk.Label(main_frame, text=f"已解锁: {unlocked}/{total}", font=("微软雅黑", 14),
                bg="#1a1a2e", fg="#AAA").pack(pady=5)
        
        # 成就列表
        ach_frame = tk.Frame(main_frame, bg="#1a1a2e")
        ach_frame.pack(pady=20)
        
        for i, (aid, ach) in enumerate(self.achievements.items()):
            row, col = i // 3, i % 3
            
            if ach["unlocked"]:
                bg_color = "#4CAF50"
                fg_color = "white"
                icon = ach["icon"]
            else:
                bg_color = "#333"
                fg_color = "#666"
                icon = "🔒"
            
            card = tk.Frame(ach_frame, bg=bg_color, relief=tk.RAISED, bd=3)
            card.grid(row=row, column=col, padx=10, pady=10)
            
            tk.Label(card, text=icon, font=("Segoe UI Emoji", 30),
                    bg=bg_color, fg=fg_color).pack(pady=5)
            tk.Label(card, text=ach["name"], font=("微软雅黑", 12, "bold"),
                    bg=bg_color, fg=fg_color, width=10).pack()
            tk.Label(card, text=ach["desc"], font=("微软雅黑", 9),
                    bg=bg_color, fg=fg_color, wraplength=100).pack(pady=5)
        
        self.speak("这是你的成就！继续努力解锁更多！")

    # =====================================================
    # 汪汪队辅助方法
    # =====================================================
    def get_pup_draw_func(self, pup_id):
        """获取狗狗的绘制函数"""
        if not THEME_AVAILABLE:
            return None
        draw_funcs = {
            "rubble": ThemeDrawings.draw_puppy_rubble,
            "chase": ThemeDrawings.draw_puppy_chase,
            "skye": ThemeDrawings.draw_puppy_skye,
            "marshall": ThemeDrawings.draw_puppy_marshall,
            "rocky": ThemeDrawings.draw_puppy_rocky,
            "zuma": ThemeDrawings.draw_puppy_zuma,
            "tracker": ThemeDrawings.draw_puppy_tracker,
            "everest": ThemeDrawings.draw_puppy_everest,
            "liberty": ThemeDrawings.draw_puppy_liberty,
            "rex": ThemeDrawings.draw_puppy_rex,
        }
        return draw_funcs.get(pup_id)
    
    def show_pup_intro(self, pup_id, callback):
        """显示狗狗介绍动画，然后执行回调"""
        pup = self.PAW_PATROL_GAMES.get(pup_id)
        if not pup:
            callback()
            return
        
        self.current_pup = pup_id
        
        # 创建介绍弹窗
        popup = tk.Toplevel(self.window)
        popup.title("汪汪队出动！")
        popup.geometry("400x350")
        popup.configure(bg=pup["color"])
        popup.transient(self.window)
        popup.grab_set()
        
        # 居中显示
        popup.update_idletasks()
        x = self.window.winfo_x() + (self.window.winfo_width() - 400) // 2
        y = self.window.winfo_y() + (self.window.winfo_height() - 350) // 2
        popup.geometry(f"+{x}+{y}")
        
        # 狗狗头像画布
        avatar_canvas = tk.Canvas(popup, width=150, height=150, bg=pup["color"], highlightthickness=0)
        avatar_canvas.pack(pady=15)
        
        # 绘制狗狗
        draw_func = self.get_pup_draw_func(pup_id)
        if draw_func:
            draw_func(avatar_canvas, 75, 85, 1.2)
        
        # 狗狗名字和角色
        tk.Label(popup, text=f"🐾 {pup['name']} 🐾", font=("微软雅黑", 24, "bold"),
                bg=pup["color"], fg="white").pack()
        tk.Label(popup, text=f"【{pup['role']}】", font=("微软雅黑", 14),
                bg=pup["color"], fg="white").pack()
        
        # 介绍语
        tk.Label(popup, text=pup["intro"], font=("微软雅黑", 13),
                bg=pup["color"], fg="white", wraplength=350).pack(pady=15)
        
        # 播放介绍语音
        self.speak(pup["intro"])
        
        # 开始按钮
        def start_game():
            popup.destroy()
            callback()
        
        tk.Button(popup, text="🚀 出发！", font=("微软雅黑", 14, "bold"),
                 bg="white", fg=pup["color"], width=12, height=1,
                 cursor="hand2", command=start_game).pack(pady=10)
        
        # 3秒后自动开始
        popup.after(4000, start_game)
    
    def show_pup_feedback(self, is_correct, custom_msg=None):
        """显示狗狗反馈（正确/错误）- 带动画特效"""
        pup_id = self.current_pup
        if not pup_id or pup_id not in self.PAW_PATROL_GAMES:
            # 默认反馈
            if is_correct:
                self.speak_praise()
                self.play_correct_animation()
            else:
                self.speak_encourage()
            return
        
        pup = self.PAW_PATROL_GAMES[pup_id]
        
        if is_correct:
            msg = custom_msg or pup["praise"]
            self.speak_praise()
            self.play_correct_animation(pup_id)
        else:
            msg = custom_msg or f"{pup['name']}说：没关系，再试一次！"
            self.speak_encourage()
    
    def play_correct_animation(self, pup_id=None):
        """播放答对动画 - 星星特效 + 狗狗跳跃"""
        # 创建动画覆盖层
        try:
            anim_window = tk.Toplevel(self.window)
            anim_window.overrideredirect(True)
            anim_window.attributes('-topmost', True)
            anim_window.attributes('-transparentcolor', 'gray15')
            
            # 获取主窗口位置
            x = self.window.winfo_rootx()
            y = self.window.winfo_rooty()
            w = self.window.winfo_width()
            h = self.window.winfo_height()
            anim_window.geometry(f"{w}x{h}+{x}+{y}")
            
            canvas = tk.Canvas(anim_window, width=w, height=h, bg='gray15', highlightthickness=0)
            canvas.pack()
            
            # 存储动画元素
            stars = []
            hearts = []
            
            # 生成星星
            for _ in range(15):
                sx = random.randint(50, w-50)
                sy = random.randint(50, h-50)
                size = random.randint(20, 40)
                color = random.choice(["#FFD700", "#FFA500", "#FF69B4", "#00CED1", "#98FB98"])
                star_id = self.draw_animated_star(canvas, sx, sy, size, color)
                stars.append({"id": star_id, "x": sx, "y": sy, "vy": random.uniform(-3, -1), "size": size})
            
            # 生成爱心
            for _ in range(8):
                hx = random.randint(100, w-100)
                hy = random.randint(h//2, h-50)
                heart_id = canvas.create_text(hx, hy, text="❤️", font=("Segoe UI Emoji", random.randint(20, 35)))
                hearts.append({"id": heart_id, "x": hx, "y": hy, "vy": random.uniform(-4, -2)})
            
            # 中央显示狗狗跳跃
            pup_canvas_size = 150
            pup_y_base = h // 2
            pup_items = []
            
            if pup_id and THEME_AVAILABLE:
                draw_func = self.get_pup_draw_func(pup_id)
                if draw_func:
                    # 画狗狗
                    draw_func(canvas, w//2, pup_y_base, 1.5)
            
            # "太棒了"文字
            text_id = canvas.create_text(w//2, h//3, text="⭐ 太棒了！⭐", 
                                        font=("微软雅黑", 36, "bold"), fill="#FFD700")
            
            # 动画帧计数
            frame = [0]
            max_frames = 30
            
            def animate():
                if frame[0] >= max_frames:
                    anim_window.destroy()
                    return
                
                frame[0] += 1
                
                # 星星上升并消失
                for star in stars:
                    star["y"] += star["vy"]
                    star["vy"] -= 0.1  # 减速
                    canvas.move(star["id"], 0, star["vy"])
                    # 淡出效果（通过缩小）
                    if frame[0] > 20:
                        canvas.delete(star["id"])
                
                # 爱心上升
                for heart in hearts:
                    heart["y"] += heart["vy"]
                    canvas.move(heart["id"], random.uniform(-1, 1), heart["vy"])
                
                # 文字跳动
                if frame[0] % 4 < 2:
                    canvas.move(text_id, 0, -3)
                else:
                    canvas.move(text_id, 0, 3)
                
                anim_window.after(50, animate)
            
            animate()
            
            # 2秒后自动关闭
            anim_window.after(1500, lambda: anim_window.destroy() if anim_window.winfo_exists() else None)
            
        except Exception as e:
            print(f"动画错误: {e}")
    
    def draw_animated_star(self, canvas, x, y, size, color):
        """绘制动画星星"""
        points = []
        for i in range(5):
            # 外点
            angle = math.radians(90 + i * 72)
            points.extend([x + size * math.cos(angle), y - size * math.sin(angle)])
            # 内点
            angle = math.radians(90 + i * 72 + 36)
            points.extend([x + size * 0.4 * math.cos(angle), y - size * 0.4 * math.sin(angle)])
        
        return canvas.create_polygon(points, fill=color, outline="#FFA000", width=2)
    
    def show_game_complete(self, score, extra_msg=""):
        """显示游戏完成界面 - 汪汪队主题（带庆祝动画）"""
        pup_id = self.current_pup
        if not pup_id or pup_id not in self.PAW_PATROL_GAMES:
            pup_id = "chase"
        pup = self.PAW_PATROL_GAMES[pup_id]
        
        # 先播放庆祝动画
        self.play_celebration_animation(pup_id)
        
        # 创建庆祝弹窗
        popup = tk.Toplevel(self.window)
        popup.title("任务完成！")
        popup.geometry("420x400")
        popup.configure(bg=pup["color"])
        popup.transient(self.window)
        popup.grab_set()
        
        # 居中显示
        popup.update_idletasks()
        x = self.window.winfo_x() + (self.window.winfo_width() - 420) // 2
        y = self.window.winfo_y() + (self.window.winfo_height() - 400) // 2
        popup.geometry(f"+{x}+{y}")
        
        # 标题
        tk.Label(popup, text="🎉 任务完成！🎉", font=("微软雅黑", 22, "bold"),
                bg=pup["color"], fg="white").pack(pady=10)
        
        # 狗狗头像（带跳跃动画）
        avatar_canvas = tk.Canvas(popup, width=140, height=140, bg=pup["color"], highlightthickness=0)
        avatar_canvas.pack(pady=5)
        
        # 绘制狗狗
        draw_func = self.get_pup_draw_func(pup_id)
        pup_y = [80]  # 用列表以便在闭包中修改
        
        def draw_pup():
            avatar_canvas.delete("pup")
            if draw_func:
                draw_func(avatar_canvas, 70, pup_y[0], 1.0)
        
        draw_pup()
        
        # 狗狗跳跃动画
        jump_frame = [0]
        def pup_jump():
            if not popup.winfo_exists():
                return
            jump_frame[0] += 1
            # 简单的上下跳跃
            if jump_frame[0] % 10 < 5:
                pup_y[0] = 75
            else:
                pup_y[0] = 85
            draw_pup()
            if jump_frame[0] < 30:
                popup.after(100, pup_jump)
        
        pup_jump()
        
        # 狗狗说话
        tk.Label(popup, text=f"{pup['name']}说：", font=("微软雅黑", 14),
                bg=pup["color"], fg="white").pack()
        tk.Label(popup, text=pup["praise"], font=("微软雅黑", 16, "bold"),
                bg=pup["color"], fg="#FFD700", wraplength=380).pack(pady=5)
        
        # 得分（带星星）
        score_frame = tk.Frame(popup, bg=pup["color"])
        score_frame.pack(pady=5)
        tk.Label(score_frame, text="⭐", font=("Segoe UI Emoji", 24),
                bg=pup["color"]).pack(side=tk.LEFT)
        tk.Label(score_frame, text=f" 得分: {score} ", font=("微软雅黑", 22, "bold"),
                bg=pup["color"], fg="white").pack(side=tk.LEFT)
        tk.Label(score_frame, text="⭐", font=("Segoe UI Emoji", 24),
                bg=pup["color"]).pack(side=tk.LEFT)
        
        if extra_msg:
            tk.Label(popup, text=extra_msg, font=("微软雅黑", 12),
                    bg=pup["color"], fg="white").pack(pady=3)
        
        # 播放语音
        self.speak(f"{pup['name']}说：{pup['praise']}你得了{score}分！")
        
        # 返回按钮
        def go_back():
            popup.destroy()
            self.create_main_menu()
        
        tk.Button(popup, text="🏠 返回主菜单", font=("微软雅黑", 12, "bold"),
                 bg="white", fg=pup["color"], width=14,
                 cursor="hand2", command=go_back).pack(pady=15)
        
        # 6秒后自动返回
        popup.after(6000, go_back)
    
    def play_celebration_animation(self, pup_id=None):
        """播放庆祝动画 - 烟花效果"""
        try:
            # 在主画布上播放简单的庆祝效果
            if hasattr(self, 'game_frame') and self.game_frame:
                for child in self.game_frame.winfo_children():
                    if isinstance(child, tk.Canvas):
                        canvas = child
                        cw = canvas.winfo_width()
                        ch = canvas.winfo_height()
                        
                        # 添加庆祝文字和星星
                        items = []
                        items.append(canvas.create_text(cw//2, ch//2, text="🎉 太棒了！🎉", 
                                    font=("微软雅黑", 32, "bold"), fill="#FFD700", tags="celebration"))
                        
                        # 周围添加星星
                        for _ in range(10):
                            sx = random.randint(50, cw-50)
                            sy = random.randint(50, ch-50)
                            star = canvas.create_text(sx, sy, text="⭐", 
                                    font=("Segoe UI Emoji", random.randint(20, 40)), tags="celebration")
                            items.append(star)
                        
                        # 1.5秒后清除
                        def clear_celebration():
                            canvas.delete("celebration")
                        canvas.after(1500, clear_celebration)
                        break
        except Exception as e:
            print(f"庆祝动画错误: {e}")
    
    # =====================================================
    # 主菜单 - 汪汪队主题版（年龄分级优化）
    # =====================================================
    def create_main_menu(self):
        self.game_running = False
        self.init_achievements()
        self.current_pup = None
        
        for widget in self.window.winfo_children():
            widget.destroy()
        self.window.configure(bg=self.bg_color)
        
        main_frame = tk.Frame(self.window, bg=self.bg_color)
        main_frame.pack(fill=tk.BOTH, expand=True, padx=15, pady=8)
        
        # 顶部栏：标题和成就按钮
        top_frame = tk.Frame(main_frame, bg=self.bg_color)
        top_frame.pack(fill=tk.X, pady=3)
        
        # 汪汪队标题
        title_frame = tk.Frame(top_frame, bg="#1976D2", relief=tk.RAISED, bd=3)
        title_frame.pack(side=tk.LEFT, padx=10)
        tk.Label(title_frame, text="🐾 汪汪队交通乐园 🐾", 
                 font=("微软雅黑", 26, "bold"), bg="#1976D2", fg="white",
                 padx=15, pady=5).pack()
        
        # 成就按钮
        unlocked = sum(1 for a in self.achievements.values() if a["unlocked"])
        tk.Button(top_frame, text=f"🏆 成就 {unlocked}/{len(self.achievements)}", 
                 font=("微软雅黑", 11, "bold"), bg="#FFD700", fg="#8B4513",
                 cursor="hand2", command=self.show_achievements).pack(side=tk.RIGHT, padx=10)
        
        # 分数显示
        score_frame = tk.Frame(top_frame, bg="#FFD700", relief=tk.RAISED, bd=2)
        score_frame.pack(side=tk.RIGHT, padx=5)
        tk.Label(score_frame, text=f"⭐ {self.score}", 
                 font=("微软雅黑", 12, "bold"), bg="#FFD700", fg="#8B4513",
                 padx=10, pady=3).pack()
        
        # 瞭望塔预览画布
        tower_canvas = tk.Canvas(main_frame, width=900, height=80, bg="#87CEEB", 
                                highlightthickness=2, highlightbackground="#1976D2")
        tower_canvas.pack(pady=5)
        
        # 画天空和草地
        tower_canvas.create_rectangle(0, 60, 900, 80, fill="#228B22", outline="")
        
        # 画瞭望塔（简化版）
        if THEME_AVAILABLE:
            ThemeDrawings.draw_lookout_tower(tower_canvas, 450, 45, 0.5)
        else:
            tower_canvas.create_polygon(420, 70, 450, 10, 480, 70, fill="#1976D2", outline="#0D47A1", width=2)
            tower_canvas.create_oval(430, 15, 470, 40, fill="#FFD700", outline="#FFA000", width=2)
        
        # 画几只狗狗在塔周围
        if THEME_AVAILABLE:
            ThemeDrawings.draw_puppy_chase(tower_canvas, 150, 48, 0.35)
            ThemeDrawings.draw_puppy_marshall(tower_canvas, 250, 48, 0.35)
            ThemeDrawings.draw_puppy_skye(tower_canvas, 650, 48, 0.35)
            ThemeDrawings.draw_puppy_rubble(tower_canvas, 750, 48, 0.35)
        
        # ========== 简单游戏区（适合3岁+）==========
        easy_section = tk.LabelFrame(main_frame, text="🌟 简单游戏（3岁+）", 
                                     font=("微软雅黑", 14, "bold"), bg="#E8F5E9", 
                                     fg="#2E7D32", relief=tk.GROOVE, bd=3)
        easy_section.pack(fill=tk.X, pady=8, padx=5)
        
        easy_games_frame = tk.Frame(easy_section, bg="#E8F5E9")
        easy_games_frame.pack(pady=8)
        
        # 简单游戏：涂色、认知、红绿灯、拼图
        easy_games = [
            ("liberty", self.start_traffic_quiz, "认交通工具"),
            ("everest", self.start_traffic_light_game, "红绿灯"),
            ("rex", self.start_vehicle_puzzle, "拼图"),
            (None, self.start_coloring_game, "涂色乐园"),  # 特殊：涂色游戏
        ]
        
        for i, (pup_id, game_func, game_name) in enumerate(easy_games):
            if pup_id:
                pup = self.PAW_PATROL_GAMES[pup_id]
                color = pup["color"]
                name = pup["name"]
                icon = pup["icon"]
            else:
                color = "#FFD93D"
                name = "涂色"
                icon = "🎨"
            
            # 创建大卡片（更容易点击）
            card = tk.Frame(easy_games_frame, bg=color, relief=tk.RAISED, bd=4)
            card.grid(row=0, column=i, padx=12, pady=5)
            
            # 狗狗头像画布（更大）
            avatar_canvas = tk.Canvas(card, width=100, height=100, bg=color, highlightthickness=0)
            avatar_canvas.pack(pady=5)
            
            if pup_id:
                draw_func = self.get_pup_draw_func(pup_id)
                if draw_func:
                    draw_func(avatar_canvas, 50, 55, 0.7)
            else:
                avatar_canvas.create_text(50, 50, text="🎨", font=("Segoe UI Emoji", 40))
            
            # 狗狗名字
            tk.Label(card, text=name, font=("微软雅黑", 13, "bold"),
                    bg=color, fg="white").pack()
            
            # 游戏按钮（更大）
            def make_callback(pid, func):
                if pid:
                    return lambda: self.show_pup_intro(pid, func)
                else:
                    return func
            
            btn = tk.Button(card, text=f"{icon} {game_name}", 
                           font=("微软雅黑", 12, "bold"),
                           bg="white", fg=color, width=12, height=2,
                           cursor="hand2", command=make_callback(pup_id, game_func))
            btn.pack(pady=8, padx=8)
        
        # ========== 进阶游戏区（适合4岁+）==========
        advanced_section = tk.LabelFrame(main_frame, text="🚀 进阶游戏（4岁+）", 
                                         font=("微软雅黑", 14, "bold"), bg="#E3F2FD", 
                                         fg="#1565C0", relief=tk.GROOVE, bd=3)
        advanced_section.pack(fill=tk.X, pady=8, padx=5)
        
        advanced_games_frame = tk.Frame(advanced_section, bg="#E3F2FD")
        advanced_games_frame.pack(pady=8)
        
        # 进阶游戏：挖掘机、赛车、飞机、消防车、火箭、火车、停车场
        advanced_games = [
            ("rubble", self.start_excavator_game),
            ("chase", self.start_racing_game),
            ("skye", self.start_airplane_game),
            ("marshall", self.start_firetruck_game),
            ("rocky", self.start_rocket_game),
            ("zuma", self.start_train_game),
            ("tracker", self.start_parking_game),
        ]
        
        for i, (pup_id, game_func) in enumerate(advanced_games):
            pup = self.PAW_PATROL_GAMES[pup_id]
            col = i % 7
            
            # 创建狗狗卡片
            card = tk.Frame(advanced_games_frame, bg=pup["color"], relief=tk.RAISED, bd=3)
            card.grid(row=0, column=col, padx=5, pady=5)
            
            # 狗狗头像画布
            avatar_canvas = tk.Canvas(card, width=70, height=70, bg=pup["color"], highlightthickness=0)
            avatar_canvas.pack(pady=3)
            
            draw_func = self.get_pup_draw_func(pup_id)
            if draw_func:
                draw_func(avatar_canvas, 35, 40, 0.5)
            
            # 狗狗名字
            tk.Label(card, text=pup["name"], font=("微软雅黑", 10, "bold"),
                    bg=pup["color"], fg="white").pack()
            
            # 游戏按钮
            def make_callback(pid, func):
                return lambda: self.show_pup_intro(pid, func)
            
            btn = tk.Button(card, text=f"{pup['icon']} {pup['game']}", 
                           font=("微软雅黑", 9, "bold"),
                           bg="white", fg=pup["color"], width=8,
                           cursor="hand2", command=make_callback(pup_id, game_func))
            btn.pack(pady=4, padx=4)
        
        # 底部按钮行
        bottom_frame = tk.Frame(main_frame, bg=self.bg_color)
        bottom_frame.pack(pady=8)
        
        # 成就
        tk.Button(bottom_frame, text="🏆 我的成就", font=("微软雅黑", 11, "bold"),
                 bg="#9C27B0", fg="white", width=12, cursor="hand2",
                 command=self.show_achievements).pack(side=tk.LEFT, padx=10)
        
        # 退出
        tk.Button(bottom_frame, text="👋 退出", font=("微软雅黑", 11, "bold"),
                 bg="#FF6B6B", fg="white", width=10, cursor="hand2",
                 command=self.window.quit).pack(side=tk.LEFT, padx=10)
        
        self.speak("汪汪队，准备出动！选择一位狗狗队员开始冒险吧！")

    def clear_game_area(self, bg_color="#87CEEB"):
        self.game_running = False
        for widget in self.window.winfo_children():
            widget.destroy()
        self.window.configure(bg=bg_color)
        
        nav_frame = tk.Frame(self.window, bg=bg_color)
        nav_frame.pack(fill=tk.X, pady=5)
        
        tk.Button(nav_frame, text="🏠 返回", font=("微软雅黑", 11),
                  bg="#96CEB4", fg="white", relief=tk.RAISED, bd=3,
                  cursor="hand2", command=self.create_main_menu).pack(side=tk.LEFT, padx=10)
        
        # 显示当前狗狗助手
        if self.current_pup and self.current_pup in self.PAW_PATROL_GAMES:
            pup = self.PAW_PATROL_GAMES[self.current_pup]
            pup_frame = tk.Frame(nav_frame, bg=pup["color"], relief=tk.RAISED, bd=2)
            pup_frame.pack(side=tk.LEFT, padx=10)
            
            # 小头像
            pup_canvas = tk.Canvas(pup_frame, width=35, height=35, bg=pup["color"], highlightthickness=0)
            pup_canvas.pack(side=tk.LEFT, padx=2)
            draw_func = self.get_pup_draw_func(self.current_pup)
            if draw_func:
                draw_func(pup_canvas, 17, 20, 0.25)
            
            tk.Label(pup_frame, text=f"{pup['name']}助阵", font=("微软雅黑", 10, "bold"),
                    bg=pup["color"], fg="white", padx=5).pack(side=tk.LEFT)
        
        self.score_label = tk.Label(nav_frame, text=f"⭐ 得分: 0",
                 font=("微软雅黑", 12, "bold"), bg=bg_color, fg="#1976D2")
        self.score_label.pack(side=tk.RIGHT, padx=10)
        
        self.game_frame = tk.Frame(self.window, bg=bg_color)
        self.game_frame.pack(fill=tk.BOTH, expand=True, padx=10, pady=5)


    # =====================================================
    # 游戏1: 挖掘机挖宝藏 (完全重写)
    # =====================================================
    def start_excavator_game(self):
        self.clear_game_area("#DEB887")
        self.exc_score = 0
        self.exc_arm_angle = -20  # 初始角度向下，方便挖土
        self.game_running = True
        
        # 获取当前狗狗信息
        pup = self.PAW_PATROL_GAMES.get("rubble", {})
        
        tk.Label(self.game_frame, text=f"🏗️ {pup.get('name', '小砾')}的挖掘机", font=("微软雅黑", 24, "bold"),
                 bg="#DEB887", fg="#8B4513").pack(pady=5)
        
        tk.Label(self.game_frame, text="← → 移动挖掘机 | ↑ ↓ 控制铲斗 | 空格键 挖土",
                 font=("微软雅黑", 12), bg="#DEB887", fg="#666").pack()
        
        # 游戏画布
        self.exc_canvas = tk.Canvas(self.game_frame, bg="#87CEEB", highlightthickness=2)
        self.exc_canvas.pack(pady=10, fill=tk.BOTH, expand=True)
        self.window.update()
        
        # 绑定键盘
        self.window.bind("<Left>", self.exc_move_left)
        self.window.bind("<Right>", self.exc_move_right)
        self.window.bind("<Up>", self.exc_arm_up)
        self.window.bind("<Down>", self.exc_arm_down)
        self.window.bind("<space>", self.exc_dig)
        
        self.exc_init_scene()
        self.speak(f"{pup.get('name', '小砾')}说：挖掘机准备好了！移动到红旗位置，按空格键挖宝藏！")
    
    def exc_init_scene(self):
        """初始化场景并生成宝藏"""
        self.exc_canvas.update()
        self.cw = self.exc_canvas.winfo_width()
        self.ch = self.exc_canvas.winfo_height()
        if self.cw < 100:
            self.cw = 900
            self.ch = 550
        
        # 关键位置
        self.ground_y = int(self.ch * 0.55)  # 地面位置（挖掘机站的地方）
        self.soil_top = int(self.ch * 0.58)  # 土壤顶部
        
        # 挖掘机初始位置（画布中间偏左）
        self.exc_x = int(self.cw * 0.15)
        
        # 生成宝藏 - 均匀分布在可到达的位置
        self.exc_treasures = []
        self.exc_dug_spots = set()  # 已挖过的位置（用于显示坑）
        
        treasures = ["💎", "⭐", "🪙", "👑", "💰", "🎁"]
        treasure_values = {"💎": 30, "⭐": 20, "🪙": 10, "👑": 50, "💰": 25, "🎁": 40}
        
        # 将地面分成6个区域，每个区域放1个宝藏，确保分布均匀且可到达
        num_treasures = 6
        section_width = (self.cw - 100) // num_treasures
        
        for i in range(num_treasures):
            # 每个区域的x范围
            min_x = 50 + i * section_width + 30
            max_x = 50 + (i + 1) * section_width - 30
            tx = random.randint(min_x, max_x)
            
            t_type = random.choice(treasures)
            t_value = treasure_values[t_type]
            
            self.exc_treasures.append({
                "x": tx,
                "type": t_type,
                "value": t_value,
                "found": False
            })
        
        # 固定云朵位置（避免每次重绘时随机变化）
        self.cloud_positions = []
        for cx_ratio in [0.12, 0.35, 0.65]:
            cx = int(self.cw * cx_ratio)
            cy = random.randint(50, 80)
            self.cloud_positions.append((cx, cy))
        
        self.exc_redraw_scene()
    
    def exc_redraw_scene(self):
        """重绘整个场景"""
        self.exc_canvas.delete("all")
        cw, ch = self.cw, self.ch
        
        # 天空（渐变蓝色）
        for i in range(0, int(ch * 0.4), 5):
            r = min(255, 135 + i // 4)
            g = min(255, 206 + i // 8)
            color = f"#{r:02x}{g:02x}{235:02x}"
            self.exc_canvas.create_rectangle(0, i, cw, i+5, fill=color, outline="")
        
        # 太阳
        sun_x = int(cw * 0.85)
        self.exc_canvas.create_oval(sun_x, 30, sun_x+70, 100, fill="#FFD700", outline="#FFA500", width=3)
        
        # 云朵（使用固定位置）
        for cx, cy in self.cloud_positions:
            for dx, dy in [(-20, 0), (0, -10), (20, 0), (0, 10)]:
                self.exc_canvas.create_oval(cx+dx-25, cy+dy-15, cx+dx+25, cy+dy+15, fill="white", outline="")
        
        # 草地
        self.exc_canvas.create_rectangle(0, self.ground_y, cw, self.soil_top, fill="#228B22", outline="")
        
        # 土壤
        self.exc_canvas.create_rectangle(0, self.soil_top, cw, ch, fill="#8B4513", outline="")
        
        # 画已挖的坑（深色土壤）
        for spot_x in self.exc_dug_spots:
            self.exc_canvas.create_oval(
                spot_x - 35, self.soil_top + 5,
                spot_x + 35, self.soil_top + 50,
                fill="#654321", outline="#543210", width=2
            )
        
        # 画宝藏标记和已找到的宝藏
        for t in self.exc_treasures:
            if t["found"]:
                # 已找到的宝藏显示在地面上
                self.exc_canvas.create_text(t["x"], self.ground_y - 40, text=t["type"], 
                                            font=("Segoe UI Emoji", 32))
            else:
                # 未找到的宝藏显示标记（宝藏就在标记正下方）
                marker_x = t["x"]
                # 画一个小旗子标记
                self.exc_canvas.create_line(marker_x, self.soil_top, marker_x, self.soil_top - 30,
                                            fill="#8B0000", width=3)
                self.exc_canvas.create_polygon(
                    marker_x, self.soil_top - 30,
                    marker_x + 20, self.soil_top - 25,
                    marker_x, self.soil_top - 20,
                    fill="#FF0000", outline="#8B0000"
                )
                # 宝藏图标（半透明提示）
                self.exc_canvas.create_text(marker_x, self.soil_top + 35, text=t["type"], 
                                            font=("Segoe UI Emoji", 20), fill="#A0522D")
        
        # 显示进度
        found = sum(1 for t in self.exc_treasures if t["found"])
        total = len(self.exc_treasures)
        self.exc_canvas.create_text(cw - 60, 30, text=f"💎 {found}/{total}", 
                                    font=("微软雅黑", 16, "bold"), fill="#FFD700")
        
        # 画挖掘机
        bucket_pos = self.draw_excavator(self.exc_canvas, self.exc_x, self.ground_y, 1.0, self.exc_arm_angle)
        self.bucket_x, self.bucket_y = bucket_pos
    
    def exc_draw(self):
        """更新场景"""
        self.exc_redraw_scene()
    
    def exc_move_left(self, event):
        if not self.game_running:
            return
        # 允许移动到画布左边缘
        if self.exc_x > 80:
            self.exc_x -= 40
            self.exc_draw()
    
    def exc_move_right(self, event):
        if not self.game_running:
            return
        # 允许移动到画布右边缘
        if self.exc_x < self.cw - 120:
            self.exc_x += 40
            self.exc_draw()
    
    def exc_arm_up(self, event):
        if not self.game_running:
            return
        # 扩大角度范围：-60到60度
        if self.exc_arm_angle < 60:
            self.exc_arm_angle += 15
            self.exc_draw()
    
    def exc_arm_down(self, event):
        if not self.game_running:
            return
        # 扩大角度范围：允许向下伸到-60度
        if self.exc_arm_angle > -60:
            self.exc_arm_angle -= 15
            self.exc_draw()
    
    def exc_dig(self, event):
        if not self.game_running:
            return
        
        # 使用铲斗的实际位置来判断挖掘
        dig_x = self.bucket_x  # 铲斗的X坐标
        dig_y = self.bucket_y  # 铲斗的Y坐标
        
        cx = self.cw // 2
        
        # 首先检查铲斗是否挖到土里（Y坐标要接近或超过土壤顶部）
        if dig_y < self.soil_top - 20:
            # 铲斗还在空中，没挖到土
            self.exc_canvas.create_text(cx, int(self.ch * 0.25), 
                text="铲斗还在空中呢！按 ↓ 把铲斗放低一点！", 
                font=("微软雅黑", 16), fill="#FF6600", tags="hint")
            self.window.after(1500, lambda: self.exc_canvas.delete("hint"))
            return
        
        # 检查是否挖到宝藏
        found_treasure = None
        for t in self.exc_treasures:
            if not t["found"]:
                # 检查铲斗位置是否接近宝藏（水平距离60像素内）
                if abs(dig_x - t["x"]) < 60:
                    t["found"] = True
                    found_treasure = t
                    self.exc_dug_spots.add(t["x"])  # 在宝藏位置显示坑
                    break
        
        # 如果没挖到宝藏，也显示一个坑
        if not found_treasure:
            self.exc_dug_spots.add(int(dig_x))
        
        # 重绘场景
        self.exc_redraw_scene()
        
        if found_treasure:
            self.exc_score += found_treasure["value"]
            self.score += found_treasure["value"]
            self.score_label.config(text=f"⭐ 得分: {self.exc_score}")
            
            # 显示找到宝藏的提示
            self.exc_canvas.create_text(cx, int(self.ch * 0.25), 
                text=f"🎉 挖到 {found_treasure['type']} 了！+{found_treasure['value']}分！", 
                font=("微软雅黑", 22, "bold"), fill="#FFD700", tags="hint")
            self.speak_praise()
            self.window.after(2500, lambda: self.exc_canvas.delete("hint"))
            
            # 检查是否全部找到
            all_found = all(t["found"] for t in self.exc_treasures)
            if all_found:
                self.game_running = False
                self.window.after(3000, lambda: self.exc_canvas.create_text(cx, int(self.ch * 0.4), 
                    text=f"🏆 太棒了！找到所有宝藏！\n总分：{self.exc_score}分！", 
                    font=("微软雅黑", 28, "bold"), fill="#32CD32"))
                self.speak(f"太棒了！乐乐找到了所有宝藏！得了{self.exc_score}分！")
                self.window.after(6000, self.create_main_menu)
        else:
            # 没挖到宝藏
            self.exc_canvas.create_text(cx, int(self.ch * 0.25), 
                text="咚！这里没有宝藏，看看红旗在哪里！", 
                font=("微软雅黑", 16), fill="#8B4513", tags="hint")
            self.window.after(1500, lambda: self.exc_canvas.delete("hint"))

    # =====================================================
    # 游戏2: 赛车冲冲冲
    # =====================================================
    def start_racing_game(self):
        self.clear_game_area("#333333")
        self.race_score = 0
        self.race_speed = 3  # 降低初始速度，更适合小朋友
        self.race_obstacles = []
        self.race_coins = []
        self.race_distance = 0
        self.game_running = True
        
        # 获取当前狗狗信息
        pup = self.PAW_PATROL_GAMES.get("chase", {})
        
        tk.Label(self.game_frame, text=f"🏎️ {pup.get('name', '阿奇')}的赛车", font=("微软雅黑", 24, "bold"),
                 bg="#333333", fg="#FF0000").pack(pady=3)
        
        tk.Label(self.game_frame, text="用左右方向键躲避障碍物，吃金币加分！",
                 font=("微软雅黑", 12), bg="#333333", fg="#AAA").pack()
        
        # 游戏画布 - 自适应窗口大小
        self.race_canvas = tk.Canvas(self.game_frame, bg="#333333", highlightthickness=2)
        self.race_canvas.pack(pady=5, fill=tk.BOTH, expand=True)
        self.window.update()
        
        # 获取画布尺寸
        self.race_cw = self.race_canvas.winfo_width()
        self.race_ch = self.race_canvas.winfo_height()
        if self.race_cw < 100:
            self.race_cw = 900
            self.race_ch = 600
        
        # 初始化赛车位置
        self.race_x = self.race_cw // 2
        self.race_y = int(self.race_ch * 0.83)
        
        # 计算赛道边界
        self.race_left = int(self.race_cw * 0.11)
        self.race_right = int(self.race_cw * 0.89)
        
        # 绑定键盘
        self.window.bind("<Left>", self.race_move_left)
        self.window.bind("<Right>", self.race_move_right)
        
        self.speak(f"{pup.get('name', '阿奇')}说：赛车比赛开始！躲避障碍物，吃金币加分！")
        self.race_game_loop()
    
    def race_move_left(self, event):
        if self.game_running and self.race_x > self.race_left + 80:
            self.race_x -= 40
    
    def race_move_right(self, event):
        if self.game_running and self.race_x < self.race_right - 80:
            self.race_x += 40
    
    def race_game_loop(self):
        if not self.game_running:
            return
        
        self.race_canvas.delete("all")
        # 动态获取画布尺寸（支持窗口最大化）
        cw = self.race_canvas.winfo_width()
        ch = self.race_canvas.winfo_height()
        if cw < 100:
            cw, ch = 900, 550
        
        # 如果画布尺寸变化，调整赛车位置
        if hasattr(self, 'race_cw') and self.race_cw > 0 and self.race_cw != cw:
            ratio = (self.race_x - self.race_left) / (self.race_right - self.race_left) if self.race_right > self.race_left else 0.5
            # 先更新边界
            new_left = int(cw * 0.22)
            new_right = int(cw * 0.78)
            self.race_x = int(new_left + ratio * (new_right - new_left))
        
        self.race_cw, self.race_ch = cw, ch
        # 重新计算赛道边界
        self.race_left = int(cw * 0.22)
        self.race_right = int(cw * 0.78)
        self.race_y = int(ch * 0.82)
        
        # 确保赛车在赛道内
        self.race_x = max(self.race_left + 50, min(self.race_x, self.race_right - 50))
        
        # 画赛道
        self.race_canvas.create_rectangle(self.race_left, 0, self.race_right, ch, fill="#444444", outline="")
        # 赛道边线
        self.race_canvas.create_rectangle(self.race_left, 0, self.race_left+10, ch, fill="#FFFF00", outline="")
        self.race_canvas.create_rectangle(self.race_right-10, 0, self.race_right, ch, fill="#FFFF00", outline="")
        # 中线（虚线效果）
        cx = cw // 2
        for i in range(0, ch, 60):
            y = (i + self.race_distance * 3) % ch
            self.race_canvas.create_rectangle(cx-5, y, cx+5, y+30, fill="white", outline="")
        
        # 计算车道位置
        lane_width = (self.race_right - self.race_left) // 5
        lanes = [self.race_left + lane_width * (i + 1) for i in range(4)]
        
        # 生成障碍物
        if random.random() < 0.015:  # 降低障碍物频率
            ox = random.choice(lanes)
            self.race_obstacles.append({"x": ox, "y": -50})
        
        # 生成金币
        if random.random() < 0.10:  # 增加金币频率，让小朋友更有成就感
            coin_x = random.choice(lanes)
            self.race_coins.append({"x": coin_x, "y": -30})
        
        # 更新障碍物
        new_obstacles = []
        for obs in self.race_obstacles:
            obs["y"] += self.race_speed + 3
            if obs["y"] < ch + 50:
                new_obstacles.append(obs)
                # 画障碍物（路障）
                self.race_canvas.create_rectangle(obs["x"]-30, obs["y"]-20, obs["x"]+30, obs["y"]+20, 
                                                  fill="#FF6600", outline="#CC5500", width=2)
                self.race_canvas.create_line(obs["x"]-25, obs["y"]-15, obs["x"]+25, obs["y"]+15, fill="white", width=3)
                self.race_canvas.create_line(obs["x"]-25, obs["y"]+15, obs["x"]+25, obs["y"]-15, fill="white", width=3)
        self.race_obstacles = new_obstacles
        
        # 更新金币
        new_coins = []
        for coin in self.race_coins:
            coin["y"] += self.race_speed + 2
            if coin["y"] < ch + 50:
                new_coins.append(coin)
                # 画金币
                self.race_canvas.create_oval(coin["x"]-15, coin["y"]-15, coin["x"]+15, coin["y"]+15, 
                                             fill="#FFD700", outline="#FFA500", width=2)
                self.race_canvas.create_text(coin["x"], coin["y"], text="$", font=("Arial", 12, "bold"), fill="#8B4513")
        self.race_coins = new_coins
        
        # 画赛车（车头朝上）
        self.draw_race_car_up(self.race_canvas, self.race_x, self.race_y, 1.0, "#FF0000")
        
        # 碰撞检测 - 障碍物
        for obs in self.race_obstacles:
            if abs(obs["x"] - self.race_x) < 35 and abs(obs["y"] - self.race_y) < 30:  # 更宽松的碰撞检测
                self.game_running = False
                self.race_canvas.create_text(cx, ch//2, text="💥 撞车了！", 
                                             font=("微软雅黑", 40, "bold"), fill="#FF0000")
                # 使用汪汪队风格的结束
                pup = self.PAW_PATROL_GAMES.get("chase", {})
                self.speak(f"阿奇说：没关系！你跑了{self.race_distance}米，得了{self.race_score}分！下次更小心！")
                self.window.after(3000, self.create_main_menu)
                return
        
        # 碰撞检测 - 金币
        for coin in self.race_coins[:]:
            if abs(coin["x"] - self.race_x) < 40 and abs(coin["y"] - self.race_y) < 40:
                self.race_coins.remove(coin)
                self.race_score += 10
                self.score += 10
                self.score_label.config(text=f"⭐ 得分: {self.race_score}")
        
        # 距离和速度
        self.race_distance += 1
        if self.race_distance % 400 == 0:  # 速度增长更慢
            self.race_speed = min(self.race_speed + 1, 8)  # 最高速度降低
        
        # 显示距离
        self.race_canvas.create_text(cx, 30, text=f"距离: {self.race_distance}m  速度: {self.race_speed}", 
                                     font=("微软雅黑", 14), fill="white")
        
        self.window.after(50, self.race_game_loop)


    # =====================================================
    # 游戏3: 飞机大冒险
    # =====================================================
    def start_airplane_game(self):
        self.clear_game_area("#87CEEB")
        self.plane_score = 0
        self.plane_clouds = []
        self.plane_stars = []
        self.plane_birds = []
        self.plane_distance = 0
        self.game_running = True
        
        # 获取当前狗狗信息
        pup = self.PAW_PATROL_GAMES.get("skye", {})
        
        tk.Label(self.game_frame, text=f"✈️ {pup.get('name', '天天')}的飞机", font=("微软雅黑", 24, "bold"),
                 bg="#87CEEB", fg="#1E3A8A").pack(pady=3)
        
        tk.Label(self.game_frame, text="用上下方向键控制飞机，收集星星，躲避小鸟！",
                 font=("微软雅黑", 12), bg="#87CEEB", fg="#555").pack()
        
        # 游戏画布 - 自适应窗口大小
        self.plane_canvas = tk.Canvas(self.game_frame, bg="#87CEEB", highlightthickness=2)
        self.plane_canvas.pack(pady=5, fill=tk.BOTH, expand=True)
        self.window.update()
        
        # 获取画布尺寸
        self.plane_cw = self.plane_canvas.winfo_width()
        self.plane_ch = self.plane_canvas.winfo_height()
        if self.plane_cw < 100:
            self.plane_cw = 900
            self.plane_ch = 600
        
        # 初始化飞机位置
        self.plane_x = int(self.plane_cw * 0.17)
        self.plane_y = self.plane_ch // 2
        
        # 绑定键盘
        self.window.bind("<Up>", self.plane_move_up)
        self.window.bind("<Down>", self.plane_move_down)
        
        self.speak(f"{pup.get('name', '天天')}说：飞机起飞！收集星星，小心小鸟！")
        self.plane_game_loop()
    
    def plane_move_up(self, event):
        if self.game_running and self.plane_y > 80:
            self.plane_y -= 40
    
    def plane_move_down(self, event):
        if self.game_running and self.plane_y < self.plane_ch - 80:
            self.plane_y += 40
    
    def plane_game_loop(self):
        if not self.game_running:
            return
        
        self.plane_canvas.delete("all")
        # 动态获取画布尺寸（支持窗口最大化）
        cw = self.plane_canvas.winfo_width()
        ch = self.plane_canvas.winfo_height()
        if cw < 100:
            cw, ch = 900, 550
        
        # 如果画布尺寸变化，调整飞机位置
        if hasattr(self, 'plane_cw') and self.plane_cw > 0 and self.plane_ch > 0:
            self.plane_x = int(self.plane_x * cw / self.plane_cw)
            self.plane_y = int(self.plane_y * ch / self.plane_ch)
        
        self.plane_cw, self.plane_ch = cw, ch
        
        # 确保飞机在有效范围内
        self.plane_x = max(80, min(self.plane_x, cw - 80))
        self.plane_y = max(80, min(self.plane_y, ch - 80))
        
        # 天空渐变背景（优化：使用条带而非逐行）
        for i in range(0, ch, 10):
            r = max(50, 135 - i // 10)
            g = max(100, 206 - i // 15)
            b = 235
            color = f"#{r:02x}{g:02x}{b:02x}"
            self.plane_canvas.create_rectangle(0, i, cw, i+10, fill=color, outline="")
        
        # 太阳
        sun_x = int(cw * 0.87)
        self.plane_canvas.create_oval(sun_x, 30, sun_x+80, 110, fill="#FFD700", outline="#FFA500", width=3)
        
        # 生成云朵
        if random.random() < 0.02:
            cy = random.randint(50, ch - 50)
            self.plane_clouds.append({"x": cw + 50, "y": cy})
        
        # 生成星星
        if random.random() < 0.08:  # 增加星星频率
            sy = random.randint(80, ch - 80)
            self.plane_stars.append({"x": cw + 50, "y": sy})
        
        # 生成小鸟（障碍物）
        if random.random() < 0.012:  # 降低小鸟频率
            by = random.randint(100, ch - 100)
            self.plane_birds.append({"x": cw + 50, "y": by})
        
        # 更新云朵
        new_clouds = []
        for cloud in self.plane_clouds:
            cloud["x"] -= 3
            if cloud["x"] > -100:
                new_clouds.append(cloud)
                # 画云朵
                cx, cy = cloud["x"], cloud["y"]
                for dx, dy in [(-30, 0), (0, -15), (30, 0), (0, 15), (-15, -8), (15, -8)]:
                    self.plane_canvas.create_oval(cx+dx-25, cy+dy-18, cx+dx+25, cy+dy+18, fill="white", outline="")
        self.plane_clouds = new_clouds
        
        # 更新星星
        new_stars = []
        for star in self.plane_stars:
            star["x"] -= 5
            if star["x"] > -30:
                new_stars.append(star)
                # 画星星
                sx, sy = star["x"], star["y"]
                self.plane_canvas.create_polygon(
                    sx, sy-20, sx+6, sy-6, sx+20, sy-6, sx+10, sy+4,
                    sx+14, sy+20, sx, sy+10, sx-14, sy+20, sx-10, sy+4,
                    sx-20, sy-6, sx-6, sy-6,
                    fill="#FFD700", outline="#FFA500", width=1
                )
        self.plane_stars = new_stars
        
        # 更新小鸟
        new_birds = []
        for bird in self.plane_birds:
            bird["x"] -= 4  # 小鸟飞得慢一点
            if bird["x"] > -50:
                new_birds.append(bird)
                # 画小鸟
                bx, by = bird["x"], bird["y"]
                # 身体
                self.plane_canvas.create_oval(bx-15, by-10, bx+15, by+10, fill="#8B4513", outline="#654321")
                # 翅膀
                wing_y = by - 15 + (5 if self.plane_distance % 10 < 5 else -5)
                self.plane_canvas.create_polygon(bx-5, by, bx-25, wing_y, bx+5, by, fill="#A0522D", outline="")
                # 嘴
                self.plane_canvas.create_polygon(bx+15, by, bx+25, by-3, bx+25, by+3, fill="#FFA500", outline="")
                # 眼睛
                self.plane_canvas.create_oval(bx+5, by-5, bx+10, by, fill="white", outline="")
                self.plane_canvas.create_oval(bx+6, by-4, bx+9, by-1, fill="black", outline="")
        self.plane_birds = new_birds
        
        # 画飞机
        self.draw_airplane(self.plane_canvas, self.plane_x, self.plane_y, 0.8, "#4169E1")
        
        # 碰撞检测 - 星星
        for star in self.plane_stars[:]:
            if abs(star["x"] - self.plane_x) < 50 and abs(star["y"] - self.plane_y) < 40:
                self.plane_stars.remove(star)
                self.plane_score += 15
                self.score += 15
                self.score_label.config(text=f"⭐ 得分: {self.plane_score}")
        
        # 碰撞检测 - 小鸟
        for bird in self.plane_birds:
            if abs(bird["x"] - self.plane_x) < 45 and abs(bird["y"] - self.plane_y) < 25:  # 更宽松
                self.game_running = False
                self.plane_canvas.create_text(cw//2, ch//2, text="💥 撞到小鸟了！", 
                                              font=("微软雅黑", 36, "bold"), fill="#FF0000")
                # 使用汪汪队风格的结束
                self.speak(f"天天说：没关系！你飞了{self.plane_distance}米，收集了{self.plane_score//15}颗星星！下次飞得更高！")
                self.window.after(3000, self.create_main_menu)
                return
        
        self.plane_distance += 2
        
        # 显示距离
        self.plane_canvas.create_text(cw//2, 30, text=f"飞行距离: {self.plane_distance}m", 
                                      font=("微软雅黑", 14, "bold"), fill="#1E3A8A")
        
        self.window.after(50, self.plane_game_loop)

    # =====================================================
    # 游戏4: 消防车救火
    # =====================================================
    def start_firetruck_game(self):
        self.clear_game_area("#2F4F4F")
        self.fire_score = 0
        self.fire_buildings = []
        self.fire_water = []
        self.fires_saved = 0
        self.game_running = True
        
        # 获取当前狗狗信息
        pup = self.PAW_PATROL_GAMES.get("marshall", {})
        
        tk.Label(self.game_frame, text=f"🚒 {pup.get('name', '毛毛')}的消防车", font=("微软雅黑", 24, "bold"),
                 bg="#2F4F4F", fg="#DC143C").pack(pady=3)
        
        tk.Label(self.game_frame, text="用左右方向键移动，按空格键喷水灭火！救5栋楼获胜！",
                 font=("微软雅黑", 12), bg="#2F4F4F", fg="#AAA").pack()
        
        self.fire_progress = tk.Label(self.game_frame, text="已救: 0/5 栋楼",
                                       font=("微软雅黑", 14, "bold"), bg="#2F4F4F", fg="#32CD32")
        self.fire_progress.pack()
        
        # 游戏画布 - 自适应窗口大小
        self.fire_canvas = tk.Canvas(self.game_frame, bg="#1a1a2e", highlightthickness=2)
        self.fire_canvas.pack(pady=5, fill=tk.BOTH, expand=True)
        self.window.update()
        
        # 获取画布尺寸
        self.fire_cw = self.fire_canvas.winfo_width()
        self.fire_ch = self.fire_canvas.winfo_height()
        if self.fire_cw < 100:
            self.fire_cw = 900
            self.fire_ch = 550
        
        # 初始化消防车位置
        self.fire_truck_x = int(self.fire_cw * 0.11)
        
        # 绑定键盘
        self.window.bind("<Left>", self.fire_move_left)
        self.window.bind("<Right>", self.fire_move_right)
        self.window.bind("<space>", self.fire_spray)
        
        # 初始化建筑
        self.fire_init_buildings()
        self.speak(f"{pup.get('name', '毛毛')}说：消防车出动！快去灭火救人！")
        self.fire_game_loop()
    
    def fire_init_buildings(self):
        self.fire_buildings = []
        colors = ["#8B4513", "#A0522D", "#CD853F", "#D2691E", "#B8860B"]
        spacing = self.fire_cw // 6
        for i in range(5):
            bx = spacing + i * spacing
            height = random.randint(150, 280)
            self.fire_buildings.append({
                "x": bx, "height": height, "color": random.choice(colors),
                "on_fire": True, "fire_level": 60, "saved": False  # 降低火焰等级，更容易灭火
            })
    
    def fire_move_left(self, event):
        if self.game_running and self.fire_truck_x > 80:
            self.fire_truck_x -= 30
    
    def fire_move_right(self, event):
        if self.game_running and self.fire_truck_x < self.fire_cw - 80:
            self.fire_truck_x += 30
    
    def fire_spray(self, event):
        if not self.game_running:
            return
        # 添加水柱
        ground_y = int(self.fire_ch * 0.87)
        self.fire_water.append({"x": self.fire_truck_x + 30, "y": ground_y - 20, "active": True})
    
    def fire_game_loop(self):
        if not self.game_running:
            return
        
        self.fire_canvas.delete("all")
        # 动态获取画布尺寸（支持窗口最大化）
        cw = self.fire_canvas.winfo_width()
        ch = self.fire_canvas.winfo_height()
        if cw < 100:
            cw, ch = 900, 550
        
        # 如果画布尺寸变化，调整消防车位置
        if hasattr(self, 'fire_cw') and self.fire_cw > 0:
            self.fire_truck_x = int(self.fire_truck_x * cw / self.fire_cw)
        
        self.fire_cw, self.fire_ch = cw, ch
        ground_y = int(ch * 0.87)
        
        # 确保消防车在有效范围内
        self.fire_truck_x = max(80, min(self.fire_truck_x, cw - 80))
        
        # 重新计算建筑物位置（按比例分布）
        spacing = cw // 6
        for i, b in enumerate(self.fire_buildings):
            b["x"] = spacing + i * spacing
        
        # 夜空背景
        self.fire_canvas.create_rectangle(0, 0, cw, ch, fill="#1a1a2e", outline="")
        
        # 星星
        for _ in range(20):
            sx = random.randint(0, cw)
            sy = random.randint(0, int(ch * 0.36))
            self.fire_canvas.create_oval(sx-1, sy-1, sx+1, sy+1, fill="white", outline="")
        
        # 月亮
        moon_x = int(cw * 0.89)
        self.fire_canvas.create_oval(moon_x, 30, moon_x+60, 90, fill="#FFFACD", outline="#FFE4B5", width=2)
        
        # 地面
        self.fire_canvas.create_rectangle(0, ground_y, cw, ch, fill="#333333", outline="")
        self.fire_canvas.create_rectangle(0, ground_y-5, cw, ground_y, fill="#555555", outline="")
        
        # 画建筑和火焰
        for b in self.fire_buildings:
            bx, height, color = b["x"], b["height"], b["color"]
            by = ground_y - height
            
            # 建筑主体
            self.fire_canvas.create_rectangle(bx-40, by, bx+40, ground_y, fill=color, outline="#333", width=2)
            
            # 窗户
            for wy in range(by + 30, ground_y - 15, 50):
                for wx in [bx-20, bx+10]:
                    window_color = "#FFFF00" if b["on_fire"] else "#87CEEB"
                    self.fire_canvas.create_rectangle(wx, wy, wx+15, wy+25, fill=window_color, outline="#333")
            
            # 火焰
            if b["on_fire"] and b["fire_level"] > 0:
                fire_size = b["fire_level"] / 100
                for _ in range(int(5 * fire_size)):
                    fx = bx + random.randint(-30, 30)
                    fy = by + random.randint(-20, 30)
                    fsize = random.randint(10, 25) * fire_size
                    colors = ["#FF4500", "#FF6600", "#FFCC00", "#FF0000"]
                    self.fire_canvas.create_oval(fx-fsize, fy-fsize, fx+fsize, fy+fsize, 
                                                 fill=random.choice(colors), outline="")
            
            # 已救标记
            if b["saved"]:
                self.fire_canvas.create_text(bx, by-20, text="✅ 已救", 
                                             font=("微软雅黑", 12, "bold"), fill="#32CD32")
        
        # 更新水柱
        new_water = []
        for w in self.fire_water:
            if w["active"]:
                w["y"] -= 15
                if w["y"] > 50:
                    new_water.append(w)
                    # 画水柱
                    self.fire_canvas.create_oval(w["x"]-8, w["y"]-15, w["x"]+8, w["y"]+15, 
                                                 fill="#00BFFF", outline="#1E90FF", width=2)
                    
                    # 检测是否击中着火建筑
                    for b in self.fire_buildings:
                        if b["on_fire"] and not b["saved"]:
                            if abs(w["x"] - b["x"]) < 50 and w["y"] < ground_y - b["height"] + 50:
                                b["fire_level"] -= 12  # 水更有效
                                if b["fire_level"] <= 0:
                                    b["on_fire"] = False
                                    b["saved"] = True
                                    self.fires_saved += 1
                                    self.fire_score += 50
                                    self.score += 50
                                    self.score_label.config(text=f"⭐ 得分: {self.fire_score}")
                                    self.fire_progress.config(text=f"已救: {self.fires_saved}/5 栋楼")
                                    self.speak_praise()
                                    
                                    if self.fires_saved >= 5:
                                        self.game_running = False
                                        self.fire_canvas.create_text(cw//2, ch//2, text="🎉 全部救完了！", 
                                                                     font=("微软雅黑", 36, "bold"), fill="#32CD32")
                                        self.speak(f"太棒了！乐乐救了所有的楼！得了{self.fire_score}分！")
                                        self.window.after(5500, self.create_main_menu)
                                        return
        self.fire_water = new_water
        
        # 画消防车
        truck_y = ground_y - 35
        self.draw_fire_truck(self.fire_canvas, self.fire_truck_x, truck_y, 0.9)
        
        # 画水管
        self.fire_canvas.create_line(self.fire_truck_x-30, truck_y-20, self.fire_truck_x+30, truck_y-40, 
                                     fill="#C0C0C0", width=5)
        
        self.window.after(60, self.fire_game_loop)


    # =====================================================
    # 游戏5: 火箭发射
    # =====================================================
    def start_rocket_game(self):
        self.clear_game_area("#0a0a23")
        self.rocket_score = 0
        self.rocket_launched = False
        self.rocket_countdown = 10
        self.rocket_fuel = 100
        self.rocket_stars = []
        self.rocket_altitude = 0
        self.game_running = True
        
        # 获取当前狗狗信息
        pup = self.PAW_PATROL_GAMES.get("rocky", {})
        
        tk.Label(self.game_frame, text=f"🚀 {pup.get('name', '灰灰')}的火箭", font=("微软雅黑", 24, "bold"),
                 bg="#0a0a23", fg="#9C27B0").pack(pady=3)
        
        tk.Label(self.game_frame, text="按空格键发射！发射后用左右键躲避陨石，收集燃料！",
                 font=("微软雅黑", 12), bg="#0a0a23", fg="#AAA").pack()
        
        self.rocket_status = tk.Label(self.game_frame, text="准备发射...",
                                       font=("微软雅黑", 14, "bold"), bg="#0a0a23", fg="#FFD700")
        self.rocket_status.pack()
        
        # 游戏画布 - 自适应窗口大小
        self.rocket_canvas = tk.Canvas(self.game_frame, bg="#0a0a23", highlightthickness=2)
        self.rocket_canvas.pack(pady=5, fill=tk.BOTH, expand=True)
        self.window.update()
        
        # 获取画布尺寸
        self.rocket_cw = self.rocket_canvas.winfo_width()
        self.rocket_ch = self.rocket_canvas.winfo_height()
        if self.rocket_cw < 100:
            self.rocket_cw = 900
            self.rocket_ch = 550
        
        # 初始化火箭位置
        self.rocket_x = self.rocket_cw // 2
        self.rocket_y = int(self.rocket_ch * 0.91)
        
        # 绑定键盘
        self.window.bind("<space>", self.rocket_launch)
        self.window.bind("<Left>", self.rocket_move_left)
        self.window.bind("<Right>", self.rocket_move_right)
        
        self.rocket_meteors = []
        self.rocket_fuels = []
        
        self.speak(f"{pup.get('name', '灰灰')}说：火箭准备发射！按空格键点火！")
        self.rocket_countdown_loop()
    
    def rocket_launch(self, event):
        if not self.rocket_launched and self.game_running:
            self.rocket_launched = True
            self.speak("点火！发射！")
    
    def rocket_move_left(self, event):
        if self.rocket_launched and self.game_running and self.rocket_x > 100:
            self.rocket_x -= 30
    
    def rocket_move_right(self, event):
        if self.rocket_launched and self.game_running and self.rocket_x < self.rocket_cw - 100:
            self.rocket_x += 30
    
    def rocket_countdown_loop(self):
        if not self.game_running:
            return
        
        self.rocket_canvas.delete("all")
        # 动态获取画布尺寸（支持窗口最大化）
        cw = self.rocket_canvas.winfo_width()
        ch = self.rocket_canvas.winfo_height()
        if cw < 100:
            cw, ch = 900, 550
        self.rocket_cw, self.rocket_ch = cw, ch
        
        # 星空背景
        for _ in range(50):
            sx = random.randint(0, cw)
            sy = random.randint(0, ch)
            size = random.randint(1, 3)
            self.rocket_canvas.create_oval(sx-size, sy-size, sx+size, sy+size, fill="white", outline="")
        
        if not self.rocket_launched:
            # 发射台
            pad_y = int(ch * 0.95)
            self.rocket_canvas.create_rectangle(cw//2-100, pad_y-30, cw//2+100, pad_y, fill="#555555", outline="#333333", width=2)
            self.rocket_canvas.create_polygon(cw//2-50, pad_y-30, cw//2, pad_y-70, cw//2+50, pad_y-30, fill="#777777", outline="#555555")
            
            # 火箭
            self.draw_rocket(self.rocket_canvas, cw//2, pad_y-130, 1.2, False)
            
            # 倒计时
            self.rocket_canvas.create_text(cw//2, ch*0.36, text=f"倒计时: {self.rocket_countdown}", 
                                           font=("微软雅黑", 48, "bold"), fill="#FFD700")
            self.rocket_canvas.create_text(cw//2, ch*0.5, text="按 空格键 发射！", 
                                           font=("微软雅黑", 20), fill="#AAA")
            
            self.rocket_countdown -= 1
            if self.rocket_countdown < 0:
                self.rocket_countdown = 10
            
            self.window.after(1000, self.rocket_countdown_loop)
        else:
            self.rocket_fly_loop()
    
    def rocket_fly_loop(self):
        if not self.game_running:
            return
        
        self.rocket_canvas.delete("all")
        # 动态获取画布尺寸（支持窗口最大化）
        cw = self.rocket_canvas.winfo_width()
        ch = self.rocket_canvas.winfo_height()
        if cw < 100:
            cw, ch = 900, 550
        
        # 如果画布尺寸变化，调整火箭位置
        if hasattr(self, 'rocket_cw') and self.rocket_cw > 0:
            self.rocket_x = int(self.rocket_x * cw / self.rocket_cw)
        
        self.rocket_cw, self.rocket_ch = cw, ch
        rocket_draw_y = int(ch * 0.73)
        
        # 确保火箭在有效范围内
        self.rocket_x = max(100, min(self.rocket_x, cw - 100))
        
        # 太空背景（随高度变化）
        bg_color = max(10, 35 - self.rocket_altitude // 500)
        self.rocket_canvas.create_rectangle(0, 0, cw, ch, fill=f"#0a0a{bg_color:02x}", outline="")
        
        # 星星
        for _ in range(80):
            sx = random.randint(0, cw)
            sy = random.randint(0, ch)
            size = random.randint(1, 3)
            brightness = random.randint(200, 255)
            self.rocket_canvas.create_oval(sx-size, sy-size, sx+size, sy+size, 
                                           fill=f"#{brightness:02x}{brightness:02x}{brightness:02x}", outline="")
        
        # 生成陨石
        if random.random() < 0.015:  # 降低陨石频率
            mx = random.randint(100, cw - 100)
            self.rocket_meteors.append({"x": mx, "y": -30})
        
        # 生成燃料
        if random.random() < 0.05:  # 增加燃料频率
            fx = random.randint(150, cw - 150)
            self.rocket_fuels.append({"x": fx, "y": -30})
        
        # 更新陨石
        new_meteors = []
        for m in self.rocket_meteors:
            m["y"] += 5  # 陨石下落更慢
            if m["y"] < ch + 50:
                new_meteors.append(m)
                # 画陨石
                mx, my = m["x"], m["y"]
                self.rocket_canvas.create_oval(mx-20, my-20, mx+20, my+20, fill="#8B4513", outline="#654321", width=2)
                # 陨石坑
                for _ in range(3):
                    cx = mx + random.randint(-12, 12)
                    cy = my + random.randint(-12, 12)
                    self.rocket_canvas.create_oval(cx-5, cy-5, cx+5, cy+5, fill="#654321", outline="")
                # 火焰尾巴
                self.rocket_canvas.create_polygon(mx, my-20, mx-10, my-40, mx+10, my-40, 
                                                  fill="#FF4500", outline="")
        self.rocket_meteors = new_meteors
        
        # 更新燃料
        new_fuels = []
        for f in self.rocket_fuels:
            f["y"] += 5
            if f["y"] < ch + 50:
                new_fuels.append(f)
                # 画燃料罐
                fx, fy = f["x"], f["y"]
                self.rocket_canvas.create_rectangle(fx-12, fy-18, fx+12, fy+18, fill="#32CD32", outline="#228B22", width=2)
                self.rocket_canvas.create_text(fx, fy, text="F", font=("Arial", 14, "bold"), fill="white")
        self.rocket_fuels = new_fuels
        
        # 画火箭
        self.draw_rocket(self.rocket_canvas, self.rocket_x, rocket_draw_y, 1.0, True)
        
        # 碰撞检测 - 陨石
        for m in self.rocket_meteors:
            if abs(m["x"] - self.rocket_x) < 30 and abs(m["y"] - rocket_draw_y) < 35:  # 更宽松
                self.game_running = False
                self.rocket_canvas.create_text(cw//2, ch//2, text="💥 撞到陨石了！", 
                                               font=("微软雅黑", 36, "bold"), fill="#FF0000")
                self.speak(f"哎呀撞到陨石了！火箭飞了{self.rocket_altitude}米，得了{self.rocket_score}分！")
                self.window.after(3000, self.create_main_menu)
                return
        
        # 碰撞检测 - 燃料
        for f in self.rocket_fuels[:]:
            if abs(f["x"] - self.rocket_x) < 35 and abs(f["y"] - rocket_draw_y) < 50:
                self.rocket_fuels.remove(f)
                self.rocket_fuel = min(100, self.rocket_fuel + 20)
                self.rocket_score += 20
                self.score += 20
                self.score_label.config(text=f"⭐ 得分: {self.rocket_score}")
        
        # 消耗燃料
        self.rocket_fuel -= 0.15  # 燃料消耗更慢
        self.rocket_altitude += 10
        
        if self.rocket_fuel <= 0:
            self.game_running = False
            self.rocket_canvas.create_text(cw//2, ch//2, text="⛽ 燃料耗尽！", 
                                           font=("微软雅黑", 36, "bold"), fill="#FFD700")
            self.speak(f"燃料用完了！火箭飞了{self.rocket_altitude}米，得了{self.rocket_score}分！")
            self.window.after(3000, self.create_main_menu)
            return
        
        # 显示状态
        self.rocket_canvas.create_text(100, 30, text=f"高度: {self.rocket_altitude}m", 
                                       font=("微软雅黑", 14), fill="white", anchor="w")
        
        # 燃料条
        fuel_bar_x = cw - 150
        self.rocket_canvas.create_rectangle(fuel_bar_x, 20, fuel_bar_x+150, 40, fill="#333333", outline="#555555")
        fuel_width = int(150 * self.rocket_fuel / 100)
        fuel_color = "#32CD32" if self.rocket_fuel > 30 else "#FF6600" if self.rocket_fuel > 10 else "#FF0000"
        self.rocket_canvas.create_rectangle(fuel_bar_x, 20, fuel_bar_x+fuel_width, 40, fill=fuel_color, outline="")
        self.rocket_canvas.create_text(fuel_bar_x+75, 30, text=f"燃料: {int(self.rocket_fuel)}%", 
                                       font=("微软雅黑", 10), fill="white")
        
        self.window.after(50, self.rocket_fly_loop)

    # =====================================================
    # 游戏6: 火车运货
    # =====================================================
    def start_train_game(self):
        self.clear_game_area("#87CEEB")
        self.train_score = 0
        self.train_cargo = []
        self.train_stations = []
        self.train_current_cargo = None
        self.train_deliveries = 0
        self.game_running = True
        
        # 获取当前狗狗信息
        pup = self.PAW_PATROL_GAMES.get("zuma", {})
        
        tk.Label(self.game_frame, text=f"🚂 {pup.get('name', '路马')}的火车", font=("微软雅黑", 24, "bold"),
                 bg="#87CEEB", fg="#228B22").pack(pady=3)
        
        tk.Label(self.game_frame, text="用左右方向键移动火车，在车站按空格装货/卸货！完成3次运送获胜！",
                 font=("微软雅黑", 11), bg="#87CEEB", fg="#555").pack()
        
        self.train_status = tk.Label(self.game_frame, text="运送: 0/3",
                                      font=("微软雅黑", 14, "bold"), bg="#87CEEB", fg="#228B22")
        self.train_status.pack()
        
        # 游戏画布 - 自适应窗口大小
        self.train_canvas = tk.Canvas(self.game_frame, bg="#87CEEB", highlightthickness=2)
        self.train_canvas.pack(pady=5, fill=tk.BOTH, expand=True)
        self.window.update()
        
        # 获取画布尺寸
        self.train_cw = self.train_canvas.winfo_width()
        self.train_ch = self.train_canvas.winfo_height()
        if self.train_cw < 100:
            self.train_cw = 900
            self.train_ch = 550
        
        # 初始化火车位置
        self.train_x = int(self.train_cw * 0.11)
        
        # 绑定键盘
        self.window.bind("<Left>", self.train_move_left)
        self.window.bind("<Right>", self.train_move_right)
        self.window.bind("<space>", self.train_action)
        
        # 初始化车站
        self.train_init_stations()
        self.speak(f"{pup.get('name', '路马')}说：火车准备出发！去车站装货送货！")
        self.train_game_loop()
    
    def train_init_stations(self):
        self.train_stations = []
        spacing = self.train_cw // 5
        stations_data = [
            {"name": "苹果站", "cargo": "🍎", "color": "#FF6B6B"},
            {"name": "香蕉站", "cargo": "🍌", "color": "#FFD700"},
            {"name": "西瓜站", "cargo": "🍉", "color": "#32CD32"},
            {"name": "葡萄站", "cargo": "🍇", "color": "#9C27B0"},
        ]
        for i, data in enumerate(stations_data):
            self.train_stations.append({
                "x": spacing + i * spacing, 
                "name": data["name"], 
                "cargo": data["cargo"], 
                "color": data["color"],
                "has_cargo": True, 
                "wants_cargo": None
            })
        self.train_assign_delivery()
    
    def train_assign_delivery(self):
        # 随机选择一个有货的站和一个要货的站
        available = [s for s in self.train_stations if s["has_cargo"]]
        if not available:
            for s in self.train_stations:
                s["has_cargo"] = True
            available = self.train_stations
        
        from_station = random.choice(available)
        to_station = random.choice([s for s in self.train_stations if s != from_station])
        
        from_station["has_cargo"] = True
        to_station["wants_cargo"] = from_station["cargo"]
        
        self.train_task = {"from": from_station, "to": to_station, "cargo": from_station["cargo"]}
    
    def train_move_left(self, event):
        if self.game_running and self.train_x > 80:
            self.train_x -= 35  # 火车移动更快
    
    def train_move_right(self, event):
        if self.game_running and self.train_x < self.train_cw - 80:
            self.train_x += 35  # 火车移动更快
    
    def train_action(self, event):
        if not self.game_running:
            return
        
        # 检查是否在车站
        for station in self.train_stations:
            if abs(self.train_x - station["x"]) < 60:
                # 装货
                if self.train_current_cargo is None and station == self.train_task["from"] and station["has_cargo"]:
                    self.train_current_cargo = station["cargo"]
                    station["has_cargo"] = False
                    self.speak(f"装上了{station['cargo']}！送到{self.train_task['to']['name']}去！")
                # 卸货
                elif self.train_current_cargo and station == self.train_task["to"]:
                    station["wants_cargo"] = None
                    self.train_current_cargo = None
                    self.train_deliveries += 1
                    self.train_score += 30
                    self.score += 30
                    self.score_label.config(text=f"⭐ 得分: {self.train_score}")
                    self.train_status.config(text=f"运送: {self.train_deliveries}/3")
                    self.speak_praise()
                    
                    if self.train_deliveries >= 3:  # 减少运送次数
                        self.game_running = False
                        self.speak(f"太棒了！乐乐完成了所有运送任务！得了{self.train_score}分！")
                        self.window.after(3000, self.create_main_menu)
                        return
                    
                    self.train_assign_delivery()
                break
    
    def train_game_loop(self):
        if not self.game_running:
            return
        
        self.train_canvas.delete("all")
        # 动态获取画布尺寸（支持窗口最大化）
        cw = self.train_canvas.winfo_width()
        ch = self.train_canvas.winfo_height()
        if cw < 100:
            cw, ch = 900, 550
        
        # 如果画布尺寸变化，调整火车位置（保持相对比例）
        if hasattr(self, 'train_cw') and self.train_cw > 0:
            ratio = self.train_x / self.train_cw
            self.train_x = int(cw * ratio)
        
        self.train_cw, self.train_ch = cw, ch
        ground_y = int(ch * 0.64)
        track_y = int(ch * 0.76)
        
        # 确保火车在有效范围内
        self.train_x = max(80, min(self.train_x, cw - 80))
        
        # 重新计算车站位置（按比例分布）
        spacing = cw // 5
        for i, station in enumerate(self.train_stations):
            station["x"] = spacing + i * spacing
        
        # 天空
        sky_height = int(ch * 0.55)
        for i in range(sky_height):
            r = min(255, 135 + i // 5)
            g = min(255, 206 + i // 8)
            b = 235
            color = f"#{r:02x}{g:02x}{b:02x}"
            self.train_canvas.create_line(0, i, cw, i, fill=color)
        
        # 太阳
        sun_x = int(cw * 0.87)
        self.train_canvas.create_oval(sun_x, 30, sun_x+70, 100, fill="#FFD700", outline="#FFA500", width=3)
        
        # 云朵
        for cx_ratio in [0.17, 0.44, 0.72]:
            cx = int(cw * cx_ratio)
            cy = random.randint(40, 70)
            for dx, dy in [(-20, 0), (0, -10), (20, 0), (0, 10)]:
                self.train_canvas.create_oval(cx+dx-25, cy+dy-15, cx+dx+25, cy+dy+15, fill="white", outline="")
        
        # 草地
        self.train_canvas.create_rectangle(0, ground_y, cw, ch, fill="#228B22", outline="")
        
        # 铁轨
        self.train_canvas.create_rectangle(0, track_y, cw, track_y+10, fill="#8B4513", outline="")
        self.train_canvas.create_rectangle(0, track_y+25, cw, track_y+35, fill="#8B4513", outline="")
        for i in range(0, cw, 40):
            self.train_canvas.create_rectangle(i, track_y-5, i+25, track_y+40, fill="#654321", outline="#543210")
        
        # 画车站
        for station in self.train_stations:
            sx = station["x"]
            color = station["color"]
            
            # 站台
            self.train_canvas.create_rectangle(sx-60, track_y-40, sx+60, track_y, fill="#DDD", outline="#999", width=2)
            
            # 站牌
            self.train_canvas.create_rectangle(sx-35, track_y-130, sx+35, track_y-40, fill=color, outline="#333", width=2)
            self.train_canvas.create_text(sx, track_y-85, text=station["name"], font=("微软雅黑", 11, "bold"), fill="white")
            
            # 货物 - 使用真实水果绘制
            if station["has_cargo"]:
                self.draw_fruit(self.train_canvas, station["cargo"], sx, track_y-20, size=50)
            
            # 需要的货物（闪烁效果）
            if station["wants_cargo"]:
                self.train_canvas.create_rectangle(sx-30, track_y-165, sx+30, track_y-130, fill="#FFD700", outline="#FFA500", width=2)
                self.train_canvas.create_text(sx, track_y-155, text="需要", font=("微软雅黑", 9), fill="#333")
                self.draw_fruit(self.train_canvas, station["wants_cargo"], sx, track_y-140, size=25)
        
        # 画火车
        train_draw_y = track_y - 25
        self.draw_train(self.train_canvas, self.train_x, train_draw_y, 0.8, "#228B22")
        
        # 画车厢（如果有货物）
        if self.train_current_cargo:
            # 车厢
            cx = self.train_x - 90
            # 车厢主体
            self.train_canvas.create_rectangle(cx-35, train_draw_y-10, cx+35, train_draw_y+30, fill="#8B4513", outline="#654321", width=2)
            # 车厢顶部
            self.train_canvas.create_rectangle(cx-38, train_draw_y-15, cx+38, train_draw_y-10, fill="#A0522D", outline="#8B4513", width=1)
            # 货物 - 使用真实水果绘制
            self.draw_fruit(self.train_canvas, self.train_current_cargo, cx, train_draw_y+8, size=45)
            # 轮子
            self.train_canvas.create_oval(cx-25, train_draw_y+25, cx-8, train_draw_y+42, fill="#222", outline="#111", width=2)
            self.train_canvas.create_oval(cx+8, train_draw_y+25, cx+25, train_draw_y+42, fill="#222", outline="#111", width=2)
            # 轮子中心
            self.train_canvas.create_oval(cx-20, train_draw_y+30, cx-13, train_draw_y+37, fill="#444", outline="")
            self.train_canvas.create_oval(cx+13, train_draw_y+30, cx+20, train_draw_y+37, fill="#444", outline="")
        
        # 任务提示
        task_text = f"任务: 从 {self.train_task['from']['name']} 运送货物到 {self.train_task['to']['name']}"
        tip_y = ch - 50
        # 任务框
        self.train_canvas.create_rectangle(cw//2-280, tip_y-25, cw//2+280, tip_y+25, fill="#FFF8DC", outline="#DDD", width=2)
        self.train_canvas.create_text(cw//2, tip_y-8, text=task_text, font=("微软雅黑", 12), fill="#333")
        # 在任务框中显示要运送的水果
        self.draw_fruit(self.train_canvas, self.train_task['cargo'], cw//2, tip_y+12, size=30)
        
        self.window.after(50, self.train_game_loop)

    # =====================================================
    # 游戏7: 交通小达人 - 认识交通工具和交通规则
    # =====================================================
    def start_traffic_quiz(self):
        self.clear_game_area("#E8F5E9")
        self.quiz_score = 0
        self.quiz_round = 0
        self.quiz_mode = "menu"
        
        # 获取当前狗狗信息
        pup = self.PAW_PATROL_GAMES.get("liberty", {})
        
        tk.Label(self.game_frame, text=f"🎓 {pup.get('name', '乐乐')}的小达人", font=("微软雅黑", 26, "bold"),
                 bg="#E8F5E9", fg="#4CAF50").pack(pady=10)
        
        # 模式选择
        mode_frame = tk.Frame(self.game_frame, bg="#E8F5E9")
        mode_frame.pack(pady=20)
        
        modes = [
            ("🚗 认识车车", "#FF6B6B", self.quiz_vehicles),
            ("🔊 听声音猜车", "#4ECDC4", self.quiz_sounds),
            ("🚦 交通规则", "#FFD93D", self.quiz_rules),
            ("🎯 快速反应", "#9C27B0", self.quiz_speed),
        ]
        
        for title, color, cmd in modes:
            btn = tk.Button(mode_frame, text=title, font=("微软雅黑", 16, "bold"),
                           bg=color, fg="white", width=14, height=2,
                           relief=tk.RAISED, bd=4, cursor="hand2", command=cmd)
            btn.pack(pady=10)
        
        self.speak(f"{pup.get('name', '乐乐')}说：选择一个模式开始学习吧！")
    
    def quiz_vehicles(self):
        """认识交通工具"""
        for widget in self.game_frame.winfo_children():
            widget.destroy()
        
        self.quiz_score = 0
        self.quiz_round = 0
        
        # 交通工具数据
        self.vehicles_data = [
            {"name": "挖掘机", "emoji": "🏗️", "desc": "用来挖土的工程车", "sound": "轰隆隆", "draw": "excavator"},
            {"name": "赛车", "emoji": "🏎️", "desc": "跑得很快的车", "sound": "嗖嗖嗖", "draw": "race_car"},
            {"name": "消防车", "emoji": "🚒", "desc": "救火的车，红色的", "sound": "呜呜呜", "draw": "fire_truck"},
            {"name": "飞机", "emoji": "✈️", "desc": "在天上飞的", "sound": "呼呼呼", "draw": "airplane"},
            {"name": "火箭", "emoji": "🚀", "desc": "飞向太空的", "sound": "轰轰轰", "draw": "rocket"},
            {"name": "火车", "emoji": "🚂", "desc": "在铁轨上跑的", "sound": "呜呜呜", "draw": "train"},
            {"name": "公交车", "emoji": "🚌", "desc": "很多人一起坐的车", "sound": "滴滴滴", "draw": None},
            {"name": "救护车", "emoji": "🚑", "desc": "救人的车，白色的", "sound": "呜哇呜哇", "draw": None},
            {"name": "警车", "emoji": "🚓", "desc": "警察叔叔开的车", "sound": "呜呜呜", "draw": None},
            {"name": "出租车", "emoji": "🚕", "desc": "可以打车坐的", "sound": "滴滴", "draw": None},
            {"name": "自行车", "emoji": "🚲", "desc": "用脚踩的两轮车", "sound": "叮铃铃", "draw": None},
            {"name": "摩托车", "emoji": "🏍️", "desc": "两个轮子的机车", "sound": "突突突", "draw": None},
        ]
        
        tk.Label(self.game_frame, text="🚗 认识交通工具", font=("微软雅黑", 22, "bold"),
                 bg="#E8F5E9", fg="#4CAF50").pack(pady=5)
        
        self.quiz_score_label = tk.Label(self.game_frame, text="⭐ 得分: 0",
                                          font=("微软雅黑", 14), bg="#E8F5E9", fg="#666")
        self.quiz_score_label.pack(pady=5)
        
        # 显示区域
        self.quiz_display = tk.Canvas(self.game_frame, width=300, height=200, bg="white",
                                       relief=tk.RAISED, bd=4)
        self.quiz_display.pack(pady=15)
        
        self.quiz_hint = tk.Label(self.game_frame, text="", font=("微软雅黑", 16),
                                   bg="#E8F5E9", fg="#333")
        self.quiz_hint.pack(pady=5)
        
        # 选项按钮
        self.quiz_options_frame = tk.Frame(self.game_frame, bg="#E8F5E9")
        self.quiz_options_frame.pack(pady=15)
        
        self.quiz_buttons = []
        colors = ["#FF6B6B", "#4ECDC4", "#45B7D1", "#96CEB4"]
        for i in range(4):
            btn = tk.Button(self.quiz_options_frame, text="", font=("微软雅黑", 14, "bold"),
                           width=12, height=2, bg=colors[i], fg="white",
                           relief=tk.RAISED, bd=3, cursor="hand2",
                           command=lambda idx=i: self.check_vehicle_quiz(idx))
            btn.grid(row=i//2, column=i%2, padx=10, pady=8)
            self.quiz_buttons.append(btn)
        
        self.new_vehicle_question()
    
    def new_vehicle_question(self):
        """生成新的交通工具问题"""
        self.quiz_round += 1
        
        # 随机选择目标
        self.quiz_target = random.choice(self.vehicles_data)
        others = random.sample([v for v in self.vehicles_data if v != self.quiz_target], 3)
        self.quiz_options = [self.quiz_target] + others
        random.shuffle(self.quiz_options)
        self.quiz_correct_idx = self.quiz_options.index(self.quiz_target)
        
        # 显示图片或emoji
        self.quiz_display.delete("all")
        
        # 尝试绘制交通工具
        draw_method = self.quiz_target.get("draw")
        if draw_method == "excavator":
            self.draw_excavator(self.quiz_display, 150, 100, 0.8, 30)
        elif draw_method == "race_car":
            self.draw_race_car(self.quiz_display, 150, 100, 0.9, "#FF0000")
        elif draw_method == "fire_truck":
            self.draw_fire_truck(self.quiz_display, 150, 100, 0.7)
        elif draw_method == "airplane":
            self.draw_airplane(self.quiz_display, 150, 100, 0.7)
        elif draw_method == "rocket":
            self.draw_rocket(self.quiz_display, 150, 120, 0.6)
        elif draw_method == "train":
            self.draw_train(self.quiz_display, 150, 120, 0.7)
        else:
            # 用大emoji显示
            self.quiz_display.create_text(150, 100, text=self.quiz_target["emoji"],
                                          font=("Segoe UI Emoji", 80))
        
        # 更新选项按钮
        colors = ["#FF6B6B", "#4ECDC4", "#45B7D1", "#96CEB4"]
        for i, btn in enumerate(self.quiz_buttons):
            btn.config(text=self.quiz_options[i]["name"], bg=colors[i], state=tk.NORMAL)
        
        self.quiz_hint.config(text="这是什么车？", fg="#333")
        self.speak(f"这是什么车？")
    
    def check_vehicle_quiz(self, idx):
        """检查答案"""
        if idx == self.quiz_correct_idx:
            self.quiz_score += 10
            self.score += 10
            self.quiz_hint.config(text=f"🎉 对啦！这是{self.quiz_target['name']}！{self.quiz_target['desc']}", fg="#32CD32")
            self.quiz_buttons[idx].config(bg="#32CD32")
            self.speak_praise()
        else:
            self.quiz_hint.config(text=f"😅 这是{self.quiz_target['name']}哦！{self.quiz_target['desc']}", fg="#FF6B6B")
            self.quiz_buttons[idx].config(bg="#808080")
            self.quiz_buttons[self.quiz_correct_idx].config(bg="#32CD32")
            self.speak_encourage()
        
        self.quiz_score_label.config(text=f"⭐ 得分: {self.quiz_score}")
        
        for btn in self.quiz_buttons:
            btn.config(state=tk.DISABLED)
        
        self.window.after(3000, self.new_vehicle_question)
    
    def quiz_sounds(self):
        """听声音猜车"""
        for widget in self.game_frame.winfo_children():
            widget.destroy()
        
        self.quiz_score = 0
        
        tk.Label(self.game_frame, text="🔊 听声音猜车车", font=("微软雅黑", 22, "bold"),
                 bg="#E8F5E9", fg="#4ECDC4").pack(pady=5)
        
        self.quiz_score_label = tk.Label(self.game_frame, text="⭐ 得分: 0",
                                          font=("微软雅黑", 14), bg="#E8F5E9", fg="#666")
        self.quiz_score_label.pack(pady=5)
        
        # 声音提示
        self.sound_label = tk.Label(self.game_frame, text="", font=("微软雅黑", 40, "bold"),
                                     bg="#E8F5E9", fg="#FF6B6B")
        self.sound_label.pack(pady=20)
        
        tk.Button(self.game_frame, text="🔊 再听一遍", font=("微软雅黑", 12),
                  bg="#FF6B6B", fg="white", command=self.replay_sound).pack(pady=10)
        
        self.quiz_hint = tk.Label(self.game_frame, text="", font=("微软雅黑", 16),
                                   bg="#E8F5E9", fg="#333")
        self.quiz_hint.pack(pady=5)
        
        # 选项按钮 - 用emoji显示
        self.quiz_options_frame = tk.Frame(self.game_frame, bg="#E8F5E9")
        self.quiz_options_frame.pack(pady=15)
        
        self.quiz_buttons = []
        colors = ["#FF6B6B", "#4ECDC4", "#45B7D1", "#96CEB4"]
        for i in range(4):
            btn = tk.Button(self.quiz_options_frame, text="", font=("Segoe UI Emoji", 40),
                           width=3, height=1, bg=colors[i], fg="white",
                           relief=tk.RAISED, bd=4, cursor="hand2",
                           command=lambda idx=i: self.check_sound_quiz(idx))
            btn.grid(row=0, column=i, padx=15, pady=10)
            self.quiz_buttons.append(btn)
        
        self.new_sound_question()
    
    def new_sound_question(self):
        """生成新的声音问题"""
        # 选择有声音的交通工具
        sound_vehicles = [v for v in self.vehicles_data if v.get("sound")]
        self.quiz_target = random.choice(sound_vehicles)
        others = random.sample([v for v in sound_vehicles if v != self.quiz_target], 3)
        self.quiz_options = [self.quiz_target] + others
        random.shuffle(self.quiz_options)
        self.quiz_correct_idx = self.quiz_options.index(self.quiz_target)
        
        # 显示声音
        self.sound_label.config(text=f"「{self.quiz_target['sound']}」")
        
        # 更新选项
        colors = ["#FF6B6B", "#4ECDC4", "#45B7D1", "#96CEB4"]
        for i, btn in enumerate(self.quiz_buttons):
            btn.config(text=self.quiz_options[i]["emoji"], bg=colors[i], state=tk.NORMAL)
        
        self.quiz_hint.config(text="哪个车车发出这个声音？", fg="#333")
        self.speak(f"{self.quiz_target['sound']}，这是什么车的声音？")
    
    def replay_sound(self):
        """重播声音"""
        if hasattr(self, 'quiz_target'):
            self.speak(f"{self.quiz_target['sound']}")
    
    def check_sound_quiz(self, idx):
        """检查声音答案"""
        if idx == self.quiz_correct_idx:
            self.quiz_score += 10
            self.score += 10
            self.quiz_hint.config(text=f"🎉 对啦！{self.quiz_target['name']}的声音是{self.quiz_target['sound']}！", fg="#32CD32")
            self.quiz_buttons[idx].config(bg="#32CD32")
            self.speak_praise()
        else:
            self.quiz_hint.config(text=f"😅 是{self.quiz_target['name']}哦！", fg="#FF6B6B")
            self.quiz_buttons[idx].config(bg="#808080")
            self.quiz_buttons[self.quiz_correct_idx].config(bg="#32CD32")
            self.speak_encourage()
        
        self.quiz_score_label.config(text=f"⭐ 得分: {self.quiz_score}")
        
        for btn in self.quiz_buttons:
            btn.config(state=tk.DISABLED)
        
        self.window.after(3000, self.new_sound_question)
    
    def quiz_rules(self):
        """交通规则学习"""
        for widget in self.game_frame.winfo_children():
            widget.destroy()
        
        self.quiz_score = 0
        
        # 交通规则数据
        self.rules_data = [
            {"question": "红灯亮了，我们应该？", "answer": "停下来等待", "wrong": ["继续走", "跑过去", "不看灯"], "emoji": "🔴"},
            {"question": "绿灯亮了，我们可以？", "answer": "安全通过", "wrong": ["继续等", "闭眼走", "跑着过"], "emoji": "🟢"},
            {"question": "黄灯亮了，我们应该？", "answer": "准备停下", "wrong": ["加速冲", "不理它", "往回走"], "emoji": "🟡"},
            {"question": "过马路要走？", "answer": "斑马线", "wrong": ["马路中间", "随便走", "跑着过"], "emoji": "🦓"},
            {"question": "坐车要系？", "answer": "安全带", "wrong": ["围巾", "绳子", "不用系"], "emoji": "🚗"},
            {"question": "看到救护车，我们要？", "answer": "让它先走", "wrong": ["挡住它", "跟着跑", "不理它"], "emoji": "🚑"},
            {"question": "在车上可以把头伸出窗外吗？", "answer": "不可以", "wrong": ["可以", "随便", "想伸就伸"], "emoji": "🚌"},
            {"question": "骑自行车要靠哪边走？", "answer": "右边", "wrong": ["左边", "中间", "随便"], "emoji": "🚲"},
        ]
        
        tk.Label(self.game_frame, text="🚦 交通规则小课堂", font=("微软雅黑", 22, "bold"),
                 bg="#E8F5E9", fg="#FFD93D").pack(pady=5)
        
        self.quiz_score_label = tk.Label(self.game_frame, text="⭐ 得分: 0",
                                          font=("微软雅黑", 14), bg="#E8F5E9", fg="#666")
        self.quiz_score_label.pack(pady=5)
        
        # 问题显示
        self.rule_emoji = tk.Label(self.game_frame, text="", font=("Segoe UI Emoji", 60),
                                    bg="#E8F5E9")
        self.rule_emoji.pack(pady=10)
        
        self.rule_question = tk.Label(self.game_frame, text="", font=("微软雅黑", 18, "bold"),
                                       bg="#E8F5E9", fg="#333")
        self.rule_question.pack(pady=10)
        
        self.quiz_hint = tk.Label(self.game_frame, text="", font=("微软雅黑", 14),
                                   bg="#E8F5E9", fg="#333")
        self.quiz_hint.pack(pady=5)
        
        # 选项
        self.quiz_options_frame = tk.Frame(self.game_frame, bg="#E8F5E9")
        self.quiz_options_frame.pack(pady=15)
        
        self.quiz_buttons = []
        colors = ["#FF6B6B", "#4ECDC4", "#45B7D1", "#96CEB4"]
        for i in range(4):
            btn = tk.Button(self.quiz_options_frame, text="", font=("微软雅黑", 14, "bold"),
                           width=12, height=2, bg=colors[i], fg="white",
                           relief=tk.RAISED, bd=3, cursor="hand2",
                           command=lambda idx=i: self.check_rule_quiz(idx))
            btn.grid(row=i//2, column=i%2, padx=10, pady=8)
            self.quiz_buttons.append(btn)
        
        self.new_rule_question()
    
    def new_rule_question(self):
        """生成新的规则问题"""
        self.quiz_target = random.choice(self.rules_data)
        
        # 生成选项
        options = [self.quiz_target["answer"]] + self.quiz_target["wrong"][:3]
        random.shuffle(options)
        self.quiz_options = options
        self.quiz_correct_idx = options.index(self.quiz_target["answer"])
        
        # 显示问题
        self.rule_emoji.config(text=self.quiz_target["emoji"])
        self.rule_question.config(text=self.quiz_target["question"])
        
        # 更新选项
        colors = ["#FF6B6B", "#4ECDC4", "#45B7D1", "#96CEB4"]
        for i, btn in enumerate(self.quiz_buttons):
            btn.config(text=options[i], bg=colors[i], state=tk.NORMAL)
        
        self.quiz_hint.config(text="", fg="#333")
        self.speak(self.quiz_target["question"])
    
    def check_rule_quiz(self, idx):
        """检查规则答案"""
        if idx == self.quiz_correct_idx:
            self.quiz_score += 10
            self.score += 10
            self.quiz_hint.config(text=f"🎉 太棒了！{self.quiz_target['answer']}是对的！", fg="#32CD32")
            self.quiz_buttons[idx].config(bg="#32CD32")
            self.speak_praise()
        else:
            self.quiz_hint.config(text=f"😅 应该是「{self.quiz_target['answer']}」哦！", fg="#FF6B6B")
            self.quiz_buttons[idx].config(bg="#808080")
            self.quiz_buttons[self.quiz_correct_idx].config(bg="#32CD32")
            self.speak_encourage()
        
        self.quiz_score_label.config(text=f"⭐ 得分: {self.quiz_score}")
        
        for btn in self.quiz_buttons:
            btn.config(state=tk.DISABLED)
        
        self.window.after(3000, self.new_rule_question)
    
    def quiz_speed(self):
        """快速反应游戏"""
        for widget in self.game_frame.winfo_children():
            widget.destroy()
        
        self.quiz_score = 0
        self.speed_time = 5.0  # 倒计时秒数
        self.speed_running = True
        
        tk.Label(self.game_frame, text="🎯 快速反应", font=("微软雅黑", 22, "bold"),
                 bg="#E8F5E9", fg="#9C27B0").pack(pady=5)
        
        self.quiz_score_label = tk.Label(self.game_frame, text="⭐ 得分: 0",
                                          font=("微软雅黑", 14), bg="#E8F5E9", fg="#666")
        self.quiz_score_label.pack(pady=5)
        
        # 倒计时
        self.speed_timer_label = tk.Label(self.game_frame, text="⏱️ 5.0",
                                           font=("Arial", 24, "bold"), bg="#E8F5E9", fg="#FF6B6B")
        self.speed_timer_label.pack(pady=5)
        
        # 目标显示
        self.speed_target_label = tk.Label(self.game_frame, text="", font=("微软雅黑", 18),
                                            bg="#E8F5E9", fg="#333")
        self.speed_target_label.pack(pady=10)
        
        self.quiz_hint = tk.Label(self.game_frame, text="", font=("微软雅黑", 14),
                                   bg="#E8F5E9", fg="#333")
        self.quiz_hint.pack(pady=5)
        
        # 选项 - 3x3网格
        self.quiz_options_frame = tk.Frame(self.game_frame, bg="#E8F5E9")
        self.quiz_options_frame.pack(pady=15)
        
        self.speed_buttons = []
        for i in range(9):
            btn = tk.Button(self.quiz_options_frame, text="", font=("Segoe UI Emoji", 35),
                           width=3, height=1, bg="#DDD", fg="white",
                           relief=tk.RAISED, bd=3, cursor="hand2",
                           command=lambda idx=i: self.check_speed_quiz(idx))
            btn.grid(row=i//3, column=i%3, padx=8, pady=8)
            self.speed_buttons.append(btn)
        
        self.new_speed_question()
    
    def new_speed_question(self):
        """生成新的快速反应问题"""
        if not self.speed_running:
            return
        
        self.speed_time = 5.0
        self.speed_answered = False
        
        # 选择目标
        all_vehicles = [v for v in self.vehicles_data]
        self.quiz_target = random.choice(all_vehicles)
        
        # 生成9个选项（包含1个正确答案）
        others = random.sample([v for v in all_vehicles if v != self.quiz_target], 8)
        options = [self.quiz_target] + others
        random.shuffle(options)
        self.speed_options = options
        self.quiz_correct_idx = options.index(self.quiz_target)
        
        # 显示目标
        self.speed_target_label.config(text=f"快找到：{self.quiz_target['name']} {self.quiz_target['emoji']}")
        
        # 更新按钮
        colors = ["#FF6B6B", "#4ECDC4", "#45B7D1", "#96CEB4", "#DDA0DD", "#FFD93D", "#FF9800", "#8BC34A", "#E91E63"]
        for i, btn in enumerate(self.speed_buttons):
            btn.config(text=options[i]["emoji"], bg=colors[i], state=tk.NORMAL)
        
        self.quiz_hint.config(text="", fg="#333")
        self.speak(f"快找到{self.quiz_target['name']}！")
        
        # 开始倒计时
        self.speed_countdown()
    
    def speed_countdown(self):
        """倒计时"""
        if not self.speed_running or self.speed_answered:
            return
        
        self.speed_time -= 0.1
        self.speed_timer_label.config(text=f"⏱️ {self.speed_time:.1f}")
        
        if self.speed_time <= 0:
            # 时间到
            self.speed_answered = True
            self.quiz_hint.config(text=f"⏰ 时间到！正确答案是 {self.quiz_target['emoji']}", fg="#FF6B6B")
            self.speed_buttons[self.quiz_correct_idx].config(bg="#32CD32")
            for btn in self.speed_buttons:
                btn.config(state=tk.DISABLED)
            self.window.after(2000, self.new_speed_question)
        else:
            self.window.after(100, self.speed_countdown)
    
    def check_speed_quiz(self, idx):
        """检查快速反应答案"""
        if self.speed_answered:
            return
        
        self.speed_answered = True
        
        if self.speed_options[idx] == self.quiz_target:
            # 根据剩余时间给分
            bonus = int(self.speed_time * 2)
            points = 10 + bonus
            self.quiz_score += points
            self.score += points
            self.quiz_hint.config(text=f"🎉 太快了！+{points}分！", fg="#32CD32")
            self.speed_buttons[idx].config(bg="#32CD32")
            self.speak_praise()
        else:
            self.quiz_hint.config(text=f"😅 不对哦！是 {self.quiz_target['emoji']}", fg="#FF6B6B")
            self.speed_buttons[idx].config(bg="#808080")
            self.speed_buttons[self.quiz_correct_idx].config(bg="#32CD32")
            self.speak_encourage()
        
        self.quiz_score_label.config(text=f"⭐ 得分: {self.quiz_score}")
        
        for btn in self.speed_buttons:
            btn.config(state=tk.DISABLED)
        
        self.window.after(2000, self.new_speed_question)

    # =====================================================
    # 游戏8: 车车拼图
    # =====================================================
    def start_vehicle_puzzle(self):
        self.clear_game_area("#FFF8E1")
        self.puzzle_score = 0
        
        # 获取当前狗狗信息
        pup = self.PAW_PATROL_GAMES.get("rex", {})
        
        tk.Label(self.game_frame, text=f"🧩 {pup.get('name', '小克')}的拼图", font=("微软雅黑", 26, "bold"),
                 bg="#FFF8E1", fg="#4ECDC4").pack(pady=10)
        
        tk.Label(self.game_frame, text="把打乱的图片拼回原样！点击两个方块交换位置",
                 font=("微软雅黑", 12), bg="#FFF8E1", fg="#666").pack()
        
        self.puzzle_score_label = tk.Label(self.game_frame, text="⭐ 得分: 0 | 步数: 0",
                                            font=("微软雅黑", 14), bg="#FFF8E1", fg="#666")
        self.puzzle_score_label.pack(pady=5)
        
        # 选择难度
        diff_frame = tk.Frame(self.game_frame, bg="#FFF8E1")
        diff_frame.pack(pady=10)
        
        tk.Label(diff_frame, text="选择难度：", font=("微软雅黑", 12),
                 bg="#FFF8E1", fg="#333").pack(side=tk.LEFT, padx=5)
        
        for text, size, color in [("简单 2x2", 2, "#96CEB4"), ("中等 3x3", 3, "#FFD93D"), ("困难 4x4", 4, "#FF6B6B")]:
            tk.Button(diff_frame, text=text, font=("微软雅黑", 11),
                     bg=color, fg="white", width=10,
                     command=lambda s=size: self.init_puzzle(s)).pack(side=tk.LEFT, padx=5)
        
        # 拼图画布
        self.puzzle_canvas = tk.Canvas(self.game_frame, width=400, height=400, bg="white",
                                        relief=tk.RAISED, bd=4)
        self.puzzle_canvas.pack(pady=15)
        self.puzzle_canvas.bind("<Button-1>", self.puzzle_click)
        
        self.puzzle_hint = tk.Label(self.game_frame, text="选择难度开始游戏！",
                                     font=("微软雅黑", 14), bg="#FFF8E1", fg="#333")
        self.puzzle_hint.pack(pady=5)
        
        self.speak(f"{pup.get('name', '小克')}说：选择难度开始拼图吧！")
    
    def init_puzzle(self, grid_size):
        """初始化拼图"""
        self.puzzle_size = grid_size
        self.puzzle_moves = 0
        self.puzzle_selected = None
        self.puzzle_complete = False
        
        # 选择一个交通工具
        vehicles = ["excavator", "race_car", "fire_truck", "airplane", "rocket", "train"]
        self.puzzle_vehicle = random.choice(vehicles)
        
        # 创建拼图块
        self.puzzle_pieces = list(range(grid_size * grid_size))
        
        # 打乱拼图（确保可解）
        for _ in range(100):
            i, j = random.sample(range(len(self.puzzle_pieces)), 2)
            self.puzzle_pieces[i], self.puzzle_pieces[j] = self.puzzle_pieces[j], self.puzzle_pieces[i]
        
        self.draw_puzzle()
        self.puzzle_hint.config(text="点击两个方块交换位置，拼出完整的图片！", fg="#333")
        self.speak("开始拼图！点击两个方块交换位置！")
    
    def draw_puzzle(self):
        """绘制拼图"""
        self.puzzle_canvas.delete("all")
        
        size = self.puzzle_size
        cell_size = 380 // size
        margin = 10
        
        for i, piece in enumerate(self.puzzle_pieces):
            row = i // size
            col = i % size
            
            x1 = margin + col * cell_size
            y1 = margin + row * cell_size
            x2 = x1 + cell_size - 2
            y2 = y1 + cell_size - 2
            
            # 计算原始位置
            orig_row = piece // size
            orig_col = piece % size
            
            # 根据位置选择颜色
            colors = ["#FF6B6B", "#4ECDC4", "#45B7D1", "#96CEB4", "#DDA0DD", "#FFD93D",
                     "#FF9800", "#8BC34A", "#E91E63", "#00BCD4", "#9C27B0", "#CDDC39",
                     "#FF5722", "#607D8B", "#795548", "#3F51B5"]
            color = colors[piece % len(colors)]
            
            # 绘制方块
            self.puzzle_canvas.create_rectangle(x1, y1, x2, y2, fill=color, outline="#333", width=2,
                                                 tags=f"piece_{i}")
            
            # 在方块上显示数字或图案
            cx = (x1 + x2) // 2
            cy = (y1 + y2) // 2
            
            # 显示数字
            self.puzzle_canvas.create_text(cx, cy, text=str(piece + 1),
                                           font=("Arial", cell_size // 3, "bold"), fill="white",
                                           tags=f"piece_{i}")
        
        # 检查是否完成
        if self.puzzle_pieces == list(range(size * size)):
            self.puzzle_complete = True
            self.puzzle_score += 100 - self.puzzle_moves
            self.score += 100 - self.puzzle_moves
            self.puzzle_hint.config(text=f"🎉 太棒了！完成拼图！用了{self.puzzle_moves}步！", fg="#32CD32")
            self.puzzle_score_label.config(text=f"⭐ 得分: {self.puzzle_score} | 步数: {self.puzzle_moves}")
            self.speak_praise()
    
    def puzzle_click(self, event):
        """处理拼图点击"""
        if self.puzzle_complete or not hasattr(self, 'puzzle_size'):
            return
        
        size = self.puzzle_size
        cell_size = 380 // size
        margin = 10
        
        # 计算点击的格子
        col = (event.x - margin) // cell_size
        row = (event.y - margin) // cell_size
        
        if 0 <= row < size and 0 <= col < size:
            idx = row * size + col
            
            if self.puzzle_selected is None:
                # 第一次选择
                self.puzzle_selected = idx
                self.highlight_piece(idx, True)
            else:
                # 第二次选择，交换
                if idx != self.puzzle_selected:
                    # 交换
                    self.puzzle_pieces[idx], self.puzzle_pieces[self.puzzle_selected] = \
                        self.puzzle_pieces[self.puzzle_selected], self.puzzle_pieces[idx]
                    self.puzzle_moves += 1
                    self.puzzle_score_label.config(text=f"⭐ 得分: {self.puzzle_score} | 步数: {self.puzzle_moves}")
                
                self.puzzle_selected = None
                self.draw_puzzle()
    
    def highlight_piece(self, idx, highlight):
        """高亮选中的方块"""
        size = self.puzzle_size
        cell_size = 380 // size
        margin = 10
        
        row = idx // size
        col = idx % size
        
        x1 = margin + col * cell_size
        y1 = margin + row * cell_size
        x2 = x1 + cell_size - 2
        y2 = y1 + cell_size - 2
        
        if highlight:
            self.puzzle_canvas.create_rectangle(x1-2, y1-2, x2+2, y2+2, outline="#FFD700", width=4,
                                                 tags="highlight")

    # =====================================================
    # 游戏9: 涂色乐园
    # =====================================================
    def start_coloring_game(self):
        self.clear_game_area("#FFFAF0")
        
        tk.Label(self.game_frame, text="🎨 汪汪队涂色乐园", font=("微软雅黑", 26, "bold"),
                 bg="#FFFAF0", fg="#FFD93D").pack(pady=5)
        
        tk.Label(self.game_frame, text="选择颜色，点击图片上的区域涂色！",
                 font=("微软雅黑", 12), bg="#FFFAF0", fg="#666").pack()
        
        # 选择交通工具
        vehicle_frame = tk.Frame(self.game_frame, bg="#FFFAF0")
        vehicle_frame.pack(pady=10)
        
        tk.Label(vehicle_frame, text="选择要涂色的车车：", font=("微软雅黑", 12),
                 bg="#FFFAF0", fg="#333").pack(side=tk.LEFT, padx=5)
        
        vehicles = [
            ("🏗️ 挖掘机", "excavator"),
            ("🏎️ 赛车", "race_car"),
            ("🚒 消防车", "fire_truck"),
            ("✈️ 飞机", "airplane"),
            ("🚀 火箭", "rocket"),
        ]
        
        for text, v_type in vehicles:
            tk.Button(vehicle_frame, text=text, font=("微软雅黑", 10),
                     bg="#E0E0E0", fg="#333", width=10,
                     command=lambda t=v_type: self.init_coloring(t)).pack(side=tk.LEFT, padx=3)
        
        # 颜色选择
        color_frame = tk.Frame(self.game_frame, bg="#FFFAF0")
        color_frame.pack(pady=10)
        
        tk.Label(color_frame, text="选择颜色：", font=("微软雅黑", 12),
                 bg="#FFFAF0", fg="#333").pack(side=tk.LEFT, padx=5)
        
        self.coloring_colors = [
            "#FF0000", "#FF9800", "#FFEB3B", "#4CAF50", "#2196F3", 
            "#9C27B0", "#E91E63", "#795548", "#000000", "#FFFFFF"
        ]
        
        self.color_buttons = []
        for color in self.coloring_colors:
            btn = tk.Button(color_frame, text="", width=3, height=1, bg=color,
                           relief=tk.RAISED, bd=2, cursor="hand2",
                           command=lambda c=color: self.select_color(c))
            btn.pack(side=tk.LEFT, padx=2)
            self.color_buttons.append(btn)
        
        self.current_color = "#FF0000"
        self.color_indicator = tk.Label(color_frame, text="  ", font=("Arial", 12),
                                         bg="#FF0000", width=4, relief=tk.SUNKEN, bd=2)
        self.color_indicator.pack(side=tk.LEFT, padx=10)
        
        # 涂色画布
        self.coloring_canvas = tk.Canvas(self.game_frame, width=500, height=350, bg="white",
                                          relief=tk.RAISED, bd=4)
        self.coloring_canvas.pack(pady=10)
        
        # 按钮
        btn_frame = tk.Frame(self.game_frame, bg="#FFFAF0")
        btn_frame.pack(pady=5)
        
        tk.Button(btn_frame, text="🔄 重新开始", font=("微软雅黑", 11),
                 bg="#FF6B6B", fg="white", command=lambda: self.init_coloring(self.coloring_vehicle)).pack(side=tk.LEFT, padx=10)
        tk.Button(btn_frame, text="💾 完成作品", font=("微软雅黑", 11),
                 bg="#4CAF50", fg="white", command=self.finish_coloring).pack(side=tk.LEFT, padx=10)
        
        self.coloring_hint = tk.Label(self.game_frame, text="选择一个车车开始涂色吧！",
                                       font=("微软雅黑", 14), bg="#FFFAF0", fg="#333")
        self.coloring_hint.pack(pady=5)
        
        self.coloring_vehicle = None
        self.coloring_regions = []
        
        self.speak("选择一个车车，然后选颜色涂色吧！")
    
    def select_color(self, color):
        """选择颜色"""
        self.current_color = color
        self.color_indicator.config(bg=color)
    
    def init_coloring(self, vehicle_type):
        """初始化涂色"""
        self.coloring_vehicle = vehicle_type
        self.coloring_canvas.delete("all")
        self.coloring_regions = []
        
        # 根据交通工具类型创建可涂色区域
        if vehicle_type == "excavator":
            self.create_excavator_coloring()
        elif vehicle_type == "race_car":
            self.create_race_car_coloring()
        elif vehicle_type == "fire_truck":
            self.create_fire_truck_coloring()
        elif vehicle_type == "airplane":
            self.create_airplane_coloring()
        elif vehicle_type == "rocket":
            self.create_rocket_coloring()
        
        self.coloring_hint.config(text="点击区域涂上你喜欢的颜色！", fg="#333")
        self.speak("开始涂色吧！")
    
    def create_excavator_coloring(self):
        """创建挖掘机涂色区域"""
        c = self.coloring_canvas
        cx, cy = 250, 200
        
        # 履带 - 可涂色区域1
        r1 = c.create_polygon(cx-80, cy+60, cx-90, cy+75, cx-90, cy+95, cx-80, cy+110,
                              cx+100, cy+110, cx+110, cy+95, cx+110, cy+75, cx+100, cy+60,
                              fill="#EEEEEE", outline="#333", width=3, tags="region_0")
        self.coloring_regions.append(r1)
        
        # 车身 - 可涂色区域2
        r2 = c.create_rectangle(cx-60, cy-20, cx+60, cy+55, fill="#EEEEEE", outline="#333", width=3, tags="region_1")
        self.coloring_regions.append(r2)
        
        # 驾驶室 - 可涂色区域3
        r3 = c.create_rectangle(cx-50, cy-80, cx+20, cy-20, fill="#EEEEEE", outline="#333", width=3, tags="region_2")
        self.coloring_regions.append(r3)
        
        # 窗户 - 可涂色区域4
        r4 = c.create_rectangle(cx-45, cy-75, cx+15, cy-35, fill="#EEEEEE", outline="#333", width=2, tags="region_3")
        self.coloring_regions.append(r4)
        
        # 大臂 - 可涂色区域5
        r5 = c.create_polygon(cx+20, cy-40, cx+30, cy-40, cx+120, cy-80, cx+115, cy-90,
                              fill="#EEEEEE", outline="#333", width=3, tags="region_4")
        self.coloring_regions.append(r5)
        
        # 铲斗 - 可涂色区域6
        r6 = c.create_polygon(cx+110, cy-85, cx+130, cy-85, cx+150, cy-50, cx+145, cy-40,
                              cx+115, cy-40, cx+100, cy-50,
                              fill="#EEEEEE", outline="#333", width=3, tags="region_5")
        self.coloring_regions.append(r6)
        
        # 绑定点击事件
        for i, region in enumerate(self.coloring_regions):
            c.tag_bind(f"region_{i}", "<Button-1>", lambda e, idx=i: self.color_region(idx))
    
    def create_race_car_coloring(self):
        """创建赛车涂色区域"""
        c = self.coloring_canvas
        cx, cy = 250, 180
        
        # 车身 - 可涂色区域1
        r1 = c.create_polygon(cx-100, cy+20, cx-80, cy-20, cx-40, cy-40, cx+40, cy-40,
                              cx+80, cy-20, cx+100, cy+20, cx+100, cy+40, cx-100, cy+40,
                              fill="#EEEEEE", outline="#333", width=3, smooth=True, tags="region_0")
        self.coloring_regions.append(r1)
        
        # 车窗 - 可涂色区域2
        r2 = c.create_polygon(cx-30, cy-35, cx+30, cy-35, cx+35, cy-10, cx-35, cy-10,
                              fill="#EEEEEE", outline="#333", width=2, tags="region_1")
        self.coloring_regions.append(r2)
        
        # 前轮 - 可涂色区域3
        r3 = c.create_oval(cx+50, cy+20, cx+90, cy+60, fill="#EEEEEE", outline="#333", width=3, tags="region_2")
        self.coloring_regions.append(r3)
        
        # 后轮 - 可涂色区域4
        r4 = c.create_oval(cx-90, cy+20, cx-50, cy+60, fill="#EEEEEE", outline="#333", width=3, tags="region_3")
        self.coloring_regions.append(r4)
        
        # 尾翼 - 可涂色区域5
        r5 = c.create_rectangle(cx-110, cy-50, cx-90, cy-30, fill="#EEEEEE", outline="#333", width=2, tags="region_4")
        self.coloring_regions.append(r5)
        
        # 绑定点击事件
        for i, region in enumerate(self.coloring_regions):
            c.tag_bind(f"region_{i}", "<Button-1>", lambda e, idx=i: self.color_region(idx))
    
    def create_fire_truck_coloring(self):
        """创建消防车涂色区域"""
        c = self.coloring_canvas
        cx, cy = 250, 180
        
        # 车身后部 - 可涂色区域1
        r1 = c.create_rectangle(cx-100, cy-20, cx-20, cy+40, fill="#EEEEEE", outline="#333", width=3, tags="region_0")
        self.coloring_regions.append(r1)
        
        # 驾驶室 - 可涂色区域2
        r2 = c.create_polygon(cx-20, cy+40, cx-20, cy-40, cx+60, cy-40, cx+70, cy+40,
                              fill="#EEEEEE", outline="#333", width=3, tags="region_1")
        self.coloring_regions.append(r2)
        
        # 车窗 - 可涂色区域3
        r3 = c.create_rectangle(cx-15, cy-35, cx+55, cy-10, fill="#EEEEEE", outline="#333", width=2, tags="region_2")
        self.coloring_regions.append(r3)
        
        # 云梯 - 可涂色区域4
        r4 = c.create_rectangle(cx-90, cy-50, cx+30, cy-30, fill="#EEEEEE", outline="#333", width=2, tags="region_3")
        self.coloring_regions.append(r4)
        
        # 前轮 - 可涂色区域5
        r5 = c.create_oval(cx+30, cy+30, cx+65, cy+65, fill="#EEEEEE", outline="#333", width=3, tags="region_4")
        self.coloring_regions.append(r5)
        
        # 后轮 - 可涂色区域6
        r6 = c.create_oval(cx-85, cy+30, cx-50, cy+65, fill="#EEEEEE", outline="#333", width=3, tags="region_5")
        self.coloring_regions.append(r6)
        
        # 绑定点击事件
        for i, region in enumerate(self.coloring_regions):
            c.tag_bind(f"region_{i}", "<Button-1>", lambda e, idx=i: self.color_region(idx))
    
    def create_airplane_coloring(self):
        """创建飞机涂色区域"""
        c = self.coloring_canvas
        cx, cy = 250, 175
        
        # 机身 - 可涂色区域1
        r1 = c.create_polygon(cx-120, cy, cx-100, cy-15, cx+80, cy-15, cx+120, cy,
                              cx+80, cy+15, cx-100, cy+15,
                              fill="#EEEEEE", outline="#333", width=3, smooth=True, tags="region_0")
        self.coloring_regions.append(r1)
        
        # 机头 - 可涂色区域2
        r2 = c.create_polygon(cx+100, cy-10, cx+130, cy, cx+100, cy+10,
                              fill="#EEEEEE", outline="#333", width=2, tags="region_1")
        self.coloring_regions.append(r2)
        
        # 上机翼 - 可涂色区域3
        r3 = c.create_polygon(cx-20, cy-15, cx+20, cy-15, cx+30, cy-70, cx-10, cy-70,
                              fill="#EEEEEE", outline="#333", width=2, tags="region_2")
        self.coloring_regions.append(r3)
        
        # 下机翼 - 可涂色区域4
        r4 = c.create_polygon(cx-20, cy+15, cx+20, cy+15, cx+30, cy+70, cx-10, cy+70,
                              fill="#EEEEEE", outline="#333", width=2, tags="region_3")
        self.coloring_regions.append(r4)
        
        # 尾翼 - 可涂色区域5
        r5 = c.create_polygon(cx-100, cy-10, cx-80, cy-10, cx-70, cy-50, cx-100, cy-50,
                              fill="#EEEEEE", outline="#333", width=2, tags="region_4")
        self.coloring_regions.append(r5)
        
        # 绑定点击事件
        for i, region in enumerate(self.coloring_regions):
            c.tag_bind(f"region_{i}", "<Button-1>", lambda e, idx=i: self.color_region(idx))
    
    def create_rocket_coloring(self):
        """创建火箭涂色区域"""
        c = self.coloring_canvas
        cx, cy = 250, 200
        
        # 火箭头 - 可涂色区域1
        r1 = c.create_polygon(cx, cy-120, cx-25, cy-60, cx+25, cy-60,
                              fill="#EEEEEE", outline="#333", width=3, tags="region_0")
        self.coloring_regions.append(r1)
        
        # 火箭身 - 可涂色区域2
        r2 = c.create_rectangle(cx-25, cy-60, cx+25, cy+60, fill="#EEEEEE", outline="#333", width=3, tags="region_1")
        self.coloring_regions.append(r2)
        
        # 左翼 - 可涂色区域3
        r3 = c.create_polygon(cx-25, cy+20, cx-60, cy+80, cx-25, cy+60,
                              fill="#EEEEEE", outline="#333", width=2, tags="region_2")
        self.coloring_regions.append(r3)
        
        # 右翼 - 可涂色区域4
        r4 = c.create_polygon(cx+25, cy+20, cx+60, cy+80, cx+25, cy+60,
                              fill="#EEEEEE", outline="#333", width=2, tags="region_3")
        self.coloring_regions.append(r4)
        
        # 窗户 - 可涂色区域5
        r5 = c.create_oval(cx-12, cy-40, cx+12, cy-15, fill="#EEEEEE", outline="#333", width=2, tags="region_4")
        self.coloring_regions.append(r5)
        
        # 火焰 - 可涂色区域6
        r6 = c.create_polygon(cx-20, cy+60, cx, cy+100, cx+20, cy+60,
                              fill="#EEEEEE", outline="#333", width=2, tags="region_5")
        self.coloring_regions.append(r6)
        
        # 绑定点击事件
        for i, region in enumerate(self.coloring_regions):
            c.tag_bind(f"region_{i}", "<Button-1>", lambda e, idx=i: self.color_region(idx))
    
    def color_region(self, idx):
        """给区域涂色"""
        if idx < len(self.coloring_regions):
            self.coloring_canvas.itemconfig(self.coloring_regions[idx], fill=self.current_color)
            self.speak("涂上颜色啦！")
    
    def finish_coloring(self):
        """完成涂色作品"""
        self.score += 50
        self.coloring_hint.config(text="🎉 太棒了！你的作品完成了！+50分！", fg="#32CD32")
        self.speak_praise()

    # =====================================================
    # 游戏10: 停车场游戏
    # =====================================================
    def start_parking_game(self):
        """停车场游戏 - 把车停进车位"""
        self.clear_game_area("#2C3E50")
        self.parking_score = 0
        self.parking_level = 1
        self.game_running = True
        
        # 获取当前狗狗信息
        pup = self.PAW_PATROL_GAMES.get("tracker", {})
        
        tk.Label(self.game_frame, text=f"🅿️ {pup.get('name', '阿克')}的停车场", font=("微软雅黑", 24, "bold"),
                 bg="#2C3E50", fg="#3498DB").pack(pady=5)
        
        tk.Label(self.game_frame, text="用方向键把车停进绿色车位！",
                 font=("微软雅黑", 12), bg="#2C3E50", fg="#AAA").pack()
        
        info_frame = tk.Frame(self.game_frame, bg="#2C3E50")
        info_frame.pack(pady=5)
        
        self.parking_score_label = tk.Label(info_frame, text="⭐ 得分: 0",
                 font=("微软雅黑", 12, "bold"), bg="#2C3E50", fg="#FFD700")
        self.parking_score_label.pack(side=tk.LEFT, padx=15)
        
        self.parking_level_label = tk.Label(info_frame, text="关卡: 1",
                 font=("微软雅黑", 12, "bold"), bg="#2C3E50", fg="#3498DB")
        self.parking_level_label.pack(side=tk.LEFT, padx=15)
        
        # 游戏画布
        self.parking_canvas = tk.Canvas(self.game_frame, width=600, height=450, 
                                        bg="#34495E", highlightthickness=2, highlightbackground="#1ABC9C")
        self.parking_canvas.pack(pady=10)
        
        self.parking_hint = tk.Label(self.game_frame, text="", font=("微软雅黑", 14),
                                     bg="#2C3E50", fg="#1ABC9C")
        self.parking_hint.pack(pady=5)
        
        # 绑定键盘
        self.window.bind("<Up>", self.parking_move_up)
        self.window.bind("<Down>", self.parking_move_down)
        self.window.bind("<Left>", self.parking_move_left)
        self.window.bind("<Right>", self.parking_move_right)
        
        self.init_parking_level()
        self.speak("把车停进绿色车位！用方向键控制！")
    
    def init_parking_level(self):
        """初始化停车关卡"""
        self.parking_canvas.delete("all")
        
        # 停车场地面
        self.parking_canvas.create_rectangle(0, 0, 600, 450, fill="#34495E", outline="")
        
        # 画停车线
        for i in range(5):
            x = 50 + i * 110
            self.parking_canvas.create_rectangle(x, 20, x+90, 120, outline="#FFF", width=2)
            self.parking_canvas.create_rectangle(x, 330, x+90, 430, outline="#FFF", width=2)
        
        # 目标车位（绿色）
        if self.parking_level == 1:
            self.target_x, self.target_y = 160, 330
        elif self.parking_level == 2:
            self.target_x, self.target_y = 380, 20
        else:
            self.target_x, self.target_y = 270, 330
        
        self.parking_canvas.create_rectangle(self.target_x, self.target_y, 
                                             self.target_x+90, self.target_y+100,
                                             fill="#27AE60", outline="#2ECC71", width=3)
        self.parking_canvas.create_text(self.target_x+45, self.target_y+50, 
                                        text="停这里", font=("微软雅黑", 12, "bold"), fill="white")
        
        # 障碍车辆
        self.obstacles = []
        if self.parking_level >= 2:
            obs_positions = [(50, 20), (270, 20), (50, 330), (380, 330)]
            for ox, oy in obs_positions[:self.parking_level]:
                if (ox, oy) != (self.target_x, self.target_y):
                    self.obstacles.append((ox, oy, ox+90, oy+100))
                    self.parking_canvas.create_rectangle(ox, oy, ox+90, oy+100, 
                                                        fill="#7F8C8D", outline="#95A5A6", width=2)
                    self.parking_canvas.create_text(ox+45, oy+50, text="🚙", 
                                                   font=("Segoe UI Emoji", 24))
        
        # 玩家车辆初始位置
        self.car_x = 270
        self.car_y = 200
        self.car_width = 70
        self.car_height = 40
        
        self.draw_parking_car()
        self.parking_hint.config(text=f"第 {self.parking_level} 关 - 把车停进绿色车位！", fg="#1ABC9C")
    
    def draw_parking_car(self):
        """绘制玩家车辆（俯视图）"""
        self.parking_canvas.delete("player_car")
        x, y = self.car_x, self.car_y
        w, h = self.car_width, self.car_height
        
        # 车身
        self.parking_canvas.create_rectangle(x-w//2, y-h//2, x+w//2, y+h//2,
                                            fill="#E74C3C", outline="#C0392B", width=2, tags="player_car")
        # 车窗
        self.parking_canvas.create_rectangle(x-w//4, y-h//3, x+w//4, y+h//3,
                                            fill="#85C1E9", outline="#5DADE2", tags="player_car")
        # 车轮
        for dx, dy in [(-w//2+8, -h//2-3), (-w//2+8, h//2+3), (w//2-8, -h//2-3), (w//2-8, h//2+3)]:
            self.parking_canvas.create_oval(x+dx-5, y+dy-8, x+dx+5, y+dy+8,
                                           fill="#2C3E50", outline="#1A252F", tags="player_car")
    
    def parking_move_up(self, event):
        if not self.game_running:
            return
        if self.car_y > 40:
            self.car_y -= 15
            self.draw_parking_car()
            self.check_parking()
    
    def parking_move_down(self, event):
        if not self.game_running:
            return
        if self.car_y < 410:
            self.car_y += 15
            self.draw_parking_car()
            self.check_parking()
    
    def parking_move_left(self, event):
        if not self.game_running:
            return
        if self.car_x > 50:
            self.car_x -= 15
            self.draw_parking_car()
            self.check_parking()
    
    def parking_move_right(self, event):
        if not self.game_running:
            return
        if self.car_x < 550:
            self.car_x += 15
            self.draw_parking_car()
            self.check_parking()
    
    def check_parking(self):
        """检查是否停好车"""
        # 检查是否撞到障碍物
        car_left = self.car_x - self.car_width // 2
        car_right = self.car_x + self.car_width // 2
        car_top = self.car_y - self.car_height // 2
        car_bottom = self.car_y + self.car_height // 2
        
        for ox1, oy1, ox2, oy2 in self.obstacles:
            if not (car_right < ox1 or car_left > ox2 or car_bottom < oy1 or car_top > oy2):
                self.parking_hint.config(text="💥 撞到了！小心一点！", fg="#E74C3C")
                self.speak("哎呀撞到了！")
                return
        
        # 检查是否停进车位
        target_cx = self.target_x + 45
        target_cy = self.target_y + 50
        
        if abs(self.car_x - target_cx) < 30 and abs(self.car_y - target_cy) < 40:
            self.game_running = False
            self.parking_score += 50 + (self.parking_level * 10)
            self.score += 50 + (self.parking_level * 10)
            
            # 检查成就
            if not hasattr(self, 'perfect_parks'):
                self.perfect_parks = 0
            self.perfect_parks += 1
            if self.perfect_parks >= 5:
                self.check_achievement("parking_master")
            
            self.parking_score_label.config(text=f"⭐ 得分: {self.parking_score}")
            self.parking_hint.config(text=f"🎉 完美停车！+{50 + self.parking_level * 10}分！", fg="#2ECC71")
            self.speak_praise()
            
            # 下一关
            if self.parking_level < 5:
                self.parking_level += 1
                self.window.after(2000, self.next_parking_level)
            else:
                self.window.after(2000, self.parking_complete)
    
    def next_parking_level(self):
        """进入下一关"""
        self.game_running = True
        self.parking_level_label.config(text=f"关卡: {self.parking_level}")
        self.init_parking_level()
        self.speak(f"第{self.parking_level}关开始！")
    
    def parking_complete(self):
        """完成所有关卡"""
        self.parking_canvas.create_rectangle(150, 150, 450, 300, fill="#2ECC71", outline="#27AE60", width=3)
        self.parking_canvas.create_text(300, 200, text="🏆 全部通关！", 
                                        font=("微软雅黑", 24, "bold"), fill="white")
        self.parking_canvas.create_text(300, 250, text=f"总分: {self.parking_score}", 
                                        font=("微软雅黑", 16), fill="white")
        self.show_game_complete(self.parking_score, "停车技术一流！")

    # =====================================================
    # 游戏11: 红绿灯过马路
    # =====================================================
    def start_traffic_light_game(self):
        """红绿灯过马路游戏"""
        self.clear_game_area("#87CEEB")
        self.traffic_score = 0
        self.traffic_round = 0
        self.traffic_light = "red"
        self.game_running = True
        self.person_y = 450
        self.person_moving = False
        
        # 获取当前狗狗信息
        pup = self.PAW_PATROL_GAMES.get("everest", {})
        
        tk.Label(self.game_frame, text=f"🚦 {pup.get('name', '珠珠')}的红绿灯", font=("微软雅黑", 24, "bold"),
                 bg="#87CEEB", fg="#E74C3C").pack(pady=5)
        
        tk.Label(self.game_frame, text="绿灯亮了才能过马路！红灯要停下来！",
                 font=("微软雅黑", 12), bg="#87CEEB", fg="#555").pack()
        
        info_frame = tk.Frame(self.game_frame, bg="#87CEEB")
        info_frame.pack(pady=5)
        
        self.traffic_score_label = tk.Label(info_frame, text="⭐ 得分: 0",
                 font=("微软雅黑", 12, "bold"), bg="#87CEEB", fg="#E74C3C")
        self.traffic_score_label.pack(side=tk.LEFT, padx=15)
        
        self.traffic_round_label = tk.Label(info_frame, text="第 1 轮",
                 font=("微软雅黑", 12, "bold"), bg="#87CEEB", fg="#3498DB")
        self.traffic_round_label.pack(side=tk.LEFT, padx=15)
        
        # 游戏画布
        self.traffic_canvas = tk.Canvas(self.game_frame, width=500, height=400, 
                                        bg="#87CEEB", highlightthickness=2, highlightbackground="#333")
        self.traffic_canvas.pack(pady=10)
        
        self.traffic_hint = tk.Label(self.game_frame, text="", font=("微软雅黑", 16, "bold"),
                                     bg="#87CEEB", fg="#333")
        self.traffic_hint.pack(pady=5)
        
        # 按钮
        btn_frame = tk.Frame(self.game_frame, bg="#87CEEB")
        btn_frame.pack(pady=10)
        
        self.walk_btn = tk.Button(btn_frame, text="🚶 走！过马路", font=("微软雅黑", 14, "bold"),
                                  bg="#2ECC71", fg="white", width=15, height=2,
                                  command=self.traffic_walk)
        self.walk_btn.pack(side=tk.LEFT, padx=10)
        
        self.stop_btn = tk.Button(btn_frame, text="🛑 停！等一等", font=("微软雅黑", 14, "bold"),
                                  bg="#E74C3C", fg="white", width=15, height=2,
                                  command=self.traffic_stop)
        self.stop_btn.pack(side=tk.LEFT, padx=10)
        
        self.draw_traffic_scene()
        self.new_traffic_round()
        self.speak("看红绿灯！绿灯走，红灯停！")
    
    def draw_traffic_scene(self):
        """绘制交通场景"""
        c = self.traffic_canvas
        c.delete("all")
        
        # 天空已经是背景色
        
        # 草地
        c.create_rectangle(0, 0, 500, 100, fill="#90EE90", outline="")
        c.create_rectangle(0, 300, 500, 400, fill="#90EE90", outline="")
        
        # 马路
        c.create_rectangle(0, 100, 500, 300, fill="#555", outline="")
        
        # 斑马线
        for i in range(10):
            x = 50 + i * 45
            c.create_rectangle(x, 100, x+30, 300, fill="white", outline="")
        
        # 红绿灯柱子
        c.create_rectangle(440, 50, 455, 150, fill="#333", outline="")
        
        # 红绿灯
        c.create_rectangle(430, 10, 480, 80, fill="#222", outline="#111", width=2)
        
        # 红灯
        self.red_light = c.create_oval(440, 15, 470, 45, fill="#440000", outline="#333")
        # 绿灯
        self.green_light = c.create_oval(440, 50, 470, 80, fill="#004400", outline="#333")
        
        # 小人
        self.draw_person()
        
        # 汽车（装饰）
        self.draw_traffic_car(100, 180, "left")
    
    def draw_person(self):
        """绘制小人"""
        c = self.traffic_canvas
        c.delete("person")
        y = self.person_y
        x = 250
        
        # 头
        c.create_oval(x-12, y-50, x+12, y-26, fill="#FFDAB9", outline="#DEB887", width=2, tags="person")
        # 身体
        c.create_rectangle(x-10, y-26, x+10, y, fill="#3498DB", outline="#2980B9", width=2, tags="person")
        # 腿
        c.create_rectangle(x-8, y, x-2, y+20, fill="#2C3E50", outline="#1A252F", tags="person")
        c.create_rectangle(x+2, y, x+8, y+20, fill="#2C3E50", outline="#1A252F", tags="person")
        # 眼睛
        c.create_oval(x-6, y-44, x-2, y-38, fill="black", tags="person")
        c.create_oval(x+2, y-44, x+6, y-38, fill="black", tags="person")
        # 笑脸
        c.create_arc(x-6, y-40, x+6, y-32, start=200, extent=140, style="arc", outline="black", width=2, tags="person")
    
    def draw_traffic_car(self, x, y, direction):
        """绘制马路上的汽车"""
        c = self.traffic_canvas
        c.delete("car")
        
        if direction == "left":
            # 车身
            c.create_rectangle(x-40, y-15, x+40, y+15, fill="#E74C3C", outline="#C0392B", width=2, tags="car")
            # 车窗
            c.create_rectangle(x-20, y-12, x+15, y+12, fill="#85C1E9", outline="#5DADE2", tags="car")
            # 车轮
            c.create_oval(x-30, y+12, x-15, y+25, fill="#2C3E50", outline="#1A252F", tags="car")
            c.create_oval(x+15, y+12, x+30, y+25, fill="#2C3E50", outline="#1A252F", tags="car")
    
    def new_traffic_round(self):
        """新一轮红绿灯"""
        if not self.game_running:
            return
        
        self.traffic_round += 1
        self.traffic_round_label.config(text=f"第 {self.traffic_round} 轮")
        self.person_y = 350
        self.person_moving = False
        self.draw_person()
        
        # 随机红绿灯
        self.traffic_light = random.choice(["red", "green", "green", "green"])  # 绿灯概率更高
        
        c = self.traffic_canvas
        if self.traffic_light == "red":
            c.itemconfig(self.red_light, fill="#FF0000")
            c.itemconfig(self.green_light, fill="#004400")
            self.traffic_hint.config(text="🔴 红灯！应该怎么做？", fg="#E74C3C")
        else:
            c.itemconfig(self.red_light, fill="#440000")
            c.itemconfig(self.green_light, fill="#00FF00")
            self.traffic_hint.config(text="🟢 绿灯！应该怎么做？", fg="#27AE60")
        
        self.walk_btn.config(state=tk.NORMAL)
        self.stop_btn.config(state=tk.NORMAL)
        
        # 语音提示
        if self.traffic_light == "red":
            self.speak("红灯亮了！")
        else:
            self.speak("绿灯亮了！")
    
    def traffic_walk(self):
        """选择过马路"""
        self.walk_btn.config(state=tk.DISABLED)
        self.stop_btn.config(state=tk.DISABLED)
        
        if self.traffic_light == "green":
            # 正确！绿灯可以走
            self.traffic_score += 10
            self.score += 10
            self.traffic_score_label.config(text=f"⭐ 得分: {self.traffic_score}")
            self.traffic_hint.config(text="🎉 对啦！绿灯可以安全过马路！", fg="#27AE60")
            
            # 检查成就
            if not hasattr(self, 'traffic_correct'):
                self.traffic_correct = 0
            self.traffic_correct += 1
            if self.traffic_correct >= 10:
                self.check_achievement("traffic_expert")
            
            self.speak_praise()
            self.animate_crossing()
        else:
            # 错误！红灯不能走
            self.traffic_hint.config(text="😱 危险！红灯不能过马路！", fg="#E74C3C")
            self.speak("红灯停！不能过马路！")
            self.window.after(2500, self.new_traffic_round)
    
    def traffic_stop(self):
        """选择停下等待"""
        self.walk_btn.config(state=tk.DISABLED)
        self.stop_btn.config(state=tk.DISABLED)
        
        if self.traffic_light == "red":
            # 正确！红灯要停
            self.traffic_score += 10
            self.score += 10
            self.traffic_score_label.config(text=f"⭐ 得分: {self.traffic_score}")
            self.traffic_hint.config(text="🎉 对啦！红灯要停下来等待！", fg="#27AE60")
            
            if not hasattr(self, 'traffic_correct'):
                self.traffic_correct = 0
            self.traffic_correct += 1
            if self.traffic_correct >= 10:
                self.check_achievement("traffic_expert")
            
            self.speak_praise()
            self.window.after(2000, self.new_traffic_round)
        else:
            # 绿灯可以走的
            self.traffic_hint.config(text="🤔 绿灯亮了，可以安全过马路哦！", fg="#F39C12")
            self.speak("绿灯可以走哦！")
            self.window.after(2500, self.new_traffic_round)
    
    def animate_crossing(self):
        """动画：小人过马路"""
        if self.person_y > 50:
            self.person_y -= 10
            self.draw_person()
            self.window.after(100, self.animate_crossing)
        else:
            self.traffic_hint.config(text="✅ 安全到达！", fg="#27AE60")
            self.window.after(1500, self.new_traffic_round)


    # =====================================================
    # 运行
    # =====================================================
    def run(self):
        self.window.mainloop()


if __name__ == "__main__":
    app = KidsVehiclesApp()
    app.run()
