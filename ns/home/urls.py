from . import views
from django.contrib import admin
from django.urls import path



app_name = 'home'

urlpatterns = [
    path('', views.HomeView.as_view(), name='index'),

    path('results/<r_nodes>/<r_prob>/<network_filename>', views.NetworkResultsView.as_view(), name='NetworkResultsView'),
]


