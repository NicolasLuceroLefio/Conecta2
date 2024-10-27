# forms.py
from django import forms
from .models import Libro
from .models import Evaluadores, Empresa




class LibroForm(forms.ModelForm):
    class Meta:
        model = Libro
        fields =['nombre', 'imagen', 'descripcion', 'direccion', 'telefono']


class SearchForm(forms.Form):
    query = forms.CharField(label='Buscar', max_length=100)


# nuevo codigo


class EvaluadoresForm(forms.ModelForm):
    claveUsuario = forms.CharField(widget=forms.PasswordInput, label='Contraseña')

    class Meta:
        model = Evaluadores
        fields = ['nombreUsuario', 'claveUsuario', 'nombrePersona', 'apellidoPersona']  # Excluimos 'perfilCreado'

class EmpresaForm(forms.ModelForm):
    claveUsuario = forms.CharField(widget=forms.PasswordInput, label='Contraseña')

    class Meta:
        model = Empresa
        fields = ['nombreUsuario', 'claveUsuario', 'nombrePersona', 'apellidoPersona']  # Excluimos 'perfilCreado'


from django import forms
from .models import GaleriaEmpresa

class GaleriaForm(forms.ModelForm):
    class Meta:
        model = GaleriaEmpresa
        fields = ['imagenGaleria1', 'imagenGaleria2', 'imagenGaleria3', 'imagenGaleria4']
        widgets = {
            'imagenGaleria1': forms.FileInput(attrs={'accept': 'image/*'}),
            'imagenGaleria2': forms.FileInput(attrs={'accept': 'image/*'}),
            'imagenGaleria3': forms.FileInput(attrs={'accept': 'image/*'}),
            'imagenGaleria4': forms.FileInput(attrs={'accept': 'image/*'}),
        }


