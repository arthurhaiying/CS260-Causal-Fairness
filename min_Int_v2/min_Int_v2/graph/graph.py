import networkx as nx
import numpy as np
from graph.spfa import *

INF = 0x7FFFFFFF

# remove a set of edges
def remove_edges(G,edge_set):
    nG = G.copy()
    nG.remove_edges_from(edge_set)
    return nG

# return a new graph with interventions
def intervention(G, proxies):
    edge_set = []
    for p in proxies:
        edge_set += list(G.in_edges(p))
    nG = remove_edges(G,edge_set)
    return nG


# return a new graph with preserved dependency paths
def preserve_paths(G, preserved, target):
    edge_set = []
    nG = G.copy()
    for v in preserved:
        cost,edges = spfa(G,v,target,tp='minmax')
        edge_set += edges
    for e in edge_set:
        nG[e[0]][e[1]]['capacity'] = INF
    return nG
