import matplotlib.pyplot as plt
import numpy as np
import os

from .. import path


def compute_degree_correlation(graph):
    total_neighbor_degrees = {}
    for node in graph.get_nodes():
        for neighbor_node in graph.neighbor_of_node(node):
            if node not in total_neighbor_degrees:
                total_neighbor_degrees[node] = len(graph.neighbor_of_node(neighbor_node))
            else:
                total_neighbor_degrees[node] += len(graph.neighbor_of_node(neighbor_node))

    knn = {}
    for node in total_neighbor_degrees.keys():
        knn[node] = float(total_neighbor_degrees[node] /float(graph.get_degree_of_node(node)))

    return knn


def plot_store_degree_correlation_log_log(dict_values):
    plot_name = 'Degree Correlation Log Log'
    file_name =  plot_name + '.png'
    file_path = os.path.join(path.DB_PLOT_DIR_PATH, file_name)

    x = []
    y = []

    for key, value in dict_values.items():
        if key > 0 and value > 0.0:
            x.append(np.log10(key))
            y.append(np.log10(value))

    plt.scatter(x, y, s=20*0.1, c='r')
    plt.title(plot_name)
    plt.xlabel('k')
    plt.ylabel('knn(k)')
    plt.savefig(file_path)
    plt.show()
    plt.close()
    return file_name


def plot_store_degree_correlation(network_name, dict_values):
    plot_name = 'Degree Correlation'
    file_name = network_name + '_' + plot_name + '.png'
    file_path = os.path.join(path.DB_PLOT_DIR_PATH, file_name)

    x = []
    y = []

    for key, value in dict_values.items():
        if key > 0 and value > 0.0:
            x.append(key)
            y.append(value)

    plt.scatter(x, y, s=20*0.1, c='r')
    plt.title(plot_name)
    plt.xlabel('k')
    plt.ylabel('knn(k)')
    plt.savefig(file_path)
    plt.close()
