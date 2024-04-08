
from django import forms
from django.contrib.auth.forms import UserCreationForm, UserChangeForm
from django.contrib.auth.models import User
from .models import Empleado, Cliente, Persona, Vehiculo, RegistroReparacion, Admin


class UserCreationFormCustom(UserCreationForm):
    username = forms.CharField(label='Usuario')
    password1 = forms.CharField(label='Contraseña', widget=forms.PasswordInput)
    password2 = forms.CharField(label='Repetir contraseña', widget=forms.PasswordInput)
    class Meta:
        model = User
        fields = ['username', 'password1', 'password2']
        help_texts = {k:"" for k in fields} 


class UserEditForm(UserChangeForm):
    password = None
    username = forms.CharField(label='username')
    class Meta:
        model = User
        fields = ['username']


class EmpleadoForm(forms.ModelForm):
    class Meta:
        model = Empleado
        exclude = ['id_empleado', 'user'] 


class ClienteForm(forms.ModelForm):
    class Meta:
        model = Cliente
        exclude = ['id_cliente'] 


class AdminForm(forms.ModelForm):
    class Meta:
        model = Admin
        exclude = ['id_admin', 'user'] 


class VehiculoForm(forms.ModelForm):
    class Meta:
        model = Vehiculo
        exclude = ['id_vehiculo'] 
        fields = '__all__'

    def clean(self):
        cleaned_data = super().clean()
        cliente = cleaned_data.get('cliente')
        if not cliente:
            raise forms.ValidationError("Debe seleccionar un cliente para crear un vehículo.")


class RegistroReparacionForm(forms.ModelForm):
    class Meta:
        model = RegistroReparacion
        exclude = ['id_registro']  
    
    def clean(self):
        cleaned_data = super().clean()
        vehiculo = cleaned_data.get('vehiculo')
        if not vehiculo:
            raise forms.ValidationError("Debe seleccionar un vehículo para crear un registro de reparación.")




