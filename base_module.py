# -*- coding: utf-8 -*-
"""
基础模块类 v1.0
所有学习模块的基类，提供统一的功能：
- 语音系统
- 窗口管理
- 定时器管理
- 临时文件清理
"""

import tkinter as tk
from tkinter import messagebox
import threading
import asyncio
import os
import tempfile
import uuid
import time
import atexit
import logging

# 配置日志
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger('LearningApp')

# 导入依赖
try:
    import edge_tts
    import pygame
    pygame.mixer.init()
    TTS_AVAILABLE = True
except ImportError:
    TTS_AVAILABLE = False
    logger.warning("edge-tts 或 pygame 未安装，语音功能不可用")

try:
    from ui_config import UI, Colors, ScreenConfig, get_path, get_data_path, IS_MOBILE
    UI_CONFIG_AVAILABLE = True
except ImportError:
    UI_CONFIG_AVAILABLE = False
    IS_MOBILE = False

try:
    from voice_config_shared import get_voice, get_praises, get_encourages
    VOICE_CONFIG_AVAILABLE = True
except ImportError:
    VOICE_CONFIG_AVAILABLE = False


class TempFileManager:
    """临时文件管理器 - 确保临时文件被正确清理"""
    
    _instance = None
    _lock = threading.Lock()
    
    def __new__(cls):
        with cls._lock:
            if cls._instance is None:
                cls._instance = super().__new__(cls)
                cls._instance._initialized = False
            return cls._instance
    
    def __init__(self):
        if self._initialized:
            return
        self._initialized = True
        self._files = set()
        self._lock = threading.Lock()
        atexit.register(self.cleanup_all)
    
    def register(self, filepath):
        """注册临时文件"""
        with self._lock:
            self._files.add(filepath)
    
    def unregister(self, filepath):
        """取消注册并删除文件"""
        with self._lock:
            self._files.discard(filepath)
        self._safe_delete(filepath)
    
    def _safe_delete(self, filepath):
        """安全删除文件"""
        try:
            if filepath and os.path.exists(filepath):
                os.remove(filepath)
                logger.debug(f"已删除临时文件: {filepath}")
        except Exception as e:
            logger.warning(f"删除临时文件失败: {filepath}, 错误: {e}")
    
    def cleanup_all(self):
        """清理所有临时文件"""
        with self._lock:
            files_to_delete = list(self._files)
            self._files.clear()
        
        for filepath in files_to_delete:
            self._safe_delete(filepath)
        
        logger.info(f"已清理 {len(files_to_delete)} 个临时文件")


# 全局临时文件管理器
temp_manager = TempFileManager()


