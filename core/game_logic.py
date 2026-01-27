# -*- coding: utf-8 -*-
"""
游戏逻辑模块 - 与UI无关的纯逻辑
"""
import random
import time
from dataclasses import dataclass, field
from typing import List, Dict, Any, Optional, Callable
from enum import Enum


class GameType(Enum):
    """游戏类型枚举"""
    FLASHCARD = "flashcard"      # 卡片学习
    QUIZ = "quiz"                # 选择题
    LISTEN = "listen"           # 听音选择
    MATCH = "match"             # 配对
    WHACK = "whack"             # 打地鼠
    MEMORY = "memory"           # 记忆翻牌
    PATTERN = "pattern"         # 找规律
    CATEGORY = "category"       # 分类
    COMPARE = "compare"         # 比大小
    ADDITION = "addition"       # 加法
    CHALLENGE = "challenge"     # 限时挑战


@dataclass
class GameSession:
    """游戏会话，记录一局游戏的状态"""
    game_type: GameType
    level: int = 1
    score: int = 0
    correct_count: int = 0
    wrong_count: int = 0
    total_questions: int = 0
    current_question: int = 0
    start_time: float = field(default_factory=time.time)
    data: Dict[str, Any] = field(default_factory=dict)
    
    @property
    def accuracy(self) -> float:
        """正确率"""
        total = self.correct_count + self.wrong_count
        return self.correct_count / total if total > 0 else 0
    
    @property
    def elapsed_time(self) -> float:
        """已用时间（秒）"""
        return time.time() - self.start_time
    
    def add_correct(self, points: int = 10):
        """答对"""
        self.correct_count += 1
        self.score += points
        self.current_question += 1
    
    def add_wrong(self):
        """答错"""
        self.wrong_count += 1
        self.current_question += 1
    
    def is_complete(self) -> bool:
        """是否完成"""
        return self.current_question >= self.total_questions


