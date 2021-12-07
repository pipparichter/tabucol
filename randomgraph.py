import random
import numpy as np
import networkx as nx
import matplotlib.pyplot as plt
import math 

def flatten(lol):
    '''
    Recursively flattens a 1-dimensional list. 
    '''
    flat = []
    for lst in lol:
        if type(lst) != list:
            return lol
        else:
            flat += flatten(lst)
    return flat


class RandomGraph():
    '''
    This class is designed to represent and generate random graphs, mimicking
    the Graph object in Mathematica. Note that this graph is not necessarily  
    '''
    def __init__(self, n, m):
        if m > math.comb(n, 2):
            msg = f'Number of edges specified must be fewer than {math.comb(n, 2)}'
            raise Exception(msg)

        self.edge_count = m
        self.vertex_count = n

        # Generate a list of vertices. 
        self.V = np.arange(1, n + 1)
        # Create a list of edges. Use a for loop to prevent duplication. 
        E = []
        possible_edges = flatten([(i, j) for i in self.V for j in self.V])
        for (i, j) in possible_edges: 
            if len(E) == m:
                break
            if ((i, j) not in E) and ((j, i) not in E) and j != i:
                E.append((i, j))
        self.E = E

    def __get_neighbors(self, v):
        '''
        Returns an array of vertices connected to v by an edge. 
        '''
        neighbors = []
        for e in self.E:
            if v in e:
                neighbors.append(e[0])
                neighbors.append(e[1])
        neighbors = list(set(neighbors))
        # Need this accomodation in case a vertex has no neighbors. 
        if len(neighbors) > 0:
            neighbors.remove(v)
        return neighbors

    def is_colorable(self, k):
        '''
        Checks to see if the Graph object is colorable with k colors. It does so
        by taking the greedy approach, which can be done in time O(|V|+|E|).
        This function ensures k >= 1.
        '''
        assert k >= 1
        highest_color_used = 0
        coloring = {}

        for v in self.V:
            # Get the colors of the neighbors which have already been colored. 
            neighbor_colors = [coloring[u] for u in self.__get_neighbors(v) if u in coloring]
            available = [color for color in range(k) if color not in neighbor_colors]
            
            if len(available) == 0:
                return False
            else:
                c = min(available)
                if c == highest_color_used:
                    coloring[v] = c + 1
                    highest_color_used = c + 1
                else:
                    coloring[v] = c

        return True
    
    def get_conflicting_edges(self, coloring):
        '''
        Returns an array of the edges whose two vertices are colored the same way,
        given the input coloring. The coloring is a dictionary, which maps each
        vertex to a color. 
        '''
        # Make sure there is a color assigned to each vertex.
        assert set(self.V) == set(coloring.keys())

        conflicts = np.array([])
        for e in self.E:
            u, v = e[0], e[1]
            # If this is true, then there is a conflict. 
            if coloring[u] == coloring[v]:
                conflicts = np.append(conflicts, e)
        return conflicts

    def get_conflicting_vertices(self, coloring):
        '''
        Returns an array of the vertices participating in a coloring conflict. 
        '''
        return np.ravel(np.unique(self.get_conflicting_edges(coloring)))


    def is_valid_coloring(self, coloring):
        '''
        Takes a dictionary as input, which maps each vertex in the graph to a
        color. Each color and vertex is assumed to be represented by an integer
        label. It returns a Boolean value, indicating whether or not the
        coloring is valid. 
        '''
        # If the number of conflicting edges is zero, the coloring is valid.
        if len(self.get_conflicting_edges(coloring)) == 0:
            return True
        else:
            return False


def plot_graph(G, coloring='black', cmap='tab20'):
    cmap = plt.get_cmap(cmap)
    # Initialize the graph using the list of edges. Any non-connected vertices
    # will be thrown out. If this is an issue, I can add things seperately. 
    G = nx.Graph(G.edges)
    nx.draw(G, cmap=cmap, node_color=coloring)
    plt.show()

