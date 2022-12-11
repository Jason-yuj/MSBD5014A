import operator
from heapq import nlargest
import math
from src.cplex2 import LpSolver, LpSolver_k
from sortedcontainers import SortedDict
import time
import numpy as np
from tqdm import tqdm
import matplotlib.pyplot as plt


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

    # possible max value D from the query
    D = 1e3 * len(t)

    # calculate tau from the parameters
    tau = math.ceil((2 / epi) * math.log((D + 1) / beta))

    inverses = []

    # case for l = 1
    if l == 1:
        for j in tqdm(range(2 * tau + 1)):
            inverses.append(true_value - sum(nlargest(j, t)))

    # case for l = 2
    elif l == 2:
        user_set = [i[1] for i in result]
        for j in tqdm(range(2 * tau + 1)):
            # use the LP solver the get the shifted inverse
            inverses.append(LpSolver(user_set, t, j))
    # based on f_tild(v,j) to get s(v,j)
    prob = get_distribution(inverses, D, tau)
    return prob, true_value, min(inverses), max(inverses)


def inverse_k(result, l, epi, beta, percentage):
    value = [i[0] for i in result]
    users = [i[1] for i in result]
    distinct_users = list(set(users))
    users_c = {}
    for user in distinct_users:
        users_c[user] = 0
    users_c = SortedDict(users_c)

    if l == 1:
        D = 1e2
    else:
        D = 2e5

    tau = math.ceil((2 / epi) * math.log((D + 1) / beta))
    k = math.ceil((len(result) - 1) * (1 - percentage))
    inverses = np.zeros(int(2 * tau)+1)

    true_res = float(result[k][0])
    j = 0
    # case for l == 1
    if l == 1:
        for i in tqdm(range(len(result))):
            count_largest = 0
            for n in range(j):
                count_largest += users_c.peekitem(-n)[1]
            count = i - count_largest
            if count <= k:
                inverses[j] = float(result[i][0])
            else:
                j += 1
                if j > 2*tau:
                    break
                else:
                    inverses[j] = float(result[i][0])
            userid = result[i][1]
            users_c[userid] += 1
    # case for l == 2
    elif l == 2:
        VC_i = [0] * len(result)
        for i in tqdm(range(len(result))):
            VC_i[i] += LpSolver_k(users, i, k)
        for j in range(len(inverses)):
            vc = np.array(VC_i)
            clipped_vc = vc[vc <= j]
            inverses[j] = min(value[:len(clipped_vc)])
    prob = get_distribution(inverses, D, tau)
    return prob, true_res, math.ceil(min(inverses)), math.floor(max(inverses))


def get_distribution(inverses, D, tau):
    min_inverse = min(inverses)
    max_inverse = max(inverses)

    prob = np.zeros(int(D+1))
    prob += (-tau-1)
    # we only need manually check r between min_inverse and max_inverse, everything else is the same
    # follow the standard process in the paper
    for r in range(math.floor(min_inverse), math.ceil(max_inverse+1)):
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
