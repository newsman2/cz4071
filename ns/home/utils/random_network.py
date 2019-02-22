import networkx as nx
import plotly.graph_objs as go
from plotly.offline import plot
from . import random_network_analyzer


def _compute_random_network_properties(network_name, n, p):
    expected_no_of_edges = random_network_analyzer.calculate_no_of_edges(n, p)
    expected_average_degree = random_network_analyzer.calculate_average_degree(n, p)
    expected_degree_distribution_plot_file_name = random_network_analyzer.calculate_degree_prob_distribution(
        network_name, n, p)
    expected_regime_type = random_network_analyzer.get_regime_type(n, p)

    expected_average_distance = random_network_analyzer.calculate_average_distance(n, p)
    expected_clustering_coefficient = random_network_analyzer.calculate_clustering_coefficient(p)
    interactive_network_plot = plot_random_interactive_network(n, p)

    return {
        'p': p,
        'expected_no_of_nodes': n,
        'expected_no_of_edges': expected_no_of_edges,
        'expected_degree_distribution_plot_file_name': expected_degree_distribution_plot_file_name,
        'expected_average_degree': expected_average_degree,
        'expected_regime_type': expected_regime_type,
        'expected_average_distance': expected_average_distance,
        'expected_clustering_coefficient': expected_clustering_coefficient,
        'interactive_network_plot': interactive_network_plot
    }


def plot_random_interactive_network(n, p):
    G = nx.random_geometric_graph(n, p)
    pos = nx.get_node_attributes(G, 'pos')

    dmin = 1
    ncenter = 0
    for n in pos:
        x, y = pos[n]
        d = (x - 0.5) ** 2 + (y - 0.5) ** 2
        if d < dmin:
            ncenter = n
            dmin = d

    edge_trace = go.Scatter(
        x=[],
        y=[],
        line=dict(width=0.5, color='#888'),
        hoverinfo='none',
        mode='lines')

    for edge in G.edges():
        x0, y0 = G.node[edge[0]]['pos']
        x1, y1 = G.node[edge[1]]['pos']
        edge_trace['x'] += tuple([x0, x1, None])
        edge_trace['y'] += tuple([y0, y1, None])

    node_trace = go.Scatter(
        x=[],
        y=[],
        text=[],
        mode='markers',
        hoverinfo='text',
        marker=dict(
            showscale=True,
            # colorscale options
            # 'Greys' | 'YlGnBu' | 'Greens' | 'YlOrRd' | 'Bluered' | 'RdBu' |
            # 'Reds' | 'Blues' | 'Picnic' | 'Rainbow' | 'Portland' | 'Jet' |
            # 'Hot' | 'Blackbody' | 'Earth' | 'Electric' | 'Viridis' |
            colorscale='YlGnBu',
            reversescale=True,
            color=[],
            size=10,
            colorbar=dict(
                thickness=15,
                title='Node Connections',
                xanchor='left',
                titleside='right'
            ),
            line=dict(width=2)))

    for node in G.nodes():
        x, y = G.node[node]['pos']
        node_trace['x'] += tuple([x])
        node_trace['y'] += tuple([y])

        for node, adjacencies in enumerate(G.adjacency()):
            node_trace['marker']['color'] += tuple([len(adjacencies[1])])
            node_info = '# of connections: ' + str(len(adjacencies[1]))
            node_trace['text'] += tuple([node_info])

    fig = go.Figure(data=[edge_trace, node_trace],
                    layout=go.Layout(
                        title='<br>Interactive Random Network',
                        titlefont=dict(size=16),
                        showlegend=False,
                        hovermode='closest',
                        margin=dict(b=20, l=5, r=5, t=40),
                        xaxis=dict(showgrid=False, zeroline=False, showticklabels=False),
                        yaxis=dict(showgrid=False, zeroline=False, showticklabels=False)))

    plot_div = plot(fig, output_type='div', include_plotlyjs=False)
    return plot_div
