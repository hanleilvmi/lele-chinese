# -*- coding: utf-8 -*-
"""
为所有模块应用主题系统
使用Python脚本安全地修改文件，保持UTF-8编码
"""

import re

def apply_theme_to_modules():
    """为各模块添加主题支持"""
    
    modules = [
        'kids_game_v3.py',
        'kids_pinyin.py', 
        'kids_math.py',
        'kids_english.py',
        'kids_thinking.py',
        'kids_vehicles.py'
    ]
    
    # 主题导入代码
    theme_import = '''
# 导入主题系统
try:
    from theme_config import get_theme, ThemeHelper
    THEME_AVAILABLE = True
    theme = ThemeHelper()
except ImportError:
    THEME_AVAILABLE = False
    theme = None
'''
    
    for module in modules:
        try:
            with open(module, 'r', encoding='utf-8') as f:
                content = f.read()
            
            # 检查是否已经添加过主题导入
            if 'from theme_config import' in content:
                print(f"⏭️ {module} 已有主题支持，跳过")
                continue
            
            # 在 voice_config_shared 导入后添加主题导入
            if 'from voice_config_shared import' in content:
                content = content.replace(
                    'from voice_config_shared import get_voice, get_praises, get_encourages',
                    'from voice_config_shared import get_voice, get_praises, get_encourages' + theme_import
                )
            elif 'VOICE_CONFIG_AVAILABLE = False' in content:
                # 在 VOICE_CONFIG_AVAILABLE = False 后添加
                content = content.replace(
                    'VOICE_CONFIG_AVAILABLE = False',
                    'VOICE_CONFIG_AVAILABLE = False' + theme_import
                )
            
            with open(module, 'w', encoding='utf-8') as f:
                f.write(content)
            
            print(f"✅ {module} 已添加主题支持")
            
        except Exception as e:
            print(f"❌ {module} 处理失败: {e}")
    
    print("\n主题系统已添加到所有模块！")
    print("各模块可以通过 theme.bg_color, theme.primary 等属性获取主题颜色")


if __name__ == "__main__":
    apply_theme_to_modules()
