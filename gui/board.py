from PyQt5.QtWidgets import (QMainWindow, QWidget, QHBoxLayout, QGridLayout, QLabel)
from PyQt5.QtGui import (QPainter, QPalette, QColor, QPixmap)
from gui.sider import (Sider, Dialog)
from game.board import Reversi
from ai.minimax_eng2 import MinimaxEngine
import time

BASEX = 65
BASEY = 65
DISC = 80

START = 0
END = 1

# LIGHT = HUMAN, DARK = AI
LIGHT = 1
DARK = -1

EMPTY = 0
SET = 1
ALTER = 2
MOUSE = 3
AI = 4

BLACK = -1
WHITE = 1
TIE = 0

trans_d = lambda x: BASEX + DISC * x
trans_c = lambda x: 1.15 * BASEX + DISC * x


class Board(QMainWindow):

    def __init__(self):
        QMainWindow.__init__(self)

        # init subparts
        self.chessBoard = ChessBoard()
        self.sider = Sider()

        # init dialog
        start_dialog = Dialog(START)

        # layout
        board = QWidget(self)

        layout = QHBoxLayout()
        layout.addWidget(self.chessBoard)
        layout.addLayout(self.sider)
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
        self.chessBoard.player = start_dialog.get_player()
        start_dialog.destroy()

        self.round()

    def round(self):
        self.chessBoard.update()


class ChessBoard(QWidget):

    def __init__(self):
        QWidget.__init__(self)

        self.game = Reversi()
        self.player = EMPTY
        self.ai = MinimaxEngine()
        self.location = -1, -1
        self.shot = 0
        self.end = 0

        # set background color
        bg = QPalette()
        bg.setColor(self.backgroundRole(), QColor(0, 60, 0))
        self.setPalette(bg)
        self.setAutoFillBackground(True)

        # set discs
        self.pieces = [[QLabel(self) for i in range(8)] for j in range(8)]
        for i in range(8):
            for j in range(8):
                piece = self.pieces[i][j]
                piece.setVisible(True)
                piece.setScaledContents(True)
                piece.setGeometry(trans_c(i), trans_c(j), 0.8 * DISC, 0.8 * DISC)

        # set piece
        self.black = QPixmap('img/black.png')
        self.white = QPixmap('img/white.png')
        self.black_h = QPixmap('img/black_half.png')
        self.white_h = QPixmap('img/white_half.png')

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
                # disc
                qp.setBrush(QColor(0, 100 if (i + j) % 2 else 120, 0))
                qp.drawRect(trans_d(i), trans_d(j), DISC, DISC)
                # piece
                if self.game.pieces[i][j] is not EMPTY:
                    self.draw_piece((i, j), SET)
                else:
                    self.draw_piece((i, j), EMPTY)

        # draw alternatives
        if self.player is LIGHT:
            placeables = self.game.get_legal_moves(self.player)
            if len(placeables) >= 1:
                for location in placeables:
                    self.draw_piece(location, ALTER)
        else:
            if self.shot is 1:
                self.draw_piece(self.location, AI)
                self.shot = 0

    def draw_piece(self, location, flag):
        x, y = location
        if flag is EMPTY:
            piece_img = QPixmap("")
        elif flag is SET:
            piece_img = self.black if self.game.pieces[x][y] == DARK else self.white
        elif flag is ALTER:
            piece_img = self.black_h if self.player == DARK else self.white_h
        elif flag is AI:
            piece_img = self.black

        self.pieces[x][y].setPixmap(piece_img)

    def mousePressEvent(self, event):
        if self.player is LIGHT:
            x = event.x()
            y = event.y()
            placeables = self.game.get_legal_moves(self.player)
            if len(placeables) >= 1:
                self.end = 0
                for location in placeables:
                    disc_x, disc_y = location
                    if trans_d(disc_x) < x < trans_d(disc_x) + DISC \
                    and trans_d(disc_y) < y < trans_d(disc_y) + DISC:
                        self.game.execute_move(location, self.player)
                        self.player = - self.player
                        self.repaint()
                        self.ai_play()

                # check AI's legal move
                if len(self.game.get_legal_moves(self.player)) == 0:
                    self.end += 1
                    if self.end is 1:
                        self.player = - self.player
                        print("AI has no legal move, it's your turn again")
                    elif self.player is 2:
                        print("GG")
                        self.endgame()

    def ai_play(self):
        if len(self.game.get_legal_moves(self.player)) >= 1:
            self.end = 0
            # move = self.ai.get_move(self.game, self.player)
            move = self.game.get_legal_moves(self.player)[0]
            self.location = move
            self.shot = 1
            self.repaint()
            # time.sleep(0.5)
            self.game.execute_move(move, self.player)
            self.player = - self.player
            self.repaint()

            # check human legal move
            if len(self.game.get_legal_moves(self.player)) == 0:
                self.end += 1
                if self.end is 1:
                    self.player = - self.player
                    print("You have no legal move, it's AI's turn")
                    self.ai_play()
                elif self.player is 2:
                    print("GG")
                    self.endgame()

    def endgame(self):
        winner, black, white = self.winner()
        label = QLabel()
        label.setFixedWidth(400)
        label.setFixedHeight(400)
        self.resize(240, 200)
        self.setWindowTitle("GAME OVER")

        if winner is BLACK:
            msg = "AI wins! Black count: " + str(black) + ", white count: " + str(white)
        elif winner is WHITE:
            msg = "You win! Black count: " + str(black) + ", white count: " + str(white)
        else:
            msg = "Tie end! Both count: " + str(black)

        label.setText(msg)

    def winner(self):
        black_count = self.game.pieces.count(-1)
        white_count = self.game.pieces.count(1)
        if black_count > white_count:
            return -1, black_count, white_count
        elif white_count > black_count:
            return 1, black_count, white_count
        else:
            return 0, black_count, white_count
