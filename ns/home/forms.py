from django import forms
from django.forms import TextInput, PasswordInput, SelectDateWidget, RadioSelect, DateInput, Select, FileInput
from .models import Network


class UploadNetworkForm(forms.ModelForm):
    # network_file = forms.Widget(widget=forms.FileInput(attrs={'class': 'form-control', 'id': 'network_file'}), label='Network File')

    class Meta:
        model = Network
        fields = ['network_file']
        widgets = {'network_file': FileInput(
            attrs={'class': 'form-control-file', 'id': 'network_file', 'label': 'Network File'})}


class GenerateRandomNetworkForm(forms.Form):
    number_of_nodes = forms.IntegerField(
        widget=forms.TextInput(
            attrs={'class': 'form-control', 'id': 'number_of_nodes', 'placeholder': '# of Nodes'}), required=False)
    probability = forms.FloatField(
        widget=forms.TextInput(
            attrs={'class': 'form-control', 'id': 'probability', 'placeholder': 'Probability'}), required=False)
