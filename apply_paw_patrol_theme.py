# -*- coding: utf-8 -*-
"""
汪汪队主题集成脚本
将汪汪队主题完整嵌入到所有学习模块中
"""

import os
import re

# 需要修改的模块文件
MODULES = [
    "kids_math.py",
    "kids_pinyin.py", 
    "kids_english.py",
    "kids_thinking.py",
    "kids_vehicles.py",
    "kids_game_v3.py",
    "kids_learning_main.py"
]

# 主题导入代码
THEME_IMPORT = '''
# 导入汪汪队主题绘图
try:
    from theme_drawings import ThemeDrawings
    from theme_config import ThemeHelper, get_current_theme
    THEME_AVAILABLE = True
except ImportError:
    THEME_AVAILABLE = False
    ThemeDrawings = None
'''

def add_theme_import(content):
    """添加主题导入"""
    # 检查是否已有主题导入
    if "from theme_drawings import" in content:
        return content
    
    # 在其他import之后添加
    lines = content.split('\n')
    insert_pos = 0
    
    for i, line in enumerate(lines):
        if line.startswith('import ') or line.startswith('from '):
            insert_pos = i + 1
        elif line.strip() and not line.startswith('#') and not line.startswith('"""') and insert_pos > 0:
            break
    
    # 找到最后一个import块
    for i in range(len(lines)-1, -1, -1):
        if lines[i].strip().startswith('import ') or lines[i].strip().startswith('from '):
            insert_pos = i + 1
            break
        if lines[i].strip().startswith('except') and 'Import' in lines[i]:
            insert_pos = i + 2
            break
    
    lines.insert(insert_pos, THEME_IMPORT)
    return '\n'.join(lines)


def process_file(filepath):
    """处理单个文件"""
    print(f"处理: {filepath}")
    
    with open(filepath, 'r', encoding='utf-8') as f:
        content = f.read()
    
    # 添加主题导入
    content = add_theme_import(content)
    
    with open(filepath, 'w', encoding='utf-8') as f:
        f.write(content)
    
    print(f"  ✓ 已添加主题导入")


def main():
    print("=" * 50)
    print("汪汪队主题集成")
    print("=" * 50)
    
    base_dir = os.path.dirname(os.path.abspath(__file__))
    
    for module in MODULES:
        filepath = os.path.join(base_dir, module)
        if os.path.exists(filepath):
            process_file(filepath)
        else:
            print(f"跳过: {module} (文件不存在)")
    
    print("\n" + "=" * 50)
    print("主题集成完成！")
    print("=" * 50)


if __name__ == "__main__":
    main()
