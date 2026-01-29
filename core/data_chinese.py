# -*- coding: utf-8 -*-
"""
汉字数据模块 - 与UI无关的纯数据
64个精选汉字，适合4岁小朋友学习
"""

class ChineseData:
    """汉字数据类"""
    
    # 初级汉字 (16个): 自然+家人
    BASIC_WORDS = [
        ("日", "rì", "日出", "☀️"),
        ("天", "tiān", "天空", "🌤️"),
        ("月", "yuè", "月亮", "🌙"),
        ("风", "fēng", "大风", "🌬️"),
        ("爸", "bà", "爸爸", "👨"),
        ("妈", "mā", "妈妈", "👩"),
        ("宝", "bǎo", "宝宝", "👶"),
        ("姐", "jiě", "姐姐", "👧"),
        ("开", "kāi", "开门", "🚪"),
        ("关", "guān", "关门", "🔒"),
        ("地", "dì", "大地", "🌍"),
        ("里", "lǐ", "里面", "📦"),
        ("他", "tā", "他们", "👦"),
        ("工", "gōng", "工人", "👷"),
        ("儿", "ér", "儿子", "👦"),
        ("老", "lǎo", "老人", "👴"),
    ]
    
    # 中级汉字 (16个): 生活+亲属
    INTERMEDIATE_WORDS = [
        ("好", "hǎo", "好人", "👍"),
        ("饭", "fàn", "吃饭", "🍚"),
        ("看", "kàn", "看书", "👀"),
        ("玩", "wán", "玩耍", "🎮"),
        ("叔", "shū", "叔叔", "👨"),
        ("自", "zì", "自己", "🙋"),
        ("姑", "gū", "姑姑", "👩"),
        ("娘", "niáng", "姑娘", "👧"),
        ("火", "huǒ", "火焰", "🔥"),
        ("土", "tǔ", "泥土", "🟤"),
        ("水", "shuǐ", "喝水", "💧"),
        ("电", "diàn", "电视", "⚡"),
        ("木", "mù", "木头", "🪵"),
        ("比", "bǐ", "比赛", "🏆"),
        ("图", "tú", "图画", "🖼️"),
        ("树", "shù", "大树", "🌳"),
    ]
    
    # 高级汉字 (32个): 数字+动物+其他
    ADVANCED_WORDS = [
        ("一", "yī", "一个", "1️⃣"),
        ("三", "sān", "三个", "3️⃣"),
        ("四", "sì", "四个", "4️⃣"),
        ("五", "wǔ", "五个", "5️⃣"),
        ("羊", "yáng", "小羊", "🐑"),
        ("白", "bái", "白色", "⬜"),
        ("牛", "niú", "小牛", "🐄"),
        ("鼠", "shǔ", "老鼠", "🐭"),
        ("心", "xīn", "爱心", "❤️"),
        ("可", "kě", "可以", "✅"),
        ("说", "shuō", "说话", "💬"),
        ("两", "liǎng", "两个", "✌️"),
        ("男", "nán", "男孩", "👦"),
        ("你", "nǐ", "你好", "👋"),
        ("不", "bù", "不要", "🚫"),
        ("子", "zǐ", "孩子", "👶"),
        ("在", "zài", "在家", "🏠"),
        ("头", "tóu", "头发", "👤"),
        ("我", "wǒ", "我们", "🙋"),
        ("房", "fáng", "房子", "🏠"),
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
    def get_all_chars(cls):
        """获取所有汉字列表"""
        all_words = cls.get_words(level=3)
        return [item[0] for item in all_words]
    
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
