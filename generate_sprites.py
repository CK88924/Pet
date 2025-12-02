# -*- coding: utf-8 -*-
"""
Generate simple cat sprites for desktop pet
生成簡單的貓咪精靈圖
"""

from PIL import Image, ImageDraw
import os

# 建立輸出目錄
BASE_DIR = "assets/default_cat"

# 尺寸
SIZE = (128, 128)

# 顏色
BG_COLOR = (0, 0, 0, 0)  # 透明背景
CAT_COLOR = (255, 255, 255, 255)  # 白色
SPOT_COLOR = (0, 0, 0, 255)  # 黑色斑點
EYE_COLOR = (0, 0, 0, 255)  # 黑色眼睛
NOSE_COLOR = (255, 192, 203, 255)  # 粉紅色鼻子
ITEM_COLOR = (255, 100, 100, 255)  # 物品顏色（紅蘋果/球）


def draw_cat_base(draw, offset_y=0, sitting=False, happy=False, sad=False):
    """繪製貓的基本形狀"""
    # 身體
    if sitting:
        # 坐姿：橢圓形身體
        draw.ellipse([30, 50+offset_y, 98, 110+offset_y], fill=CAT_COLOR)
    else:
        # 站姿：橢圓形身體
        draw.ellipse([25, 60+offset_y, 103, 100+offset_y], fill=CAT_COLOR)
    
    # 頭部
    draw.ellipse([38, 30+offset_y, 90, 75+offset_y], fill=CAT_COLOR)
    
    # 耳朵（三角形）
    if sad:
        # 難過時耳朵下垂
        draw.polygon([(38, 45+offset_y), (45, 55+offset_y), (50, 40+offset_y)], fill=CAT_COLOR)
        draw.polygon([(78, 40+offset_y), (83, 55+offset_y), (90, 45+offset_y)], fill=CAT_COLOR)
    else:
        draw.polygon([(42, 40+offset_y), (50, 25+offset_y), (58, 40+offset_y)], fill=CAT_COLOR)
        draw.polygon([(70, 40+offset_y), (78, 25+offset_y), (86, 40+offset_y)], fill=CAT_COLOR)
    
    # 眼睛
    if happy:
        # 開心眼 ^ ^
        draw.line([(48, 55+offset_y), (51, 50+offset_y), (55, 55+offset_y)], fill=EYE_COLOR, width=2)
        draw.line([(73, 55+offset_y), (76, 50+offset_y), (80, 55+offset_y)], fill=EYE_COLOR, width=2)
    elif sad:
        # 難過眼 T T
        draw.line([(48, 52+offset_y), (55, 52+offset_y)], fill=EYE_COLOR, width=2)
        draw.line([(51, 52+offset_y), (51, 58+offset_y)], fill=EYE_COLOR, width=2)
        draw.line([(73, 52+offset_y), (80, 52+offset_y)], fill=EYE_COLOR, width=2)
        draw.line([(76, 52+offset_y), (76, 58+offset_y)], fill=EYE_COLOR, width=2)
    else:
        # 正常眼
        draw.ellipse([48, 48+offset_y, 55, 58+offset_y], fill=EYE_COLOR)
        draw.ellipse([73, 48+offset_y, 80, 58+offset_y], fill=EYE_COLOR)
    
    # 鼻子
    draw.ellipse([61, 60+offset_y, 67, 65+offset_y], fill=NOSE_COLOR)
    
    # 斑點
    draw.ellipse([75, 35+offset_y, 85, 45+offset_y], fill=SPOT_COLOR)
    
    if not sitting:
        # 腿（只在站立時顯示）
        draw.rectangle([35, 95+offset_y, 43, 110+offset_y], fill=CAT_COLOR)
        draw.rectangle([52, 95+offset_y, 60, 110+offset_y], fill=CAT_COLOR)
        draw.rectangle([68, 95+offset_y, 76, 110+offset_y], fill=CAT_COLOR)
        draw.rectangle([85, 95+offset_y, 93, 110+offset_y], fill=CAT_COLOR)
    
    # 尾巴
    if sitting:
        # 坐姿尾巴（捲曲）
        draw.arc([88, 55+offset_y, 118, 95+offset_y], 180, 360, fill=CAT_COLOR, width=8)
    else:
        # 站姿尾巴
        draw.arc([90, 65+offset_y, 120, 95+offset_y], 180, 360, fill=CAT_COLOR, width=6)


def create_idle_frames():
    """建立閒置動畫幀"""
    print("正在生成閒置動畫...")
    img = Image.new('RGBA', SIZE, BG_COLOR)
    draw = ImageDraw.Draw(img)
    draw_cat_base(draw)
    img.save(os.path.join(BASE_DIR, 'idle', '0.png'))
    
    img = Image.new('RGBA', SIZE, BG_COLOR)
    draw = ImageDraw.Draw(img)
    draw_cat_base(draw, offset_y=-2)
    img.save(os.path.join(BASE_DIR, 'idle', '1.png'))


def create_walk_frames(direction='right'):
    """建立行走動畫幀"""
    print(f"正在生成向{direction}行走動畫...")
    folder = f'walk_{direction}'
    for i in range(4):
        img = Image.new('RGBA', SIZE, BG_COLOR)
        draw = ImageDraw.Draw(img)
        offset_y = -3 if i % 2 == 0 else 0
        draw_cat_base(draw, offset_y=offset_y)
        if direction == 'left':
            img = img.transpose(Image.FLIP_LEFT_RIGHT)
        img.save(os.path.join(BASE_DIR, folder, f'{i}.png'))


