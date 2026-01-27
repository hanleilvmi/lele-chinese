# -*- coding: utf-8 -*-
"""
汉字更新工具 - 从 汉字表.txt 读取汉字并更新到程序

使用方法：
1. 编辑 汉字表.txt 添加新汉字
2. 双击运行这个文件，或命令行运行: python 更新汉字.py
3. 程序会自动更新 core/data_chinese.py 和 chinese_app_pydroid.py
"""
import os
import re

def read_words_from_txt(filepath='汉字表.txt'):
    """从txt文件读取汉字"""
    words = []
    
    if not os.path.exists(filepath):
        print(f"错误：找不到文件 {filepath}")
        return words
    
    with open(filepath, 'r', encoding='utf-8') as f:
        for line in f:
            line = line.strip()
            # 跳过空行和注释
            if not line or line.startswith('#'):
                continue
            
            parts = line.split(',')
            if len(parts) >= 3:
                char = parts[0].strip()
                pinyin = parts[1].strip()
                word = parts[2].strip()
                # 生成一个简单的emoji占位符
                emoji = "📝"
                words.append((char, pinyin, word, emoji))
            else:
                print(f"警告：格式错误，跳过: {line}")
    
    return words

def update_core_data(words):
    """更新 core/data_chinese.py"""
    filepath = 'core/data_chinese.py'
    
    if not os.path.exists(filepath):
        print(f"警告：找不到 {filepath}，跳过")
        return False
    
    # 分成三个等级（每12个一组）
    basic = words[:12] if len(words) >= 12 else words
    intermediate = words[12:24] if len(words) >= 24 else words[12:] if len(words) > 12 else []
    advanced = words[24:] if len(words) > 24 else []
    
    def format_words(word_list):
        lines = []
        for char, pinyin, word, emoji in word_list:
            lines.append(f'        ("{char}", "{pinyin}", "{word}", "{emoji}"),')
        return '\n'.join(lines)
    
    content = f'''# -*- coding: utf-8 -*-
"""
汉字数据模块 - 与UI无关的纯数据
自动生成，请勿手动修改！如需添加汉字请编辑 汉字表.txt
"""

class ChineseData:
    """汉字数据类"""
    
    # 基础汉字: (汉字, 拼音, 词组, emoji)
    BASIC_WORDS = [
{format_words(basic)}
    ]
    
    # 进阶汉字
    INTERMEDIATE_WORDS = [
{format_words(intermediate)}
    ]
    
    # 高级汉字
    ADVANCED_WORDS = [
{format_words(advanced)}
    ]
    
    @classmethod
    def get_words(cls, level=1):
        """根据等级获取汉字"""
        if level == 1:
            return cls.BASIC_WORDS.copy()
        elif level == 2:
            return cls.BASIC_WORDS + cls.INTERMEDIATE_WORDS
        else:
            return cls.BASIC_WORDS + cls.INTERMEDIATE_WORDS + cls.ADVANCED_WORDS
    
    @classmethod
    def get_word_by_char(cls, char, level=3):
        """根据汉字查找数据"""
        all_words = cls.get_words(level)
        for item in all_words:
            if item[0] == char:
                return item
        return None
    
    @classmethod
    def get_word_count(cls, level):
        """获取指定等级的汉字数量"""
        return len(cls.get_words(level))
'''
    
    with open(filepath, 'w', encoding='utf-8') as f:
        f.write(content)
    
    print(f"✓ 已更新 {filepath}")
    return True

def update_pydroid(words):
    """更新 chinese_app_pydroid.py 中的汉字数据"""
    filepath = 'chinese_app_pydroid.py'
    
    if not os.path.exists(filepath):
        print(f"警告：找不到 {filepath}，跳过")
        return False
    
    with open(filepath, 'r', encoding='utf-8') as f:
        content = f.read()
    
    # 分成三个等级
    basic = words[:12] if len(words) >= 12 else words
    intermediate = words[12:24] if len(words) >= 24 else words[12:] if len(words) > 12 else []
    advanced = words[24:] if len(words) > 24 else []
    
    def format_words_inline(word_list):
        lines = []
        for char, pinyin, word, emoji in word_list:
            lines.append(f'        ("{char}", "{pinyin}", "{word}", "{emoji}"),')
        return '\n'.join(lines)
    
    # 构建新的 ChineseData 类
    new_class = f'''class ChineseData:
    BASIC_WORDS = [
{format_words_inline(basic)}
    ]
    INTERMEDIATE_WORDS = [
{format_words_inline(intermediate)}
    ]
    ADVANCED_WORDS = [
{format_words_inline(advanced)}
    ]
    
    @classmethod
    def get_words(cls, level=1):
        if level == 1:
            return cls.BASIC_WORDS.copy()
        elif level == 2:
            return cls.BASIC_WORDS + cls.INTERMEDIATE_WORDS
        else:
            return cls.BASIC_WORDS + cls.INTERMEDIATE_WORDS + cls.ADVANCED_WORDS'''
    
    # 用正则替换 ChineseData 类
    pattern = r'class ChineseData:.*?@classmethod\s+def get_words\(cls, level=1\):.*?return cls\.BASIC_WORDS \+ cls\.INTERMEDIATE_WORDS \+ cls\.ADVANCED_WORDS'
    
    new_content = re.sub(pattern, new_class, content, flags=re.DOTALL)
    
    if new_content == content:
        print(f"警告：未能更新 {filepath}，可能格式已变化")
        return False
    
    with open(filepath, 'w', encoding='utf-8') as f:
        f.write(new_content)
    
    print(f"✓ 已更新 {filepath}")
    return True

def main():
    print("=" * 50)
    print("乐乐识字乐园 - 汉字更新工具")
    print("=" * 50)
    print()
    
    # 读取汉字
    words = read_words_from_txt()
    
    if not words:
        print("错误：没有读取到任何汉字！")
        print("请检查 汉字表.txt 文件是否存在且格式正确")
        input("\n按回车键退出...")
        return
    
    print(f"读取到 {len(words)} 个汉字")
    print()
    
    # 更新文件
    update_core_data(words)
    update_pydroid(words)
    
    print()
    print("=" * 50)
    print("更新完成！")
    print(f"共 {len(words)} 个汉字")
    print()
    print("提示：")
    print("- 电脑版：直接运行即可看到新汉字")
    print("- 平板版：需要重新推送到GitHub编译APK")
    print("=" * 50)
    
    input("\n按回车键退出...")

if __name__ == '__main__':
    main()
