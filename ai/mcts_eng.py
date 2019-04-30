from copy import deepcopy
import os
import random
import numpy as np
import math
import sys


board_weight = [[100, -3, 11, 8, 8, 11, -3, 100],
                [-3, -7, -4, 1, 1, -4, -7, -3],
                [11, -4, 2, 2, 2, 2, -4, 11],
                [8, 1, 2, -3, -3, 2, 1, 8],
                [8, 1, 2, -3, -3, 2, 1, 8],
                [11, -4, 2, 2, 2, 2, -4, 11],
                [-3, -7, -4, 1, 1, -4, -7, -3],
                [100, -3, 11, 8, 5, 11, -3, 100]]


def weight_change(board, add_item, judge_item, add_weight, mulop):
    change_item = [(0, 1), (1, 0), (0, 6), (1, 7), (6, 0), (7, 1), (7, 6), (6, 7)]
    if judge_item[0] in add_item or judge_item[1] in add_item:
        for item in add_item:
            if item in judge_item:
                add_weight[item[0]][item[1]] = 2.1 * mulop * (7 - len(add_item))
            else:
                add_weight[item[0]][item[1]] = 1.2 * mulop * (7 - len(add_item))
    else:
        for item in add_item:
            if mulop == -0.9 and item in change_item:
                add_weight[item[0]][item[1]] = 0.6 * 3 * (7 - len(add_item))
            elif mulop == 2.1 and item in change_item:
                add_weight[item[0]][item[1]] = 0.6 * 3 * (7 - len(add_item))
            else:
                add_weight[item[0]][item[1]] = 0.6 * mulop * (7 - len(add_item))


def add_weight(board, line_cut, add_weight, color, flag):
    for piece in line_cut:
        if flag == 1:
            add_item = [(0, column) for column in piece]
            index = range(1, 7)
            judge_item = [(0, 0), (0, 7)]
        elif flag == 3:
            add_item = [(7, column) for column in piece]
            index = range(6, 0, -1)
            judge_item = [(7, 0), (7, 7)]
        elif flag == 2:
            add_item = [(row, 0) for row in piece]
            index = range(1, 7)
            judge_item = [(0, 0), (7, 0)]
        else:
            add_item = [(row, 7) for row in piece]
            index = range(6, 0, -1)
            judge_item = [(0, 7), (7, 7)]

        if flag % 2 == 1:
            for i in index:
                line_num = 0
                tmp = piece[0]
                while tmp != 0 and board[i][tmp] == 0 and board[i][tmp-1] == 0:
                    piece = [tmp-1] + piece
                    tmp -= 1
                tmp = piece[-1]
                while tmp != 7 and board[i][tmp] == 0 and board[i][tmp+1] == 0:
                    piece = piece + [tmp+1]
                    tmp += 1
                for j in piece:
                    if board[i][j] == 0:
                        line_num += 1
                        add_item.append((i, j))
                if line_num == 0:
                    break
        else:
            for i in index:
                line_num = 0
                tmp = piece[0]
                while tmp != 0 and board[tmp][i] == 0 and board[tmp-1][i] == 0:
                    piece = [tmp-1] + piece
                    tmp -= 1
                tmp = piece[-1]
                while tmp != 7 and board[tmp][i] == 0 and board[tmp+1][i] == 0:
                    piece = piece + [tmp+1]
                    tmp += 1
                for j in piece:
                    if board[j][i] == 0:
                        line_num += 1
                        add_item.append((j, i))
                if line_num == 0:
                    break

        if len(add_item) <= 6:
            base = 1
            if (0, 1) in add_item or (1, 0) in add_item:
                if board[0][0] == color:
                    base = 1.5
            if (0, 6) in add_item or (1, 7) in add_item:
                if board[0][7] == color:
                    base = 1.5
            if (6, 0) in add_item or (7, 1) in add_item:
                if board[7][0] == color:
                    base = 1.5
            if (7, 6) in add_item or (6, 7) in add_item:
                if board[7][7] == color:
                    base = 1.5
            if len(add_item) % 2 == 1:
                if base == 1.5:
                    base = 2.1
                weight_change(board, add_item, judge_item, add_weight, base)
            else:
                if base == 1.5:
                    base = 0.9
                weight_change(board, add_item, judge_item, add_weight, -base)


def weight(board, color):
    pieces = board.get_squares(color)
    op_pieces = board.get_squares(-1 * color)
    score = sum([board_weight[x][y] for x, y in pieces]) - \
            sum([board_weight[x][y] for x, y in op_pieces])
    return score

def unstability_difference(board, color):
    op_color = -1 * color
    my_unstable = op_unstable = 0
    if board[0][0] == 0:
        my_unstable += (board[0][1] == color) + (board[1][1] == color) + (board[1][0] == color)
        op_unstable += (board[0][1] == op_color) + (board[1][1] == op_color) + (board[1][0] == op_color)
    if board[0][7] == 0:
        my_unstable += (board[0][6] == color) + (board[1][6] == color) + (board[1][7] == color)
        op_unstable += (board[0][6] == op_color) + (board[1][6] == op_color) + (board[1][7] == op_color)
    if board[7][0] == 0:
        my_unstable += (board[7][1] == color) + (board[6][1] == color) + (board[6][0] == color)
        op_unstable += (board[7][1] == op_color) + (board[6][1] == op_color) + (board[6][0] == op_color)
    if board[7][7] == 0:
        my_unstable += (board[6][7] == color) + (board[6][6] == color) + (board[7][6] == color)
        op_unstable += (board[6][7] == op_color) + (board[6][6] == op_color) + (board[7][6] == op_color)
    return my_unstable - op_unstable

