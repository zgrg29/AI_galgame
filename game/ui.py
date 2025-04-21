import sys
from PyQt6.QtWidgets import (
    QApplication, QWidget, QLabel, QLineEdit, QPushButton, QTextEdit,
    QVBoxLayout, QHBoxLayout, QMessageBox
)
from PyQt6.QtCore import Qt
from game.generator import generate_next_dialog

class GalgameUI(QWidget):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("AI Galgame 生成器")
        self.setGeometry(100, 100, 600, 600)
        self.settings = {}
        self.dialogs = []  # 存储对话内容
        self.dialog_index = 0  # 当前显示的对话索引
        self.previous_dialog = ""  # 上一轮对话内容

        self.main_layout = QVBoxLayout()
        self.page_widget = QWidget()
        self.page_layout = QVBoxLayout()
        self.page_widget.setLayout(self.page_layout)

        self.main_layout.addWidget(self.page_widget)
        self.setLayout(self.main_layout)

        self.init_input_ui()

    def init_input_ui(self):
        self.clear_layout()

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

        self.page_layout.addWidget(title)
        self.page_layout.addWidget(self.duration_input)
        self.page_layout.addWidget(self.plot_input)
        self.page_layout.addWidget(self.character1_input)
        self.page_layout.addWidget(self.character2_input)
        self.page_layout.addWidget(self.extra_input)
        self.page_layout.addWidget(self.start_button)

    def start_game(self):
        self.settings = {
            "duration": int(self.duration_input.text()),
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

        self.dialogs = generate_next_dialog(self.settings, self.previous_dialog)
        if not self.dialogs:
            QMessageBox.warning(self, "错误", "无法生成对话内容")
            return

        self.dialog_index = 0
        self.previous_dialog = "\n".join(self.dialogs)
        self.init_game_ui()

    def init_game_ui(self):
        self.clear_layout()

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

        self.page_layout.addWidget(self.dialog_display)
        self.page_layout.addLayout(button_layout)

        self.show_dialog()

    def next_dialog(self):
        # 如果当前对话已经显示完，生成新的对话
        if self.dialog_index >= len(self.dialogs) - 1:
            # 生成下一部分的对话
            new_dialogs = generate_next_dialog(self.settings, self.previous_dialog)
            
            # 如果生成了新的对话，将它们添加到现有的对话列表中
            if new_dialogs:
                self.dialogs.extend(new_dialogs)  # 将新对话添加到现有对话列表
                self.previous_dialog = "\n".join(self.dialogs)  # 更新已显示的对话
                self.dialog_index = len(self.dialogs) - len(new_dialogs)  # 将对话索引指向新添加的部分

        # 移动到下一个对话
        self.dialog_index += 1
        self.show_dialog()


    def show_dialog(self):
        if self.dialog_index < len(self.dialogs):
            self.dialog_display.setPlainText(self.dialogs[self.dialog_index])

    def clear_layout(self):
        while self.page_layout.count():
            item = self.page_layout.takeAt(0)
            widget = item.widget()
            if widget is not None:
                widget.deleteLater()
            elif item.layout():
                self.clear_sub_layout(item.layout())

    def clear_sub_layout(self, layout):
        while layout.count():
            sub_item = layout.takeAt(0)
            widget = sub_item.widget()
            if widget is not None:
                widget.deleteLater()
            elif sub_item.layout():
                self.clear_sub_layout(sub_item.layout())
        layout.deleteLater()


def run_game():
    app = QApplication(sys.argv)
    window = GalgameUI()
    window.show()
    sys.exit(app.exec())
