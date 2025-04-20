# game/ui.py

import sys
from PyQt6.QtWidgets import (
    QApplication, QWidget, QLabel, QLineEdit, QPushButton, QTextEdit,
    QVBoxLayout, QHBoxLayout, QMessageBox
)
from PyQt6.QtCore import Qt
from game.generator import generate_dialog

class GalgameUI(QWidget):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("AI Galgame 生成器")
        self.setGeometry(100, 100, 600, 600)
        self.settings = {}
        self.dialogs = []
        self.dialog_index = 0

        self.init_input_ui()

    def init_input_ui(self):
        self.clear_layout()

        layout = QVBoxLayout()

        title = QLabel("AI Galgame 生成器")
        title.setStyleSheet("font-size: 24px; font-weight: bold; color: #0078D7")
        title.setAlignment(Qt.AlignmentFlag.AlignCenter)

        self.duration_input = QLineEdit()
        self.duration_input.setPlaceholderText("游戏时长（分钟，例如60）")

        self.plot_input = QLineEdit()
        self.plot_input.setPlaceholderText("主要剧情主题")

        self.character1_input = QLineEdit()
        self.character1_input.setPlaceholderText("角色1（名字:描述）")

        self.character2_input = QLineEdit()
        self.character2_input.setPlaceholderText("角色2（名字:描述）")

        self.extra_input = QLineEdit()
        self.extra_input.setPlaceholderText("额外设定（可选）")

        self.start_button = QPushButton("生成游戏")
        self.start_button.setStyleSheet("background-color: #0078D7; color: white; padding: 10px; font-size: 16px;")
        self.start_button.clicked.connect(self.start_game)

        layout.addWidget(title)
        layout.addWidget(self.duration_input)
        layout.addWidget(self.plot_input)
        layout.addWidget(self.character1_input)
        layout.addWidget(self.character2_input)
        layout.addWidget(self.extra_input)
        layout.addWidget(self.start_button)

        self.setLayout(layout)

    def start_game(self):
        self.settings = {
            "duration": self.duration_input.text(),
            "plot": self.plot_input.text(),
            "characters": []
        }

        for text in [self.character1_input.text(), self.character2_input.text()]:
            if ":" in text:
                name, desc = text.split(":", 1)
                self.settings["characters"].append({"name": name.strip(), "desc": desc.strip()})
            elif text.strip():
                self.settings["characters"].append({"name": "角色", "desc": text.strip()})

        if self.extra_input.text().strip():
            self.settings["extra"] = self.extra_input.text().strip()

        self.dialogs = generate_dialog(self.settings)
        if not self.dialogs:
            QMessageBox.warning(self, "错误", "无法生成对话内容")
            return

        self.dialog_index = 0
        self.init_game_ui()

    def init_game_ui(self):
        self.clear_layout()

        layout = QVBoxLayout()

        self.dialog_display = QTextEdit()
        self.dialog_display.setReadOnly(True)
        self.dialog_display.setStyleSheet("font-size: 16px;")

        self.next_button = QPushButton("下一句")
        self.next_button.setStyleSheet("padding: 10px; font-size: 16px;")
        self.next_button.clicked.connect(self.next_dialog)

        self.back_button = QPushButton("返回")
        self.back_button.setStyleSheet("padding: 10px; font-size: 16px;")
        self.back_button.clicked.connect(self.init_input_ui)

        button_layout = QHBoxLayout()
        button_layout.addWidget(self.back_button)
        button_layout.addWidget(self.next_button)

        layout.addWidget(self.dialog_display)
        layout.addLayout(button_layout)

        self.setLayout(layout)
        self.show_dialog()

    def next_dialog(self):
        if self.dialog_index < len(self.dialogs) - 1:
            self.dialog_index += 1
            self.show_dialog()

    def show_dialog(self):
        if self.dialog_index < len(self.dialogs):
            self.dialog_display.setPlainText(self.dialogs[self.dialog_index])

    def clear_layout(self):
        """清除当前界面布局"""
        layout = self.layout()
        if layout is not None:
            while layout.count():
                item = layout.takeAt(0)
                widget = item.widget()
                if widget is not None:
                    widget.deleteLater()
            self.setLayout(None)

def run_game():
    app = QApplication(sys.argv)
    window = GalgameUI()
    window.show()
    sys.exit(app.exec())
