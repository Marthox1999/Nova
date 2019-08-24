from django.urls import include, path
from reportes.views import *
from django.contrib.auth import views as auth_views

app_name='reportes'

urlpatterns = [
    path('masVendidos/', masVendidos, name='masVendidos'),

]