def pieces_difference(board, color):
    return len(board.get_squares(color)) - len(board.get_squares(-1 * color))

def op_move_count(board, color):
    return len(board.get_legal_moves(-1 * color))

def stability_difference(board, color):
    def line_stability_difference(line, my_color):
        op_color = -1 * my_color
        my_stable = op_stable = 0
        if line[0] == my_color:
            for piece in line:
                if piece == my_color:
                    my_stable += 1
                else:
                    break
            if my_stable == 8:
                return my_stable - op_stable
        if line[7] == my_color:
            for piece in line[::-1]:
                if piece == my_color:
                    my_stable += 1
                else:
                    break
        if line[0] == op_color:
            for piece in line:
                if piece == op_color:
                    op_stable += 1
                else:
                    break
            if op_stable == 8:
                return my_stable - op_stable
        if line[7] == op_color:
            for piece in line[::-1]:
                if piece == op_color:
                    op_stable += 1
                else:
                    break
        return my_stable - op_stable

    return line_stability_difference(board[0], color) + \
           line_stability_difference(board[7], color) + \
           line_stability_difference([b[0] for b in board], color) + \
           line_stability_difference([b[7] for b in board], color)


def evaluate(board, color):
    """ Return the evaluated value of current board. """
    if is_terminal(board, color):
        my_count = board.count(state.color)
        op_count = board.count(-1 * state.color)
        if my_count > op_count:
            return 100000 + my_count
        elif my_count < op_count:
            return -100000 - op_count
        else:
            return 0
    else:
        return 1 * weight(board, color) \
            - 10 * unstability_difference(board, color) \
            - 5 * op_move_count(board, color) \
            + 50 * stability_difference(board, color) \
            - 5 * pieces_difference(board, color)


def is_terminal(board, color):
        my_moves = board.get_legal_moves(color)
        op_moves = board.get_legal_moves(-1 * color)
        return len(my_moves) == 0 and len(op_moves) == 0


class TreeNode():

    def __init__(self, board, color, parent):
        self.board = board
        self.color = color
        self.is_terminal = is_terminal(board, color)
        self.is_fully_expanded  =   self.is_terminal
        self.parent             =   parent
        self.visit_num          =   0
        self.total_reward       =   0
        self.children           =   {}
        self.v                  =   evaluate(board, color)

    def is_terminal(board, color):
        my_moves = board.get_legal_moves(color)
        op_moves = board.get_legal_moves(-1 * color)
        return len(my_moves) == 0 and len(op_moves) == 0



class MCTSEngine():
    """ Game engine that implements MCTS Algo. """

    def __init__(self):
        self.iter_limit = 200
        self.exploration_constant = 1 / math.sqrt(1.5)

    def get_move(self,
                 board,
                 color,
                 move_num=None,
                 time_remaining=None,
                 time_opponent=None):
        """ Return a move for the given color using MCTS algo """
        new_board = deepcopy(board)
        return self.search(new_board, color)

    def search(self, board, color):
        self.root = TreeNode(board, color, None)
        self.color = color

        for i in range(self.iter_limit):
            node = self.treePolicy(self.root)
            reward = node.v

            self.backup(node, reward)

        best_child = self.bestChild(self.root)
        return self.getAction(self.root, best_child)

    # return leaf node
    def treePolicy(self, node):
        while not node.is_terminal:
            if node.is_fully_expanded:
                node = self.bestChild(node)
            else:
                return self.expand(node)
        return node

    def expand(self, node):
        possible_actions = node.board.get_legal_moves(node.color)
        best_value = float("-inf")
        times = 0

        # chose best unexpanded child 
        for action in possible_actions:
            # if action is in untried actions
            if action not in node.children.keys():
                times = times + 1
                new_board = deepcopy(node.board)
                new_board.execute_move(action, node.color)
                v = evaluate(new_board, node.color)
                if v > best_value:
                    best_value = v
                    best_child = TreeNode(new_board, -1 * node.color, node)
                    best_action = action
        
        node.children[best_action] = best_child
        if len(possible_actions) == len(node.children):
            node.is_fully_expanded = True
        return best_child    

    def backup(self, node, reward):
        while node is not None:
            node.visit_num += 1
            node.total_reward += reward
            node = node.parent

    def bestChild(self, node):
        best_value = float("-inf")
        best_nodes = []
        
        for action in node.children.keys():
            child = node.children[action]
            value = child.total_reward / child.visit_num + child.v * math.sqrt(node.visit_num) / (1 + child.visit_num)
            value = node.color * value
            if value > best_value:
                best_value = value
                best_nodes = [child]
            elif value >= best_value * 0.85:
                best_nodes.append(child)
        return random.choice(best_nodes)

    def getAction(self, root, best_child):
        for action, node in root.children.items():
            if node is best_child:
                return action


engine = MCTSEngine