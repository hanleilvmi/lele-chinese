"""
语音配置共享模块 v1.2
用于在各个学习模块之间共享语音风格设置
集成学习数据管理、休息提醒、安全退出
优化：使用ui_config统一路径管理
"""

import os
import json
import threading
from datetime import datetime

# 尝试导入UI配置模块
try:
    from ui_config import get_data_path, get_path
    UI_CONFIG_AVAILABLE = True
except ImportError:
    UI_CONFIG_AVAILABLE = False

# 导入基础模块
try:
    from learning_base import (
        temp_file_manager, TimerManager, RestReminder,
        confirm_exit, setup_window_close_handler,
        safe_execute, GameStateManager
    )
    BASE_MODULE_AVAILABLE = True
except ImportError:
    BASE_MODULE_AVAILABLE = False
    print("警告: learning_base 模块未找到，部分功能不可用")

# 语音风格配置
VOICE_STYLES = {
    "汪汪队风格": {
        "voice": "zh-CN-YunxiNeural",
        "desc": "活泼男童声，汪汪队台词",
        "praises": [
            # 汪汪队经典台词
            "汪汪队，出动！答对啦！",
            "没有困难的工作，只有勇敢的狗狗！",
            "太棒了，乐乐是最勇敢的狗狗！",
            "耶！任务完成！",
            "狗狗们，做得好！",
            "莱德队长为你骄傲！",
            "汪汪汪，你真棒！",
            # 阿奇风格
            "阿奇说，乐乐真厉害！",
            "汪汪队需要你这样的小英雄！",
            "阿奇为你点赞！",
            # 毛毛风格
            "毛毛说，太酷了！",
            "消防狗狗毛毛为你鼓掌！",
            "毛毛觉得你超级棒！",
            # 小砾风格
            "小砾说，挖掘机都为你欢呼！",
            "工程狗狗小砾给你点赞！",
            "小砾说你是最棒的！",
            # 路马风格
            "路马说，你像海浪一样厉害！",
            "水上救援成功！路马为你骄傲！",
            "路马说你真是太聪明了！",
            # 天天风格
            "天天说，你飞得比我还高！",
            "飞行狗狗天天为你欢呼！",
            "天天说你是小天才！",
            # 灰灰风格
            "灰灰说，这个问题难不倒你！",
            "环保狗狗灰灰为你点赞！",
            "灰灰说你超级聪明！",
            # 更多表扬
            "乐乐真厉害，给你一个大大的赞！",
            "狗狗们都为你欢呼！",
            "你是汪汪队的荣誉成员！",
            "莱德说，乐乐做得太好了！",
            "汪汪队为你感到骄傲！",
            "你是最棒的小狗狗！",
            "任务完成得太漂亮了！",
            "汪汪队给你颁发勇气勋章！",
        ],
        "encourages": [
            # 汪汪队鼓励台词
            "没关系，汪汪队永不放弃！",
            "加油，勇敢的狗狗不怕困难！",
            "再试一次，你一定行！",
            "别担心，汪汪队来帮你！",
            "狗狗们，我们再来一次！",
            "莱德说，失败是成功之母！",
            "阿奇说，再试一次吧！",
            "毛毛说，别灰心，你可以的！",
            "小砾说，我们一起加油！",
            "路马说，大海也有风浪，没关系！",
            "天天说，跌倒了再爬起来！",
            "灰灰说，动动脑筋再想想！",
            "汪汪队相信你！",
            "勇敢的狗狗不怕失败！",
            "没事的，我们再来一次！",
            "加油加油，乐乐最棒！",
        ]
    },
    "温柔姐姐": {
        "voice": "zh-CN-XiaoyiNeural",
        "desc": "温柔女声，亲切鼓励",
        "praises": [
            "哇，乐乐真棒！",
            "太厉害了，答对啦！",
            "乐乐好聪明呀！",
            "真棒真棒，给你点赞！",
            "乐乐是最棒的小朋友！",
            "太聪明了，继续加油！",
            "答对了，乐乐真厉害！",
            "好棒呀，姐姐为你骄傲！",
            "乐乐真是小天才！",
            "太棒了，给你一朵小红花！",
            "乐乐越来越聪明了！",
            "答得真好，继续保持！",
        ],
        "encourages": [
            "没关系，再试一次！",
            "加油，乐乐一定行！",
            "别着急，慢慢来！",
            "没事的，我们再来！",
            "乐乐加油，你可以的！",
            "姐姐相信你，再试试！",
            "慢慢想，不着急！",
            "没关系，下次一定行！",
        ]
    },
    "活泼哥哥": {
        "voice": "zh-CN-YunjianNeural",
        "desc": "阳光男声，热情活泼",
        "praises": [
            "耶！乐乐太厉害了！",
            "哇塞，答对啦！",
            "乐乐真是小天才！",
            "太棒了，给你比个心！",
            "厉害厉害，乐乐最棒！",
            "答对了，哥哥为你鼓掌！",
            "乐乐好聪明，继续加油！",
            "太强了，乐乐真厉害！",
            "哥哥为你骄傲！",
            "乐乐越来越棒了！",
            "太酷了，答得真好！",
            "乐乐是最聪明的小朋友！",
        ],
        "encourages": [
            "没关系，再来一次！",
            "加油加油，你能行！",
            "别灰心，继续努力！",
            "没事，哥哥相信你！",
            "再试试，乐乐最棒！",
            "加油，你一定可以的！",
            "别着急，慢慢来！",
            "没关系，下次一定行！",
        ]
    },
    "可爱童声": {
        "voice": "zh-CN-XiaoxiaoNeural",
        "desc": "可爱女童声，活泼有趣",
        "praises": [
            "哇，乐乐好棒棒！",
            "太厉害啦，答对了！",
            "乐乐真聪明呀！",
            "棒棒哒，给你小红花！",
            "乐乐是最棒的！",
            "好厉害呀，继续加油！",
            "答对啦，乐乐真棒！",
            "太聪明了，为你鼓掌！",
            "乐乐好厉害呀！",
            "太棒啦，给你点赞！",
            "乐乐越来越聪明啦！",
            "答得真好，继续加油！",
        ],
        "encourages": [
            "没关系呀，再试一次！",
            "加油加油，你可以的！",
            "别着急，慢慢想！",
            "没事没事，我们再来！",
            "乐乐加油，一定行！",
            "再想想，你可以的！",
            "没关系，下次一定对！",
            "加油呀，乐乐最棒！",
        ]
    },
}

