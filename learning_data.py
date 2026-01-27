# -*- coding: utf-8 -*-
"""
学习数据管理模块 v1.2
统一管理学习进度、错题记录、奖励系统
优化：使用BatchSaver减少频繁IO
优化：使用ui_config统一路径管理
"""

import json
import os
import atexit
from datetime import datetime, date, timedelta

# 尝试导入UI配置模块
try:
    from ui_config import get_data_path, get_path
    UI_CONFIG_AVAILABLE = True
except ImportError:
    UI_CONFIG_AVAILABLE = False

# 数据文件路径
if UI_CONFIG_AVAILABLE:
    DATA_DIR = get_path()
    PROGRESS_FILE = get_data_path("learning_progress.json")
else:
    DATA_DIR = os.path.dirname(os.path.abspath(__file__))
    PROGRESS_FILE = os.path.join(DATA_DIR, "learning_progress.json")

# 尝试导入BatchSaver
try:
    from learning_base import BatchSaver
    BATCH_SAVER_AVAILABLE = True
except ImportError:
    BATCH_SAVER_AVAILABLE = False

# 默认数据结构
DEFAULT_DATA = {
    "user_info": {
        "name": "乐乐",
        "age": 3,
        "created_date": ""
    },
    "overall": {
        "total_score": 0,
        "total_correct": 0,
        "total_wrong": 0,
        "days_learned": 0,
        "last_date": "",
        "total_time_minutes": 0
    },
    "modules": {
        "literacy": {"score": 0, "correct": 0, "wrong": 0, "time": 0, "level": 1},
        "pinyin": {"score": 0, "correct": 0, "wrong": 0, "time": 0, "level": 1},
        "math": {"score": 0, "correct": 0, "wrong": 0, "time": 0, "level": 1},
        "english": {"score": 0, "correct": 0, "wrong": 0, "time": 0, "level": 1},
        "thinking": {"score": 0, "correct": 0, "wrong": 0, "time": 0, "level": 1},
        "vehicles": {"score": 0, "correct": 0, "wrong": 0, "time": 0, "level": 1}
    },
    "rewards": {
        "stars": 0,
        "badges": [],
        "achievements": []
    },
    "wrong_questions": {
        "literacy": [],
        "pinyin": [],
        "math": [],
        "english": []
    },
    "daily_records": [],
    "mastered_items": {
        "characters": [],
        "pinyin": [],
        "english_words": [],
        "numbers": [],
        "shapes": []
    },
    "daily_plan": {
        "target_questions": 30,      # 每日目标答题数
        "target_minutes": 20,        # 每日目标学习时长（分钟）
        "rest_reminder": 15,         # 休息提醒间隔（分钟）
        "today_questions": 0,        # 今日已答题数
        "today_correct": 0,          # 今日答对数
        "today_minutes": 0,          # 今日学习时长
        "today_date": "",            # 今日日期
        "last_rest_reminder": ""     # 上次休息提醒时间
    },
    "review_items": {
        # 艾宾浩斯复习记录
        # 格式: {"item": "内容", "category": "类别", "learn_date": "首次学习日期", 
        #        "review_count": 复习次数, "next_review": "下次复习日期", "ease_factor": 难度系数}
        "literacy": [],   # 识字复习
        "pinyin": [],     # 拼音复习
        "english": [],    # 英语复习
        "math": []        # 数学复习
    },
    "parent_settings": {
        "password": "",              # 家长密码（空表示未设置）
        "daily_time_limit": 60,      # 每日学习时间限制（分钟），0表示不限制
        "session_time_limit": 30,    # 单次学习时间限制（分钟），0表示不限制
        "allowed_hours_start": 8,    # 允许学习的开始时间（小时）
        "allowed_hours_end": 21,     # 允许学习的结束时间（小时）
        "weekend_extra_time": 15,    # 周末额外时间（分钟）
        "lock_after_limit": False,   # 达到时间限制后是否锁定
        "show_answers": True,        # 是否显示答案提示
        "difficulty_lock": False,    # 是否锁定难度（防止孩子调整）
        "notifications": []          # 家长通知记录
    },
    "daily_challenges": {
        "date": "",                  # 挑战日期
        "challenges": [],            # 今日挑战列表
        "completed": [],             # 已完成的挑战ID
        "streak": 0,                 # 连续完成天数
        "total_completed": 0         # 累计完成挑战数
    }
}

