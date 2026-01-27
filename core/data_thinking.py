# -*- coding: utf-8 -*-
"""
思维训练数据模块 - 与UI无关的纯数据
"""
import random

class ThinkingData:
    """思维训练数据类"""
    
    # 分类数据: (类别名, 物品列表)
    CATEGORIES = [
        ("水果", ["🍎", "🍌", "🍊", "🍇", "🍓", "🍑", "🍐", "🍉", "🍒", "🥝"]),
        ("动物", ["🐕", "🐱", "🐰", "🐻", "🦁", "🐘", "🐵", "🐼", "🐯", "🦊"]),
        ("交通工具", ["🚗", "🚌", "🚂", "✈️", "🚢", "🚁", "🚲", "🛵", "🚀", "🚒"]),
        ("食物", ["🍔", "🍕", "🍜", "🍣", "🍰", "🍦", "🍩", "🍪", "🥪", "🌮"]),
        ("植物", ["🌸", "🌻", "🌹", "🌷", "🌺", "🌼", "🌿", "🍀", "🌳", "🌴"]),
        ("天气", ["☀️", "🌧️", "⛈️", "🌈", "❄️", "🌪️", "🌤️", "⛅", "🌙", "⭐"]),
    ]
    
    # 形状颜色（用于找不同、规律等）
    SHAPES = ["⭕", "🔺", "🟦", "🟩", "⬛", "🔶", "🔷", "⬜"]
    COLORS = ["🔴", "🟠", "🟡", "🟢", "🔵", "🟣", "⚫", "⚪"]
    
    # 记忆卡片图案
    MEMORY_CARDS = ["🍎", "🍌", "🍊", "🍇", "🐕", "🐱", "🚗", "✈️", "⭐", "❤️", "🌸", "🌙"]
    
    @classmethod
    def get_categories(cls):
        """获取所有分类"""
        return cls.CATEGORIES.copy()
    
    @classmethod
    def generate_find_different(cls, count=4):
        """
        生成找不同题目
        返回: (items_list, different_index)
        """
        base = random.choice(cls.SHAPES)
        items = [base] * count
        diff_idx = random.randint(0, count - 1)
        different = random.choice([s for s in cls.SHAPES if s != base])
        items[diff_idx] = different
        return (items, diff_idx)
    
    @classmethod
    def generate_pattern(cls, length=4):
        """
        生成规律题目
        返回: (pattern_list, answer, options)
        """
        # 简单的AB规律
        a, b = random.sample(cls.SHAPES, 2)
        pattern = []
        for i in range(length):
            pattern.append(a if i % 2 == 0 else b)
        answer = a if length % 2 == 0 else b
        options = random.sample(cls.SHAPES, 4)
        if answer not in options:
            options[0] = answer
        random.shuffle(options)
        return (pattern, answer, options)
    
    @classmethod
    def generate_category_question(cls):
        """
        生成分类题目
        返回: (category_name, correct_items, wrong_item)
        """
        cat_name, cat_items = random.choice(cls.CATEGORIES)
        correct = random.sample(cat_items, 3)
        other_cats = [c for c in cls.CATEGORIES if c[0] != cat_name]
        wrong_cat = random.choice(other_cats)
        wrong = random.choice(wrong_cat[1])
        return (cat_name, correct, wrong)
    
    @classmethod
    def generate_memory_cards(cls, pairs=6):
        """
        生成记忆翻牌卡片
        返回: 打乱的卡片列表（每个图案出现2次）
        """
        selected = random.sample(cls.MEMORY_CARDS, pairs)
        cards = selected * 2
        random.shuffle(cards)
        return cards
    
    @classmethod
    def generate_matching_pairs(cls, count=6):
        """
        生成配对题目
        返回: [(item, item), ...]
        """
        items = random.sample(cls.MEMORY_CARDS, count)
        return [(item, item) for item in items]
