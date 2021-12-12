import networkx as nx
import numpy as np
import bnlearn as bn
from model.bn import *
from graph.mincut import *
from graph.utils import *
from graph.graph import *

if __name__ == '__main__':
    # construct a nx digraph from edge_weight
    G = build_graph('./data/edge_weight.txt')
    # load dataset
    df = load_data('./data/insurance.csv')
    # define proxies, target, preserved vars, and queries
    # note that each query may be a list of sub-queries
    proxies = ['SocioEcon']
    target = 'PropCost'
    preserved = ['DrivingSkill']
    query0 = [{'evidences' : {'Age':0}, 'targets' : [target]},
              {'evidences' : {'Age':1}, 'targets' : [target]},
              {'evidences' : {'Age':2}, 'targets' : [target]},]
    
    query1 = [{'evidences' : {'SocioEcon':0, 'Age':0}, 'targets' : [target]},
              {'evidences' : {'SocioEcon':0, 'Age':1}, 'targets' : [target]},
              {'evidences' : {'SocioEcon':0, 'Age':2}, 'targets' : [target]},
              {'evidences' : {'SocioEcon':1, 'Age':0}, 'targets' : [target]},
              {'evidences' : {'SocioEcon':1, 'Age':1}, 'targets' : [target]},
              {'evidences' : {'SocioEcon':1, 'Age':2}, 'targets' : [target]},
              {'evidences' : {'SocioEcon':2, 'Age':0}, 'targets' : [target]},
              {'evidences' : {'SocioEcon':2, 'Age':1}, 'targets' : [target]},
              {'evidences' : {'SocioEcon':2, 'Age':2}, 'targets' : [target]},
              {'evidences' : {'SocioEcon':3, 'Age':0}, 'targets' : [target]},
              {'evidences' : {'SocioEcon':3, 'Age':1}, 'targets' : [target]},
              {'evidences' : {'SocioEcon':3, 'Age':2}, 'targets' : [target]}]
    
    query2 = [{'evidences' : {'DrivingSkill':0}, 'targets' : [target]},
              {'evidences' : {'DrivingSkill':1}, 'targets' : [target]},
              {'evidences' : {'DrivingSkill':2}, 'targets' : [target]},]
    query3 = [{'evidences' : {'CarValue':0}, 'targets' : [target]},
              {'evidences' : {'CarValue':1}, 'targets' : [target]},
              {'evidences' : {'CarValue':2}, 'targets' : [target]},
              {'evidences' : {'CarValue':3}, 'targets' : [target]},
              {'evidences' : {'CarValue':4}, 'targets' : [target]},]

    """
    # Part1: find the original BN's query results
    # build an original BN
    orig_model = build_bn(list(G.edges))
    # run parameter learning on original model
    orig_model = parameter_learning(orig_model,df)
    # run queries
    for q in query2:
        ans = inference(orig_model,q['evidences'],q['targets'])
    for q in query3:
        ans = inference(orig_model,q['evidences'],q['targets'])
        
    
    # Part2 : run mincut and parameter learning on a new model
    # find a mincut and remove edges from the original graph
    G1 = intervention(G,proxies)
    cut_value,cut_set = minimum_cut(G1, sources=proxies, target=target)
    print(cut_set)
    G2 = remove_edges(G,cut_set)
    # build a bn model
    model1 = build_bn(list(G2.edges))
    # parameter learning on model
    model1 = parameter_learning(model1,df)
    # run queries
    for q in query2:
        ans = inference(model1,q['evidences'],q['targets'])
    for q in query3:
        ans = inference(model1,q['evidences'],q['targets'])
    
    """
    
    # Part3: Approximation Algorithm with preserved variables
    G3 = preserve_paths(G,preserved,target)
    G3 = intervention(G3,proxies)
    cut_value,cut_set = minimum_cut(G3, sources=proxies, target=target)
    print(cut_value,cut_set)
    G4 = remove_edges(G,cut_set)
    # build a bn model
    model2 = build_bn(list(G4.edges))
    # parameter learning
    model2 = parameter_learning(model2,df)
    # run queries
    for q in query2:
        ans = inference(model2,q['evidences'],q['targets'])
    for q in query3:
        ans = inference(model2,q['evidences'],q['targets'])
    
