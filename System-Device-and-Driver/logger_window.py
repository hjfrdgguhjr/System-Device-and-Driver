import os
from datetime import datetime
from PyQt5.QtWidgets import *

class LoggerWindow(QMainWindow):
    def __init__(self, cfg):
        super().__init__()
        self.config_manager = cfg
        self.log_count = 0
        self.init_ui()
        self.config_manager.log_message_signal.connect(self.add_log_message)

    def init_ui(self):
        self.setWindowTitle("Логи системы")
        self.setGeometry(250, 250, 700, 450)

        self.setStyleSheet("""
            QMainWindow { background-color: #1a1a2e; }
            QTextEdit { background-color: #0f3460; color: #e6e6e6; border: 1px solid #16213e; border-radius: 5px; font-family: monospace; font-size: 11px; }
            QPushButton { background: #16213e; color: white; border: 1px solid #0f3460; border-radius: 4px; padding: 8px 15px; font-size: 12px; }
            QPushButton:hover { background: #00b4d8; border-color: #00b4d8; }
            QCheckBox { color: #e6e6e6; font-size: 12px; }
        """)

        central = QWidget()
        self.setCentralWidget(central)
        layout = QVBoxLayout(central)

        controls = QHBoxLayout()
        self.clear_btn = QPushButton("Очистить логи")
        self.clear_btn.clicked.connect(self.clear_logs)
        self.save_btn = QPushButton("Сохранить в файл")
        self.save_btn.clicked.connect(self.save_logs)
        self.auto_scroll = QCheckBox("Автоскролл")
        self.auto_scroll.setChecked(True)

        controls.addWidget(self.clear_btn)
        controls.addWidget(self.save_btn)
        controls.addStretch()
        controls.addWidget(self.auto_scroll)

        self.log_text = QTextEdit()
        self.log_text.setReadOnly(True)

        self.status_bar = QStatusBar()
        self.setStatusBar(self.status_bar)
        self.status_bar.showMessage("Логгер готов")

        layout.addLayout(controls)
        layout.addWidget(self.log_text)
        self.add_log_message("Логгер инициализирован", "SYSTEM")

    def add_log_message(self, msg, cat="INFO"):
        self.log_count += 1
        time = datetime.now().strftime("%H:%M:%S")

        colors = {
            "SYSTEM": "#00b4d8", "INFO": "#2ecc71", "WARNING": "#f39c12",
            "ERROR": "#e74c3c", "BUTTON": "#9b59b6", "CONFIG": "#3498db"
        }
        color = colors.get(cat, "#e6e6e6")

        entry = f'<span style="color: #95a5a6;">[{time}]</span> '
        entry += f'<span style="color: {color}; font-weight: bold;">[{cat}]</span> '
        entry += f'<span style="color: #e6e6e6;">{msg}</span><br>'

        self.log_text.append(entry)
        if self.auto_scroll.isChecked():
            self.log_text.verticalScrollBar().setValue(self.log_text.verticalScrollBar().maximum())

        self.status_bar.showMessage(f"Записей: {self.log_count}")
        if self.log_count > 1000:
            self.log_text.clear()
            self.log_count = 0
            self.status_bar.showMessage("Логи очищены")

    def clear_logs(self):
        self.log_text.clear()
        self.log_count = 0
        self.add_log_message("Логи очищены", "SYSTEM")

    def save_logs(self):
        time = datetime.now().strftime("%Y%m%d_%H%M%S")
        file = f"logs/log_{time}.txt"

        if not os.path.exists("logs"):
            os.makedirs("logs")

        try:
            with open(file, 'w', encoding='utf-8') as f:
                f.write(self.log_text.toPlainText())
            self.add_log_message(f"Логи сохранены в {file}", "SYSTEM")

            msg = QMessageBox()
            msg.setIcon(QMessageBox.Information)
            msg.setWindowTitle("Сохранение логов")
            msg.setText(f"Логи сохранены в:\n{file}")
            msg.setStyleSheet("QMessageBox { background: #1a1a2e; } QLabel { color: #e6e6e6; }")
            msg.exec_()
        except Exception as e:
            self.add_log_message(f"Ошибка сохранения: {str(e)}", "ERROR")