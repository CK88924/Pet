# -*- coding: utf-8 -*-
"""
桌面寵物設定檔案
Configuration file for desktop pet
"""

import os

# 專案路徑設定
BASE_DIR = os.path.dirname(os.path.abspath(__file__))
ASSETS_DIR = os.path.join(BASE_DIR, 'assets')

# 當前使用的寵物（可修改此值來切換寵物）
CURRENT_PET = 'default_cat'

# 寵物素材路徑
PET_ASSETS_DIR = os.path.join(ASSETS_DIR, CURRENT_PET)

# 視窗設定
WINDOW_WIDTH = 128
WINDOW_HEIGHT = 128
WINDOW_ALWAYS_ON_TOP = True

# 動畫設定
ANIMATION_SPEED = 100  # 毫秒，每幀之間的間隔
ANIMATION_STATES = {
    'idle': {
        'frames': 2,
        'speed': 200,
        'folder': 'idle'
    },
    'walk_left': {
        'frames': 4,
        'speed': 100,
        'folder': 'walk_left'
    },
    'walk_right': {
        'frames': 4,
        'speed': 100,
        'folder': 'walk_right'
    },
    'sleep': {
        'frames': 2,
        'speed': 300,
        'folder': 'sleep'
    },
    'sit': {
        'frames': 1,
        'speed': 100,
        'folder': 'sit'
    },
    'eat': {
        'frames': 2,
        'speed': 200,
        'folder': 'eat'
    },
    'play': {
        'frames': 2,
        'speed': 150,
        'folder': 'play'
    },
    'happy': {
        'frames': 2,
        'speed': 200,
        'folder': 'happy'
    },
    'sad': {
        'frames': 2,
        'speed': 300,
        'folder': 'sad'
    }
}

# 動畫鏡像設定 (key 由 value 鏡像生成)
MIRROR_ANIMATIONS = {
    'walk_left': 'walk_right',
}

# 可選動畫 (如果缺少，將使用 idle 替代)
OPTIONAL_ANIMATIONS = ['sleep', 'sit', 'eat', 'play', 'happy', 'sad']

# 行為設定
BEHAVIOR_UPDATE_INTERVAL = 3000  # 毫秒，行為更新間隔
BEHAVIOR_PROBABILITIES = {
    'idle': 0.4,      # 40% 閒置
    'walk': 0.3,      # 30% 行走
    'sleep': 0.2,     # 20% 睡覺
    'sit': 0.1        # 10% 坐下
}

# 移動設定
MOVE_SPEED = 2  # 像素/幀
WALK_DURATION_MIN = 2000  # 毫秒
WALK_DURATION_MAX = 5000  # 毫秒

# 螢幕邊界設定
SCREEN_MARGIN = 10  # 離螢幕邊緣的最小距離（像素）
