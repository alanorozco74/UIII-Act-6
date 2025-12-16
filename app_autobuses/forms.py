from django import forms
from django.forms import ModelForm
from .models import Autobus, Ruta, Empleado, Pasajero, Viaje, Boleto
import uuid
from django.utils import timezone

class AutobusForm(ModelForm):
    class Meta:
        model = Autobus
        fields = '__all__'
        widgets = {
            'modelo': forms.TextInput(attrs={'class': 'form-control'}),
            'marca': forms.TextInput(attrs={'class': 'form-control'}),
            'placa': forms.TextInput(attrs={'class': 'form-control'}),
            'año': forms.NumberInput(attrs={'class': 'form-control'}),
            'capacidad': forms.NumberInput(attrs={'class': 'form-control'}),
            'estado': forms.Select(attrs={'class': 'form-control'}),
            'imagen': forms.FileInput(attrs={'class': 'form-control'}),
        }

class RutaForm(ModelForm):
    class Meta:
        model = Ruta
        fields = '__all__'
        widgets = {
            'origen': forms.TextInput(attrs={'class': 'form-control'}),
            'destino': forms.TextInput(attrs={'class': 'form-control'}),
            'distancia_km': forms.NumberInput(attrs={'class': 'form-control'}),
            'duracion_estimada': forms.TextInput(attrs={'class': 'form-control'}),
            'precio_base': forms.NumberInput(attrs={'class': 'form-control'}),
            'activa': forms.CheckboxInput(attrs={'class': 'form-check-input'}),
        }

class EmpleadoForm(ModelForm):
    class Meta:
        model = Empleado
        fields = '__all__'
        widgets = {
            'nombre': forms.TextInput(attrs={'class': 'form-control'}),
            'apellido': forms.TextInput(attrs={'class': 'form-control'}),
            'puesto': forms.Select(attrs={'class': 'form-control'}),
            'telefono': forms.TextInput(attrs={'class': 'form-control'}),
            'email': forms.EmailInput(attrs={'class': 'form-control'}),
            'fecha_contratacion': forms.DateInput(attrs={'class': 'form-control', 'type': 'date'}),
            'salario': forms.NumberInput(attrs={'class': 'form-control'}),
            'imagen': forms.FileInput(attrs={'class': 'form-control'}),
            'activo': forms.CheckboxInput(attrs={'class': 'form-check-input'}),
        }

class PasajeroForm(ModelForm):
    class Meta:
        model = Pasajero
        fields = '__all__'
        widgets = {
            'nombre': forms.TextInput(attrs={'class': 'form-control'}),
            'apellido': forms.TextInput(attrs={'class': 'form-control'}),
            'telefono': forms.TextInput(attrs={'class': 'form-control'}),
            'email': forms.EmailInput(attrs={'class': 'form-control'}),
            'fecha_nacimiento': forms.DateInput(attrs={'class': 'form-control', 'type': 'date'}),
            'direccion': forms.Textarea(attrs={'class': 'form-control', 'rows': 3}),
        }

class ViajeForm(ModelForm):
    class Meta:
        model = Viaje
        fields = '__all__'
        widgets = {
            'autobus': forms.Select(attrs={'class': 'form-control'}),
            'ruta': forms.Select(attrs={'class': 'form-control'}),
            'conductor': forms.Select(attrs={'class': 'form-control'}),
            'fecha_salida': forms.DateTimeInput(attrs={'class': 'form-control', 'type': 'datetime-local'}),
            'fecha_llegada_estimada': forms.DateTimeInput(attrs={'class': 'form-control', 'type': 'datetime-local'}),
            'estado': forms.Select(attrs={'class': 'form-control'}),
            'asientos_disponibles': forms.NumberInput(attrs={'class': 'form-control'}),
        }
    
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['autobus'].queryset = Autobus.objects.all()
        self.fields['ruta'].queryset = Ruta.objects.all()
        self.fields['conductor'].queryset = Empleado.objects.all()

class BoletoForm(ModelForm):
    class Meta:
        model = Boleto
        fields = ['viaje', 'pasajero', 'asiento_numero', 'precio', 'estado']
        widgets = {
            'viaje': forms.Select(attrs={'class': 'form-control'}),
            'pasajero': forms.Select(attrs={'class': 'form-control'}),
            'asiento_numero': forms.NumberInput(attrs={'class': 'form-control'}),
            'precio': forms.NumberInput(attrs={'class': 'form-control'}),
            'estado': forms.Select(attrs={'class': 'form-control'}),
        }
    
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        
        # VIAJES: Mostrar todos con formato amigable
        viajes_opciones = []
        for viaje in Viaje.objects.all():
            texto = f"{viaje.ruta} - {viaje.fecha_salida.strftime('%d/%m/%Y %H:%M')} ({viaje.get_estado_display()})"
            viajes_opciones.append((viaje.id, texto))
        
        self.fields['viaje'].choices = [('', 'Selecciona un viaje...')] + viajes_opciones
        
        # PASAJEROS: Mostrar todos
        pasajeros_opciones = []
        for pasajero in Pasajero.objects.all():
            texto = f"{pasajero.nombre} {pasajero.apellido}"
            pasajeros_opciones.append((pasajero.id, texto))
        
        self.fields['pasajero'].choices = [('', 'Selecciona un pasajero...')] + pasajeros_opciones
    
    def clean(self):
        cleaned_data = super().clean()
        viaje = cleaned_data.get('viaje')
        asiento_numero = cleaned_data.get('asiento_numero')
        
        if viaje and asiento_numero:
            # Validar que el asiento esté en rango
            if asiento_numero < 1 or asiento_numero > viaje.autobus.capacidad:
                self.add_error('asiento_numero', 
                    f'El autobús solo tiene capacidad para {viaje.autobus.capacidad} asientos')
            
            # Validar que el asiento no esté ocupado
            if Boleto.objects.filter(viaje=viaje, asiento_numero=asiento_numero).exists():
                # Excluir el boleto actual si estamos editando
                if self.instance and self.instance.pk:
                    if not Boleto.objects.filter(viaje=viaje, asiento_numero=asiento_numero).exclude(pk=self.instance.pk).exists():
                        return cleaned_data
                self.add_error('asiento_numero', f'El asiento {asiento_numero} ya está ocupado')
        
        return cleaned_data
    
    def save(self, commit=True):
        instance = super().save(commit=False)
        
        # Generar código automático si no tiene
        if not instance.codigo_boleto:
            instance.codigo_boleto = f"B{str(uuid.uuid4())[:8].upper()}"
        
        # NOTA: No usamos fecha_pago porque no existe en el modelo
        # Si necesitas registrar cuando se paga, podrías:
        # 1. Usar fecha_compra (que ya existe y se auto-genera)
        # 2. O agregar un campo fecha_pago al modelo después
        
        if commit:
            instance.save()
        return instance