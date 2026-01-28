# -*- coding: utf-8 -*-
"""
Kivy 音频模块 v2.1
支持 Windows / Android / 鸿蒙 平台
修复：Android TTS初始化和播放问题
"""
import os
import sys
import threading
import random
import tempfile
import uuid

# 禁用代理
for key in list(os.environ.keys()):
    if 'proxy' in key.lower():
        del os.environ[key]
os.environ['NO_PROXY'] = '*'
os.environ['no_proxy'] = '*'

sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from core.audio_interface import AudioInterface

# ============================================================
# 平台检测
# ============================================================
PLATFORM = 'desktop'
ANDROID_AVAILABLE = False

try:
    from kivy.utils import platform as kivy_platform
    if kivy_platform == 'android':
        PLATFORM = 'android'
        ANDROID_AVAILABLE = True
        print("[audio] Kivy检测到Android平台")
except:
    pass

# 如果Kivy没检测到，尝试jnius
if not ANDROID_AVAILABLE:
    try:
        from jnius import autoclass
        # 尝试加载Android类来确认是Android平台
        autoclass('android.content.Context')
        PLATFORM = 'android'
        ANDROID_AVAILABLE = True
        print("[audio] jnius检测到Android平台")
    except:
        print("[audio] 非Android平台，使用桌面模式")

# Kivy音频
from kivy.core.audio import SoundLoader
from kivy.clock import Clock

# Edge TTS（仅桌面）
EDGE_TTS_AVAILABLE = False
edge_tts = None

if PLATFORM == 'desktop':
    try:
        import edge_tts as _edge_tts
        edge_tts = _edge_tts
        EDGE_TTS_AVAILABLE = True
        print("[audio] Edge TTS可用")
    except ImportError:
        print("[audio] Edge TTS不可用")

# 语音配置
def get_voice():
    return "zh-CN-XiaoyiNeural"

def get_praises():
    return ['太棒了！', '真厉害！', '做得好！', '你真聪明！', '好厉害！', '汪汪队为你骄傲！']

def get_encourages():
    return ['再试一次！', '没关系！', '加油！', '你可以的！', '继续努力！']

try:
    from voice_config_shared import get_voice, get_praises, get_encourages
except ImportError:
    pass


