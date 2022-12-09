import time
from src.database import connect
from src.inverse import inverse
import numpy as np
from random import choices
import argparse
import matplotlib.pyplot as plt
import docplex
from docplex.mp.model import Model


if __name__ == '__main__':
    parser = argparse.ArgumentParser(description='sql over DP demo')
    parser.add_argument('--db', type=str, default='./database.ini', help='path to database initialization file')
    parser.add_argument('--query', '--q', type=str, default='./q12', help='path to query file')
    parser.add_argument('--type', '--t', type=int, choices=[1, 2], default=1, help='type of the query')
    parser.add_argument('--out', type=str, default='./prob_density.png',
                        help='File to output of the probability density of the result')
    opt = parser.parse_args()

    # read query from file
    file = open(opt.query, 'r')
    q = file.read()
    # fetch the query result directly from the database
    res = connect(q, opt.db)
    print("database connection ok")
    start = time.time()
    # set up for parameters
    beta = 1 / 3
    epi = 1
    l = opt.type
    # calculate the s(v,r) for every possible r
    res_bar, true_value, min_inverse, max_inverse = inverse(res, l, epi, beta)

    # set up the distribution for the sampling
    prob = np.exp(res_bar * (epi / 2))
    prob = prob / np.sum(prob)
    population = [i for i in range(len(prob + 1))]
    # output the sampling result for 10 times
    result = choices(population, list(prob), k=1)
    end = time.time()
    print("processing time: {}".format(end - start))
    result = np.mean(np.array(result))
    print("query result over DP: {}".format(result))
    print("true query result: {}".format(true_value))
    print("relative error: {}".format((true_value - result)/result))
    plt.plot(list(range(min_inverse, max_inverse+1)), prob[min_inverse:max_inverse+1])
    plt.savefig(opt.out)
