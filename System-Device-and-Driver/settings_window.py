from PyQt5.QtWidgets import *
from PyQt5.QtCore import *


class ToggleSlider(QSlider):
    def __init__(self, parent=None):
        super().__init__(Qt.Horizontal, parent)
        self.setRange(0, 1)
        self.setFixedWidth(100)
        self.setValue(1)

    def mousePressEvent(self, e):
        if e.button() == Qt.LeftButton:
            self.setValue(0 if self.value() == 1 else 1)
            self.valueChanged.emit(self.value())


class SettingsWindow(QWidget):
    def __init__(self, cfg):
        super().__init__()
        self.config_manager = cfg
        self.button_widgets = []
        self.init_ui()
        self.load_current_config()

    def init_ui(self):
        self.setStyleSheet("""
            QWidget { background-color: #1a1a2e; }
            QLabel { color: #e6e6e6; font-size: 14px; }
            QSlider::groove:horizontal { background: #0f3460; height: 8px; border-radius: 4px; border: 1px solid #16213e; }
            QSlider::sub-page:horizontal { background: #00b4d8; border-radius: 4px; }
            QSlider::add-page:horizontal { background: #0f3460; border-radius: 4px; }
            QSlider::handle:horizontal { background: white; width: 20px; height: 20px; border-radius: 10px; margin: -6px 0; border: 2px solid #00b4d8; }
            QComboBox { background: #16213e; color: #e6e6e6; border: 1px solid #0f3460; border-radius: 4px; padding: 6px; min-width: 160px; }
            QComboBox:hover { border-color: #00b4d8; }
            QPushButton { background: #0f3460; color: white; border-radius: 6px; padding: 10px 20px; font-size: 13px; min-width: 120px; }
            QPushButton:hover { background: #00b4d8; }
        """)

        layout = QVBoxLayout()
        layout.setSpacing(20)
        layout.setContentsMargins(30, 30, 30, 30)

        header_container = QWidget()
        header_container.setFixedHeight(60)
        header_container.setStyleSheet("""
            QWidget {
                background: transparent;
                border-bottom: 2px solid #0f3460;# 
            }
        """)

        header_layout = QVBoxLayout(header_container)
        header_layout.setContentsMargins(0, 0, 0, 0)

        title = QLabel("Настройки управления")
        title.setStyleSheet("QLabel { font-size: 20px; font-weight: bold; color: #00b4d8; }")
        title.setAlignment(Qt.AlignCenter)

        header_layout.addStretch()
        header_layout.addWidget(title)
        header_layout.addStretch()

        layout.addWidget(header_container)

        self.buttons_container = QWidget()
        buttons_layout = QVBoxLayout()
        buttons_layout.setSpacing(25)

        for i in range(3):
            btn_setting = self.create_button_setting(i + 1)
            buttons_layout.addWidget(btn_setting)

        self.buttons_container.setLayout(buttons_layout)
        layout.addWidget(self.buttons_container)
        layout.addStretch()

        actions = QHBoxLayout()
        self.save_btn = QPushButton("Сохранить")
        self.save_btn.clicked.connect(self.save_config)
        self.save_btn.setStyleSheet("background: #00b4d8; font-weight: bold;")

        self.load_btn = QPushButton("Загрузить")
        self.load_btn.clicked.connect(self.load_config)
        self.load_btn.setMinimumWidth(120)

        self.default_btn = QPushButton("Сбросить")
        self.default_btn.clicked.connect(self.reset_to_default)
        self.default_btn.setMinimumWidth(120)

        actions.addWidget(self.load_btn)
        actions.addWidget(self.default_btn)
        actions.addStretch()
        actions.addWidget(self.save_btn)
        layout.addLayout(actions)
        self.setLayout(layout)

    def create_button_setting(self, btn_id):
        container = QWidget()
        container.setStyleSheet("QWidget { background: #16213e; border-radius: 8px; padding: 15px; }")
        layout = QHBoxLayout()
        layout.setSpacing(20)

        label = QLabel(f"Кнопка {btn_id}")
        label.setStyleSheet("font-size: 15px; font-weight: bold; color: #00b4d8; min-width: 90px;")

        slider = ToggleSlider()
        cmds = ['действие1', 'действие2', 'действие3']
        cmd_vals = ['action1', 'action2', 'action3']

        combo = QComboBox()
        combo.addItems(cmds)
        combo.setMinimumWidth(160)

        btn_data = {
            'id': btn_id,
            'slider': slider,
            'combo': combo,
            'command_values': cmd_vals,
            'commands': cmds
        }
        self.button_widgets.append(btn_data)

        slider.valueChanged.connect(lambda v, idx=len(self.button_widgets) - 1: self.on_slider_changed(idx, v))
        combo.currentIndexChanged.connect(lambda i, idx=len(self.button_widgets) - 1: self.on_command_changed(idx, i))

        layout.addWidget(label)
        layout.addStretch()
        layout.addWidget(slider)
        layout.addSpacing(20)
        layout.addWidget(combo)
        container.setLayout(layout)
        return container

    def on_slider_changed(self, idx, val):
        enabled = val == 1
        btn_id = self.button_widgets[idx]['id']
        cmd = self.button_widgets[idx]['command_values'][self.button_widgets[idx]['combo'].currentIndex()]
        self.config_manager.update_button_state(btn_id, enabled, cmd)
        self.config_manager.log_message_signal.emit(f"Кнопка {btn_id}: {'включена' if enabled else 'выключена'}",
                                                    "BUTTON")

    def on_command_changed(self, idx, combo_idx):
        if combo_idx >= 0:
            btn_id = self.button_widgets[idx]['id']
            cmd = self.button_widgets[idx]['command_values'][combo_idx]
            enabled = self.button_widgets[idx]['slider'].value() == 1
            self.config_manager.update_button_state(btn_id, enabled, cmd)
            cmd_name = self.button_widgets[idx]['commands'][combo_idx]
            self.config_manager.log_message_signal.emit(f"Кнопка {btn_id}: команда '{cmd_name}'", "BUTTON")

    def load_current_config(self):
        config = self.config_manager.load_config()
        for btn_cfg in config.get('buttons', []):
            btn_id = btn_cfg.get('id', 1) - 1
            if 0 <= btn_id < len(self.button_widgets):
                self.button_widgets[btn_id]['slider'].setValue(1 if btn_cfg.get('enabled', True) else 0)
                cmd = btn_cfg.get('command', 'action1')
                if cmd in self.button_widgets[btn_id]['command_values']:
                    idx = self.button_widgets[btn_id]['command_values'].index(cmd)
                    self.button_widgets[btn_id]['combo'].setCurrentIndex(idx)
        self.config_manager.log_message_signal.emit("Настройки загружены", "CONFIG")

    def save_config(self):
        data = {'buttons': [], 'settings': {'version': '1.0'}}
        for b in self.button_widgets:
            enabled = b['slider'].value() == 1
            cmd = b['command_values'][b['combo'].currentIndex()]
            data['buttons'].append({
                'id': b['id'],
                'enabled': enabled,
                'command': cmd,
                'name': f'Кнопка {b["id"]}'
            })

        if self.config_manager.save_config(data):
            QMessageBox.information(self, "Сохранение", "Настройки сохранены!")

    def load_config(self):
        self.load_current_config()
        QMessageBox.information(self, "Загрузка", "Настройки загружены")

    def reset_to_default(self):
        reply = QMessageBox.question(self, "Сброс", "Сбросить все настройки?", QMessageBox.Yes | QMessageBox.No)
        if reply == QMessageBox.Yes:
            for b in self.button_widgets:
                b['slider'].setValue(1)
                b['combo'].setCurrentIndex(0)
            self.config_manager.log_message_signal.emit("Настройки сброшены", "CONFIG")