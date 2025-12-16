from django.db import models
from django.core.validators import MinValueValidator, MaxValueValidator
import os

def autobus_imagen_path(instance, filename):
    ext = filename.split('.')[-1]
    filename = f'autobus_{instance.id}.{ext}'
    return os.path.join('autobuses', filename)

def empleado_imagen_path(instance, filename):
    ext = filename.split('.')[-1]
    filename = f'empleado_{instance.id}.{ext}'
    return os.path.join('empleados', filename)

class Autobus(models.Model):
    ESTADOS = [
        ('activo', 'Activo'),
        ('mantenimiento', 'En Mantenimiento'),
        ('inactivo', 'Inactivo'),
    ]
    
    modelo = models.CharField(max_length=50)
    marca = models.CharField(max_length=50)
    placa = models.CharField(max_length=10, unique=True)
    año = models.IntegerField(validators=[MinValueValidator(2000), MaxValueValidator(2024)])
    capacidad = models.IntegerField(validators=[MinValueValidator(10), MaxValueValidator(100)])
    estado = models.CharField(max_length=20, choices=ESTADOS, default='activo')
    imagen = models.ImageField(upload_to=autobus_imagen_path, null=True, blank=True)
    fecha_creacion = models.DateTimeField(auto_now_add=True)
    
    def __str__(self):
        return f'{self.marca} {self.modelo} - {self.placa}'
    
    class Meta:
        verbose_name = 'Autobús'
        verbose_name_plural = 'Autobuses'

class Ruta(models.Model):
    origen = models.CharField(max_length=100)
    destino = models.CharField(max_length=100)
    distancia_km = models.DecimalField(max_digits=10, decimal_places=2)
    duracion_estimada = models.CharField(max_length=20, help_text="Formato: 2h 30m")
    precio_base = models.DecimalField(max_digits=10, decimal_places=2)
    activa = models.BooleanField(default=True)
    
    def __str__(self):
        return f'{self.origen} → {self.destino}'
    
    class Meta:
        ordering = ['origen']

class Empleado(models.Model):
    PUESTOS = [
        ('conductor', 'Conductor'),
        ('auxiliar', 'Auxiliar'),
        ('administrativo', 'Administrativo'),
        ('gerente', 'Gerente'),
    ]
    
    nombre = models.CharField(max_length=50)
    apellido = models.CharField(max_length=50)
    puesto = models.CharField(max_length=20, choices=PUESTOS)
    telefono = models.CharField(max_length=15)
    email = models.EmailField()
    fecha_contratacion = models.DateField()
    salario = models.DecimalField(max_digits=10, decimal_places=2)
    imagen = models.ImageField(upload_to=empleado_imagen_path, null=True, blank=True)
    activo = models.BooleanField(default=True)
    
    def __str__(self):
        return f'{self.nombre} {self.apellido} - {self.puesto}'
    
    class Meta:
        ordering = ['apellido']

class Pasajero(models.Model):
    nombre = models.CharField(max_length=50)
    apellido = models.CharField(max_length=50)
    telefono = models.CharField(max_length=15)
    email = models.EmailField()
    fecha_nacimiento = models.DateField()
    direccion = models.TextField()
    
    def __str__(self):
        return f'{self.nombre} {self.apellido}'
    
    class Meta:
        ordering = ['apellido']

class Viaje(models.Model):
    ESTADOS = [
        ('programado', 'Programado'),
        ('en_curso', 'En Curso'),
        ('completado', 'Completado'),
        ('cancelado', 'Cancelado'),
    ]
    
    # CLAVES FORÁNEAS (NO CAMBIÉ NADA)
    autobus = models.ForeignKey(Autobus, on_delete=models.CASCADE)
    ruta = models.ForeignKey(Ruta, on_delete=models.CASCADE)
    conductor = models.ForeignKey(Empleado, on_delete=models.CASCADE, limit_choices_to={'puesto': 'conductor'})
    fecha_salida = models.DateTimeField()
    fecha_llegada_estimada = models.DateTimeField()
    estado = models.CharField(max_length=20, choices=ESTADOS, default='programado')
    asientos_disponibles = models.IntegerField()
    
    def __str__(self):
        return f'Viaje {self.id}: {self.ruta}'
    
    class Meta:
        ordering = ['-fecha_salida']

class Boleto(models.Model):
    ESTADOS = [
        ('reservado', 'Reservado'),
        ('pagado', 'Pagado'),
        ('usado', 'Usado'),
        ('cancelado', 'Cancelado'),
    ]
    
    # CLAVES FORÁNEAS (NO CAMBIÉ NADA)
    viaje = models.ForeignKey(Viaje, on_delete=models.CASCADE)
    pasajero = models.ForeignKey(Pasajero, on_delete=models.CASCADE)
    asiento_numero = models.IntegerField()
    precio = models.DecimalField(max_digits=10, decimal_places=2)
    estado = models.CharField(max_length=20, choices=ESTADOS, default='reservado')
    fecha_compra = models.DateTimeField(auto_now_add=True)
    codigo_boleto = models.CharField(max_length=10, unique=True)
    
    def __str__(self):
        return f'Boleto {self.codigo_boleto} - {self.pasajero}'
    
    class Meta:
        ordering = ['-fecha_compra']