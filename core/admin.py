from django.contrib import admin
from .models import Municipalidad,User,usuarioEncarga,tienda_fisica
from django import forms
from .forms import *

# Register your models here.
admin.site.site_header = 'Administracion'
admin.site.index_title = 'Panel de control'
admin.site.site_title = 'Administracion'

# Register your models here.
from django.contrib.auth.models import Group
admin.site.unregister(Group)


from django.db.models import Q

class MunicipalidadAdmin(admin.ModelAdmin):
    list_per_page = 10
    list_display = ['id_munic', 'nombre', 'provincia']
    search_fields = ['nombre', 'provincia']
    list_filter = ['provincia']
    #def has_add_permission(self, request, obj=None):
     #   return False

    #def has_delete_permission(self, request, obj=None):
     #   return False

    #def has_change_permission(self, request, obj=None):
     #   return False

class TiendaAdmin(admin.ModelAdmin):
    list_per_page = 10
    list_display = ['id_tienda', 'direccion', 'numero_contac','user']
    search_fields = ['direccion', 'numero_contac']
    list_filter = ['id_tienda']



class Usuariomuniadmin(admin.ModelAdmin):  
    list_per_page = 10
    form = USuarioEncarForm
    class Meta:
        verbose_name = 'Administrador'
        verbose_name_plural = 'Administradores'
    list_display = ['id', 'username', 'tipo_user','date_joined','is_active','numero_contac']
    search_fields = ['username', 'numero_contac']
    list_filter = ['tipo_user','is_active']
    exclude = ['date_joined','last_login','imagen','groups']
   
    list_display_links = ('id', 'username')

class Usuariotrabajadmin(admin.ModelAdmin):  
    list_per_page = 10
    form = USuarioTrabajForm
    class Meta:
        verbose_name = 'Trabajador'
        verbose_name_plural = 'Trabajdores'
    list_display = ['id', 'username', 'tipo_user','date_joined','is_active','numero_contac']
    search_fields = ['username', 'numero_contac']
    list_filter = ['tipo_user','is_active']
    exclude = ['date_joined','last_login','imagen','groups']
   
    list_display_links = ('id', 'username')

class UsuariosdAdmin(admin.ModelAdmin):
    list_per_page = 10
    form = CustomUserCreationform
    list_display = ['id', 'username', 'tipo_user','date_joined','is_active','numero_contac']
    search_fields = ['username', 'numero_contac']
    list_filter = ['tipo_user','is_active']
    exclude = ['date_joined','last_login','imagen','is_superuser','groups']
    list_display_links = ('id', 'username')
    def get_queryset(self, request):
        query = Q(tipo_user='persona')
        query.add(Q(tipo_user='pyme'), Q.OR)
        queryset = User.objects.filter(query)
        return queryset
        


admin.site.register(Municipalidad,MunicipalidadAdmin)
admin.site.register(User,UsuariosdAdmin)
admin.site.register(usuarioEncarga,Usuariomuniadmin)
admin.site.register(usuarioTrabaj,Usuariotrabajadmin)
admin.site.register(tienda_fisica,TiendaAdmin)