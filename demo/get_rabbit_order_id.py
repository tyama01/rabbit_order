import sys
import networkx as nx 


# rabbit_order id 取得
rabbit_order_id = []
with open('output_new_id.txt', 'r', encoding='utf-8') as fin:
    for line in fin.readlines():
        try:
            num = int(line)
        except ValueError as e:
            print(e, file=sys.stderr)
            continue

        rabbit_order_id.append(num)

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

original_id = list(G.nodes)
original_id.sort() # id を昇順にソート
    
mapping = {k: v for k, v in zip(original_id, rabbit_order_id)}
G = nx.relabel_nodes(G, mapping)


# 変更したIDのグラフを出力
output_file = input("output graph name : ")
out_path = output_file + ".txt"
nx.write_edgelist(G, out_path, data=False)
