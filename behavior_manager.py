# -*- coding: utf-8 -*-
"""
行為管理器
Behavior Manager
"""

import random
import config


class BehaviorManager:
    """管理寵物的行為邏輯"""
    
    def __init__(self):
        """初始化行為管理器"""
        self.current_behavior = 'idle'
        self.walk_direction = None  # 'left' 或 'right'
        self.behavior_start_time = 0
        self.behavior_duration = 0
    
    def choose_random_behavior(self):
        """
        根據機率隨機選擇行為
        
        Returns:
            行為名稱
        """
        rand = random.random()
        cumulative = 0
        
        for behavior, probability in config.BEHAVIOR_PROBABILITIES.items():
            cumulative += probability
            if rand <= cumulative:
                return behavior
        
        return 'idle'
    
    def update_behavior(self):
        """
        更新行為狀態
        
        Returns:
            新的行為狀態
        """
        behavior = self.choose_random_behavior()
        self.current_behavior = behavior
        
        # 如果是行走行為，隨機選擇方向
        if behavior == 'walk':
            self.walk_direction = random.choice(['left', 'right'])
            self.behavior_duration = random.randint(
                config.WALK_DURATION_MIN, 
                config.WALK_DURATION_MAX
            )
        
        return self.get_animation_state()
    
    def get_animation_state(self):
        """
        根據當前行為取得對應的動畫狀態
        
        Returns:
            動畫狀態名稱
        """
        if self.current_behavior == 'walk':
            return f'walk_{self.walk_direction}'
        else:
            return self.current_behavior
    
    def is_walking(self):
        """檢查是否正在行走"""
        return self.current_behavior == 'walk'
    
    def get_walk_direction(self):
        """取得行走方向"""
        return self.walk_direction
    
    def reverse_direction(self):
        """反轉行走方向（當碰到螢幕邊界時）"""
        if self.walk_direction == 'left':
            self.walk_direction = 'right'
        else:
            self.walk_direction = 'left'
