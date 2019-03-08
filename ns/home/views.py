from django.shortcuts import render
from django.views.generic import View
from .forms import UploadNetworkForm, GenerateRandomNetworkForm
import pandas as pd
from ns import settings
from django.shortcuts import redirect
from .utils.random_network import _compute_random_network_properties
from .utils.real_network.real_network import _compute_real_network_properties, _load_graph_csv_from_file_system, _is_network_too_big, plot_real_interactive_network
from multiprocessing import Pool


# Create your views here.
class HomeView(View):
    template_name = 'home/index.html'
    form_class_upload = UploadNetworkForm
    form_class_generate = GenerateRandomNetworkForm

    def get(self, request):
        form_upload = self.form_class_upload(None)
        form_generate = self.form_class_generate(None)

        return render(request, self.template_name, {'form_upload': form_upload, 'form_generate': form_generate})

    def post(self, request):
        form_upload = self.form_class_upload(request.POST, request.FILES)
        form_generate = self.form_class_generate(request.POST)
        if 'btn_upload' in request.POST:
            if form_upload.is_valid():
                file = form_upload.save(commit=False)
                network_file = request.FILES['network_file']
                network_filename = request.FILES['network_file'].name

                file_name, file_format = network_filename.rsplit(".", maxsplit=1)
                file.save()
                convert_txt_to_csv(file_name, file_format, network_file)
            return redirect('home:RealNetworkResults', network_filename=file_name)

        elif 'btn_generate' in request.POST:
            if form_generate.is_valid():
                n = request.POST['number_of_nodes']
                p = request.POST['probability']

            url = '/results/random/?nodes=' + n + '&prob=' + p
            return redirect(url)

        return render(request, self.template_name, {'form_upload': form_upload, 'form_generate': form_generate})


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


class RealNetworkResultsView(View):
    template_name = 'home/real_network_results.html'

    def get(self, request, network_filename):

        network = _load_graph_csv_from_file_system(network_filename)
        is_too_big = _is_network_too_big(network.number_of_nodes(), network.number_of_edges(), network, network_filename)

        if is_too_big:
            return render(request, self.template_name, {
                'is_too_big': is_too_big,
                'no_of_nodes': network.number_of_nodes(),
                'no_of_edges': network.number_of_edges(),
                'degree_distribution_plot_path_file_name': network_filename,
                'degree_distribution_plot_path': settings.MEDIA_URL + 'plot/' + network_filename + '_degree_distribution_log_binning.png',

            })
        else:
            properties = _compute_real_network_properties(network_filename, network)
            return render(request, self.template_name, {
                'no_of_nodes': properties['no_of_nodes'],
                'no_of_edges': properties['no_of_edges'],
                'average_degree': properties['average_degree'],
                'degree_second_moment': properties['degree_second_moment'],
                'real_kmax': properties['real_kmax'],
                'real_kmin': properties['real_kmin'],
                'average_distance': properties['average_distance'],
                'diameter': properties['diameter'],
                'global_clustering_coefficient': properties['global_clustering_coefficient'],
                'average_clustering_coefficient': properties['average_clustering_coefficient']
            })


class ScaleFreeNetworkResultsView(View):
    template_name = 'home/scale_free_network_results.html'

    def get(self, request):

        properties = _compute_real_network_properties()

        return render(request, self.template_name, {
            'is_too_big': properties['is_too_big'],
            'analyzed_network_properties': properties['analyzed_network_properties']
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
