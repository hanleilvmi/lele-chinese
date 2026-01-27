# -*- coding: utf-8 -*-
"""
Kivy 音频模块
支持 Windows 和 Android 平台
使用 edge_tts + Kivy SoundLoader
"""
import os
import sys
import threading
import random
import tempfile
import uuid
import time

# 在导入任何网络库之前禁用代理
for key in list(os.environ.keys()):
    if 'proxy' in key.lower():
        del os.environ[key]
os.environ['NO_PROXY'] = '*'
os.environ['no_proxy'] = '*'

sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from core.audio_interface import AudioInterface

# 检测平台
PLATFORM = 'desktop'
ANDROID_TTS = None

try:
    from jnius import autoclass
    TTS = autoclass('android.speech.tts.TextToSpeech')
    Activity = autoclass('org.kivy.android.PythonActivity')
    Locale = autoclass('java.util.Locale')
    PLATFORM = 'android'
    ANDROID_TTS = True
    print("检测到 Android 平台")
except ImportError:
    print("非 Android 平台，使用桌面模式")

# Kivy 音频
from kivy.core.audio import SoundLoader

# 尝试导入 edge_tts
EDGE_TTS_AVAILABLE = False
edge_tts = None

if PLATFORM == 'desktop':
    try:
        import edge_tts as _edge_tts
        edge_tts = _edge_tts
        EDGE_TTS_AVAILABLE = True
        print("使用 edge_tts 语音引擎")
    except ImportError as e:
        print(f"edge_tts 不可用: {e}")

# 导入语音配置
try:
    sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
    from voice_config_shared import get_voice, get_praises, get_encourages
    VOICE_CONFIG_AVAILABLE = True
except ImportError:
    VOICE_CONFIG_AVAILABLE = False
    def get_voice():
        return "zh-CN-XiaoyiNeural"
    def get_praises():
        return ['太棒了', '真厉害', '做得好', '你真聪明', '好厉害']
    def get_encourages():
        return ['再试一次', '没关系', '加油', '你可以的']


