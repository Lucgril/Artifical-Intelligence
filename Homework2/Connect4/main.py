import numpy as np

BOARDHEIGHT = 6
BOARDWIDTH = 7


def create_board():
    board = np.full([BOARDHEIGHT, BOARDWIDTH], ' ')
    return board


