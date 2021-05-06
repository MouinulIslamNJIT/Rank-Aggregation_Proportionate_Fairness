import pandas as pd
import random
import math

import networkx as nx
import networkx as nx
from networkx.algorithms import bipartite
import random
import math


df = pd.read_csv('data/movielens_single_v2.csv')
allGenre = []
group = []
genre = df['genre']
movieId  = df['movieId']
score =  df['score']

allGenre = []
allgroup = []
for g in genre:
    if g not in allGenre:
        allGenre.append(g)
    allgroup.append(allGenre.index(g))



rankScore = []
for i in range(0,len(movieId)):
    rankScore.append((score[i],movieId[i],allgroup[i]))

rankScore.sort(reverse=True)

movieIdDic = {}
rank = []
i = 1
group = []
for item in rankScore:
    rank.append(i)
    group.append(item[2])
    movieIdDic[item[1]] = i
    i = i + 1


rank = rank[0:35]
group = group[0:35]


numberOfItem = len(rank)

rankGrp = {}
for i in range(0, len(rank)):
    rankGrp[rank[i]] = group[i]

grpCount = {}
for i in group:
    grpCount[i] = 0

rankGrpPos = {}
for i in rank:
    grpCount[rankGrp[i]] = grpCount[rankGrp[i]] + 1
    rankGrpPos[i] = grpCount[rankGrp[i]]

rankRange = {}
for item in rank:
    i = rankGrpPos[item]
    n = numberOfItem
    fp = grpCount[rankGrp[item]]
    r1 = math.floor((i-1) * n / fp)+1
    r2 = math.ceil(i * n / fp)
    if r2 > numberOfItem:
        r2 = numberOfItem
    rankRange[item] = (r1, r2)

B = nx.Graph()
top_nodes = []
bottom_nodes = []

for i in rank:
    top_nodes.append(i)
    bottom_nodes.append(str(i))
B.add_nodes_from(top_nodes, bipartite=0)
B.add_nodes_from(bottom_nodes, bipartite=1)

for i in rank:
    r1, r2 = rankRange[i]
    # print(r1,r2)
    for j in range(1, numberOfItem + 1):
        if j >= r1 and j <= r2:
            # print(i,j)
            B.add_edge(i, str(j), weight=abs(i - j))
        else:
            B.add_edge(i, str(j), weight=100000000000)
            # print(i,j)

my_matching = nx.algorithms.bipartite.minimum_weight_full_matching(B, top_nodes, "weight")

print(my_matching)
