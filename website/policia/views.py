# -​*- coding: utf-8 -*​-
import datetime
import logging
from django.core.paginator import Paginator
from django.http import HttpResponse, HttpResponseRedirect
from django.shortcuts import render, get_object_or_404
from django.core.urlresolvers import reverse
from django.views import generic
from django.contrib.auth.decorators import login_required
from django.contrib.auth import authenticate, login as auth_login, logout
from django.shortcuts import redirect
from django.http import JsonResponse
from django.utils import timezone
import urllib2
from urllib2 import HTTPError
import os
import sys
import math

lib_path = os.path.abspath('../../')
sys.path.append(lib_path)
from API.APITextos import APITextos
from .models import Tarea

#########################
# API REST
#########################

def _formatTwitterFigure(n):
    millnames = ['','K','M','B','T']
    n = float(n)
    millidx = max(0,min(len(millnames)-1,
        int(math.floor(0 if n == 0 else math.log10(abs(n))/3))))
    return '{:.0f}{}'.format(n / 10**(3 * millidx), millnames[millidx])

def _formatUsersJson(usuarios):
    usuarios = map((lambda user:
        {
            'name': user.name,
            'screen_name': user.screen_name,
            'followers': _formatTwitterFigure(user.followers),
            'following': _formatTwitterFigure(user.following),
            'location': user.location,
            'created_at': user.created_at.strftime("%d/%m/%Y")
        })
        , usuarios)
    return JsonResponse({
        'status': 'ready',
        'users': usuarios
    })

def _getUsersSimilarMethod(isByUsername, searchIn, searchBy):
    if isByUsername:
        if searchIn == 'all' and searchBy == 'topic':
            return APITextos.getUsersSimilar_user_all_topic
        elif searchIn == 'all' and searchBy == 'semantic':
            return APITextos.getUsersSimilar_user_all_semantic
        elif searchIn == 'relations' and searchBy == 'topic':
            return APITextos.getUsersSimilar_user_relations_topic
        elif searchIn == 'relations' and searchBy == 'semantic':
            return APITextos.getUsersSimilar_user_relations_semantic
        else:
            raise Exception('Parámetros searchIn o searchBy incorrectos')
    else:
        if searchBy == 'topic':
            return APITextos.getUsersSimilar_text_all_topic
        elif searchBy == 'semantic':
            return APITextos.getUsersSimilar_text_all_semantic
        else:
            raise Exception('Parámetro searchBy incorrecto')

@login_required
def eliminarAPI(request, idTarea=0):
    try:
        tarea = Tarea.objects.get(pk=idTarea)
        if tarea.usuario == request.user:
            tarea.delete()
            return JsonResponse("ok", safe=False)
        else:
            return JsonResponse("permission_denied", safe=False)

    except:
        return JsonResponse("invalid_id", safe=False)


@login_required
def notificarAPI(request, idTarea=0):
    try:
        tarea = Tarea.objects.get(pk=idTarea)
        if tarea.usuario == request.user:
            tarea.enviar_email = True
            tarea.save()
            return JsonResponse("ok", safe=False)
        else:
            return JsonResponse("permission_denied", safe=False)

    except:
        return JsonResponse("invalid_id", safe=False)

def _getTipo(searchIn, searchBy, searchUsername, searchText):
    if searchUsername is None:
        return 'text_all_' + searchBy
    else:
        return 'user_' + searchIn + "_" + searchBy

def _getSearchBy(tipo):
    if 'topic' in tipo:
        return 'topic'
    else:
        return 'semantic'

def _getSearchIn(tipo):
    if 'all' in tipo:
        return 'all'
    else:
        return 'relations'

def _crearTarea(request, searchIn, searchBy, searchUsername, searchText, searchLanguage, searchMax):

    tarea = Tarea(
        usuario = request.user,
        tipo = _getTipo(searchIn, searchBy, searchUsername, searchText),
        username = searchUsername,
        texto = searchText,
        idioma = searchLanguage,
        num_usuarios = searchMax,
        inicio = timezone.now(),
        fin = None,
        enviar_email = False
    )
    tarea.save()
    return tarea.id;

