from __future__ import unicode_literals

from django.db import models
from django.utils import timezone
from django.contrib.auth.models import AbstractBaseUser
from django.contrib.auth.models import BaseUserManager
from django.conf import settings


"""
Manager de usuarios
"""
class UsuarioManager(BaseUserManager):

    """
    Crea y persiste un usuario SIN privilegios de admin

    Parameters
    ----------
    email : Correo electronico valido
    password : Clave

    Returns
    -------
    Usuario creado

    """
    def create_user(self, email, password=None):
        user = self.model(email=email)
        user.set_password(password)
        user.is_staff = false;
        user.is_active = True;
        user.save()
        return user

    """
    Crea y persiste un usuario CON privilegios de admin

    Parameters
    ----------
    email : Correo electronico valido
    password : Clave

    Returns
    -------
    Usuario creado

    """
    def create_superuser(self, email, password):
        user = self.model(email=email)
        user.set_password(password)
        user.is_staff = True;
        user.is_active = True;
        user.save()
        return user

"""
Modelo que representa un usuario
"""
class Usuario(AbstractBaseUser):
    email = models.EmailField(max_length=100, unique=True)
    nombre = models.CharField(max_length=100)
    apellidos = models.CharField(max_length=200)
    objects = UsuarioManager()
    is_staff = models.BooleanField(default=False)
    is_active = models.BooleanField(default=True)
    USERNAME_FIELD = 'email'

    """
    Identificador largo del usuario

    Returns
    -------
    Email del usuario

    """
    def get_full_name(self):
        return self.email


    """
    Identificador corto del usuario

    Returns
    -------
    Email del usuario

    """
    def get_short_name(self):
        return self.email

    """
    Determina si el usuario tiene permiso para manipular un objeto

    Parameters
    ----------
    perm : Permisos
    obj : Objeto

    Returns
    -------
    Siempre True (no usamos sistema de permisos)

    """
    def has_perm(self, perm, obj=None):
        return True

    """
    Determina si el usuario tiene permiso para utilizar una aplicacion

    Parameters
    ----------
    app_label : Nombre de la aplicacion

    Returns
    -------
    Siempre True (no usamos sistema de permisos)

    """
    def has_module_perms(self, app_label):
        return True

"""
Modelo que representa una tarea lanzada por un usuario
"""
class Tarea(models.Model):
    usuario = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    tipo = models.CharField(max_length=100)
    username = models.CharField(max_length=20)
    idioma = models.CharField(max_length=2)
    num_usuarios = models.PositiveSmallIntegerField()
    inicio = models.DateTimeField()
    fin = models.DateTimeField(null=True)
