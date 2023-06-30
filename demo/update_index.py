import networkx as nx 

# 読み込み
dataset_name = input("Enter the dataset name : ")
dataset_path = dataset_name + ".txt"
f = open(dataset_path, 'r')
lines = f.readlines()
f.close()

G = nx.Graph() # 無向グラフ生成
for line in lines :
    data = line.split()
    if data[0] == data[1] :
        continue
    G.add_edge(int(data[0]), int(data[1]))
    
#x = list(G.nodes)
#print(x)

original_id = list(G.nodes)
original_id.sort() # id を昇順にソート

# ノードID を変更
n = nx.number_of_nodes(G) # ノード数
new_id = [i for i in range(n)]
mapping = {k: v for k, v in zip(original_id, new_id)}
print(mapping)
G = nx.relabel_nodes(G, mapping)

x = list(G.nodes)
print(x)

# 変更したIDのグラフを出力
output_file = input("output graph name : ")
out_path = output_file + ".txt"
nx.write_edgelist(G, out_path, data=False)

# 隣接頂点取得 (ノード：3の隣接頂点)
#for x in G.neighbors(3):
    #print(x)







