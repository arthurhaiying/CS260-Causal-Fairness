from pysat.examples.rc2 import RC2
from pysat.formula import WCNF

from GraphUtils import find_all_dependence_paths, find_all_paths
from dnf2cnf import dnf2cnf
import GraphUtils




def allocate_variables(dag):
    # allocate one boolean variable for each edge
    # return name_to_vars: a dictionary from variable name to variable id
    count = 1
    name_to_vars = {}
    for u, neighbors in dag.adjacency.items():
        for v,w in neighbors:
            name = "x_%s_%s" %(u, v) 
            name_to_vars[name] = count
            count+=1
    return name_to_vars

def allocate_weights(dag, name_to_vars):
    weights = []
    for u, neighbors in dag.adjacency.items():
        for v,w in neighbors:
            # assign weight for each edge (u, v)
            name = "x_%s_%s" %(u, v) 
            var = name_to_vars[name]
            weights.append((var, w)) 
    return weights

def block_path(dag, path, name_to_vars, wcnf):
    # add clause for blocking path 
    clause = []
    for i in range(len(path)-1):
        # a path is blocked if one of its edges is not satisfied
        u, v = path[i], path[i+1]
        name = "x_%s_%s" %(u, v) 
        var = name_to_vars[name]
        clause.append(-var)

    wcnf.append(clause)

def open_path(dag, path, name_to_vars, dnf):
    # add clause for open path
    term = []
    for i in range(len(path)-1):
        # a path is open of all of its edges are satisfied
        u, v = path[i], path[i+1]
        name = "x_%s_%s" %(u, v) 
        var = None
        if name in name_to_vars.keys():
            var = name_to_vars[name]
        else: # reversed direction
            name2 = "x_%s_%s" %(v, u)
            var = name_to_vars[name2]

        term.append(var)
    
    dnf.append(term)

def block_direct_paths_from_proxy(dag, target, proxy, name_to_vars, wcnf):
    # block causal influence from P to Y
    paths = find_all_paths(dag, proxy, target)
    for path in paths:
        block_path(dag, path, name_to_vars, wcnf)

def preserve_dependency_from_variable(dag, target, reserve, name_to_vars, wcnf):
    # preserve dependency from X to Y
    depend_paths = find_all_dependence_paths(dag, reserve, target)
    dnf = []
    for path in depend_paths:
        # open at least one dependency path
        open_path(dag, path, name_to_vars, dnf)

    cnf = dnf2cnf(dnf) # convert open-path constraints dnf to cnf 
    for clause in cnf:
        wcnf.append(clause)
    


def compile(dag, target, proxy_vars, reserve_vars):
    '''
        compile an mininum-cost intervention problem in W-MAXSAT formula
        Argument:
            dag: weighted DAG
            proxy_vars: block all directed path from each proxy variable to target (after removing edges)
            reserve_vars: preserve dependency between each reserved variable and target (after removing edges) 
        Return:
            WCNF: weighted CNF for removing a set of edges with minmum cost
    '''

    wcnf = []
    # Step 1: allocate edge variables and weights
    name_to_vars = allocate_variables(dag)
    weights = allocate_weights(dag, name_to_vars)

    # Step 2: add contraints for blocking each proxy variable
    for proxy in proxy_vars:
        block_direct_paths_from_proxy(dag, target, proxy, name_to_vars, wcnf)

    # Step 3: add constraints for preserving dependence for each preserved variable
    for reserve in reserve_vars:
        preserve_dependency_from_variable(dag, target, reserve, name_to_vars, wcnf)

    return wcnf, weights, name_to_vars

def named_clause(clause, name_to_vars):
    l = []
    var_to_names = {v:k for k,v in name_to_vars.items()}
    for var in clause:
        if var < 0:
            var = -var
            name = var_to_names[var]
            l.append('~'+name)
        else:
            name = var_to_names[var]
            l.append(name)

    return l

def named_weights(weights, name_to_vars):
    l = []
    var_to_names = {v:k for k,v in name_to_vars.items()}
    for var,w in weights:
        l.append((var_to_names[var], w))
    return l





if __name__ == '__main__':
    print("Test Asia Network...")
    dag = GraphUtils.NetworkAsia()
    proxy = "smoke"
    target = "dysp"
    reserve = "xray"
    print("Target: {} Proxy: {} Preserved: {}".format(proxy, target, reserve))
    p_paths = find_all_paths(dag,proxy,target)
    u_paths = find_all_dependence_paths(dag,reserve,target)
    print("P-paths: ", p_paths)
    print("U-paths: ", u_paths)
    wcnf, weights, name_to_vars = compile(dag, target, [proxy], [reserve])
    print("Start printing CNF---------------------------------------------------")
    for clause in wcnf:
        clause = named_clause(clause, name_to_vars)
        print(clause)
    print("Finish CNF")
    print("Start printing weights------------------------------------------------")

    print("weights: ", named_weights(weights, name_to_vars))
    
    print("Solve wcnf-------------------------------------------------------------")
    wcnf2 = WCNF()
    for clause in wcnf:
        wcnf2.append(clause)
    for v,w in weights:
        wcnf2.append([v], weight=w)
    
    rc2 = RC2(wcnf2)
    model = rc2.compute()
    cost = rc2.cost
    print("model: {} cost: {}".format(model, cost))

    var_to_names = {v:k for k,v in name_to_vars.items()}
    remove_edges = []
    for var in model:
        if var < 0:
            var = -var
            edge = var_to_names[var]
            remove_edges.append(edge)

    print("Remove edges: {}".format(remove_edges)) # should be x_smoke_Lung, x_bronc_dysp
