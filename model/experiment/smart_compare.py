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

def show_plot(_x, _y_s, subject='clusters_num'):
    data = [go.Scatter(x = _x, y = _y[1], name='Natasha, '+_y[0]) for _y in _y_s]
    data += [go.Scatter(x = _x, y = _y[2], name='Newman, '+_y[0]) for _y in _y_s]
    data += [go.Scatter(x = _x, y = _y[3], name='Walktrap, '+_y[0]) for _y in _y_s]
    plot({"data": data, "layout": go.Layout(title=subject)}, auto_open=True)

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

def get_membership(filename):
    with open(filename, 'r') as f:
        f.seek(0)
        ans = f.readline().split()
        ans = [int(i) for i in ans]
        return ans

def compare(graphs, n):
    n_s = [i+1 for i in range(len(graphs))]
    res_s = []
    c_s = ["pagerank",]
    for c in c_s:
        my_num = []
        newman_num = []
        walktrap_num = []
        for g in graphs:
            edges = g.get_edgelist()
            centralities = get_centralities(g, n, c)
            w_s = get_random_weights(len(edges))
            write_data("erdos_renyi.in", n, edges, cent=centralities, w_s=w_s)
            os.system("./../model < erdos_renyi.in > membership.out")

            my_num.append(read_data("membership.out"))
#            print(read_data('membership.out'))

            base_clustering = g.community_leading_eigenvector(weights=w_s)
            newman_num.append(len(base_clustering))
   
#            raghavan_clustering = g.community_label_propagation(weights=w_s)
#            ragh_num.append(len(raghavan_clustering))
            walktrap_base_clustering = g.community_walktrap(weights=w_s).as_clustering()
            walktrap_num.append(len(walktrap_base_clustering))

        res_s.append((c, my_num, newman_num, walktrap_num))
    show_plot(n_s, res_s, subject='clusters_num')

def compare_modularity(graphs, n):
    n_s = np.arange(len(graphs))
    res_s = []
    c_s = ["pagerank"]
    for c in c_s:
        my_mod = []
        newman_mod = []
        walktrap_mod = []
        for g in graphs:
            edges = g.get_edgelist()
            centralities = get_centralities(g, n, c)
            w_s = get_random_weights(len(edges))
            write_data("erdos_renyi.in", n, edges, cent=centralities, w_s=w_s)
            os.system("./../model < erdos_renyi.in > membership.out")

            memb = get_membership('membership.out')
     #       print(len(memb))
            my_modularity = g.modularity(membership=memb)
            my_mod.append(my_modularity)

            newman_base_clustering = g.community_leading_eigenvector(weights=w_s)
            newman_mod.append(newman_base_clustering.modularity)

            walktrap_base_clustering = g.community_walktrap(weights=w_s).as_clustering()
            walktrap_mod.append(walktrap_base_clustering.modularity)
 #           raghavan_clustering = g.community_label_propagation(weights=w_s)
 #           ragh_mod.append(raghavan_clustering.modularity)
#            greedy_base_clustering = g.community_fastgreedy(weights=w_s).as_clustering()
#            greedy_mod.append(greedy_base_clustering.modularity)

        res_s.append((c, my_mod, newman_mod, walktrap_mod))
    show_plot(n_s, res_s, subject='modularity')

def get_composition(n, memb):
    comp = np.zeros(n)
    memb.sort()
#    print('memb: ', memb)
    cur = memb[0]
    counter = 0
    for c in memb:
        if c==cur:
            counter += 1
        else:
            comp[counter-1] += 1
            counter = 1
            cur = c
    if memb[len(memb)-1] == memb[len(memb)-2]:
        comp[counter-1] += 1
#    print('comp: ', comp)
    return comp

def show_hist(n, _y_s_1, _y_s_2):
    _x_1 = [i+1 for i in range(int(n/6))]
    _x_2 = [i+1 for i in range(int(n/6))]

    traces = []
    for (_y_1, _y_2) in zip(_y_s_1, _y_s_2):
        traces.append(go.Bar(x=_x_1, y=_y_1[:len(_x_1)]))
        traces.append(go.Bar(x=_x_2, y=_y_2[:len(_x_2)]))

    m = len(_y_s_1)
    cols = 4
    rows = int((2*m+3)/4)

    titles = []
    for i in range(len(_y_s_1)):
        titles.append('Natasha, '+str(int(n/5)*i))
        titles.append('Label propagation, '+str(int(n/5)*i))

    fig = tools.make_subplots(rows=rows, cols=cols, subplot_titles=titles)

    x = 1
    y = 1
    for trace in traces:
        fig.append_trace(trace, x, y)
        if y==cols:
            y = 1
            x += 1
        else:
            y += 1

#    data = [go.Bar(x=[i+1 for i in range(n)], y=_y) for _y in _y_s]
    fig['layout'].update(height=400*rows, width=1800, title='Clusters composition')
    plot(fig)
    #plot({"data": data}, auto_open=True)

def get_composition_from_newman(n, memb):
    comp = np.zeros(n)
#    print('memb: ', memb)
    for c in memb:
        comp[len(c)-1] += 1
#    print('comp: ', comp)
    return comp

def get_hist(graphs, n):
    n_s = np.arange(len(graphs))
    res_s = []
    c_s = ["static",]
    for c in c_s:
        my_comp = []
        newman_comp = []
        for g in graphs:
            edges = g.get_edgelist()
            centralities = get_centralities(g, n, c)
            w_s = get_random_weights(len(edges))
            write_data("erdos_renyi.in", n, edges, cent=centralities, w_s=w_s)
            os.system("./../model < erdos_renyi.in > membership.out")

            memb = get_membership('membership.out')
            my_comp.append(get_composition(n, memb))

#            newman_base_clustering = g.community_infomap(edge_weights=w_s, vertex_weights=w_s)
#            newman_comp.append(get_composition_from_newman(n, newman_base_clustering))

            newman_base_clustering = g.community_label_propagation(weights=w_s)
            newman_comp.append(get_composition_from_newman(n, newman_base_clustering))


#            walktrap_base_clustering = g.community_walktrap(weights=w_s).as_clustering()
#            walktrap_memb.append(walktrap_base_clustering[0])
 #           raghavan_clustering = g.community_label_propagation(weights=w_s)
 #           ragh_mod.append(raghavan_clustering.modularity)
#            greedy_base_clustering = g.community_fastgreedy(weights=w_s).as_clustering()
#            greedy_mod.append(greedy_base_clustering.modularity)
            

        res_s = (my_comp, newman_comp)
    show_hist(n, my_comp, newman_comp)
#    print(res_s[0][1])
#    data = [go.Bar(x=[i+1 for i in range(n)], y=res_s[0][1][0])]
#    plot({"data": data}, auto_open=True)

def generate_sequence(n):
    graphs = []
    draw = choice([0, 1], size=(n, n), p=(29/30, 1/30))
    m = get_matrix(draw)
#    print(m)
    g0 = ig.Graph.Adjacency(m.tolist())
    graphs.append(g0)
    order = []
    for i in range(1, n):
        for j in range(i):
            if m[i][j] == 1:
                order.append((i, j))
    shuffle(order)
    step = 0
    for idx in order:
        m[idx[0], idx[1]] = 0
        step += 1
        if step==int(n/5):
            graphs.append(ig.Graph.Adjacency(m.tolist()))
            step = 0
    return graphs

if __name__ == "__main__":
    n = 130
    random.seed(2)
    graphs = generate_sequence(n)
    get_hist(graphs, n)
#    print(res_s)
#    compare_modularity_with_Newman(n, l_max)

