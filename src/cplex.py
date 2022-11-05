from docplex.mp.model import Model

if __name__ == '__main__':
    opt_mod = Model(name="Simple Program")
    x = opt_mod.continuous_var(name="x", lb=0)
    y = opt_mod.continuous_var(name="y", lb=0)
    c1 = opt_mod.add_constraint(x+y >= 8, ctname="c1")
    c2 = opt_mod.add_constraint(2*x + y >= 10, ctname="c2")
    c2 = opt_mod.add_constraint(x + 4*y >= 11, ctname="c3")
    obj_fn = 5*x + 4*y
    opt_mod.set_objective('min', obj_fn)
    opt_mod.print_information()

    opt_mod.solve()
    opt_mod.print_solution()
