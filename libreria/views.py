from django.shortcuts import render, redirect, get_object_or_404
from django.http import HttpResponse
from .models import Libro, Evaluaciones, GaleriaEmpresa 
from .forms import LibroForm,SearchForm, GaleriaForm
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm
from django.contrib.auth import authenticate, login, logout
from django.db.models import Q

from .forms import EvaluadoresForm, EmpresaForm
from django.contrib.auth.decorators import login_required
from django.urls import reverse
from django.contrib.auth import login as auth_login
from django.core.exceptions import PermissionDenied
from .decorators import evaluador_required, empresa_required

from django.db.models import Avg
from django.shortcuts import get_object_or_404, redirect, render
from django.urls import reverse


# Create your views here en views.py.

def inicio(request):
    libros = Libro.objects.all() # Obtener todos los libros
    return render(request, 'paginas/inicio.html',{'libros':libros}) # Renderiza una plantilla HTML en el navegador


@empresa_required
def nosotros(request):
   # Obtener la galería asociada al libro del usuario logueado
    libro = Libro.objects.filter(empresa=request.user).first()
    galeria = GaleriaEmpresa.objects.filter(perfilEmpresa=libro).first()
    
    # Renderizar la plantilla con el contexto adecuado
    return render(request, 'paginas/nosotros.html', {'galeria': galeria})



def ustedes(request):
    return render(request, 'paginas/ustedes.html') # Buscar un archivo HTML en templates/nosotros.html

def libros(request):
    libros = Libro.objects.all() # Obtener todos los libros
    #print(libros) 
    return render(request, 'libros/index.html', {'libros':libros}) # Buscar un archivo HTML en templates

@login_required
def crear(request):
    formulario = LibroForm(request.POST or None, request.FILES or None)
    if formulario.is_valid():
        libro = formulario.save(commit=False)  # No guarda aún en la base de datos
        libro.empresa = request.user  # Asigna la empresa del usuario logueado
        libro.save()  # Guarda el libro con la empresa asignada
        return redirect('libros')  # Redireccionar a la lista de libros
    return render(request, 'libros/crear.html', {'formulario': formulario})


def editar(request,id):
    libro = Libro.objects.get(id=id)
    formulario = LibroForm(request.POST or None, request.FILES or None, instance=libro)
    if formulario.is_valid() and request.POST:
      formulario.save()
      return redirect('libros') # Redireccionar a la lista de libros
    return render(request,'libros/editar.html',{'formulario':formulario})

def eliminar(request, id):
    libro = Libro.objects.get(id=id)
    libro.delete()
    return redirect('libros') # Redireccionar a la lista de libros



def iniciar_sesion(request):
    if request.method == 'POST':
        form = AuthenticationForm(request, data=request.POST)
        if form.is_valid():
            user = form.get_user()
            login(request, user)
            return redirect('inicio')  # Redirige a la página de inicio o donde desees =================================================
    else:
        form = AuthenticationForm()
    return render(request, 'iniciar_sesion_empresa.html', {'form': form})


def cerrar_sesion(request):
    logout(request)
    return redirect('inicio')  # Redirige a la página de inicio o donde desees

def search(request):
    query = request.GET.get('query', '')
    results = []

    if query:
        results = Libro.objects.filter(
            Q(nombre__icontains=query) |
            Q(descripcion__icontains=query)
        )

    return render(request, 'search_results.html', {'query': query, 'results': results})


def registrar_evaluador(request):
    if request.method == 'POST':
        form = EmpresaForm(request.POST)
        if form.is_valid():
            empresa = form.save(commit=False)
            empresa.set_password(form.cleaned_data['claveUsuario'])
            empresa.tipo_empresa = 'evaluador'  # valor por defecto aquí ################################################### 
            empresa.save()
            return redirect('nosotros')
    else:
        form = EmpresaForm()
    return render(request, 'registrar_evaluador.html', {'form': form})

def registrar_empresa(request):
    if request.method == 'POST':
        form = EmpresaForm(request.POST)
        if form.is_valid():
            empresa = form.save(commit=False)
            empresa.set_password(form.cleaned_data['claveUsuario'])
            empresa.tipo_empresa = 'empresa'  # valor por defecto aquí ###################################################
            empresa.save()
            return redirect('nosotros')
    else:
        form = EmpresaForm()
    return render(request, 'registrar_empresa.html', {'form': form})


