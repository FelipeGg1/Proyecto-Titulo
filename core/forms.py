from dataclasses import field, fields
from django import forms
from django.forms import ModelForm

from core.models import *

#
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth import get_user_model

User = get_user_model()


class LoginForm(forms.Form):
    username = forms.CharField()
    password = forms.CharField(widget=forms.PasswordInput())




class PerfilForm(ModelForm):
    
    username = forms.CharField(label='Nombre De Usuario:',max_length=15)
    password = forms.CharField(label='Contraseña:',max_length=15)
    nombre = forms.CharField(label='Nombre:',max_length=15)
    apellido = forms.CharField(label='Apellido:',max_length=15)
    email = forms.EmailField(label='Correo:',max_length=50)
    is_pyme = forms.BooleanField(label='Soy Pyme:',required=False)
    is_persona = forms.BooleanField(label='Soy Persona:',required=False)
    
    
    

    class Meta: 
        model = User
        fields = ['username', 'password', 'nombre', 'apellido', 'email','is_pyme','is_persona']
    
    

        

# class PersonaForm(ModelForm):
#     numero_contac = forms.IntegerField(label='Numero de Contacto:')

#     class Meta:
#         model = Persona
#         fields = ['numero_contac']
USER_CHOICES = (
    ('pyme','PYME'),
    ('persona', 'PERSONA'),
)
USER_MUNI_CHOICES = (
    ('encargado','Encargado'),
    ('admin','Admin'),
    ('trabajador','Trabajador')
)
PRODUCTO_CHOICES = (
    ('materia_prima','MATERIA_PRIMA'),
    ('producto_final', 'PRODUCTO_FINAL'),
)

class CustomUserCreationform(UserCreationForm):
    tipo_user = forms.ChoiceField(label='Tipo de usuario',choices=USER_CHOICES, initial='persona')
    numero_contac = forms.IntegerField(label='Numero de contacto')
    imagen  = forms.ImageField(label='Imagen De perfil:')
    first_name = forms.CharField(label='Nombre:',max_length=40)
    last_name = forms.CharField(label='Apellido:',max_length=40)
    
    class Meta:
        model = User
        fields = ['username', "password1", "password2", 'tipo_user','numero_contac','imagen','email','first_name','last_name']
        def __init__(self, *args, **kwargs):
            super(CustomUserCreationform, self).__init__(*args, **kwargs)
            self.fields['tipo_user'].initial = 'persona'

    def __init__(self, *args, **kwargs):
        super(CustomUserCreationform, self).__init__(*args, **kwargs)
        for field_name in ('username', 'password1', 'password2', 'tipo_user'):
            self.fields[field_name].help_text = ''

class USuarioEncarForm(CustomUserCreationform):
    tipo_user = forms.ChoiceField(label='Tipo de usuario',choices=USER_MUNI_CHOICES, initial='encargado')
    def __init__(self, *args, **kwargs):
            super(USuarioEncarForm, self).__init__(*args, **kwargs)
            self.fields['tipo_user'].initial = 'encargado'
            self.fields['tipo_user'].widget = forms.HiddenInput()
            self.fields['is_superuser'].initial = True
            self.fields['is_superuser'].widget = forms.HiddenInput()
            self.fields['is_staff'].initial = True
            self.fields['is_staff'].widget = forms.HiddenInput()
            
    
    class Meta:
        model = usuarioEncarga
        fields = ['username', "password1", "password2", 'tipo_user','numero_contac','cargo','is_superuser','is_staff','Municipalidad','imagen','email','first_name','last_name']

class USuarioTrabajForm(CustomUserCreationform):
    tipo_user = forms.ChoiceField(label='Tipo de usuario',choices=USER_MUNI_CHOICES, initial='trabajador')
    def __init__(self, *args, **kwargs):
            super(USuarioTrabajForm, self).__init__(*args, **kwargs)
            self.fields['tipo_user'].initial = 'trabajador'
            self.fields['tipo_user'].widget = forms.HiddenInput()

    class Meta:
        model = usuarioTrabaj
        fields = ['username', "password1", "password2", 'tipo_user','numero_contac','cargo','tienda_fisica','imagen','email','first_name','last_name']

class oferta_empleoform(ModelForm):
    Nombre_ofer = forms.CharField(label='Cargo:',max_length=40)
    descripcion = forms.CharField(label='Descripcion:',max_length=40)
    pago = forms.IntegerField(label='Pago:')
    class Meta:
        model = Oferta_empleo
        fields = ['Nombre_ofer','descripcion','pago','extra']

class solicitud_empform(ModelForm):
    extra = forms.FileField(label='Curriculum:')
    class Meta:
        model = SolicitudOferta
        fields = ['extra']

class producto_form(ModelForm):
    nombre = forms.CharField(label='Nombre:',max_length=40)
    imagen  = forms.ImageField(label='Imagen:')
    descripcion = forms.CharField(label='Descripcion:',max_length=40)
    stock = forms.IntegerField(label='Stock:')
    tipo_producto = forms.ChoiceField(label='Tipo de Producto',choices=PRODUCTO_CHOICES)

    class Meta:
        model = Producto
        fields = ['nombre','imagen','descripcion','stock','tipo_producto']

class reporteform(ModelForm):
    anotacion = forms.CharField(label='Anotacion:')
    class Meta:
        model = ReporteStrike
        fields = ['anotacion']
        
class tiendaform(ModelForm):
    imagen  = forms.ImageField(label='Imagen:')
    direccion = forms.CharField(label='Direccion:',max_length=40)
    numero_contac = forms.IntegerField(label='numero_contac:')
    class Meta:
        model = tienda_fisica
        fields = ['imagen','direccion','numero_contac']






    
