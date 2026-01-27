# -*- coding: utf-8 -*-
"""
数学数据模块 - 与UI无关的纯数据
"""
import random

class MathData:
    """数学数据类"""
    
    # 数字数据: (数字, 中文, emoji表示)
    NUMBERS = [
        (1, "一", "🍎"),
        (2, "二", "🍎🍎"),
        (3, "三", "🍎🍎🍎"),
        (4, "四", "🍎🍎🍎🍎"),
        (5, "五", "🍎🍎🍎🍎🍎"),
        (6, "六", "🍎🍎🍎🍎🍎🍎"),
        (7, "七", "🍎🍎🍎🍎🍎🍎🍎"),
        (8, "八", "🍎🍎🍎🍎🍎🍎🍎🍎"),
        (9, "九", "🍎🍎🍎🍎🍎🍎🍎🍎🍎"),
        (10, "十", "🍎🍎🍎🍎🍎🍎🍎🍎🍎🍎"),
    ]
    
    # 形状数据: (名称, 边数, 颜色, emoji)
    SHAPES = [
        ("圆形", 0, "#FF6B6B", "⭕"),
        ("三角形", 3, "#4ECDC4", "🔺"),
        ("正方形", 4, "#45B7D1", "🟦"),
        ("长方形", 4, "#96CEB4", "🟩"),
        ("五角星", 5, "#FFD93D", "⭐"),
        ("心形", 0, "#FF69B4", "❤️"),
    ]
    
    # 水果emoji列表（用于数数）
    COUNTING_ITEMS = ["🍎", "🍌", "🍊", "🍇", "🍓", "🍑", "🍐", "🍉"]
    
    @classmethod
    def get_numbers(cls, max_num=10):
        """获取数字数据"""
        return [n for n in cls.NUMBERS if n[0] <= max_num]
    
    @classmethod
    def get_shapes(cls):
        """获取形状数据"""
        return cls.SHAPES.copy()
    
    @classmethod
    def get_max_number_by_level(cls, level):
        """根据等级获取最大数字"""
        return {1: 10, 2: 15, 3: 20}.get(level, 10)
    
    @classmethod
    def generate_addition(cls, max_num=10):
        """生成加法题目，返回 (a, b, answer)"""
        a = random.randint(1, max_num // 2)
        b = random.randint(1, max_num - a)
        return (a, b, a + b)
    
    @classmethod
    def generate_compare(cls, max_num=10):
        """生成比大小题目，返回 (a, b, answer)，answer: '>' '<' '='"""
        a = random.randint(1, max_num)
        b = random.randint(1, max_num)
        if a > b:
            answer = '>'
        elif a < b:
            answer = '<'
        else:
            answer = '='
        return (a, b, answer)
    
    @classmethod
    def generate_counting(cls, max_count=10):
        """生成数数题目，返回 (emoji, count)"""
        emoji = random.choice(cls.COUNTING_ITEMS)
        count = random.randint(1, max_count)
        return (emoji, count)