class AudioManager:
    """音频管理器 - 统一管理语音和音效"""
    
    def __init__(self):
        self.tts_available = TTS_AVAILABLE
        self.voice = get_voice() if VOICE_CONFIG_AVAILABLE else "zh-CN-YunxiNeural"
        self.praises = get_praises() if VOICE_CONFIG_AVAILABLE else ["太棒了！", "真厉害！"]
        self.encourages = get_encourages() if VOICE_CONFIG_AVAILABLE else ["加油！", "再试试！"]
        
        self.temp_dir = tempfile.gettempdir()
        self.speech_id = 0
        self.speech_lock = threading.Lock()
        self.is_playing = False
        
        # 音频文件夹
        if UI_CONFIG_AVAILABLE:
            self.audio_dir = get_path("audio")
        else:
            self.audio_dir = os.path.join(os.path.dirname(os.path.abspath(__file__)), "audio")
        
        # 扫描预录音频
        self.praise_audios = self._scan_audio_folder("praise")
        self.encourage_audios = self._scan_audio_folder("encourage")
    
    def _scan_audio_folder(self, folder_name):
        """扫描音频文件夹"""
        folder_path = os.path.join(self.audio_dir, folder_name)
        if not os.path.exists(folder_path):
            return []
        
        audio_files = []
        for f in os.listdir(folder_path):
            if f.lower().endswith(('.mp3', '.wav', '.ogg')):
                audio_files.append(os.path.join(folder_path, f))
        return audio_files
    
    def speak(self, text, rate="+0%", callback=None, lang="cn"):
        """异步播放语音"""
        if not self.tts_available:
            logger.warning("TTS 不可用")
            return
        
        with self.speech_lock:
            self.speech_id += 1
            current_id = self.speech_id
        
        # 停止当前播放
        self._stop_current()
        
        # 选择语音
        if lang == "en":
            voice = "en-US-AnaNeural"
        else:
            voice = self.voice
        
        # 在新线程中播放
        thread = threading.Thread(
            target=self._speak_thread,
            args=(text, rate, current_id, callback, voice),
            daemon=True
        )
        thread.start()
        thread.start()
    
    def _speak_thread(self, text, rate, speech_id, callback=None, voice=None):
        """语音播放线程"""
        if voice is None:
            voice = self.voice
        audio_file = None
        try:
            # 检查是否被取消
            with self.speech_lock:
                if speech_id != self.speech_id:
                    return
            
            # 生成音频文件
            audio_file = os.path.join(self.temp_dir, f"tts_{uuid.uuid4().hex}.mp3")
            temp_manager.register(audio_file)
            
            # 异步生成语音
            async def generate():
                communicate = edge_tts.Communicate(text, voice, rate=rate)
                await communicate.save(audio_file)
            
            asyncio.run(generate())
            
            # 再次检查是否被取消
            with self.speech_lock:
                if speech_id != self.speech_id:
                    return
            
            # 检查文件是否生成成功
            if not os.path.exists(audio_file):
                logger.error(f"音频文件生成失败: {audio_file}")
                return
            
            # 播放音频
            self._stop_current()
            pygame.mixer.music.load(audio_file)
            pygame.mixer.music.play()
            
            # 等待播放完成
            while pygame.mixer.music.get_busy():
                with self.speech_lock:
                    if speech_id != self.speech_id:
                        pygame.mixer.music.stop()
                        break
                time.sleep(0.1)
            
            # 回调
            if callback:
                callback()
                
        except Exception as e:
            logger.error(f"语音播放错误: {e}")
        finally:
            # 清理临时文件
            if audio_file:
                time.sleep(0.1)  # 等待文件释放
                temp_manager.unregister(audio_file)
    
    def _stop_current(self):
        """停止当前播放"""
        try:
            if pygame.mixer.music.get_busy():
                pygame.mixer.music.stop()
        except Exception as e:
            logger.warning(f"停止播放失败: {e}")
    
    def play_praise(self):
        """播放表扬语"""
        import random
        if self.praise_audios:
            self._play_audio_file(random.choice(self.praise_audios))
        else:
            self.speak(random.choice(self.praises), "+10%")
    
    def play_encourage(self):
        """播放鼓励语"""
        import random
        if self.encourage_audios:
            self._play_audio_file(random.choice(self.encourage_audios))
        else:
            self.speak(random.choice(self.encourages), "+0%")
    
    def _play_audio_file(self, filepath):
        """播放音频文件"""
        def _play():
            try:
                self._stop_current()
                pygame.mixer.music.load(filepath)
                pygame.mixer.music.play()
            except Exception as e:
                logger.error(f"播放音频文件失败: {e}")
        
        threading.Thread(target=_play, daemon=True).start()
    
    def stop(self):
        """停止所有音频"""
        with self.speech_lock:
            self.speech_id += 1
        self._stop_current()


