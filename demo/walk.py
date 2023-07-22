import networkx as nx 
import random

# コミュニティ内を walk_num 回 Random Walk
# 使い方　コミュニティ内のサブグラフを作成した後に使用
def random_walk(G, v, walk_num, v_walk_num_cnt):
    
    for i in range(walk_num + 1):
        if(v in v_walk_num_cnt):
            v_walk_num_cnt[v] += 1
        else:
            v_walk_num_cnt[v] = 1
            
        neighbors = list(G.neighbors(v))
        random_index = random.randrange(len(neighbors))
        v = neighbors[random_index]
    
    return v_walk_num_cnt


# 近似 PageRank

def pr_random_walk(G, v, walk_num, v_walk_num_cnt, d):
    
    node_list = list(G.nodes)
    
    for i in range(walk_num + 1):
        
        if(v in v_walk_num_cnt):
            v_walk_num_cnt[v] += 1
        else:
            v_walk_num_cnt[v] = 1
            
        r_value = random.random()
        
        if(r_value <= d):
            neighbors = list(G.neighbors(v))
            random_index = random.randrange(len(neighbors))
            v = neighbors[random_index]
        else:
            random_index = random.randrange(len(node_list))
            v = node_list[random_index]
    
    return v_walk_num_cnt
    
            
            
        
