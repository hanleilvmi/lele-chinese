# -*- coding: utf-8 -*-
"""
汉字数据模块 - 与UI无关的纯数据
自动生成，请勿手动修改！如需添加汉字请编辑 汉字表.txt
"""

class ChineseData:
    """汉字数据类"""
    
    # 基础汉字: (汉字, 拼音, 词组, emoji)
    BASIC_WORDS = [
        ("人", "rén", "人们", "📝"),
        ("口", "kǒu", "口水", "📝"),
        ("手", "shǒu", "小手", "📝"),
        ("足", "zú", "足球", "📝"),
        ("日", "rì", "日出", "📝"),
        ("月", "yuè", "月亮", "📝"),
        ("水", "shuǐ", "喝水", "📝"),
        ("火", "huǒ", "火焰", "📝"),
        ("山", "shān", "高山", "📝"),
        ("石", "shí", "石头", "📝"),
        ("田", "tián", "田地", "📝"),
        ("土", "tǔ", "泥土", "📝"),
    ]
    
    # 进阶汉字
    INTERMEDIATE_WORDS = [
        ("大", "dà", "大小", "📝"),
        ("小", "xiǎo", "小鸟", "📝"),
        ("上", "shàng", "上面", "📝"),
        ("下", "xià", "下面", "📝"),
        ("左", "zuǒ", "左边", "📝"),
        ("右", "yòu", "右边", "📝"),
        ("天", "tiān", "天空", "📝"),
        ("地", "dì", "大地", "📝"),
        ("花", "huā", "鲜花", "📝"),
        ("草", "cǎo", "小草", "📝"),
        ("树", "shù", "大树", "📝"),
        ("鸟", "niǎo", "小鸟", "📝"),
    ]
    
    # 高级汉字
    ADVANCED_WORDS = [
        ("爸", "bà", "爸爸", "📝"),
        ("妈", "mā", "妈妈", "📝"),
        ("爷", "yé", "爷爷", "📝"),
        ("奶", "nǎi", "奶奶", "📝"),
        ("哥", "gē", "哥哥", "📝"),
        ("姐", "jiě", "姐姐", "📝"),
        ("弟", "dì", "弟弟", "📝"),
        ("妹", "mèi", "妹妹", "📝"),
        ("吃", "chī", "吃饭", "📝"),
        ("喝", "hē", "喝水", "📝"),
        ("看", "kàn", "看书", "📝"),
        ("听", "tīng", "听歌", "📝"),
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