# ============================================================
# Android TTS 封装类
# ============================================================
class AndroidTTS:
    """Android TTS封装 - 简化版，更可靠"""
    
    def __init__(self):
        self.tts = None
        self.ready = False
        self.context = None
        self._init_count = 0
        
    def init(self, callback=None):
        """初始化TTS"""
        if PLATFORM != 'android':
            print("[AndroidTTS] 非Android平台，跳过初始化")
            return
        
        self._init_count += 1
        print(f"[AndroidTTS] 开始初始化 (尝试 #{self._init_count})")
        
        try:
            from jnius import autoclass
            
            # 获取Activity
            PythonActivity = autoclass('org.kivy.android.PythonActivity')
            self.context = PythonActivity.mActivity
            
            if self.context is None:
                print("[AndroidTTS] Activity未就绪，延迟重试")
                if self._init_count < 10:
                    Clock.schedule_once(lambda dt: self.init(callback), 1.0)
                return
            
            # 创建TTS实例（不使用监听器，更简单可靠）
            TextToSpeech = autoclass('android.speech.tts.TextToSpeech')
            self.tts = TextToSpeech(self.context, None)
            
            # 延迟设置语言（等待TTS引擎初始化）
            Clock.schedule_once(lambda dt: self._setup_language(callback), 1.5)
            
        except Exception as e:
            print(f"[AndroidTTS] 初始化失败: {e}")
            import traceback
            traceback.print_exc()
    
    def _setup_language(self, callback=None):
        """设置语言"""
        if not self.tts:
            print("[AndroidTTS] TTS实例为空")
            return
        
        try:
            from jnius import autoclass
            Locale = autoclass('java.util.Locale')
            
            # 尝试设置中文
            result = -1
            try:
                result = self.tts.setLanguage(Locale.CHINA)
                print(f"[AndroidTTS] setLanguage(CHINA) = {result}")
            except:
                pass
            
            if result < 0:
                try:
                    result = self.tts.setLanguage(Locale.CHINESE)
                    print(f"[AndroidTTS] setLanguage(CHINESE) = {result}")
                except:
                    pass
            
            if result < 0:
                try:
                    locale = Locale("zh", "CN")
                    result = self.tts.setLanguage(locale)
                    print(f"[AndroidTTS] setLanguage(zh_CN) = {result}")
                except:
                    pass
            
            # 设置语速
            try:
                self.tts.setSpeechRate(0.9)
            except:
                pass
            
            self.ready = True
            print("[AndroidTTS] 初始化完成，ready=True")
            
            if callback:
                callback(True)
                
        except Exception as e:
            print(f"[AndroidTTS] 设置语言失败: {e}")
            # 即使设置语言失败，也尝试使用
            self.ready = True
            if callback:
                callback(True)
    
    def speak(self, text):
        """播放语音"""
        if not self.ready or not self.tts:
            print(f"[AndroidTTS] 未就绪，无法播放: {text}")
            return False
        
        try:
            from jnius import autoclass
            TextToSpeech = autoclass('android.speech.tts.TextToSpeech')
            
            # 使用QUEUE_FLUSH清空队列后播放
            # API 21+ 的speak方法签名: speak(text, queueMode, params, utteranceId)
            try:
                # 新API (Android 5.0+)
                result = self.tts.speak(text, TextToSpeech.QUEUE_FLUSH, None, "tts_" + str(uuid.uuid4())[:8])
                print(f"[AndroidTTS] speak(新API) = {result}, text={text}")
            except Exception as e1:
                print(f"[AndroidTTS] 新API失败: {e1}")
                try:
                    # 旧API
                    HashMap = autoclass('java.util.HashMap')
                    params = HashMap()
                    result = self.tts.speak(text, TextToSpeech.QUEUE_FLUSH, params)
                    print(f"[AndroidTTS] speak(旧API) = {result}, text={text}")
                except Exception as e2:
                    print(f"[AndroidTTS] 旧API也失败: {e2}")
                    return False
            
            return True
            
        except Exception as e:
            print(f"[AndroidTTS] speak异常: {e}")
            import traceback
            traceback.print_exc()
            return False
    
    def stop(self):
        """停止播放"""
        if self.tts:
            try:
                self.tts.stop()
            except:
                pass


# 全局Android TTS实例
_android_tts = None

def get_android_tts():
    global _android_tts
    if _android_tts is None and PLATFORM == 'android':
        _android_tts = AndroidTTS()
    return _android_tts


