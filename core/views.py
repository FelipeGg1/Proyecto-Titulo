import random
from email import message
import http
from re import template
from sre_constants import SUCCESS
import string
from unittest import result
from django.http import HttpResponse
from django.shortcuts import render, redirect
from .forms import *
from .models import Producto

from collections import namedtuple
from django.core.paginator import Paginator

from django.contrib.auth import login as loginuser
from django.contrib.auth import authenticate, logout
from django.contrib.auth.decorators import login_required
import datetime
#
import os
os.add_dll_directory(r"C:\Program Files\GTK3-Runtime Win64\bin")
from django.db import connection,transaction
from django.template.loader import render_to_string
from weasyprint import HTML
from django.db.models import Q

import tempfile
from django.db.models import Sum

#   Productos
@login_required
def reg_post(request):#imagen
    tipo = request.user.tipo_user
    if tipo == 'pyme':
        data = {
            'form': producto_form(),
        }
        if request.method == 'POST':
            form = producto_form(request.POST, request.FILES)
            if form.is_valid():
                producto = form.save(commit=False) 
                producto.user = request.user
                producto.save()

                return redirect('index')
        else:
            form = producto_form
            return render(request,'core/reg_post.html', data)
    else:
        return redirect('index')

def reporte(request,id):
    
    tuserid = request.user.id
    
    cursoro = connection.cursor()
    cursoro.execute("select post_ptr_id from core_producto where id_producto = %s;",[id])
    row = cursoro.fetchone()
    id_post = row[0]

    cursor = connection.cursor()
    cursor.execute("select count(id_strike) +1 as num_strike from core_reportestrike where id_post_id = %s;", [id_post])
    # get a single line from the result
    row = cursor.fetchone()
    # get the value in the first column of the result (the only column)
    numstrike = row[0]
    if request.method == 'POST':
        form = reporteform(data=request.POST)
        if form.is_valid():
            reporte = form.save(commit=False)
            reporte.num_strike = numstrike
            reporte.num_strike = numstrike
            reporte.id_post_id = id_post
            reporte.id_user_admin_id = tuserid
            reporte.save()
            form.save
            return redirect(to='../../producto/'+id)
    else:
        form = reporteform
        return render(request,'core/prod_emp/reporte.html',  {'form': form, 'numstrike': numstrike,'id_post':id_post})
            


def listar_productos(request):
    productos =  Producto.objects.all
    data ={
        'productos':productos
    }
    return render(request, 'core/prod_emp/listprod.html', data)

# vista completa del producto

def producto(request, id):
    tipo = request.user.tipo_user
    prod = Producto.objects.get(id_producto=id)
    tuserid = request.user.id

    cursoro = connection.cursor()
    cursoro.execute("select post_ptr_id from core_producto where id_producto = %s;",[id])
    row = cursoro.fetchone()
    id_post = row[0]

    cursor_visita = connection.cursor()
    cursor_visita.execute("update core_post set nr_visita = nr_visita + 1 where id_post = %s;",[id_post])


    cursor = connection.cursor()
    cursor.execute("select count(id_strike) +1 as num_strike from core_reportestrike where id_post_id = %s;", [id_post])
    # get a single line from the result
    row = cursor.fetchone()
    # get the value in the first column of the result (the only column)
    numstrike = row[0]
    if tipo == 'pyme':
        if request.method == 'POST':
            form = reporteform(request.POST)
            if form.is_valid():
                reporte = form.save(commit=False)
                reporte.num_strike = numstrike
                reporte.num_strike = numstrike
                reporte.id_post_id = id_post
                reporte.id_user_admin_id = tuserid
                reporte.save()
                
                return render(request, 'core/prod_emp/producto.html', {'prod': prod,'form': form})
        else:
            form = reporteform
            return render(request, 'core/prod_emp/producto.html', {'prod': prod,'form': form})
    else:
        
        return render(request, 'core/prod_emp/producto.html', {'prod': prod})
