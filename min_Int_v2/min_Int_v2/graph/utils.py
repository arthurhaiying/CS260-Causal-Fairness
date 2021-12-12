import numpy as np
import networkx as nx

def save_graph_edges(G,dire):
    with open(dire,'w') as fd:
        for e in G.edges:
            w = np.random.randint(0,100)
            fd.write(f'{e[0]} {e[1]} {w}\n')

def build_graph(dire):
    G = nx.DiGraph()
    with open(dire,'r') as fd:
        edges = fd.readlines()
    for e in edges:
        e = e.split(' ')
        G.add_edge(e[0],e[1],capacity=float(e[2]))
    return G
        
