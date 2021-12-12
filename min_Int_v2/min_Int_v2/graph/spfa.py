import networkx as nx
import numpy as np

INF = 0x7FFFFFFF
"""
 G a nx DiGraph
 s source node
 t destination node
 mod: 'minmax' or 'mean'
   'minmax': find a path that contains the least max edge value
   'mean' : find a path that has the least min value
"""
def spfa_minmax(G,s,t):
    d = {} # distance from s to t
    Q = [] # queue
    E = {} # save the path from s to t
    for n in G.nodes:
        d[n] = INF
        E[n] = []
    d[s] = 0
    Q.append(s)
    while len(Q) > 0:
        u = Q[0]
        Q.pop(0)

        for v in G.successors(u):
            if max(d[u],G[u][v]['capacity']) < d[v]:
                d[v] = max(d[u],G[u][v]['capacity'])
                E[v] = E[u].copy() + [(u,v)]
                if v not in Q:
                    Q.append(v)
        for v in G.predecessors(u):
            if max(d[u],G[v][u]['capacity']) < d[v]:
                d[v] = max(d[u],G[v][u]['capacity'])
                E[v] = E[u].copy() + [(v,u)]
                if v not in Q:
                    Q.append(v)                    
    return d[t],E[t]

def spfa_mean(G,s,t):
    d = {} # distance from s to t
    Q = [] # queue
    E = {} # save the path from s to t
    N = {} # number of nodes on a path
    for n in G.nodes:
        d[n] = INF
        E[n] = []
        N[n] = 1
    d[s] = 0
    Q.append(s)

    while len(Q) > 0:
        u = Q[0]
        Q.pop(0)
        for v in G.successors(u):
            if (d[u]*N[u] + G[u][v]['capacity']) < d[v] * (N[u]+1):
                d[v] = d[u]*N[u] + G[u][v]['capacity']
                N[v] = N[u] + 1
                E[v] = E[u].copy() + [(u,v)]
                if v not in Q:
                    Q.append(v)
        for v in G.predecessors(u):
            if (d[u]*N[u] + G[v][u]['capacity']) < d[v] * (N[u]+1):
                d[v] = d[u]*N[u] + G[v][u]['capacity']
                N[v] = N[u] + 1
                E[v] = E[u].copy() + [(v,u)]
                if v not in Q:
                    Q.append(v)
                    
    return d[t],E[t]

# only keep ancestors
def spfa(G,s,t,tp='minmax'):
    nG = G.copy()
    anc1 = nx.ancestors(nG,s)
    anc2 = nx.ancestors(nG,t)
    anc = anc1.union(anc2)
    anc.add(s)
    anc.add(t)
    nG.remove_nodes_from([x for x in G.nodes if x not in anc])
    # we make each new capacity of the edge be W-capacity
    W = 1e6
    for e in nG.edges:
        nG[e[0]][e[1]]['capacity'] = W - nG[e[0]][e[1]]['capacity']
    if tp == 'minmax':
        return spfa_minmax(nG,s,t)
    elif tp == 'mean':
        return spfa_mean(nG,s,t)
    return None
    
