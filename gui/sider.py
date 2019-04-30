from PyQt5.QtWidgets import (QWidget, QPushButton, QVBoxLayout, QDialog, QLabel, QLCDNumber)
from PyQt5.QtCore import QTimer

START = 0
END = 1

HUMAN = 1
AI = -1

BLACK = -1
WHITE = 1
TIE = 0


class Sider(QWidget):

    def __init__(self):
        QWidget.__init__(self)

        self.timer = QTimer(self)
        self.timer.start(1000)
        self.timer.timeout.connect(self.ontime)

        # lcd
        self.time = 0
        self.lcd = QLCDNumber()
        # billborad
        self.log = QLabel(self)
        self.msg = ""
        self.count = 0

        layout = QVBoxLayout()
        layout.addWidget(self.lcd)
        layout.addWidget(self.log)
        layout.setStretch(0, 1)
        layout.setStretch(1, 3)
        self.setLayout(layout)
        self.show()

    def ontime(self):
        if self.time > 0:
            self.time -= 1
            self.lcd.display(self.time)

    def time_refresh(self):
        self.time = 60

    def log_refresh(self, x, y, time):
        self.count += 1
        self.msg += "Ai no." + str(self.count) + "| location: (" + str(x) + ", " + str(y) \
                    + "), time used: " + str(time) + " secs.\n"
        self.log.setText(self.msg)


class Dialog(QDialog):
    def __init__(self, dia_type):
        QDialog.__init__(self)

        self.player = 0
        self.winner = 0
        self.black = 0
        self.white = 0

        if dia_type == START:
            self.start()

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

    def end(self):
        self.resize(240, 200)
        self.setWindowTitle("GAME OVER")
        label = QLabel(self)

        if self.winner is BLACK:
            msg = "AI wins! Black count: " + str(self.black) + ", white count: " + str(self.white)
        elif self.winner is WHITE:
            msg = "You win! Black count: " + str(self.black) + ", white count: " + str(self.white)
        elif self.winner is TIE:
            msg = "Tie end! Both count: " + str(self.black)

        label.setText(msg)

        layout = QVBoxLayout()
        layout.addWidget(label)
        self.setLayout(layout)

    def human_first(self):
        self.player = HUMAN
        self.close()

    def ai_first(self):
        self.player = AI
        self.close()

    def get_player(self):
        return self.player

    def set_winner(self, result):
        self.winner, self.black, self.white = result
        self.end()
