# decorators.py
# decorators.py
from django.shortcuts import redirect

def evaluador_required(view_func):
    def _wrapped_view(request, *args, **kwargs):
        if request.user.is_authenticated and request.user.tipo_empresa == 'evaluador':
            return view_func(request, *args, **kwargs)
        return redirect('nosotros')  # Redirige a la página de inicio para evaluadores
    return _wrapped_view

def empresa_required(view_func):
    def _wrapped_view(request, *args, **kwargs):
        if request.user.is_authenticated and request.user.tipo_empresa == 'empresa':
            return view_func(request, *args, **kwargs)
        return redirect('inicio')  # Redirige a la página 'nosotros' para empresas
    return _wrapped_view
