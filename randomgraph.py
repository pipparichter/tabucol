import random
import scipy.stats
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
    # NOTE: p is often a function of p, e.g. d/n for some value d. 
    def __init__(self, n, p):
        '''
        Generates a random graph with n vertices. The number of edges is
        determined by p, which is edge probability. 

        Uses the G(n, p) model introduced by Erdos and Renyi. 

        Params
        ------
        n : int
            Number of vertices in the random graph. 
        p : float
            Probability of an edge existing between any two vertices. 
        '''
        self.vertex_count = n
        # Generate a list of vertices. 
        self.V = list(range(n))

        # Select m random edges.
        possible_edges = flatten([(i, j) for i in self.V for j in self.V if i != j])
        possible_edges = remove_duplicate_edges(possible_edges)
       
        E = []
        for edge in possible_edges:
            # Draws a number form a normal distribution centered at 0.  
            rv = scipy.stats.uniform.rvs(size=1)[0]
            if rv < p: # Add an edge with a certain probability p. 
                E.append(edge)
        self.E = E
        self.edge_count = len(E)

