import numpy as np
import random as rd

BOARDWIDTH = 10  # number of columns in the board
BOARDHEIGHT = 10  # number of rows in the board
dicOfStates = {}



def generation(ratio):
    board = []

    # Initialize puzzle board with all 0
    for i in range(BOARDWIDTH):
        column = []
        for j in range(BOARDHEIGHT):
            column.append(0)
        board.append(column)

    # List that contains the structure of the objects
    # in increasing order of size (from 1 to 3)
    obj_list = [[(0, 0)], \
                [(0, 0), (0, 1)], \
                [(0, 0), (1, 0)], \
                [(0, 0), (0, 1), (0, -1)], \
                [(0, 0), (1, 0), (-1, 0)], \
                [(0, 0), (1, 0), (0, 1)], \
                [(0, 0), (1, 0), (0, -1)], \
                [(0, 0), (-1, 0), (0, -1)], \
                [(0, 0), (-1, 0), (0, 1)], \
                ]

    # Insert piano in the room
    board[BOARDWIDTH - 2][0] = board[BOARDWIDTH - 2][1] = board[BOARDWIDTH - 1][0] = board[BOARDWIDTH - 1][1] = 1

    # Insert object in the room
    obs, cells = 0, 0

    while cells/100 < ratio:
        r = rd.randint(0, 8)
        while True:
            i = rd.randint(1, 8)
            j = rd.randint(1, 8)
            check = True
            for cell in obj_list[r]:
                if board[i + cell[0]][j + cell[1]] != 0:
                    check = False
            if not check:
                continue
            for cell in obj_list[r]:
                board[i + cell[0]][j + cell[1]] = 2 + obs
                cells += 1
            obs += 1
            break

    print("Number of objects : " + str(obs))
    print("Number of cells : " + str(cells))

    return board, obs


board, obs = generation(0.3)

print(str(board))
print(str(obs))

