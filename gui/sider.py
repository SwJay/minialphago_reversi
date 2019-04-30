from PyQt5.QtWidgets import (QPushButton, QVBoxLayout, QDialog, QLabel)

START = 0
END = 1

HUMAN = 1
AI = -1


class Sider(QVBoxLayout):
    def __init__(self):
        QVBoxLayout.__init__(self)

        self.start_button = QPushButton("start")
        self.start_button.clicked.connect(self.start)

        self.addStretch(1)
        self.addWidget(self.start_button)
        self.addStretch(1)

    def start(self):
        self.removeWidget(self.start_button)


class Dialog(QDialog):
    def __init__(self, dia_type):
        QDialog.__init__(self)

        self.player = 0
        self.winner = 0
        self.black = 0
        self.white = 0

        if dia_type == START:
            self.start()
        elif dia_type == END:
            self.end()

    def start(self):
        self.resize(240, 200)
        self.setWindowTitle("start")

        btn1 = QPushButton("Play First")
        btn2 = QPushButton("AI First")

        btn1.clicked.connect(self.human_first)
        btn2.clicked.connect(self.ai_first)

        layout = QVBoxLayout()
        layout.addWidget(btn1)
        layout.addWidget(btn2)

        self.setLayout(layout)

    def human_first(self):
        self.player = HUMAN
        self.close()

    def ai_first(self):
        self.player = AI
        self.close()

    def get_player(self):
        return self.player
