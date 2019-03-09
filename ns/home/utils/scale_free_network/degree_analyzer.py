import math
import os
from collections import Counter
import matplotlib.pyplot as plt
import networkx as nx
from .. import path as path
from . import plot_util




def count_degree(network):
    dic_list = {}
    for (node, val) in network.degree():
        dic_list[node] = val
    return dic_list




def calculate_degree_distribution(network):
    return nx.degree_histogram(network)


def calculate_degree_prob_distribution(no_of_nodes, degree_distribution):
    for key, value in degree_distribution.items():
        degree_distribution[key] = float(value) / no_of_nodes

    return degree_distribution

def plot_and_store_degree_prob_distribution(network_name, degree_count):

    file_name = network_name + '_degree_distribution_log_binning.png'
    file_path = os.path.join(path.DB_PLOT_DIR_PATH, file_name)

    n, bins = plot_util.log_binning(degree_count, n_bins=50, plot=False)
    bin_centers = list((bins[1:] + bins[:-1]) / 2)
    n = list(n)

    x_log, y_log = plot_util.get_log_log_points(bin_centers, n)
    plt.scatter(x_log, y_log, s=2, c='r')
    plt.title('Log-Log Degree Distribution with Log Binning')
    plt.xlabel('k')
    plt.ylabel('P(k)')
    plt.savefig(file_path)
    # plt.show()
    plt.close()

    return file_name



def calculate_degree_moment(degree_count, n=1):
    return sum([
        math.pow(c, n) for c in degree_count.values()
    ]) / len(degree_count.values())


def find_largest_degree(degree_distribution):
    return (len(degree_distribution)-1)


def find_smallest_degree(degree_distribution):
    j = 0
    for i in degree_distribution:
        if i != 0:
            return j
        else:
            j += 1
