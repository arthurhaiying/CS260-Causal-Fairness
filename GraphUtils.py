from operator import truediv
from typing import DefaultDict
import networkx as nx
import numpy as np

from collections import defaultdict
import itertools as iter

class DAG:
    def __init__(self, name="dag"):
        self.name = name
        self.adjacency = defaultdict(list) # an adjacency dict node -> (node, weight)

    def add_node(self, node):
        self.adjacency[node] = []

    def add_edge(self, u, v, weight=None):
        self.adjacency[u].append((v, weight))
    
    def add_edges_from(self, edges):
        for edge in edges:
            self.add_edge(*edge)

    def is_neighbor(self, u1, u2):
        for v,_ in self.adjacency[u1]:
            if v == u2:
                return True
        return False




def find_all_paths(dag, src, dst):
    '''
        Find all simple paths from source to destination
    '''
    result = []
    find_all_paths_rec(dag, src, dst, [], result)
    return result

def find_all_paths_rec(dag, u, dst, path, result):
    # run dfs from node u
    if u == dst:
        result.append(path+[dst])
        return
    path2 = path+[u]
    for v,w in dag.adjacency[u]:
        if v not in path:
            # if neighbor is not visited in current path upto u
            find_all_paths_rec(dag, v, dst, path2, result)

def find_all_dependence_paths(dag, src, dst):
    '''
        Find all dependency path from src to dst
        A dependency path is an undirected path that does not contain A -> B <- C (convergent structure)
    '''
    G = DAG() 
    for u,neighbors in dag.adjacency.items():
        for v,w in neighbors:
            G.add_edge(u,v,weight=w)
            G.add_edge(v,u,weight=w)
            # undirected graph

    paths = find_all_paths(G, src, dst)
    paths = list(filter(lambda x:check_dependence_path(dag, x), paths))
    return paths


def check_dependence_path(dag, path):
    # check if the undirected path contains A -> B <- C (convergent structure)
    indices = [] 
    for i in range(len(path)-1):
        u, v = path[i], path[i+1]
        if dag.is_neighbor(u, v) and not dag.is_neighbor(v, u):
            indices.append(1) # left
        elif dag.is_neighbor(v, u) and not dag.is_neighbor(u, v):
            indices.append(-1) # right
        else:
            raise ValueError("dag is not directed?")

    for i in range(len(indices)-1):
        if indices[i] == 1 and indices[i+1] == -1:
            # find convergent structure
            return False

    return True

def NetworkAsia():
    G = DAG()
    G.add_edge("asia","tub",1)
    G.add_edge("tub","either",1)
    G.add_edge("either","xray",1)
    G.add_edge("smoke","lung",1)
    G.add_edge("lung","either",2)
    G.add_edge("smoke","bronc",3)
    G.add_edge("either","dysp",1)
    G.add_edge("bronc","dysp",2)
    return G

def NetWorkSachs():
    G = DAG()
    G.add_edge("PKC","PKA")
    G.add_edge("PKC","Raf")
    G.add_edge("PKC","Mek")
    G.add_edge("PKC","Jnk")
    G.add_edge("PKC","P38")

    G.add_edge("PKA","Raf")
    G.add_edge("PKA","Mek")
    G.add_edge("PKA","Erk")
    G.add_edge("PKA","Akt")
    G.add_edge("PKA","Jnk")
    G.add_edge("PKA","P38")

    G.add_edge("Raf","Mek")
    G.add_edge("Mek","Erk")
    G.add_edge("Erk","Akt")
    return G

def NetWorkAlarm():
    G = DAG()
    G.add_edge("PMB","PAP")
    G.add_edge("PMB","SHNT")
    G.add_edge("MVS","VMCH")
    G.add_edge("VMCH","VTUB")
    G.add_edge("DISC","VTUB")
    G.add_edge("VTUB","PRSS")
    G.add_edge("VTUB","VLNG")
    G.add_edge("KINK","PRSS")
    G.add_edge("KINK","VLNG")
    G.add_edge("INT","SHNT")
    G.add_edge("INT","MINV")
    G.add_edge("INT","VALV")
    G.add_edge("INT","VLNG")
    G.add_edge("INT","PRSS")
    G.add_edge("VLNG","MINV")
    G.add_edge("VLNG","VALV")
    G.add_edge("VLNG","ECO2")
    G.add_edge("FIO2","PVS")
    G.add_edge("VALV","PVS")
    G.add_edge("VALV","ACO2")
    G.add_edge("SHNT","SAO2")
    G.add_edge("PVS","SAO2")
    G.add_edge("SAO2","CCHL")
    G.add_edge("ACO2","CCHL")
    G.add_edge("ACO2","ECO2")
    G.add_edge("ANES","CCHL")
    G.add_edge("APL","TPR")
    G.add_edge("TPR","BP")
    G.add_edge("TPR","CCHL")
    G.add_edge("CCHL","HR")
    G.add_edge("LVF","HIST")
    G.add_edge("LVF","LVV")
    G.add_edge("LVF","STKV")
    G.add_edge("HYP","LVV")
    G.add_edge("HYP","STKV")
    G.add_edge("LVV","CVP")
    G.add_edge("LVV","PCWP")
    G.add_edge("ERLO","HRBP")
    G.add_edge("STKV","CO")
    G.add_edge("HR","HRBP")
    G.add_edge("HR","CO")
    G.add_edge("HR","HRSA")
    G.add_edge("HR","HREK")
    G.add_edge("ERCA","HREK")
    G.add_edge("CO","BP")
    return G


        
        

        





if __name__ == '__main__':
    G = DAG()
    G.add_edge(0,1)
    G.add_edge(0,2)
    G.add_edge(0,3)
    G.add_edge(1,3)
    G.add_edge(2,1)
    G.add_edge(2,0)
    paths = find_all_paths(G, 2, 3)
    for path in paths:
        print("path: {}".format(path))

    dag = NetworkAsia()
    proxy = "smoke"
    target = "dysp"
    reserve = "xray"
    p_paths = find_all_paths(dag,proxy,target)
    u_paths = find_all_dependence_paths(dag,reserve,target)
    print("P-paths: ", p_paths)
    print("U-paths: ", u_paths)
    reserve2 = "asia"
    print("U-paths: ", find_all_dependence_paths(dag,reserve2,target))


'''>>> from pysat.examples.rc2 import RC2
>>> from pysat.formula import WCNF
>>>
>>> wcnf = WCNF()
>>> wcnf.append([-1, -2])  # adding hard clauses
>>> wcnf.append([-1, -3])
>>>
>>> wcnf.append([1], weight=1)  # adding soft clauses
>>> wcnf.append([2], weight=1)
>>> wcnf.append([3], weight=1)
>>>
>>> with RC2(wcnf) as rc2:
...     rc2.compute()  # solving the MaxSAT problem
[-1, 2, 3]
...     print(rc2.cost)
1
...     rc2.add_clause([-2, -3])  # adding one more hard clause
...     rc2.compute()  # computing another model
[-1, -2, 3]
...     print(rc2.cost)
2
'''


