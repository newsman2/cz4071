#from graph_tool import topology
import os
from multiprocessing.spawn import freeze_support
from .. import path
import networkx as nx

import matplotlib.pyplot as plt
import numpy as np
from multiprocessing import Process, Queue
from multiprocessing.managers import BaseManager
import math


def _shortest_distance_runner_small_network(result_queue, network, thread_id, n_threads=8):
    # vertices = list(network.vertices())
    vertices = list(network.nodes())
    l = len(vertices)
    distance_distribution = {}

    for i in range(thread_id, l, n_threads):
        v = vertices[i]
        v_id = int(v)

        # distance_map = topology.shortest_distance(
        #     network,
        #     source=v,
        #     target=None,
        #     directed=False
        # )
        distance_map = nx.shortest_path(network, source=v, target=None, weight=None)

        distance_array = distance_map.get_array()[v_id:]
        for j in np.nditer(distance_array):
            distance = int(j)

            if distance not in distance_distribution:
                distance_distribution[distance] = 0

            distance_distribution[distance] += 1

    result_queue.put(distance_distribution)



def _convert_multiprocessing_queue_to_list(queue):
    result = []
    while not queue.empty():
        result.append(queue.get())

    return result



def combine_multiple_distance_distributions(distance_distribution_list):
    result = {}

    for distance_distribution in distance_distribution_list:
        for k, v in distance_distribution.items():
            if k not in result:
                result[k] = 0

            result[k] += v

    return result
    

#If i am not wrong, this method get the distance of any 2 pair of nodes

def get_distance_distribution(network, n_process=4):
    # n_nodes = network.num_vertices()
    n_nodes = len(network)
    # n_edges = network.num_edges()
    n_edges = network.number_of_edges()

    vertices = list(network.nodes())
    l = len(vertices)
    distance_distribution = {}

    # if n_nodes > 10000 or n_edges > 500000:
    #     return None

    for i in range(1, len(vertices)):
        v = vertices[i]
        v_id = int(v)

        # distance_map = topology.shortest_distance(
        #     network,
        #     source=v,
        #     target=None,
        #     directed=False
        # )
        # distance_map = nx.shortest_path(network, source=v, target=None, weight=None)

        distance_map = nx.single_source_shortest_path_length(network, source=v)

        # distance_map = nx.all_pairs_shortest_path_length(network)

        # distance_array = distance_map.get_array()[v_id:]
        # distance_array = distance_map.ToArray()
        # for j in np.nditer(distance_array):
        # for j in distance_map.items():
        for key, value in distance_map.items():
            # distance = int(j)
            distancewithsq = distance_map[key]
            distance = int(distancewithsq)

            if distance not in distance_distribution:
                distance_distribution[distance] = 0
                # distance_distribution.insert(distance, 0)
            distance_distribution[distance] += 1
    return distance_distribution

    # processes = []
    # result_queue = Queue(n_process)
    # for i in range(n_process):
    #     p = Process(
    #         target=_shortest_distance_runner_small_network,
    #         args=(result_queue, network, i, n_process,)
    #     )
    #
    #     print('Starting process ID:', i)
    #     p.start()
    #     processes.append(p)
    #
    # print('Processes created!')
    # for p in processes:
    #     p.join()
    #
    # print('Done!')
    #
    # result_list = _convert_multiprocessing_queue_to_list(result_queue)
    # return combine_multiple_distance_distributions(result_list)


def calculate_average_distance(network):
    return nx.average_shortest_path_length(network)


def find_network_diameter(network):
    return nx.diameter(network)


#Not sure if we are using this method

def calculate_distance_prob_distribution(distance_distribution):
    result = {}
    if distance_distribution is None:
        return None

    total = sum(distance_distribution.values())
    for k, v in distance_distribution.items():
        if k > total or k == 0:
            continue

        result[k] = float(distance_distribution[k]) / float(total)

    return result
    

# plotting of graph
def plot_and_store_distance_prob_distribution(network_name, distance_prob_distribution):
    file_name = network_name + '_distance_distribution.png'
    file_path = os.path.join(path.DB_PLOT_DIR_PATH, file_name)
    print(distance_prob_distribution)

    x = []
    y = []

    for k, v in distance_prob_distribution.items():
        # x.append(math.log10(k))
        # y.append(math.log10(v))
        x.append(k)
        y.append(v)

    plt.clf()
    plt.scatter(x, y, c='r')
    plt.title('Shortest Distance Distribution')
    plt.xlabel('d')
    plt.ylabel('P(d)')
    plt.savefig(file_path)
    plt.show()
    plt.close()

    return file_name



def main():
    BaseManager.register('get_queue', callable=lambda:  Queue.Queue())

    manager = BaseManager(address=('', 5000), authkey='abc')
    manager.start()
    manager.shutdown()

if __name__ == '__main__':
    # freeze_support() here if program needs to be frozen
    freeze_support()
    # main()  # execute this only when run directly, not when imported!


# def get_distance_distribution(network, n_process=4):
#     n_nodes = network.num_vertices()
#     n_edges = network.num_edges()
#
#     if n_nodes > 10000 or n_edges > 500000:
#         return None
#
#     processes = []
#     result_queue = Queue(n_process)
#     for i in range(n_process):
#         p = Process(
#             target=_shortest_distance_runner_small_network,
#             args=(result_queue, network, i, n_process,)
#         )
#
#         # print 'Starting process ID:', i
#         p.start()
#         processes.append(p)
#
#     # print 'Processes created!'
#     for p in processes:
#         p.join()
#
#     # print 'Done!'
#
#     result_list = _convert_multiprocessing_queue_to_list(result_queue)
#     return combine_multiple_distance_distributions(result_list)

#The main here seems to be used for random network
#
# if __name__ == '__main__':
#     from graph.generator import random_network_generator
#
#     network = random_network_generator.generate_random_network(1000, p=0.746)
#     distance_distribution = get_distance_distribution(network, n_process=2)
#     print distance_distribution
#
#     print calculate_average_distance(network.num_vertices(), distance_distribution)
#     print find_network_diameter(distance_distribution)
#     print calculate_distance_prob_distribution(distance_distribution)
#
