# -*- coding: utf-8 -*-
"""
交通工具数据模块 - 与UI无关的纯数据
"""
import random

class VehiclesData:
    """交通工具数据类"""
    
    # 交通工具: (名称, 类型, emoji, 颜色, 描述)
    VEHICLES = [
        ("汽车", "陆地", "🚗", "#FF6B6B", "在马路上跑"),
        ("公交车", "陆地", "🚌", "#FFD93D", "很多人一起坐"),
        ("火车", "陆地", "🚂", "#4ECDC4", "在铁轨上跑"),
        ("飞机", "天空", "✈️", "#45B7D1", "在天上飞"),
        ("轮船", "水上", "🚢", "#96CEB4", "在水里开"),
        ("直升机", "天空", "🚁", "#DDA0DD", "可以悬停"),
        ("自行车", "陆地", "🚲", "#FF9800", "用脚踩"),
        ("摩托车", "陆地", "🛵", "#8BC34A", "两个轮子"),
        ("火箭", "天空", "🚀", "#E91E63", "飞向太空"),
        ("消防车", "陆地", "🚒", "#F44336", "救火用的"),
        ("救护车", "陆地", "🚑", "#FFFFFF", "救人用的"),
        ("警车", "陆地", "🚓", "#1976D2", "警察开的"),
        ("出租车", "陆地", "🚕", "#FFEB3B", "打车用的"),
        ("卡车", "陆地", "🚚", "#795548", "运货用的"),
        ("挖掘机", "陆地", "🏗️", "#FFC107", "挖土用的"),
    ]
    
    # 汪汪队角色与游戏对应
    PAW_PATROL = {
        "chase": {"name": "阿奇", "color": "#1976D2", "role": "警犬", "vehicle": "警车"},
        "marshall": {"name": "毛毛", "color": "#F44336", "role": "消防犬", "vehicle": "消防车"},
        "skye": {"name": "天天", "color": "#EC407A", "role": "飞行犬", "vehicle": "直升机"},
        "rubble": {"name": "小砾", "color": "#FFC107", "role": "工程犬", "vehicle": "挖掘机"},
        "rocky": {"name": "灰灰", "color": "#4CAF50", "role": "环保犬", "vehicle": "回收车"},
        "zuma": {"name": "路马", "color": "#FF9800", "role": "水上救援犬", "vehicle": "气垫船"},
        "everest": {"name": "珠珠", "color": "#00BCD4", "role": "雪山救援犬", "vehicle": "雪地车"},
        "tracker": {"name": "阿克", "color": "#8BC34A", "role": "丛林犬", "vehicle": "吉普车"},
        "rex": {"name": "小克", "color": "#795548", "role": "恐龙犬", "vehicle": "恐龙车"},
        "liberty": {"name": "乐乐", "color": "#9C27B0", "role": "城市犬", "vehicle": "摩托车"},
    }
    
    # 交通规则
    TRAFFIC_RULES = [
        ("红灯", "停", "🔴", "红灯停"),
        ("绿灯", "行", "🟢", "绿灯行"),
        ("黄灯", "等", "🟡", "黄灯等一等"),
        ("斑马线", "走", "🦓", "过马路走斑马线"),
        ("人行道", "走", "🚶", "行人走人行道"),
    ]
    
    @classmethod
    def get_vehicles(cls):
        """获取所有交通工具"""
        return cls.VEHICLES.copy()
    
    @classmethod
    def get_vehicles_by_type(cls, vehicle_type):
        """根据类型获取交通工具"""
        return [v for v in cls.VEHICLES if v[1] == vehicle_type]
    
    @classmethod
    def get_paw_patrol(cls):
        """获取汪汪队数据"""
        return cls.PAW_PATROL.copy()
    
    @classmethod
    def get_pup_by_id(cls, pup_id):
        """根据ID获取狗狗数据"""
        return cls.PAW_PATROL.get(pup_id)
    
    @classmethod
    def get_traffic_rules(cls):
        """获取交通规则"""
        return cls.TRAFFIC_RULES.copy()
    
    @classmethod
    def generate_vehicle_quiz(cls, count=4):
        """
        生成交通工具认知题目
        返回: (target_vehicle, options)
        """
        selected = random.sample(cls.VEHICLES, count)
        target = random.choice(selected)
        return (target, selected)
    
    @classmethod
    def generate_traffic_light_question(cls):
        """
        生成红绿灯题目
        返回: (light_color, correct_action)
        """
        rule = random.choice(cls.TRAFFIC_RULES[:3])  # 只取红黄绿灯
        return (rule[0], rule[1], rule[2])
