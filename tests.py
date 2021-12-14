# This file is for testing the functionality of the TabuCol and RandomGraph
# classes. 
import random
import math
import itertools

from tabucol import TabuCol
from randomgraph import RandomGraph
from graph import Graph, flatten, remove_duplicate_edges

# TODO Things to test
# RandomGraph correctly generates random graphs 
# The is_colorable function is working correctly
# The is_valid_coloring function is working correctly
#   (write the visualizer for this)
# TabuCol is spitting out valid colorings, and failing to find valid colorings
# when none exist. 

# What are some edge cases?
# Graphs of size 1
# Big graphs (maybe size 100? 500?)
# Graphs with no edges
# Fully-connected graphs. 


# First, test RandomGraph. 

# Make sure RandomGraph is actually generating random graphs.
def test_randomgraph_is_random():
    n, m = 50, 75
    fail = False
    for i in range(100):
        G1 = RandomGraph(n, m)
        G2 = RandomGraph(n, m)

        shared = []
        for (u, v) in G1.E:
            if (u, v) in G2.E or (v, u) in G2.E:
                shared.append((u, v))
        if len(shared) == m:
           return False 
    return True

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
        
# Tested this in mathematica; seems to be working. 
def generate_colorable_graphs(k, n, num=100, p=0.5):
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
        for u, v in E:
            print('{'+str(u)+','+str(v)+'}', end=',')
        graphs.append(Graph(E, V=V))

    return graphs



