from typing import DefaultDict
import networkx as nx
import numpy as np

from collections import defaultdict

INFINITY = np.float32('inf')

class Edge:
    def __init__(self, u, v, weight=None):
        self.u = u
        self.v = v
        self.weight = weight

    def __repr__(self):
        return "Edge(u={},v={},w={})".format(self.u, self.v, self.weight)

class DAG:
    def __init__(self, name="dag"):
        self.name = name
        self.nodes = [] # node list
        self.adjacency = defaultdict(list) # an adjacency list (node -> list of neighbors) for DAG

    def add_node(self, node):
        self.nodes.append(node)

    def add_nodes_from(self, nodes):
        self.nodes.extend(list(nodes))
    
    def add_edges_from(self, edges):
        for edge in edges:
            u, v, weight = edge
            self.add_edge(u, v, weight)

    def add_edge(self, u, v, weight=None):
        if u not in self.nodes:
            self.nodes.append(u)
        if v not in self.nodes:
            self.nodes.append(v)
        edge = Edge(u, v, weight)
        self.adjacency[u].append(edge)




'''
Find minimum cut using NetworkX library
Arguments:
    dag: an DAG object with adjacency list
    sources: a list of proxy nodes
    target: target node
Return:
    cutset: a list of edges to be removed to block all directed paths from sources to target
    cut_value: the sum of weights of edges in cutset
'''
def minimum_cut(dag, sources, target):
    # create networkX graph G from dag
    G = nx.DiGraph()
    G.add_node('dummy') # add dummy source node
    for s in sources:
        G.add_edge('dummy', s, capacity=INFINITY)
        # connect dummy source to every proxy node
        # set infinite weight so that this edge cannot be cut through
    for node,edges in dag.adjacency.items():
        for edge in edges:
            G.add_edge(node, edge.v, capacity=edge.weight)
            # copy every edge from dag

    cut_value, partition = nx.minimum_cut(G, 'dummy', target)
    reachable, non_reachable = partition
    # find mininum cut

    cutset = []
    # retrieve every outgoing edges from the reachable set
    for node in reachable:
        if node == 'dummy':
            continue
        for edge in dag.adjacency[node]:
            if edge.v not in reachable:
                cutset.append(edge)

    return cut_value, cutset



if __name__ == '__main__':
    nodes = list(range(6))
    edges = [
        (0, 1, 16),
        (0, 2, 13),
        (1, 2, 10),
        (1, 3, 12),
        (3, 2, 9),
        (2, 4, 14),
        (4, 3, 7),
        (3, 5, 20),
        (4, 5, 4)
    ]

    dag = DAG('dag')
    dag.add_nodes_from(nodes)
    dag.add_edges_from(edges)
    cut_value, cut_edges = minimum_cut(dag, [0,1], 5)
    print("cut value: {}".format(cut_value))
    print("edges: {}".format(cut_edges))













