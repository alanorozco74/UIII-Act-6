from django.urls import path
from . import views

urlpatterns = [
    # Vista principal
    path('', views.index, name='index'),
    
    # Autobuses
    path('autobuses/', views.autobus_listar, name='autobus_listar'),
    path('autobuses/crear/', views.autobus_crear, name='autobus_crear'),
    path('autobuses/editar/<int:id>/', views.autobus_editar, name='autobus_editar'),
    path('autobuses/eliminar/<int:id>/', views.autobus_eliminar, name='autobus_eliminar'),
    
    # Rutas
    path('rutas/', views.ruta_listar, name='ruta_listar'),
    path('rutas/crear/', views.ruta_crear, name='ruta_crear'),
    path('rutas/editar/<int:id>/', views.ruta_editar, name='ruta_editar'),
    path('rutas/eliminar/<int:id>/', views.ruta_eliminar, name='ruta_eliminar'),
    
    # Empleados
    path('empleados/', views.empleado_listar, name='empleado_listar'),
    path('empleados/crear/', views.empleado_crear, name='empleado_crear'),
    path('empleados/editar/<int:id>/', views.empleado_editar, name='empleado_editar'),
    path('empleados/eliminar/<int:id>/', views.empleado_eliminar, name='empleado_eliminar'),
    
    # Pasajeros
    path('pasajeros/', views.pasajero_listar, name='pasajero_listar'),
    path('pasajeros/crear/', views.pasajero_crear, name='pasajero_crear'),
    path('pasajeros/editar/<int:id>/', views.pasajero_editar, name='pasajero_editar'),
    path('pasajeros/eliminar/<int:id>/', views.pasajero_eliminar, name='pasajero_eliminar'),
    
    # Viajes
    path('viajes/', views.viaje_listar, name='viaje_listar'),
    path('viajes/crear/', views.viaje_crear, name='viaje_crear'),
    path('viajes/editar/<int:id>/', views.viaje_editar, name='viaje_editar'),
    path('viajes/eliminar/<int:id>/', views.viaje_eliminar, name='viaje_eliminar'),
    
    # Boletos
    path('boletos/', views.boleto_listar, name='boleto_listar'),
    path('boletos/crear/', views.boleto_crear, name='boleto_crear'),
    path('boletos/editar/<int:id>/', views.boleto_editar, name='boleto_editar'),
    path('boletos/eliminar/<int:id>/', views.boleto_eliminar, name='boleto_eliminar'),
    
    # Función de emergencia
    path('boletos/manual/', views.crear_boleto_manual, name='boleto_manual'),
]