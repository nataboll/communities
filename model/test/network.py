import plotly.offline as py 
import plotly.graph_objs as go 

trace = go.Scatter( 
    x=[1, 2, 2, 1], 
    y=[3, 4, 3, 4], 
    mode='markers',
    marker=dict(size=[100, 100, 100, 100])
)

# Edges
x0 = [1, 2]
y0 = [3, 3]
x1 = [2, 1]
y1 = [4, 4]

fig = go.Figure(
    data=[trace],
    layout=go.Layout(
        annotations = [
            dict(ax=x0[i], ay=y0[i], axref='x', ayref='y',
                x=x1[i], y=y1[i], xref='x', yref='y') for i in range(0, len(x0))
        ]
    )
) 
py.plot(fig)
