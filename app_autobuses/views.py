from django.shortcuts import render, redirect, get_object_or_404
from django.contrib import messages
from django.http import HttpResponse
from .models import Autobus, Ruta, Empleado, Pasajero, Viaje, Boleto
from .forms import AutobusForm, RutaForm, EmpleadoForm, PasajeroForm, ViajeForm, BoletoForm
import uuid
from django.db.models import Sum

# ========== VISTA PRINCIPAL ==========
def index(request):
    context = {
        'total_autobuses': Autobus.objects.count(),
        'total_rutas': Ruta.objects.filter(activa=True).count(),
        'total_empleados': Empleado.objects.filter(activo=True).count(),
        'total_pasajeros': Pasajero.objects.count(),
        'viajes_programados': Viaje.objects.filter(estado='programado').count(),
        'boletos_vendidos': Boleto.objects.filter(estado='pagado').count(),
    }
    return render(request, 'app_autobuses/index.html', context)

# ========== AUTOBUSES ==========
def autobus_listar(request):
    autobuses = Autobus.objects.all().order_by('marca', 'modelo')
    return render(request, 'app_autobuses/autobus/listar.html', {'autobuses': autobuses})

def autobus_crear(request):
    if request.method == 'POST':
        form = AutobusForm(request.POST, request.FILES)
        if form.is_valid():
            form.save()
            messages.success(request, 'Autobús creado exitosamente.')
            return redirect('autobus_listar')
        else:
            messages.error(request, 'Error al crear el autobús.')
    else:
        form = AutobusForm()
    return render(request, 'app_autobuses/autobus/crear.html', {'form': form})

def autobus_editar(request, id):
    autobus = get_object_or_404(Autobus, id=id)
    if request.method == 'POST':
        form = AutobusForm(request.POST, request.FILES, instance=autobus)
        if form.is_valid():
            form.save()
            messages.success(request, 'Autobús actualizado exitosamente.')
            return redirect('autobus_listar')
        else:
            messages.error(request, 'Error al actualizar el autobús.')
    else:
        form = AutobusForm(instance=autobus)
    return render(request, 'app_autobuses/autobus/editar.html', {'form': form, 'autobus': autobus})

def autobus_eliminar(request, id):
    autobus = get_object_or_404(Autobus, id=id)
    if request.method == 'POST':
        autobus.delete()
        messages.success(request, 'Autobús eliminado exitosamente.')
        return redirect('autobus_listar')
    return render(request, 'app_autobuses/autobus/eliminar.html', {'autobus': autobus})

# ========== RUTAS ==========
def ruta_listar(request):
    rutas = Ruta.objects.all().order_by('origen', 'destino')
    return render(request, 'app_autobuses/ruta/listar.html', {'rutas': rutas})

def ruta_crear(request):
    if request.method == 'POST':
        form = RutaForm(request.POST)
        if form.is_valid():
            form.save()
            messages.success(request, 'Ruta creada exitosamente.')
            return redirect('ruta_listar')
        else:
            messages.error(request, 'Error al crear la ruta.')
    else:
        form = RutaForm()
    return render(request, 'app_autobuses/ruta/crear.html', {'form': form})

def ruta_editar(request, id):
    ruta = get_object_or_404(Ruta, id=id)
    if request.method == 'POST':
        form = RutaForm(request.POST, instance=ruta)
        if form.is_valid():
            form.save()
            messages.success(request, 'Ruta actualizada exitosamente.')
            return redirect('ruta_listar')
        else:
            messages.error(request, 'Error al actualizar la ruta.')
    else:
        form = RutaForm(instance=ruta)
    return render(request, 'app_autobuses/ruta/editar.html', {'form': form, 'ruta': ruta})

def ruta_eliminar(request, id):
    ruta = get_object_or_404(Ruta, id=id)
    if request.method == 'POST':
        ruta.delete()
        messages.success(request, 'Ruta eliminada exitosamente.')
        return redirect('ruta_listar')
    return render(request, 'app_autobuses/ruta/eliminar.html', {'ruta': ruta})

# ========== EMPLEADOS ==========
def empleado_listar(request):
    empleados = Empleado.objects.all().order_by('apellido', 'nombre')
    return render(request, 'app_autobuses/empleado/listar.html', {'empleados': empleados})

