import igraph as ig
import random
import os
from plotly.offline import plot
import plotly
import plotly.graph_objs as go

def write_data(filename, n, edges):
    random.seed(2)
    with open(filename, 'w') as f:
        f.seek(0)
        f.write(str(n)+' '+str(len(edges))+'\n')
        for i in range(2):
            for item in edges:
                w = round(random.random(), 3)
                f.write(str(item[0])+' '+str(item[1])+' '+str(w)+'\n')

def read_data(filename):
    with open(filename, 'r') as f:
        f.seek(0)
        ans = f.readline()
        return float(ans)

def show_plot(_x, _y):
    plot({"data": [go.Scatter(x = _x, y = _y)], "layout": go.Layout(title="c_1/c_2")}, auto_open=True)

def get_centralities(g, name):
    if name=="pagerank":
        return g.pagerank()
    elif name=="betweenness":
        betw = g.betweenness()
        b_max = max(betw)
        betw_norm = [b/(b_max+1) for b in betw]
        return betw_norm
    elif name=="closeness":
        return g.closeness()
    elif name=="degree":
        dg = g.degree()
        m = max(dg)
        return [d/m for d in dg]
    elif name=="static":
        return [1/2,] * len(g.get_adjacency())
    elif name=="random":
        random.seed(2)
        w_s = []
        for _ in range(len(g.get_adjacency())):
            w_s.append(random.random(), 3)

if __name__ == "__main__":
    n = 5
    m_s = [m+2 for m in range(n-2)]
    res_s = []
    for m in m_s:
        g = ig.Graph.Barabasi(n, m, outpref=True, directed=False)
        edges = g.get_edgelist()
        centralities = get_centralities(g, "pagerank")
        write_data("barabasi_albert.in", n, edges, centralities)
        os.system("./../model < barabasi_albert.in > barabasi_albert.out")
        res_s.append(read_data("barabasi_albert.out"))
#    print(res_s)
    show_plot(m_s, res_s)
