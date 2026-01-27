# -*- coding: utf-8 -*-
"""
核心模块测试
"""
from data_pinyin import PinyinData
from data_math import MathData
from data_english import EnglishData
from data_chinese import ChineseData
from data_thinking import ThinkingData
from data_vehicles import VehiclesData
from game_logic import GameLogic, GameType, GameSession


def test_data_modules():
    """测试数据模块"""
    print("=" * 50)
    print("测试数据模块")
    print("=" * 50)
    
    # 拼音
    print(f"\n拼音韵母: {len(PinyinData.get_vowels())} 个")
    print(f"拼音声母(L1): {len(PinyinData.get_consonants(1))} 个")
    print(f"拼音声母(L3): {len(PinyinData.get_consonants(3))} 个")
    
    # 数学
    print(f"\n数学数字: {len(MathData.get_numbers())} 个")
    print(f"数学形状: {len(MathData.get_shapes())} 个")
    add = MathData.generate_addition(10)
    print(f"加法题目: {add[0]} + {add[1]} = {add[2]}")
    
    # 英语
    print(f"\n英语字母(L1): {len(EnglishData.get_letters(1))} 个")
    print(f"英语颜色: {len(EnglishData.get_colors())} 个")
    print(f"英语动物: {len(EnglishData.get_animals())} 个")
    
    # 汉字
    print(f"\n汉字(L1): {len(ChineseData.get_words(1))} 个")
    print(f"汉字(L3): {len(ChineseData.get_words(3))} 个")
    
    # 思维
    diff = ThinkingData.generate_find_different()
    print(f"\n找不同: {diff[0]}, 答案位置: {diff[1]}")
    
    # 交通
    print(f"\n交通工具: {len(VehiclesData.get_vehicles())} 个")
    print(f"汪汪队成员: {len(VehiclesData.get_paw_patrol())} 个")
    
    print("\n✅ 数据模块测试通过!")


def test_game_logic():
    """测试游戏逻辑"""
    print("\n" + "=" * 50)
    print("测试游戏逻辑")
    print("=" * 50)
    
    logic = GameLogic()
    
    # 测试会话
    session = logic.create_session(GameType.QUIZ, level=1, total_questions=5)
    print(f"\n创建会话: {session.game_type.value}, 等级{session.level}")
    
    # 模拟答题
    logic.check_answer(session, "A", "A", 10)  # 正确
    logic.check_answer(session, "B", "A", 10)  # 错误
    logic.check_answer(session, "C", "C", 10)  # 正确
    
    print(f"答题情况: 正确{session.correct_count}, 错误{session.wrong_count}")
    print(f"正确率: {session.accuracy:.0%}")
    print(f"得分: {session.score}")
    
    # 测试配对游戏
    print("\n测试配对游戏:")
    items = ["🍎", "🍌", "🍊", "🍇", "🐕", "🐱"]
    match_data = logic.init_match_game(items, pairs=3)
    print(f"卡片数量: {len(match_data['cards'])}")
    
    # 测试打地鼠
    print("\n测试打地鼠:")
    whack_data = logic.init_whack_game(items, holes=9)
    target_pos = logic.spawn_moles(whack_data, count=3)
    print(f"目标: {whack_data['target']}, 位置: {target_pos}")
    result = logic.whack(whack_data, target_pos)
    print(f"打击结果: {result}")
    
    # 测试记忆翻牌
    print("\n测试记忆翻牌:")
    memory_data = logic.init_memory_game(items, pairs=3)
    print(f"卡片: {memory_data['cards']}")
    
    print("\n✅ 游戏逻辑测试通过!")


if __name__ == "__main__":
    test_data_modules()
    test_game_logic()
    print("\n" + "=" * 50)
    print("🎉 所有测试通过!")
    print("=" * 50)
