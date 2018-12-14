from GameModels import Game, State
from Heuristics import Heuristic1, Heuristic2


from copy import deepcopy
import time
import sys
import psutil

LEVEL = 3
BOARDHEIGHT = 6
BOARDWIDTH = 7

heuristic = Heuristic1()
game = Game()
turn = 'R'

while True:

    # Red turn (non human player)
    mx = -9999
    ix = game.getState()

    if turn == 'R':
        start_time = time.time()

        states = game.neighbors(turn)

        print("Red is playing, please wait...")
        print

        for s in states:
            h = heuristic.Hl(game, s, LEVEL, turn)
            if h >= mx:
                mx = h
                ix = s

        game.makeMove(ix)

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

        game.print_board(game.getState().representation.board)

        turn = 'G'
        if State.isSolution(ix, 'R'):
            print("RED PLAYER WINS!")
            break

    # Yellow turn
    mx = -9999
    if turn == 'G':
        states = game.neighbors(turn)

        # print ("Yellow is playing")
        print("It is your turn! Insert a pawn in position:")
        print

        print("Row:")
        row = input()
        row = int(row) - 1

        print("Column:")
        column = input()
        column = int(column) - 1

        state = game.getState()
        stor = deepcopy(state.representation.board)

        if column >= BOARDWIDTH:
            print("Move it is not allowed, please try again!")
            continue
        if row >= BOARDHEIGHT:
            print("Move it is not allowed, please try again!")
            continue
        if stor[column][row] != ' ':
                print("Move it is not allowed, please try again!")
                continue
        if stor[row][column] == ' ':
            stor[row][column] = 'G'
            state = State(stor)

        game.makeMove(state)
        game.print_board(game.getState().representation.board)

        turn = 'R'
        if State.isSolution(state, 'G'):
            print("YOU WIN!")
            break

