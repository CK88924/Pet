# -*- coding: utf-8 -*-
"""
寵物狀態管理系統
Pet Stats Management System
"""

import time
from PyQt5.QtCore import QObject, pyqtSignal


class PetStats(QObject):
    """管理寵物的所有狀態值"""
    
    # 信號：當狀態改變時發送
    stats_changed = pyqtSignal(dict)  # 發送所有狀態
    stat_warning = pyqtSignal(str, int)  # (stat_name, value) 當狀態過低時警告
    level_up = pyqtSignal(int)  # (new_level) 升級時發送
    
    def __init__(self):
        """初始化寵物狀態"""
        super().__init__()
        
        # 基礎屬性 (0-100)
        self.hunger = 100  # 飢餓度（越高越飽）
        self.happiness = 100  # 快樂度
        self.health = 100  # 健康度
        self.energy = 100  # 精力
        
        # 成長系統
        self.level = 1  # 等級
        self.experience = 0  # 經驗值
        self.exp_to_next_level = 100  # 升級所需經驗
        
        # 年齡系統
        self.birth_time = time.time()  # 出生時間（時間戳）
        self.age_seconds = 0  # 年齡（秒）
        
        # 統計資料
        self.feed_count = 0  # 餵食次數
        self.play_count = 0  # 玩耍次數
        self.pet_count = 0  # 撫摸次數
        self.clean_count = 0  # 清潔次數
        
        # 衰減速率（每秒降低的量）
        self.decay_rates = {
            'hunger': 0.05,  # 每秒降低 0.05
            'happiness': 0.03,
            'health': 0.02,
            'energy': 0.04
        }
        
        # 最後更新時間
        self.last_update = time.time()
        
        print("[PetStats] 寵物狀態系統初始化完成")
    
    def update(self):
        """
        更新狀態（每幀調用）
        處理狀態自動衰減
        """
        current_time = time.time()
        delta_time = current_time - self.last_update
        self.last_update = current_time
        
        # 更新年齡
        self.age_seconds = current_time - self.birth_time
        
        # 狀態衰減
        self.hunger = max(0, self.hunger - self.decay_rates['hunger'] * delta_time)
        self.happiness = max(0, self.happiness - self.decay_rates['happiness'] * delta_time)
        self.health = max(0, self.health - self.decay_rates['health'] * delta_time)
        
        # 精力恢復（如果在休息狀態）或消耗
        if self.energy < 30:  # 低精力時恢復更快
            self.energy = min(100, self.energy + 0.05 * delta_time)
        else:
            self.energy = max(0, self.energy - self.decay_rates['energy'] * delta_time)
        
        # 狀態互相影響
        if self.hunger < 20:  # 太餓影響健康
            self.health = max(0, self.health - 0.1 * delta_time)
        
        if self.health < 20:  # 不健康影響快樂
            self.happiness = max(0, self.happiness - 0.1 * delta_time)
        
        # 檢查低狀態警告
        self._check_warnings()
        
        # 發送狀態更新信號
        self.stats_changed.emit(self.get_all_stats())
    
    def _check_warnings(self):
        """檢查狀態是否過低並發出警告"""
        warning_threshold = 20
        
        if self.hunger < warning_threshold:
            self.stat_warning.emit('hunger', int(self.hunger))
        if self.happiness < warning_threshold:
            self.stat_warning.emit('happiness', int(self.happiness))
        if self.health < warning_threshold:
            self.stat_warning.emit('health', int(self.health))
        if self.energy < warning_threshold:
            self.stat_warning.emit('energy', int(self.energy))
    
    def modify_stat(self, stat_name, amount):
        """
        修改特定狀態值
        
        Args:
            stat_name: 狀態名稱 ('hunger', 'happiness', 'health', 'energy')
            amount: 變化量（可正可負）
        """
        if stat_name == 'hunger':
            self.hunger = max(0, min(100, self.hunger + amount))
        elif stat_name == 'happiness':
            self.happiness = max(0, min(100, self.happiness + amount))
        elif stat_name == 'health':
            self.health = max(0, min(100, self.health + amount))
        elif stat_name == 'energy':
            self.energy = max(0, min(100, self.energy + amount))
        
        self.stats_changed.emit(self.get_all_stats())
    
    def add_experience(self, amount):
        """
        增加經驗值
        
        Args:
            amount: 經驗值數量
        """
        self.experience += amount
        
        # 檢查是否升級
        while self.experience >= self.exp_to_next_level:
            self.experience -= self.exp_to_next_level
            self.level += 1
            self.exp_to_next_level = int(self.exp_to_next_level * 1.5)  # 每級所需經驗增加
            self.level_up.emit(self.level)
            print(f"[PetStats] 升級！當前等級: {self.level}")
    
    def get_all_stats(self):
        """
        取得所有狀態
        
        Returns:
            dict: 包含所有狀態的字典
        """
        return {
            'hunger': int(self.hunger),
            'happiness': int(self.happiness),
            'health': int(self.health),
            'energy': int(self.energy),
            'level': self.level,
            'experience': self.experience,
            'exp_to_next_level': self.exp_to_next_level,
            'age_days': self.age_seconds / 86400,  # 轉換為天數
            'age_hours': self.age_seconds / 3600,  # 轉換為小時
            'feed_count': self.feed_count,
            'play_count': self.play_count,
            'pet_count': self.pet_count,
            'clean_count': self.clean_count
        }
    
    def to_dict(self):
        """
        轉換為字典（用於存檔）
        
        Returns:
            dict: 可序列化的狀態字典
        """
        return {
            'hunger': self.hunger,
            'happiness': self.happiness,
            'health': self.health,
            'energy': self.energy,
            'level': self.level,
            'experience': self.experience,
            'exp_to_next_level': self.exp_to_next_level,
            'birth_time': self.birth_time,
            'feed_count': self.feed_count,
            'play_count': self.play_count,
            'pet_count': self.pet_count,
            'clean_count': self.clean_count
        }
    
    def from_dict(self, data):
        """
        從字典載入（用於讀檔）
        
        Args:
            data: 狀態字典
        """
        self.hunger = data.get('hunger', 100)
        self.happiness = data.get('happiness', 100)
        self.health = data.get('health', 100)
        self.energy = data.get('energy', 100)
        self.level = data.get('level', 1)
        self.experience = data.get('experience', 0)
        self.exp_to_next_level = data.get('exp_to_next_level', 100)
        self.birth_time = data.get('birth_time', time.time())
        self.feed_count = data.get('feed_count', 0)
        self.play_count = data.get('play_count', 0)
        self.pet_count = data.get('pet_count', 0)
        self.clean_count = data.get('clean_count', 0)
        
        self.last_update = time.time()
        print("[PetStats] 從存檔載入狀態完成")
