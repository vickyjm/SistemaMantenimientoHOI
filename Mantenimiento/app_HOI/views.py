# -*- coding: utf-8 -*-

from django.shortcuts import render
from django.shortcuts import render_to_response
from django.template import RequestContext
from django.contrib.auth import authenticate, login
from django.contrib.auth.models import User
from django.core import validators
from django.core.exceptions import ValidationError
from django.core.exceptions import ObjectDoesNotExist
from django.http import HttpResponseRedirect
from app_HOI.forms import * 
from app_HOI.models import *
from django.contrib.auth.decorators import login_required 
import datetime

#    opciones_tipo_mov = ((0, "Solicitud aprobada"),
#                         (1, "Solicitud rechazada"),
#                         (2, "Cantidad de item modificada"),
#                         (3, "Item creado"),
#                         (4, "Item modificado"),
#                         (5, "Categoría creada"),
#                         (6, "Categoría modificada"),
#                         (7, "Usuario eliminado"))

@login_required
def verperfil(request):

    grupo = request.user.groups.values('name')
    if not grupo: nombre_grupo = "-"
    else: nombre_grupo = grupo[0].get('name')

#    items = Item.objects.filter(id_usuario_accion = request.user)
 #   categorias = Categoria.objects.filter(id_usuario_accion = request.user)
  #  solicitudes = '1'
   # movimientos = []
    #movimientos.append(items)
    #movimientos.append(categorias)
    #print(movimientos)
    return render(request, 'verperfil.html',{'user': request.user})
#    return render(request, 'verperfil.html',{'user': request.user,
 #                                            'grupo': nombre_grupo,
  #                                           'solicitudes' : solicitudes,
   #                                          'items': items,
#                                             'categorias': categorias})


# Vista usada al iniciar el sistema
def inicio_sesion(request):
    if request.method == 'POST':
        form = iniciarSesionForm(request.POST)
        if form.is_valid():
            # Verifico si el usuario existe, esté activo o no
            user = authenticate(username = form.cleaned_data['cedula'],password = form.cleaned_data['contraseña'])
            if user is not None:
                if user.is_active:
                    login(request, user)
                    return HttpResponseRedirect('verperfil')
                else:
                    msg = "Su usuario se encuentra inactivo. Contacte al administrador"
                    return render(request,'inicio_sesion.html',{'form': form, 'msg': msg})
            else:
                msg = "Usuario o contraseña incorrecta"
                return render(request,'inicio_sesion.html',{'form': form, 'msg': msg})
    else:
        form = iniciarSesionForm()
    return render(request, 'inicio_sesion.html', {'form': form})

def registro(request):
    if request.method == "POST":
        form = registroForm(request.POST)
        if form.is_valid():
            ci = form.cleaned_data['cedula']
            if User.objects.filter(username=ci).exists():
                msg = "Esta cédula ya se encuentra registrada"
                return render(request,'registro.html',{'form' : form, 'msg' : msg})
            if (form.cleaned_data['contraseña1']!= form.cleaned_data['contraseña2']):
                msg = "Las contraseñas no coinciden. Intente de nuevo"
                return render(request,'registro.html',{'form' : form, 'msg' : msg})
            user = User.objects.create_user(username=ci,
                                 password=form.cleaned_data['contraseña1'])
            user.first_name = form.cleaned_data['nombre']
            user.last_name = form.cleaned_data['apellido']
            if (form.cleaned_data['correo']!=""):
                user.email = form.cleaned_data['correo']
            if (form.cleaned_data['tipo'] == "Técnico"):
                group = Group.objects.get(name='tecnicos') 
                user.groups.add(group)
            else:
                group = Group.objects.get(name='almacenistas') 
                user.groups.add(group)

            user.save()
    else:
        form = registroForm()
    return render(request,'registro.html', {'form': form})
   
