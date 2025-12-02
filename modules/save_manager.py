# -*- coding: utf-8 -*-
"""
存檔管理系統
Save/Load Management System
"""

import json
import os
from datetime import datetime


class SaveManager:
    """管理遊戲存檔"""
    
    def __init__(self, save_path='data/save.json'):
        """
        初始化存檔管理器
        
        Args:
            save_path: 存檔檔案路徑
        """
        self.save_path = save_path
        self.auto_save_interval = 300  # 自動存檔間隔（秒）
        
        print(f"[SaveManager] 存檔系統初始化完成 - 存檔路徑: {save_path}")
    
    def save_game(self, pet_stats, inventory, event_system):
        """
        儲存遊戲
        
        Args:
            pet_stats: PetStats 實例
            inventory: InventoryManager 實例
            event_system: EventSystem 實例
        
        Returns:
            bool: 是否成功
        """
        try:
            data = {
                'version': '2.0',
                'save_time': datetime.now().isoformat(),
                'pet_stats': pet_stats.to_dict(),
                'inventory': inventory.to_dict(),
                'event_system': event_system.to_dict()
            }
            
            # 確保目錄存在
            os.makedirs(os.path.dirname(self.save_path), exist_ok=True)
            
            # 寫入檔案
            with open(self.save_path, 'w', encoding='utf-8') as f:
                json.dump(data, f, indent=2, ensure_ascii=False)
            
            print(f"[SaveManager] 遊戲已儲存: {self.save_path}")
            return True
            
        except Exception as e:
            print(f"[SaveManager] 儲存失敗: {e}")
            return False
    
    def load_game(self, pet_stats, inventory, event_system):
        """
        載入遊戲
        
        Args:
            pet_stats: PetStats 實例
            inventory: InventoryManager 實例
            event_system: EventSystem 實例
        
        Returns:
            bool: 是否成功載入
        """
        if not os.path.exists(self.save_path):
            print(f"[SaveManager] 存檔不存在: {self.save_path}")
            return False
        
        try:
            with open(self.save_path, 'r', encoding='utf-8') as f:
                data = json.load(f)
            
            # 檢查版本
            version = data.get('version', '1.0')
            print(f"[SaveManager] 載入存檔版本: {version}")
            
            # 載入各系統資料
            if 'pet_stats' in data:
                pet_stats.from_dict(data['pet_stats'])
            
            if 'inventory' in data:
                inventory.from_dict(data['inventory'])
            
            if 'event_system' in data:
                event_system.from_dict(data['event_system'])
            
            save_time = data.get('save_time', '未知')
            print(f"[SaveManager] 遊戲已載入: {save_time}")
            return True
            
        except Exception as e:
            print(f"[SaveManager] 載入失敗: {e}")
            return False
    
    def save_exists(self):
        """
        檢查存檔是否存在
        
        Returns:
            bool: 存檔是否存在
        """
        return os.path.exists(self.save_path)
    
    def delete_save(self):
        """
        刪除存檔
        
        Returns:
            bool: 是否成功
        """
        try:
            if os.path.exists(self.save_path):
                os.remove(self.save_path)
                print(f"[SaveManager] 存檔已刪除: {self.save_path}")
                return True
            return False
        except Exception as e:
            print(f"[SaveManager] 刪除存檔失敗: {e}")
            return False
