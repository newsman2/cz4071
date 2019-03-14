
from .. import path

import matplotlib
import matplotlib.pyplot as plt
import networkx as nx
from . import graph
import pandas as pd
import os
import math
from .real_network_analyzer import GraphAnalyzer


'''
#Did not amend the data hence not sure if this method is required

def _store_graph_csv_to_file_system(graph_name, graph_csv):
    f = open(os.path.join(CONFIG.DB_NETWORK_DIR_PATH, graph_name + '.csv'), 'w')
    f.write(graph_csv)
    f.close()
'''


def _compute_real_network_properties(graph):
    analyzer = GraphAnalyzer(graph)
    analyzer.compute_average_degree()
    # print("Average degree: " + str(round(analyzer.avg_degree, 5)))
    # print("largest k: " + str(analyzer.comptute_max_degree()))
    # print("|V|: " + str(graph.get_node_count()))
    # print("|E|: " + str(graph.get_edge_count()))
    # Impossible loading time
    # analyzer.compute_sssp_related_properties([])
    # print("Betweenness: " + str(len(analyzer.bc_values)))
    # print("Avg path length: " + str(round(analyzer.avg_path_length, 5)))
    # print("Closeness: " + str(len(analyzer.close_values)))
    analyzer.compute_degree_correlation()
    # print("Degree correlation: " + str(list(analyzer.knn.values())[:10]))
    analyzer.compute_degree_based_clustering_coef()
    analyzer.compute_avg_clustering_coef()
    # print("Avg clustering coef: " + str(analyzer.avg_clustering_coef))
    analyzer.compute_degree_prob_distribution()
    # print("Degree prob distribution: " + str(analyzer.degree_prob_distribution))
    global_cluster_coef =  graph.get_global_clustering_coefficient()
    # print("Global Clustering Coefficient: " + str(global_cluster_coef))

    print('no_of_nodes '+ str(graph.get_node_count()))
    print('no_of_edges '+ str(graph.get_edge_count()))
    print('real_kmax '+ str(analyzer.comptute_max_degree()))
    print('real_kmin '+ str(analyzer.comptute_min_degree()))
    print('average_degree '+ str(round(analyzer.avg_degree,5)))
    print('avg_clustering_coef '+ str(analyzer.avg_clustering_coef))
    # print('clustering_coef' + str(analyzer.degree_based_clustering_coef))
    print('global_clustering_coefficient '+ str(global_cluster_coef))
    # print("degree_correlation "+ str(analyzer.knn))
    print('degree_first_moment '+ str(analyzer.compute_nth_moment(1)))
    print('degree_second_moment '+ str(analyzer.compute_nth_moment(2)))
    print('degree_third_moment '+ str(analyzer.compute_nth_moment(3)))


    k = 1
    plt.rcParams["figure.figsize"] = (11, 7)
    nx_graph = nx.Graph()
    # own_graph = graph.Graph("csv/amazon.txt")
    # own_graph = graph.Graph("csv/amazon")
    # print(own_graph.get_vertices())
    # own_graph = graph.Graph(sys.argv[1])
    degrees = graph.get_each_node_degree()
    # print(own_graph.get_degrees())
    hubs = []
    matplotlib.rcParams.update({'font.size': 20})
    for v in graph.get_nodes():
        # print(v)
        if degrees[v] > k:
            hubs.append(v)
            # print(v)
            for w in graph.neighbor_of_node(v):
                nx_graph.add_edge(v, w)
    result_dir = path.DB_PLOT_DIR_PATH
    # if nx_graph.nodes():
    cluster_coeff_plot, degree_corr_plot, degree_dist_plot = draw_properties(analyzer.degree_based_clustering_coef,analyzer.avg_clustering_coef,analyzer.knn,analyzer.degree_prob_distribution,analyzer.avg_degree,graph)

    # ignore if got isinstance(... warning, still works
    real_network_graph = plot_graph(nx_graph, result_dir)

    # property_info_dict = {"avg_degree" : analyzer.avg_degree,
    #                     "degree_distribution" : analyzer.degree_prob_distribution,
    #                     "degrees" : graph.get_each_node_degree(),
    #                     "bc_values" : analyzer.bc_values,
    #                     "avg_path_len" : analyzer.avg_path_length,
    #                     "closeness" : analyzer.close_values,
    #                     "degree_correlation" : analyzer.knn,
    #                     "avg_clustering_coef" : analyzer.avg_clustering_coef,
    #                     "clustering_coef" : analyzer.degree_based_clustering_coef,
    #                     "1st_moment" : analyzer.compute_nth_moment(1),
    #                     "2nd_moment" : analyzer.compute_nth_moment(2),
    #                     "3rd_moment" : analyzer.compute_nth_moment(3)}

    return {
        'no_of_nodes': graph.get_node_count(),
        'no_of_edges': graph.get_edge_count(),
        'real_kmax': str(analyzer.comptute_max_degree()),
        'real_kmin': str(analyzer.comptute_min_degree()),
        'average_degree': str(round(analyzer.avg_degree, 5)),
        'avg_clustering_coef': analyzer.avg_clustering_coef,
        # 'clustering_coef':analyzer.degree_based_clustering_coef,
        'global_clustering_coefficient': global_cluster_coef,
        # "degree_correlation": analyzer.knn,
        'degree_first_moment': analyzer.compute_nth_moment(1),
        'degree_second_moment': analyzer.compute_nth_moment(2),
        'degree_third_moment': analyzer.compute_nth_moment(3),
        
        'cluster_coeff_plot_file_name':cluster_coeff_plot,
        'degree_corr_plot_file_name': degree_corr_plot,
        'degree_prob_distribution_plot_file_name': degree_dist_plot,
        'real_network_graph': real_network_graph,
        # 'distance_distribution': distance_distribution,
        # 'distance_prob_distribution_plot_file_name': distance_prob_distribution_plot_file_name,
        # 'average_distance': average_distance,
        # 'diameter': diameter,
    }


