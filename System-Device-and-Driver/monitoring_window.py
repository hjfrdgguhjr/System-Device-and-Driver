from PyQt5.QtWidgets import *
from PyQt5.QtCore import *


class MonitoringWindow(QWidget):

    def __init__(self, config_manager):
        super().__init__()
        self.config_manager = config_manager
        self.init_ui()

    def init_ui(self):
        self.setStyleSheet("""
            QWidget {
                background-color: #1a1a2e;
            }
            QLabel {
                color: #e6e6e6;
                font-size: 14px;
            }
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

        title = QLabel("Мониторинг системы")
        title.setStyleSheet("""
            QLabel {
                font-size: 20px;
                font-weight: bold;
                color: #00b4d8;
            }
        """)
        title.setAlignment(Qt.AlignCenter)

        header_layout.addStretch()
        header_layout.addWidget(title)
        header_layout.addStretch()

        layout.addWidget(header_container)

        data_container = QWidget()
        data_container.setStyleSheet("""
            QWidget {
                background: #16213e;
                border-radius: 8px;
                padding: 25px;
            }
        """)
        data_layout = QGridLayout()
        data_layout.setSpacing(20)

        metrics = [
            ("Сpu:", "70%", "#2ecc71"),
            ("", "", "#3498db"),
            ("Gpu:", "68%", "#9b59b6"),
            ("", "", "#e74c3c"),
            ("Ram", "39%", "#f39c12"),
            ("", "", "#2ecc71"),
            ("", "", "#3498db"),
            ("", "", "#f39c12")
        ]

        for i, (label, value, color) in enumerate(metrics):
            lbl = QLabel(label)
            lbl.setStyleSheet("font-weight: bold; font-size: 13px;")

            val = QLabel(value)
            val.setStyleSheet(f"color: {color}; font-weight: bold; font-size: 13px;")

            row = i // 2
            col = (i % 2) * 2
            data_layout.addWidget(lbl, row, col)
            data_layout.addWidget(val, row, col + 1)

        data_container.setLayout(data_layout)
        layout.addWidget(data_container)

        layout.addStretch()

        self.setLayout(layout)