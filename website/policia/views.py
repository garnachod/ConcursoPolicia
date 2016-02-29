# -​*- coding: utf-8 -*​-

from django.http import HttpResponse, HttpResponseRedirect
from django.shortcuts import render, get_object_or_404
from django.core.urlresolvers import reverse
from django.views import generic
from django.contrib.auth.decorators import login_required
from django.contrib.auth import authenticate, login as auth_login, logout
from django.shortcuts import redirect
from django.http import JsonResponse
from django.utils import timezone
import os
import sys
import math

lib_path = os.path.abspath('../../')
sys.path.append(lib_path)
from API.APITextos import APITextos
from .models import Tarea

# IMPORTANTE: Abreviar cifras de seguidores/siguiendo
# http://stackoverflow.com/questions/25611937/abbreviate-a-localized-number-in-javascript-for-thousands-1k-and-millions-1m

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
    return JsonResponse({ 'users': usuarios })

@login_required
def buscarSimilaresAPI(request):
    try:
        searchUsername = request.GET['search-username']
        searchLanguage = request.GET['search-language']
        searchMax = request.GET['search-max']
        searchBy = request.GET['search-by']
        searchIn = request.GET['search-in']
    except Exception, e:
        return JsonResponse("missing_params", safe=False)

    tarea = Tarea(
        usuario = request.user,
        tipo = "user_" + searchIn + "_" + searchBy,
        username = searchUsername,
        idioma = searchLanguage,
        num_usuarios = searchMax,
        inicio = timezone.now(),
        fin = None,
        enviar_email = False
    )
    tarea.save()
    username = searchUsername
    language = searchLanguage
    maxResults = int(searchMax)
    idTarea = tarea.id

    method = 'APITextos.getUsersSimilar_user_' + searchIn + '_' + searchBy + '(username, language, maxResults, idTarea)'

    try:
        result = eval(method)
    except Exception, e:
        result = []

    if result == []:
        return JsonResponse("no_results", safe=False)
    elif result == False:
        return JsonResponse("downloading", safe=False)
    else:
        return _formatUsersJson(result)

#########################
# Secciones del panel
#########################
@login_required
def tareas(request):
    nombre = request.user.nombre + " " + request.user.apellidos
    email = request.user.email

    return render(request, "policia/tareas.html", {
        'nombre': nombre,
        'email': email,
        'titulo': 'Tareas pendientes'
    })

@login_required
def buscarSimilares(request):
    nombre = request.user.nombre + " " + request.user.apellidos
    email = request.user.email

    return render(request, "policia/buscar-similares.html", {
        'nombre': nombre,
        'email': email,
        'titulo': 'Búsqueda de usuarios similares'
    })

@login_required
def buscarTexto(request):
    nombre = request.user.nombre + " " + request.user.apellidos
    email = request.user.email
    return render(request, "policia/buscar-texto.html", {
        'nombre': nombre,
        'email': email,
        'titulo': 'Búsqueda de usuarios por texto'
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