def plot_graph(graph, save_dir):
    pos = nx.random_layout(graph)
    options = {
        'pos': pos,
        'node_color': 'black',
        'node_size': 0.005,
        'edge_color': 'blue',
        'width': 0.00025,

    }
    file_name = 'Real_Network' + '_degree_distribution_log_binning.png'
    file_path = os.path.join(path.DB_PLOT_DIR_PATH, file_name)

    nx.draw(graph, **options)
    # %matplotlib inline
    # nx.draw_networkx(graph, **options)
    # plt.savefig(os.path.join(save_dir, 'graph.png'))
    plt.savefig(file_path)
    # plt.show()
    return file_name

def plot_curve(data, x_label, y_label, title, log=False, h_line=None, v_line=None):
    x = list(data.keys())
    y = list(data.values())
    file_name = title + '.png'
    file_path = os.path.join(path.DB_PLOT_DIR_PATH, file_name)

    if log:
        # Remove zeros for log-log plots
        for k in x:
            if k == 0 or data[k] == 0:
                del data[k]
        x = [math.log(i) for i in data.keys()]
        y = [math.log(i) for i in data.values()]
    plt.scatter(x, y, s=10)
    if h_line:
        if log:
            h_line = math.log(h_line)
        plt.axhline(h_line, color='r')
    if v_line:
        if log:
            v_line = math.log(v_line)
        plt.axvline(v_line, color='r')


    plt.xlabel(x_label)
    plt.ylabel(y_label)
    plt.title(title)
    plt.savefig(file_path)
    plt.show()
    return file_name

def draw_properties(clustering_coef,avg_clustering_coef,degree_corr,degree_distribution,avg_degree,graph):
    # with open(os.path.join(save_dir, "properties.pkl"), "rb") as f:
    #     property_info_dict = pickle.load(f)

    # degree_distribution = property_info_dict["degree_distribution"]
    # degree_corr = property_info_dict["degree_correlation"]
    # clustering_coef = property_info_dict["clustering_coef"]

    cluster_coef_graph = plot_curve(clustering_coef, "log(k)", "log(C(k))", "Clustering Coefficient",
            log=True,
            h_line=avg_clustering_coef)
    # cluster_coef_graph = graph.plot_store_degree_correlation_log_log()
    degree_corr_graph = plot_curve(degree_corr, "log(k)", "log(knn)", "Degree Correlation",
            log=True)
    degree_dist_graph = plot_curve(degree_distribution, "log(k)", "log(P(k))", "Degree Distribution",
            log=True,
            v_line=avg_degree)

    return cluster_coef_graph, degree_corr_graph, degree_dist_graph


def _load_graph_csv_from_file_system(graph_name):
    network = pd.read_csv(path.CSV_NETWORK_DIR_PATH + "\\" + graph_name + ".csv")
    tmp = list(zip(network['FromNodeId'], network['ToNodeId']))
    g = nx.Graph()
    g.add_edges_from(tmp)
    return g

# def _is_network_too_big(no_of_nodes, no_of_edges):
#     return no_of_nodes > 10000 or no_of_edges > 500000

if __name__ == "__main__":

    graph = graph.Graph("csv/amazon")

    _compute_real_network_properties(graph)