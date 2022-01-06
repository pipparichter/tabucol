# The goal is to determine which features of the Tabu-Col algorithm are the
# most important for performance. 
import random
import numpy as np
import copy

from graph import Graph, flatten

def state_to_coloring(s):
    '''
    This function converts a Tabu-Col "state", represented as a list of lists of
    vertex labels, to a coloring dictionary.
    '''
    coloring = {}
    for (i, group) in enumerate(s):
        for v in group:
            coloring[v] = i
    return coloring

def apply_move(s, move):
    '''
    Take a move, represented by a vertex-coloring group pair, and applies it
    to a state. 
    '''
    s_prime = copy.deepcopy(s)
    v, c = move
    for group in s_prime:
        if v in group:
            group.remove(v)
    s_prime[c].append(v)
    return s_prime

class Control():
    def __init__(self, G, k):
        self.G = G
        self.k = k
     
    def __init_s(self):
        '''
        Creates an initial state.
        '''
        s0 = [[] for i in range(self.k)]
        for v in self.G.V: # Add each vertex to a random coloring group.
            idx = random.randint(0, self.k - 1)
            s0[idx] += [v]
        return s0
     
    def f(self, s):
        '''
        The objective function f of the Tabu-Col algorithm. It is defined as the
        number of edges for which both vertices are in the same coloring group. 
        
        Params
        -----
        state : list
            A list of lists representing the state of the system. 
        '''
        coloring = state_to_coloring(s)
        return len(self.G.get_conflicting_vertices(coloring))
    
    def __get_possible_moves(self, s):
        '''
        Generate a list of all moves from the current state, i.e. all moves
        which bring a conflicting vertex out of its current coloring group. 
        '''
        # First, get a list of all conflicting vertices.
        coloring = state_to_coloring(s)
        conflicting = self.G.get_conflicting_vertices(coloring)
        
        possible_moves = []
        for v in conflicting:
            possible_colors = np.delete(np.arange(self.k), coloring[v])
            possible_moves += [(v, c) for c in possible_colors]
        return possible_moves

    def __get_moves(self, s):
        '''
        Gets a list of valid moves, given the features which are turned on. 
 
        Params
        ------
        s : list
            The current state, represented as a list of lists. 
        A_on : bool
            Boolean indicating whether or not to make use of the aspiration
            function. 
        T_on : bool
            Boolean indicating whether or not to make use of the Tabu list. 
        '''
        # Get the key for the current state.
        z = self.f(s)
 
        possible_moves = self.__get_possible_moves(s)
        # Sometimes, possible_moves is smaller than rep. This accounts for that
        # case. 
        return random.sample(possible_moves, min(len(possible_moves), self.rep))
   
    def run(self, maxiters=1000, rep=10):
        '''
        Run the Control algorithm on self.G for self.k colors. Returns -1 if the
        algorithm gets stuck (no new moves can be generated), -2 if the maximum
        number of iterations is reached, and the number of iterations if the
        algorithm is successful. 
 
        Params
        ------
        maxiters : bool
            The number of iterations the algorithm will run through before
            exiting. 
        T_size : int
            The size of the Tabu list. If T_size > the number of possible moves,
            an error will be thrown. 
        rep : int
            The number of neighbors to consider at each iteration. 
        '''
        # Initialize all local variables and relevant attributes. 
        self.rep = rep
        s = self.__init_s()

        iters = 0
        while self.f(s) > 0 and iters < maxiters:
            print(f'{iters} Control iterations completed.', end='\r')
            # Get a list of self.rep possible moves. 
            moves = self.__get_moves(s)

            g = lambda move : self.f(apply_move(s, move)) 
            move = min(moves, key=g)
            s = apply_move(s, move)
            iters += 1
        
        if iters >= maxiters:
            print(f'FAILURE: Control was unable to find a solution within {maxiters} iterations.')
            return -2
        else:
            print(f'SUCCESS: Control found a solution in {iters} iterations.')
            return iters
             


