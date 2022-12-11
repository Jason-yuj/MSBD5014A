# MSBD5014A

## Overview

This code is the project of MSBD5014A in Fall 2022 supervised by Ke Yi, and the project title is SQl over Differential Privacy.

Primary source paper is: 

```
   "Shifted Inverse: A General Mechanism for Monotonic Functions under User Differential Privacy."
   Juanru Fang, Wei Dong, Ke Yi.
   ACM Conference on Computer and Communications Security (CCS), November 2022.
```

and one background paper:

```
   "R2T: Instance-optimal Truncation for Differentially Private Query Evaluation with Foreign Keys."
   Wei Dong, Juanru Fang, Ke Yi, Yuchao Tao, and Ashwin Machanavajjhala.
   ACM SIGMOD International Conference on Management of Data (SIGMOD), June 2022.
```

## Software

- we use **python** for programming language.
- we use [**postgreSQL**](https://www.postgresql.org/) as the relational database.
- we use [**cplex**](https://www.ibm.com/docs/en/icos/20.1.0?topic=cplex-setting-up-python-api) for solving linear program.

- all the relational tables will be the same as **tpch**. 
  Typically in this implementation, we generate 100MB data for experiment.

## Dependencies

check requirement file in the repo.

- **psycopg2, config** for connecting database.
- **docplex, cplex** for solving linear program.
- **numpy** for calculation.
- **tqdm, matplotlib** for visualization.
- [**sortedcontainers**](https://grantjenks.com/docs/sortedcontainers/#) for better efficiency in some cases.

## Usage

after setting up all the software, you need to prepare a file where you write your query.

Application options can be seen with:

```
python main.py --help
```

usage of arguments:

- **db**, filepath of database connect, default will be _database.ini_.
- **query**, filepath of query, default will be _q12_.
- **type**, type of the query, only have count and k(for k-selection) for now. Default will be _count_, corresponding to q12.
- **out**, filepath of the output which is a probability density, default will be _prob_density.png_.
- **k**, specific quantile we want for the k-selection query, default will be _0.5_.
- **l**, case for l of the query, default will be _1_, corresponding to q12.
- **epi**, privacy budget. Default will be _1_.

Sample:

```
python main.py --db ./database.ini --q ./q12 --t count --l 1 --out ./prob_density.png --epi 1
```
In this case, we will get the result of q12, which is a count function with l = 1, and the privacy budget is 1.

the result will be:
```
processing time: 1.6703591346740723
query result over DP: 595557.0
true query result: 600572
relative error: 0.008350372644745342

```

## Query

- q12 is a count query for l = 1
- q5 is a count query for l = 2
- q7 is a k-selection query for l = 2
- q18 is a k-selection query for l = 1