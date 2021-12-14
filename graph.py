import numpy as np
import itertools
# There is probably a better way to import this. 
import sys
sys.path.append('./PyMiniSolvers/')
import minisolvers

def flatten(lol):
    '''
    Recursively flattens a 1-dimensional list. 

    Params
    ------
    lol : list
        A list to flatten
    '''
    flat = []
    for lst in lol:
        if type(lst) != list:
            return lol
        else:
            flat += flatten(lst)
    return flat

class Graph:

    def __init__(self, E, V=None):
        
        # If no vertex list is specified, extract the list of vertices from E. 
        if V is None:
            self.V = list(set(flatten([list(t) for t in E])))
        else:
            self.V = V
        
        self.E = E
        self.vertex_count = len(self.V)
        self.edge_count = len(E)

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

    def coloring_to_sat(self, k):
        '''
        Converts a coloring problem into a K-Satisfiability problem. K-SAT formula
        should be in Conjunctive Normal form, a series of OR clauses joined by ands. 
        '''
        # Generate a list of vertex-color pairs, and map eacch to an integer. 
        # This is necessary, as minisolver uses integers.
        vc = flatten([(v, c) for v in self.V for c in range(k)])
        mapping = {pair:var for var, pair in enumerate(vc)}
        
        clauses = [[var for var in mapping.values()]]
        
        # For each edge (u, v), add a clause (not v or not u) for each color. 
        for u, v in self.E:
            for c in range(k):
                # The negative indicates a "not."
                clauses += [[-mapping[(u, c)], -mapping[(v, c)]]]

        return mapping, clauses


    def is_colorable(self, k):
        '''
        Checks to see if the Graph object is colorable with k colors. It uses
        the MiniSAT algorithm. 
        '''
        # Initialize the MiniSAT solver. 
        mapping, clauses = self.coloring_to_sat(k)
        S = minisolvers.MinisatSolver()

        for i in range(len(mapping)):
            S.new_var() # Add a new variable. 

        for clause in clauses:
            S.add_clause(clause)

        return S.solve()


#     def is_colorable(self, k):
#         '''
#         Checks to see if the Graph object is colorable with k colors. It does so
#         by taking the greedy approach, which can be done in time O(|V|+|E|).
#         This function ensures k >= 1.
#         '''
#         assert k >= 1
#         coloring = {}
# 
#         per = itertools.permutations(self.V)
#         
#         for permutation in per:
#             for v in permutation:
#                 # Get the colors of the neighbors which have already been colored. 
#                 neighbor_colors = [coloring[u] for u in self.__get_neighbors(v) if u in coloring]
#                 available = [color for color in range(k) if color not in neighbor_colors]
#                 if len(available) == 0:
#                     return False
#                 else:
#                     c = min(available)
#                     coloring[v] = c
# 
#         return True
    
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


