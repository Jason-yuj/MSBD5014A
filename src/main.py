import time
from database import connect
import more_itertools
from inverse import inverse
import numpy as np
from random import choices
import docplex
from docplex.mp.model import Model

if __name__ == '__main__':
    # read query from file
    file = open('../q5', 'r')
    q = file.read()
    # fetch the query result directly from the database
    res = connect(q)
    print("connect ok")
    start = time.time()
    # set up for parameters
    beta = 1/3
    epi = 1
    l = 2
    # calculate the s(v,r) for every possible r
    res_bar = inverse(res, l, epi, beta)
    end = time.time()
    print(end - start)

    # set up the distribution for the sampling
    prob = np.exp(res_bar * (epi / 2))
    prob = prob / np.sum(prob)
    population = [i for i in range(len(prob + 1))]
    # output the sampling result for 10 times
    print(choices(population, list(prob), k=10))
