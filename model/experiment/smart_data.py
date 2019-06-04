import igraph as ig
import random
import os
from plotly.offline import plot
import plotly
import plotly.graph_objs as go
from numpy.random import choice
from random import shuffle
import json

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
        ans0 = f.readline()
        ans1 = f.readline().split()
        return (float(ans0), ans1)

def show_plot(_x, _y_s):
    data = [go.Scatter(x = _x, y = _y[1], name=_y[0]) for _y in _y_s]
    plot({"data": data, "layout": go.Layout(title="c")}, auto_open=True)

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
        random.seed(2)
        w_s = []
        for _ in range(n):
            w_s.append(round(random.random(), 3))

def get_random_weights(m):
    w_s = []
    for _ in range(n):
        w_s.append(round(random.random(), 3))

def get_matrix(draw):
    for i in range(len(draw)):
        draw[i][i] = 0
    for i in range(1, len(draw)):
        for j in range(i):
            draw[i][j] = draw[j][i]
    return draw

def generate_sequence(n):
    graphs = []
    draw = choice([0, 1], p=[2/3, 1/3], size=(n, n))
    m = get_matrix(draw)
#    print(m)
    graphs.append(ig.Graph.Adjacency(m.tolist()))
    order = []
    for i in range(1, n):
        for j in range(i):
            if m[i][j] == 1:
                order.append((i, j))
    shuffle(order)
    for idx in order:
        m[idx[0], idx[1]] = 0
#        print(m)
        graphs.append(ig.Graph.Adjacency(m.tolist()))

    edgelists = [g.get_edgelist() for g in graphs]
    with open('saved.txt', 'w') as f:
        f.write(json.dumps(edgelists))

    return graphs

if __name__ == "__main__":
    n = 10
#    c_s = ["static", "random", "degree", "closeness", "betweenness", "pagerank"]
    c_s = ['static',]
    res_s = []
    to_write = []
    random.seed(2)
    graphs = generate_sequence(n)
    n_s = [i for i in range(len(graphs))]
    i = 0
    for c in c_s:
        res = []
        for g in graphs:
            edges = g.get_edgelist()
#            print(i, ' deleted:')
            i += 1
#            print(g.get_adjacency(), '\n\n')
            centralities = get_centralities(g, n, c)
            w_s = g.similarity_jaccard(pairs=edges)
            write_data("erdos_renyi.in", n, edges, cent=centralities, w_s=w_s)
            os.system("./../model < erdos_renyi.in > erdos_renyi.out")
            ans = read_data("erdos_renyi.out")
            res.append(ans[0])
            to_write.append(ans[1])
        res_s.append((c, res))

    with open('communities.txt', 'w') as f:
        f.write(json.dumps(to_write))
    show_plot(n_s, res_s)
#    print(res_s)
