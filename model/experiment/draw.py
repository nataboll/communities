import json
import networkx as nx
import matplotlib.pyplot as plt
import os

def get_matrices(storage_path):
    with open(storage_path, 'r') as f:
        raw_data = f.read()
        if raw_data:
            return json.loads(raw_data)
    return {}

if __name__=='__main__':
    os.system("rm graphs/*")
    os.system("python smart_data.py")
    storage_path = 'saved.txt'
    m_s = get_matrices(storage_path)
    c_s = get_matrices('communities.txt')
    for i, m in enumerate(m_s):
        G = nx.DiGraph()
        G.add_edges_from(m)
        color_map = [str(1/(int(c)**2+1)) for c in c_s[i]]
        plt.clf()
        nx.draw(G, node_color = color_map, with_labels = True, arrowstyle='->')
        plt.savefig(f"graphs/graph{i}.png", format="PNG")