class BaseGameModule:
    """游戏模块基类"""
    
    # 模块名称（子类需要覆盖）
    MODULE_NAME = "base"
    MODULE_TITLE = "基础模块"
    MODULE_COLOR = "#FF6B6B"
    
    def __init__(self):
        self.window = tk.Tk()
        self.window.title(f"🎈 {self.MODULE_TITLE} 🎈")
        
        # 设置窗口大小
        self._setup_window()
        
        # 初始化组件
        self.audio = AudioManager()
        self.pending_timers = []
        self.score = 0
        self.game_frame = None
        
        # 设置关闭处理
        self.window.protocol("WM_DELETE_WINDOW", self.on_close_window)
        atexit.register(self.cleanup_on_exit)
    
    def _setup_window(self):
        """设置窗口"""
        if UI_CONFIG_AVAILABLE:
            w, h = ScreenConfig.get_window_size()
            if w and h:
                window_width, window_height = w, h
            else:
                window_width = self.window.winfo_screenwidth()
                window_height = self.window.winfo_screenheight()
        else:
            window_width = 1050
            window_height = 800
        
        screen_width = self.window.winfo_screenwidth()
        screen_height = self.window.winfo_screenheight()
        x = (screen_width - window_width) // 2
        y = (screen_height - window_height) // 2 - 30
        self.window.geometry(f"{window_width}x{window_height}+{x}+{y}")
        
        self.window_width = window_width
        self.window_height = window_height
    
    def on_close_window(self):
        """窗口关闭处理"""
        result = messagebox.askyesno(
            "👋 确认退出",
            f"确定要退出{self.MODULE_TITLE}吗？",
            icon='question',
            default='yes'
        )
        if result:
            self.cleanup_on_exit()
            self.window.quit()
    
    def cleanup_on_exit(self):
        """退出时清理"""
        try:
            # 取消所有定时器
            for timer_id in self.pending_timers:
                try:
                    self.window.after_cancel(timer_id)
                except:
                    pass
            self.pending_timers.clear()
            
            # 停止音频
            self.audio.stop()
            
            logger.info(f"{self.MODULE_TITLE} 已清理退出")
        except Exception as e:
            logger.error(f"清理错误: {e}")
    
    def safe_after(self, delay, callback):
        """安全的定时器调用"""
        timer_id = self.window.after(delay, callback)
        self.pending_timers.append(timer_id)
        return timer_id
    
    def cancel_timer(self, timer_id):
        """取消定时器"""
        try:
            self.window.after_cancel(timer_id)
            if timer_id in self.pending_timers:
                self.pending_timers.remove(timer_id)
        except:
            pass
    
    def speak(self, text, rate="+0%", lang="cn"):
        """播放语音"""
        self.audio.speak(text, rate, lang=lang)
    
    def speak_praise(self):
        """播放表扬"""
        self.audio.play_praise()
        self.play_correct_animation()
    
    def speak_encourage(self):
        """播放鼓励"""
        self.audio.play_encourage()
    
    def play_correct_animation(self):
        """播放答对动画 - 星星和爱心特效"""
        try:
            import math
            import random
            
            # 在游戏画布上显示庆祝效果
            if hasattr(self, 'game_frame') and self.game_frame:
                for child in self.game_frame.winfo_children():
                    if isinstance(child, tk.Canvas):
                        canvas = child
                        cw = canvas.winfo_width()
                        ch = canvas.winfo_height()
                        if cw < 100:
                            continue
                        
                        # 添加庆祝文字
                        items = []
                        items.append(canvas.create_text(cw//2, ch//2, text="⭐ 太棒了！⭐", 
                                    font=("微软雅黑", 28, "bold"), fill="#FFD700", tags="celebration"))
                        
                        # 周围添加星星和爱心
                        for _ in range(8):
                            sx = random.randint(50, cw-50)
                            sy = random.randint(50, ch-50)
                            emoji = random.choice(["⭐", "🌟", "❤️", "💖", "✨"])
                            star = canvas.create_text(sx, sy, text=emoji, 
                                    font=("Segoe UI Emoji", random.randint(18, 32)), tags="celebration")
                            items.append(star)
                        
                        # 1.2秒后清除
                        def clear_celebration():
                            try:
                                canvas.delete("celebration")
                            except:
                                pass
                        canvas.after(1200, clear_celebration)
                        break
        except Exception as e:
            logger.debug(f"动画效果错误: {e}")
    
    def play_celebration_effect(self, canvas):
        """在指定画布上播放庆祝效果"""
        try:
            import random
            cw = canvas.winfo_width()
            ch = canvas.winfo_height()
            if cw < 100:
                return
            
            # 添加庆祝元素
            canvas.create_text(cw//2, ch//2 - 20, text="🎉 太棒了！🎉", 
                        font=("微软雅黑", 26, "bold"), fill="#FFD700", tags="celebration")
            
            for _ in range(6):
                sx = random.randint(80, cw-80)
                sy = random.randint(80, ch-80)
                emoji = random.choice(["⭐", "🌟", "💫", "✨"])
                canvas.create_text(sx, sy, text=emoji, 
                        font=("Segoe UI Emoji", random.randint(20, 35)), tags="celebration")
            
            # 1.5秒后清除
            canvas.after(1500, lambda: canvas.delete("celebration"))
        except Exception as e:
            logger.debug(f"庆祝效果错误: {e}")
    
    def clear_game_area(self, bg_color="#FFF8E1"):
        """清空游戏区域"""
        # 清理定时器
        for timer_id in self.pending_timers:
            try:
                self.window.after_cancel(timer_id)
            except:
                pass
        self.pending_timers.clear()
        
        # 清空窗口
        for widget in self.window.winfo_children():
            widget.destroy()
        
        self.window.configure(bg=bg_color)
        
        # 创建导航栏
        nav_frame = tk.Frame(self.window, bg=bg_color)
        nav_frame.pack(fill=tk.X, pady=5)
        
        tk.Button(
            nav_frame, text="🏠 返回主菜单",
            font=("微软雅黑", 11), bg="#96CEB4", fg="white",
            relief=tk.RAISED, bd=3, cursor="hand2",
            command=self.create_main_menu
        ).pack(side=tk.LEFT, padx=10)
        
        tk.Label(
            nav_frame, text=f"⭐ 总分: {self.score}",
            font=("微软雅黑", 12, "bold"), bg=bg_color, fg="#FF6B6B"
        ).pack(side=tk.RIGHT, padx=10)
        
        # 创建游戏区域
        self.game_frame = tk.Frame(self.window, bg=bg_color)
        self.game_frame.pack(fill=tk.BOTH, expand=True, padx=20, pady=10)
    
    def create_main_menu(self):
        """创建主菜单（子类需要覆盖）"""
        raise NotImplementedError("子类必须实现 create_main_menu 方法")
    
    def run(self):
        """运行应用"""
        self.create_main_menu()
        self.window.mainloop()


# 导出
__all__ = [
    'BaseGameModule',
    'AudioManager', 
    'TempFileManager',
    'temp_manager',
    'logger',
    'TTS_AVAILABLE',
    'UI_CONFIG_AVAILABLE',
    'IS_MOBILE'
]