def _buscarDuplicado(request, searchIn, searchBy, searchUsername, searchText, searchLanguage, searchMax):
    try:
        tarea = Tarea.objects.filter(
            # Buscar tareas creadas hoy
            inicio__gte = datetime.date.today(),
            # Por el usuario actual
            usuario = request.user,
            # Con el mismo searchIn, searchBy, searchUsername, searchText, searchLanguage, searchMax
            tipo = _getTipo(searchIn, searchBy, searchUsername, searchText),
            username = searchUsername,
            texto = searchText,
            idioma = searchLanguage,
            num_usuarios = searchMax,
        )[0]
        return tarea.id
    except Exception, e:
        return None

@login_required
def buscarSimilaresAPI(request):
    try:
        searchUsername = request.GET['search-username']
        searchLanguage = request.GET['search-language']
        searchMax = request.GET['search-max']
        searchBy = request.GET['search-by']
        searchIn = request.GET['search-in']
    except Exception, e:
        return JsonResponse({
            'status': "missing_params"
        })

    idTarea = None
    if "id" in request.GET:
        idTarea = request.GET["id"]
    else:
        idTarea = _buscarDuplicado(request, searchIn, searchBy, searchUsername, None, searchLanguage, searchMax)

    if idTarea is None:
        try:
            idTarea = _crearTarea(request, searchIn, searchBy, searchUsername, None, searchLanguage, searchMax)
        except:
            return JsonResponse({
                'status': "db_error"
            })

    try:
        method = _getUsersSimilarMethod(True, searchIn, searchBy);
        result = method(searchUsername, searchLanguage, int(searchMax), idTarea)
    except Exception, e:
        result = []

    if result == []:
        return JsonResponse({
            'status': "no_results"
        })
    elif result == False:
        return JsonResponse({
            'status': "downloading",
            'taskId': idTarea
        })
    else:
        return _formatUsersJson(result)

@login_required
def buscarTextoAPI(request):
    try:
        searchText = request.POST['search-text']
        searchLanguage = request.POST['search-language']
        searchMax = request.POST['search-max']
        searchBy = request.POST['search-by']
    except Exception, e:
        return JsonResponse({
            'status': "missing_params"
        })

    idTarea = None
    if "id" in request.POST:
        idTarea = request.POST["id"]
        print idTarea
    else:
        idTarea = _buscarDuplicado(request, 'all', searchBy, None, searchText, searchLanguage, searchMax)

    if idTarea is None:
        try:
            idTarea = _crearTarea(request, 'all', searchBy, None, searchText, searchLanguage, searchMax)
        except:
            return JsonResponse({
                'status': "db_error"
            })

    try:
        method = _getUsersSimilarMethod(False, 'all', searchBy);
        result = method(searchText, searchLanguage, int(searchMax), idTarea)
    except Exception, e:
        return JsonResponse({
            'exception': str(e),
            'status': "no_results"
        })

    if result == []:
        return JsonResponse({
            'status': "no_results"
        })
    elif result == False:
        return JsonResponse({
            'status': "downloading",
            'taskId': idTarea
        })
    else:
        return _formatUsersJson(result)


@login_required
def validarUsuarioTwitterAPI(request, usuarioTwitter):
    try:
         urllib2.urlopen("http://twitter.com/" + usuarioTwitter)
    except urllib2.HTTPError, err:
        return JsonResponse("invalid", safe=False)
    return JsonResponse("valid", safe=False)

@login_required
def textoAPI(request, idTarea):
    try:
        tarea = Tarea.objects.get(pk=idTarea)
        if tarea.usuario == request.user:
            return JsonResponse(tarea.texto, safe=False)
        else:
            return JsonResponse("", safe=False)

    except:
        return JsonResponse("", safe=False)


