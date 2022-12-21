import time
from src.database import connect
from src.inverse import inverse, inverse_k
import numpy as np
from random import choices
import argparse
import matplotlib.pyplot as plt
import math
import docplex
from docplex.mp.model import Model


def rank_error(res, k, private_result):
    values = [float(i[0]) for i in res]
    k = math.ceil((len(res) - 1) * (1 - k))
    ele = min(values, key=lambda x: abs(x - private_result))
    first_idx = values.index(ele)
    last_idx = len(values) - 1 - values[::-1].index(ele)
    if first_idx <= k <= last_idx:
        return 0
    else:
        return min(abs(last_idx-k), abs(first_idx-k))

if __name__ == '__main__':
    parser = argparse.ArgumentParser(description='sql over DP demo')
    parser.add_argument('--db', type=str, default='./database.ini', help='path to database initialization file')
    parser.add_argument('--query', '--q', type=str, default='./q12', help='path to query file')
    parser.add_argument('--type', '--t', type=str, choices=["count", "k"], help='type of the query', default="count")
    parser.add_argument('--l', type=int, choices=[1, 2], default=1, help='case for l')
    parser.add_argument('--out', type=str, default='./prob_density.png',
                        help='File to output of the probability density of the result')
    parser.add_argument('--k', type=float, default=0.5,
                        help='quantile for k-selection')
    parser.add_argument('--epi', type=float, default=1,
                        help='privacy budget')
    opt = parser.parse_args()

    # read query from file
    file = open(opt.query, 'r')
    q = file.read()
    # fetch the query result directly from the database
    res = connect(q, opt.db)
    print("database connection ok")
    # print(res[451])
    start = time.time()
    # set up for parameters
    beta = 1 / 3
    epi = opt.epi
    type = opt.type
    l = opt.l
    k = opt.k
    if type == "k":
        res_bar, true_value, min_inverse, max_inverse = inverse_k(res, l, epi, beta, k)
    elif type == "count":
        # calculate the s(v,r) for every possible r
        res_bar, true_value, min_inverse, max_inverse = inverse(res, l, epi, beta)
    # set up the distribution for the sampling
    prob = np.exp(res_bar * (epi / 2))
    prob = prob / np.sum(prob)
    population = [i for i in range(len(prob + 1))]
    # # output the sampling result for 10 times
    result = choices(population, list(prob), k=1)
    end = time.time()
    print("processing time: {}".format(end - start))
    result = np.mean(np.array(result))
    print("query result over DP: {}".format(result))
    print("true query result: {}".format(true_value))
    print("relative error: {}".format((true_value - result)/true_value))
    if type == "k":
        print("rank error: {}".format(rank_error(res, k, result)))
    plt.plot(list(range(min_inverse, max_inverse+1)), prob[min_inverse:max_inverse+1])
    plt.savefig(opt.out)
