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
- we use **postgreSQL** as the relational database.
- we use **cplex** for solving linear program.
- all the tables will be the same as **tpch**. 
  Typically in this implementation, we generate 100MB data for experiment.

## Dependencies

check requirement file in the repo.

- **psycopg2, config** for connecting database.
- **docplex, cplex** for solving linear program.
- **numpy** for calculation.
- **tqdm, matplotlib** for visualization.

## Usage

after setting up all the software, you need to prepare a file where you write your query.

Application options can be seen with:

```
python main.py --help
```

usage of arguments:

- **db**, filepath of database connect, default will be _database.ini_.
- **query**, filepath of query, default will be _q12_.
- **type**, type of the query (may be modified later), default will be _1_, corresponding to q12.
- **out**, filepath of the output which is a probability density, default will be _prob_density.png_.

Sample:

```
python main.py --db ./database.ini --q ./q12 --t 1 --out ./prob_density.png
```