# -*- coding: utf-8 -*-
"""
事件與成就系統
Event and Achievement System
"""

import json
import random
import time
from PyQt5.QtCore import QObject, pyqtSignal


class EventSystem(QObject):
    """管理隨機事件和成就系統"""
    
    # 信號
    event_triggered = pyqtSignal(str, dict)  # (event_id, event_data)
    achievement_unlocked = pyqtSignal(str, dict)  # (achievement_id, achievement_data)
    notification = pyqtSignal(str, str)  # (title, message)
    
    def __init__(self, pet_stats, inventory):
        """
        初始化事件系統
        
        Args:
            pet_stats: PetStats 實例
            inventory: InventoryManager 實例
        """
        super().__init__()
        
        self.pet_stats = pet_stats
        self.inventory = inventory
        
        # 載入資料
        self.events_data = self._load_data('data/events.json')
        self.achievements_data = self._load_data('data/achievements.json')
        
        # 已解鎖的成就
        self.unlocked_achievements = set()
        
        # 事件觸發間隔
        self.min_event_interval = 60  # 最小間隔（秒）
        self.last_event_time = 0
        
        print(f"[EventSystem] 事件系統初始化完成 - {len(self.events_data)} 個事件, {len(self.achievements_data)} 個成就")
    
    def _load_data(self, filepath):
        """載入 JSON 資料"""
        try:
            with open(filepath, 'r', encoding='utf-8') as f:
                return json.load(f)
        except Exception as e:
            print(f"[EventSystem] 載入資料失敗 {filepath}: {e}")
            return {}
    
    def try_trigger_event(self):
        """
        嘗試觸發隨機事件
        
        Returns:
            bool: 是否觸發了事件
        """
        current_time = time.time()
        
        # 檢查間隔
        if current_time - self.last_event_time < self.min_event_interval:
            return False
        
        # 收集可觸發的事件
        available_events = []
        for event_id, event_data in self.events_data.items():
            # 檢查條件
            if self._check_event_condition(event_data):
                prob = event_data.get('probability', 0.1)
                available_events.append((event_id, event_data, prob))
        
        if not available_events:
            return False
        
        # 根據機率選擇事件
        for event_id, event_data, prob in available_events:
            if random.random() < prob:
                self._trigger_event(event_id, event_data)
                self.last_event_time = current_time
                return True
        
        return False
    
    def _check_event_condition(self, event_data):
        """檢查事件觸發條件"""
        condition = event_data.get('condition', {})
        
        if not condition:
            return True  # 無條件
        
        stats = self.pet_stats.get_all_stats()
        
        for stat_name, requirement in condition.items():
            if stat_name not in stats:
                continue
            
            stat_value = stats[stat_name]
            
            # 支援比較運算符
            if isinstance(requirement, dict):
                for op, value in requirement.items():
                    if op == '<' and not (stat_value < value):
                        return False
                    elif op == '>' and not (stat_value > value):
                        return False
                    elif op == '<=' and not (stat_value <= value):
                        return False
                    elif op == '>=' and not (stat_value >= value):
                        return False
                    elif op == '==' and not (stat_value == value):
                        return False
            else:
                # 直接數值比較
                if stat_value != requirement:
                    return False
        
        return True
    
    def _trigger_event(self, event_id, event_data):
        """觸發事件"""
        print(f"[EventSystem] 觸發事件: {event_id}")
        
        # 應用效果
        effect = event_data.get('effect', {})
        
        # 狀態變化
        for stat in ['hunger', 'happiness', 'health', 'energy']:
            if stat in effect:
                self.pet_stats.modify_stat(stat, effect[stat])
        
        # 新增物品
        if 'add_item' in effect:
            item_id = effect['add_item']
            quantity = effect.get('quantity', 1)
            self.inventory.add_item(item_id, quantity)
        
        # 發送通知
        name = event_data.get('name', '事件發生')
        description = event_data.get('description', '')
        self.notification.emit(name, description)
        self.event_triggered.emit(event_id, event_data)
    
    def check_achievements(self):
        """檢查並解鎖成就"""
        for achievement_id, achievement_data in self.achievements_data.items():
            # 已解鎖的跳過
            if achievement_id in self.unlocked_achievements:
                continue
            
            # 檢查條件
            if self._check_achievement_condition(achievement_data):
                self._unlock_achievement(achievement_id, achievement_data)
    
    def _check_achievement_condition(self, achievement_data):
        """檢查成就解鎖條件"""
        requirement = achievement_data.get('requirement', {})
        
        if not requirement:
            return True  # 無條件成就（首次觸發）
        
        stats = self.pet_stats.get_all_stats()
        
        for key, value in requirement.items():
            if key not in stats:
                return False
            
            if stats[key] < value:
                return False
        
        return True
    
    def _unlock_achievement(self, achievement_id, achievement_data):
        """解鎖成就"""
        print(f"[EventSystem] 解鎖成就: {achievement_id}")
        
        self.unlocked_achievements.add(achievement_id)
        
        # 發放獎勵
        reward = achievement_data.get('reward', {})
        if 'item' in reward:
            item_id = reward['item']
            quantity = reward.get('quantity', 1)
            self.inventory.add_item(item_id, quantity)
        
        # 發送通知
        name = achievement_data.get('name', '成就解鎖')
        description = achievement_data.get('description', '')
        self.notification.emit(f"🏆 {name}", description)
        self.achievement_unlocked.emit(achievement_id, achievement_data)
    
    def get_unlocked_achievements(self):
        """取得已解鎖的成就清單"""
        result = []
        for achievement_id in self.unlocked_achievements:
            if achievement_id in self.achievements_data:
                data = self.achievements_data[achievement_id].copy()
                data['id'] = achievement_id
                result.append(data)
        return result
    
    def get_achievement_progress(self):
        """取得成就進度"""
        total = len(self.achievements_data)
        unlocked = len(self.unlocked_achievements)
        return {
            'total': total,
            'unlocked': unlocked,
            'percentage': (unlocked / total * 100) if total > 0 else 0
        }
    
    def to_dict(self):
        """轉換為字典（用於存檔）"""
        return {
            'unlocked_achievements': list(self.unlocked_achievements),
            'last_event_time': self.last_event_time
        }
    
    def from_dict(self, data):
        """從字典載入（用於讀檔）"""
        self.unlocked_achievements = set(data.get('unlocked_achievements', []))
        self.last_event_time = data.get('last_event_time', 0)
        print(f"[EventSystem] 從存檔載入: {len(self.unlocked_achievements)} 個成就")
