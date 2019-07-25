from django.contrib import admin
from django.urls import path, include
from . import views

urlpatterns = [
    path('', views.index , name = 'index'),
    path('task', views.task , name = 'task'),
    path('medtransact', views.medtransact, name = 'medtransact')
]