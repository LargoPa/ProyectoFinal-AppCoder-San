
from django.shortcuts import render, redirect, get_object_or_404
from django.http import HttpResponse
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm
from django.contrib.auth.models import User
from django.contrib.auth import login, logout, authenticate
from django.db import IntegrityError
from django.utils import timezone
from django.contrib.auth.decorators import login_required
from .models import Empleado, Cliente, Persona, Vehiculo, RegistroReparacion, Admin
from .forms import UserEditForm, AdminForm, EmpleadoForm, ClienteForm, VehiculoForm, RegistroReparacionForm, UserCreationFormCustom
from django.contrib.auth.decorators import user_passes_test
from django.contrib.admin.views.decorators import staff_member_required
from django.contrib.auth.views import PasswordChangeView
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.auth.forms import UserChangeForm
from django.core.exceptions import ObjectDoesNotExist
from django.contrib.auth.models import Group
from django.urls import reverse_lazy



def home(request):
    return render(request, 'index.html')


@login_required
def volver_pagina_anterior(request):
    url_anterior = request.META.get('HTTP_REFERER')
    return redirect(url_anterior or '/')


@login_required
@staff_member_required
def register(request):
    if request.method == 'POST':
        user_form = UserCreationFormCustom(request.POST)
        empleado_form = EmpleadoForm(request.POST)
        if user_form.is_valid() and empleado_form.is_valid():
            user = user_form.save()
            empleado = empleado_form.save(commit=False)
            empleado.user = user
            empleado.save()
            return redirect('home')
    else:
        user_form = UserCreationFormCustom()
        empleado_form = EmpleadoForm()
    return render(request, 'register.html', {'user_form': user_form, 'empleado_form': empleado_form})


def login_view(request):
    if request.method == 'GET':
        return render(request, 'login.html', {
            'form': AuthenticationForm
        })
    else:
        user = authenticate(request, username=request.POST['username'], password=request.POST['password'])
        if user is None:
            return render(request, 'login.html', {
                'form': AuthenticationForm,
                'error': 'Usuario o contraseña son incorrectos',
            })
        else:
            login(request, user)
            return redirect('home')


@login_required
def logout_view(request):
    logout(request)
    return redirect('home')


# PERFILES
@login_required
def ver_perfil(request):
    user = request.user
    if hasattr(user, 'admin'):
        perfil = user.admin
    elif hasattr(user, 'empleado'):
        perfil = user.empleado
    elif hasattr(user, 'cliente'):
        perfil = user.cliente
    else:
        perfil = None
    if perfil and perfil.email != user.email:
        user.email = perfil.email
        user.save()
    return render(request, 'user/ver_perfil.html', {'user': user, 'perfil': perfil})


@login_required
@staff_member_required
def editar_perfil_admin(request):
    user = request.user
    try:
        admin_instance = Admin.objects.get(user=user)
    except Admin.DoesNotExist:
        admin_instance, created = Admin.objects.get_or_create(user=user)
    if request.method == 'POST':
        form = AdminForm(request.POST, instance=admin_instance)
        if form.is_valid():
            form.save()
            return redirect('ver_perfil')
    else:
        form = AdminForm(instance=admin_instance)
    return render(request, 'user/editar_perfil.html', {'form': form})


@login_required
def editar_perfil_empleado(request):
    usuario = request.user
    empleado = None
    if hasattr(usuario, 'empleado'):
        empleado = usuario.empleado
    if request.method == 'POST':
        form = EmpleadoForm(request.POST, instance=empleado)
        if form.is_valid():
            empleado = form.save(commit=False)
            empleado.user.email = usuario.email
            empleado.user.save()
            empleado.save() 
            return redirect('ver_perfil') 
    else:
        form = EmpleadoForm(instance=empleado)
    return render(request, 'user/editar_perfil.html', {'form': form, 'empleado': empleado})


@login_required
def editar_user(request):
    usuario = request.user
    if request.method == 'POST':
        mi_formulario = UserEditForm(request.POST, instance=request.user)
        if mi_formulario.is_valid():
            mi_formulario.save()
            return redirect('ver_perfil')
    else:
        mi_formulario = UserEditForm(instance=request.user)
    return render(request, 'user/editar_user.html', {'mi_formulario': mi_formulario, 'usuario': usuario})


class CambiarContrasenia(LoginRequiredMixin, PasswordChangeView):
    template_name = 'user/cambiar_contrasenia.html'
    success_url = reverse_lazy('ver_perfil')


# CLIENTES
@login_required
def detalle_clientes(request):
    clientes = Cliente.objects.all()
    return render(request, 'user/cliente/detalle_clientes.html', {'clientes': clientes})


@login_required
def detalle_cliente(request, cliente_id):
    cliente = get_object_or_404(Cliente, pk=cliente_id)
    return render(request, 'user/cliente/detalle_cliente.html', {'cliente': cliente})


@login_required
def editar_cliente(request, id_cliente):
    cliente = get_object_or_404(Cliente, pk=id_cliente)
    if request.method == 'POST':
        form = ClienteForm(request.POST, instance=cliente)
        if form.is_valid():
            form.save()
            return redirect('detalle_clientes')
    else:
        form = ClienteForm(instance=cliente)
    return render(request, 'user/cliente/editar_cliente.html', {'form': form, 'cliente': cliente})


@login_required
def crear_cliente(request):
    if request.method == 'POST':
        form = ClienteForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('detalle_clientes')
    else:
        form = ClienteForm()
    return render(request, 'user/cliente/crear_cliente.html', {'form': form})


@login_required
def eliminar_cliente(request, cliente_id):
    cliente = get_object_or_404(Cliente, pk=cliente_id)
    if request.method == 'POST':
        cliente.delete()
        return redirect('detalle_clientes')
    return render(request, 'confirmar_eliminar.html', {'tipo': 'cliente', 'objeto': cliente})



