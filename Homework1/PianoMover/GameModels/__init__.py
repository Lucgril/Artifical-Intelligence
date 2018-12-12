import numpy as np
from collections import defaultdict
import copy

BOARDWIDTH = 10  # number of columns in the board
BOARDHEIGHT = 10  # number of rows in the board


class PianoMoverRepresentation:

    def __init__(self, board, obj):
        self.board = board
        self.piano = np.where(self.board == 1)
        self.obj = obj


class PianoMoverState:

    def __init__(self, parent, cost, level, board, obj):
        self.parent = parent
        self.cost = cost
        self.level = level
        self.representation = PianoMoverRepresentation(board, obj)

    def __eq__(self, state):
        if not isinstance(state, PianoMoverState):
            return False

        return np.array_equal(self.representation.board, state.representation.board) and \
                np.array_equal(self.representation.piano, state.representation.piano) and\
                self.representation.obj == state.representation.obj

    def __hash__(self):

        return hash((str(self.representation.board), str(self.representation.piano),\
                     self.representation.obj))


class Game:

    def __init__(self, initialState = None):
        self.state = initialState

    def neighbors(self, state):
        out = set([])
        return out

    def getState(self):
        return self.state

    def solution(self, state):
        return True


class PianoMoverGame(Game):

    def __init__(self, board, obj):
        self.state = PianoMoverState(None, 0, 0, board, obj)

    def solution(self, state):
        out = (state.representation.board[0][BOARDHEIGHT - 2] == 1) and (state.representation.board[0][BOARDHEIGHT - 1] == 1) and \
              (state.representation.board[1][BOARDHEIGHT - 2] == 1) and (state.representation.board[1][BOARDHEIGHT - 1] == 1)
        return out

    def neighbors(self, state):
        out = set([])
        rep = state.representation
        moves = defaultdict(list)

        for i in range(1, 2 + rep.obj):

            obj = np.where(rep.board == i)
            
            if len(obj[0]) == 0:
                break

            #left
            if all(j > 0 for j in obj[1]):
                free = False
                
                for j in range(0, len(obj[0])):
                    if (rep.board[obj[0][j]][obj[1][j] - 1] in [0, i]) and\
                    (rep.board[obj[0][j]][obj[1][j] - 1] in [0, i]):
                        free = True
                    else:
                        free = False
                        break

                if free:
                        moves[i].append((0, -1))

            #up
            if all(j > 0 for j in obj[0]):
                free = False
                for j in range(0, len(obj[0])):
                    if (rep.board[obj[0][j] - 1][obj[1][j]] in [0, i]) and \
                    (rep.board[obj[0][j] - 1][obj[1][j]] in [0, i]):
                       free = True
                    else:
                        free = False
                        break
                if free:
                    moves[i].append((-1, 0))

            #right
            if all(j < 9 for j in obj[1]):
                free = False
                for j in range(0, len(obj[0])):
                    if (rep.board[obj[0][j]][obj[1][j] + 1] in [0, i]) and \
                       (rep.board[obj[0][j]][obj[1][j] + 1] in [0, i]):
                        free = True
                    else:
                        free = False
                        break
                if free:
                    moves[i].append((0, +1))

            #down
            if all(j < 9 for j in obj[0]):
                free = False
                for j in range(0, len(obj[0])):
                    if (rep.board[obj[0][j] + 1][obj[1][j]] in [0, i]) and \
                       (rep.board[obj[0][j] + 1][obj[1][j]] in [0, i]):
                        free = True
                    else:
                        free = False
                        break
                if free:
                    moves[i].append((+1, 0))

        for i in range(1, 2 + rep.obj):
            obj = np.where(rep.board == i)

            if len(obj[0]) == 0:
                break

            for move in moves[i]:
                temp = copy.deepcopy(rep.board)

                for j in range(len(obj[0])):
                    temp[obj[0][j]][obj[1][j]] = 0

                for j in range(len(obj[0])):
                    temp[obj[0][j] + move[0]][obj[1][j] + move[1]] = i

                n = PianoMoverState(state, len(obj[0]), state.level + 1, temp, rep.obj)
                out.add(n)
        return out


