import igraph as ig
import random
import os
from plotly.offline import plot
import plotly
import plotly.graph_objs as go

def write_data(filename, n, edges, cent=None, w_s=None):
    if w_s is None:
        w_s = [1/2,]*len(edges)

    with open(filename, 'w') as f:
        f.seek(0)
        f.write(str(n)+' '+str(len(edges))+'\n')
        for i in range(2):
            for item in enumerate(edges):
                f.write(str(item[1][0])+' '+str(item[1][1])+' '+str(w_s[item[0]])+'\n')
        if cent:
            for i in range(2):
                for c in cent:
                    f.write(str(c)+'\n')

def read_data(filename):
    with open(filename, 'r') as f:
        f.seek(0)
        ans = f.readline()
        return float(ans)

def show_plot(_x, _y_s):
    data = [go.Scatter(x = _x, y = _y[1], name=_y[0]) for _y in _y_s]
    plot({"data": data, "layout": go.Layout(title="c(p)")}, auto_open=True)

def get_centralities(g, n, name):
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
        return [d/(m+1) for d in dg]
    elif name=="static":
        return [1/2,] * n
    elif name=="random":
        w_s = []
        for _ in range(n):
            w_s.append(round(random.random(), 3))

def get_random_weights(m):
    w_s = []
    for _ in range(m):
        w_s.append(round(random.random(), 3))

if __name__ == "__main__":
    random.seed(2)
    n = 100
    m_s = [m+2 for m in range(n-2)]
    res_s = []
    c_s = ["static", "random", "degree", "closeness", "betweenness", "pagerank"]
    for c in c_s:
        res = []
        for m in m_s:
            g = ig.Graph.Barabasi(n, m, outpref=True, directed=False)
            edges = g.get_edgelist()
            centralities = get_centralities(g, n, c)
#            w_s = get_random_weights(len(edges))
            w_s = g.similarity_jaccard(pairs=edges)
            write_data("ba.in", n, edges, centralities, w_s)
            os.system("./../model < ba.in > ba.out")
            res.append(read_data("ba.out"))
        res_s.append([c, res])
    show_plot(m_s, res_s)