def create_sleep_frames():
    """建立睡覺動畫幀"""
    print("正在生成睡覺動畫...")
    for i in range(2):
        img = Image.new('RGBA', SIZE, BG_COLOR)
        draw = ImageDraw.Draw(img)
        # 躺下的貓
        draw.ellipse([20, 60, 108, 90], fill=CAT_COLOR)
        draw.ellipse([85, 50, 118, 78], fill=CAT_COLOR)
        draw.polygon([(90, 55), (95, 45), (100, 55)], fill=CAT_COLOR)
        draw.polygon([(105, 55), (110, 45), (115, 55)], fill=CAT_COLOR)
        if i == 0:
            draw.line([(92, 62), (98, 62)], fill=EYE_COLOR, width=2)
            draw.line([(105, 62), (111, 62)], fill=EYE_COLOR, width=2)
        else:
            draw.ellipse([92, 61, 98, 63], fill=EYE_COLOR)
            draw.ellipse([105, 61, 111, 63], fill=EYE_COLOR)
        draw.ellipse([99, 68, 103, 71], fill=NOSE_COLOR)
        draw.ellipse([95, 52, 102, 58], fill=SPOT_COLOR)
        draw.arc([15, 65, 35, 85], 90, 270, fill=CAT_COLOR, width=5)
        img.save(os.path.join(BASE_DIR, 'sleep', f'{i}.png'))


def create_sit_frame():
    """建立坐下幀"""
    print("正在生成坐下動畫...")
    img = Image.new('RGBA', SIZE, BG_COLOR)
    draw = ImageDraw.Draw(img)
    draw_cat_base(draw, sitting=True)
    img.save(os.path.join(BASE_DIR, 'sit', '0.png'))


def create_eat_frames():
    """建立吃東西動畫"""
    print("正在生成吃東西動畫...")
    for i in range(2):
        img = Image.new('RGBA', SIZE, BG_COLOR)
        draw = ImageDraw.Draw(img)
        draw_cat_base(draw, sitting=True)
        
        # 畫一個蘋果
        apple_y = 90 if i == 0 else 85  # 蘋果上下動
        draw.ellipse([80, apple_y, 100, apple_y+20], fill=(255, 50, 50, 255))
        draw.line([(90, apple_y), (90, apple_y-5)], fill=(0, 100, 0, 255), width=2)
        
        img.save(os.path.join(BASE_DIR, 'eat', f'{i}.png'))


def create_play_frames():
    """建立玩耍動畫"""
    print("正在生成玩耍動畫...")
    for i in range(2):
        img = Image.new('RGBA', SIZE, BG_COLOR)
        draw = ImageDraw.Draw(img)
        
        offset_y = -10 if i == 1 else 0  # 跳躍
        draw_cat_base(draw, offset_y=offset_y, happy=True)
        
        # 畫一個球
        ball_x = 100 if i == 0 else 105
        draw.ellipse([ball_x, 90, ball_x+20, 110], fill=(50, 50, 255, 255))
        
        img.save(os.path.join(BASE_DIR, 'play', f'{i}.png'))


def create_happy_frames():
    """建立開心動畫"""
    print("正在生成開心動畫...")
    for i in range(2):
        img = Image.new('RGBA', SIZE, BG_COLOR)
        draw = ImageDraw.Draw(img)
        
        offset_y = -5 if i == 1 else 0  # 輕微跳動
        draw_cat_base(draw, offset_y=offset_y, happy=True)
        
        # 愛心 (用圖形繪製)
        if i == 1:
            # 左圓
            draw.ellipse([95, 30, 105, 40], fill=(255, 0, 0, 255))
            # 右圓
            draw.ellipse([105, 30, 115, 40], fill=(255, 0, 0, 255))
            # 下方三角形
            draw.polygon([(95, 35), (115, 35), (105, 45)], fill=(255, 0, 0, 255))
        
        img.save(os.path.join(BASE_DIR, 'happy', f'{i}.png'))


def create_sad_frames():
    """建立難過動畫"""
    print("正在生成難過動畫...")
    for i in range(2):
        img = Image.new('RGBA', SIZE, BG_COLOR)
        draw = ImageDraw.Draw(img)
        
        draw_cat_base(draw, sad=True)
        
        # 淚水
        if i == 1:
            draw.ellipse([50, 60, 53, 65], fill=(100, 100, 255, 255))
            draw.ellipse([75, 60, 78, 65], fill=(100, 100, 255, 255))
        
        img.save(os.path.join(BASE_DIR, 'sad', f'{i}.png'))


def main():
    """主程式"""
    print("=" * 50)
    print("開始生成桌面寵物素材...")
    print("=" * 50)
    
    # 確保目錄存在
    folders = ['idle', 'walk_left', 'walk_right', 'sleep', 'sit', 
               'eat', 'play', 'happy', 'sad']
    for folder in folders:
        os.makedirs(os.path.join(BASE_DIR, folder), exist_ok=True)
    
    # 生成所有動畫
    create_idle_frames()
    create_walk_frames('right')
    create_walk_frames('left')
    create_sleep_frames()
    create_sit_frame()
    create_eat_frames()
    create_play_frames()
    create_happy_frames()
    create_sad_frames()
    
    print("=" * 50)
    print("所有素材生成完成！")
    print(f"素材位置：{BASE_DIR}")
    print("=" * 50)


if __name__ == "__main__":
    try:
        main()
    except Exception as e:
        import traceback
        traceback.print_exc()
