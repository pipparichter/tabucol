# This file is for testing the functionality of the TabuCol and RandomGraph
# classes. 
import random
import math
import itertools
import numpy as np
import pandas as pd

from tabucol import TabuCol
from randomgraph import RandomGraph
from graph import Graph, flatten, remove_duplicate_edges


def generate_uncolorable_graphs(k, n, m, num=100):
    '''
    Generate num graphs with n vertices and m edges which are not colorable by k colors. 

    Params
    ------
    n : int
        Positive integer indicating the number of vertices in the graphs. 
    m : int
        Positive integer indicating the number of edges in the graphs. 
    k : int
        Positive integer indicating the number of available colors 
    num : int
        Positive integer indicating the number of graphs to generate. Default is
        100 graphs. 
    '''
    if k > m:
        msg = 'Cannot have a K value greater than the specified number of edges.'
        raise ValueError(msg)

    graphs = []
    V = list(range(n)) # Generate a list of vertices. 

    for i in range(num):
        # In order to ensure a graph is not colorable by k colors, there must be
        # at least k fully-connected vertices. 
        E, sub_V = [], random.sample(V, k + 1)
        all_E = remove_duplicate_edges([(v, u) for v in V for u in V if u != v])
        
        for u, v in all_E:
            if u in sub_V and v in sub_V:
                E.append((u, v))
                all_E.remove((u, v))
        
        while len(E) < m:
            u, v = random.choice(all_E)
            E.append((u, v))
            all_E.remove((u, v))
        
        graphs.append(Graph(E, V=V))
    return graphs


def random_split(lst, k):
    '''
    Recursively splits a list into k random segments.
    '''
    if k <= 0:
        raise ValueError('k must be positive.')
    if k == 1:
        return [lst]
    else:
        # Max size of any individual chunk
        # max_size = len(lst) - k
        # NOTE: Should I be halving this? Only purpose is to make the splits
        # more evenly distributed. 
        max_size = math.ceil((len(lst) - k) / 2)
        idx = random.randint(1, max_size)
        
        random.shuffle(lst)
        l1, l2 = lst[:idx], lst[idx:]
        return [l1] + random_split(l2, k - 1)
        

def generate_colorable_graphs(k, n, m, num=100):
    '''
    Use the method used in the Mathematica notebooks to generate random graphs. 
    
    Params
    ------
    n : int
        Positive integer indicating the number of vertices in the graphs. 
    m : int
        Positive integer indicating the number of edges in the graphs. 
    k : int
        Positive integer indicating the number of available colors 
    num : int
        Positive integer indicating the number of graphs to generate. Default is
        100 graphs. 
    '''
    graphs = []
    while len(graphs) < num:
        g = RandomGraph(n, m)
        if g.is_colorable(k):
            print(f'{len(graphs)} out of {num} graphs generated.', end='\r')
            graphs.append(g)

    return graphs


def generate_colorable_graphs_petford_and_welsh(k, n, num=100, p=0.5):
    '''
    Uses the method described in Petford and Welsh to generate K-colorable
    graphs. 

    SOURCE : http://www.solipsys.co.uk/documents/RandomisedThreeColouring_Petford_Welsh.pdf 

    Params
    ------
    n : int
        Positive integer indicating the number of vertices in the graphs. 
    k : int
        Positive integer indicating the number of available colors 
    num : int
        Positive integer indicating the number of graphs to generate. Default is
        100 graphs. 
    p : float
        A number between 0 and 1, denotes the probability with which to form an
        edge between two vertices. 
    '''
    graphs = []
    V = list(range(n))
    
    for i in range(num):
        random.shuffle(V)
        
        # Choose k integers such that sum(k) = n. 
        K = map(sum, random_split([1]*n, k))
        # Use the integers to split up V.     
        idx, subsets = 0, []
        for inc in K:
            subsets.append(V[idx:idx + inc])
            idx += inc

        E = []
        # Need to look at every two subsets independently. 
        it = itertools.combinations(subsets, 2)
        for V1, V2 in it:
            # Sets are disjoint; no u == v. 
            edges = remove_duplicate_edges([(u, v) for u in V1 for v in V2])
            # Edges are drawn with probability p. So, select (p * len(edges)). 
            E += random.sample(edges, math.ceil(p * len(edges)))
        graphs.append(Graph(E, V=V))

    return graphs


def T_A_effect_comparison(k, graphs, T_size=10):
    '''
    Runs a series of trials to determine the effects of the Tabu list and
    Aspiration function on the performance of TabuCol. 
    '''
    # control, no T, no A, neither
    cats = ['control', 'no T', 'no A', 'no T or A', 'control']
    data = [[0], [0], [0], [0]]
    failures = [0, 0, 0, 0]
    mods = [{'T_on':True, 'A_on':True}, {'T_on':False, 'A_on':True},
            {'T_on':True, 'A_on':False}, {'T_on':False, 'A_on':False}]
    
    graphs = generate_colorable_graphs(k, n, int(ratio * n), num=num)
    
    for G in graphs:
        tc = TabuCol(G, k)
        for cat, mod in enumerate(mods):
            x = tc.run(T_size=T_size, **mod)
            if x == np.inf:
                failures[cat] += 1
            else:
                data[cat].append(x)
        i += 1 # Only increment if a colorable graph is produced. 
    
    df = pd.DataFrame(columns=['mod', 'iters'])
    for cat in cats:
        for x in data[cats.index(cat)]:
            df = df.append({'mod':cat, 'iters':x}, ignore_index=True)

    return (df, failures)


def optimize_T_size(k, graphs):
    '''
    Run a series of trials to determine the optimal size of the tabu list. 
    '''
    tabucols = [TabuCol(G, k) for G in graphs]
    
    sizes = list(range(1, n, 2))
    data = [[] for i in range(len(sizes))]
    failures = [0 for i in range(len(sizes))]
   
    for i, size in enumerate(sizes):
        for tc in tabucols:
            x = tc.run(T_size=size)
            if x < np.inf:
                data[i].append(x)
            else:
                failures[i] += 1

    df = pd.DataFrame(columns=['size', 'iters'])
    for size in sizes:
        for x in data[sizes.index(size)]:
            df = df.append({'size':size, 'iters':x}, ignore_index=True)

    return (df, failures)