# EMPLEADOS
@login_required
@staff_member_required
def detalle_empleados(request):
    empleados = Empleado.objects.all()
    return render(request, 'user/empleado/detalle_empleados.html', {'empleados': empleados})


@login_required
@staff_member_required
def editar_empleado(request, id_empleado):
    empleado = get_object_or_404(Empleado, pk=id_empleado)
    if request.method == 'POST':
        form = EmpleadoForm(request.POST, instance=empleado)
        if form.is_valid():
            form.save()
            return redirect('detalle_empleados')
    else:
        form = EmpleadoForm(instance=empleado)
    return render(request, 'user/empleado/editar_empleado.html', {'form': form, 'empleado': empleado})


@login_required
@staff_member_required
def detalle_empleado(request, empleado_id):
    empleado = get_object_or_404(Empleado, pk=empleado_id)
    return render(request, 'user/empleado/detalle_empleado.html', {'empleado': empleado})


@login_required
@staff_member_required
def eliminar_empleado(request, empleado_id):
    empleado = get_object_or_404(Empleado, pk=empleado_id)
    user = empleado.user
    if request.method == 'POST':
        empleado.delete()
        user.delete()
        return redirect('detalle_empleados')
    return render(request, 'confirmar_eliminar.html', {'tipo': 'empleado', 'objeto': empleado})


# VEHICULOS
@login_required
def detalle_vehiculos(request):
    vehiculos = Vehiculo.objects.all()
    return render(request, 'vehiculo/detalle_vehiculos.html', {'vehiculos': vehiculos})


@login_required
def detalle_vehiculo(request, id_vehiculo):
    vehiculo = get_object_or_404(Vehiculo, pk=id_vehiculo)
    cliente_id = vehiculo.cliente.id_cliente if vehiculo.cliente else None
    return render(request, 'vehiculo/detalle_vehiculo.html', {'vehiculo': vehiculo, 'cliente_id': cliente_id})


@login_required
def detalle_vehiculos_cliente(request, cliente_id):
    cliente = get_object_or_404(Cliente, pk=cliente_id)
    vehiculos = Vehiculo.objects.filter(cliente=cliente)
    return render(request, 'vehiculo/detalle_vehiculos_cliente.html', {'cliente': cliente, 'vehiculos': vehiculos})


@login_required
def crear_vehiculo(request):
    if request.method == 'POST':
        form = VehiculoForm(request.POST, request.FILES)
        if form.is_valid():
            form.save()
            return redirect('detalle_vehiculos')
    else:
        form = VehiculoForm()
    return render(request, 'vehiculo/crear_vehiculo.html', {'form': form})


@login_required
def editar_vehiculo(request, vehiculo_id):
    vehiculo = get_object_or_404(Vehiculo, pk=vehiculo_id)
    if request.method == 'POST':
        form = VehiculoForm(request.POST, request.FILES, instance=vehiculo)
        if form.is_valid():
            form.save()
            return redirect('detalle_vehiculos')
    else:
        form = VehiculoForm(instance=vehiculo)
    return render(request, 'vehiculo/editar_vehiculo.html', {'form': form})


@login_required
def eliminar_vehiculo(request, vehiculo_id):
    vehiculo = get_object_or_404(Vehiculo, pk=vehiculo_id)
    if request.method == 'POST':
        vehiculo.delete()
        return redirect('detalle_vehiculos')
    return render(request, 'confirmar_eliminar.html', {'tipo': 'vehiculo', 'objeto': vehiculo})


# REGISTROS
@login_required
def detalle_registros_reparacion(request):
    registros = RegistroReparacion.objects.all()
    return render(request, 'registro/detalle_registros_reparacion.html', {'registros': registros})


@login_required
def detalle_registros_reparacion_vehiculo(request, vehiculo_id):
    vehiculo = get_object_or_404(Vehiculo, pk=vehiculo_id)
    registros = RegistroReparacion.objects.filter(vehiculo=vehiculo)
    return render(request, 'registro/detalle_registros_reparacion_vehiculo.html', {'registros': registros, 'vehiculo': vehiculo})


@login_required
def detalle_registro_reparacion(request, registro_id):
    registro = get_object_or_404(RegistroReparacion, pk=registro_id)
    vehiculo_id = registro.vehiculo.id_vehiculo if registro.vehiculo else None
    return render(request, 'registro/detalle_registro_reparacion.html', {'registro': registro, 'vehiculo_id': vehiculo_id})


@login_required
def crear_registro_reparacion(request):
    if request.method == 'POST':
        form = RegistroReparacionForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('detalle_registros_reparacion')
    else:
        form = RegistroReparacionForm()
    return render(request, 'registro/crear_registro_reparacion.html', {'form': form})


@login_required
def editar_registro_reparacion(request, registro_id):
    registro = get_object_or_404(RegistroReparacion, pk=registro_id)
    if request.method == 'POST':
        form = RegistroReparacionForm(request.POST, instance=registro)
        if form.is_valid():
            form.save()
            return redirect('detalle_registros_reparacion')
    else:
        form = RegistroReparacionForm(instance=registro)
    return render(request, 'registro/editar_registro_reparacion.html', {'form': form})


@login_required
def eliminar_registro_reparacion(request, registro_id):
    registro = get_object_or_404(RegistroReparacion, pk=registro_id)
    if request.method == 'POST':
        registro.delete()
        referer = request.META.get('HTTP_REFERER')
        if referer:
            return redirect(referer)
        else:
            return redirect('detalle_registros_reparacion')
    return render(request, 'confirmar_eliminar.html', {'tipo': 'registro', 'objeto': registro})





