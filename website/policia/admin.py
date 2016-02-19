from django.contrib import admin
from django import forms
from django.contrib.auth.admin import UserAdmin
from django.contrib.auth.forms import ReadOnlyPasswordHashField
from django.contrib.auth.models import Group
from django.contrib.auth.forms import UserChangeForm, UserCreationForm

from .models import Usuario

class UsuarioCreationForm(UserCreationForm):
    """
    Formulario para la creacion de nuevos usuarios.
    """
    password1 = forms.CharField(label='Clave', widget=forms.PasswordInput)
    password2 = forms.CharField(label='Repita la clave', widget=forms.PasswordInput)

    class Meta:
        """
        Configuracion del modelo de usuario.
        """
        model = Usuario
        fields = ('email', 'nombre', 'apellidos',)

    def clean_password2(self):
        """
        Compara los passwords escritos en el formulario.

        Returns
        -------
        Password validado.

        """
        password1 = self.cleaned_data.get("password1")
        password2 = self.cleaned_data.get("password2")
        if password1 and password2 and password1 != password2:
            raise forms.ValidationError("Las claves no coinciden")
        return password2

    def save(self, commit=True):
        """
        Crea y opcionalmente persiste un usuario

        Parameters
        ----------
        commit : Boolean para persistir o no el usuario

        Returns
        -------
        El objeto usuario creado

        """
        user = super(UserCreationForm, self).save(commit=False)
        user.set_password(self.cleaned_data["password1"])
        if commit:
            user.save()
        return user

class UsuarioChangeForm(forms.ModelForm):
    """
    Formulario para modificar datos de un usuario existente
    """
    password = ReadOnlyPasswordHashField()

    class Meta:
        """
        Configuracion del modelo de usuario.
        """
        model = Usuario
        fields = ('email', 'password', 'nombre', 'apellidos', 'is_active', 'is_staff')

    def clean_password(self):
        """
        Returns
        -------
        El password inicial
        """
        return self.initial["password"]

class UsuarioAdmin(UserAdmin):
    """
    Configuracion del panel de administracion
    """
    form = UsuarioChangeForm
    add_form = UsuarioCreationForm

    # Campos a usar para mostrar el modelo Usuario
    list_display = ('email', 'nombre', 'apellidos', 'is_staff')
    list_filter = ('is_staff',)
    fieldsets = (
        (None, {'fields': ('email', 'password')}),
        ('Datos personales', {'fields': ('nombre', 'apellidos', )}),
        ('Permisos', {'fields': ('is_staff',)}),
    )

    # Sobreescribimos los campos a usar cuando se crea un usuario nuevo
    add_fieldsets = (
        (None, {
            'classes': ('wide',),
            'fields': ('email', 'nombre', 'apellidos', 'password1', 'password2')}
        ),
    )
    search_fields = ('email',)
    ordering = ('email',)
    filter_horizontal = ()

# Registramos el modelo Usuario para mostrarlo en el panel de administracion
admin.site.register(Usuario, UsuarioAdmin)

# No hacemos uso del sistema de permisos de Django
admin.site.unregister(Group)
