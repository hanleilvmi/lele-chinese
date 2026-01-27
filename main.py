# -*- coding: utf-8 -*-
"""
乐乐的识字乐园 - Android APK 入口文件
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

try:
    # 使用完整版本
    from ui_kivy.chinese_app import ChineseLearnApp
    
    if __name__ == '__main__':
        ChineseLearnApp().run()
        
except Exception as e:
    print(f"启动失败: {e}")
    import traceback
    traceback.print_exc()
    
    # 显示错误界面
    try:
        from kivy.app import App
        from kivy.uix.label import Label
        
        class ErrorApp(App):
            def build(self):
                return Label(text=f'启动失败:\n{str(e)[:200]}', font_size='18sp')
        
        ErrorApp().run()
    except:
        pass
