import json
import os
from datetime import datetime
from PyQt5.QtCore import QObject, pyqtSignal


class ConfigManager(QObject):
    config_changed = pyqtSignal(dict)
    log_message_signal = pyqtSignal(str, str)
    button_state_changed = pyqtSignal(int, bool, str)

    def __init__(self):
        super().__init__()
        self.config_file = "button_config.json"
        self.default_config = {
            'buttons': [
                {'id': 1, 'enabled': True, 'command': 'action1', 'name': 'Кнопка 1'},
                {'id': 2, 'enabled': True, 'command': 'action2', 'name': 'Кнопка 2'},
                {'id': 3, 'enabled': True, 'command': 'action3', 'name': 'Кнопка 3'}
            ],
            'settings': {'version': '1.0', 'last_saved': ''}
        }

    def load_config(self):
        try:
            if os.path.exists(self.config_file):
                with open(self.config_file, 'r', encoding='utf-8') as f:
                    return json.load(f)
        except Exception as e:
            self.log_message_signal.emit(f"Ошибка загрузки: {str(e)}", "ERROR")
        return self.default_config

    def save_config(self, data):
        try:
            data['settings']['last_saved'] = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
            with open(self.config_file, 'w', encoding='utf-8') as f:
                json.dump(data, f, ensure_ascii=False, indent=2)
            self.config_changed.emit(data)
            self.log_message_signal.emit("Конфигурация сохранена", "CONFIG")
            return True
        except Exception as e:
            self.log_message_signal.emit(f"Ошибка сохранения: {str(e)}", "ERROR")
            return False

    def update_button_state(self, btn_id, enabled, cmd):
        self.button_state_changed.emit(btn_id, enabled, cmd)