#==============================================
@login_required
def listar_prod_usu(request):
    tipo = request.user.tipo_user
    if tipo == 'pyme':
        # queryset = Artist.objects.select_related(
        # 'songs', 'fans'
        # ).filter(songs__title__icontains='love', fans__votes_casted__gte=100)
        tuserid = request.user.id
        posts = Producto.objects.filter(user_id=tuserid)
        # posts = Producto.objects.raw("select * from vistaProd_usu where id_user_id = '{0}';".format(tuserid)) 
        #cursor = connection.cursor()
        # posts = Producto.objects.raw (''' 
                    
        #             select 
        #                 id_producto, 
        #                 nombre, 
        #                 descripcion, 
        #                 stock, 
        #                 tipo_producto , 
        #                 imagen 
        #                 from core_producto 
        #                 where user_id = %s ;

        #             ''', [tuserid])
        # cursor.execute(query, [tuserid])
        # posts = cursor.fetchall()
        # posts.columns = ['id_producto','nombre','descripcion','stock','tipo_producto','imagen']
        

        return render(request, 'core/prod_emp/listar_prod_usu.html', {'data': posts})
    else:
        return render(request,'core/index.html')

#   Ofertas laborales
@login_required
def reg_emp(request):
    tipo = request.user.tipo_user
    if tipo == 'pyme':
        data = {
            'form': oferta_empleoform(),
        }
        if request.method == 'POST':
            form = oferta_empleoform(request.POST)
            if form.is_valid():
                emple = form.save(commit=False)
                emple.user = request.user
                emple.save() 
                return redirect('index')
        else:
            form = Oferta_empleo
            return render(request,'core/reg_emp.html', data)
    else:
        return render(request,'core/index.html')
    

def listar_laboral(request):
    empleos =  Oferta_empleo.objects.all
    data ={
        'empleos':empleos
    }
    return render(request, 'core/listempl.html', data)
@login_required
def listar_emp_usu(request):
    tipo = request.user.tipo_user
    if tipo == 'pyme':
        tuserid = request.user.id
        emps = Oferta_empleo.objects.filter(user_id=tuserid)
        
        

        return render(request, 'core/prod_emp/list_emp_usu.html', {'data': emps})
    else:
        return render(request,'core/index.html')

def empleo(request, id):
    emp = Oferta_empleo.objects.get(id_oferta=id)
    if request.user.is_authenticated:
        tipo = request.user.tipo_user
        tuserid = request.user.id

        cursoro = connection.cursor()
        cursoro.execute("select post_ptr_id from core_oferta_empleo where id_oferta = %s;",[id])
        row = cursoro.fetchone()
        id_post = row[0]

        cursor_visita = connection.cursor()
        cursor_visita.execute("update core_post set nr_visita = nr_visita + 1 where id_post = %s;",[id_post])

        cursor = connection.cursor()
        cursor.execute("select count(id_strike) +1 as num_strike from core_reportestrike where id_post_id = %s;", [id_post])
        # get a single line from the result
        row = cursor.fetchone()
        # get the value in the first column of the result (the only column)
        numstrike = row[0]
        if tipo == 'encargado':
            if request.method == 'POST':
                form = reporteform(data=request.POST)
                if form.is_valid():
                    reporte = form.save(commit=False)
                    reporte.num_strike = numstrike
                    reporte.num_strike = numstrike
                    reporte.id_post_id = id_post
                    reporte.id_user_admin_id = tuserid
                    reporte.save()
                    form.save
                    return redirect('/empleo/'+id)
            else:
                form = reporteform
                return render(request, 'core/prod_emp/empleo.html', {'emp': emp,'form': form})
        if tipo == 'persona':
            if request.method == 'POST':
                form_soli = solicitud_empform(request.POST, request.FILES)
                if form_soli.is_valid():
                    soli = form_soli.save(commit=False)
                    soli.user = request.user
                    soli.id_oferta_id = id
                    soli.save()
                    return redirect('/empleo/'+id)
            else:
                form_soli = solicitud_empform
                return render(request, 'core/prod_emp/empleo.html', {'emp': emp,'form_soli': form_soli})

        else:
            return render(request, 'core/prod_emp/empleo.html', {'emp': emp})
    else:
            return render(request, 'core/prod_emp/empleo.html', {'emp': emp})