# ============================================================
# 主音频类
# ============================================================
class KivyAudio(AudioInterface):
    """Kivy音频实现"""
    
    def __init__(self):
        self.platform = PLATFORM
        self.tts_ready = False
        self.temp_dir = None
        self.speech_id = 0
        self.current_sound = None
        self.tts_lock = threading.Lock()
        self._pending_speaks = []
        self._android_tts = None
        
        # 创建临时目录
        try:
            self.temp_dir = tempfile.mkdtemp()
        except:
            self.temp_dir = '/tmp'
        
        # 初始化
        self._init_tts()
    
    def _init_tts(self):
        """初始化TTS"""
        print(f"[KivyAudio] 初始化TTS, platform={self.platform}")
        
        if self.platform == 'android':
            # Android平台
            self._android_tts = get_android_tts()
            if self._android_tts:
                self._android_tts.init(callback=self._on_android_tts_ready)
            else:
                print("[KivyAudio] 无法创建AndroidTTS实例")
        elif EDGE_TTS_AVAILABLE:
            # 桌面平台使用Edge TTS
            self.tts_ready = True
            print("[KivyAudio] Edge TTS就绪")
        else:
            # 后备方案
            self._init_pyttsx3()
    
    def _on_android_tts_ready(self, success):
        """Android TTS就绪回调"""
        print(f"[KivyAudio] Android TTS回调, success={success}")
        self.tts_ready = success
        # 处理等待队列
        self._process_pending()
    
    def _init_pyttsx3(self):
        """初始化pyttsx3"""
        try:
            import pyttsx3
            self._pyttsx3 = pyttsx3.init()
            self.tts_ready = True
            print("[KivyAudio] pyttsx3就绪")
        except Exception as e:
            print(f"[KivyAudio] pyttsx3失败: {e}")
    
    def _process_pending(self):
        """处理等待队列"""
        while self._pending_speaks and self.tts_ready:
            text = self._pending_speaks.pop(0)
            self._do_speak(text)
    
    def speak(self, text: str, rate: str = "+0%"):
        """朗读文字"""
        print(f"[KivyAudio] speak: '{text}', ready={self.tts_ready}, platform={self.platform}")
        
        if not self.tts_ready:
            print(f"[KivyAudio] TTS未就绪，加入队列")
            self._pending_speaks.append(text)
            return
        
        self._do_speak(text)
    
    def _do_speak(self, text: str):
        """执行语音播放"""
        if self.platform == 'android':
            # Android平台 - 在主线程调用
            Clock.schedule_once(lambda dt: self._speak_android(text), 0)
        elif EDGE_TTS_AVAILABLE:
            # 桌面平台 - 后台线程
            self.speech_id += 1
            t = threading.Thread(target=self._speak_edge_tts, args=(text, self.speech_id), daemon=True)
            t.start()
        elif hasattr(self, '_pyttsx3'):
            # pyttsx3后备
            try:
                self._pyttsx3.say(text)
                self._pyttsx3.runAndWait()
            except:
                pass
    
    def _speak_android(self, text: str):
        """Android TTS播放"""
        if self._android_tts:
            result = self._android_tts.speak(text)
            print(f"[KivyAudio] Android speak结果: {result}")
        else:
            print("[KivyAudio] AndroidTTS实例不存在")
    
    def _speak_edge_tts(self, text: str, speech_id: int):
        """Edge TTS播放（桌面）"""
        try:
            if speech_id != self.speech_id:
                return
            
            import asyncio
            audio_file = os.path.join(self.temp_dir, f"tts_{uuid.uuid4().hex}.mp3")
            
            async def generate():
                communicate = edge_tts.Communicate(text, get_voice())
                await communicate.save(audio_file)
            
            loop = asyncio.new_event_loop()
            asyncio.set_event_loop(loop)
            try:
                loop.run_until_complete(generate())
            finally:
                loop.close()
            
            if os.path.exists(audio_file):
                Clock.schedule_once(lambda dt: self._play_file(audio_file), 0)
        except Exception as e:
            print(f"[KivyAudio] Edge TTS错误: {e}")
    
    def _play_file(self, filepath: str):
        """播放音频文件"""
        try:
            if self.current_sound:
                self.current_sound.stop()
            
            sound = SoundLoader.load(filepath)
            if sound:
                self.current_sound = sound
                sound.play()
                # 延迟清理
                Clock.schedule_once(lambda dt: self._cleanup(filepath), sound.length + 1)
        except Exception as e:
            print(f"[KivyAudio] 播放文件错误: {e}")
    
    def _cleanup(self, filepath):
        """清理临时文件"""
        try:
            if os.path.exists(filepath):
                os.remove(filepath)
        except:
            pass
    
    def play_praise(self):
        """播放表扬"""
        self.speak(random.choice(get_praises()))
    
    def play_encourage(self):
        """播放鼓励"""
        self.speak(random.choice(get_encourages()))
    
    def play_sound(self, sound_name: str):
        """播放音效"""
        pass  # 暂不实现
    
    def stop(self):
        """停止播放"""
        self.speech_id += 1
        if self._android_tts:
            self._android_tts.stop()
        if self.current_sound:
            try:
                self.current_sound.stop()
            except:
                pass
    
    def cleanup(self):
        """清理"""
        pass


# ============================================================
# 全局实例
# ============================================================
_audio_instance = None

def get_audio():
    """获取音频实例"""
    global _audio_instance
    if _audio_instance is None:
        _audio_instance = KivyAudio()
    return _audio_instance
