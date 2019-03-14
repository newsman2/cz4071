
import matplotlib.pyplot as plt
import os
import time
import numpy as np

#import config


def connected_neighbours_links(network):
    print('Counting number of connected neighbours...')
    start_time = int(round(time.time() * 1000))
    node_cc_links = dict()
    for key, nodes in network.items():
        # print('key: ' + str(key) + ' value: ' + str(nodes))
        cc_links = list()

        for node in nodes:
            nodes_list = list(nodes)
            # print('node: ' + node)
            nodes_list.remove(node)
            # print('after removed nodes list: ' + str(nodes_list))

            for n in nodes_list:
                if node in network[int(n)]:
                    # print('connected nodes of node ' + n + ': ' + str(network[int(n)]))
                    # print('connected nodes: ' + str(node) + ' and ' + str(n))
                    link = [int(node), int(n)]
                    link.sort()
                    if link not in cc_links:
                        cc_links.append(link)
            cc_links.sort()
            # print(cc_links)
            # print(len(cc_links))
            # break  # break after single iteration of for node in nodes
        node_cc_links[int(key)] = len(cc_links)
        # print(node_cc_links)
        # if key == 0:
        #     break
    end_time = int(round(time.time() * 1000))
    compute_time = int(end_time) - int(start_time)
    print('({}ms) Count the number of connected neighbours for each node'.format(compute_time))
    # print(node_cc_links)
    return node_cc_links


def clustering_coefficient(node_degree, node_cc_links):
    clustering_coeff = dict()
    print('length: ' + str(len(node_degree)))
    for key, node_degree in node_degree.items():
        if int(node_degree) > 1:
            cc = float((2 * int(node_cc_links[key]))/(int(node_degree) * (int(node_degree) - 1)))
            # print(cc)
            clustering_coeff[int(key)] = round(cc, 2)
        # else:
        #     clustering_coeff[int(key)] = 0
        # break
    # print(clustering_coeff)
    return clustering_coeff


def plot_store_clustering_coefficient(network_name, dict_values, node_degree, plot_name):
    file_name = network_name + '_' + plot_name + '.png'
    file_path = os.path.join(config.DB_PLOT_DIR_PATH, file_name)

    y = []
    x = []
    for key, value in dict_values.items():
        if key > 0 and value > 0.0:
            # print(node_degree[key])
            x.append(node_degree[key])
            y.append(value)

    plt.scatter(x, y, s=20*0.1, c='r')
    plt.title(plot_name)
    plt.xlabel('k')
    plt.ylabel('C(k)')
    plt.savefig(file_path)
    plt.close()

def plot_store_clustering_coefficient_log_log(network_name, dict_values, node_degree, plot_name):
    file_name = network_name + '_' + plot_name + '.png'
    file_path = os.path.join(config.DB_PLOT_DIR_PATH, file_name)

    y = []
    x = []
    for key, value in dict_values.items():
        if key > 0 and value > 0.0:
            # print(node_degree[key])
            x.append(np.log10(node_degree[key]))
            y.append(np.log10(value))

    plt.scatter(x, y, s=20 * 0.1, c='r')
    plt.title(plot_name)
    plt.xlabel('k')
    plt.ylabel('C(k)')
    plt.savefig(file_path)
    plt.close()
