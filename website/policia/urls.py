from django.conf.urls import url
from . import views

app_name = 'policia'

urlpatterns = [

    # API REST
    url(r'^api/buscar/similares/$', views.buscarSimilaresAPI, name='buscarSimilaresAPI'),
    url(r'^api/buscar/texto/$', views.buscarTextoAPI, name='buscarTextoAPI'),
    url(r'^api/buscar/tiempo/$', views.buscarTiempoAPI, name='buscarTiempoAPI'),
    url(r'^api/validar/usuario/(?P<usuarioTwitter>\w+)/$', views.validarUsuarioTwitterAPI, name='validarUsuarioTwitterAPI'),
    url(r'^api/tarea/notificar/(?P<idTarea>[0-9]+)/$', views.notificarAPI, name='notificarAPI'),
    url(r'^api/tarea/texto/(?P<idTarea>[0-9]+)/$', views.textoAPI, name='textoAPI'),
    url(r'^api/tarea/eliminar/(?P<idTarea>[0-9]+)/$', views.eliminarAPI, name='eliminarAPI'),

    # Sistema de autenticacion de usuarios
    url(r'^login/$', views.login, name='login'),
    url(r'^login/(?P<code>[0-9]{1})/$', views.login, name='login'),
    url(r'^autenticar/$', views.autenticar, name='autenticar'),
    url(r'^salir/$', views.salir, name='salir'),

    # Secciones del panel del control
    url(r'^resultados/(?P<idTarea>[0-9]+)/$', views.resultados, name='resultados'),
    url(r'^buscar/similares/$', views.buscarSimilares, name='buscarSimilares'),
    url(r'^buscar/tiempo/$', views.buscarTiempo, name='buscarTiempo'),
    url(r'^buscar/texto/$', views.buscarTexto, name='buscarTexto'),
    url(r'^$', views.tareas, name='tareas'),
    url(r'^tareas/(?P<page>[0-9]+)/$', views.tareas, name='tareas'),

]
