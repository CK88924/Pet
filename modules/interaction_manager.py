# -*- coding: utf-8 -*-
"""
互動系統管理器
Interaction Management System
"""

import time
from PyQt5.QtCore import QObject, pyqtSignal


class InteractionManager(QObject):
    """處理寵物所有互動行為"""

    interaction_performed = pyqtSignal(str, dict)
    cooldown_finished = pyqtSignal(str)

    def __init__(self, pet_stats, inventory):
        super().__init__()

        self.pet_stats = pet_stats
        self.inventory = inventory

        self.cooldowns = {
            'feed': 5,
            'play': 10,
            'pet': 3,
            'clean': 15,
            'rest': 8   # ⭐新增休息冷卻
        }

        self.last_interaction_time = {}
        print("[Interaction] 互動系統初始化完成")

    def can_interact(self, action):
        """檢查冷卻"""
        if action not in self.last_interaction_time:
            return True
        return (time.time() - self.last_interaction_time[action]) >= self.cooldowns[action]

    # 🍎 餵食
    def feed(self, food_id):
        if not self.can_interact('feed'):
            print("[Interaction] 餵食冷卻中")
            return

        food_info = self.inventory.get_item_info(food_id)

        if food_info and self.inventory.use_item(food_id):
            self.pet_stats.modify_stat('hunger', food_info.get('hunger', 20))
            self.pet_stats.modify_stat('happiness', food_info.get('happiness', 5))
            self.pet_stats.modify_stat('health', food_info.get('health', 0))

            self.last_interaction_time['feed'] = time.time()
            print(f"[Interaction] 餵食 → {food_id}")

    # 🎾 玩耍
    def play(self):
        if not self.can_interact('play'):
            print("[Interaction] 玩耍冷卻中")
            return

        toy = self.inventory.get_random_toy()

        if toy and self.inventory.use_item(toy):
            info = self.inventory.get_item_info(toy)
            self.pet_stats.modify_stat('happiness', info.get('happiness', 20))
            self.pet_stats.modify_stat('energy', -abs(info.get('energy', -10)))
            print(f"[Interaction] 玩耍 → {toy}")
        else:
            self.pet_stats.modify_stat('happiness', 10)
            self.pet_stats.modify_stat('energy', -10)
            print("[Interaction] 玩耍 →（無玩具）")

        self.last_interaction_time['play'] = time.time()

    # 🐾 撫摸
    def pet(self):
        if not self.can_interact('pet'):
            print("[Interaction] 撫摸冷卻中")
            return

        self.pet_stats.modify_stat('happiness', 10)
        self.last_interaction_time['pet'] = time.time()
        print("[Interaction] 撫摸 → +10 快樂")

    # 🧼 清潔
    def clean(self):
        if not self.can_interact('clean'):
            print("[Interaction] 清潔冷卻中")
            return

        self.pet_stats.modify_stat('health', 20)
        self.pet_stats.modify_stat('happiness', 5)
        self.last_interaction_time['clean'] = time.time()
        print("[Interaction] 清潔 → +20 健康, +5 快樂")

    # 😴 休息（⭐新增）
    def rest(self):
        if not self.can_interact('rest'):
            print("[Interaction] 休息冷卻中")
            return

        self.pet_stats.modify_stat('energy', 30)
        self.pet_stats.modify_stat('happiness', 5)
        self.last_interaction_time['rest'] = time.time()

        print("[Interaction] 休息 → +30 精力, +5 快樂")
