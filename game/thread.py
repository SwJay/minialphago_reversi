from PyQt5.QtCore import (QThread, pyqtSignal)


class Worker(QThread):
    signal = pyqtSignal()

    def __init__(self, parent=None):
        QThread.__init__(self, parent)

    def run(self):
        pass
