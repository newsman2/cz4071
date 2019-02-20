from . import views
from django.contrib import admin
from django.urls import path

urlpatterns = [
    path('', views.HomeView.as_view(), name='home'),
]