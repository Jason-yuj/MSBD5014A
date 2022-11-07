import docplex
from docplex.mp.model import Model
import re
import math


def LpSolver(user_set, value, j):
    mod = Model(name="Linear Program")
    # variables for users
    users = {}
    # variables for user sets
    s = {}
    # objective function
    obj_fn = 0
    # constraint
    t = 0
    for i in range(len(user_set)):
        su, cu = re.findall(r'\d+', user_set[i])
        xname = "x{0}".format(i)
        supp = "s{0}".format(su)
        cust = "c{0}".format(cu)
        s[xname] = mod.continuous_var(name=xname, lb=0, ub=1)
        if supp not in users.keys():
            users[supp] = mod.continuous_var(name=supp, lb=0, ub=1)
        if cust not in users.keys():
            users[cust] = mod.continuous_var(name=cust, lb=0, ub=1)
        mod.add_constraint(users[supp] + users[cust] >= s[xname])
        obj_fn += (1-s[xname])*value[i]

    for k in users.keys():
        t += users[k]

    mod.add_constraint(t <= j)
    mod.set_objective('min', obj_fn)
    mod.solve()
    # only need int
    return math.ceil(mod.objective_value)

# this part is for testing
if __name__ == '__main__':
    opt_mod = Model(name="Simple Program")
    x = opt_mod.continuous_var(name="x", lb=0)
    y = opt_mod.continuous_var(name="y", lb=0)
    c1 = opt_mod.add_constraint(x + y >= 8, ctname="c1")
    c2 = opt_mod.add_constraint(2 * x + y >= 10, ctname="c2")
    c2 = opt_mod.add_constraint(x + 4 * y >= 11, ctname="c3")
    obj_fn = 5 * x + 4 * y
    opt_mod.set_objective('min', obj_fn)

    opt_mod.solve()
    print(opt_mod.objective_value)
    print(docplex.version)

