from __future__ import unicode_literals

from django.db import models
from django.utils import timezone
from django.contrib.auth.models import AbstractBaseUser
from django.contrib.auth.models import BaseUserManager
from django.conf import settings

class UsuarioManager(BaseUserManager):
    """
    Manager de usuarios
    """

    def create_user(self, email, password=None):
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
        user = self.model(email=email)
        user.set_password(password)
        user.is_staff = false;
        user.is_active = True;
        user.save()
        return user

    def create_superuser(self, email, password):
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
        user = self.model(email=email)
        user.set_password(password)
        user.is_staff = True;
        user.is_active = True;
        user.save()
        return user

class Usuario(AbstractBaseUser):
    """
    Modelo que representa un usuario
    """
    email = models.EmailField(max_length=100, unique=True)
    nombre = models.CharField(max_length=100)
    apellidos = models.CharField(max_length=200)
    objects = UsuarioManager()
    is_staff = models.BooleanField(default=False)
    is_active = models.BooleanField(default=True)
    USERNAME_FIELD = 'email'

    def get_full_name(self):
        """
        Identificador largo del usuario

        Returns
        -------
        Email del usuario

        """
        return self.email

    def get_short_name(self):
        """
        Identificador corto del usuario

        Returns
        -------
        Email del usuario

        """
        return self.email

    def has_perm(self, perm, obj=None):
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
        return True

    def has_module_perms(self, app_label):
        """
        Determina si el usuario tiene permiso para utilizar una aplicacion

        Parameters
        ----------
        app_label : Nombre de la aplicacion

        Returns
        -------
        Siempre True (no usamos sistema de permisos)

        """
        return True

class Tarea(models.Model):
    """
    Modelo que representa una tarea lanzada por un usuario
    """
    usuario = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    tipo = models.CharField(max_length=100)
    username = models.CharField(max_length=20)
    idioma = models.CharField(max_length=2)
    num_usuarios = models.PositiveSmallIntegerField()
    inicio = models.DateTimeField()
    fin = models.DateTimeField(null=True)
