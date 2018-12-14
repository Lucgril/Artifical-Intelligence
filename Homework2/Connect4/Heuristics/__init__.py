class Heuristic1:
    def __init__(self):
        pass

    # Level 0
    def H0(self, state):

        cont1 = 0
        for j in range(0, 7):
            for i in range(0, 5):
                if state.representation.board[i][j] == 'R' and state.representation.board[i + 1][j] == 'R':
                    cont1 += 1
        cont2 = 0
        for i in range(0, 6):
            for j in range(0, 5):
                if state.representation.board[i][j] == 'R' and state.representation.board[i][j + 1] == 'R':
                    cont2 += 1

        return cont1 + cont2

    # Level h
    def Hl(self, game, state, h, turn):
        if h == 0:
            return self.H0(state)
        if turn == 'R':
            nexTurn = 'G'
            return max([self.Hl(game, x, h - 1, nexTurn) for x in game.neighbors(turn)])
        else:
            nexTurn = 'R'
            return min([self.Hl(game, x, h - 1, nexTurn) for x in game.neighbors(turn)])


class Heuristic2:
    def __init__(self):
        pass

    # Level 0
    def H0(self, state):

        v = 0
        cont1 = 3
        for j in range(0, 7):
            for i in range(0, 6):
                if state.representation.board[i][j] == 'R':
                    cont1 -= 1
                    if cont1 == 0:
                        v += 1
                        cont1 = 3
                else:
                    cont1 = 3

        r = 0
        cont2 = 3
        for i in range(0, 6):
            for j in range(0, 7):
                if state.representation.board[i][j] == 'R':
                    cont2 -= 1
                    if cont2 == 0:
                        r += 1
                        cont2 = 3
                else:
                    cont2 = 3

        VV = 0
        cont3 = 3
        for j in range(0, 7):
            for i in range(0, 6):
                if state.representation.board[i][j] == 'G':
                    cont3 -= 1
                    if cont3 == 0:
                        VV += 1
                        cont3 = 3
                else:
                    cont3 = 3

        RR = 0
        cont4 = 3
        for i in range(0, 6):
            for j in range(0, 7):
                if state.representation.board[i][j] == 'G':
                    cont4 -= 1
                    if cont4 == 0:
                        RR += 1
                        cont4 = 3
                else:
                    cont4 = 3

        return v + r - VV - RR

    # Level h
    def Hl(self, game, state, h, turn):
        if h == 0:
            return self.H0(state)
        if turn == 'R':
            nexTurn = 'G'
            return max([self.Hl(game, x, h - 1, nexTurn) for x in game.neighbors(turn)])
        else:
            nexTurn = 'R'
            return min([self.Hl(game, x, h - 1, nexTurn) for x in game.neighbors(turn)])

