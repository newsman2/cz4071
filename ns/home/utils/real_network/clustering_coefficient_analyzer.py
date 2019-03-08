import networkx as nx
import numpy as np


def calculate_global_clustering_coefficient(network):
    return nx.transitivity(network)


def calculate_average_clustering_coefficient(network):
    return nx.average_clustering(network)


def calculate_local_clustering_coefficients(network):
    return nx.clustering(network)