def recuperarContraseña(request):
    if request.method == "POST":
        form = recuperarContraseñaForm(request.POST)
        if form.is_valid():
            ci = form.cleaned_data['cedula']
            if User.objects.filter(username=ci).exists():
                if (form.cleaned_data['contraseña1']!= form.cleaned_data['contraseña2']):
                    msg = "Las contraseñas no coinciden. Intente de nuevo"
                    return render(request,'recuperarContrasenia.html',{'form' : form, 'msg' : msg})
                user = User.objects.get(username=ci)
                user.set_password(form.cleaned_data['contraseña1'])
                user.save()
                msg = "Su contraseña fue cambiada"
                return render(request,'recuperarContrasenia.html',{'form' : form, 'msg' : msg})  
            else:
                msg = "La cédula ingresada no se encuentra registrada"
                return render(request,'recuperarContrasenia.html',{'form' : form, 'msg' : msg})
    else:
        form = recuperarContraseñaForm()
    return render(request,'recuperarContrasenia.html',{'form': form})

def crearItem(request):
    if request.method == "POST":
        form = itemForm(request.POST)
        if form.is_valid():
            inombre = form.cleaned_data['nombre']
            icategoria = form.cleaned_data['categoria']
            idcat = Categoria.objects.get(nombre = icategoria)
            print (idcat.id)
            print (icategoria)
            try: 
                item = Item.objects.get(nombre = inombre)
                #item = Item.objects.get(id_categoria = idcat)
                if item.filter(id_categoria = idcat.id).exists():
                #if item.nombre.filter(nombre='inombre').exists():
                    print ("Ya existe")
                #except: 
                else:
                    obj = Item(nombre = inombre,
                                cantidad = form.cleaned_data['cantidad'],
                                id_categoria = idcat,
                                prioridad = form.cleaned_data['prioridad'],
                                minimo = form.cleaned_data['minimo']
                                )
                    obj.save()
                    print("Crea item")
            except:
                print ("No hay items")
                obj = Item(nombre = inombre,
                            cantidad = form.cleaned_data['cantidad'],
                            id_categoria = idcat,
                            prioridad = form.cleaned_data['prioridad'],
                            minimo = form.cleaned_data['minimo'],
                            estado = 1
                            )
                obj.save()
                mensaje = "Item %s creado exitosamente" % (inombre) 
                form = itemForm(initial={'cantidad': '0', 'minimo': '5'})   
    else:
        form = itemForm(initial={'cantidad': '0', 'minimo': '5'})
    return render(request,'crearItem.html', {'form': form})

def categoria(request):
    if request.method == "POST":
        form = categoriaForm(request.POST)
    
        if form.is_valid():
            catnombre = form.cleaned_data['nombre']

            try: 
                cat = Categoria.objects.get(nombre = catnombre)
                # Verifica si el nombre de la categoria ya existe
                if Categoria.objects.filter(pk=cat.pk).exists():
                    mensaje = "Categoría '%s' ya existe" % (catnombre)
            # Si no existe, crea el objeto y lo guarda
            except ObjectDoesNotExist:
                obj = Categoria(nombre = catnombre,
                                estado = 1)
                obj.save()
                mensaje = "Categoría '%s' creada exitosamente" % (catnombre)
                form = categoriaForm()
        categorias = Categoria.objects.order_by('nombre')

    else:
        form = categoriaForm()
        mensaje = None  
        categorias = Categoria.objects.order_by('nombre')

    return render(request,'categoria.html', {'form': form, 
                                             'categorias': categorias, 
                                             'mensaje': mensaje})

# Vista creada para editar una categoria en el sistema
def categoria_editar(request, _id):

    categoria = Categoria.objects.get(id = _id)
    # Lista de items dentro de la categoria
    #items = Item.objects.filter(id_categoria = _id)
    # Cantidad de items dentro de la categoria
    #cantidad = items.count()

    if request.method == "POST":
        
        form = categoria_editarForm(request.POST)
        
        if form.is_valid():
            #Obtiene datos del formulario
            cnombre = form.cleaned_data['nombre']
            cestado = form.cleaned_data['estado']
            try:
                # Obtiene la categoria con el nombre del formulario
                cat = Categoria.objects.get(nombre = cnombre)
                # Si la categoria es la misma a editar
                if int(cat.pk) == int(_id):
                    # Verifica si hay cambio en la categoria
                    if int(cestado) != int(categoria.estado):
                        categoria.estado = cestado
                        categoria.save()
                        mensaje = "Categoría editada exitosamente"
                    # No hubo cambios en la categoria
                    else: 
                        mensaje = None
                # Si la categoria no es la misma a editar
                else:
                    mensaje = "La categoría '%s' ya existe" % cnombre
            # Si no existe una categoria con el nombre introducido
            except:
                categoria.nombre = cnombre
                categoria.estado = cestado
                categoria.save()
                mensaje = "Categoría editada exitosamente"

    else:
        # Formulario con los datos a editar
        form = categoria_editarForm(initial={'nombre': categoria.nombre, 
                                             'estado': categoria.estado})
        mensaje = None
    return render(request,'categoria_editar.html', {'categoria': categoria, 
                                                    'form': form,
                                                    'mensaje': mensaje})

