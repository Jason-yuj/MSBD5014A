import more_itertools
from heapq import nlargest
import math


def inverse(result, l, epi, beta):
    """
    # in this function we will calculate shifted inverse from the query result
    :param result: true query result from database
    :param l: case for l
    :return:
    """
    t = list(more_itertools.flatten(result))

    true_value = sum(t)

    D = 1e3 * len(t)

    tau = math.ceil((2 / epi) * math.log((D+1)/beta))

    inverses = []

    for j in range(2 * tau + 1):
        inverses.append(true_value - sum(nlargest(j, t)))

    prob = get_distribution(inverses, D, tau)

    return prob


def get_distribution(inverses, D, tau):
    min_inverse = min(inverses)
    max_inverse = max(inverses)

    prob = []
    for r in range(int(D + 1)):
        if r <= min_inverse or r > max_inverse:
            prob.append(-tau-1)
        elif min_inverse <= r <= max_inverse:
            if r == inverses[tau]:
                prob.append(0)
                continue
            for j in range(1, 2*tau+1):
                if 0 < j <= tau:
                    if inverses[j] < r <= inverses[j-1]:
                        prob.append(-tau+j-1)
                elif tau < j <= 2*tau:
                    if inverses[j] <= r < inverses[j-1]:
                        prob.append(-tau-1)
    return prob

if __name__ == '__main__':
    pass