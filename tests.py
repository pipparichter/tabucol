# This file is for testing the functionality of the TabuCol and RandomGraph
# classes. 

from tabucol import TabuCol
from randomgraph import RandomGraph
from graph import Graph

from testgraphs import *

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


# TODO: Compare these values to those generated in Mathematica. 
def test_randomgraph_is_colorable(n, ratio, k, false=False):
    m = int(n * ratio)
    is_colorable = [RandomGraph(n, m).is_colorable(k, colorable=False) for i in range(100)]
    p = is_colorable.count(True) / 100
    print(f'n = {n}, |E|/|V| = {ratio} : {p} {k}-colorable.')




print('TEST: Does is_colorable work correctly?')
print('---------------------------------------')
# Test against all the test graphs. They all should be 3-colorable.
for G in [G1, G2, G3, G4, G5]:
    g = Graph(G)
    if not g.is_colorable(3):
        print('FAIL')
        break
    else:
        print('SUCCESS: Graph correctly identified as 3-colorable.')
