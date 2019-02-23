from . import views
from django.contrib import admin
from django.urls import path


app_name = 'home'

urlpatterns = [
    path('', views.HomeView.as_view(), name='HomeView'),
    path('results/', views.ResultsView.as_view(), name='ResultsView'),
]