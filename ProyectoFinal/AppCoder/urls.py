
from django.urls import path
from . import views
from django.contrib.auth.views import LogoutView
from django.conf import settings
from django.conf.urls.static import static



urlpatterns = [
    path('', views.home, name='home'),
    
    #Login - Register - Logout
    path('register/', views.register, name='register'),
    path('login/', views.login_view, name='login'),
    path('logout/', views.logout_view, name='logout'),
    
    # Detalle de clientes y empleados
    path('detalle_clientes/', views.detalle_clientes, name='detalle_clientes'),
    path('detalle_cliente/<int:cliente_id>/', views.detalle_cliente, name='detalle_cliente'),
    path('detalle_empleados/', views.detalle_empleados, name='detalle_empleados'),
    path('detalle_empleado/<int:empleado_id>/', views.detalle_empleado, name='detalle_empleado'),
    
    # Crear cliente
    path('crear_cliente/', views.crear_cliente, name='crear_cliente'),
    
    # Ver Perfil
    path('perfil/', views.ver_perfil, name='ver_perfil'),
    
    # Editar (cliente o empleado o  admin)
    path('editar_perfil_admin/', views.editar_perfil_admin, name='editar_perfil_admin'),
    path('editar_perfil_empleado/', views.editar_perfil_empleado, name='editar_perfil_empleado'),
    path('editar_empleado/<int:id_empleado>/', views.editar_empleado, name='editar_empleado'),
    path('editar_cliente/<int:id_cliente>/', views.editar_cliente, name='editar_cliente'),
    
    # Editar User
    path('editar_user/', views.editar_user, name='editar_user'),
    path('cambiar_contrasenia/', views.CambiarContrasenia.as_view(), name='cambiar_contrasenia'),
    
    # Eliminar
    path('eliminar_cliente/<int:cliente_id>/', views.eliminar_cliente, name='eliminar_cliente'),
    path('eliminar_empleado/<int:empleado_id>/', views.eliminar_empleado, name='eliminar_empleado'),
    
    # Vehiculo
    path('detalle_vehiculos/', views.detalle_vehiculos, name='detalle_vehiculos'),
    path('detalle_vehiculos_cliente/<int:cliente_id>/', views.detalle_vehiculos_cliente, name='detalle_vehiculos_cliente'),
    path('detalle_vehiculo/<int:id_vehiculo>/', views.detalle_vehiculo, name='detalle_vehiculo'),
    path('crear_vehiculo/', views.crear_vehiculo, name='crear_vehiculo'),
    path('editar_vehiculo/<int:vehiculo_id>/', views.editar_vehiculo, name='editar_vehiculo'),
    path('eliminar_vehiculo/<int:vehiculo_id>/', views.eliminar_vehiculo, name='eliminar_vehiculo'),
    
    # Registro
    path('detalle_registros_reparacion/', views.detalle_registros_reparacion, name='detalle_registros_reparacion'),
    path('detalle_registro_reparacion/<int:registro_id>/', views.detalle_registro_reparacion, name='detalle_registro_reparacion'),
    path('detalle_registros_vehiculo/<int:vehiculo_id>/', views.detalle_registros_reparacion_vehiculo, name='detalle_registros_reparacion_vehiculo'),
    path('crear_registro_reparacion/', views.crear_registro_reparacion, name='crear_registro_reparacion'),
    path('editar_registro_reparacion/<int:registro_id>/', views.editar_registro_reparacion, name='editar_registro_reparacion'),
    path('eliminar_registro_reparacion/<int:registro_id>/', views.eliminar_registro_reparacion, name='eliminar_registro_reparacion'),

    # Volver
    path('volver/', views.volver_pagina_anterior, name='volver_pagina_anterior'),
    
]


if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
    


