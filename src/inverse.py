import operator
import more_itertools
from heapq import nlargest
import math
from cplex2 import LpSolver
import time
import numpy as np


def inverse(result, l, epi, beta):
    """
    # in this function we will calculate shifted inverse from the query result
    :param result: true query result from database
    :param l: case for l
    :return:
    """

    t = [i[0] for i in result]

    true_value = sum(t)
    print(true_value)

    D = 1e3 * len(t)

    tau = math.ceil((2 / epi) * math.log((D + 1) / beta))

    inverses = []

    if l == 1:

        for j in range(2 * tau + 1):
            inverses.append(true_value - sum(nlargest(j, t)))

    elif l == 2:

        user_set = [i[1] for i in result]
        for j in range(2 * tau + 1):
            inverses.append(LpSolver(user_set, t, j))
    prob = get_distribution(inverses, D, tau)
    return prob


def get_distribution(inverses, D, tau):
    min_inverse = min(inverses)
    max_inverse = max(inverses)

    prob = np.zeros(int(D+1))
    prob += (-tau-1)
    for r in range(min_inverse, max_inverse+1):
        prob[r] -= (-tau-1)
        if r == inverses[tau]:
            continue
        for j in range(1, 2 * tau + 1):
            if 0 < j <= tau:
                if inverses[j] < r <= inverses[j - 1]:
                    prob[r] += (-tau + j - 1)
            elif tau < j <= 2 * tau:
                if inverses[j] <= r < inverses[j - 1]:
                    prob[r] += (tau - j)
    return prob

if __name__ == '__main__':
    pass