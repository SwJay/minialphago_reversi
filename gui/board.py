from PyQt5.QtWidgets import (QMainWindow, QWidget, QHBoxLayout, QGridLayout, QLabel)
from PyQt5.QtGui import (QPainter, QPalette, QColor, QPixmap)
from gui.menu import (Menu, Dialog)
from game.logic import Reversi

BASEX = 65
BASEY = 65
DISC = 80
START = 0
END = 1
# LIGHT = HUMAN, DARK = AI
LIGHT = -1
DARK = 1
EMPTY = 0
ALTER = 0.2
MOUSE = 0.4


class Board(QMainWindow):

    def __init__(self):
        QMainWindow.__init__(self)

        # init subparts
        self.chessBoard = ChessBoard()
        self.menu = Menu()
        self.game = Reversi()

        # init dialog
        start_dialog = Dialog(START)

        # layout
        board = QWidget(self)

        layout = QHBoxLayout()
        layout.addWidget(self.chessBoard)
        layout.addLayout(self.menu)
        # set horizontal proportion 4:1
        layout.setStretch(0, 4)
        layout.setStretch(1, 1)

        board.setLayout(layout)
        self.setCentralWidget(board)
        self.setGeometry(450, 100, 1000, 800)
        self.setWindowTitle("Reversi")
        self.show()

        # open start dialog
        start_dialog.exec()
        self.player = start_dialog.get_player()
        start_dialog.destroy()

        self.init_game()

    def init_game(self):
        self.place((3, 3))
        self.place((3, 4))
        self.place((4, 4))
        self.place((4, 3))
        self.round()

    def place(self, location):
        self.game.place(location, self.player)
        self.chessBoard.draw_piece(location, self.player)
        self.player = - self.player

    # def replace(self, location):

    def round(self):
        placeables = self.game.get_placeable(self.player)
        if len(placeables) >= 1:
            for placeable in placeables:
                self.chessBoard.set_alternative(placeable, self.player)
        # else:
            # back to enemy


class ChessBoard(QWidget):

    def __init__(self):
        QWidget.__init__(self)

        # set background color
        bg = QPalette()
        bg.setColor(self.backgroundRole(), QColor(0, 60, 0))
        self.setPalette(bg)
        self.setAutoFillBackground(True)

        # set layout
        grid = QGridLayout()
        self.setLayout(grid)

        # set discs
        self.pieces = [[Chess((i,j)) for i in range(8)] for j in range(8)]
        for i in range(8):
            for j in range(8):
                piece = self.pieces[i][j]
                piece.setVisible(True)
                piece.setScaledContents(True)
                # piece.setGeometry(1.15 * BASEX + DISC * i, 1.15 * BASEY + DISC * j, 0.8 * DISC, 0.8 * DISC)
                grid.addWidget(piece, *(i, j))

        # set piece
        self.black = QPixmap('img/black.png')
        self.white = QPixmap('img/white.png')

    def paintEvent(self, event):
        qp = QPainter()
        qp.begin(self)
        self.draw_board(qp)
        qp.end()

    def draw_board(self, qp):
        col = QColor(255, 255, 255)
        qp.setPen(col)
        
        # draw discs
        for i in range(0, 8):
            for j in range(0, 8):
                qp.setBrush(QColor(0, 100 if (i + j) % 2 else 120, 0))
                qp.drawRect(BASEX + i * DISC, BASEY + j * DISC, DISC, DISC)

    def draw_piece(self, location, piece):
        x, y = location
        piece_img = self.black if piece == DARK else self.white
        label = self.pieces[x][y]
        label.set_piece(piece_img, EMPTY)
        # label.setPixmap(piece_img)
        # label.setGeometry(1.15 * BASEX + DISC * x, 1.15 * BASEY + DISC * y, 0.8 * DISC, 0.8 * DISC)

    def set_alternative(self, plaecable, piece):
        location, bingo = plaecable
        self.draw_piece(location, piece)


class Chess(QLabel):

    def __init__(self, location):
        QLabel.__init__(self)

        x, y = location
        self.style = EMPTY
        self.setGeometry(1.15 * BASEX + DISC * x, 1.15 * BASEY + DISC * y, 0.8 * DISC, 0.8 * DISC)

    def set_piece(self, piece_img, style):
        self.setPixmap(piece_img)
