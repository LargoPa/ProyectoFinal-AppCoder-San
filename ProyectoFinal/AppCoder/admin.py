
from django.contrib import admin
from .models import Cliente, Empleado, Vehiculo, RegistroReparacion, Admin

admin.site.register(Admin)
admin.site.register(Cliente)
admin.site.register(Empleado)
admin.site.register(Vehiculo)
admin.site.register(RegistroReparacion)
