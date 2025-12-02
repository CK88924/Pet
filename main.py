# -*- coding: utf-8 -*-
"""
桌面寵物 2.1 修正版
修復內容：
1. 🖱 右鍵可開啟控制面板
2. 🚫 不再走出螢幕，會自動反向
"""

import sys, os
from PyQt5.QtWidgets import QApplication, QLabel, QMenu, QAction, QSystemTrayIcon
from PyQt5.QtCore import Qt, QTimer, QPoint
from PyQt5.QtGui import QPixmap, QIcon, QTransform

import config
from behavior_manager import BehaviorManager

# Modules
from modules.pet_stats import PetStats
from modules.inventory_manager import InventoryManager
from modules.interaction_manager import InteractionManager
from modules.event_system import EventSystem
from modules.save_manager import SaveManager
from modules.ui_panel import StatusPanel


class DesktopPet2(QLabel):

    def __init__(self):
        super().__init__()

        print("[Pet2.0] 初始化桌面寵物 2.0...")

        # internal state
        self.dragging = False
        self.drag_pos = QPoint()
        self.current_state = None
        self.current_frame = 0
        self.frame_count = 0
        self.animations = {}

        # system modules
        self.pet_stats = PetStats()
        self.inventory = InventoryManager()
        self.interaction_manager = InteractionManager(self.pet_stats, self.inventory)
        self.event_system = EventSystem(self.pet_stats, self.inventory)
        self.save_manager = SaveManager()
        self.behavior_manager = BehaviorManager()

        # UI 控制面板
        self.status_panel = StatusPanel(
            self.pet_stats, self.inventory, self.interaction_manager, self.event_system
        )

        # Timers
        self.animation_timer = QTimer(self)
        self.animation_timer.timeout.connect(self.update_animation)

        self.behavior_timer = QTimer(self)
        self.behavior_timer.timeout.connect(self.update_behavior)

        self.movement_timer = QTimer(self)
        self.movement_timer.timeout.connect(self.update_movement)

        self.stats_timer = QTimer(self)
        self.stats_timer.timeout.connect(self.update_stats)

        self.event_timer = QTimer(self)
        self.event_timer.timeout.connect(self.check_events)

        self.autosave_timer = QTimer(self)
        self.autosave_timer.timeout.connect(self.auto_save)

        # Load save if exists
        if self.save_manager.save_exists():
            self.save_manager.load_game(self.pet_stats, self.inventory, self.event_system)

        self.load_animations()
        self.setup_window()
        self.create_tray_icon()
        self.connect_signals()

        # start timers
        self.animation_timer.start(config.ANIMATION_SPEED)
        self.behavior_timer.start(config.BEHAVIOR_UPDATE_INTERVAL)
        self.movement_timer.start(16)
        self.stats_timer.start(1000)
        self.event_timer.start(30000)
        self.autosave_timer.start(300000)

        print("[Pet2.0] 初始化完成！")

    # ─────────────────────────────────────────
    # Window settings
    # ─────────────────────────────────────────
    def setup_window(self):
        # ⭐ 修復：允許滑鼠事件 & 不顯示邊框
        self.setWindowFlags(Qt.FramelessWindowHint | Qt.WindowStaysOnTopHint | Qt.Tool)
        self.setAttribute(Qt.WA_TranslucentBackground)
        self.setFixedSize(config.WINDOW_WIDTH, config.WINDOW_HEIGHT)
        self.move(600, 600)

    # ─────────────────────────────────────────
    # Mouse events (拖曳 + 右鍵叫面板)
    # ─────────────────────────────────────────
    def mousePressEvent(self, event):
        """滑鼠事件處理"""
        if event.button() == Qt.LeftButton:
            self.dragging = True
            self.drag_pos = event.globalPos() - self.pos()

        elif event.button() == Qt.RightButton:
            self.toggle_panel()

    def mouseMoveEvent(self, event):
        if self.dragging:
            self.move(event.globalPos() - self.drag_pos)

    def mouseReleaseEvent(self, event):
        self.dragging = False

    # ─────────────────────────────────────────
    # 系統托盤
    # ─────────────────────────────────────────
    def create_tray_icon(self):
        icon = QIcon(self.animations["idle"]["frames"][0])
        self.tray = QSystemTrayIcon(icon, self)

        menu = QMenu()
        menu.addAction("📊 控制面板", self.toggle_panel)
        menu.addAction("💾 存檔", self.manual_save)
        menu.addSeparator()
        menu.addAction("❌ 退出", self.quit_app)

        self.tray.setContextMenu(menu)
        self.tray.show()

    def toggle_panel(self):
        if self.status_panel.isVisible():
            self.status_panel.hide()
        else:
            self.status_panel.show()

    # ─────────────────────────────────────────
    # 動畫系統
    # ─────────────────────────────────────────
    def load_animations(self):
        print("[Pet2.0] 🔍 載入動畫...")

        for state, info in config.ANIMATION_STATES.items():
            if state not in config.MIRROR_ANIMATIONS:
                self._load_frames(state, info["folder"], info["frames"], info["speed"])

        # 鏡像生成
        for new_state, src_state in config.MIRROR_ANIMATIONS.items():
            print(f"  ⟳ 自動生成鏡像動畫 → {new_state}（來源: {src_state}）")
            frames = self.animations[src_state]["frames"]
            mirrored = [pix.transformed(QTransform().scale(-1, 1)) for pix in frames]
            self.animations[new_state] = {"frames": mirrored, "speed": self.animations[src_state]["speed"]}

        # idle fallback
        if "idle" in self.animations:
            idle_frames = self.animations["idle"]["frames"]
            idle_speed = self.animations["idle"]["speed"]
            for key, anim in list(self.animations.items()):
                if len(anim["frames"]) == 0:
                    print(f"  ⚠ {key} 沒圖片 → 使用 idle 替代")
                    self.animations[key] = {"frames": idle_frames, "speed": idle_speed}

        self.set_animation_state("idle")

    def _load_frames(self, state, folder, count, speed):
        path = os.path.join(config.PET_ASSETS_DIR, folder)
        frames = []

        for i in range(count):
            fp = os.path.join(path, f"{i}.png")
            if os.path.exists(fp):
                frames.append(QPixmap(fp))

        self.animations[state] = {"frames": frames, "speed": speed}
        print(f"  ✓ 載入動畫: {state} ({len(frames)} 幀)")

    def set_animation_state(self, state):
        if state in self.animations:
            self.current_state = state
            self.current_frame = 0
            self.frame_count = len(self.animations[state]["frames"])
            self.animation_timer.setInterval(self.animations[state]["speed"])

    def update_animation(self):
        if self.frame_count == 0:
            return
        frames = self.animations[self.current_state]["frames"]
        self.setPixmap(frames[self.current_frame])
        self.current_frame = (self.current_frame + 1) % self.frame_count

    # ─────────────────────────────────────────
    # Movement & boundary constraint
    # ─────────────────────────────────────────
    def update_behavior(self):
        self.set_animation_state(self.behavior_manager.update_behavior())

    def update_movement(self):
        if not self.behavior_manager.is_walking() or self.dragging:
            return

        direction = self.behavior_manager.get_walk_direction()
        new_x = self.x() + (config.MOVE_SPEED if direction == "right" else -config.MOVE_SPEED)
        screen_width = QApplication.primaryScreen().size().width()

        # ⭐ 防止走出螢幕邊界
        if new_x < 0:
            new_x = 0
            self.behavior_manager.force_flip_direction("right")

        elif new_x + self.width() > screen_width:
            new_x = screen_width - self.width()
            self.behavior_manager.force_flip_direction("left")

        self.move(new_x, self.y())

    # ─────────────────────────────────────────
    # Stats / Events
    # ─────────────────────────────────────────
    def update_stats(self):
        self.pet_stats.update()
        self.status_panel.refresh_stats()

    def check_events(self):
        self.event_system.try_trigger_event()
        self.event_system.check_achievements()

    # ─────────────────────────────────────────
    # Save System
    # ─────────────────────────────────────────
    def auto_save(self):
        self.manual_save()

    def manual_save(self):
        self.save_manager.save_game(self.pet_stats, self.inventory, self.event_system)

    def connect_signals(self):
        self.status_panel.save_requested.connect(self.manual_save)
        self.status_panel.exit_requested.connect(self.quit_app)

    # ─────────────────────────────────────────
    # Quit
    # ─────────────────────────────────────────
    def quit_app(self):
        print("[Pet2.0] 正在退出並自動存檔...")
        self.manual_save()
        self.tray.hide()
        QApplication.quit()


def main():
    app = QApplication(sys.argv)
    app.setQuitOnLastWindowClosed(False)
    pet = DesktopPet2()
    pet.show()
    print("\n🐾 桌面寵物 2.0 已啟動！")
    sys.exit(app.exec_())


if __name__ == "__main__":
    main()
