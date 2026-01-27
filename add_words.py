# -*- coding: utf-8 -*-
"""
字库管理工具 - 一键添加新汉字
用法: python add_words.py 花草鸟鱼
"""

import sys
import os
import json

# 尝试导入拼音库
try:
    from pypinyin import pinyin, Style
    PINYIN_AVAILABLE = True
except ImportError:
    PINYIN_AVAILABLE = False
    print("提示: 安装 pypinyin 可自动生成拼音 (pip install pypinyin)")

# 常用汉字的emoji映射（可扩展）
EMOJI_MAP = {
    # 自然
    "花": "🌸", "草": "🌿", "树": "🌳", "叶": "🍃", "山": "⛰️", "石": "🪨",
    "云": "☁️", "雨": "🌧️", "雪": "❄️", "星": "⭐", "河": "🏞️", "海": "🌊",
    # 动物
    "鸟": "🐦", "鱼": "🐟", "虫": "🐛", "马": "🐴", "猫": "🐱", "狗": "🐕",
    "鸡": "🐔", "鸭": "🦆", "猪": "🐷", "兔": "🐰", "龙": "🐲", "蛇": "🐍",
    "虎": "🐯", "象": "🐘", "熊": "🐻", "猴": "🐵", "蝴": "🦋", "蜂": "🐝",
    # 人物
    "人": "👤", "男": "👦", "女": "👧", "孩": "👶", "友": "🤝", "师": "👨‍🏫",
    # 身体
    "手": "✋", "足": "🦶", "口": "👄", "耳": "👂", "目": "👁️", "头": "🗣️",
    # 食物
    "米": "🍚", "面": "🍜", "菜": "🥬", "果": "🍎", "糖": "🍬", "蛋": "🥚",
    # 物品
    "车": "🚗", "船": "🚢", "门": "🚪", "窗": "🪟", "床": "🛏️", "桌": "🪑",
    "书": "📚", "笔": "✏️", "纸": "📄", "包": "🎒", "伞": "☂️", "钟": "🕐",
    # 颜色
    "红": "🔴", "黄": "🟡", "蓝": "🔵", "绿": "🟢", "黑": "⚫", "紫": "🟣",
    # 数字
    "二": "2️⃣", "六": "6️⃣", "七": "7️⃣", "八": "8️⃣", "九": "9️⃣", "十": "🔟",
    "百": "💯", "千": "🔢", "万": "🔢",
    # 动作
    "走": "🚶", "跑": "🏃", "跳": "🦘", "飞": "✈️", "吃": "🍽️", "喝": "🥤",
    "笑": "😊", "哭": "😢", "唱": "🎤", "画": "🎨", "写": "✍️", "读": "📖",
    # 其他
    "大": "🔺", "中": "⏺️", "上": "⬆️", "下": "⬇️", "左": "⬅️", "右": "➡️",
    "早": "🌅", "晚": "🌙", "春": "🌸", "夏": "☀️", "秋": "🍂", "冬": "❄️",
    "爱": "❤️", "乐": "😄", "美": "💖", "新": "✨", "快": "⚡", "慢": "🐢",
}

# 常用组词模板
WORD_TEMPLATES = {
    "花": ["小花", "花朵", "鲜花"], "草": ["小草", "青草", "草地"],
    "鸟": ["小鸟", "鸟儿", "飞鸟"], "鱼": ["小鱼", "金鱼", "鱼儿"],
    "虫": ["小虫", "虫子", "昆虫"], "马": ["小马", "马儿", "骑马"],
    "猫": ["小猫", "猫咪", "花猫"], "狗": ["小狗", "狗狗", "大狗"],
    "鸡": ["小鸡", "公鸡", "母鸡"], "鸭": ["小鸭", "鸭子", "野鸭"],
    "兔": ["小兔", "兔子", "白兔"], "猪": ["小猪", "猪猪", "大猪"],
    "山": ["大山", "山上", "高山"], "云": ["白云", "云朵", "乌云"],
    "雨": ["下雨", "雨水", "大雨"], "雪": ["下雪", "雪花", "白雪"],
    "星": ["星星", "明星", "星光"], "河": ["小河", "河水", "河边"],
    "海": ["大海", "海水", "海边"], "石": ["石头", "石子", "岩石"],
    "红": ["红色", "红花", "红旗"], "黄": ["黄色", "黄花", "金黄"],
    "蓝": ["蓝色", "蓝天", "深蓝"], "绿": ["绿色", "绿草", "绿叶"],
    "黑": ["黑色", "黑夜", "漆黑"], "紫": ["紫色", "紫花", "紫红"],
}

