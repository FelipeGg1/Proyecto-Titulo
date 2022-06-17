from __future__ import unicode_literals
from django.contrib import admin
from django.contrib.auth.models import AbstractUser
from django.db import models
# Create your models here.
from django.core.validators import MaxValueValidator, MinValueValidator

# class ProductoEmpresaTitular(models.Model):
#     id_prod_emp_tit = models.AutoField(primary_key=True)
#     nombre_prod_emp_tit = models.CharField(max_length=50)
#     descrpcion_prod_emp_tit = models.CharField(max_length=200)
#     id_empresatitular = models.ForeignKey(EmpresaTitular,to_field='id_empresatitular', on_delete=models.CASCADE)


class User(AbstractUser):
    tipo_user = models.CharField(max_length=20,blank=False,null=False )
    imagen = models.ImageField(upload_to='userimg/',blank=False,null=False)
    numero_contac = models.IntegerField(blank=False,null=False)
    class Meta:
        db_table = 'auth_user'
        verbose_name = 'Perona/Pyme'
        verbose_name_plural = 'Peronas/Pymes'
    
    def __init__(self, *args, **kwargs):
            super(User, self).__init__(*args, **kwargs)
    def save_model(self, request, obj, form, change):
        if obj.password.startswith('pbkdf2'):
            obj.password=obj.password
        else:
            obj.set_password(obj.password) 
        super().save_model(request, obj, form, change)

class Municipalidad(models.Model):
    class Meta:
        verbose_name = 'Municipalidad'
        verbose_name_plural = 'Municipalidades'
    id_munic = models.AutoField(primary_key=True)
    nombre = models.CharField(max_length=40)
    provincia = models.CharField(max_length=40)
    def __str__(self):
        return 'Municipaldiad: ' + self.nombre

class usuarioEncarga(User):
    class Meta:
        verbose_name = 'Encargado'
        verbose_name_plural = 'Encargados'
    cargo = models.CharField(max_length=20)
    Municipalidad = models.ForeignKey(Municipalidad, on_delete=models.CASCADE)



class tienda_fisica(models.Model):
    id_tienda = models.AutoField(primary_key=True)
    imagen = models.ImageField(blank=False,null=False)
    direccion = models.CharField(max_length=40)
    numero_contac = models.IntegerField()
    user = models.ForeignKey(User,related_name='propietario', on_delete=models.CASCADE)

class usuarioTrabaj(User):
    class Meta:
        verbose_name = 'Trabajador'
        verbose_name_plural = 'Trabajadores'
    cargo = models.CharField(max_length=20)
    tienda_fisica = models.ForeignKey(tienda_fisica,related_name='tienda_trabaj', on_delete=models.CASCADE)

class Post(models.Model):
    id_post = models.AutoField(primary_key=True)
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    nr_visita = models.IntegerField(blank=True,null=True,default='0')

class Oferta_empleo(Post):
    id_oferta = models.AutoField(primary_key=True)
    Nombre_ofer = models.CharField(max_length=50)
    descripcion = models.CharField(max_length=50)
    pago = models.IntegerField(blank=False,null=False)
    extra = models.FileField(upload_to='Archivos_ofertas_Emp/',blank=False,null=False)
    

class SolicitudOferta(models.Model):
    id_solicitud = models.AutoField(primary_key=True)
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    extra = models.FileField(upload_to='Archivos_Postulaciones/')
    id_oferta = models.ForeignKey(Oferta_empleo,to_field='id_oferta', on_delete=models.CASCADE,blank=False,null=False)

class Producto(Post):
    id_producto = models.AutoField(primary_key=True)
    nombre = models.CharField(max_length=20)
    imagen = models.ImageField(upload_to='productos/')
    descripcion = models.CharField(max_length=100) 
    stock = models.IntegerField()
    tipo_producto = models.CharField(max_length=20,blank=False,null=False)    
    
class ReporteStrike(models.Model):
    id_strike = models.AutoField(primary_key=True)
    num_strike = models.IntegerField()
    anotacion = models.CharField(max_length=100)
    id_user_admin = models.ForeignKey(User, on_delete=models.CASCADE)
    id_post = models.ForeignKey(Post,to_field='id_post',on_delete=models.CASCADE)



