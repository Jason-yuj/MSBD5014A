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
    res = connect(q)
    print("connect ok")
    start = time.time()
    res_bar = inverse(res, 2, 1, 1 / 3)
    end = time.time()
    print(end - start)

    prob = np.exp(res_bar * (2 / 1))
    prob = prob / np.sum(prob)
    population = [i for i in range(len(prob + 1))]
    print(choices(population, list(prob), k=10))
