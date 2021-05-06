import pandas as pd
import random
import math

import networkx as nx
from networkx.algorithms import bipartite

from timeit import default_timer as timer


df1 = pd.read_csv('data/rn_1k_n_100.csv')
df2 = pd.read_csv('data/1k_attribute.csv')

group = df2['protected attribute']

rankArray = {}
for i in range(0,1000):
    rankArray[i] = []

for  i in range(0,10):
    rArr = df1[str(i)]
    for j in range(0,len(rArr)):
        rankArray[j].append(rArr[j])


allMatch = []





import pandas as pd

object = pd.read_pickle(r'data/top25_dfs.pickle')

data = object[1]
num_of_player = 10
#data = data[0:num_of_player]
data = data.transpose()
players = data.keys()

itemList = data.keys()
G1 = []
G2 = []
row = data.iloc[25, :]
for i in range(0,num_of_player):
    if(row[i] == 0):
        G1.append(players[i])
    else:
        G2.append(players[i])

p1 = len(G1)/len(itemList)
p2 = len(G2)/len(itemList)


group = data.iloc[25, :]

playeridDic = {}
j = 0
for p in players :
    playeridDic[p] = j
    j = j + 1

start = timer()


for rankIds in range(1,25):

    rank = data.iloc[i, :10]
    ranktup = []
    j = 0
    for i in rank:
        ranktup.append((i, j))
        j = j + 1
    ranktup.sort()
    rank = []

    for i, j in ranktup:
        rank.append(j)



    rankGrp = {}
    for i in range(0,len(rank)):
        rankGrp[i] = row[i]




    numberOfItem = len(rank)
    numberOfGroup = 2

    #input






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
        r1 = math.floor(i*n/fp)
        r2 = math.ceil((i+1)*n/fp) - 1
        if r2 > numberOfItem:
            r2 = numberOfItem
        rankRange[item] = (r1,r2)


    B = nx.Graph()
    top_nodes = []
    bottom_nodes = []

    for i in rank:
        top_nodes.append(i)
        bottom_nodes.append(str(i))
    B.add_nodes_from(top_nodes, bipartite=0)
    B.add_nodes_from(bottom_nodes, bipartite=1)

    for i in rank:
        r1,r2 = rankRange[i]
        #print(r1,r2)
        for j in range(1,numberOfItem+1):
            if j >= r1 and j <= r2:
                #print(i,j)
                B.add_edge(i, str(j), weight = abs(i-j))
            else:
                B.add_edge(i, str(j), weight=1000000000)
                #print(i,j)

    my_matching = nx.algorithms.bipartite.minimum_weight_full_matching(B, top_nodes, "weight")
    allMatch.append(my_matching)
    #print(my_matching)



import itertools

items = []
for i in range(0,len(rank)):
    items.append(i)
combinations = [p for p in itertools.product(items, repeat=2)]

def KendallTau(P,Q,combinations):


    distance = 0
    for tup in combinations:
        if P[tup[0]] < P[tup[1]] and  Q[tup[1]] < Q[tup[0]]:
            distance = distance + 1
    return distance

minD = 10000000000
resRank = None
for rank1 in allMatch:
    d = 0
    for rank2 in allMatch:
        d = d + KendallTau(rank1, rank2, combinations)
    #print('ktau = ', d)
    if d < minD:
        minD = d
        resRank = rank1

print('min ktau = ', minD)
end = timer()
print('time required = ', end - start)


#print(resRank)