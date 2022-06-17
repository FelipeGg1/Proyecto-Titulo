from django.urls import path
from .views import *
from django.conf import settings
from django.conf.urls.static import static

urlpatterns = [
    path('', index, name='index'),
    #usuarios
    path('login', login, name='login'),
    path('logout', logout_view, name="logout") ,
    path('registro', registro_usuario, name='registro'),
    path('perfil', perfil, name = 'perfil'),
    path('perfil_pyme/<id>', perfil_pyme, name = 'perfil_pyme'),
    #productos
    path('reg_post',reg_post, name ='reg_post'),
    path('producto/<id>',producto, name ='producto'),
    path('listar_prod_usu' ,listar_prod_usu, name='listar_prod_usu'),
    #Ofertas de empleo
    path('empleo/<id>',empleo, name ='empleo'),
    path('reg_emp',reg_emp , name = 'reg_emp'),
    path('listar_emp_usu' ,listar_emp_usu, name='listar_emp_usu'),
    #
    path('producto/<id>/reporte',reporte, name ='reporte'),
    
    #path('registro', registro_usuario.as_view(), name='registro'),
    #path('about/', TemplateView.as_view(template_name="about.html")),
    path('export-pdf',export_pdf, name ='export-pdf'),
    path('eliminar_post/<id>',eliminar_post, name ='eliminar_post'),
    path('eliminar_tienda/<id>',eliminar_tienda, name ='eliminar_tienda'),
    path('eliminar_trabajador/<id>',eliminar_trabajador, name ='eliminar_trabajador'),

    path('modificar_producto/<id>', modificar_producto, name="modificar_producto"),
    path('modificar_empleo/<id>', modificar_empleo, name="modificar_empleo"),
    path('modificar_tienda/<id>', modificar_tienda, name="modificar_tienda"),
    path('modificar_trabajador/<id>', modificar_trabajador, name="modificar_trabajador"),

    

    
]
urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)