# Create your views here.
def index(request):
    productos =  Producto.objects.all()
    
    productos_paginator = Paginator(productos,4)
    pageprod_num = request.GET.get('pageprod')
    pageprod = productos_paginator.get_page(pageprod_num)
    
    empleos =  Oferta_empleo.objects.all()

    empleos_paginator = Paginator(empleos,4)
    pageEmpl_num = request.GET.get('pageEmp')
    pageEmp = empleos_paginator.get_page(pageEmpl_num)

    post_count = Producto.objects.all().count()  
    if post_count > 1:
        prim = Producto.objects.all()[0]
        secon = Producto.objects.all()[1]
    else:
        prim = ''
        secon = ''
    data = {
            'productos':productos,
            'empleos':empleos,
            'prim':prim,
            'secon':secon,
            'countprod':productos_paginator.count,
            'pageprod':pageprod,
            'empcount':empleos_paginator.count,
            'pageEmp':pageEmp,            
            }

    return render(request, 'core/index.html', data)
# userid = request.user.id
# emps = Producto.objects.filter(user_id = userid) 
# Usuario
@login_required
def perfil(request):    
    tipo = request.user.tipo_user
    tuserid = request.user.id
    
    if tipo == 'pyme':
        emps = Oferta_empleo.objects.filter(user_id=tuserid)
        prods = Producto.objects.filter(user_id=tuserid)

        cursoro = connection.cursor()
        cursoro.execute("select id_tienda from core_tienda_fisica where user_id= %s",[tuserid])
        row = cursoro.fetchall()
        cant_tiendas = len(row)
        if cant_tiendas > 0:
            id_tienda1 = row[0]
            if cant_tiendas > 1:
                id_tienda2 = row[1]
            else:
                id_tienda2 = row[0]
            trabajs = usuarioTrabaj.objects.filter(Q(tienda_fisica_id=id_tienda1)|Q(tienda_fisica_id=id_tienda2)) 
        else:
            trabajs = []
        tiends = tienda_fisica.objects.filter(user_id=tuserid)

        cursorb = connection.cursor()
        
        cursorb.execute("select * from solicitudes_postulantes where user_id= %s ; ",[tuserid])
        solicit = cursorb.fetchall()
        colnames = [desc[0] for desc in cursorb.description]

        
        
        data = {
                'colnames':colnames,
                'solicit':solicit,
                'emps': emps,
                'prods': prods,
                'tiends':tiends,
                'trabajs':trabajs,
                'formprod': producto_form(),
                'formofer': oferta_empleoform(),
                'formtiend': tiendaform(),
                'formtrabaj': USuarioTrabajForm(),
            }
        if request.method == 'POST':
            formprod = producto_form(request.POST, request.FILES)
            formofer = oferta_empleoform(request.POST, request.FILES)
            formtiend = tiendaform(request.POST, request.FILES)
            formtrabaj = USuarioTrabajForm(request.POST, request.FILES)
            if formofer.is_valid():
                emple = formofer.save(commit=False)
                emple.user = request.user
                emple.save() 
            if formprod.is_valid():
                producto = formprod.save(commit=False) 
                producto.user = request.user
                producto.save()
            if formtiend.is_valid():
                if cant_tiendas < 3:
                    tienda = formtiend.save(commit=False)
                    tienda.user = request.user
                    tienda.save()
                else:
                    return redirect('perfil')
            if formtrabaj.is_valid():
                trabajador = formtrabaj.save(commit=False)
                trabajador.save()
            
            return redirect('perfil')
            
        else:
            formprod = producto_form
            formofer = oferta_empleoform
            return render(request,'core/cuenta/perfil.html', data)

    else:
        return render(request,'core/cuenta/perfil.html')



