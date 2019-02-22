from django.shortcuts import render
from django.views.generic import View
from .forms import UploadNetworkForm
import pandas as pd
from ns import settings


# Create your views here.
class HomeView(View):
    template_name = 'home/index.html'
    form_class = UploadNetworkForm

    def get(self, request):
        form = self.form_class(None)

        return render(request, self.template_name, {'form': form})

    def post(self, request):
        form = self.form_class(request.POST, request.FILES)

        if form.is_valid():
            file = form.save(commit=False)
            network_file = request.FILES['network_file']
            network_filename = request.FILES['network_file'].name

            file_name, file_format = network_filename.rsplit(".", maxsplit=1)
            file.save()

        # convert_txt_to_csv(file_name, file_format, network_file)

        return render(request, self.template_name, {'form': form})


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

    with open(settings.MEDIA_ROOT+'/network_files/'+file_name+'.'+file_format) as f:
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
    save_file_to = settings.MEDIA_ROOT+'/network_csv_files/'+file_name+'.csv'
    df.to_csv(save_file_to)
