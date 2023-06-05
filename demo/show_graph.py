import networkx as nx 
import matplotlib.pyplot as plt

# 元グラフ読み込み
graph_name = input("Enter graph name : ")
G = nx.read_edgelist(graph_name + ".txt" , nodetype=int)
print(G)

# グラフ表示
nx.draw(G, with_labels=True)
plt.savefig(graph_name + "_show.png")