#########################
# Secciones del panel
#########################

def _getNumTareasFinalizadas(request):
    return Tarea.objects.filter(usuario=request.user).exclude(fin__isnull=True).count()

@login_required
def resultados(request, idTarea=0):
    try:
        tarea = Tarea.objects.get(pk=idTarea)
        if tarea.username != None:
            return HttpResponseRedirect(reverse('policia:buscarSimilares') +
                '?username=' + tarea.username +
                '&idioma=' + tarea.idioma +
                '&max=' + str(tarea.num_usuarios) +
                '&by=' + _getSearchBy(tarea.tipo) +
                '&in=' + _getSearchIn(tarea.tipo) +
                '&id=' + str(idTarea))
        else:
            return HttpResponseRedirect(reverse('policia:buscarTexto') +
                '?id=' + str(tarea.id) +
                '&idioma=' + tarea.idioma +
                '&max=' + str(tarea.num_usuarios) +
                '&by=' + _getSearchBy(tarea.tipo))

    except Exception, e:
        return HttpResponseRedirect(reverse('policia:tareas'))

@login_required
def tareas(request, page=1):
    nombre = request.user.nombre + " " + request.user.apellidos
    email = request.user.email
    tareas = Tarea.objects.filter(usuario=request.user).order_by('-inicio')
    paginator = Paginator(tareas, 10)
    anterior = int(page) - 1
    if int(page) >= paginator.num_pages:
        siguiente = 0
    else:
        siguiente = int(page) + 1

    try:
        tareas = paginator.page(page)
    except:
        tareas = []

    return render(request, "policia/tareas.html", {
        'nombre': nombre,
        'email': email,
        'titulo': 'Tareas pendientes',
        'tareas': tareas,
        'pagina': page,
        'anterior': anterior,
        'siguiente':siguiente,
        'numTareasFinalizadas': _getNumTareasFinalizadas(request)
    })

@login_required
def buscarSimilares(request):
    nombre = request.user.nombre + " " + request.user.apellidos
    email = request.user.email

    return render(request, "policia/buscar-similares.html", {
        'nombre': nombre,
        'email': email,
        'titulo': 'Búsqueda de usuarios similares',
        'numTareasFinalizadas': _getNumTareasFinalizadas(request)
    })

@login_required
def buscarTexto(request):
    nombre = request.user.nombre + " " + request.user.apellidos
    email = request.user.email
    return render(request, "policia/buscar-texto.html", {
        'nombre': nombre,
        'email': email,
        'titulo': 'Búsqueda de usuarios por texto',
        'numTareasFinalizadas': _getNumTareasFinalizadas(request)
    })
def buscarTiempo(request):
    nombre = request.user.nombre + " " + request.user.apellidos
    email = request.user.email
    return render(request, "policia/buscar-tiempo.html", {
        'nombre': nombre,
        'email': email,
        'titulo': 'Búsqueda de usuarios tiempo en la publicación',
        'numTareasFinalizadas': _getNumTareasFinalizadas(request)
    })
#########################
# Sitema de autenticación
#########################
def login(request, code=None):
    if code == "0":
        error = "El usuario indicado fue deshabilitado."
    elif code == "1":
        error = "El email o contraseña indicados no son válidos."
    else:
        error = None
    return render(request, "policia/login.html", { 'error': error })

def salir(request):
    logout(request)
    return redirect("/")

def autenticar(request):
    email = request.POST['login-email']
    password = request.POST['login-password']
    user = authenticate(email=email, password=password)
    if user is not None:
        if user.is_active:
            # login ok
            auth_login(request, user)
            return redirect('/')
        else:
            # inactive user error
            return HttpResponseRedirect(reverse('policia:login', args=(0,)))
    else:
        # invalid user or password
        return HttpResponseRedirect(reverse('policia:login', args=(1,)))
