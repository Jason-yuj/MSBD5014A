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
    :param epi: privacy budget
    :param beta: probability beta
    :param result: query result from database, check the psycopg2 API
                   for q12, only one element, which are the result from a single user
                   for q5, the format will be (result, user set)
    :param l: case for l
    :return: s(v,r) for all r
    """
    # get the result from all the possible use set
    t = [i[0] for i in result]

    # we would like to get the true result from here
    true_value = sum(t)
    print(true_value)

    # possible max value D from the query
    D = 1e3 * len(t)

    # calculate tau from the parameters
    tau = math.ceil((2 / epi) * math.log((D + 1) / beta))

    inverses = []

    # case for l = 1
    if l == 1:
        for j in range(2 * tau + 1):
            inverses.append(true_value - sum(nlargest(j, t)))

    # case for l = 2
    elif l == 2:
        user_set = [i[1] for i in result]
        for j in range(2 * tau + 1):
            # use the LP solver the get the shifted inverse
            inverses.append(LpSolver(user_set, t, j))

    # based on f_tild(v,j) to get s(v,j)
    prob = get_distribution(inverses, D, tau)
    return prob


def get_distribution(inverses, D, tau):
    min_inverse = min(inverses)
    max_inverse = max(inverses)

    prob = np.zeros(int(D+1))
    prob += (-tau-1)
    # we only need mannually check r between min_inverse and max_inverse, everything else is the same
    # follow the standard process in the paper
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