class GameLogic:
    """游戏逻辑类 - 处理所有与UI无关的游戏逻辑"""
    
    def __init__(self):
        self.total_score = 0
        self.sessions: List[GameSession] = []
    
    # ==================== 通用逻辑 ====================
    
    def create_session(self, game_type: GameType, level: int = 1, 
                       total_questions: int = 10) -> GameSession:
        """创建新的游戏会话"""
        session = GameSession(
            game_type=game_type,
            level=level,
            total_questions=total_questions
        )
        self.sessions.append(session)
        return session
    
    def check_answer(self, session: GameSession, user_answer: Any, 
                     correct_answer: Any, points: int = 10) -> bool:
        """检查答案"""
        is_correct = user_answer == correct_answer
        if is_correct:
            session.add_correct(points)
            self.total_score += points
        else:
            session.add_wrong()
        return is_correct
    
    def get_random_options(self, correct: Any, all_items: List, 
                           count: int = 4) -> List:
        """生成随机选项（包含正确答案）"""
        options = [correct]
        others = [item for item in all_items if item != correct]
        options.extend(random.sample(others, min(count - 1, len(others))))
        random.shuffle(options)
        return options
    
    # ==================== 配对游戏逻辑 ====================
    
    def init_match_game(self, items: List, pairs: int = 6) -> Dict:
        """初始化配对游戏"""
        selected = random.sample(items, pairs)
        cards = []
        for i, item in enumerate(selected):
            cards.append({"id": i, "value": item, "matched": False})
            cards.append({"id": i, "value": item, "matched": False})
        random.shuffle(cards)
        return {
            "cards": cards,
            "flipped": [],
            "matched_pairs": 0,
            "total_pairs": pairs
        }
    
    def flip_card(self, game_data: Dict, card_index: int) -> Dict:
        """翻牌逻辑，返回结果"""
        cards = game_data["cards"]
        flipped = game_data["flipped"]
        
        # 已经翻开或已配对的牌不能再翻
        if cards[card_index]["matched"] or card_index in flipped:
            return {"action": "ignore"}
        
        flipped.append(card_index)
        
        if len(flipped) == 2:
            card1 = cards[flipped[0]]
            card2 = cards[flipped[1]]
            
            if card1["id"] == card2["id"]:
                # 配对成功
                card1["matched"] = True
                card2["matched"] = True
                game_data["matched_pairs"] += 1
                game_data["flipped"] = []
                
                is_complete = game_data["matched_pairs"] >= game_data["total_pairs"]
                return {"action": "match", "complete": is_complete}
            else:
                # 配对失败，需要翻回去
                return {"action": "no_match", "cards_to_flip_back": flipped.copy()}
        
        return {"action": "flip"}
    
    def reset_flipped(self, game_data: Dict):
        """重置翻开的牌"""
        game_data["flipped"] = []
    
    # ==================== 打地鼠逻辑 ====================
    
    def init_whack_game(self, items: List, holes: int = 9) -> Dict:
        """初始化打地鼠游戏"""
        return {
            "items": items,
            "holes": [None] * holes,
            "target": None,
            "score": 0,
            "round": 0,
            "max_rounds": 10
        }
    
    def spawn_moles(self, game_data: Dict, count: int = 3) -> int:
        """生成地鼠，返回目标位置"""
        items = game_data["items"]
        holes = game_data["holes"]
        
        # 清空所有洞
        for i in range(len(holes)):
            holes[i] = None
        
        # 随机选择位置
        positions = random.sample(range(len(holes)), count)
        
        # 随机选择目标
        target = random.choice(items)
        game_data["target"] = target
        
        # 放置地鼠
        target_pos = positions[0]
        holes[target_pos] = target
        
        for pos in positions[1:]:
            other = random.choice([i for i in items if i != target])
            holes[pos] = other
        
        game_data["round"] += 1
        return target_pos
    
    def whack(self, game_data: Dict, position: int) -> Dict:
        """打地鼠，返回结果"""
        holes = game_data["holes"]
        target = game_data["target"]
        
        if holes[position] == target:
            game_data["score"] += 10
            return {"hit": True, "score": 10}
        elif holes[position] is not None:
            return {"hit": False, "wrong": True}
        else:
            return {"hit": False, "miss": True}
    
    # ==================== 记忆翻牌逻辑 ====================
    
    def init_memory_game(self, items: List, pairs: int = 6) -> Dict:
        """初始化记忆翻牌游戏"""
        selected = random.sample(items, pairs)
        cards = selected * 2
        random.shuffle(cards)
        return {
            "cards": cards,
            "revealed": [False] * len(cards),
            "first_flip": None,
            "matched": 0,
            "total_pairs": pairs,
            "attempts": 0
        }
    
    def memory_flip(self, game_data: Dict, index: int) -> Dict:
        """记忆翻牌逻辑"""
        cards = game_data["cards"]
        revealed = game_data["revealed"]
        
        if revealed[index]:
            return {"action": "ignore"}
        
        revealed[index] = True
        
        if game_data["first_flip"] is None:
            game_data["first_flip"] = index
            return {"action": "first_flip", "card": cards[index]}
        else:
            first = game_data["first_flip"]
            game_data["first_flip"] = None
            game_data["attempts"] += 1
            
            if cards[first] == cards[index]:
                game_data["matched"] += 1
                is_complete = game_data["matched"] >= game_data["total_pairs"]
                return {
                    "action": "match", 
                    "card": cards[index],
                    "complete": is_complete
                }
            else:
                return {
                    "action": "no_match",
                    "cards_to_hide": [first, index]
                }
    
    def memory_hide_cards(self, game_data: Dict, indices: List[int]):
        """隐藏未配对的牌"""
        for i in indices:
            game_data["revealed"][i] = False
    
    # ==================== 计分和统计 ====================
    
    def get_praise_message(self, accuracy: float) -> str:
        """根据正确率获取表扬语"""
        if accuracy >= 0.9:
            return "太棒了！你是最聪明的小朋友！"
        elif accuracy >= 0.7:
            return "很好！继续加油！"
        elif accuracy >= 0.5:
            return "不错哦！再练习一下会更好！"
        else:
            return "没关系，多练习就会进步的！"
    
    def calculate_stars(self, session: GameSession) -> int:
        """计算获得的星星数"""
        if session.accuracy >= 0.9:
            return 3
        elif session.accuracy >= 0.7:
            return 2
        elif session.accuracy >= 0.5:
            return 1
        return 0
