import time
from database import connect
from inverse import inverse
import numpy as np
from random import choices

if __name__ == '__main__':

    # read query from file
    file = open('../query', 'r')
    q = file.read()
    res = connect(q)
    print("connect ok")
    start = time.time()
    res_bar = inverse(res, 1, 1, 1/3)
    end = time.time()

    prob = np.exp(np.array(res_bar) * ( 2 / 1))
    prob = prob / np.sum(prob)
    population = [i for i in range(len(prob + 1))]
    print(choices(population, list(prob), k=10))
    print(end - start)