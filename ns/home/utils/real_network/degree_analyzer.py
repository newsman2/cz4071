from itertools import groupby
import os
import math
import numpy as np
import time

import matplotlib.pyplot as plt

#import config
# import graph.analyzer.plotutil as plot_util
from .. import path as config


def count_degree_old(vertex):
    # not a good way to get degree
    # each_node_degree = [len(list(group)) for key, group in groupby(vertex)]
    # print(len(each_node_degree))

    start_time = int(round(time.time() * 1000))

    each_node_degree = [];
    index = 1;
    for key, group in groupby(vertex):
        # print('key: ' + str(key))
        # print('index: ' + str(index))

        if int(key) != int(index):
            # print('not equal')
            each_node_degree.insert(index-1, 0)
            index += 2
        else:
            index += 1

        each_node_degree.append(len(list(group)))
        # if key == '10':
        #     break

    end_time = int(round(time.time() * 1000))
    compute_time = int(end_time) - int(start_time)
    print('({}ms) Count degree'.format(compute_time))

    return each_node_degree


def count_degree(network):
    start_time = int(round(time.time() * 1000))
    node_degree = {}
    for key, value in network.items():
        node_degree[key] = len(value)
    end_time = int(round(time.time() * 1000))
    compute_time = int(end_time) - int(start_time)
    # print('({}ms) Count the number of degree for each node'.format(compute_time))
    # print(node_degree)
    return node_degree


# Count how many nodes with degree x,
# Where x can be 1 to 100
def count_node_with_degree_x(node_degree):
    degree_frequency = {}
    for key, value in node_degree.items():
        if value not in degree_frequency:
            degree_frequency[value] = 0
        degree_frequency[value] += 1
    s_degree_frequency = dict()
    for key in sorted(degree_frequency.keys()):
        s_degree_frequency[key] = degree_frequency[key]
    return s_degree_frequency


def calculate_degree_distribution(no_of_nodes, degree_frequency):
    prob_degree_distribution = {}
    for key, value in degree_frequency.items():
        prob_degree_distribution[key] = float(value / no_of_nodes)
    return prob_degree_distribution


def degree_distribution(network):
    node_degree = count_degree(network)
    degree_frequency = count_node_with_degree_x(node_degree)
    return calculate_degree_distribution(len(network), degree_frequency)


def calculate_degree_n_moment(degree_count, n):
    return sum([math.pow(x, n) for x in degree_count.values()]) / len(degree_count.values())


def find_k_max(degree_distribution):
    return max(degree_distribution.keys())


def find_k_min(degree_distribution):
    return min(degree_distribution.keys())


def plot_store_degree_distribution_log_log(network_name, dict_values, plot_name):
    file_name = network_name + '_' + plot_name + '.png'
    file_path = os.path.join(config.DB_PLOT_DIR_PATH, file_name)

    degree_list = []
    probability_list = []
    for key, value in dict_values.items():
        if key > 0 and value > 0.0:
            # print(type(key))
            # print(np.log10(key))
            degree_list.append(np.log10(key))
            probability_list.append(np.log10(value))

    plt.scatter(degree_list, probability_list, s=20*0.1, c='r')
    plt.title(plot_name)
    plt.xlabel('k')
    plt.ylabel('P(k)')
    plt.savefig(file_path)
    plt.close()


def plot_store_degree_distribution(network_name, dict_values, plot_name):
    file_name = network_name + '_' + plot_name + '.png'
    file_path = os.path.join(config.DB_PLOT_DIR_PATH, file_name)

    degree_list = []
    probability_list = []
    for key, value in dict_values.items():
        if key > 0 and value > 0.0:
            # print(type(key))
            # print(np.log10(key))
            degree_list.append(key)
            probability_list.append(value)

    plt.scatter(degree_list, probability_list, s=20*0.1, c='r')
    plt.title(plot_name)
    plt.xlabel('k')
    plt.ylabel('P(k)')
    plt.savefig(file_path)
    plt.close()
