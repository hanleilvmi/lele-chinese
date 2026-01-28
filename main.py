# -*- coding: utf-8 -*-
"""
乐乐的识字乐园 - Android/鸿蒙 APK 入口文件
v1.3.0 - 修复TTS语音问题
"""
import os
import sys

# 确保能找到模块
app_dir = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, app_dir)
sys.path.insert(0, os.path.join(app_dir, 'ui_kivy'))
sys.path.insert(0, os.path.join(app_dir, 'core'))

# 设置环境变量
os.environ['KIVY_NO_FILELOG'] = '1'
os.environ['KIVY_NO_CONSOLELOG'] = '0'  # 保留控制台日志用于调试

# 检测平台
def get_platform():
    try:
        from jnius import autoclass
        return 'android'
    except:
        return 'desktop'

PLATFORM = get_platform()
print(f"[main] 平台: {PLATFORM}")

try:
    # 先初始化字体配置
    print("[main] 初始化字体配置...")
    try:
        from ui_kivy import font_config
        print("[main] 字体配置完成")
    except Exception as e:
        print(f"[main] 字体配置失败: {e}")
    
    # 使用完整版本
    print("[main] 加载应用...")
    from ui_kivy.chinese_app import ChineseLearnApp
    
    if __name__ == '__main__':
        print("[main] 启动应用...")
        ChineseLearnApp().run()
        
except Exception as e:
    print(f"[main] 启动失败: {e}")
    import traceback
    traceback.print_exc()
    
    # 显示错误界面
    try:
        from kivy.app import App
        from kivy.uix.label import Label
        from kivy.uix.boxlayout import BoxLayout
        from kivy.uix.scrollview import ScrollView
        
        class ErrorApp(App):
            def build(self):
                layout = BoxLayout(orientation='vertical', padding=20)
                scroll = ScrollView()
                error_text = f'启动失败:\n\n{str(e)}\n\n请检查:\n1. 是否安装了中文TTS语音包\n2. 存储权限是否已授予'
                label = Label(
                    text=error_text, 
                    font_size='16sp',
                    size_hint_y=None,
                    text_size=(None, None)
                )
                label.bind(texture_size=label.setter('size'))
                scroll.add_widget(label)
                layout.add_widget(scroll)
                return layout
        
        ErrorApp().run()
    except:
        pass
