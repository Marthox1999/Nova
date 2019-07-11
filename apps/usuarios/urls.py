from django.urls import include, path

from usuarios.views import ingreso, paginaPrincipal_admin

urlpatterns = [
    path('', ingreso, name='ingreso'),
    path('principalAdmin/',paginaPrincipal_admin,name='paginaPrincipal_admin'),
] 