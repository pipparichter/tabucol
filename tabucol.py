# The goal is to determine which features of the Tabu-Col algorithm are the
# most important for performance. 
import random
import numpy as np
import copy

from graph import Graph, flatten

def get_key(s):
    '''
    Takes a list of lists, which represents a state, as input, and converts it
    to a form to be used to index the A dictionary. 
    '''
    sorted_s = list(map(sorted, s))
    return str(s)

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

class TabuCol():
    def __init__(self, G, k):
        self.G = G
        self.k = k
  
    def __init_rep(self, rep):
        '''
        Initializes the value of rep, after passing it through several checks. If
        no rep value is given, it selects a default of approximately one-third
        of the vertex count. 
        '''
        if not rep:
            return int(self.G.vertex_count * 0.3)
        elif rep > self.G.vertex_count:
            msg = 'rep must be less than the number of vertices.'
            raise ValueError(msg)
        elif rep < 1:
            msg = 'rep must be a positive integer.'
            raise ValueError(msg)
        else:
            return rep
    
    def __init_s(self):
        '''
        Creates an initial state.
        '''
        s0 = [[] for i in range(self.k)]
        for v in self.G.V: # Add each vertex to a random coloring group.
            idx = random.randint(0, self.k - 1)
            s0[idx] += [v]
        return s0

    def __init_T(self, size):
        '''
        Initialize a random Tabu list of size T_size.

        Params
        ------
        size : int
            A positive integer indicating the number of elements in the Tabu
            list at any given time. 
        '''
        if not size:
            size = int(self.G.vertex_count * 0.3)
        elif size > self.G.vertex_count * self.k:
            msg = 'T_size must be less than the number of vertices.'
            raise ValueError(msg)
        elif size < 1:
            msg = 'T_size must be a positive integer.'
            raise ValueError(msg)
        vc_pairs = flatten([(v, c) for v in self.G.V for c in range(self.k)])
        return random.sample(vc_pairs, size)
     
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
    
    def update_A(self, s, s_prime):
        '''
        Update the value of the aspiration funtion for a given s and s_prime
        (i.e. a state and its neighbor). Note that this function assumes that
        the requirements for updating have been met, and throws an assertion
        error if otherwise. 

        Params
        ------
        s : list
            A list of lists representing the current state of the system. 
        s_prime : list
            A list of lists representing a neighboring state of s. 
        '''
        s_key = get_key(s)
        z = self.f(s)
        assert self.f(s_prime) <= self.A.get(s_key, z - 1)

        self.A[s_key] = self.f(s_prime) - 1

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
            colors = np.delete(np.arange(self.k), coloring[v])
            possible_moves += [(int(v), int(c)) for c in colors]
        return possible_moves


    def __get_moves(self, s, A_on, T_on):
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
        s_key = get_key(s)
        z = self.f(s)

        possible_moves = self.__get_possible_moves(s)
        random.shuffle(possible_moves)
        
        moves = []
        for move in possible_moves:

            if len(moves) == self.rep:
                break
            
            if T_on and A_on: # If the Tabu list is being used. 
                s_prime = apply_move(s, move)
                if move not in self.T:
                    moves.append(move)
                # Every time a state s_prime is generated which meets this
                # condition, update the value of the aspiration function. 
                elif (self.f(s_prime) <= self.A.get(s_key, z - 1)):
                    self.update_A(s, s_prime)
                    moves.append(move)
                    self.T.remove(move) # Drop tabu status of the move. 
           
            elif T_on and (not A_on):
                if move not in self.T:
                    moves.append(move)

            elif (not A_on) and (not T_on):
                moves.append(move)
        
        return moves
   
    def run(self, 
            maxiters=1000,
            T_size=None,
            rep=None,
            A_on=True, 
            T_on=True,
            select_best_move_on=True):
        '''
        Run the TabuCol algorithm on self.G for self.k colors.

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
        A_on : bool
            Boolean indicating whether or not to use the aspiration function in
            the algorithm. True by default. 
        T_on : bool
            Boolean indicating whether or not to use a Tabu list in the
            algorithm. True by default. 
        select_best_move_on : bool
            Boolean which can be used to disable the feature which selects the
            best move of the available moves in the system. True by default. 
        '''
        # Initialize all local variables and relevant attributes. 
        self.rep = self.__init_rep(rep)
        s = self.__init_s()
        self.A = {}
        self.T = self.__init_T(T_size)

        switches = (A_on, T_on)
        
        iters = 0
        while self.f(s) > 0 and iters < maxiters:
            print(f'{iters} TabuCol iterations completed.', end='\r')
            # Get a list of self.rep possible moves. 
            moves = self.__get_moves(s, *switches)
            if len(moves) == 0:
                # If no moves could be generated, the algorithm is stuck. 
                print('FAILURE: TabuCol was unable to generate any new moves.')
                return np.inf    

            g = lambda move : self.f(apply_move(s, move)) 

            if select_best_move_on:
                # Select the best move from the list of possible moves. 
                move = min(moves, key=g)
            else: 
                # Select a random move from the list of possible moves. 
                move = random.choice(moves)
            s = apply_move(s, move)

            # Update the Tabu list by adding the most recent move, and removing
            # the last move. 
            if T_on:
                self.T = [move] + self.T[:-1]
            
            iters += 1
        
        if iters >= maxiters:
            print(f'FAILURE: TabuCol was unable to find a solution within {maxiters} iterations.')
            return np.inf
        else:
            print(f'SUCCESS: TabuCol found a solution in {iters} iterations.')
            return iters
             


