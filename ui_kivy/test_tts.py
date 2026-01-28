# -*- coding: utf-8 -*-
"""
TTS 测试脚本 v2.0
用于调试Android/鸿蒙平板上的语音问题
"""
import os
import sys

app_dir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.insert(0, app_dir)
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

from kivy.app import App
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.button import Button
from kivy.uix.label import Label
from kivy.uix.scrollview import ScrollView
from kivy.clock import Clock
from kivy.utils import platform

# 日志
_logs = []

def log(msg):
    print(msg)
    _logs.append(str(msg))
    if len(_logs) > 50:
        _logs.pop(0)


class TTSTestApp(App):
    
    def build(self):
        self.title = 'TTS测试 v2'
        self.tts = None
        self.tts_ready = False
        
        root = BoxLayout(orientation='vertical', padding=10, spacing=5)
        
        # 状态
        self.status = Label(text='初始化中...', font_size='20sp', size_hint=(1, 0.1))
        root.add_widget(self.status)
        
        # 平台信息
        self.info = Label(text=f'平台: {platform}', font_size='16sp', size_hint=(1, 0.08))
        root.add_widget(self.info)
        
        # 按钮
        btns = BoxLayout(size_hint=(1, 0.25), spacing=10)
        
        b1 = Button(text='初始化TTS', font_size='18sp')
        b1.bind(on_press=lambda x: self.init_tts())
        btns.add_widget(b1)
        
        b2 = Button(text='测试:你好', font_size='18sp')
        b2.bind(on_press=lambda x: self.test_speak("你好"))
        btns.add_widget(b2)
        
        b3 = Button(text='测试:欢迎', font_size='18sp')
        b3.bind(on_press=lambda x: self.test_speak("欢迎来到乐乐的识字乐园"))
        btns.add_widget(b3)
        
        root.add_widget(btns)
        
        # 更多测试按钮
        btns2 = BoxLayout(size_hint=(1, 0.15), spacing=10)
        
        b4 = Button(text='测试:ABC', font_size='18sp')
        b4.bind(on_press=lambda x: self.test_speak("A B C"))
        btns2.add_widget(b4)
        
        b5 = Button(text='测试:123', font_size='18sp')
        b5.bind(on_press=lambda x: self.test_speak("一二三"))
        btns2.add_widget(b5)
        
        b6 = Button(text='清空日志', font_size='18sp')
        b6.bind(on_press=lambda x: self.clear_log())
        btns2.add_widget(b6)
        
        root.add_widget(btns2)
        
        # 日志
        self.log_label = Label(
            text='日志:\n',
            font_size='12sp',
            size_hint_y=None,
            halign='left',
            valign='top'
        )
        self.log_label.bind(texture_size=self.log_label.setter('size'))
        
        scroll = ScrollView(size_hint=(1, 0.42))
        scroll.add_widget(self.log_label)
        root.add_widget(scroll)
        
        # 自动初始化
        Clock.schedule_once(lambda dt: self.init_tts(), 1.0)
        
        # 定时更新日志
        Clock.schedule_interval(lambda dt: self.update_log(), 0.5)
        
        return root
    
    def update_log(self):
        self.log_label.text = 'LOG:\n' + '\n'.join(_logs[-30:])
    
    def clear_log(self):
        _logs.clear()
        log("日志已清空")
    
    def init_tts(self):
        log(f"=== 开始初始化 ===")
        log(f"platform = {platform}")
        
        if platform != 'android':
            self.status.text = '非Android平台'
            log("非Android，跳过")
            return
        
        try:
            log("导入jnius...")
            from jnius import autoclass
            log("jnius导入成功")
            
            log("获取PythonActivity...")
            PythonActivity = autoclass('org.kivy.android.PythonActivity')
            activity = PythonActivity.mActivity
            log(f"activity = {activity}")
            
            if activity is None:
                log("Activity为空！延迟重试...")
                self.status.text = 'Activity未就绪'
                Clock.schedule_once(lambda dt: self.init_tts(), 2.0)
                return
            
            log("获取TextToSpeech类...")
            TTS = autoclass('android.speech.tts.TextToSpeech')
            log("创建TTS实例...")
            self.tts = TTS(activity, None)
            log(f"TTS实例: {self.tts}")
            
            # 延迟设置语言
            Clock.schedule_once(lambda dt: self.setup_language(), 1.5)
            
        except Exception as e:
            log(f"初始化异常: {e}")
            import traceback
            log(traceback.format_exc())
            self.status.text = f'错误: {str(e)[:30]}'
    
    def setup_language(self):
        log("=== 设置语言 ===")
        
        if not self.tts:
            log("TTS实例为空")
            return
        
        try:
            from jnius import autoclass
            Locale = autoclass('java.util.Locale')
            
            # 尝试不同的Locale
            locales = [
                ('CHINA', Locale.CHINA),
                ('CHINESE', Locale.CHINESE),
                ('SIMPLIFIED_CHINESE', Locale.SIMPLIFIED_CHINESE),
            ]
            
            for name, locale in locales:
                try:
                    result = self.tts.setLanguage(locale)
                    log(f"setLanguage({name}) = {result}")
                    if result >= 0:
                        break
                except Exception as e:
                    log(f"{name} 失败: {e}")
            
            # 设置语速
            try:
                self.tts.setSpeechRate(0.9)
                log("语速设置完成")
            except:
                pass
            
            self.tts_ready = True
            self.status.text = 'TTS就绪 ✓'
            log("=== TTS就绪 ===")
            
        except Exception as e:
            log(f"设置语言异常: {e}")
            self.status.text = '语言设置失败'
    
    def test_speak(self, text):
        log(f"=== 测试播放: {text} ===")
        log(f"tts_ready = {self.tts_ready}")
        log(f"tts = {self.tts}")
        
        if not self.tts_ready or not self.tts:
            log("TTS未就绪")
            self.status.text = 'TTS未就绪'
            return
        
        try:
            from jnius import autoclass
            TTS = autoclass('android.speech.tts.TextToSpeech')
            
            log(f"调用speak()...")
            
            # 尝试新API
            try:
                import uuid
                utterance_id = "test_" + str(uuid.uuid4())[:8]
                result = self.tts.speak(text, TTS.QUEUE_FLUSH, None, utterance_id)
                log(f"speak(新API) 返回: {result}")
            except Exception as e1:
                log(f"新API失败: {e1}")
                
                # 尝试旧API
                try:
                    HashMap = autoclass('java.util.HashMap')
                    params = HashMap()
                    result = self.tts.speak(text, TTS.QUEUE_FLUSH, params)
                    log(f"speak(旧API) 返回: {result}")
                except Exception as e2:
                    log(f"旧API也失败: {e2}")
            
            self.status.text = f'已播放: {text}'
            
        except Exception as e:
            log(f"播放异常: {e}")
            import traceback
            log(traceback.format_exc())


if __name__ == '__main__':
    TTSTestApp().run()
