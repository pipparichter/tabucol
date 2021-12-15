import random
import numpy as np
import networkx as nx
import matplotlib.pyplot as plt
import math 

from graph import flatten, remove_duplicate_edges, Graph


class RandomGraph(Graph):
    '''
    This class is designed to represent and generate random graphs, mimicking
    the Graph object in Mathematica. Note that this graph is not necessarily  
    '''
    def __init__(self, n, m):
        '''

        '''
        if m > math.comb(n, 2):
            msg = f'Number of edges specified must be fewer than {math.comb(n, 2)}'
            raise Exception(msg)

        self.edge_count = m
        self.vertex_count = n
        # Generate a list of vertices. 
        self.V = list(range(n))

        # Select m random edges.
        possible_edges = flatten([(i, j) for i in self.V for j in self.V])
        possible_edges = remove_duplicate_edges(possible_edges)
        self.E = random.sample(possible_edges, m) 


