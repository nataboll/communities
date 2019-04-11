import igraph as ig
import random

def write_data(filename, n, edges):
    random.seed(2)
    with open(filename, 'w') as f:
        f.seek(0)
        f.write(str(n)+' '+str(len(edges))+'\n')
        for i in range(2):
            for item in edges:
                f.write(str(item[0])+' '+str(item[1])+' '+str(round(random.random(), 3))+'\n')

if __name__ == "__main__":
    n = 100
    p = 1/3
    g = ig.Graph.Erdos_Renyi(n, p, directed=False, loops=False)
    edges = g.get_edgelist()
    write_data("erdos_renyi.in", n, edges)
    print(g.betweenness())
