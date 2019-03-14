from ..real_network.real_network import _load_graph_csv_from_file_system
from ..scale_free_network import degree_analyzer, scale_free_network_analyzer


def _compute_scale_free_properties(network):
    # no_of_nodes = network.num_vertices()
    # no_of_nodes = network.nodes()
    no_of_nodes = len(network)
    degree_count = degree_analyzer.count_degree(network)
    # degree_distribution = degree_analyzer.calculate_degree_distribution(degree_count)
    degree_distribution = degree_analyzer.calculate_degree_distribution(network)
    real_kmax = degree_analyzer.find_largest_degree(degree_distribution)
    real_kmin = degree_analyzer.find_smallest_degree(degree_distribution)
    # degree_exponent = scale_free_network_analyzer.calculate_real_degree_exponent(degree_count)
    expected_degree_exponent = scale_free_network_analyzer.calculate_expected_degree_exponent(no_of_nodes, real_kmax,real_kmin)
    expected_kmax = scale_free_network_analyzer.calculate_expected_max_degree(no_of_nodes, real_kmin, expected_degree_exponent)
    expected_average_distance = scale_free_network_analyzer.calculate_expected_average_distance(no_of_nodes, expected_degree_exponent)

    print('expected_kmax'+ str(expected_kmax))
    print('expected_average_distance'+ str(expected_average_distance))
    print('expected_degree_exponent'+ str(expected_degree_exponent))

    return {
        # 'degree_exponent': degree_exponent,
        'expected_kmax': expected_kmax,
        'expected_average_distance': expected_average_distance,
        'expected_degree_exponent': expected_degree_exponent
    }

if __name__ == "__main__":
    networkx = _load_graph_csv_from_file_system("amazon")
    _compute_scale_free_properties(networkx)