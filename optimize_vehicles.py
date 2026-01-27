# -*- coding: utf-8 -*-
"""
优化交通乐园游戏 - 针对3-4岁小朋友
主要改进：
1. 降低游戏难度
2. 增加视觉反馈和提示
3. 简化操作
4. 增加趣味性
"""

def optimize_vehicles():
    with open('kids_vehicles.py', 'r', encoding='utf-8') as f:
        content = f.read()
    
    # ========== 优化赛车游戏 ==========
    # 1. 降低障碍物生成频率 (0.03 -> 0.015)
    # 2. 降低初始速度 (5 -> 3)
    # 3. 增加金币生成频率 (0.05 -> 0.08)
    # 4. 增大碰撞容错 (50 -> 40)
    
    old_race_init = '''        self.race_score = 0
        self.race_speed = 5
        self.race_obstacles = []
        self.race_coins = []'''
    
    new_race_init = '''        self.race_score = 0
        self.race_speed = 3  # 降低初始速度，更适合小朋友
        self.race_obstacles = []
        self.race_coins = []'''
    
    content = content.replace(old_race_init, new_race_init)
    
    # 降低障碍物生成频率
    content = content.replace(
        'if random.random() < 0.03:\n            ox = random.choice(lanes)\n            self.race_obstacles.append',
        'if random.random() < 0.015:  # 降低障碍物频率\n            ox = random.choice(lanes)\n            self.race_obstacles.append'
    )
    
    # 增加金币生成频率
    content = content.replace(
        'if random.random() < 0.05:\n            coin_x = random.choice(lanes)\n            self.race_coins.append',
        'if random.random() < 0.10:  # 增加金币频率，让小朋友更有成就感\n            coin_x = random.choice(lanes)\n            self.race_coins.append'
    )
    
    # 降低碰撞检测严格度
    content = content.replace(
        'if abs(obs["x"] - self.race_x) < 50 and abs(obs["y"] - self.race_y) < 40:',
        'if abs(obs["x"] - self.race_x) < 35 and abs(obs["y"] - self.race_y) < 30:  # 更宽松的碰撞检测'
    )
    
    # 降低速度增长
    content = content.replace(
        'if self.race_distance % 200 == 0:\n            self.race_speed = min(self.race_speed + 1, 15)',
        'if self.race_distance % 400 == 0:  # 速度增长更慢\n            self.race_speed = min(self.race_speed + 1, 8)  # 最高速度降低'
    )
    
    # ========== 优化飞机游戏 ==========
    # 1. 降低小鸟生成频率
    # 2. 增加星星生成频率
    # 3. 降低小鸟速度
    
    content = content.replace(
        'if random.random() < 0.02:\n            by = random.randint(100, ch - 100)\n            self.plane_birds.append',
        'if random.random() < 0.012:  # 降低小鸟频率\n            by = random.randint(100, ch - 100)\n            self.plane_birds.append'
    )
    
    content = content.replace(
        'if random.random() < 0.04:\n            sy = random.randint(80, ch - 80)\n            self.plane_stars.append',
        'if random.random() < 0.08:  # 增加星星频率\n            sy = random.randint(80, ch - 80)\n            self.plane_stars.append'
    )
    
    # 降低小鸟速度
    content = content.replace(
        'bird["x"] -= 7',
        'bird["x"] -= 4  # 小鸟飞得慢一点'
    )
    
    # 降低飞机碰撞检测严格度
    content = content.replace(
        'if abs(bird["x"] - self.plane_x) < 60 and abs(bird["y"] - self.plane_y) < 35:',
        'if abs(bird["x"] - self.plane_x) < 45 and abs(bird["y"] - self.plane_y) < 25:  # 更宽松'
    )
    
    # ========== 优化消防车游戏 ==========
    # 1. 减少需要救的楼数 (5 -> 3)
    # 2. 降低火焰等级，更容易灭火
    # 3. 增加水柱效果
    
    content = content.replace(
        '"on_fire": True, "fire_level": 100, "saved": False',
        '"on_fire": True, "fire_level": 60, "saved": False  # 降低火焰等级，更容易灭火'
    )
    
    content = content.replace(
        'b["fire_level"] -= 5',
        'b["fire_level"] -= 12  # 水更有效'
    )
    
    # ========== 优化火箭游戏 ==========
    # 1. 降低陨石生成频率
    # 2. 增加燃料生成频率
    # 3. 降低燃料消耗速度
    # 4. 降低陨石速度
    
    content = content.replace(
        'if random.random() < 0.03:\n            mx = random.randint(100, cw - 100)\n            self.rocket_meteors.append',
        'if random.random() < 0.015:  # 降低陨石频率\n            mx = random.randint(100, cw - 100)\n            self.rocket_meteors.append'
    )
    
    content = content.replace(
        'if random.random() < 0.02:\n            fx = random.randint(150, cw - 150)\n            self.rocket_fuels.append',
        'if random.random() < 0.05:  # 增加燃料频率\n            fx = random.randint(150, cw - 150)\n            self.rocket_fuels.append'
    )
    
    content = content.replace(
        'self.rocket_fuel -= 0.3',
        'self.rocket_fuel -= 0.15  # 燃料消耗更慢'
    )
    
    content = content.replace(
        'm["y"] += 8',
        'm["y"] += 5  # 陨石下落更慢'
    )
    
    # 降低陨石碰撞检测严格度
    content = content.replace(
        'if abs(m["x"] - self.rocket_x) < 40 and abs(m["y"] - rocket_draw_y) < 50:',
        'if abs(m["x"] - self.rocket_x) < 30 and abs(m["y"] - rocket_draw_y) < 35:  # 更宽松'
    )
    
    # ========== 优化火车游戏 ==========
    # 1. 减少运送次数 (5 -> 3)
    # 2. 增加移动速度
    
    content = content.replace(
        '完成5次运送获胜',
        '完成3次运送获胜'
    )
    
    content = content.replace(
        'if self.train_deliveries >= 5:',
        'if self.train_deliveries >= 3:  # 减少运送次数'
    )
    
    content = content.replace(
        'self.train_status.config(text=f"运送: {self.train_deliveries}/5")',
        'self.train_status.config(text=f"运送: {self.train_deliveries}/3")'
    )
    
    content = content.replace(
        'self.train_status = tk.Label(self.game_frame, text="运送: 0/5"',
        'self.train_status = tk.Label(self.game_frame, text="运送: 0/3"'
    )
    
    # 增加火车移动速度
    content = content.replace(
        'self.train_x -= 20',
        'self.train_x -= 35  # 火车移动更快'
    )
    
    content = content.replace(
        'self.train_x += 20',
        'self.train_x += 35  # 火车移动更快'
    )
    
    # 保存文件
    with open('kids_vehicles.py', 'w', encoding='utf-8') as f:
        f.write(content)
    
    print("✅ 交通乐园游戏优化完成！")
    print("主要改进：")
    print("  🏎️ 赛车游戏：降低速度和障碍物频率，增加金币")
    print("  ✈️ 飞机游戏：降低小鸟频率和速度，增加星星")
    print("  🚒 消防车游戏：降低火焰等级，水更有效")
    print("  🚀 火箭游戏：降低陨石频率，增加燃料，消耗更慢")
    print("  🚂 火车游戏：减少运送次数，移动更快")


if __name__ == "__main__":
    optimize_vehicles()
