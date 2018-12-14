from copy import deepcopy
import numpy as np

BOARDHEIGHT = 6
BOARDWIDTH = 7


class Connect4Representation:
    def __init__(self, x):
        self.board = x


class State:
    def __init__(self, x):
        self.representation = Connect4Representation(x)

    def isSolution(state, turn):

        # Check if the board is full
        if len(np.where(state.representation.board == ' ')[0]) == 42:
            print("NO WINNER, the board is full!")
            return True

        # Check horizontal locations for win
        for i in range(BOARDWIDTH - 3):
            for j in range(BOARDHEIGHT):
                if state.representation.board[j][i] == turn and state.representation.board[j][i + 1] == turn \
                        and state.representation.board[j][i + 2] == turn and state.representation.board[j][i + 3] == turn:
                    return True

        # Check vertical locations for win
        for i in range(BOARDWIDTH):
            for j in range(BOARDHEIGHT - 3):
                if state.representation.board[j][i] == turn and state.representation.board[j + 1][i] == turn \
                        and state.representation.board[j + 2][i] == turn and state.representation.board[j + 3][i] == turn:
                    return True

        # Check positively sloped diagonals
        for i in range(BOARDWIDTH - 3):
            for j in range(BOARDHEIGHT - 3):
                if state.representation.board[j][i] == turn and state.representation.board[j + 1][i + 1] == turn \
                        and state.representation.board[j + 2][i + 2] == turn and state.representation.board[j + 3][i + 3] == turn:
                    return True

        # Check negatively sloped diagonals
        for i in range(BOARDWIDTH - 3):
            for j in range(3, BOARDHEIGHT):
                if state.representation.board[j][i] == turn and state.representation.board[j - 1][i + 1] == turn \
                        and state.representation.board[j - 2][i + 2] == turn and state.representation.board[j - 3][i + 3] == turn:
                    return True

        return False


