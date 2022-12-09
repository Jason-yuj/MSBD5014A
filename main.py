import time
from database import connect
import more_itertools
from inverse import inverse
import numpy as np
from random import choices
import argparse
import docplex
from docplex.mp.model import Model


def main():
    parser = argparse.ArgumentParser(description='process detail')
    parser.add_argument('--db', type=str, default='../database.ini', help='path to database initialization file')
    parser.add_argument('--query', type=str, default='../q12', help='path to query file')
    parser.add_argument('--type', type=str, default='1', help='type of the query')
    opt = parser.parse_args()


if __name__ == '__main__':
    # read query from file
    file = open('../q12', 'r')
    dbfile = "../database.ini"
    q = file.read()
    # fetch the query result directly from the database
    res = connect(q, dbfile)
    print("connection ok")
    start = time.time()
    # set up for parameters
    beta = 1 / 3
    epi = 1
    l = 1
    # calculate the s(v,r) for every possible r
    res_bar = inverse(res, l, epi, beta)

    # set up the distribution for the sampling
    prob = np.exp(res_bar * (epi / 2))
    prob = prob / np.sum(prob)
    population = [i for i in range(len(prob + 1))]
    # output the sampling result for 10 times
    result = choices(population, list(prob), k=10)
    end = time.time()
    print("processing time: " + str(end - start))
    print("query result: "+ str(result))
    print(np.mean(np.array(result)))
