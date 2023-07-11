import networkx as nx
import numpy as np
import matplotlib.pyplot as plt
import matplotlib as mpl
from scipy.stats import linregress
from matplotlib import rcParams as rcp
import random
from walk import *

 

# -------------- データ読み込み ------------------
dataset_name = input("Enter the dataset name : ")
dataset_path = "../datasets/" + dataset_name
f = open(dataset_path + ".txt", 'r')
lines = f.readlines()
f.close()

G = nx.Graph() # 無向グラフ生成
for line in lines :
    data = line.split()
    if data[0] == data[1] :
        continue
    G.add_edge(int(data[0]), int(data[1]))
    
print(G) # 無向グラフ情報出力

f = open(dataset_path + "_louvain.txt", 'r')
lines = f.readlines()
f.close()

c_id = {} # {所属するコミュニティ：頂点idのリスト}
id_c = {} # {頂点id:所属するコミュニティ}
for line in lines :
    data = line.split()
    c_id.setdefault(int(data[0]), []).append(int(data[1]))
    id_c[int(data[1])] = int(data[0])
    
print("community_num : " + str(len(c_id))) # コミュニティ数出力

# ------------- PageRank 演算 ------------------------
pr = nx.pagerank(G, alpha=0.85)
pr_sort = sorted(pr.items(), key=lambda x:x[1], reverse=True)

x = []
for item in pr_sort:
    x.append(item[0])

print("-------PageRank---------")
c = 0
for id in x:
    print(pr[id])
    c += 1
    
    if c > 15 :
        break