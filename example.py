from tabucol import TabuCol
from randomgraph import RandomGraph
import math 

k = 3
n = 10
m = 15


G = RandomGraph(n, m)
print(G.is_colorable(3))
# Check to make sure the randomly generated graph is colorable with k colors.
# Next, initialize a TabuCol object.

# NOTE: Probably should test out different values of rep and T_size. 

tc = TabuCol(G, k)
tc.run(maxiters=1000, remove_A=True)
tc.run(maxiters=1000, remove_A=False)
