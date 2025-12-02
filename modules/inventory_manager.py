# -*- coding: utf-8 -*-
"""
物品與庫存管理系統
Inventory Management System
"""

import json
import os
import random
from PyQt5.QtCore import QObject, pyqtSignal


class InventoryManager(QObject):
    """管理物品庫存"""

    # 信號
    inventory_changed = pyqtSignal(dict)  # 庫存變更
    item_added = pyqtSignal(str, int)  # (item_id, quantity)
    item_used = pyqtSignal(str)  # (item_id)

    def __init__(self):
        """初始化庫存管理器"""
        super().__init__()

        # 載入物品資料
        self.foods_data = self._load_data('data/foods.json')
        self.items_data = self._load_data('data/items.json')

        # 玩家庫存 {item_id: quantity}
        self.inventory = {}

        # 初始物品
        self._init_starter_items()

        print(f"[Inventory] 庫存系統初始化完成 - 載入 {len(self.foods_data)} 種食物, {len(self.items_data)} 種物品")

    def _load_data(self, filepath):
        """載入 JSON 資料"""
        try:
            with open(filepath, 'r', encoding='utf-8') as f:
                return json.load(f)
        except Exception as e:
            print(f"[Inventory] 載入資料失敗 {filepath}: {e}")
            return {}

    def _init_starter_items(self):
        """設定初始物品"""
        starter_items = {
            'apple': 5,
            'milk': 3,
            'ball': 2,
            'brush': 1
        }

        for item_id, quantity in starter_items.items():
            self.inventory[item_id] = quantity

        print(f"[Inventory] 初始物品設定完成: {starter_items}")

    # ⭐⭐⭐ 新增：隨機挑食物
    def get_random_food(self):
        available = [i for i in self.foods_data if self.get_item_count(i) > 0]
        if not available:
            return None
        return random.choice(available)

    # ⭐⭐⭐ 新增：隨機挑玩具
    def get_random_toy(self):
        available = [
            i for i, info in self.items_data.items()
            if self.get_item_count(i) > 0 and info.get("type") == "toy"
        ]
        if not available:
            return None
        return random.choice(available)

    def add_item(self, item_id, quantity=1):
        """新增物品到庫存"""
        if item_id not in self.foods_data and item_id not in self.items_data:
            print(f"[Inventory] 未知的物品 ID: {item_id}")
            return False

        if item_id in self.inventory:
            self.inventory[item_id] += quantity
        else:
            self.inventory[item_id] = quantity

        self.item_added.emit(item_id, quantity)
        self.inventory_changed.emit(self.inventory.copy())
        print(f"[Inventory] 新增物品: {item_id} x{quantity}")
        return True

    def use_item(self, item_id):
        """使用物品（消耗一個）"""
        if item_id not in self.inventory or self.inventory[item_id] <= 0:
            print(f"[Inventory] 物品不足: {item_id}")
            return False

        self.inventory[item_id] -= 1
        if self.inventory[item_id] == 0:
            del self.inventory[item_id]

        self.item_used.emit(item_id)
        self.inventory_changed.emit(self.inventory.copy())
        print(f"[Inventory] 使用物品: {item_id}")
        return True

    def get_item_count(self, item_id):
        return self.inventory.get(item_id, 0)

    def get_item_info(self, item_id):
        if item_id in self.foods_data:
            return self.foods_data[item_id]
        elif item_id in self.items_data:
            return self.items_data[item_id]
        return None

    def to_dict(self):
        return {'inventory': self.inventory.copy()}

    def from_dict(self, data):
        self.inventory = data.get('inventory', {})
        self.inventory_changed.emit(self.inventory.copy())
        print(f"[Inventory] 從存檔載入庫存完成: {len(self.inventory)} 種物品")
