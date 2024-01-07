from django.contrib import admin
from django.urls import path
from . import views

urlpatterns = [
    path('', views.index, name='home') # a path to index home page
]
