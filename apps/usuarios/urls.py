from django.urls import include, path

from usuarios.views import ingreso

urlpatterns = [
    path('', ingreso, name='ingreso'),
]