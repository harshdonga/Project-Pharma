from django.contrib import admin
from django.urls import path , include
from . import views
urlpatterns = [
    path('', views.home , name = 'home'),
    path('manufacturers/', include('manufacturers.urls')),
    path('logistics/', include('logistics.urls')),
]