def empleado_crear(request):
    if request.method == 'POST':
        form = EmpleadoForm(request.POST, request.FILES)
        if form.is_valid():
            form.save()
            messages.success(request, 'Empleado creado exitosamente.')
            return redirect('empleado_listar')
        else:
            messages.error(request, 'Error al crear el empleado.')
    else:
        form = EmpleadoForm()
    return render(request, 'app_autobuses/empleado/crear.html', {'form': form})

def empleado_editar(request, id):
    empleado = get_object_or_404(Empleado, id=id)
    if request.method == 'POST':
        form = EmpleadoForm(request.POST, request.FILES, instance=empleado)
        if form.is_valid():
            form.save()
            messages.success(request, 'Empleado actualizado exitosamente.')
            return redirect('empleado_listar')
        else:
            messages.error(request, 'Error al actualizar el empleado.')
    else:
        form = EmpleadoForm(instance=empleado)
    return render(request, 'app_autobuses/empleado/editar.html', {'form': form, 'empleado': empleado})

def empleado_eliminar(request, id):
    empleado = get_object_or_404(Empleado, id=id)
    if request.method == 'POST':
        empleado.delete()
        messages.success(request, 'Empleado eliminado exitosamente.')
        return redirect('empleado_listar')
    return render(request, 'app_autobuses/empleado/eliminar.html', {'empleado': empleado})

# ========== PASAJEROS ==========
def pasajero_listar(request):
    pasajeros = Pasajero.objects.all().order_by('apellido', 'nombre')
    return render(request, 'app_autobuses/pasajero/listar.html', {'pasajeros': pasajeros})

def pasajero_crear(request):
    if request.method == 'POST':
        form = PasajeroForm(request.POST)
        if form.is_valid():
            form.save()
            messages.success(request, 'Pasajero creado exitosamente.')
            return redirect('pasajero_listar')
        else:
            messages.error(request, 'Error al crear el pasajero.')
    else:
        form = PasajeroForm()
    return render(request, 'app_autobuses/pasajero/crear.html', {'form': form})

def pasajero_editar(request, id):
    pasajero = get_object_or_404(Pasajero, id=id)
    if request.method == 'POST':
        form = PasajeroForm(request.POST, instance=pasajero)
        if form.is_valid():
            form.save()
            messages.success(request, 'Pasajero actualizado exitosamente.')
            return redirect('pasajero_listar')
        else:
            messages.error(request, 'Error al actualizar el pasajero.')
    else:
        form = PasajeroForm(instance=pasajero)
    return render(request, 'app_autobuses/pasajero/editar.html', {'form': form, 'pasajero': pasajero})

def pasajero_eliminar(request, id):
    pasajero = get_object_or_404(Pasajero, id=id)
    if request.method == 'POST':
        pasajero.delete()
        messages.success(request, 'Pasajero eliminado exitosamente.')
        return redirect('pasajero_listar')
    return render(request, 'app_autobuses/pasajero/eliminar.html', {'pasajero': pasajero})

# ========== VIAJES ==========
def viaje_listar(request):
    viajes = Viaje.objects.all().order_by('-fecha_salida')
    return render(request, 'app_autobuses/viaje/listar.html', {'viajes': viajes})

def viaje_crear(request):
    if request.method == 'POST':
        form = ViajeForm(request.POST)
        if form.is_valid():
            viaje = form.save()
            messages.success(request, f'Viaje creado exitosamente.')
            return redirect('viaje_listar')
        else:
            messages.error(request, 'Error al crear el viaje.')
    else:
        form = ViajeForm()
    return render(request, 'app_autobuses/viaje/crear.html', {'form': form})

def viaje_editar(request, id):
    viaje = get_object_or_404(Viaje, id=id)
    if request.method == 'POST':
        form = ViajeForm(request.POST, instance=viaje)
        if form.is_valid():
            form.save()
            messages.success(request, 'Viaje actualizado exitosamente.')
            return redirect('viaje_listar')
        else:
            messages.error(request, 'Error al actualizar el viaje.')
    else:
        form = ViajeForm(instance=viaje)
    return render(request, 'app_autobuses/viaje/editar.html', {'form': form, 'viaje': viaje})

def viaje_eliminar(request, id):
    viaje = get_object_or_404(Viaje, id=id)
    if request.method == 'POST':
        viaje.delete()
        messages.success(request, 'Viaje eliminado exitosamente.')
        return redirect('viaje_listar')
    return render(request, 'app_autobuses/viaje/eliminar.html', {'viaje': viaje})

