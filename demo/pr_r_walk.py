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

node_list = list(G.nodes)

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


# -------------- Random Walk ----------------

walk_num = 10000 *15 *16
v_walk_num_cnt = {}
index_list = []

random_index = random.randrange(len(node_list))
v = node_list[random_index]

v_walk_num_cnt =  pr_random_walk(G, v, walk_num, v_walk_num_cnt, 0.85)


# ------------- PageRank 演算 ------------------------
pr = nx.pagerank(G, alpha=0.85)
pr_sort = sorted(pr.items(), key=lambda x:x[1], reverse=True)

labels_data = []
for item in pr_sort:
    labels_data.append(item[0])

"""
for i in range(20):
    print("------------------")
    print("PR value : {}".format(pr[labels_data[i]]))
    print("wlak num : {}".format(v_walk_num_cnt[labels_data[i]]))
    print("------------------")
"""
    
# ------------- Plot ------------------------

# フォントを設定する。
rcp['font.family'] = 'sans-serif'
rcp['font.sans-serif'] = ['Hiragino Maru Gothic Pro', 'Yu Gothic', 'Meirio', 'Takao', 'IPAexGothic', 'IPAPGothic', 'VL PGothic', 'Noto Sans CJK JP']

# カラーマップを用意する。
cmap = plt.get_cmap("tab10")

# Figureを作成する。
fig = plt.figure()
# Axesを作成する。
ax = fig.add_subplot(111)

# Figureの解像度と色を設定する。
fig.set_dpi(150)
fig.set_facecolor("white")

# Axesのタイトルと色を設定する。
#ax.set_title("物品の所有率")
ax.set_facecolor("white")

# x軸とy軸のラベルを設定する。
ax.set_xlabel("node ID", fontsize=14)
ax.set_ylabel("walk nums", fontsize=14)

x = np.arange(len(labels_data))

com_label_size = []
for i in range((len(c_id))):
    com_label_size.append(len(c_id[i]))

com_label_size_sort = np.argsort(com_label_size)[::-1]
common_com_list = com_label_size_sort[:11]
small_com_list = com_label_size_sort[10:]

common_com_y = np.array([])
small_com_y = np.array([])
for id in labels_data:
    if(id_c[id] in common_com_list):
        if(id in v_walk_num_cnt):
            common_com_y = np.append(common_com_y, v_walk_num_cnt[id])
        else:
            common_com_y = np.append(common_com_y, 0)
    else:
        common_com_y = np.append(common_com_y, np.nan)
        
for id in labels_data:
    if(id_c[id] in small_com_list):
        if(id in v_walk_num_cnt):
            small_com_y = np.append(small_com_y, v_walk_num_cnt[id])
        else:
            small_com_y = np.append(small_com_y, 0)
    else:
        small_com_y = np.append(small_com_y, np.nan)


"""
y = []
for id in labels_data:
    if(id in v_walk_num_cnt):
        y.append(v_walk_num_cnt[id])
    else:
        y.append(0)
"""
        
# x軸の目盛の位置を設定する。
ax.xaxis.set_major_locator(mpl.ticker.FixedLocator(x))
# x軸の目盛のラベルを設定する。
#ax.xaxis.set_major_formatter(mpl.ticker.FixedFormatter(labels_data))
#ax.xaxis.set_visible(False)
ax.axes.xaxis.set_ticks([]) # x軸ラベル非表示

#ax.scatter(x, y)

ax.scatter(x, common_com_y, label="common community")
ax.scatter(x, small_com_y, label="small community")

#ax.set_xscale('log')
#ax.set_yscale('log')

plt.legend()
plt.show()
