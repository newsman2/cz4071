import matplotlib
matplotlib.use('Agg')
from . import degree_analyzer
from . import distance_analyzer
from . import clustering_coefficient_analyzer
from .. import path as PATH
import pandas as pd
import networkx as nx
import plotly.graph_objs as go
from plotly.offline import plot
import matplotlib.pyplot as plt
import os


#network_name is amazon
#network = _load_graph_csv_from_file_system(network_name)

def _compute_real_network_properties(network_name, network):

    # Number of nodes
    no_of_nodes = network.number_of_nodes()
    # Number of edges
    no_of_edges = network.number_of_edges()

    # Real Network Properties

    # Each node with its degree
    degree_count = degree_analyzer.count_degree(network)
    # List of frequency of degree. The position is the k degree. Example position 1 of the list means the frequency of degree 1
    degree_distribution = degree_analyzer.calculate_degree_distribution(network)

    # pool = mp.Pool(mp.cpu_count())
    # result = pool.map(_generate_network_image, network_name)

    # network_image_url = _generate_network_image(network_name, network)

    degree_prob_distribution_plot_url = degree_analyzer.plot_and_store_degree_prob_distribution(network_name, degree_count)

    # Degree Moment which each value to the power of n given n in the input parameter

    # Mean
    average_degree = degree_analyzer.calculate_degree_moment(degree_count, n=1)
    # Nth moment where n is 2 in this method
    degree_second_moment = degree_analyzer.calculate_degree_moment(degree_count, n=2)

    # Find the maximum/highest degree of the graph
    real_kmax = degree_analyzer.find_largest_degree(degree_distribution)
    # Find the minimum/lowest degree of the graph
    real_kmin = degree_analyzer.find_smallest_degree(degree_distribution)

    # Find global clustering
    global_clustering_coefficient = clustering_coefficient_analyzer.calculate_global_clustering_coefficient(network)
    # Find average clustering
    average_clustering_coefficient = clustering_coefficient_analyzer.calculate_average_clustering_coefficient(network)

    # distance_distribution = distance_analyzer.get_distance_distribution(network)
    # distance_prob_distribution = distance_analyzer.calculate_distance_prob_distribution(distance_distribution)
    # distance_prob_distribution_plot_file_name = distance_analyzer.plot_and_store_distance_prob_distribution(
    #     network_name,
    #     distance_prob_distribution
    # )

    # find the average distance of the graph path
    # average_distance = distance_analyzer.calculate_average_distance(network)

    # find the diameter of the graph
    # diameter = distance_analyzer.find_network_diameter(network)

    return {
        'no_of_nodes': no_of_nodes,
        'no_of_edges': no_of_edges,
        # 'degree_prob_distribution_plot_file_name': degree_prob_distribution_plot_url,
        'average_degree': average_degree,
        'degree_second_moment': degree_second_moment,
        'real_kmax': real_kmax,
        'real_kmin': real_kmin,
        # 'distance_prob_distribution_plot_file_name': distance_prob_distribution_plot_file_name,
        # 'average_distance': average_distance,
        # 'diameter': diameter,
        'global_clustering_coefficient': global_clustering_coefficient,
        'average_clustering_coefficient': average_clustering_coefficient
    }

'''
#Did not amend the data hence not sure if this method is required

def _store_graph_csv_to_file_system(graph_name, graph_csv):
    f = open(os.path.join(CONFIG.DB_NETWORK_DIR_PATH, graph_name + '.csv'), 'w')
    f.write(graph_csv)
    f.close()
'''


def _load_graph_csv_from_file_system(graph_name):
    network = pd.read_csv(PATH.CSV_NETWORK_DIR_PATH + "/" + graph_name + ".csv")
    tmp = list(zip(network['FromNodeId'], network['ToNodeId']))
    g = nx.Graph()
    g.add_edges_from(tmp)
    return g


def _generate_network_image(network_name, network):
    plt.figure(figsize=(18, 18))
    #G = nx.gnp_random_graph(50, 0.25)
    #G = _load_graph_csv_from_file_system(network_name)
    G = network
    file_name = network_name + '_network_image.png'
    file_path = os.path.join(PATH.DB_PLOT_DIR_PATH, file_name)

    nx.draw(G, node_size=10)
    graph_pos = nx.spring_layout(G)
    nx.draw_networkx_nodes(G, graph_pos, node_size=10, node_color='blue', alpha=0.3)
    nx.draw_networkx_edges(G, graph_pos)
    nx.draw_networkx_labels(G, graph_pos, font_size=8, font_family='sans-serif')

    plt.savefig(file_path)
    # plt.show()
    plt.close()

    return file_name


def _is_network_too_big(no_of_nodes, no_of_edges, network, network_name):
    # Each node with its degree
    degree_count = degree_analyzer.count_degree(network)
    degree_prob_distribution_plot_url = degree_analyzer.plot_and_store_degree_prob_distribution(network_name, degree_count)
    return no_of_nodes > 10000 or no_of_edges > 500000


def plot_real_interactive_network(network):

    pos = nx.get_node_attributes(network, 'pos')

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

    for edge in network.edges():
        x0, y0 = network.node[edge[0]]['pos']
        x1, y1 = network.node[edge[1]]['pos']
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

    for node in network.nodes():
        x, y = network.node[node]['pos']
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