# 徽章定义
BADGES = {
    "first_star": {"name": "初露锋芒", "desc": "获得第一颗星星", "emoji": "🌟", "condition": lambda d: d["rewards"]["stars"] >= 1},
    "ten_stars": {"name": "小小明星", "desc": "累计获得10颗星星", "emoji": "⭐", "condition": lambda d: d["rewards"]["stars"] >= 10},
    "fifty_stars": {"name": "闪耀之星", "desc": "累计获得50颗星星", "emoji": "🌠", "condition": lambda d: d["rewards"]["stars"] >= 50},
    "hundred_stars": {"name": "超级巨星", "desc": "累计获得100颗星星", "emoji": "💫", "condition": lambda d: d["rewards"]["stars"] >= 100},
    "first_day": {"name": "学习起步", "desc": "完成第一天学习", "emoji": "📚", "condition": lambda d: d["overall"]["days_learned"] >= 1},
    "seven_days": {"name": "坚持一周", "desc": "累计学习7天", "emoji": "📅", "condition": lambda d: d["overall"]["days_learned"] >= 7},
    "thirty_days": {"name": "学习达人", "desc": "累计学习30天", "emoji": "🏆", "condition": lambda d: d["overall"]["days_learned"] >= 30},
    "perfect_ten": {"name": "完美十连", "desc": "连续答对10题", "emoji": "🎯", "condition": lambda d: d.get("current_streak", 0) >= 10},
    "literacy_master": {"name": "识字小能手", "desc": "识字正确率达到90%", "emoji": "📖", "condition": lambda d: _calc_accuracy(d, "literacy") >= 90},
    "math_master": {"name": "数学小天才", "desc": "数学正确率达到90%", "emoji": "🔢", "condition": lambda d: _calc_accuracy(d, "math") >= 90},
    "english_master": {"name": "英语小达人", "desc": "英语正确率达到90%", "emoji": "🔤", "condition": lambda d: _calc_accuracy(d, "english") >= 90},
    "all_rounder": {"name": "全能宝宝", "desc": "所有模块都学习过", "emoji": "🎖️", "condition": lambda d: all(m["correct"] > 0 for m in d["modules"].values())},
    "daily_goal": {"name": "今日之星", "desc": "完成每日学习目标", "emoji": "🌈", "condition": lambda d: d.get("daily_plan", {}).get("today_questions", 0) >= d.get("daily_plan", {}).get("target_questions", 30)},
    "early_bird": {"name": "早起鸟儿", "desc": "早上9点前开始学习", "emoji": "🐦", "condition": lambda d: d.get("early_bird_achieved", False)},
    "night_owl": {"name": "学习小夜猫", "desc": "晚上学习并完成目标", "emoji": "🦉", "condition": lambda d: d.get("night_owl_achieved", False)},
    # 新增挑战相关徽章
    "challenge_first": {"name": "挑战新手", "desc": "完成第一个每日挑战", "emoji": "🎪", "condition": lambda d: d.get("daily_challenges", {}).get("total_completed", 0) >= 1},
    "challenge_week": {"name": "挑战达人", "desc": "连续7天完成挑战", "emoji": "🏅", "condition": lambda d: d.get("daily_challenges", {}).get("streak", 0) >= 7},
    "challenge_master": {"name": "挑战大师", "desc": "累计完成50个挑战", "emoji": "👑", "condition": lambda d: d.get("daily_challenges", {}).get("total_completed", 0) >= 50},
    "speed_demon": {"name": "闪电侠", "desc": "5分钟内答对10题", "emoji": "⚡", "condition": lambda d: d.get("speed_achievement", False)},
    "explorer": {"name": "探索家", "desc": "尝试所有6种游戏模式", "emoji": "🧭", "condition": lambda d: len(d.get("explored_modes", [])) >= 6},
    "two_hundred_stars": {"name": "星光璀璨", "desc": "累计获得200颗星星", "emoji": "✨", "condition": lambda d: d["rewards"]["stars"] >= 200},
}

# 每日挑战模板
DAILY_CHALLENGE_TEMPLATES = [
    {"id": "answer_10", "name": "答题小能手", "desc": "今天答对10道题", "target": 10, "type": "correct", "reward_stars": 2, "emoji": "📝"},
    {"id": "answer_20", "name": "答题达人", "desc": "今天答对20道题", "target": 20, "type": "correct", "reward_stars": 3, "emoji": "📚"},
    {"id": "streak_5", "name": "连胜挑战", "desc": "连续答对5道题", "target": 5, "type": "streak", "reward_stars": 2, "emoji": "🔥"},
    {"id": "literacy_5", "name": "识字小达人", "desc": "识字答对5道题", "target": 5, "type": "module_correct", "module": "literacy", "reward_stars": 2, "emoji": "📖"},
    {"id": "math_5", "name": "数学小天才", "desc": "数学答对5道题", "target": 5, "type": "module_correct", "module": "math", "reward_stars": 2, "emoji": "🔢"},
    {"id": "english_5", "name": "英语小明星", "desc": "英语答对5道题", "target": 5, "type": "module_correct", "module": "english", "reward_stars": 2, "emoji": "🔤"},
    {"id": "pinyin_5", "name": "拼音小专家", "desc": "拼音答对5道题", "target": 5, "type": "module_correct", "module": "pinyin", "reward_stars": 2, "emoji": "🗣️"},
    {"id": "thinking_3", "name": "思维小达人", "desc": "思维答对3道题", "target": 3, "type": "module_correct", "module": "thinking", "reward_stars": 2, "emoji": "🧠"},
    {"id": "time_10", "name": "坚持学习", "desc": "学习满10分钟", "target": 10, "type": "time", "reward_stars": 2, "emoji": "⏰"},
    {"id": "time_15", "name": "学习小达人", "desc": "学习满15分钟", "target": 15, "type": "time", "reward_stars": 3, "emoji": "⏱️"},
    {"id": "review_3", "name": "复习小能手", "desc": "完成3项复习", "target": 3, "type": "review", "reward_stars": 2, "emoji": "🔄"},
    {"id": "perfect_5", "name": "完美答题", "desc": "连续答对5题不出错", "target": 5, "type": "perfect", "reward_stars": 3, "emoji": "💯"},
]