@login_required
def comentar_libro(request, libro_id):
    libro = get_object_or_404(Libro, id=libro_id)
    
    if request.method == 'POST':
        comentario = request.POST.get('comentario')
        puntuacion_servicio = request.POST.get('puntuacionServicio')
        puntuacion_producto = request.POST.get('puntuacionProducto')

        if comentario and puntuacion_servicio and puntuacion_producto:
            nueva_evaluacion = Evaluaciones(
                perfilEmpresa=libro,
                comentarioEvaluador=comentario,
                puntuacionServicio=int(puntuacion_servicio),
                puntuacionProducto=int(puntuacion_producto),
                usuarioEvaluador=request.user  # Capturando el usuario logueado es guardado en el sistema
            )
            nueva_evaluacion.save()
            return redirect(reverse('detalle_libro', args=[libro_id]))
        else:
            return render(request, 'detalle_libro.html', {'libro': libro, 'error': 'Por favor, completa todos los campos.'})

    return render(request, 'detalle_libro.html', {'libro': libro})



def subir_imagenes(request):
    if request.method == 'POST':
        form = GaleriaForm(request.POST, request.FILES)
        if form.is_valid():
            # Obtener el libro asociado al usuario logueado
            libro = Libro.objects.filter(empresa=request.user).first()
            
            # Crear o obtener la galería para el libro
            galeria, created = GaleriaEmpresa.objects.get_or_create(
                perfilEmpresa=libro
            )
            
            # Actualiza los campos de la galería
            if form.cleaned_data['imagenGaleria1']:
                galeria.imagenGaleria1 = form.cleaned_data['imagenGaleria1']
            if form.cleaned_data['imagenGaleria2']:
                galeria.imagenGaleria2 = form.cleaned_data['imagenGaleria2']
            if form.cleaned_data['imagenGaleria3']:
                galeria.imagenGaleria3 = form.cleaned_data['imagenGaleria3']
            if form.cleaned_data['imagenGaleria4']:
                galeria.imagenGaleria4 = form.cleaned_data['imagenGaleria4']
                
            galeria.save()
            return redirect('mostrar_imagenes')
    else:
        form = GaleriaForm()
    
    return render(request, 'subir_imagenes.html', {'form': form})

def mostrar_imagenes(request):
    # Obtener la galería asociada al libro del usuario logueado
    libro = Libro.objects.filter(empresa=request.user).first()
    galeria = GaleriaEmpresa.objects.filter(perfilEmpresa=libro).first()
    
    # Renderizar la plantilla con el contexto adecuado
    return render(request, 'mostrar_imagenes.html', {'galeria': galeria})



def perfil(request):
    # Obtener el libro asociado al usuario actual
    libro = get_object_or_404(Libro, empresa=request.user)
    return render(request, 'libros/perfil.html', {'libro': libro})

def editar_perfil(request):
    # Obtener el libro asociado al usuario actual
    libro = get_object_or_404(Libro, empresa=request.user)
    
    if request.method == 'POST':
        formulario = LibroForm(request.POST, request.FILES, instance=libro)
        if formulario.is_valid():
            formulario.save()
            return redirect('nosotros')  # Redireccionar a la vista de perfil después de editar
    else:
        formulario = LibroForm(instance=libro)
    
    return render(request, 'libros/editar_perfil.html', {'formulario': formulario})




def login_view(request):
    if request.method == 'POST':
        form = AuthenticationForm(request, data=request.POST)
        if form.is_valid():
            user = form.get_user()
            login(request, user)
            if user.tipo_empresa == 'evaluador':
                return redirect('')
            elif user.tipo_empresa == 'empresa':
                return redirect('')
            else:
                return redirect('')  # Redirige a una vista de inicio general si es necesario
    else:
        form = AuthenticationForm()
    return render(request, 'login.html', {'form': form})

def detalle_libro(request, id):
    libro = get_object_or_404(Libro, id=id)
    evaluaciones = Evaluaciones.objects.filter(perfilEmpresa=libro)
    
    # Calcular el promedio de puntuación de servicio
    if evaluaciones.exists():
        promedio_puntuacion_servicio = evaluaciones.aggregate(
            average_puntuacion_servicio=Avg('puntuacionServicio')
        )['average_puntuacion_servicio']
    else:
        promedio_puntuacion_servicio = None
    
    return render(request, 'libros/detalle_libro.html', {
        'libro': libro,
        'evaluaciones': evaluaciones,
        'promedio_puntuacion_servicio': promedio_puntuacion_servicio
    })



@login_required
def responder_comentario(request, comentario_id):
    comentario = get_object_or_404(Evaluaciones, id=comentario_id)
    
    if request.method == 'POST':
        respuesta = request.POST.get('respuesta')

        if respuesta:
            comentario.respuesta = respuesta
            comentario.save()
            # Utiliza reverse para construir la URL de redireccionamiento
            return redirect(reverse('detalle_libro', args=[comentario.perfilEmpresa.id]))
        else:
            return render(request, 'detalle_libro.html', {'libro': comentario.perfilEmpresa, 'error': 'Por favor, completa el campo de respuesta.'})

    return render(request, 'detalle_libro.html', {'libro': comentario.perfilEmpresa})