# Vista utilizada para editar un item en el sistema
def item_editar(request, _id):
    # Obtiene el objeto de item a editar
    item = Item.objects.get(id = _id)
    nombre = item.nombre
    if request.method == "POST":
        form = item_editarForm(request.POST)

        if form.is_valid():
            # Obtiene los datos del formulario
            inombre = form.cleaned_data['nombre']
            icategoria = form.cleaned_data['categoria']
            idcat = Categoria.objects.get(nombre = icategoria)
            print (idcat)
            try:
                itemexiste = Item.objects.get(nombre = inombre, 
                                              id_categoria = idcat.id)
                if int(itemexiste.id) == int(_id): 
                    item.cantidad = form.cleaned_data['cantidad']
                    item.prioridad = form.cleaned_data['prioridad']
                    item.minimo = form.cleaned_data['minimo']
                    item.estado = form.cleaned_data['estado']
                    item.save()
                    mensaje = "Item '%s' editado exitosamente" %nombre
                else:
                    mensaje = "Nombre '%s' ya existe en la categoría '%s'" %(inombre, idcat)
                    
            except ObjectDoesNotExist:

                item.nombre = inombre
                item.cantidad = form.cleaned_data['cantidad']
                item.id_categoria = idcat
                item.prioridad = form.cleaned_data['prioridad']
                item.minimo = form.cleaned_data['minimo']
                item.estado = form.cleaned_data['estado']
                item.save()
                mensaje = "Item '%s' editado exitosamente" %nombre
                nombre = inombre
    else: 
        # Formulario con los datos del item a editar
        form = item_editarForm(initial = {'nombre': item.nombre, 
                                        'cantidad': item.cantidad,
                                        'categoria': item.id_categoria,
                                        'prioridad': item.prioridad,
                                        'minimo': item.minimo,
                                        'estado': item.estado})
        mensaje = None
    return render(request, 'item_editar.html', {'form' : form, 
                                                'nombre' : nombre,
                                                'mensaje': mensaje})
           
           
# Vista utilizada para mostrar los items del inventario
def inventario(request):
    items = Item.objects.order_by('nombre')
    if request.method == "POST":
        pass  
    else:
        pass
    return render(request,'inventario.html', {'items': items})


def solicitud(request):
    solicitudes = Crea.objects.order_by('fecha')

    if request.method == "POST":
        pass  
    else:
        pass
    return render(request,'solicitud.html', {'solicitudes': solicitudes})

def crearSolicitud(request):
    if request.method == "POST":
        mensaje = None
        form = solicitudForm(request.POST)

        if form.is_valid():
            sdpto = form.cleaned_data['dpto']
            sitem = form.cleaned_data['item']
            scantidad = form.cleaned_data['cantidad']
            iditem = Item.objects.get(nombre = sitem)

            nueva_solicitud = Solicitud(fecha = datetime.datetime.now(),
                                        dpto = sdpto,
                                        cantidad = scantidad)
            nueva_solicitud.save()

            obj = Crea(id_usuario = request.user,
                       id_item = iditem,
                       id_solicitud = nueva_solicitud,
                       fecha = datetime.datetime.now())
            obj.save()

            mensaje = "Solicitud creada exitosamente" 
            form = solicitudForm(initial={'cantidad': '1'})
    else:
        mensaje = None
        form = solicitudForm(initial={'cantidad': '1'})
    return render(request,'crearSolicitud.html', {'form': form, 'mensaje':mensaje})

def solicitud_eliminar(request, _id):
    if request.method == "GET":
        return render(request,'solicitud_eliminar.html')
    else:
        obj = Crea.objects.get(pk=_id)

        solicitud = Solicitud.objects.get(pk = obj.id_solicitud.pk)
        solicitud.delete()
    
        obj.delete()
    return HttpResponseRedirect('/solicitud')