def _calc_accuracy(data, module):
    """计算模块正确率"""
    m = data["modules"].get(module, {})
    total = m.get("correct", 0) + m.get("wrong", 0)
    if total == 0:
        return 0
    return int(m.get("correct", 0) / total * 100)


import threading

class LearningData:
    """学习数据管理类 - 线程安全的单例"""
    
    _instance = None
    _lock = threading.Lock()  # 线程安全锁
    
    def __new__(cls):
        # 双重检查锁定模式
        if cls._instance is None:
            with cls._lock:
                if cls._instance is None:
                    cls._instance = super().__new__(cls)
                    cls._instance._initialized = False
        return cls._instance
    
    def __init__(self):
        if self._initialized:
            return
        self._initialized = True
        self._data_lock = threading.Lock()  # 数据访问锁
        self.data = self._load_data()
        self.session_start = datetime.now()
        self.current_streak = 0  # 当前连续答对数
        self._dirty = False  # 数据是否已修改
        
        # 初始化BatchSaver
        if BATCH_SAVER_AVAILABLE:
            self._batch_saver = BatchSaver(self._do_save, interval_seconds=30)
        else:
            self._batch_saver = None
        
        # 注册退出时保存
        atexit.register(self.force_save)
    
    def _load_data(self):
        """加载数据"""
        try:
            if os.path.exists(PROGRESS_FILE):
                with open(PROGRESS_FILE, 'r', encoding='utf-8') as f:
                    data = json.load(f)
                    # 合并默认值（处理新增字段）
                    return self._merge_defaults(data)
        except Exception as e:
            print(f"加载数据失败: {e}")
        
        # 返回默认数据
        data = DEFAULT_DATA.copy()
        data["user_info"]["created_date"] = date.today().isoformat()
        return data
    
    def _merge_defaults(self, data):
        """合并默认值，确保所有字段存在"""
        import copy
        result = copy.deepcopy(DEFAULT_DATA)
        
        def merge(default, loaded):
            if isinstance(default, dict) and isinstance(loaded, dict):
                for key in default:
                    if key in loaded:
                        default[key] = merge(default[key], loaded[key])
                for key in loaded:
                    if key not in default:
                        default[key] = loaded[key]
                return default
            return loaded
        
        return merge(result, data)
    
    def save(self):
        """保存数据（使用BatchSaver优化）"""
        self._dirty = True
        if self._batch_saver:
            self._batch_saver.mark_dirty()
        else:
            self._do_save()
    
    def _do_save(self):
        """实际执行保存（带备份机制）"""
        if not self._dirty:
            return
        
        with self._data_lock:
            try:
                # 先创建备份
                backup_file = PROGRESS_FILE + ".bak"
                if os.path.exists(PROGRESS_FILE):
                    try:
                        import shutil
                        shutil.copy2(PROGRESS_FILE, backup_file)
                    except Exception as e:
                        print(f"创建备份失败: {e}")
                
                # 写入临时文件
                temp_file = PROGRESS_FILE + ".tmp"
                with open(temp_file, 'w', encoding='utf-8') as f:
                    json.dump(self.data, f, ensure_ascii=False, indent=2)
                
                # 验证写入的数据
                with open(temp_file, 'r', encoding='utf-8') as f:
                    json.load(f)  # 验证 JSON 格式正确
                
                # 替换原文件
                if os.path.exists(PROGRESS_FILE):
                    os.remove(PROGRESS_FILE)
                os.rename(temp_file, PROGRESS_FILE)
                
                self._dirty = False
            except Exception as e:
                print(f"保存数据失败: {e}")
                # 尝试从备份恢复
                if os.path.exists(backup_file):
                    try:
                        import shutil
                        shutil.copy2(backup_file, PROGRESS_FILE)
                        print("已从备份恢复数据")
                    except:
                        pass
    
    def force_save(self):
        """强制立即保存（退出时调用）"""
        if self._batch_saver:
            self._batch_saver.force_save()
        elif self._dirty:
            self._do_save()
    
    def check_daily_login(self):
        """检查每日登录，更新学习天数"""
        today = date.today().isoformat()
        if self.data["overall"]["last_date"] != today:
            self.data["overall"]["days_learned"] += 1
            self.data["overall"]["last_date"] = today
            self.save()
            return True  # 新的一天
        return False
    
    def add_score(self, module, points, is_correct):
        """添加分数
        
        Args:
            module: 模块名称 (literacy, pinyin, math, english, thinking, vehicles)
            points: 得分（必须为非负整数）
            is_correct: 是否正确
        
        Returns:
            list: 新获得的徽章列表
        """
        # 参数验证
        valid_modules = ["literacy", "pinyin", "math", "english", "thinking", "vehicles"]
        if module not in valid_modules:
            print(f"警告: 无效的模块名称 '{module}'，有效值: {valid_modules}")
            return []
        
        if not isinstance(points, (int, float)) or points < 0:
            print(f"警告: 无效的分数 '{points}'，必须为非负数")
            points = max(0, int(points)) if isinstance(points, (int, float)) else 0
        
        with self._data_lock:
            # 更新模块数据
            if module in self.data["modules"]:
                self.data["modules"][module]["score"] += points
                if is_correct:
                    self.data["modules"][module]["correct"] += 1
                    self.current_streak += 1
                else:
                    self.data["modules"][module]["wrong"] += 1
                    self.current_streak = 0
            
            # 更新总体数据
            self.data["overall"]["total_score"] += points
            if is_correct:
                self.data["overall"]["total_correct"] += 1
            else:
                self.data["overall"]["total_wrong"] += 1
            
            # 更新每日计划数据
            self.add_today_question(is_correct)
            
            # 检查时间相关成就
            self.check_time_achievements()
            
            # 检查是否获得星星（每答对3题得1星）
            if is_correct and self.data["overall"]["total_correct"] % 3 == 0:
                self.data["rewards"]["stars"] += 1
            
            # 检查并更新难度等级（每答5题检查一次）
            if module in self.data["modules"]:
                m = self.data["modules"][module]
                total = m["correct"] + m["wrong"]
                if total > 0 and total % 5 == 0:
                    self.update_level(module)
            
            # 检查每日挑战完成状态
            self.check_challenge_completion()
            
            # 检查新徽章
            new_badges = self._check_new_badges()
        
        self.save()
        return new_badges
    
    def _check_new_badges(self):
        """检查是否获得新徽章"""
        new_badges = []
        self.data["current_streak"] = self.current_streak
        
        for badge_id, badge_info in BADGES.items():
            if badge_id not in self.data["rewards"]["badges"]:
                try:
                    if badge_info["condition"](self.data):
                        self.data["rewards"]["badges"].append(badge_id)
                        new_badges.append(badge_info)
                except:
                    pass
        
        return new_badges
    
    def add_wrong_question(self, module, question_data):
        """添加错题"""
        if module in self.data["wrong_questions"]:
            # 避免重复
            for q in self.data["wrong_questions"][module]:
                if q.get("question") == question_data.get("question"):
                    q["wrong_count"] = q.get("wrong_count", 1) + 1
                    self.save()
                    return
            
            question_data["wrong_count"] = 1
            question_data["added_date"] = date.today().isoformat()
            self.data["wrong_questions"][module].append(question_data)
            
            # 最多保留50道错题
            if len(self.data["wrong_questions"][module]) > 50:
                self.data["wrong_questions"][module] = self.data["wrong_questions"][module][-50:]
            
            self.save()
    
    def remove_wrong_question(self, module, question):
        """移除错题（答对后）"""
        if module in self.data["wrong_questions"]:
            self.data["wrong_questions"][module] = [
                q for q in self.data["wrong_questions"][module] 
                if q.get("question") != question
            ]
            self.save()
    
    def get_wrong_questions(self, module):
        """获取错题列表"""
        return self.data["wrong_questions"].get(module, [])
    
    def add_mastered_item(self, category, item):
        """添加已掌握的内容"""
        if category in self.data["mastered_items"]:
            if item not in self.data["mastered_items"][category]:
                self.data["mastered_items"][category].append(item)
                self.save()
    
    def get_mastered_items(self, category):
        """获取已掌握的内容"""
        return self.data["mastered_items"].get(category, [])
    
    def get_level(self, module):
        """获取模块难度等级"""
        return self.data["modules"].get(module, {}).get("level", 1)
    
    def update_level(self, module):
        """根据正确率自动调整难度"""
        if module not in self.data["modules"]:
            return None
        
        m = self.data["modules"][module]
        total = m["correct"] + m["wrong"]
        
        if total < 5:  # 至少答5题才调整
            return None
        
        # 计算最近的正确率（使用总体数据，但考虑最近表现）
        accuracy = m["correct"] / total * 100
        current_level = m.get("level", 1)
        
        # 根据正确率调整等级
        # 正确率>=80%且答题>=10题，升级
        if accuracy >= 80 and total >= 10 and current_level < 3:
            m["level"] = current_level + 1
            self.save()
            return "up"
        # 正确率<50%且答题>=8题，降级
        elif accuracy < 50 and total >= 8 and current_level > 1:
            m["level"] = current_level - 1
            self.save()
            return "down"
        
        return None
    
    def set_level(self, module, level):
        """手动设置难度等级（家长功能）"""
        if module in self.data["modules"]:
            self.data["modules"][module]["level"] = max(1, min(3, level))
            self.save()
    
    def get_stats(self, module=None):
        """获取统计数据"""
        if module:
            m = self.data["modules"].get(module, {})
            total = m.get("correct", 0) + m.get("wrong", 0)
            accuracy = int(m.get("correct", 0) / total * 100) if total > 0 else 0
            return {
                "score": m.get("score", 0),
                "correct": m.get("correct", 0),
                "wrong": m.get("wrong", 0),
                "total": total,
                "accuracy": accuracy,
                "level": m.get("level", 1)
            }
        else:
            o = self.data["overall"]
            total = o.get("total_correct", 0) + o.get("total_wrong", 0)
            accuracy = int(o.get("total_correct", 0) / total * 100) if total > 0 else 0
            return {
                "score": o.get("total_score", 0),
                "correct": o.get("total_correct", 0),
                "wrong": o.get("total_wrong", 0),
                "total": total,
                "accuracy": accuracy,
                "days": o.get("days_learned", 0),
                "stars": self.data["rewards"]["stars"],
                "badges": len(self.data["rewards"]["badges"])
            }
    
    def get_badges(self):
        """获取已获得的徽章"""
        result = []
        for badge_id in self.data["rewards"]["badges"]:
            if badge_id in BADGES:
                badge = BADGES[badge_id].copy()
                badge["id"] = badge_id
                del badge["condition"]
                result.append(badge)
        return result
    
    def get_all_badges(self):
        """获取所有徽章（包括未获得的）"""
        result = []
        for badge_id, badge_info in BADGES.items():
            badge = {
                "id": badge_id,
                "name": badge_info["name"],
                "desc": badge_info["desc"],
                "emoji": badge_info["emoji"],
                "unlocked": badge_id in self.data["rewards"]["badges"]
            }
            result.append(badge)
        return result
    
    def get_stars(self):
        """获取星星数量"""
        return self.data["rewards"]["stars"]
    
    def end_session(self):
        """结束学习会话，记录时长"""
        duration = (datetime.now() - self.session_start).seconds // 60
        if duration > 0:
            self.data["overall"]["total_time_minutes"] += duration
            
            # 更新今日学习时长
            self._update_today_minutes(duration)
            
            # 记录每日学习
            today = date.today().isoformat()
            daily = next((d for d in self.data["daily_records"] if d["date"] == today), None)
            if daily:
                daily["minutes"] += duration
            else:
                self.data["daily_records"].append({
                    "date": today,
                    "minutes": duration
                })
            
            # 只保留最近30天记录
            self.data["daily_records"] = self.data["daily_records"][-30:]
            self.save()
    
    # =====================================================
    # 每日学习计划相关方法
    # =====================================================
    
    def _reset_daily_plan_if_needed(self):
        """如果是新的一天，重置每日计划数据"""
        today = date.today().isoformat()
        if self.data["daily_plan"]["today_date"] != today:
            self.data["daily_plan"]["today_questions"] = 0
            self.data["daily_plan"]["today_correct"] = 0
            self.data["daily_plan"]["today_minutes"] = 0
            self.data["daily_plan"]["today_date"] = today
            self.data["daily_plan"]["last_rest_reminder"] = ""
            self.save()
    
    def _update_today_minutes(self, minutes):
        """更新今日学习时长"""
        self._reset_daily_plan_if_needed()
        self.data["daily_plan"]["today_minutes"] += minutes
        self.save()
    
    def add_today_question(self, is_correct):
        """记录今日答题"""
        self._reset_daily_plan_if_needed()
        self.data["daily_plan"]["today_questions"] += 1
        if is_correct:
            self.data["daily_plan"]["today_correct"] += 1
        self.save()
    
    def get_daily_plan(self):
        """获取每日计划数据"""
        self._reset_daily_plan_if_needed()
        plan = self.data["daily_plan"]
        
        # 计算进度百分比
        q_progress = min(100, int(plan["today_questions"] / plan["target_questions"] * 100)) if plan["target_questions"] > 0 else 0
        
        # 计算今日学习时长（包括当前会话）
        session_minutes = (datetime.now() - self.session_start).seconds // 60
        total_today_minutes = plan["today_minutes"] + session_minutes
        
        return {
            "target_questions": plan["target_questions"],
            "target_minutes": plan["target_minutes"],
            "rest_reminder": plan["rest_reminder"],
            "today_questions": plan["today_questions"],
            "today_correct": plan["today_correct"],
            "today_minutes": total_today_minutes,
            "question_progress": q_progress,
            "goal_completed": plan["today_questions"] >= plan["target_questions"],
            "session_minutes": session_minutes
        }
    
    def set_daily_targets(self, target_questions=None, target_minutes=None, rest_reminder=None):
        """设置每日目标"""
        if target_questions is not None:
            self.data["daily_plan"]["target_questions"] = target_questions
        if target_minutes is not None:
            self.data["daily_plan"]["target_minutes"] = target_minutes
        if rest_reminder is not None:
            self.data["daily_plan"]["rest_reminder"] = rest_reminder
        self.save()
    
    def should_show_rest_reminder(self):
        """检查是否应该显示休息提醒"""
        plan = self.data["daily_plan"]
        rest_interval = plan["rest_reminder"]
        
        if rest_interval <= 0:
            return False
        
        session_minutes = (datetime.now() - self.session_start).seconds // 60
        
        # 检查是否达到休息提醒间隔
        if session_minutes > 0 and session_minutes % rest_interval == 0:
            # 检查是否已经提醒过
            last_reminder = plan.get("last_rest_reminder", "")
            current_reminder_key = f"{date.today().isoformat()}_{session_minutes // rest_interval}"
            
            if last_reminder != current_reminder_key:
                self.data["daily_plan"]["last_rest_reminder"] = current_reminder_key
                self.save()
                return True
        
        return False
    
    def get_session_minutes(self):
        """获取当前会话学习时长（分钟）"""
        return (datetime.now() - self.session_start).seconds // 60
    
    def check_time_achievements(self):
        """检查时间相关成就"""
        hour = datetime.now().hour
        
        # 早起鸟儿（9点前）
        if hour < 9 and not self.data.get("early_bird_achieved", False):
            self.data["early_bird_achieved"] = True
            self.save()
        
        # 学习小夜猫（晚上8点后且完成目标）
        if hour >= 20:
            plan = self.get_daily_plan()
            if plan["goal_completed"] and not self.data.get("night_owl_achieved", False):
                self.data["night_owl_achieved"] = True
                self.save()
    
    # =====================================================
    # 艾宾浩斯智能复习系统
    # =====================================================
    
    # 艾宾浩斯复习间隔（天数）：1, 2, 4, 7, 15, 30
    REVIEW_INTERVALS = [1, 2, 4, 7, 15, 30]
    
    def add_review_item(self, category, item, display_name=None):
        """添加需要复习的内容
        
        Args:
            category: 类别 (literacy, pinyin, english, math)
            item: 内容标识
            display_name: 显示名称（可选）
        """
        if "review_items" not in self.data:
            self.data["review_items"] = {"literacy": [], "pinyin": [], "english": [], "math": []}
        
        if category not in self.data["review_items"]:
            self.data["review_items"][category] = []
        
        # 检查是否已存在
        for r in self.data["review_items"][category]:
            if r["item"] == item:
                return  # 已存在，不重复添加
        
        today = date.today().isoformat()
        next_review = (date.today() + timedelta(days=1)).isoformat()  # 第一次复习在1天后
        
        review_data = {
            "item": item,
            "display_name": display_name or item,
            "category": category,
            "learn_date": today,
            "review_count": 0,
            "next_review": next_review,
            "ease_factor": 2.5,  # 初始难度系数
            "correct_streak": 0  # 连续答对次数
        }
        
        self.data["review_items"][category].append(review_data)
        self.save()
    
    def update_review_item(self, category, item, is_correct):
        """更新复习项目状态
        
        Args:
            category: 类别
            item: 内容标识
            is_correct: 是否答对
        
        Returns:
            下次复习日期
        """
        if "review_items" not in self.data:
            return None
        
        if category not in self.data["review_items"]:
            return None
        
        for r in self.data["review_items"][category]:
            if r["item"] == item:
                r["review_count"] += 1
                
                if is_correct:
                    r["correct_streak"] += 1
                    # 答对：增加难度系数，延长复习间隔
                    r["ease_factor"] = min(3.0, r["ease_factor"] + 0.1)
                    
                    # 根据复习次数确定下次间隔
                    idx = min(r["review_count"], len(self.REVIEW_INTERVALS) - 1)
                    base_interval = self.REVIEW_INTERVALS[idx]
                    # 根据难度系数调整间隔
                    interval = int(base_interval * r["ease_factor"] / 2.5)
                else:
                    r["correct_streak"] = 0
                    # 答错：降低难度系数，缩短复习间隔
                    r["ease_factor"] = max(1.3, r["ease_factor"] - 0.2)
                    interval = 1  # 答错后第二天再复习
                
                r["next_review"] = (date.today() + timedelta(days=interval)).isoformat()
                r["last_review"] = date.today().isoformat()
                
                self.save()
                return r["next_review"]
        
        return None
    
    def get_due_reviews(self, category=None):
        """获取今天需要复习的内容
        
        Args:
            category: 指定类别，None表示所有类别
        
        Returns:
            需要复习的项目列表
        """
        if "review_items" not in self.data:
            return []
        
        today = date.today().isoformat()
        due_items = []
        
        categories = [category] if category else self.data["review_items"].keys()
        
        for cat in categories:
            if cat not in self.data["review_items"]:
                continue
            for r in self.data["review_items"][cat]:
                if r["next_review"] <= today:
                    due_items.append(r)
        
        # 按优先级排序：先复习逾期最久的
        due_items.sort(key=lambda x: x["next_review"])
        
        return due_items
    
    def get_review_stats(self):
        """获取复习统计数据"""
        if "review_items" not in self.data:
            return {"total": 0, "due_today": 0, "mastered": 0, "by_category": {}}
        
        today = date.today().isoformat()
        stats = {
            "total": 0,
            "due_today": 0,
            "mastered": 0,  # 复习次数>=5且连续答对>=3
            "by_category": {}
        }
        
        for category, items in self.data["review_items"].items():
            cat_stats = {"total": len(items), "due": 0, "mastered": 0}
            
            for r in items:
                stats["total"] += 1
                
                if r["next_review"] <= today:
                    stats["due_today"] += 1
                    cat_stats["due"] += 1
                
                if r["review_count"] >= 5 and r.get("correct_streak", 0) >= 3:
                    stats["mastered"] += 1
                    cat_stats["mastered"] += 1
            
            stats["by_category"][category] = cat_stats
        
        return stats
    
    def get_review_calendar(self, days=7):
        """获取未来几天的复习日历
        
        Args:
            days: 天数
        
        Returns:
            {日期: 复习数量} 的字典
        """
        if "review_items" not in self.data:
            return {}
        
        calendar = {}
        today = date.today()
        
        for i in range(days):
            day = (today + timedelta(days=i)).isoformat()
            calendar[day] = 0
        
        for category, items in self.data["review_items"].items():
            for r in items:
                if r["next_review"] in calendar:
                    calendar[r["next_review"]] += 1
        
        return calendar
    
    def remove_mastered_item(self, category, item):
        """移除已完全掌握的内容（可选）"""
        if "review_items" not in self.data:
            return
        
        if category in self.data["review_items"]:
            self.data["review_items"][category] = [
                r for r in self.data["review_items"][category] if r["item"] != item
            ]
            self.save()
    
    # =====================================================
    # 家长控制面板相关方法
    # =====================================================
    
    def get_parent_settings(self):
        """获取家长设置"""
        if "parent_settings" not in self.data:
            self.data["parent_settings"] = {
                "password": "",
                "daily_time_limit": 60,
                "session_time_limit": 30,
                "allowed_hours_start": 8,
                "allowed_hours_end": 21,
                "weekend_extra_time": 15,
                "lock_after_limit": False,
                "show_answers": True,
                "difficulty_lock": False,
                "notifications": []
            }
        return self.data["parent_settings"]
    
    def set_parent_password(self, password):
        """设置家长密码"""
        settings = self.get_parent_settings()
        settings["password"] = password
        self.save()
    
    def verify_parent_password(self, password):
        """验证家长密码"""
        settings = self.get_parent_settings()
        stored = settings.get("password", "")
        if not stored:
            return True  # 未设置密码
        return password == stored
    
    def update_parent_settings(self, **kwargs):
        """更新家长设置"""
        settings = self.get_parent_settings()
        for key, value in kwargs.items():
            if key in settings:
                settings[key] = value
        self.save()
    
    def check_time_allowed(self):
        """检查当前时间是否允许学习"""
        settings = self.get_parent_settings()
        hour = datetime.now().hour
        
        start = settings.get("allowed_hours_start", 8)
        end = settings.get("allowed_hours_end", 21)
        
        return start <= hour < end
    
    def check_time_limit_reached(self):
        """检查是否达到时间限制"""
        settings = self.get_parent_settings()
        
        # 检查单次时间限制
        session_limit = settings.get("session_time_limit", 0)
        if session_limit > 0:
            session_minutes = self.get_session_minutes()
            if session_minutes >= session_limit:
                return "session", session_minutes
        
        # 检查每日时间限制
        daily_limit = settings.get("daily_time_limit", 0)
        if daily_limit > 0:
            # 周末额外时间
            if datetime.now().weekday() >= 5:  # 周六日
                daily_limit += settings.get("weekend_extra_time", 0)
            
            plan = self.get_daily_plan()
            if plan["today_minutes"] >= daily_limit:
                return "daily", plan["today_minutes"]
        
        return None, 0
    
    def add_parent_notification(self, message):
        """添加家长通知"""
        settings = self.get_parent_settings()
        notification = {
            "time": datetime.now().isoformat(),
            "message": message
        }
        settings["notifications"].append(notification)
        # 只保留最近50条
        settings["notifications"] = settings["notifications"][-50:]
        self.save()
    
    def get_parent_notifications(self, count=20):
        """获取家长通知"""
        settings = self.get_parent_settings()
        return settings.get("notifications", [])[-count:]
    
    def get_weekly_report(self):
        """获取周报数据"""
        today = date.today()
        week_start = today - timedelta(days=today.weekday())
        
        report = {
            "week_start": week_start.isoformat(),
            "total_minutes": 0,
            "total_questions": 0,
            "total_correct": 0,
            "daily_data": [],
            "module_stats": {}
        }
        
        # 统计本周每日数据
        for i in range(7):
            day = week_start + timedelta(days=i)
            day_str = day.isoformat()
            
            daily = next((d for d in self.data.get("daily_records", []) if d["date"] == day_str), None)
            minutes = daily["minutes"] if daily else 0
            
            report["daily_data"].append({
                "date": day_str,
                "weekday": ["周一", "周二", "周三", "周四", "周五", "周六", "周日"][i],
                "minutes": minutes
            })
            report["total_minutes"] += minutes
        
        # 模块统计
        for module, data in self.data.get("modules", {}).items():
            report["module_stats"][module] = {
                "correct": data.get("correct", 0),
                "wrong": data.get("wrong", 0),
                "level": data.get("level", 1)
            }
        
        report["total_questions"] = self.data["overall"].get("total_correct", 0) + self.data["overall"].get("total_wrong", 0)
        report["total_correct"] = self.data["overall"].get("total_correct", 0)
        
        return report
    
    def reset_progress(self, module=None):
        """重置学习进度（家长功能）"""
        if module:
            if module in self.data["modules"]:
                self.data["modules"][module] = {"score": 0, "correct": 0, "wrong": 0, "time": 0, "level": 1}
            if module in self.data.get("wrong_questions", {}):
                self.data["wrong_questions"][module] = []
            if module in self.data.get("review_items", {}):
                self.data["review_items"][module] = []
        else:
            # 重置所有（保留用户信息和家长设置）
            user_info = self.data.get("user_info", {})
            parent_settings = self.data.get("parent_settings", {})
            
            self.data = self._merge_defaults({})
            self.data["user_info"] = user_info
            self.data["parent_settings"] = parent_settings
        
        self.save()
    
    # =====================================================
    # 每日挑战系统
    # =====================================================
    
    def _init_daily_challenges(self):
        """初始化每日挑战数据结构"""
        if "daily_challenges" not in self.data:
            self.data["daily_challenges"] = {
                "date": "",
                "challenges": [],
                "completed": [],
                "streak": 0,
                "total_completed": 0
            }
    
    def generate_daily_challenges(self):
        """生成今日挑战（每天随机选择3个）"""
        import random
        
        self._init_daily_challenges()
        today = date.today().isoformat()
        
        # 如果今天已经生成过，直接返回
        if self.data["daily_challenges"]["date"] == today:
            return self.data["daily_challenges"]["challenges"]
        
        # 检查昨天是否完成了挑战（更新连续天数）
        yesterday = (date.today() - timedelta(days=1)).isoformat()
        if self.data["daily_challenges"]["date"] == yesterday:
            # 昨天有挑战，检查是否完成
            if len(self.data["daily_challenges"]["completed"]) > 0:
                self.data["daily_challenges"]["streak"] += 1
            else:
                self.data["daily_challenges"]["streak"] = 0
        elif self.data["daily_challenges"]["date"] != today:
            # 不是连续的，重置连续天数
            self.data["daily_challenges"]["streak"] = 0
        
        # 随机选择3个挑战
        selected = random.sample(DAILY_CHALLENGE_TEMPLATES, min(3, len(DAILY_CHALLENGE_TEMPLATES)))
        
        self.data["daily_challenges"]["date"] = today
        self.data["daily_challenges"]["challenges"] = selected
        self.data["daily_challenges"]["completed"] = []
        
        self.save()
        return selected
    
    def get_daily_challenges(self):
        """获取今日挑战"""
        self._init_daily_challenges()
        today = date.today().isoformat()
        
        # 如果今天还没生成挑战，先生成
        if self.data["daily_challenges"]["date"] != today:
            self.generate_daily_challenges()
        
        challenges = self.data["daily_challenges"]["challenges"]
        completed = self.data["daily_challenges"]["completed"]
        
        # 计算每个挑战的进度
        result = []
        for c in challenges:
            challenge = c.copy()
            challenge["completed"] = c["id"] in completed
            challenge["progress"] = self._get_challenge_progress(c)
            result.append(challenge)
        
        return result
    
    def _get_challenge_progress(self, challenge):
        """获取挑战进度"""
        c_type = challenge.get("type", "")
        target = challenge.get("target", 0)
        
        if c_type == "correct":
            # 今日答对题数
            plan = self.get_daily_plan()
            return min(plan["today_correct"], target)
        
        elif c_type == "streak":
            # 当前连续答对数
            return min(self.current_streak, target)
        
        elif c_type == "module_correct":
            # 特定模块今日答对数（简化：使用总答对数的一部分）
            plan = self.get_daily_plan()
            return min(plan["today_correct"] // 2, target)  # 简化计算
        
        elif c_type == "time":
            # 今日学习时长
            plan = self.get_daily_plan()
            return min(plan["today_minutes"], target)
        
        elif c_type == "review":
            # 今日复习数（简化）
            return 0
        
        elif c_type == "perfect":
            # 连续答对数
            return min(self.current_streak, target)
        
        return 0
    
    def check_challenge_completion(self):
        """检查并更新挑战完成状态"""
        self._init_daily_challenges()
        today = date.today().isoformat()
        
        if self.data["daily_challenges"]["date"] != today:
            return []
        
        newly_completed = []
        challenges = self.data["daily_challenges"]["challenges"]
        completed = self.data["daily_challenges"]["completed"]
        
        for c in challenges:
            if c["id"] in completed:
                continue
            
            progress = self._get_challenge_progress(c)
            if progress >= c["target"]:
                completed.append(c["id"])
                self.data["daily_challenges"]["total_completed"] += 1
                
                # 奖励星星
                self.data["rewards"]["stars"] += c.get("reward_stars", 1)
                
                newly_completed.append(c)
        
        if newly_completed:
            self.save()
        
        return newly_completed
    
    def get_challenge_stats(self):
        """获取挑战统计"""
        self._init_daily_challenges()
        
        return {
            "streak": self.data["daily_challenges"].get("streak", 0),
            "total_completed": self.data["daily_challenges"].get("total_completed", 0),
            "today_completed": len(self.data["daily_challenges"].get("completed", [])),
            "today_total": len(self.data["daily_challenges"].get("challenges", []))
        }


# 全局实例
def get_learning_data():
    """获取学习数据实例"""
    return LearningData()
