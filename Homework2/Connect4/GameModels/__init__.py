import numpy as np
from copy import deepcopy

BOARDHEIGHT = 6
BOARDWIDTH = 7


class Connect4State:

    def __init__(self, board):
        self.board = board

    def __eq__(self, state):
        if not isinstance(state, Connect4State):
            return False

        return np.array_equal(self.board, state.board)

    def __hash__(self):

        return hash((str(self.board)))


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


class Connect4Game(Game):

    def __init__(self, board):
        self.state = Connect4State(board)

    def makeMove(self, s):
        repos = deepcopy(s.board)
        self.state = Connect4State(repos)

    def solution(self, state, turn):

        repos = deepcopy(state.board)

        # Check if the board is full
        if len(np.where(repos == ' ')[0]) == 42:
            print("NO WINNER, the board is full!")
            return True

        # Check horizontal locations for win
        for i in range(BOARDWIDTH - 3):
            for j in range(BOARDHEIGHT):
                if repos[j][i] == turn and repos[j][i + 1] == turn and repos[j][i + 2] == turn and repos[j][i + 3] == turn:
                    return True

        # Check vertical locations for win
        for i in range(BOARDWIDTH):
            for j in range(BOARDHEIGHT - 3):
                if repos[j][i] == turn and repos[j + 1][i] == turn and repos[j + 2][i] == turn and repos[j + 3][i] == turn:
                    return True

        # Check positively sloped diagonals
        for i in range(BOARDWIDTH - 3):
            for j in range(BOARDHEIGHT - 3):
                if repos[j][i] == turn and repos[j + 1][i + 1] == turn and repos[j + 2][i + 2] == turn and repos[j + 3][i + 3] == turn:
                    return True

        # Check negatively sloped diagonals
        for i in range(BOARDWIDTH - 3):
            for j in range(3, BOARDHEIGHT):
                if repos[j][i] == turn and repos[j - 1][i + 1] == turn and repos[j - 2][i + 2] == turn and repos[j - 3][i + 3] == turn:
                    return True

        return False

    def neighbors(self, state, turn):

        repos = deepcopy(state.representation.board)
        pm = set([])
        tranq = set([])
        win = True
        tranquility = False

        # Check if I can make a winner move
        if win:
            # Horizontal check
            for i in range(BOARDWIDTH - 3):
                for j in range(BOARDHEIGHT):
                    if repos[j][i] == turn and repos[j][i + 1] == turn and repos[j][i + 2] == turn and repos[j][i + 3] == ' ':
                        repos[j][i + 3] = turn
                        n = Connect4State(repos)
                        pm.add(n)
                        return pm
                    elif repos[j][i] == ' ' and repos[j][i + 1] == turn and repos[j][i + 2] == turn and repos[j][i + 3] == turn:
                        repos[j][i] = turn
                        n = Connect4State(repos)
                        pm.add(n)
                        return pm
                    elif repos[j][i] == turn and repos[j][i + 1] == ' ' and repos[j][i + 2] == turn and repos[j][i + 3] == turn:
                        repos[j][i + 1] = turn
                        n = Connect4State(repos)
                        pm.add(n)
                        return pm
                    elif repos[j][i] == turn and repos[j][i + 1] == turn and repos[j][i + 2] == ' ' and repos[j][i + 3] == turn:
                        repos[j][i + 2] = turn
                        n = Connect4State(repos)
                        pm.add(n)
                        return pm

            # Vertical check
            for i in range(BOARDWIDTH):
                for j in range(BOARDHEIGHT - 3):
                    if repos[j][i] == turn and repos[j + 1][i] == turn and repos[j + 2][i] == turn and repos[j + 3][i] == ' ':
                        repos[j + 3][i] = turn
                        n = Connect4State(repos)
                        pm.add(n)
                        return pm
                    elif repos[j][i] == ' ' and repos[j + 1][i] == turn and repos[j + 2][i] == turn and repos[j + 3][i] == turn:
                        repos[j][i] = turn
                        n = Connect4State(repos)
                        pm.add(n)
                        return pm
                    elif repos[j][i] == turn and repos[j + 1][i] == ' ' and repos[j + 2][i] == turn and repos[j + 3][i] == turn:
                        repos[j + 1][i] = turn
                        n = Connect4State(repos)
                        pm.add(n)
                        return pm
                    elif repos[j][i] == turn and repos[j + 1][i] == turn and repos[j + 2][i] == ' ' and repos[j + 3][i] == turn:
                        repos[j + 2][i] = turn
                        n = Connect4State(repos)
                        pm.add(n)
                        return pm

            # Positively diagonals check
            for i in range(BOARDWIDTH - 3):
                for j in range(BOARDHEIGHT - 3):
                    if repos[j][i] == turn and repos[j + 1][i + 1] == turn and repos[j + 2][i + 2] == turn and repos[j + 3][i + 3] == ' ':
                        repos[j + 3][i + 3] = turn
                        n = Connect4State(repos)
                        pm.add(n)
                        return pm
                    elif repos[j][i] == ' ' and repos[j + 1][i + 1] == turn and repos[j + 2][i + 2] == turn and repos[j + 3][i + 3] == turn:
                        repos[j][i] = turn
                        n = Connect4State(repos)
                        pm.add(n)
                        return pm
                    elif repos[j][i] == turn and repos[j + 1][i + 1] == ' ' and repos[j + 2][i + 2] == turn and repos[j + 3][i + 3] == turn:
                        repos[j + 1][i + 1] = turn
                        n = Connect4State(repos)
                        pm.add(n)
                        return pm
                    elif repos[j][i] == turn and repos[j + 1][i + 1] == turn and repos[j + 2][i + 2] == ' ' and repos[j + 3][i + 3] == turn:
                        repos[j + 2][i + 2] = turn
                        n = Connect4State(repos)
                        pm.add(n)
                        return pm

            # Negatively diagonals check
            for i in range(BOARDWIDTH - 3):
                for j in range(3, BOARDHEIGHT):
                    if repos[j][i] == turn and repos[j - 1][i + 1] == turn and repos[j - 2][i + 2] == turn and repos[j - 3][i + 3] == ' ':
                        repos[j - 3][i + 3] = turn
                        n = Connect4State(repos)
                        pm.add(n)
                        return pm
                    elif repos[j][i] == ' ' and repos[j - 1][i + 1] == turn and repos[j - 2][i + 2] == turn and repos[j - 3][i + 3] == turn:
                        repos[j][i] = turn
                        n = Connect4State(repos)
                        pm.add(n)
                        return pm
                    elif repos[j][i] == turn and repos[j - 1][i + 1] == ' ' and repos[j - 2][i + 2] == turn and repos[j - 3][i + 3] == turn:
                        repos[j - 1][i + 1] = turn
                        n = Connect4State(repos)
                        pm.add(n)
                        return pm
                    elif repos[j][i] == turn and repos[j - 1][i + 1] == turn and repos[j - 2][i + 2] == ' ' and repos[j - 3][i + 3] == turn:
                        repos[j - 2][i + 2] = turn
                        n = Connect4State(repos)
                        pm.add(n)
                        return pm
            win = False

        # If I don't have possible winner move, there is a dangerous opponent move that should be blocked
        if not win:

            # Horizontal check
            for i in range(BOARDWIDTH - 3):
                for j in range(BOARDHEIGHT):
                    if repos[j][i] == 'o' and repos[j][i + 1] == 'o' and repos[j][i + 2] == 'o' and repos[j][i + 3] == ' ':
                        repos[j][i + 3] = turn
                        n = Connect4State(repos)
                        pm.add(n)
                        return pm
                    elif repos[j][i] == ' ' and repos[j][i + 1] == 'o' and repos[j][i + 2] == 'o' and repos[j][i + 3] == 'o':
                        repos[j][i] = turn
                        n = Connect4State(repos)
                        pm.add(n)
                        return pm
                    elif repos[j][i] == 'o' and repos[j][i + 1] == ' ' and repos[j][i + 2] == 'o' and repos[j][i + 3] == 'o':
                        repos[j][i + 1] = turn
                        n = Connect4State(repos)
                        pm.add(n)
                        return pm
                    elif repos[j][i] == 'o' and repos[j][i + 1] == 'o' and repos[j][i + 2] == ' ' and repos[j][i + 3] == 'o':
                        repos[j][i + 2] = turn
                        n = Connect4State(repos)
                        pm.add(n)
                        return pm

            # Vertical check
            for i in range(BOARDWIDTH):
                for j in range(BOARDHEIGHT - 3):
                    if repos[j][i] == 'o' and repos[j + 1][i] == 'o' and repos[j + 2][i] == 'o' and repos[j + 3][i] == ' ':
                        repos[j + 3][i] = turn
                        n = Connect4State(repos)
                        pm.add(n)
                        return pm
                    elif repos[j][i] == ' ' and repos[j + 1][i] == 'o' and repos[j + 2][i] == 'o' and repos[j + 3][i] == 'o':
                        repos[j][i] = turn
                        n = Connect4State(repos)
                        pm.add(n)
                        return pm
                    elif repos[j][i] == 'o' and repos[j + 1][i] == ' ' and repos[j + 2][i] == 'o' and repos[j + 3][i] == 'o':
                        repos[j + 1][i] = turn
                        n = Connect4State(repos)
                        pm.add(n)
                        return pm
                    elif repos[j][i] == 'o' and repos[j + 1][i] == 'o' and repos[j + 2][i] == ' ' and repos[j + 3][i] == 'o':
                        repos[j + 2][i] = turn
                        n = Connect4State(repos)
                        pm.add(n)
                        return pm

            # Positively diagonals check
            for i in range(BOARDWIDTH - 3):
                for j in range(BOARDHEIGHT - 3):
                    if repos[j][i] == 'o' and repos[j + 1][i + 1] == 'o' and repos[j + 2][i + 2] == 'o' and repos[j + 3][i + 3] == ' ':
                        repos[j + 3][i + 3] = turn
                        n = Connect4State(repos)
                        pm.add(n)
                        return pm
                    elif repos[j][i] == ' ' and repos[j + 1][i + 1] == 'o' and repos[j + 2][i + 2] == 'o' and repos[j + 3][i + 3] == 'o':
                        repos[j][i] = turn
                        n = Connect4State(repos)
                        pm.add(n)
                        return pm
                    elif repos[j][i] == 'o' and repos[j + 1][i + 1] == ' ' and repos[j + 2][i + 2] == 'o' and repos[j + 3][i + 3] == 'o':
                        repos[j + 1][i + 1] = turn
                        n = Connect4State(repos)
                        pm.add(n)
                        return pm
                    elif repos[j][i] == 'o' and repos[j + 1][i + 1] == 'o' and repos[j + 2][i + 2] == ' ' and repos[j + 3][i + 3] == 'o':
                        repos[j + 2][i + 2] = turn
                        n = Connect4State(repos)
                        pm.add(n)
                        return pm

            # Negatively diagonals check
            for i in range(BOARDWIDTH - 3):
                for j in range(3, BOARDHEIGHT):
                    if repos[j][i] == 'o' and repos[j - 1][i + 1] == 'o' and repos[j - 2][i + 2] == 'o' and repos[j - 3][i + 3] == ' ':
                        repos[j - 3][i + 3] = turn
                        n = Connect4State(repos)
                        pm.add(n)
                        return pm
                    elif repos[j][i] == ' ' and repos[j - 1][i + 1] == 'o' and repos[j - 2][i + 2] == 'o' and repos[j - 3][i + 3] == 'o':
                        repos[j][i] = turn
                        n = Connect4State(repos)
                        pm.add(n)
                        return pm
                    elif repos[j][i] == 'o' and repos[j - 1][i + 1] == ' ' and repos[j - 2][i + 2] == 'o' and repos[j - 3][i + 3] == 'o':
                        repos[j - 1][i + 1] = turn
                        n = Connect4State(repos)
                        pm.add(n)
                        return pm
                    elif repos[j][i] == 'o' and repos[j - 1][i + 1] == 'o' and repos[j - 2][i + 2] == ' ' and repos[j - 3][i + 3] == 'o':
                        repos[j - 2][i + 2] = turn
                        n = Connect4State(repos)
                        pm.add(n)
                        return pm

            tranquility = True

        if tranquility:
            for j in range(0, BOARDWIDTH):
                for i in range(0, BOARDHEIGHT):
                    if repos[i][j] != ' ' and i != 0 and repos[i - 1][j] == ' ':
                        repos[i - 1][j] = turn
                        n = Connect4State(repos)
                        tranq.add(n)
                    if repos[i][j] == ' ' and i == 5:
                        repos[i][j] = turn
                        n = Connect4State(repos)
                        tranq.add(n)
            return tranq

    @staticmethod
    def print_board(board):
        # Print the board
        print('  '.join(map(str, range(BOARDWIDTH))))
        for y in range(BOARDHEIGHT):
            print('  '.join(str(board[x][y]) for x in range(BOARDWIDTH)))
        print()