class KivyAudio(AudioInterface):
    """Kivy 音频实现 - 使用 Kivy SoundLoader"""
    
    def __init__(self):
        self.platform = PLATFORM
        self.tts = None
        self.tts_ready = False
        self.temp_dir = None
        self.speech_id = 0
        self.current_sound = None
        self.tts_lock = threading.Lock()
        
        # 安全创建临时目录
        try:
            self.temp_dir = tempfile.mkdtemp()
        except Exception as e:
            print(f"创建临时目录失败: {e}")
            self.temp_dir = None
        
        # 初始化TTS - 延迟初始化Android TTS
        if self.platform == 'android' and ANDROID_TTS:
            # Android TTS需要延迟初始化，等Activity准备好
            from kivy.clock import Clock
            Clock.schedule_once(self._init_android_tts, 1.0)
        elif EDGE_TTS_AVAILABLE:
            self.tts_ready = True
            print("Edge TTS 初始化成功")
        else:
            # 使用 pyttsx3 作为后备
            try:
                import pyttsx3
                self.tts = pyttsx3.init()
                voices = self.tts.getProperty('voices')
                for voice in voices:
                    if 'chinese' in voice.name.lower() or 'zh' in voice.id.lower():
                        self.tts.setProperty('voice', voice.id)
                        break
                self.tts.setProperty('rate', 180)
                self.tts_ready = True
                print("pyttsx3 TTS 初始化成功")
            except Exception as e:
                print(f"TTS 初始化失败: {e}")
    
    def _init_android_tts(self, dt):
        """延迟初始化Android TTS"""
        try:
            if Activity.mActivity is not None:
                # 创建TTS实例
                self.tts = TTS(Activity.mActivity, None)
                
                # 尝试设置中文语言
                try:
                    # 尝试简体中文
                    result = self.tts.setLanguage(Locale.SIMPLIFIED_CHINESE)
                    if result < 0:
                        # 如果失败，尝试CHINESE
                        result = self.tts.setLanguage(Locale.CHINESE)
                    if result < 0:
                        # 如果还失败，尝试用字符串创建Locale
                        zh_locale = Locale("zh", "CN")
                        self.tts.setLanguage(zh_locale)
                except Exception as e:
                    print(f"设置TTS语言失败: {e}")
                    # 使用默认语言
                    pass
                
                self.tts_ready = True
                print("Android TTS 初始化成功")
            else:
                print("Activity未准备好，稍后重试")
                from kivy.clock import Clock
                Clock.schedule_once(self._init_android_tts, 1.0)
        except Exception as e:
            print(f"Android TTS 初始化失败: {e}")
            # 重试几次
            if not hasattr(self, '_tts_retry_count'):
                self._tts_retry_count = 0
            self._tts_retry_count += 1
            if self._tts_retry_count < 5:
                from kivy.clock import Clock
                Clock.schedule_once(self._init_android_tts, 2.0)
            else:
                self.tts_ready = False
    
    def speak(self, text: str, rate: str = "+0%"):
        """朗读文字（异步）"""
        if not self.tts_ready:
            print(f"TTS未就绪，无法播放: {text}")
            return
        
        # Android/鸿蒙：直接在主线程调用TTS
        if self.platform == 'android' and ANDROID_TTS and self.tts:
            try:
                # 使用Clock确保在主线程执行
                from kivy.clock import Clock
                Clock.schedule_once(lambda dt: self._android_speak(text), 0)
                return
            except Exception as e:
                print(f"Android TTS调度失败: {e}")
                return
        
        # 停止当前播放
        if self.current_sound:
            try:
                self.current_sound.stop()
            except:
                pass
            self.current_sound = None
        
        self.speech_id += 1
        current_id = self.speech_id
        
        # 在后台线程生成语音（桌面平台）
        t = threading.Thread(target=self._speak_thread, args=(text, rate, current_id), daemon=True)
        t.start()
    
    def _android_speak(self, text):
        """Android TTS播放（主线程）"""
        try:
            if self.tts and self.tts_ready:
                self.tts.speak(text, TTS.QUEUE_FLUSH, None, None)
                print(f"Android TTS播放: {text}")
        except Exception as e:
            print(f"Android TTS播放失败: {e}")
    
    def _speak_thread(self, text: str, rate: str, speech_id: int):
        """语音生成和播放线程"""
        # 完全禁用代理
        import os as os_module
        for key in list(os_module.environ.keys()):
            if 'proxy' in key.lower():
                del os_module.environ[key]
        os_module.environ['NO_PROXY'] = '*'
        os_module.environ['no_proxy'] = '*'
        
        try:
            # 检查是否被取消
            if speech_id != self.speech_id:
                print(f"[_speak_thread] 已取消")
                return
            
            if self.platform == 'android' and ANDROID_TTS:
                try:
                    self.tts.speak(text, TTS.QUEUE_FLUSH, None, None)
                except Exception as e:
                    print(f"Android TTS 播放失败: {e}")
                return
            
            if EDGE_TTS_AVAILABLE:
                audio_file = os.path.join(self.temp_dir, f"tts_{uuid.uuid4().hex}.mp3")
                voice = get_voice()
                
                # 使用 asyncio 生成语音
                import asyncio
                
                async def generate():
                    communicate = edge_tts.Communicate(text, voice, rate=rate)
                    await communicate.save(audio_file)
                
                # 创建新的事件循环
                loop = asyncio.new_event_loop()
                asyncio.set_event_loop(loop)
                try:
                    loop.run_until_complete(generate())
                finally:
                    loop.close()
                
                # 使用 Kivy 播放音频（需要在主线程）
                if os.path.exists(audio_file):
                    from kivy.clock import Clock
                    Clock.schedule_once(lambda dt, f=audio_file: self._play_audio(f, speech_id), 0)
            
            elif self.tts:
                # pyttsx3 后备
                with self.tts_lock:
                    self.tts.say(text)
                    self.tts.runAndWait()
        
        except Exception as e:
            pass  # 静默处理错误
    
    def _play_audio(self, audio_file: str, speech_id: int):
        """在主线程播放音频"""
        try:
            # 停止之前的播放
            if self.current_sound:
                try:
                    self.current_sound.stop()
                except:
                    pass
            
            # 加载并播放
            sound = SoundLoader.load(audio_file)
            if sound:
                self.current_sound = sound
                sound.bind(on_stop=lambda s: self._on_sound_stop(audio_file))
                sound.play()
            else:
                self._cleanup_file(audio_file)
        except Exception as e:
            self._cleanup_file(audio_file)
    
    def _on_sound_stop(self, audio_file: str):
        """音频播放完成回调"""
        from kivy.clock import Clock
        Clock.schedule_once(lambda dt: self._cleanup_file(audio_file), 0.5)
    
    def _cleanup_file(self, filepath):
        """清理临时文件"""
        try:
            if filepath and os.path.exists(filepath):
                os.remove(filepath)
        except:
            pass
    
    def play_praise(self):
        """播放表扬语音"""
        praises = get_praises()
        self.speak(random.choice(praises), "+10%")
    
    def play_encourage(self):
        """播放鼓励语音"""
        encourages = get_encourages()
        self.speak(random.choice(encourages))
    
    def play_sound(self, sound_name: str):
        """播放音效"""
        # 音效文件路径
        base_dir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
        sound_paths = {
            'correct': os.path.join(base_dir, 'audio/effects/correct.wav'),
            'wrong': os.path.join(base_dir, 'audio/effects/wrong.wav'),
            'click': os.path.join(base_dir, 'audio/effects/click.wav'),
            'win': os.path.join(base_dir, 'audio/effects/win.wav'),
        }
        
        path = sound_paths.get(sound_name)
        if not path or not os.path.exists(path):
            return
        
        try:
            sound = SoundLoader.load(path)
            if sound:
                sound.play()
        except Exception as e:
            print(f"音效播放失败: {e}")
    
    def stop(self):
        """停止播放"""
        self.speech_id += 1  # 取消当前播放
        
        if self.current_sound:
            try:
                self.current_sound.stop()
            except:
                pass
            self.current_sound = None
    
    def cleanup(self):
        """清理临时文件"""
        import shutil
        try:
            shutil.rmtree(self.temp_dir, ignore_errors=True)
        except:
            pass


# 全局音频实例
_audio_instance = None

def get_audio():
    """获取音频实例（单例）"""
    global _audio_instance
    if _audio_instance is None:
        _audio_instance = KivyAudio()
    return _audio_instance
