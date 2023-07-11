import networkx as nx
import numpy as np
import matplotlib.pyplot as plt
import matplotlib as mpl
from scipy.stats import linregress
from matplotlib import rcParams as rcp

 

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

# ----------------- コミュニティグラフ生成  -------------------------
#x = list(G.neighbors(0))
#print(len(x))

c_edge = {} # {(コミュニティ間のつながり)：エッジ数}
for c_num in range(len(c_id)):
    c_num_size = len(c_id[c_num])
    for i in range(c_num_size):
        neigbors = list(G.neighbors(c_id[c_num][i]))
        for j in range(len(neigbors)):
            if(id_c[j] == c_num):
                continue
            
            key = (c_num, id_c[j])
            if(key in c_edge):
                c_edge[key] += 1
            else:
                c_edge[key] = 1
                

print(len(c_edge))

c_edge_key = list(c_edge.keys())

c_G = nx.Graph()
for e in c_edge_key:
    c_G.add_edge(e[0], e[1])
                
print(c_G)
#print(nx.is_connected(c_G)) # 連結かどうか

# -------------------- Analysis Plot------------------------------

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
ax.set_xlabel("community labels", fontsize=14)
ax.set_ylabel("community size (num of nodes)", fontsize=14)

# x軸の目盛のラベルの位置を変数xで保持する。
y = []
for i in range(len(c_id)):
    y.append(len(c_id[i]))

z = np.sort(y)[::-1]
labels_data = np.argsort(y)[::-1]
x = np.arange(len(labels_data))

# x軸の目盛の位置を設定する。
ax.xaxis.set_major_locator(mpl.ticker.FixedLocator(x))
# x軸の目盛のラベルを設定する。
ax.xaxis.set_major_formatter(mpl.ticker.FixedFormatter(labels_data))

x1 = x[:11]
x2 = x[10:]
        
z1 = z[:11]
z2 = z[10:]

bar1 = ax.bar(x1, z1, label="common community")
bar2 = ax.bar(x2, z2, label="small community")
        
plt.legend()
plt.show()

