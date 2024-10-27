from django.contrib import admin
from .models import Libro
from .models import Evaluadores, Empresa

# Register your models here.
admin.site.register(Libro)

@admin.register(Evaluadores)
class EvaluadoresAdmin(admin.ModelAdmin):
    list_display = ('nombreUsuario', 'nombrePersona', 'apellidoPersona', 'is_active', 'is_staff')

@admin.register(Empresa)
class EmpresaAdmin(admin.ModelAdmin):
    list_display = ('nombreUsuario', 'nombrePersona', 'apellidoPersona', 'is_active', 'is_staff')