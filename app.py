import sys

from PyQt5.QtWidgets import QApplication
from gui.board import Board


if __name__ == '__main__':
    app = QApplication(sys.argv)
    window = Board()
    sys.exit(app.exec_())
