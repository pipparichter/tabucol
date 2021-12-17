# This file is for actually testing the behavior of TabuCol. 

import matplotlib.pyplot as plt
import numpy as np
import pandas as pd
import seaborn as sns

from testutils import *
from tabucol import TabuCol
from randomgraph import RandomGraph
from graph import Graph

ratio = 2.2
k = 3
n = 50

graphs = generate_colorable_graphs(3, 50, int(n * ratio))

df, failures = optimize_T_size(k, graphs)
ax = sns.stripplot(x='size', y='iters', data=df)
ax.set_title(f'TabuCol performance with varying Tabu list sizes\n k={k}, n={n}, ratio={ratio}')
plt.show()

# df, failures = A_T_effect_comparison(k, graphs)
# ax = sns.stripplot(x='size', y='iters', data=df)
# ax.set_title('Comparing effects of aspiration function and Tabu list\n k={k}, n={n}, ratio={ratio}')
# plt.show()
# print(failures)
