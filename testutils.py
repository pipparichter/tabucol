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
    cats = ['control', 'no T', 'no A', 'no T or A']
    data = [[0] for i in range(len(cats))]
    failures = {cat:0 for cat in cats}

    mods = [{'T_on':True, 'A_on':True}, {'T_on':False, 'A_on':True},
            {'T_on':True, 'A_on':False}, {'T_on':False, 'A_on':False}]
    
    for G in graphs:
        tc = TabuCol(G, k)
        for idx, cat in enumerate(cats):
            x = tc.run(T_size=T_size, **mods[idx])
            if x >= 0:
                data[idx].append(x)
            else:
                failures[cat] += 1
    
    df = pd.DataFrame(columns=['mod', 'iters'])
    for cat in cats:
        for x in data[cats.index(cat)]:
            df = df.append({'mod':cat, 'iters':x}, ignore_index=True)

    return (df, failures)


def optimize_T_size(k, graphs):
    '''
    Run a series of trials to determine the optimal size of the tabu list. 
    '''
    n = graphs[0].vertex_count
    tabucols = [TabuCol(G, k) for G in graphs]
    
    sizes = list(range(5, n * k, 5))
    data = [[] for i in range(len(sizes))]
    failures = {size:0 for size in sizes}
   
    for i, size in enumerate(sizes):
        for tc in tabucols:
            x = tc.run(T_size=size)
            if x >= 0:
                data[i].append(x)
            else:
                failures[size] += 1

    df = pd.DataFrame(columns=['size', 'iters'])
    for size in sizes:
        for x in data[sizes.index(size)]:
            df = df.append({'size':size, 'iters':x}, ignore_index=True)

    return (df, failures)


def what_causes_failures(k, graphs):
    '''
    Applies a certain modification to the TabuCol system: control (both the tabu
    list and the aspiration function are used), no tabu-list, no aspiration
    function, or neither. It then parses what causes failures, when a failure
    occurs (either maximum number of iterations is exceeded, or the algorithm
    gets stuck).

    Returns a DataFrame with the relevant information. 

    Params
    ------
    k : int
        K value, the number of colors to use in the coloring problem. 
    graphs: list
        A list of graph.Graph objects to which the TabuCol algorithm will be
        applied. 
    cat : str
        One of control, no T, no A, or no T or A. Refers to the modification
        which will be made to the TabuCol algorithm. 
    '''
    tabucols = [TabuCol(graph, k) for graph in graphs]
    cats = ['control', 'no T', 'no A', 'no T or A']
    results = ['maxiters', 'stuck', 'success']
    # Setting up the DataFrame.
    data = pd.DataFrame({'category':flatten([[cat]*len(results) for cat in cats]), 
        'result':results*len(cats), 
        'count':[0]*len(cats)*len(results)})

    mods = [{'T_on':True, 'A_on':True}, {'T_on':False, 'A_on':True},
            {'T_on':True, 'A_on':False}, {'T_on':False, 'A_on':False}]
    
    for cat, mod in zip(cats, mods):
        for tc in tabucols:
            result = tc.run(**mod)
            
            if result == -1:
                data.loc[((data['category'] == cat) & (data['result'] == 'stuck')), 'count'] += 1
            elif result == -2:
                data.loc[((data['category'] == cat) & (data['result'] == 'maxiters')), 'count'] += 1
            else:
                data.loc[((data['category'] == cat) & (data['result'] == 'success')), 'count'] += 1
    
    return (cats, data)
