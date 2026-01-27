# -*- coding: utf-8 -*-
"""修复模块文件"""
import re

def fix_file(filename):
    with open(filename, 'r', encoding='utf-8') as f:
        content = f.read()
    
    # 1. 修改答题等待时间 4000 -> 5500
    content = re.sub(r'after\(4000, self\.new_', 'after(5500, self.new_', content)
    content = re.sub(r'after\(4000, self\.create_main_menu\)', 'after(5500, self.create_main_menu)', content)
    
    with open(filename, 'w', encoding='utf-8') as f:
        f.write(content)
    print(f"Fixed {filename}")

# 修复所有模块
for f in ['kids_pinyin.py', 'kids_math.py', 'kids_english.py', 'kids_thinking.py', 'kids_vehicles.py']:
    fix_file(f)

print("Done!")