# 配置文件路径
if UI_CONFIG_AVAILABLE:
    CONFIG_FILE = get_data_path("voice_config.json")
else:
    CONFIG_FILE = os.path.join(os.path.dirname(os.path.abspath(__file__)), "voice_config.json")

def load_voice_config():
    """加载语音配置"""
    try:
        if os.path.exists(CONFIG_FILE):
            with open(CONFIG_FILE, 'r', encoding='utf-8') as f:
                return json.load(f)
    except:
        pass
    return {"style": "汪汪队风格"}

def get_current_style():
    """获取当前语音风格"""
    config = load_voice_config()
    style_name = config.get("style", "汪汪队风格")
    if style_name not in VOICE_STYLES:
        style_name = "汪汪队风格"
    return style_name, VOICE_STYLES[style_name]

def get_voice():
    """获取当前语音"""
    _, style = get_current_style()
    return style["voice"]

def get_praises():
    """获取当前风格的表扬语"""
    _, style = get_current_style()
    return style["praises"]

def get_encourages():
    """获取当前风格的鼓励语"""
    _, style = get_current_style()
    return style["encourages"]


# =====================================================
# 学习数据集成
# =====================================================

_learning_data = None

def get_learning_data():
    """获取学习数据实例（懒加载）"""
    global _learning_data
    if _learning_data is None:
        try:
            from learning_data import LearningData
            _learning_data = LearningData()
        except ImportError:
            _learning_data = None
    return _learning_data

