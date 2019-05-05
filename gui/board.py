from PyQt5.QtWidgets import (QMainWindow, QWidget, QHBoxLayout, QLabel, QMessageBox)
from PyQt5.QtGui import (QPainter, QPalette, QColor, QPixmap)
from PyQt5.QtCore import pyqtSignal
from gui.sider import (Sider, Dialog)
from game.reversi import Reversi
from ai.minimax_eng2 import MinimaxEngine
import time

BASEX = 65
BASEY = 65
DISC = 80

START = 0
END = 1

HUMAN = 1
AI = -1

LIGHT = 1
DARK = -1

EMPTY = 0
SET = 1
ALTER = 2
SHOT = 3

trans_d = lambda x: BASEX + DISC * x
trans_c = lambda x: 1.15 * BASEX + DISC * x


class Board(QMainWindow):

    def __init__(self):
        QMainWindow.__init__(self)

        self.totoal_time = 0
        self.statusBar().showMessage("total time for ai: " + str(self.totoal_time))

        # init subparts
        self.chessBoard = ChessBoard()
        self.sider = Sider()

        # init dialog
        start_dialog = Dialog(START)

        # layout
        board = QWidget(self)

        layout = QHBoxLayout()
        layout.addWidget(self.chessBoard)
        layout.addWidget(self.sider)
        # set horizontal proportion 4:1
        layout.setStretch(0, 2)
        layout.setStretch(1, 1)

        board.setLayout(layout)
        self.setCentralWidget(board)
        self.setGeometry(250, 100, 1200, 800)
        self.setWindowTitle("Reversi")
        self.show()

        # open start dialog
        start_dialog.exec()
        # first hand take the light piece
        self.chessBoard.player = start_dialog.get_player()
        start_dialog.destroy()

        self.start()

        self.chessBoard.time_sig.connect(self.sider.time_refresh)
        self.chessBoard.ai_sig.connect(self.update_status)
        self.chessBoard.box_sig.connect(self.box)

    def start(self):
        self.sider.time_refresh()
        if self.chessBoard.player is HUMAN:
            self.chessBoard.update()
        else:
            self.chessBoard.ai_play()

    def update_status(self, x, y, second):
        self.sider.log_refresh(x, y, second)
        self.totoal_time += second
        m, s = divmod(self.totoal_time, 60)
        self.statusBar().showMessage("total time for ai: %02d min %02d sec" % (m, s))

    def box(self, flag):
        msg = "AI has no legal move, it's your turn again" if flag else "You have no legal move, it's AI's turn again"
        reply = QMessageBox.information(self, "No legal move", msg, QMessageBox.Yes)


class ChessBoard(QWidget):
    # signal
    time_sig = pyqtSignal()
    ai_sig = pyqtSignal(int, int, int)  # x, y, time
    box_sig = pyqtSignal(bool)

    def __init__(self):
        QWidget.__init__(self)

        self.game = Reversi()
        self.player = EMPTY
        self.color = LIGHT
        self.ai = MinimaxEngine()
        self.location = -1, -1
        # identify ai step
        self.shot = 0

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
        if self.player is HUMAN:
            placeables = self.game.get_legal_moves(self.color)
            if len(placeables) >= 1:
                for location in placeables:
                    self.draw_piece(location, ALTER)
        else:
            if self.shot is 1:
                self.draw_piece(self.location, SHOT)
                self.shot = 0

    def draw_piece(self, location, flag):
        x, y = location
        if flag is EMPTY:
            piece_img = QPixmap("")
        elif flag is SET:
            piece_img = self.black if self.game.pieces[x][y] == DARK else self.white
        elif flag is ALTER:
            piece_img = self.black_h if self.color == DARK else self.white_h
        elif flag is SHOT:
            piece_img = self.black if self.color == DARK else self.white

        self.pieces[x][y].setPixmap(piece_img)

    def mousePressEvent(self, event):
        if self.player is HUMAN:
            x = event.x()
            y = event.y()
            placeables = self.game.get_legal_moves(self.color)
            if len(placeables) >= 1:
                for location in placeables:
                    disc_x, disc_y = location
                    if trans_d(disc_x) < x < trans_d(disc_x) + DISC \
                            and trans_d(disc_y) < y < trans_d(disc_y) + DISC:
                        self.game.execute_move(location, self.color)
                        self.player = - self.player
                        self.color = - self.color
                        self.repaint()
                        self.ai_play()

                # check AI's legal move
                if len(self.game.get_legal_moves(self.color)) == 0:
                    self.player = - self.player
                    self.color = - self.color
                    if len(self.game.get_legal_moves(self.color)) == 0:
                        self.endgame()
                    else:
                        print("AI has no legal move, it's your turn again")
                        self.box_sig.emit(True)
                        self.time_sig.emit()
                else:
                    # ldc for ai
                    self.time_sig.emit()

    def ai_play(self):
        if len(self.game.get_legal_moves(self.color)) >= 1:
            start = time.time()
            move = self.ai.get_move(self.game, self.color)
            # move = self.game.get_legal_moves(self.player)[0]
            end = time.time()
            ai_time = end - start
            self.ai_sig.emit(move[0], move[1], ai_time)

            self.location = move
            self.shot = 1
            self.repaint()
            time.sleep(0.5)
            self.game.execute_move(move, self.color)
            self.player = - self.player
            self.color = - self.color
            self.repaint()

            # check human legal move
            if len(self.game.get_legal_moves(self.color)) == 0:
                self.player = - self.player
                if len(self.game.get_legal_moves(self.color)) == 0:
                    self.endgame()
                else:
                    print("You no legal move, it's AI's turn again")
                    self.ai_play()
                    self.box_sig.emit(False)
                    self.time_sig.emit()
            else:
                # ldc for human
                self.time_sig.emit()

    def endgame(self):
        dia = Dialog(END)
        dia.set_winner(self.winner())
        dia.exec()

    def winner(self):
        black_count = self.game.count(-1)
        white_count = self.game.count(1)
        if black_count > white_count:
            return -1, black_count, white_count
        elif white_count > black_count:
            return 1, black_count, white_count
        else:
            return 0, black_count, white_count
