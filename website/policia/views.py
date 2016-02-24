# -​*- coding: utf-8 -*​-

from django.http import HttpResponse, HttpResponseRedirect
from django.shortcuts import render, get_object_or_404
from django.core.urlresolvers import reverse
from django.views import generic
from django.contrib.auth.decorators import login_required
from django.contrib.auth import authenticate, login as auth_login, logout
from django.shortcuts import redirect

@login_required
def tareas(request):
    nombre = request.user.nombre + " " + request.user.apellidos
    email = request.user.email
    return render(request, "policia/tareas.html", {
        'nombre': nombre,
        'email': email
    })

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
