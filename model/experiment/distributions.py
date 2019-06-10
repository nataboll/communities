import igraph as ig
import random
import os
from plotly.offline import plot
import plotly
import plotly.graph_objs as go
from numpy.random import choice
from random import shuffle
import numpy as np
from plotly import tools
import json

def show_hist(n, _y_1, _y_2, _y_3, _y_4):
    n1, n2, n3, n4 = n, n, n, n
    while _y_1[n1-1] == 0:
        n1 -= 1
    n1 = min(n, int(n1*3/2))
    while _y_2[n2-1] == 0:
        n2 -= 1
    n2 = min(n, int(n2*3/2))
    while _y_3[n3-1] == 0:
        n3 -= 1
    n3 = min(n, int(n3*3/2))
    while _y_4[n4-1] == 0:
        n4 -= 1
    n4 = min(n, int(n4*3/2))

    _x_1 = [i+1 for i in range(n1)]
    _x_2 = [i+1 for i in range(n2)]
    _x_3 = [i+1 for i in range(n3)]
    _x_4 = [i+1 for i in range(n4)]

    traces = []
    traces.append(go.Bar(x=_x_1, y=_y_1[:len(_x_1)]))
    traces.append(go.Bar(x=_x_2, y=_y_2[:len(_x_2)]))
    traces.append(go.Bar(x=_x_3, y=_y_3[:len(_x_3)]))
    traces.append(go.Bar(x=_x_4, y=_y_4[:len(_x_4)]))

    cols = 2
    rows = 2

    titles = []
    titles.append('undirected')
    titles.append('directed')
    titles.append('undirected')
    titles.append('directed')

    fig = tools.make_subplots(rows=rows, cols=cols, subplot_titles=titles)

    x = 1
    y = 1
    for trace in traces[:2]:
        fig.append_trace(trace, x, y)
        y += 1

    x = 2
    y = 1
    for trace in traces[2:]:
        fig.append_trace(trace, x, y)
        y += 1

    fig['layout'].update(height=400*rows, width=800, title='Clusters composition')
    plot(fig)

def get_composition(n, memb):
    comp = np.zeros(n)
    memb.sort()
    cur = memb[0]
    counter = 1

    for c in memb[1:]:
        if c==cur:
            counter += 1
        else:
            comp[counter-1] += 1
            counter = 1
            cur = c

    comp[counter-1] += 1
    return comp

def get_membership(filename):
    ans0, ans = 0, 0
    with open(filename, 'r') as f:
        f.seek(0)
        ans0 = f.readline()
        ans = f.readline().split()
        ans = [int(i) for i in ans]
    return (ans0, ans)

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

def write_results(filename, data):
    with open(filename, 'w') as f:
        f.write(json.dumps(data))


def get_hist(n):
    c_s = [1/2,]*n
    res = [[0,]*n, [0,]*n]
    res_num = [[0,]*n, [0,]*n]
    in_iter, out_iter = 1, 100

    for k in range(out_iter):
        graphs = generate_sequence(n)
        for i in range(2):
            g = graphs[i]
            edges = g.get_edgelist()
            w_s = [1/2,]*len(edges)
            write_data("erdos_renyi.in", n, edges, cent=c_s, w_s=w_s)

            for it in range(in_iter):
                os.system("./../model < erdos_renyi.in > membership.out")
                num, memb = get_membership('membership.out')
                to_add = get_composition(n, memb)

                for j in range(n):
                    res[i][j] += to_add[j]

                res_num[i][int(num)-1] += 1

    write_results('results.out', (res, res_num))

    res[0] = [r/(in_iter*out_iter*100) for r in res[0]]
    res[1] = [r/(in_iter*out_iter*100) for r in res[1]]
    res_num[0] = [r/(in_iter*out_iter) for r in res_num[0]]
    res_num[1] = [r/(in_iter*out_iter) for r in res_num[1]]
    show_hist(n, res[0], res[1], res_num[0], res_num[1])

def get_undir_matrix(draw):
    for i in range(len(draw)):
        draw[i][i] = 0
    for i in range(1, len(draw)):
        for j in range(i):
            draw[i][j] = draw[j][i]
    return draw

def get_dir_matrix(draw):
    for i in range(len(draw)):
        draw[i][i] = 0
    for i in range(1, len(draw)):
        for j in range(i):
            draw[i][j] = 0
    return draw

def generate_sequence(n):
    graphs = []
    draw = choice([0, 1], size=(n, n), p=(1/2, 1/2))

    m = get_undir_matrix(draw)
    g0 = ig.Graph.Adjacency(m.tolist())
    graphs.append(g0)

    m = get_dir_matrix(draw)
    g1 = ig.Graph.Adjacency(m.tolist())
    graphs.append(g1)

    return graphs

if __name__ == "__main__":
    n = 200
    random.seed(2)
    get_hist(n)

