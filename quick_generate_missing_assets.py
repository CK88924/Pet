# -*- coding: utf-8 -*-
"""
快速生成缺失的動畫素材（eat, play, happy, sad）
每個狀態產生 2 幀的簡單占位圖，方便測試。
"""
import os
from PIL import Image, ImageDraw

BASE_DIR = os.path.join('assets', 'default_cat')
SIZE = (128, 128)
BG_COLOR = (0, 0, 0, 0)

# 定義每個缺失動畫的顏色
STATE_COLORS = {
    'eat': (255, 200, 200, 255),   # 淺紅
    'play': (200, 200, 255, 255),  # 淺藍
    'happy': (255, 255, 150, 255), # 淺黃
    'sad': (150, 150, 255, 255),   # 淺紫
}

for state, color in STATE_COLORS.items():
    folder = os.path.join(BASE_DIR, state)
    os.makedirs(folder, exist_ok=True)
    for i in range(2):
        img = Image.new('RGBA', SIZE, BG_COLOR)
        draw = ImageDraw.Draw(img)
        # 繪製一個填滿顏色的矩形作為占位
        draw.rectangle([20, 20, 108, 108], fill=color)
        # 在左上角寫入狀態名稱和幀號，方便辨識
        draw.text((5, 5), f"{state}\n{i}")
        img_path = os.path.join(folder, f"{i}.png")
        img.save(img_path)
        print(f"生成 {state}/{i}.png")
print('所有缺失動畫已生成')
