from django.shortcuts import render
from django.views.generic import View
from .forms import NetworkForm
import pandas as pd
from ns import settings
from django.shortcuts import redirect
from .utils.random_network.random_network import _compute_random_network_properties
from .utils.real_network.real_network import _compute_real_network_properties, _load_graph_csv_from_file_system
from .utils.scale_free_network.scale_free_network import _compute_scale_free_properties
from multiprocessing import Pool
from .utils.real_network import graph


# Create your views here.
class HomeView(View):
    template_name = 'home/index.html'
    # form_class_upload = UploadNetworkForm
    # form_class_generate = GenerateRandomNetworkForm
    form_class_network = NetworkForm

    def get(self, request):
        # form_upload = self.form_class_upload(None)
        # form_generate = self.form_class_generate(None)
        form_network = self.form_class_network(None)

        return render(request, self.template_name, {'form_network': form_network})

    def post(self, request):
        form_network = self.form_class_network(request.POST, request.FILES)
        if form_network.is_valid():
            file = form_network.save(commit=False)

            network_file = request.FILES['network_file']
            network_filename = request.FILES['network_file'].name

            r_nodes = request.POST['number_of_nodes']
            r_prob = request.POST['probability']

            file_name, file_format = network_filename.rsplit(".", maxsplit=1)
            file.save()
            convert_txt_to_csv(file_name, file_format, network_file)

            return redirect('home:NetworkResultsView', r_nodes=r_nodes, r_prob=r_prob, network_filename=file_name)

        return render(request, self.template_name, {'form_network': form_network})


class NetworkResultsView(View):
    template_name = 'home/network_results.html'

    def get(self, request, r_nodes, r_prob, network_filename):
        #n = int(request.GET.get('nodes', '5'))
        #p = float(request.GET.get('prob', '0.5'))
        r_nodes = int(r_nodes)
        r_prob = float(r_prob)

        scale_free_network = _load_graph_csv_from_file_system(network_filename)
        real_network_graph = graph.Graph(network_filename)

        random_properties = _compute_random_network_properties('Random_Network', r_nodes, r_prob)
        scale_properties = _compute_scale_free_properties(scale_free_network)
        real_properties = _compute_real_network_properties(real_network_graph)

        if 'expected_diameter' in random_properties and 'expected_average_distance' in random_properties:
            return render(request, self.template_name, {
                'ra_p': random_properties['p'],
                'ra_expected_no_of_nodes': random_properties['expected_no_of_nodes'],
                'ra_expected_no_of_edges': random_properties['expected_no_of_edges'],
                'ra_expected_average_degree': random_properties['expected_average_degree'],
                'ra_expected_regime_type': random_properties['expected_regime_type'],
                'ra_expected_clustering_coefficient': random_properties['expected_clustering_coefficient'],

                'ra_expected_diameter': random_properties['expected_diameter'],
                'ra_expected_average_distance': random_properties['expected_average_distance'],

                'ra_expected_degree_distribution_plot_file_name': random_properties['expected_degree_distribution_plot_file_name'],
                'ra_expected_degree_distribution_plot_file_path': settings.MEDIA_URL + '/plot/' + random_properties['expected_degree_distribution_plot_file_name'],

                'ra_expected_distance_distribution_plot_file_name': random_properties['expected_distance_distribution_plot_file_name'],
                'ra_expected_distance_distribution_plot_file_path': settings.MEDIA_URL + '/plot/' + random_properties['expected_distance_distribution_plot_file_name'],

                'ra_degree_centrality_interactive_graph': random_properties['degree_centrality_interactive_graph'],
                'ra_betweeness_interactive_graph': random_properties['betweeness_interactive_graph'],
                'ra_closeness_interactive_graph': random_properties['closeness_interactive_graph'],
                'ra_interactive_network_plot': random_properties['interactive_network_plot'],


                're_no_of_nodes': real_properties['no_of_nodes'],
                're_no_of_edges': real_properties['no_of_edges'],
                're_real_kmax': real_properties['real_kmax'],
                're_real_kmin': real_properties['real_kmin'],
                're_average_degree': real_properties['average_degree'],
                're_avg_clustering_coef': real_properties['avg_clustering_coef'],
                're_global_clustering_coefficient': real_properties['global_clustering_coefficient'],
                're_degree_first_moment': real_properties['degree_first_moment'],
                're_degree_second_moment': real_properties['degree_second_moment'],
                're_degree_third_moment': real_properties['degree_third_moment'],

                're_cluster_coeff_plot_file_name': real_properties['cluster_coeff_plot_file_name'],
                're_cluster_coeff_plot_file_path': settings.MEDIA_URL + '/plot/' + real_properties['cluster_coeff_plot_file_name'],

                're_degree_corr_plot_file_name': real_properties['degree_corr_plot_file_name'],
                're_degree_corr_plot_file_path': settings.MEDIA_URL + '/plot/' + real_properties['degree_corr_plot_file_name'],

                're_degree_prob_distribution_plot_file_name': real_properties['degree_prob_distribution_plot_file_name'],
                're_degree_prob_distribution_plot_file_path': settings.MEDIA_URL + '/plot/' + real_properties['degree_prob_distribution_plot_file_name'],

                're_real_network_graph_file_name': real_properties['real_network_graph'],
                're_real_network_graph_file_path': settings.MEDIA_URL + '/plot/' + real_properties['real_network_graph'],


                'sc_expected_kmax': scale_properties['expected_kmax'],
                'sc_expected_average_distance': scale_properties['expected_average_distance'],
                'sc_expected_degree_exponent': scale_properties['expected_degree_exponent']
            })
        else:
            return render(request, self.template_name, {
                'ra_p': random_properties['p'],
                'ra_expected_no_of_nodes': random_properties['expected_no_of_nodes'],
                'ra_expected_no_of_edges': random_properties['expected_no_of_edges'],
                'ra_expected_average_degree': random_properties['expected_average_degree'],
                'ra_expected_regime_type': random_properties['expected_regime_type'],
                'ra_expected_clustering_coefficient': random_properties['expected_clustering_coefficient'],

                #'ra_expected_diameter': random_properties['expected_diameter'],
                #'ra_expected_average_distance': random_properties['expected_average_distance'],

                'ra_expected_degree_distribution_plot_file_name': random_properties[
                    'expected_degree_distribution_plot_file_name'],
                'ra_expected_degree_distribution_plot_file_path': settings.MEDIA_URL + '/plot/' + random_properties[
                    'expected_degree_distribution_plot_file_name'],

                'ra_expected_distance_distribution_plot_file_name': random_properties[
                    'expected_distance_distribution_plot_file_name'],
                'ra_expected_distance_distribution_plot_file_path': settings.MEDIA_URL + '/plot/' + random_properties[
                    'expected_distance_distribution_plot_file_name'],

                'ra_degree_centrality_interactive_graph': random_properties['degree_centrality_interactive_graph'],
                'ra_betweeness_interactive_graph': random_properties['betweeness_interactive_graph'],
                'ra_closeness_interactive_graph': random_properties['closeness_interactive_graph'],
                'ra_interactive_network_plot': random_properties['interactive_network_plot'],

                're_no_of_nodes': real_properties['no_of_nodes'],
                're_no_of_edges': real_properties['no_of_edges'],
                're_real_kmax': real_properties['real_kmax'],
                're_real_kmin': real_properties['real_kmin'],
                're_average_degree': real_properties['average_degree'],
                're_avg_clustering_coef': real_properties['avg_clustering_coef'],
                're_global_clustering_coefficient': real_properties['global_clustering_coefficient'],
                're_degree_first_moment': real_properties['degree_first_moment'],
                're_degree_second_moment': real_properties['degree_second_moment'],
                're_degree_third_moment': real_properties['degree_third_moment'],

                're_cluster_coeff_plot_file_name': real_properties['cluster_coeff_plot_file_name'],
                're_cluster_coeff_plot_file_path': settings.MEDIA_URL + '/plot/' + real_properties[
                    'cluster_coeff_plot_file_name'],

                're_degree_corr_plot_file_name': real_properties['degree_corr_plot_file_name'],
                're_degree_corr_plot_file_path': settings.MEDIA_URL + '/plot/' + real_properties[
                    'degree_corr_plot_file_name'],

                're_degree_prob_distribution_plot_file_name': real_properties[
                    'degree_prob_distribution_plot_file_name'],
                're_degree_prob_distribution_plot_file_path': settings.MEDIA_URL + '/plot/' + real_properties[
                    'degree_prob_distribution_plot_file_name'],

                're_real_network_graph_file_name': real_properties['real_network_graph'],
                're_real_network_graph_file_path': settings.MEDIA_URL + '/plot/' + real_properties[
                    'real_network_graph'],

                'sc_expected_kmax': scale_properties['expected_kmax'],
                'sc_expected_average_distance': scale_properties['expected_average_distance'],
                'sc_expected_degree_exponent': scale_properties['expected_degree_exponent']
            })