#vista perfil de pyme
def perfil_pyme(request, id):
    pyme = User.objects.get(id=id)
    emps = Oferta_empleo.objects.filter(user_id=id)
    prods = Producto.objects.filter(user_id=id)
    tiends = tienda_fisica.objects.filter(user_id=id)
    data ={
        'user': pyme,
        'emps':emps,
        'prods':prods,
        'tiends':tiends,
    }

    return render(request, 'core/cuenta/perfil_otro_user.html',data)


def login(request):
    message = None
    if request.method == "POST":
        form = LoginForm(request.POST)
        if form.is_valid():
            username = request.POST['username']
            password = request.POST['password']
            user = authenticate(username=username, password=password)
            if user is not None:
                
                    loginuser(request, user)
                    message = "Te has identificado de modo correcto"
                    return render(request,'core/index.html', {'message': message, 'form':form})
                
            else:
                message = "nombre de usuario y/o password incorrecto"
    else:
        form = LoginForm()
    return render(request,'core/login.html', {'message': message, 'form':form})

def logout_view(request):
    logout(request)
    return redirect('login')

def registro_usuario(request):
    data ={
        'form': CustomUserCreationform(),
    }

    if request.method == 'POST':
        formulario = CustomUserCreationform(request.POST, request.FILES)
        if formulario.is_valid():
            formulario.save()
            #autenticar al usuario
            user = authenticate(
                username = formulario.cleaned_data['username'], 
                password = formulario.cleaned_data['password1'] )
            loginuser(request, user)
            return redirect(to="index")
        data["form"] = formulario
    return render(request,'core/registro.html', data)

def export_pdf(request):
    response = HttpResponse(content_type='application/pdf')
    response['Content-Disposition'] = 'attachment; filename=Inventario' + \
        str(datetime.datetime.now())+'.pdf'
    response['Content-Transfer-Encoding'] = 'binary'

    userid = request.user.id
    prods = Producto.objects.filter(user_id=userid)
    sum_pr = prods.aggregate(Sum('nr_visita'))

    emps = Oferta_empleo.objects.filter(user_id=userid)
    sum_em = emps.aggregate(Sum('nr_visita'))

    html_string= render_to_string('core/pdf-output.html',{'prods':prods,'prodtotal':sum_pr['nr_visita__sum'],
                                    'emps':emps,'emptotal':sum_em['nr_visita__sum']})
    html=HTML(string= html_string, base_url=request.build_absolute_uri())

    result=html.write_pdf()    
    with tempfile.NamedTemporaryFile(delete=True) as output:
        output.write(result)
        output.flush()

        output.seek(0)
        response.write(output.read())
    return response
@login_required
def eliminar_post(request, id):
    #
    userid = request.user.id

    cursoro = connection.cursor()
    cursoro.execute("select user_id from core_post where id_post = %s;",[id])
    row = cursoro.fetchone()
    id_user = row[0]

    if id_user == userid:

        post = Post.objects.get(id_post=id)
        post.delete()

        return redirect(to='perfil')
    else:
        return redirect(to="index")


@login_required
def eliminar_tienda(request, id):
    userid = request.user.id
    cursoro = connection.cursor()
    cursoro.execute("select user_id from core_tienda_fisica where id_tienda = %s;",[id])
    row = cursoro.fetchone()
    id_user = row[0]
    if id_user == userid:
        tienda = tienda_fisica.objects.get(id_tienda=id)
        tienda.delete()
        return redirect(to='perfil')
    else:
        return redirect(to="index")
        