class Game:
    def __init__(self):
        x = [[' ' for x in range(7)] for x in range(6)]
        self.state = State(x)

    def makeMove(self, s):
        repos = deepcopy(s.representation.board)
        self.state = State(repos)

    def getState(self):
        return self.state

    def neighbors(self, turn):

        state = self.state
        repos = deepcopy(state.representation.board)
        sto = deepcopy(repos)
        tranq = set([])
        pm = set([])
        win = True
        tranquility = True

        # Check if I can make a winner move
        if win:
            # Horizontal check
            for i in range(BOARDWIDTH - 3):
                for j in range(BOARDHEIGHT):
                    if repos[j][i] == 'R' and repos[j][i + 1] == 'R' and repos[j][i + 2] == 'R' \
                            and repos[j][i + 3] == ' ':
                        repos[j][i + 3] = turn
                        n = State(repos)
                        pm.add(n)
                        return pm
                    elif repos[j][i] == ' ' and repos[j][i + 1] == 'R' and repos[j][i + 2] == 'R' \
                            and repos[j][i + 3] == 'R':
                        repos[j][i] = turn
                        n = State(repos)
                        pm.add(n)
                        return pm
                    elif repos[j][i] == 'R' and repos[j][i + 1] == ' ' and repos[j][i + 2] == 'R' \
                            and repos[j][i + 3] == 'R':
                        repos[j][i + 1] = turn
                        n = State(repos)
                        pm.add(n)
                        return pm
                    elif repos[j][i] == 'R' and repos[j][i + 1] == 'R' and repos[j][i + 2] == ' ' \
                            and repos[j][i + 3] == 'R':
                        repos[j][i + 2] = turn
                        n = State(repos)
                        pm.add(n)
                        return pm

            # Vertical check
            for i in range(BOARDWIDTH):
                for j in range(BOARDHEIGHT - 3):
                    if repos[j][i] == 'R' and repos[j + 1][i] == 'R' and repos[j + 2][i] == 'R' \
                            and repos[j + 3][i] == ' ':
                        repos[j + 3][i] = turn
                        n = State(repos)
                        pm.add(n)
                        return pm
                    elif repos[j][i] == ' ' and repos[j + 1][i] == 'R' and repos[j + 2][i] == 'R' \
                            and repos[j + 3][i] == 'R':
                        repos[j][i] = turn
                        n = State(repos)
                        pm.add(n)
                        return pm
                    elif repos[j][i] == 'R' and repos[j + 1][i] == ' ' and repos[j + 2][i] == 'R' \
                            and repos[j + 3][i] == 'R':
                        repos[j + 1][i] = turn
                        n = State(repos)
                        pm.add(n)
                        return pm
                    elif repos[j][i] == 'R' and repos[j + 1][i] == 'R' and repos[j + 2][i] == ' ' \
                            and repos[j + 3][i] == 'R':
                        repos[j + 2][i] = turn
                        n = State(repos)
                        pm.add(n)
                        return pm

            # Positively diagonals check
            for i in range(BOARDWIDTH - 3):
                for j in range(BOARDHEIGHT - 3):
                    if repos[j][i] == 'R' and repos[j + 1][i + 1] == 'R' and repos[j + 2][i + 2] == 'R' \
                            and repos[j + 3][i + 3] == ' ':
                        repos[j + 3][i + 3] = turn
                        n = State(repos)
                        pm.add(n)
                        return pm
                    elif repos[j][i] == ' ' and repos[j + 1][i + 1] == 'R' and repos[j + 2][i + 2] == 'R' \
                            and repos[j + 3][i + 3] == 'R':
                        repos[j][i] = turn
                        n = State(repos)
                        pm.add(n)
                        return pm
                    elif repos[j][i] == 'R' and repos[j + 1][i + 1] == ' ' and repos[j + 2][i + 2] == 'R' \
                            and repos[j + 3][i + 3] == 'R':
                        repos[j + 1][i + 1] = turn
                        n = State(repos)
                        pm.add(n)
                        return pm
                    elif repos[j][i] == 'R' and repos[j + 1][i + 1] == 'R' and repos[j + 2][i + 2] == ' ' \
                            and repos[j + 3][i + 3] == 'R':
                        repos[j + 2][i + 2] = turn
                        n = State(repos)
                        pm.add(n)
                        return pm

            # Negatively diagonals check
            for i in range(BOARDWIDTH - 3):
                for j in range(3, BOARDHEIGHT):
                    if repos[j][i] == 'R' and repos[j - 1][i + 1] == 'R' and repos[j - 2][i + 2] == 'R' \
                            and repos[j - 3][i + 3] == ' ':
                        repos[j - 3][i + 3] = turn
                        n = State(repos)
                        pm.add(n)
                        return pm
                    elif repos[j][i] == ' ' and repos[j - 1][i + 1] == 'R' and repos[j - 2][i + 2] == 'R' \
                            and repos[j - 3][i + 3] == 'R':
                        repos[j][i] = turn
                        n = State(repos)
                        pm.add(n)
                        return pm
                    elif repos[j][i] == 'R' and repos[j - 1][i + 1] == ' ' and repos[j - 2][i + 2] == 'R' \
                            and repos[j - 3][i + 3] == 'R':
                        repos[j - 1][i + 1] = turn
                        n = State(repos)
                        pm.add(n)
                        return pm
                    elif repos[j][i] == 'R' and repos[j - 1][i + 1] == 'R' and repos[j - 2][i + 2] == ' ' \
                            and repos[j - 3][i + 3] == 'R':
                        repos[j - 2][i + 2] = turn
                        n = State(repos)
                        pm.add(n)
                        return pm
            win = False

        # If I don't have possible winner move, there is a dangerous opponent move that should be blocked
        if not win:

            # Horizontal check
            for i in range(BOARDWIDTH - 3):
                for j in range(BOARDHEIGHT):
                    if repos[j][i] == 'G' and repos[j][i + 1] == 'G' and repos[j][i + 2] == 'G' \
                            and repos[j][i + 3] == ' ':
                        repos[j][i + 3] = turn
                        n = State(repos)
                        pm.add(n)
                        return pm
                    elif repos[j][i] == ' ' and repos[j][i + 1] == 'G' and repos[j][i + 2] == 'G' \
                            and repos[j][i + 3] == 'G':
                        repos[j][i] = turn
                        n = State(repos)
                        pm.add(n)
                        return pm
                    elif repos[j][i] == 'G' and repos[j][i + 1] == ' ' and repos[j][i + 2] == 'G' \
                            and repos[j][i + 3] == 'G':
                        repos[j][i + 1] = turn
                        n = State(repos)
                        pm.add(n)
                        return pm
                    elif repos[j][i] == 'G' and repos[j][i + 1] == 'G' and repos[j][i + 2] == ' ' \
                            and repos[j][i + 3] == 'G':
                        repos[j][i + 2] = turn
                        n = State(repos)
                        pm.add(n)
                        return pm

            # Vertical check
            for i in range(BOARDWIDTH):
                for j in range(BOARDHEIGHT - 3):
                    if repos[j][i] == 'G' and repos[j + 1][i] == 'G' and repos[j + 2][i] == 'G' \
                            and repos[j + 3][i] == ' ':
                        repos[j + 3][i] = turn
                        n = State(repos)
                        pm.add(n)
                        return pm
                    elif repos[j][i] == ' ' and repos[j + 1][i] == 'G' and repos[j + 2][i] == 'G' \
                            and repos[j + 3][i] == 'G':
                        repos[j][i] = turn
                        n = State(repos)
                        pm.add(n)
                        return pm
                    elif repos[j][i] == 'G' and repos[j + 1][i] == ' ' and repos[j + 2][i] == 'G' \
                            and repos[j + 3][i] == 'G':
                        repos[j + 1][i] = turn
                        n = State(repos)
                        pm.add(n)
                        return pm
                    elif repos[j][i] == 'G' and repos[j + 1][i] == 'G' and repos[j + 2][i] == ' ' \
                            and repos[j + 3][i] == 'G':
                        repos[j + 2][i] = turn
                        n = State(repos)
                        pm.add(n)
                        return pm

            # Positively diagonals check
            for i in range(BOARDWIDTH - 3):
                for j in range(BOARDHEIGHT - 3):
                    if repos[j][i] == 'G' and repos[j + 1][i + 1] == 'G' and repos[j + 2][i + 2] == 'G' \
                            and repos[j + 3][i + 3] == ' ':
                        repos[j + 3][i + 3] = turn
                        n = State(repos)
                        pm.add(n)
                        return pm
                    elif repos[j][i] == ' ' and repos[j + 1][i + 1] == 'G' and repos[j + 2][i + 2] == 'G' \
                            and repos[j + 3][i + 3] == 'G':
                        repos[j][i] = turn
                        n = State(repos)
                        pm.add(n)
                        return pm
                    elif repos[j][i] == 'G' and repos[j + 1][i + 1] == ' ' and repos[j + 2][i + 2] == 'G' \
                            and repos[j + 3][i + 3] == 'G':
                        repos[j + 1][i + 1] = turn
                        n = State(repos)
                        pm.add(n)
                        return pm
                    elif repos[j][i] == 'G' and repos[j + 1][i + 1] == 'G' and repos[j + 2][i + 2] == ' ' \
                            and repos[j + 3][i + 3] == 'G':
                        repos[j + 2][i + 2] = turn
                        n = State(repos)
                        pm.add(n)
                        return pm

            # Negatively diagonals check
            for i in range(BOARDWIDTH - 3):
                for j in range(3, BOARDHEIGHT):
                    if repos[j][i] == 'G' and repos[j - 1][i + 1] == 'G' and repos[j - 2][i + 2] == 'G' \
                            and repos[j - 3][i + 3] == ' ':
                        repos[j - 3][i + 3] = turn
                        n = State(repos)
                        pm.add(n)
                        return pm
                    elif repos[j][i] == ' ' and repos[j - 1][i + 1] == 'o' and repos[j - 2][i + 2] == 'o' \
                            and repos[j - 3][i + 3] == 'o':
                        repos[j][i] = turn
                        n = State(repos)
                        pm.add(n)
                        return pm
                    elif repos[j][i] == 'G' and repos[j - 1][i + 1] == ' ' and repos[j - 2][i + 2] == 'G' \
                            and repos[j - 3][i + 3] == 'G':
                        repos[j - 1][i + 1] = turn
                        n = State(repos)
                        pm.add(n)
                        return pm
                    elif repos[j][i] == 'G' and repos[j - 1][i + 1] == 'G' and repos[j - 2][i + 2] == ' ' \
                            and repos[j - 3][i + 3] == 'G':
                        repos[j - 2][i + 2] = turn
                        n = State(repos)
                        pm.add(n)
                        return pm

            tranquility = True

        # if there aren't dangerous opponent moves and possible winner move, analyze all possible moves
        if tranquility:
            for j in range(0, 7):
                for i in range(0, 6):
                    if sto[i][j] != ' ' and i != 0 and sto[i - 1][j] == ' ':
                        sto[i - 1][j] = turn
                        n = State(sto)
                        tranq.add(n)
                        sto = deepcopy(repos)
                    if sto[i][j] == ' ' and i == 5:
                        sto[i][j] = turn
                        n = State(sto)
                        tranq.add(n)
                        sto = deepcopy(repos)
            return tranq

    @staticmethod
    def print_board(board):
        print(" -------------------------------")

        temp = 1
        for row in board:
            # Draw each row
            linetodraw = ""
            for value in row:
                linetodraw += " | " + value
            linetodraw += " |"
            print(linetodraw + "  " + str(temp))
            temp += 1
            print(" -------------------------------")

        print('   1   2   3   4   5   6   7')