# 造句模板
SENTENCE_TEMPLATES = {
    "花": "花园里开满了小花。", "草": "小草绿油油的。",
    "鸟": "小鸟在天上飞。", "鱼": "鱼儿在水里游。",
    "虫": "小虫子在爬。", "马": "小马跑得真快。",
    "猫": "小猫咪喵喵叫。", "狗": "小狗汪汪叫。",
    "鸡": "公鸡喔喔叫。", "鸭": "小鸭嘎嘎叫。",
    "兔": "小兔子蹦蹦跳。", "猪": "小猪哼哼叫。",
    "山": "山上有很多树。", "云": "白云飘在蓝天上。",
    "雨": "下雨了，要打伞。", "雪": "下雪了，好漂亮。",
    "星": "星星亮晶晶。", "河": "小河流水哗哗响。",
    "海": "大海真大呀。", "石": "石头硬硬的。",
    "红": "红红的苹果真好吃。", "黄": "黄黄的香蕉弯弯的。",
    "蓝": "蓝蓝的天空真美。", "绿": "绿绿的小草真可爱。",
}

# 简化笔顺数据（基础笔画）
STROKE_TEMPLATES = {
    # 简单字
    "二": [[(30, 70), (170, 70)], [(20, 130), (180, 130)]],
    "十": [[(100, 30), (100, 170)], [(30, 100), (170, 100)]],
    "大": [[(30, 60), (170, 60)], [(100, 30), (100, 100)], [(100, 100), (40, 170)], [(100, 100), (160, 170)]],
    "小": [[(100, 30), (100, 170)], [(100, 80), (50, 130)], [(100, 80), (150, 130)]],
    "人": [[(100, 30), (50, 170)], [(100, 30), (150, 170)]],
    "口": [[(50, 50), (50, 150)], [(50, 50), (150, 50)], [(150, 50), (150, 150)], [(50, 150), (150, 150)]],
    "山": [[(100, 30), (100, 170)], [(40, 80), (40, 170)], [(160, 80), (160, 170)]],
    "上": [[(100, 50), (100, 130)], [(50, 130), (150, 130)], [(30, 170), (170, 170)]],
    "下": [[(30, 50), (170, 50)], [(100, 50), (100, 130)], [(100, 130), (60, 170)]],
    "中": [[(50, 40), (50, 160)], [(50, 40), (150, 40)], [(150, 40), (150, 160)], [(50, 160), (150, 160)], [(100, 40), (100, 160)]],
    "花": [[(40, 30), (40, 60)], [(40, 45), (70, 45)], [(100, 30), (70, 80)], [(100, 30), (130, 80)], [(100, 80), (100, 170)], [(60, 120), (140, 120)], [(100, 120), (60, 170)], [(100, 120), (140, 170)]],
    "草": [[(40, 30), (40, 60)], [(40, 45), (70, 45)], [(130, 30), (130, 60)], [(130, 45), (160, 45)], [(50, 80), (150, 80)], [(100, 80), (100, 130)], [(50, 130), (150, 130)], [(30, 170), (170, 170)]],
    "鸟": [[(60, 30), (100, 60)], [(140, 30), (100, 60)], [(60, 60), (60, 130)], [(60, 60), (140, 60)], [(140, 60), (140, 130)], [(60, 100), (140, 100)], [(60, 130), (140, 130)], [(100, 130), (100, 170)]],
    "鱼": [[(60, 30), (100, 50)], [(140, 30), (100, 50)], [(50, 60), (150, 60)], [(50, 60), (50, 130)], [(150, 60), (150, 130)], [(50, 95), (150, 95)], [(50, 130), (150, 130)], [(70, 150), (130, 150)], [(100, 150), (100, 170)]],
}


def get_pinyin(char):
    """获取拼音"""
    if PINYIN_AVAILABLE:
        try:
            py = pinyin(char, style=Style.TONE)
            if py and py[0]:
                return py[0][0]
        except:
            pass
    return "?"


def get_emoji(char):
    """获取emoji"""
    return EMOJI_MAP.get(char, "📝")


def get_words(char):
    """获取组词"""
    if char in WORD_TEMPLATES:
        return WORD_TEMPLATES[char]
    return [char + "字", "写" + char, char + char]


