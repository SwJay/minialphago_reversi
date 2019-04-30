"""
obsolete logic
"""

import numpy as np

EMPTY = 0
LIGHT = -1
DARK = 1


class Reversi(object):

    def __init__(self):
        self._board = np.zeros((8, 8))
        self._dirs = [(1, 0), (1, 1), (0, 1), (-1, 1), (-1, 0), (-1, -1), (0, -1), (1, -1)]

    def place(self, direction, piece):
        x, y = direction
        self._board[x][y] = piece

    def get_piece(self, location):
        x, y = location
        return self._board[x][y]

    def get_next_location(self, location, direction):
        x = location[0] + direction[0]
        y = location[1] + direction[1]
        if x < 0 or x >= 8 or y < 0 or y >= 8:
            return False
        else:
            return x, y

    def get_next_piece(self, location, direction):
        if location is not False:
            next_piece = self.get_next_location(location, direction)
            if next_piece is not False:
                x, y = next_piece
                return self._board[x][y]
        return False

    def is_placeable(self, location, piece):
        x, y = location
        # check if empty
        if self._board[x][y] == EMPTY:
            bingo = []
            # check if placeable
            for direction in self._dirs:
                location_tmp = location
                count = 0
                while True:
                    next_piece = self.get_next_piece(location_tmp, direction)
                    if next_piece == - piece:
                        count += 1
                        location_tmp = self.get_next_location(location_tmp, direction)
                    elif next_piece == EMPTY:
                        count = 0
                        break
                    else:
                        break
                if count >= 1:
                    bingo.append((direction, count))
            if len(bingo) >= 1:
                return bingo
        return False

    def get_placeable(self, piece):
        placeable = []
        for x in range(8):
            for y in range(8):
                bingo = self.is_placeable((x, y), piece)
                if bingo is not False:
                    placeable.append(((x, y), bingo))
        return placeable

    def reverse(self, location, bingo):
        piece = self.get_piece(location)
        for item in bingo:
            direction, count = item
            location_tmp = location
            for i in range(count):
                location_tmp = self.get_next_location(location_tmp, direction)
                self.place(location_tmp, piece)