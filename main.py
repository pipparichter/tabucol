# This file is for actually testing the behavior of TabuCol. 

import matplotlib.pyplot as plt
import numpy as np
import math
import pandas as pd
import seaborn as sns
from testutils import *
from tabucol import TabuCol
from control import Control
from randomgraph import RandomGraph
from graph import Graph

# print(reproduce_hdw_table2())

df = pd.read_csv('./data.csv')
df = df[df['iters'] < 0]
fig, axes = plt.subplots(2)
for i, (algorithm, group) in enumerate(df.groupby('algorithm')):
    x, y = [], []
    for n, subgroup in group.groupby('n'):
        x.append(int(n))
        y.append(len(subgroup['iters']))
    axes[i].bar(x, y)
    # axes[i].set_ylim([0, 700])
    axes[i].set_title(str(algorithm))
plt.tight_layout()
plt.show()


# k = 3
# # See how well the TabuCol algorithm performs relative to the control according
# # to graph size. 
# df = pd.DataFrame(columns=['algorithm', 'k', 'n', 'p', 'iters'])
# for n in range(10, 100, 10):
#     # Edge-vertez ratio of around 2.2 corresponds to 2.2 * n edges, or p of
#     # around (2.2 * n) / (n choose 2)
#     p = (2.2 * n) / math.comb(n, 2)
#     graphs = generate_colorable_graphs(k, n, p, num=50)
#     for graph in graphs:
#         tc = TabuCol(graph, k)
#         # Following Hertz and de Werra... they use rep size of about 50 percent
#         # of vertex size (slightly more, in some instances. I will copy them and
#         # use T_size = 7. 
#         tc_result = tc.run(rep=int(n * 0.5), T_size=7, maxiters=10000)
#         
#         ctrl = Control(graph, k)
#         ctrl_result = ctrl.run(maxiters=10000)
# 
#         df = df.append({'algorithm':'ctrl', 'k':k, 'n':n, 'p':p,
#             'iters':ctrl_result}, ignore_index=True)
#         df = df.append({'algorithm':'tabucol', 'k':k, 'n':n, 'p':p,
#             'iters':tc_result}, ignore_index=True)
# df.to_csv('./data.csv')

# for k, ratio in zip([3, 4], [2.3, 3.6]):
#     n = 50
#     graphs = generate_colorable_graphs(k, n, int(n * ratio), num=100) * 5
# 
#     df, failures = optimize_T_size(k, graphs)
#     
#     fig = plt.figure()
#     ax = sns.stripplot(x='size', y='iters', data=df)
#     ax.set_title(f'TabuCol performance with varying Tabu list sizes\n k={k}, n={n}, ratio={ratio}')
#     fig.add_axes(ax)
#     fig.savefig(f'./{k}_{n}_{ratio}_performance.png')
#     ax.clear()
#     fig.clf()
#     
#     fig = plt.figure()
#     ax = plt.axes()
#     ax.bar(failures.keys(), failures.values())
#     ax.set_title(f'Number of Tabucol failures with varying Tabu list sizes\n k={k}, n={n}, ratio={ratio}')
#     ax.set_ylabel('number of failures')
#     ax.set_xlabel('tabu list size')
#     fig.add_axes(ax)
#     plt.savefig(f'./{k}_{n}_{ratio}_failures.png')
#     ax.clear()
#     fig.clf()

# for k, ratio in zip([3, 4, 5], [2.3, 3.6, 5.8]):
#     n = 50
#     graphs = generate_colorable_graphs(k, n, int(n * ratio), num=100)
# 
#     df, failures = T_A_effect_comparison(k, graphs)
#     
#     fig = plt.figure()
#     ax = sns.stripplot(x='mod', y='iters', data=df)
#     ax.set_title(f'Comparing effects of aspiration function and Tabu list\n k={k}, n={n}, ratio={ratio}')
#     fig.add_axes(ax)
#     fig.savefig(f'./T_A_effect_comparison_{k}_{n}_{ratio}_performance.png')
#     ax.clear()
#     fig.clf()
# 
#     fig = plt.figure()
#     ax = plt.axes()
#     ax.bar(failures.keys(), failures.values())
#     ax.set_title(f'Number of Tabucol failures with and without the T-list and A\n k={k}, n={n}, ratio={ratio}')
#     ax.set_ylabel('number of failures')
#     ax.set_xlabel('tabu list size')
#     ax.set_xticks(['control', 'no T', 'no A', 'no T or A'])
#     fig.add_axes(ax)
#     plt.savefig(f'./T_A_effect_comparison_{k}_{n}_{ratio}_failures.png')
#     ax.clear()
#     fig.clf()

# for k, ratio in zip([3, 4, 5], [2.3, 3.6, 5.8]):
#     n = 50
#     graphs = generate_colorable_graphs(k, n, int(n * ratio), num=100)
# 
#     groups, data = what_causes_failures(k, graphs)
#     
#     data = data.pivot('result', 'category', 'count')
#     ax = data.plot(kind='bar')
#     ax.set_ylabel('count')
#     ax.set_title(f'What causes TabuCol failures?\n k={k}, n={n}, ratio={ratio}')
# 
#     plt.savefig(f'./what_causes_falures_{k}_{n}_{ratio}.png')
#     plt.clf()
#     

