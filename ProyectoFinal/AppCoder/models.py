
from typing import Any
from django.db import models
from django.contrib.auth.models import User
from django.utils import timezone
from datetime import date



class Persona(models.Model):
    id_persona = models.AutoField(primary_key=True) 
    dni = models.IntegerField(unique=True, blank=True, null=True)
    nombre = models.CharField(max_length=40)
    segundo_nombre = models.CharField(max_length=40, blank=True)
    apellido = models.CharField(max_length=40)
    num_celular = models.CharField(unique=True, max_length=30)
    email = models.EmailField(unique=True, blank=True)
    direccion = models.CharField(max_length=100, blank=True)
    fecha_nacimiento = models.DateField(default=date.today, blank=True, null=True)
    genero = models.CharField(max_length=10, choices=[('M', 'Masculino'), ('F', 'Femenino'), ('O', 'Otro')], blank=True)
    estado_civil = models.CharField(max_length=20, blank=True)
    nacionalidad = models.CharField(max_length=50, blank=True)
    
    def __str__(self) -> str:
        return f'Nombre: {self.nombre} - Apellido: {self.apellido} - DNI: {self.dni}'


class Empleado(Persona):
    id_empleado = models.AutoField(primary_key=True) 
    user = models.OneToOneField(User, on_delete=models.CASCADE, related_name='empleado')
    cargo = models.CharField(max_length=50, blank=True)
    horas_trabajadas = models.IntegerField(blank=True, null=True)
    fecha_contratacion = models.DateField(default=date.today)
    salario = models.DecimalField(max_digits=10, decimal_places=2, blank=True, null=True)
    fecha_terminacion = models.DateField(blank=True, null=True)


class Cliente(Persona):
    id_cliente = models.AutoField(primary_key=True)
    fecha_registro = models.DateField(auto_now_add=True)


class Admin(Persona):
    id_admin = models.AutoField(primary_key=True) 
    user = models.OneToOneField(User, on_delete=models.CASCADE, related_name='admin')


class Vehiculo(models.Model):
    id_vehiculo = models.AutoField(primary_key=True) 
    placa = models.CharField(max_length=10, unique=True) 
    cliente = models.ForeignKey(Cliente, on_delete=models.CASCADE, null=True, blank=True)
    tipo_vehiculo = models.CharField(max_length=50)
    marca = models.CharField(max_length=50)
    modelo = models.CharField(max_length=50)
    año = models.PositiveIntegerField(blank=True)
    color = models.CharField(max_length=50, blank=True)
    kilometraje = models.PositiveIntegerField(blank=True, null=True)
    numero_serie = models.CharField(max_length=50, unique=True, blank=True)
    fecha_compra = models.DateField(blank=True, null=True)
    estado = models.CharField(max_length=50, blank=True)
    historial_mantenimiento = models.TextField(blank=True)
    imagen_vehiculo = models.ImageField(upload_to='vehiculos/', blank=True, null=True)

    def __str__(self):
        return f'Placa: {self.placa} - Cliente: {self.cliente.nombre}, {self.cliente.apellido} ({self.cliente.dni})'


class RegistroReparacion(models.Model):
    id_registro = models.AutoField(primary_key=True) 
    vehiculo = models.ForeignKey(Vehiculo, on_delete=models.CASCADE)
    fecha_entrada = models.DateTimeField(default=timezone.now)
    fecha_salida = models.DateTimeField(blank=True, null=True)
    descripcion_trabajo = models.TextField(blank=True)
    costo_reparacion = models.DecimalField(max_digits=10, decimal_places=2, blank=True, null=True)
    responsable_reparacion = models.ForeignKey(Empleado, on_delete=models.SET_NULL, null=True)
    ESTADO_CHOICES = [
        ('R', 'Realizando'),
        ('C', 'Completada'),
        ('D', 'Pendiente'),
    ]
    estado_reparacion = models.CharField(max_length=1, choices=ESTADO_CHOICES, default='R')
    PRIORIDAD_CHOICES = [
        ('A', 'Alta'),
        ('M', 'Media'),
        ('B', 'Baja'),
    ]
    prioridad_reparacion = models.CharField(max_length=1, choices=PRIORIDAD_CHOICES, default='M')
    piezas_repuesto = models.TextField(blank=True)

    def __str__(self):
        return f'ID: {self.id_registro} - Vehículo: {self.vehiculo} - Fecha de entrada: {self.fecha_entrada} - Fecha de salida: {self.fecha_salida}'




