from . import degree_analyzer as da
from . import clustering as ca
from . import degree_correlation as dc
import networkx as nx
from .real_network import _load_graph_csv_from_file_system


class Graph:
    network = dict()
    networkx = nx.Graph()

    # Initializer / Instance Attributes
    def __init__(self, input_file):
        self.graph_name = input_file
        # get_data_frame("amazon")
        # self.networkx_graph =_load_graph_csv_from_file_system("amazon")
        self.loaded = False
        self.read()

    def read(self):
        if self.loaded:
            return

        self.networkx = _load_graph_csv_from_file_system("amazon");

        with open(self.graph_name + ".txt", "r") as input_graph:
            for line in input_graph:
                if line.startswith('#'):
                    continue

                split = line.split()

                if int(split[1]) not in self.network:
                    self.network[int(split[1])] = []

                if int(split[0]) not in self.network:
                    edge_to_list = [int(split[1])]
                    self.network[int(split[0])] = edge_to_list
                elif int(split[0]) in self.network:
                    retrieve = self.network[int(split[0])]
                    edge_to_list = list()
                    for value in retrieve:
                        edge_to_list.append(value)
                    edge_to_list.append(int(split[1]))
                    self.network[int(split[0])] = edge_to_list

            s_network = dict()
            for key in sorted(self.network.keys()):
                edge_to_list = self.network[key]
                edge_to_list = sorted(edge_to_list)
                s_network[key] = edge_to_list

            self.network = s_network
            self.loaded = True
    def neighbor_of_node(self, node):
        return self.network[node]

    def get_node_count(self):
        return len(self.network)

    def get_nodes(self):
        node_list = list()
        for key in self.network.keys():
            node_list.append(key)
        return node_list

    def get_degree_of_node(self, node):
        return len(self.network[node])

    def get_edge_count(self):
        count = 0
        for node, edge_list in self.network.items():
            count += len(edge_list)
        return count

    def get_each_node_degree(self):
        return da.count_degree(self.network)

    def get_each_degree_frequency(self):
        return da.count_node_with_degree_x(self.get_each_node_degree())

    def get_degree_distribution(self):
        return da.calculate_degree_distribution(self.get_node_count(), self.get_each_degree_frequency())

    def get_moment_n(self, n):
        return da.calculate_degree_n_moment(self.get_each_node_degree(), n)

    def get_max_k(self):
        return da.find_k_max(self.get_each_degree_frequency())

    def get_min_k(self):
        return da.find_k_min(self.get_each_degree_frequency())

    def get_clustering_coefficient(self):
        return ca.clustering_coefficient(self.get_each_node_degree(), ca.connected_neighbours_links(self.network))

    def get_global_clustering_coefficient(self):
        return nx.transitivity(self.networkx)

    def get_degree_correlation(self):
        return dc.compute_degree_correlation(self)

    def plot_store_degree_correlation_log_log(self):
       return dc.plot_store_degree_correlation_log_log( self.get_degree_correlation())

    def plot_store_degree_correlation(self):
        dc.plot_store_degree_correlation(self.graph_name, self.get_degree_correlation())

    # def plot_closeness(self):
    #    closeness = nx.closeness_centrality(self.networkx_graph)
    #    x = list(closeness.keys())
    #    y = list(closeness.values())
    #    print(x)
    #    print(y)
    #
    #    p.offline.plot({
    #        "data": [go.Scatter(x=x, y=y)],
    #        "layout": go.Layout(title="closeness")
    #    }, auto_open=True,  )
    #
    # def plot_betweeness(self):
    #    closeness = nx.betweenness_centrality(self.networkx_graph)
    #    x = list(closeness.keys())
    #    y = list(closeness.values())
    #    print(x)
    #    print(y)
    #
    #    p.offline.plot({
    #        "data": [go.Scatter(x=x, y=y)],
    #        "layout": go.Layout(title="betweeness")
    #    }, auto_open=True,  )

       # def get_data_frame(self, graph_name):
       #     graph_dict = {"Nodes": "", "Edges": ""}
       #
       #     from_node = []
       #     to_node = []
       #     df = pd.DataFrame()
       #
       #     # graph_name = "amazon"
       #
       #     tmp = 0
       #     node = False
       #     edge = False
       #     start = False
       #
       #
       #     with open(self.graph_name + ".txt", "r") as f:
       #         for line in f:
       #             for word in line.split():
       #                 if node == True:
       #                     graph_dict['Nodes'] = word
       #                     node = False
       #                 if edge == True:
       #                     graph_dict['Edges'] = word
       #                     edge = False
       #
       #                 if start == True:
       #                     if tmp % 2 == 0:
       #                         from_node.append(word)
       #                     else:
       #                         to_node.append(word)
       #                 if word == "Nodes:":
       #                     node = True
       #                 if word == "Edges:":
       #                     edge = True
       #
       #                 if word == "ToNodeId":
       #                     start = True
       #                 tmp += 1
       #
       #         df['FromNodeId'] = from_node
       #         df['ToNodeId'] = to_node
       #         df['Nodes'] = graph_dict["Nodes"]
       #         df['Edges'] = graph_dict["Edges"]
       #
       #     # you might wanna edit this path to save the file to your preferred location
       #     # df.to_csv(r"csv\amazon.csv")
       #     df.to_csv(path.CSV_NETWORK_DIR_PATH + "\\" + graph_name + ".csv")



# class Graph:
#     def __init__(self, input_file):
#         self.graph_file = input_file
#         self.loaded = False
#         self.read()
#
#     def read(self):
#         """
#         Read the graph from the input file provided.
#         Stores the graph internally in a compressed sparse row format.
#         """
#         if self.loaded:
#             return
#         self.vertices = [] # the accumulated number of neighbors for vertices
#         self.edges = [] # neighbors for each vertex
#         self.degrees = [] # the degree for each vertex
#         with open(self.graph_file, "r") as input_graph:
#             # for line in input_graph:
#             #     if line.startswith('#'):
#             #         continue
#             #     self.vertices.append(len(self.edges))
#             #     cleaned_line = line.rstrip("\n")
#             #     # special case: no neighbor
#             #     if cleaned_line == "":
#             #         self.degrees.append(0)
#             #     else:
#             #         destinations = cleaned_line.split()
#             #         self.degrees.append(len(destinations))
#             #         for destination in destinations:
#             #             self.edges.append(int(destination))
#             for line in input_graph:
#                 self.vertices.append(len(self.edges))
#                 cleaned_line = line.rstrip("\n")
#                 # special case: no neighbor
#                 if cleaned_line == "":
#                     self.degrees.append(0)
#                 else:
#                     destinations = cleaned_line.split(" ")
#                     self.degrees.append(len(destinations))
#                     for destination in destinations:
#                         self.edges.append(int(destination))
#         self.vertices.append(len(self.edges))
#         # count |V| and |E|
#         self.vertex_count = len(self.vertices) - 1
#         self.edge_count = len(self.edges)
#         self.loaded = True
#
#     def neighbor_of(self, vertex):
#         start_index = self.vertices[vertex]
#         end_index = self.vertices[vertex + 1]
#         return self.edges[start_index:end_index]
#
#     def get_vertices(self):
#         return range(self.get_vertex_count())
#
#     def get_vertex_count(self):
#         return self.vertex_count
#
#     def get_edge_count(self):
#         return self.edge_count
#
#     def get_degrees(self):
#         return self.degrees
