import time
import psutil
import sys
import random as rd
import numpy as np

import GameModels as G
import Heuristics as H

FORNITURE_SIZE_2 = 2
FORNITURE_SIZE_3 = 6
BOARDWIDTH = 10  # number of columns in the board
BOARDHEIGHT = 10  # number of rows in the board
RATIO = 0.3
dicOfStates = {}


def argMin(setOfStates):
    v = []
    k = []
    for sk in setOfStates:
        dicOfStates[sk] = heuristic.euclidean(sk)
        if sk in dicOfStates:
            v.append(dicOfStates[sk])
            k.append(sk)
    if len(v) > 0:
        return k[v.index(min(v))]
    else:
        return None


def pick(setOfStates):
    return argMin(setOfStates)


def backpath(state):
    padre = state.parent
    lStates = [state]
    while padre!=None:
        lStates.append(padre)
        padre = padre.parent
    return reversed(lStates)


def search(game, state0):
    sHorizon = set([])
    sExplored = set([])
    sHorizon.add(state0)
    while (len(sHorizon) > 0):
        view = pick(sHorizon)
        if not (view is None):
            if game.solution(view):
                return backpath(view)
            sExplored.add(view)
            sHorizon = ((sHorizon | game.neighbors(view)) - sExplored)
    return None


def get_starting_board(ratio):
    board = np.full([10, 10], 0)

    # List that contains the structure of the objects
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

    # Insert objects in the room
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


# Main
start_time = time.time()

heuristic = H.PianoMoverHeur()

# Instance generation
board, obj = get_starting_board(RATIO)
print(board)
print("\n")
game = G.PianoMoverGame(board, obj)

state0 = game.getState()
dicOfStates[state0] = heuristic.euclidean(state0)
solution = search(game, state0)

print("Start \n")

cost = 0

for x in solution.__iter__():
    cost += x.cost
    print(x.representation.board)
    print("\n")
    print("Level of the node: " + str(x.level))
print("Cost of the solution: " + str(cost))

# Current file name
print("\n \n")
print("The file name is: ")
print(sys.argv[0])

# Time needed
print("\n \n")
print("The time needed is: ")
print("--- %s seconds ---" % (time.time() - start_time))

# Memory used
print("\n \n")
print("The memory used is: ")
print(psutil.virtual_memory())