# ========== BOLETOS ==========
def boleto_listar(request):
    boletos = Boleto.objects.all().order_by('-fecha_compra')
    
    # Estadísticas
    total_ingresos = boletos.filter(estado='pagado').aggregate(total=Sum('precio'))['total'] or 0
    boletos_pagados = boletos.filter(estado='pagado').count()
    boletos_reservados = boletos.filter(estado='reservado').count()
    boletos_usados = boletos.filter(estado='usado').count()
    boletos_cancelados = boletos.filter(estado='cancelado').count()
    
    context = {
        'boletos': boletos,
        'total_ingresos': total_ingresos,
        'boletos_pagados': boletos_pagados,
        'boletos_reservados': boletos_reservados,
        'boletos_usados': boletos_usados,
        'boletos_cancelados': boletos_cancelados,
    }
    
    return render(request, 'app_autobuses/boleto/listar.html', context)

def boleto_crear(request):
    # Verificar datos necesarios
    if not Viaje.objects.exists():
        messages.error(request, 'No hay viajes registrados. Crea un viaje primero.')
        return redirect('viaje_crear')
    
    if not Pasajero.objects.exists():
        messages.error(request, 'No hay pasajeros registrados. Crea un pasajero primero.')
        return redirect('pasajero_crear')
    
    if request.method == 'POST':
        form = BoletoForm(request.POST)
        if form.is_valid():
            boleto = form.save()
            messages.success(request, f'✅ Boleto {boleto.codigo_boleto} creado exitosamente!')
            return redirect('boleto_listar')
        else:
            # Mostrar errores específicos
            for field, errors in form.errors.items():
                for error in errors:
                    messages.error(request, f'{field}: {error}')
    else:
        form = BoletoForm()
    
    context = {
        'form': form,
        'viajes': Viaje.objects.all(),
        'pasajeros': Pasajero.objects.all(),
    }
    
    return render(request, 'app_autobuses/boleto/crear.html', context)

def boleto_editar(request, id):
    boleto = get_object_or_404(Boleto, id=id)
    
    if request.method == 'POST':
        form = BoletoForm(request.POST, instance=boleto)
        if form.is_valid():
            form.save()
            messages.success(request, f'Boleto {boleto.codigo_boleto} actualizado.')
            return redirect('boleto_listar')
    else:
        form = BoletoForm(instance=boleto)
    
    return render(request, 'app_autobuses/boleto/editar.html', {'form': form, 'boleto': boleto})

def boleto_eliminar(request, id):
    boleto = get_object_or_404(Boleto, id=id)
    
    if request.method == 'POST':
        codigo = boleto.codigo_boleto
        boleto.delete()
        messages.success(request, f'Boleto {codigo} eliminado.')
        return redirect('boleto_listar')
    
    return render(request, 'app_autobuses/boleto/eliminar.html', {'boleto': boleto})

# ========== FUNCIÓN DE EMERGENCIA ==========
def crear_boleto_manual(request):
    """Función de emergencia para crear un boleto si nada funciona"""
    if request.method == 'POST':
        viaje_id = request.POST.get('viaje_id')
        pasajero_id = request.POST.get('pasajero_id')
        asiento = request.POST.get('asiento')
        precio = request.POST.get('precio')
        estado = request.POST.get('estado', 'pagado')
        
        try:
            viaje = Viaje.objects.get(id=viaje_id)
            pasajero = Pasajero.objects.get(id=pasajero_id)
            
            boleto = Boleto.objects.create(
                viaje=viaje,
                pasajero=pasajero,
                asiento_numero=asiento,
                precio=precio,
                estado=estado,
                codigo_boleto=f"MAN-{str(uuid.uuid4())[:8].upper()}"
            )
            
            messages.success(request, f'✅ Boleto {boleto.codigo_boleto} creado manualmente!')
            return redirect('boleto_listar')
            
        except Viaje.DoesNotExist:
            messages.error(request, 'El viaje seleccionado no existe.')
        except Pasajero.DoesNotExist:
            messages.error(request, 'El pasajero seleccionado no existe.')
        except Exception as e:
            messages.error(request, f'Error: {str(e)}')
    
    # Mostrar formulario simple
    viajes = Viaje.objects.all()
    pasajeros = Pasajero.objects.all()
    
    return render(request, 'app_autobuses/boleto/manual.html', {
        'viajes': viajes,
        'pasajeros': pasajeros
    })