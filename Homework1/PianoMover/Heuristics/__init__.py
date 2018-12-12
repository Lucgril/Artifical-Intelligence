import numpy as np


class Heuristic:

    def __init__(self):
        pass

    def H(self, state):
        return 1


class PianoMoverHeur(Heuristic):

    # Manhattan Heuristic Function
    def manhattan(self, state):

        n_obj = len(np.where(state.representation.board[:1 + state.representation.piano[0][2], \
                             state.representation.piano[1][0]:10] > 1)[0])

        distance = (abs(state.representation.piano[0][0] - 0) + \
                    abs(state.representation.piano[1][0] - 8)) * (n_obj + 1)

        return distance

    # Euclidean Heuristic Function
    def euclidean(self, state):

        n_obj = len(np.where(state.representation.board[:1 + state.representation.piano[0][2], \
                             state.representation.piano[1][0]:10] > 1)[0])

        v1 = np.array([state.representation.piano[0][0], state.representation.piano[1][0]])
        v2 = np.array([0, 8])

        return np.linalg.norm(v1 - v2) * (n_obj + 1)