def record_answer(module, points, is_correct, question_data=None):
    """记录答题结果
    
    Args:
        module: 模块名称 (literacy, pinyin, math, english, thinking, vehicles)
        points: 得分
        is_correct: 是否正确
        question_data: 错题数据（可选）
    
    Returns:
        dict: {"badges": 新徽章列表, "level_change": 难度变化("up"/"down"/None), "new_level": 新等级}
    """
    ld = get_learning_data()
    if ld is None:
        return {"badges": [], "level_change": None, "new_level": 1}
    
    # 记录答题前的等级
    old_level = ld.get_level(module)
    
    new_badges = ld.add_score(module, points, is_correct)
    
    # 记录错题
    if not is_correct and question_data:
        ld.add_wrong_question(module, question_data)
    elif is_correct and question_data:
        # 答对后从错题中移除
        ld.remove_wrong_question(module, question_data.get("question", ""))
    
    # 检查难度是否变化
    new_level = ld.get_level(module)
    level_change = None
    if new_level > old_level:
        level_change = "up"
    elif new_level < old_level:
        level_change = "down"
    
    return {"badges": new_badges, "level_change": level_change, "new_level": new_level}

def get_module_level(module):
    """获取模块难度等级"""
    ld = get_learning_data()
    if ld is None:
        return 1
    return ld.get_level(module)

def get_wrong_questions(module):
    """获取错题列表"""
    ld = get_learning_data()
    if ld is None:
        return []
    return ld.get_wrong_questions(module)

def get_stars():
    """获取星星数量"""
    ld = get_learning_data()
    if ld is None:
        return 0
    return ld.get_stars()

# =====================================================
# 每日学习计划相关函数
# =====================================================

def get_daily_plan():
    """获取每日学习计划数据"""
    ld = get_learning_data()
    if ld is None:
        return {
            "target_questions": 30,
            "today_questions": 0,
            "today_correct": 0,
            "today_minutes": 0,
            "question_progress": 0,
            "goal_completed": False,
            "session_minutes": 0
        }
    return ld.get_daily_plan()

def should_show_rest_reminder():
    """检查是否应该显示休息提醒"""
    ld = get_learning_data()
    if ld is None:
        return False
    return ld.should_show_rest_reminder()

def get_session_minutes():
    """获取当前会话学习时长"""
    ld = get_learning_data()
    if ld is None:
        return 0
    return ld.get_session_minutes()

# =====================================================
# 智能复习系统相关函数
# =====================================================

def add_to_review(category, item, display_name=None):
    """添加内容到复习列表"""
    ld = get_learning_data()
    if ld is None:
        return
    ld.add_review_item(category, item, display_name)

def update_review(category, item, is_correct):
    """更新复习状态"""
    ld = get_learning_data()
    if ld is None:
        return None
    return ld.update_review_item(category, item, is_correct)

def get_due_reviews(category=None):
    """获取今天需要复习的内容"""
    ld = get_learning_data()
    if ld is None:
        return []
    return ld.get_due_reviews(category)

def get_review_stats():
    """获取复习统计"""
    ld = get_learning_data()
    if ld is None:
        return {"total": 0, "due_today": 0, "mastered": 0, "by_category": {}}
    return ld.get_review_stats()


# =====================================================
# 基础功能导出（供各模块使用）
# =====================================================

def get_temp_file_manager():
    """获取临时文件管理器"""
    if BASE_MODULE_AVAILABLE:
        return temp_file_manager
    return None

def create_timer_manager(window):
    """创建定时器管理器"""
    if BASE_MODULE_AVAILABLE:
        return TimerManager(window)
    return None

def create_rest_reminder(window, interval_minutes=15):
    """创建休息提醒器"""
    if BASE_MODULE_AVAILABLE:
        return RestReminder(window, interval_minutes)
    return None

def create_game_state_manager():
    """创建游戏状态管理器"""
    if BASE_MODULE_AVAILABLE:
        return GameStateManager()
    return None

def setup_safe_exit(window, on_exit_callback=None):
    """设置安全退出处理"""
    if BASE_MODULE_AVAILABLE:
        setup_window_close_handler(window, on_exit_callback)

def do_confirm_exit(window, on_exit_callback=None):
    """执行退出确认"""
    if BASE_MODULE_AVAILABLE:
        return confirm_exit(window, on_exit_callback)
    else:
        window.quit()
        return True

def register_temp_file(filepath):
    """注册临时文件"""
    if BASE_MODULE_AVAILABLE:
        temp_file_manager.register_file(filepath)

def cleanup_temp_file(filepath):
    """清理临时文件"""
    if BASE_MODULE_AVAILABLE:
        temp_file_manager.cleanup_file(filepath)
    else:
        try:
            if os.path.exists(filepath):
                os.remove(filepath)
        except:
            pass