@login_required
def eliminar_trabajador(request, id):

    userid = request.user.id
    cursoro = connection.cursor()
    cursoro.execute("select  b.user_id as jefe from core_usuariotrabaj a join core_tienda_fisica b on(a.tienda_fisica_id = b.id_tienda) where  user_ptr_id = %s;",[id])
    row = cursoro.fetchone()
    id_user = row[0]
    if id_user == userid:

        trab = usuarioTrabaj.objects.get(user_ptr_id=id)
        trab.delete()

        return redirect(to='perfil')
    else:
        return redirect(to="index")

@login_required
def modificar_producto(request, id):
    userid = request.user.id

    cursoro = connection.cursor()
    cursoro.execute("select user_id from core_producto a join core_post b on( b.id_post= a.post_ptr_id) where a.id_producto  = %s;",[id])
    row = cursoro.fetchone()
    id_user = row[0]

    if id_user == userid:
        producto = Producto.objects.get(id_producto=id)
        data = {
            'form' : producto_form(instance=producto)
        }
        if request.method == 'POST':
            formulario = producto_form(data=request.POST, instance=producto, files=request.FILES)
            if formulario.is_valid():
                formulario.save()
                data['mensaje'] = "Modificacion correcta"
                return redirect(to='perfil')
        return render(request, 'core/prod_emp/modificar_producto.html', data)
    else:
        return redirect(to="index")
@login_required
def modificar_empleo(request, id):
    userid = request.user.id

    cursoro = connection.cursor()
    cursoro.execute("SELECT user_id from core_oferta_empleo a join core_post b on( b.id_post= a.post_ptr_id) where a.id_oferta = %s;",[id])
    row = cursoro.fetchone()
    id_user = row[0]

    if id_user == userid:
        empleo = Oferta_empleo.objects.get(id_oferta=id)
        data = {
            'form' : oferta_empleoform(instance=empleo)
        }
        if request.method == 'POST':
            formulario = oferta_empleoform(data=request.POST, instance=empleo, files=request.FILES)
            if formulario.is_valid():
                formulario.save()
                data['mensaje'] = "Modificacion correcta"
                return redirect(to='perfil')
        return render(request, 'core/prod_emp/modificar_empleo.html', data)
    else:
        return redirect(to="index")
@login_required
def modificar_tienda(request, id):
    userid = request.user.id
    cursoro = connection.cursor()
    cursoro.execute("select user_id from core_tienda_fisica where id_tienda = %s;",[id])
    row = cursoro.fetchone()
    id_user = row[0]
    if id_user == userid:
        tienda = tienda_fisica.objects.get(id_tienda=id)
        data = {
            'form' : tiendaform(instance=tienda)
        }
        if request.method == 'POST':
            formulario = tiendaform(data=request.POST, instance=tienda, files=request.FILES)
            if formulario.is_valid():
                formulario.save()
                data['mensaje'] = "Modificacion correcta"
                return redirect(to='perfil')
        return render(request, 'core/prod_emp/modificar_tienda.html', data)
    else:
        return redirect(to="index")
@login_required
def modificar_trabajador(request, id):
    userid = request.user.id
    cursoro = connection.cursor()
    cursoro.execute("select  b.user_id as jefe from core_usuariotrabaj a join core_tienda_fisica b on(a.tienda_fisica_id = b.id_tienda) where  user_ptr_id = %s;",[id])
    row = cursoro.fetchone()
    id_user = row[0]
    if id_user == userid:
        trabajador = usuarioTrabaj.objects.get(user_ptr_id=id)
        data = {
            'form' : USuarioTrabajForm(instance=trabajador)
        }
        
        if request.method == 'POST':
            formulario = USuarioTrabajForm(data=request.POST, instance=trabajador, files=request.FILES)
            if formulario.is_valid():
                formulario.save()
                data['mensaje'] = "Modificacion correcta"
                return redirect(to='perfil')
        return render(request, 'core/prod_emp/modificar_trabajador.html', data)
    else:
        return redirect(to="index")
    
