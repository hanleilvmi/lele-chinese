# -*- coding: utf-8 -*-
"""
修复主题导入问题
"""

def fix_module(filename):
    """修复单个模块的主题导入"""
    with open(filename, 'r', encoding='utf-8') as f:
        content = f.read()
    
    # 移除错误插入的主题导入代码
    bad_patterns = [
        '''
# 导入主题系统
try:
    from theme_config import get_theme, ThemeHelper
    THEME_AVAILABLE = True
    theme = ThemeHelper()
except ImportError:
    THEME_AVAILABLE = False
    theme = None
''',
        '''# 导入主题系统
try:
    from theme_config import get_theme, ThemeHelper
    THEME_AVAILABLE = True
    theme = ThemeHelper()
except ImportError:
    THEME_AVAILABLE = False
    theme = None
''',
    ]
    
    for pattern in bad_patterns:
        content = content.replace(pattern, '')
    
    # 修复被破坏的导入语句
    # kids_pinyin.py 的问题
    content = content.replace(
        'from voice_config_shared import get_voice, get_praises, get_encourages\n, create_rest_reminder',
        'from voice_config_shared import get_voice, get_praises, get_encourages, create_rest_reminder'
    )
    
    # 其他模块可能的问题
    content = content.replace(
        'from voice_config_shared import get_voice, get_praises, get_encourages\n    VOICE_CONFIG_AVAILABLE',
        'from voice_config_shared import get_voice, get_praises, get_encourages\n    VOICE_CONFIG_AVAILABLE'
    )
    
    with open(filename, 'w', encoding='utf-8') as f:
        f.write(content)
    
    print(f"✅ 已修复 {filename}")


def add_theme_import_correctly(filename):
    """在正确位置添加主题导入"""
    with open(filename, 'r', encoding='utf-8') as f:
        content = f.read()
    
    # 如果已经有正确的主题导入，跳过
    if 'THEME_AVAILABLE = True' in content and 'theme = ThemeHelper()' in content:
        # 检查是否在正确位置（文件顶部，不在类内部）
        lines = content.split('\n')
        theme_line = -1
        class_line = -1
        for i, line in enumerate(lines):
            if 'THEME_AVAILABLE = True' in line:
                theme_line = i
            if line.startswith('class '):
                class_line = i
                break
        
        if theme_line > 0 and class_line > 0 and theme_line < class_line:
            print(f"⏭️ {filename} 主题导入已正确，跳过")
            return
    
    # 主题导入代码块
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
    
    # 找到合适的插入位置：在 VOICE_CONFIG_AVAILABLE = False 之后
    if 'VOICE_CONFIG_AVAILABLE = False' in content:
        content = content.replace(
            'VOICE_CONFIG_AVAILABLE = False\n\n\nclass',
            'VOICE_CONFIG_AVAILABLE = False\n' + theme_import + '\nclass'
        )
        content = content.replace(
            'VOICE_CONFIG_AVAILABLE = False\n\nclass',
            'VOICE_CONFIG_AVAILABLE = False\n' + theme_import + '\nclass'
        )
    
    with open(filename, 'w', encoding='utf-8') as f:
        f.write(content)
    
    print(f"✅ 已添加主题导入到 {filename}")


if __name__ == "__main__":
    modules = [
        'kids_pinyin.py',
        'kids_math.py',
        'kids_english.py',
        'kids_thinking.py',
        'kids_vehicles.py'
    ]
    
    print("第一步：修复被破坏的导入...")
    for m in modules:
        try:
            fix_module(m)
        except Exception as e:
            print(f"❌ {m}: {e}")
    
    print("\n第二步：添加正确的主题导入...")
    for m in modules:
        try:
            add_theme_import_correctly(m)
        except Exception as e:
            print(f"❌ {m}: {e}")
    
    print("\n完成！")
