import sys
from PyQt5.QtWidgets import *
from PyQt5.QtCore import *
from PyQt5.QtGui import *

from config_manager import ConfigManager
from settings_window import SettingsWindow
from logger_window import LoggerWindow
from monitoring_window import MonitoringWindow


class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        self.config_manager = ConfigManager()
        self.logger_window = None
        self.init_ui()
        self.config_manager.log_message_signal.connect(self.handle_log_message)

    def init_ui(self):
        self.setWindowTitle("Система мониторинга и управления")
        self.setGeometry(100, 100, 1000, 650)

        self.setStyleSheet("""
            QMainWindow { background-color: #1a1a2e; }
            QTabWidget::pane { background: #16213e; border: 1px solid #0f3460; border-radius: 5px; }
            QTabBar::tab { background: #0f3460; color: #e6e6e6; padding: 12px 20px; margin-right: 2px; font-size: 13px; font-weight: 500; min-width: 140px; }
            QTabBar::tab:selected { background: #00b4d8; color: white; }
            QTabBar::tab:hover:!selected { background: #16213e; }
        """)

        self.tab_widget = QTabWidget()
        self.setCentralWidget(self.tab_widget)
        self.tab_widget.setElideMode(Qt.ElideRight)

        self.monitoring_window = MonitoringWindow(self.config_manager)
        self.settings_window = SettingsWindow(self.config_manager)

        self.tab_widget.addTab(self.monitoring_window, "Мониторинг")
        self.tab_widget.addTab(self.settings_window, "Настройки")

        self.create_toolbar()

        self.status_bar = QStatusBar()
        self.setStatusBar(self.status_bar)
        self.status_bar.showMessage("Система готова к работе")

        self.config_manager.log_message_signal.emit("Приложение запущено", "SYSTEM")

    def create_toolbar(self):
        toolbar = QToolBar("Основные инструменты")
        toolbar.setMovable(False)
        toolbar.setStyleSheet("""
            QToolBar { background: #16213e; border: none; padding: 8px; spacing: 15px; }
            QToolButton { color: #e6e6e6; padding: 10px 15px; font-size: 13px; min-width: 120px; border-radius: 4px; }
            QToolButton:hover { background: #00b4d8; }
        """)
        self.addToolBar(toolbar)

        log_action = QAction("📋 Логи", self)
        log_action.triggered.connect(self.open_logger_window)
        toolbar.addAction(log_action)
        toolbar.addSeparator()



    def open_logger_window(self):
        if not self.logger_window:
            self.logger_window = LoggerWindow(self.config_manager)
        self.logger_window.show()
        self.logger_window.raise_()
        self.logger_window.activateWindow()
        self.config_manager.log_message_signal.emit("Окно логов открыто", "SYSTEM")

    def handle_log_message(self, message, category):
        if category in ["ERROR", "WARNING"]:
            self.status_bar.showMessage(f"{message} - {category}", 3000)
        elif category == "SYSTEM":
            self.status_bar.showMessage(message, 2000)


if __name__ == "__main__":
    app = QApplication(sys.argv)
    app.setStyle("Fusion")

    dark_palette = QPalette()
    dark_palette.setColor(QPalette.Window, QColor(26, 26, 46))
    dark_palette.setColor(QPalette.WindowText, QColor(230, 230, 230))
    dark_palette.setColor(QPalette.Base, QColor(22, 33, 62))
    dark_palette.setColor(QPalette.AlternateBase, QColor(15, 52, 96))
    dark_palette.setColor(QPalette.ToolTipBase, QColor(0, 180, 216))
    dark_palette.setColor(QPalette.ToolTipText, QColor(230, 230, 230))
    dark_palette.setColor(QPalette.Text, QColor(230, 230, 230))
    dark_palette.setColor(QPalette.Button, QColor(15, 52, 96))
    dark_palette.setColor(QPalette.ButtonText, QColor(230, 230, 230))
    dark_palette.setColor(QPalette.BrightText, QColor(255, 255, 255))
    dark_palette.setColor(QPalette.Link, QColor(0, 180, 216))
    dark_palette.setColor(QPalette.Highlight, QColor(0, 180, 216))
    dark_palette.setColor(QPalette.HighlightedText, QColor(0, 0, 0))

    app.setPalette(dark_palette)
    window = MainWindow()
    window.show()
    sys.exit(app.exec_())