def get_sentence(char):
    """获取造句"""
    if char in SENTENCE_TEMPLATES:
        return SENTENCE_TEMPLATES[char]
    words = get_words(char)
    return f"乐乐学会了{words[0]}。"


def get_stroke(char):
    """获取笔顺"""
    return STROKE_TEMPLATES.get(char, None)


def add_words_to_database(chars, level=3):
    """添加汉字到字库"""
    db_path = os.path.join(os.path.dirname(__file__), "word_database.py")
    
    if not os.path.exists(db_path):
        print(f"错误: 找不到 {db_path}")
        return
    
    with open(db_path, 'r', encoding='utf-8') as f:
        content = f.read()
    
    # 获取现有字符
    existing_chars = set()
    for line in content.split('\n'):
        if line.strip().startswith('("') and '", "' in line:
            char = line.strip()[2:3]
            if '\u4e00' <= char <= '\u9fff':
                existing_chars.add(char)
    
    # 准备新字数据
    new_chars = []
    new_emojis = []
    new_strokes = []
    
    for char in chars:
        if not ('\u4e00' <= char <= '\u9fff'):
            continue
        if char in existing_chars:
            print(f"跳过: {char} (已存在)")
            continue
        
        py = get_pinyin(char)
        emoji = get_emoji(char)
        words = get_words(char)
        sentence = get_sentence(char)
        stroke = get_stroke(char)
        
        new_chars.append(f'    ("{char}", "{py}", "{emoji}", {words}, "{sentence}"),')
        new_emojis.append(f'    "{char}": "{emoji}",')
        if stroke:
            new_strokes.append(f'    "{char}": {stroke},')
        
        print(f"添加: {char} ({py}) {emoji}")
    
    if not new_chars:
        print("没有新字需要添加")
        return
    
    # 更新文件
    # 1. 添加到 CHARACTERS_LEVEL_3
    level_marker = "# 等级3：亲人和其他"
    if level_marker in content:
        # 找到等级3的结束位置（]之前）
        idx = content.find(level_marker)
        # 找到这个列表的结束 ]
        bracket_idx = content.find("\n]", idx)
        if bracket_idx > 0:
            insert_pos = bracket_idx
            new_content = content[:insert_pos] + "\n" + "\n".join(new_chars) + content[insert_pos:]
            content = new_content
    
    # 2. 添加到 CHAR_EMOJI_MAP
    emoji_marker = "CHAR_EMOJI_MAP = {"
    if emoji_marker in content and new_emojis:
        idx = content.find(emoji_marker)
        bracket_idx = content.find("\n}", idx)
        if bracket_idx > 0:
            insert_pos = bracket_idx
            new_content = content[:insert_pos] + "\n" + "\n".join(new_emojis) + content[insert_pos:]
            content = new_content
    
    # 3. 添加到 STROKE_DATA
    stroke_marker = "STROKE_DATA = {"
    if stroke_marker in content and new_strokes:
        idx = content.find(stroke_marker)
        # 找到最后一个字的笔顺数据后面
        bracket_idx = content.find("\n}", idx)
        if bracket_idx > 0:
            insert_pos = bracket_idx
            new_content = content[:insert_pos] + "\n" + "\n".join(new_strokes) + content[insert_pos:]
            content = new_content
    
    # 写回文件
    with open(db_path, 'w', encoding='utf-8') as f:
        f.write(content)
    
    print(f"\n✅ 成功添加 {len(new_chars)} 个新字到字库！")
    print("提示: 没有笔顺数据的字会在田字格中显示轮廓供练习")


def show_help():
    """显示帮助"""
    print("""
╔══════════════════════════════════════════════════╗
║          字库管理工具 - 一键添加新汉字           ║
╠══════════════════════════════════════════════════╣
║  用法:                                           ║
║    python add_words.py 花草鸟鱼                  ║
║    python add_words.py 春夏秋冬                  ║
║                                                  ║
║  功能:                                           ║
║    • 自动生成拼音（需安装pypinyin）              ║
║    • 自动匹配emoji                               ║
║    • 自动生成组词和造句                          ║
║    • 自动添加笔顺数据（如有）                    ║
║                                                  ║
║  文件:                                           ║
║    字库数据: word_database.py                    ║
╚══════════════════════════════════════════════════╝
""")


if __name__ == "__main__":
    if len(sys.argv) < 2:
        show_help()
    else:
        chars = "".join(sys.argv[1:])
        add_words_to_database(chars)
