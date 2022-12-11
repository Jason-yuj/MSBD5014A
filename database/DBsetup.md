# Dabasase Setup

## PostgreSQL

Assume you installed PostgreSQL successfully in your system.

Create a database named tpch, and connect to this database

```
postgres=# create database tpch;

CREATE DATABASE

postgres=# \c tpch 
```

## Schema

Create all the tables in the schema file in this directory.

## Data generation

You can download TPCH tools from [official website](https://www.tpc.org/tpc_documents_current_versions/current_specifications5.asp)

Or get dbgen from [GitHub](https://github.com/electrum/tpch-dbgen)

- **makefile.suite** Modify as the following
    ```
    CC =gcc
    #Current values for DATABASE are: INFORMIX, DB2, TDAT (Teradata)
                                SQLSERVER, SYBASE, ORACLE, VECTORWISE
    #Current values for MACHINE are:  ATT, DOS, HP, IBM, ICL, MVS,
                                    SGI, SUN, U2200, VMS, LINUX, WIN32
    #Current values for WORKLOAD are:  TPCH
    DATABASE= POSTGRESQL   # add PostgreSQL
    MACHINE = LINUX
    WORKLOAD = TPCH
  ```
  
- **tpcd.h**
  add the following:
```
      #ifdef POSTGRESQL <<<<<和makefile中的保持一致
      #define GEN_QUERY_PLAN  "EXPLAIN PLAN"
      #define START_TRAN      "SET TRANSACTION"
      #define END_TRAN        "COMMIT;"
      #define SET_OUTPUT      ""
      #define SET_ROWCOUNT    "LIMIT %d\n"
      #define SET_DBASE      ""
      #endif
```

- compile and generate data
    ```
  make -f makefile.suite
  
  ./dbgen -s 3
  ```

- we will get 8 table file whose extenstion will be **.tbl** 

## Copy Data

copy the data we generated to the table we created like the following for all 8 tables:

```
tpch=# \copy part from '/data/tbase/tpch/2.18.0_rc2/dbgen/part.tbl'with CSV DELIMITER '|';
```
## Primary key and foreign key

check key file in this directory

## Reference

We refer this [website](https://www.modb.pro/db/23243) for setting up
