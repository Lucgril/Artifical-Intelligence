BOARDWIDTH = 10  # number of columns in the board
BOARDHEIGHT = 10  # number of rows in the board


class Heuristic:

    def __init__(self):
        pass

    def H(self, state):
        return 1


class PianoMoverHeur(Heuristic):

    def manhattan(self, state):
        return abs(state.representation.piano[0][0] - 0) + abs(state.representation.piano[1][0] - (BOARDHEIGHT - 2))