class RandomNetworkResultsView(View):
    template_name = "home/random_network_results.html"

    def get(self, request):
        # n = 10
        # p = 0.5
        n = int(request.GET.get('nodes', '5'))
        p = float(request.GET.get('prob', '0.5'))
        # plot_div = plot_random_interactive_network(n, p)
        properties = _compute_random_network_properties(
            'Random_Network', n, p)

        return render(request, self.template_name, {
            'p': properties['p'],
            'expected_no_of_nodes': properties['expected_no_of_nodes'],
            'expected_no_of_edges': properties['expected_no_of_edges'],
            'expected_degree_distribution_plot_file_name': properties['expected_degree_distribution_plot_file_name'],
            'degree_distribution_plot_path': settings.MEDIA_URL+'/plot/'+properties['expected_degree_distribution_plot_file_name'],
            'expected_average_degree': properties['expected_average_degree'],
            'expected_regime_type': properties['expected_regime_type'],
            'expected_average_distance': properties['expected_average_distance'],
            'expected_clustering_coefficient': properties['expected_clustering_coefficient'],
            'plot': properties['interactive_network_plot']
        })


def convert_txt_to_csv(file_name, file_format, file):
    graph_dict = {"Nodes": "", "Edges": ""}

    from_node = []
    to_node = []
    df = pd.DataFrame()

    graph_name = file_name

    tmp = 0
    node = False
    edge = False
    start = False

    with open(settings.MEDIA_ROOT + '/network_files/' + file_name + '.' + file_format) as f:
        for line in f:
            for word in line.split():
                if node is True:
                    graph_dict['Nodes'] = word
                    node = False
                if edge is True:
                    graph_dict['Edges'] = word
                    edge = False

                if start is True:
                    if tmp % 2 == 0:
                        from_node.append(word)
                    else:
                        to_node.append(word)
                if word == "Nodes:":
                    node = True
                if word == "Edges:":
                    edge = True

                if word == "ToNodeId":
                    start = True
                tmp += 1

    df['FromNodeId'] = from_node
    df['ToNodeId'] = to_node
    df['Nodes'] = graph_dict["Nodes"]
    df['Edges'] = graph_dict["Edges"]

    # you might wanna edit this path to save the file to your preferred location
    save_file_to = settings.MEDIA_ROOT + '/network_csv_files/' + file_name + '.csv'
    df.to_csv(save_file_to)
