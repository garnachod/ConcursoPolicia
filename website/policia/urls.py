from django.conf.urls import url
from . import views

app_name = 'policia'

urlpatterns = [
    url(r'^login/$', views.login, name='login'),
    url(r'^login/(?P<code>[0-9]{1})/$', views.login, name='login'),
    url(r'^autenticar/$', views.autenticar, name='autenticar'),
    url(r'^salir/$', views.salir, name='salir'),
    url(r'^buscar/similares/$', views.buscarSimilares, name='buscarSimilares'),
    url(r'^buscar/texto/$', views.buscarTexto, name='buscarTexto'),
    url(r'^$', views.tareas, name='tareas'),
]
