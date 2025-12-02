# -*- coding: utf-8 -*-
from PyQt5.QtWidgets import QWidget, QVBoxLayout, QLabel, QProgressBar, QPushButton, QGroupBox, QHBoxLayout, QListWidget, QMessageBox
from PyQt5.QtCore import pyqtSignal, Qt


class StatusPanel(QWidget):
    """寵物狀態顯示面板"""

    save_requested = pyqtSignal()
    exit_requested = pyqtSignal()

    def __init__(self, pet_stats, inventory, interaction_manager, event_system):
        super().__init__()

        self.pet_stats = pet_stats
        self.inventory = inventory
        self.interaction_manager = interaction_manager
        self.event_system = event_system

        self.setWindowFlags(Qt.WindowStaysOnTopHint | Qt.Tool)
        self.setFixedSize(300, 520)
        self.setWindowTitle("🐾 寵物控制面板")

        layout = QVBoxLayout()
        layout.addWidget(self.create_status_group())
        layout.addWidget(self.create_inventory_group())
        layout.addWidget(self.create_interaction_group())  # ⭐ 新增互動控制區
        layout.addWidget(self.create_control_group())
        self.setLayout(layout)

    # ──────────────────────────────────────────────
    # 狀態群組
    # ──────────────────────────────────────────────
    def create_status_group(self):
        group = QGroupBox("📊 寵物狀態")
        layout = QVBoxLayout()

        self.hunger_bar = self.create_bar("飢餓度", self.pet_stats.hunger)
        self.happiness_bar = self.create_bar("快樂度", self.pet_stats.happiness)
        self.health_bar = self.create_bar("健康", self.pet_stats.health)
        self.energy_bar = self.create_bar("精力", self.pet_stats.energy)

        for bar in [self.hunger_bar, self.happiness_bar, self.health_bar, self.energy_bar]:
            layout.addWidget(bar["label"])
            layout.addWidget(bar["bar"])

        group.setLayout(layout)
        return group

    def create_bar(self, name, value):
        label = QLabel(f"{name}: {round(value,2)}/100")
        bar = QProgressBar()
        bar.setValue(int(value))
        return {"label": label, "bar": bar}

    # ──────────────────────────────────────────────
    # 庫存
    # ──────────────────────────────────────────────
    def create_inventory_group(self):
        group = QGroupBox("🎒 物品")
        layout = QVBoxLayout()
        self.inventory_list = QListWidget()
        self.update_inventory_list()
        layout.addWidget(self.inventory_list)
        group.setLayout(layout)
        return group

    # ──────────────────────────────────────────────
    # ⭐ 互動控制功能區
    # ──────────────────────────────────────────────
    def create_interaction_group(self):
        group = QGroupBox("🧩 互動")
        layout = QHBoxLayout()

        btn_feed = QPushButton("🍎 餵食")
        btn_feed.clicked.connect(self.on_feed)

        btn_play = QPushButton("🎾 玩耍")
        btn_play.clicked.connect(self.on_play)

        btn_pet = QPushButton("🐾 撫摸")
        btn_pet.clicked.connect(self.on_pet)

        btn_clean = QPushButton("🧼 清潔")
        btn_clean.clicked.connect(self.on_clean)

        btn_rest = QPushButton("😴 休息")
        btn_rest.clicked.connect(self.on_rest)

        for btn in [btn_feed, btn_play, btn_pet, btn_clean, btn_rest]:
            btn.setStyleSheet("font-size: 13px; padding:4px;")

        layout.addWidget(btn_feed)
        layout.addWidget(btn_play)
        layout.addWidget(btn_pet)
        layout.addWidget(btn_clean)
        layout.addWidget(btn_rest)

        group.setLayout(layout)
        return group

    # ──────────────────────────────────────────────
    # 動作功能
    # ──────────────────────────────────────────────
    def on_feed(self):
        item = self.inventory.get_random_food()
        if item:
            self.interaction_manager.feed(item)
            self.refresh_stats()
        else:
            QMessageBox.warning(self, "沒有食物", "❗ 你沒有可以餵食的物品了！")

    def on_play(self):
        self.interaction_manager.play()
        self.refresh_stats()

    def on_pet(self):
        self.interaction_manager.pet()
        self.refresh_stats()

    def on_clean(self):
        self.interaction_manager.clean()
        self.refresh_stats()

    def on_rest(self):
        self.interaction_manager.rest()
        self.refresh_stats()

    # ──────────────────────────────────────────────
    # UI 更新
    # ──────────────────────────────────────────────
    def refresh_stats(self):
        bars = [
            ("飢餓度", self.hunger_bar, self.pet_stats.hunger),
            ("快樂度", self.happiness_bar, self.pet_stats.happiness),
            ("健康", self.health_bar, self.pet_stats.health),
            ("精力", self.energy_bar, self.pet_stats.energy)
        ]
        for text, bar, value in bars:
            bar["label"].setText(f"{text}: {round(value,2)}/100")
            bar["bar"].setValue(int(value))

        self.update_inventory_list()
        self.repaint()

    def update_inventory_list(self):
        self.inventory_list.clear()
        for item, qty in self.inventory.inventory.items():
            self.inventory_list.addItem(f"{item} × {qty}")

    # ──────────────────────────────────────────────
    # 存檔 & 退出
    # ──────────────────────────────────────────────
    def create_control_group(self):
        group = QGroupBox("⚙ 控制區")
        layout = QHBoxLayout()

        btn_save = QPushButton("💾 存檔")
        btn_save.clicked.connect(self.on_save)

        btn_hide = QPushButton("🙈 隱藏")
        btn_hide.clicked.connect(self.hide)

        btn_exit = QPushButton("❌ 退出")
        btn_exit.clicked.connect(self.on_exit)

        layout.addWidget(btn_save)
        layout.addWidget(btn_hide)
        layout.addWidget(btn_exit)
        group.setLayout(layout)
        return group

    def on_save(self):
        self.save_requested.emit()

    def on_exit(self):
        reply = QMessageBox.question(
            self, "退出確認", "確定退出程式嗎？（會自動存檔）",
            QMessageBox.Yes | QMessageBox.No
        )
        if reply == QMessageBox.Yes:
            self.exit_requested.emit()
