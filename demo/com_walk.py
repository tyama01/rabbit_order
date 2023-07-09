import networkx as nx
import numpy as np
import matplotlib.pyplot as plt
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

# -------------- コミュニティ内で Random Walk ----------------

com_walk_list = []
walk_num = 10000
for com_label in range(len(c_id)):
    c_nodes = c_id[com_label]
    H = G.subgraph(c_nodes)
    v_walk_num_cnt = {}
    index_list = []
    c = 0
    while(c < 15):
        random_index = random.randrange(len(c_nodes))
        
        if(random_index in index_list):
            continue
        
        index_list.append(random_index)
        
        v = c_nodes[random_index]
        v_walk_num_cnt = random_walk(H, v, walk_num, v_walk_num_cnt)
        
        c += 1
        
    com_walk_list.append(v_walk_num_cnt)
    
print(len(com_walk_list))