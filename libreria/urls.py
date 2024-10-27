from django.urls import path
from . import views
from django.conf import settings
from django.conf.urls.static import static
from django.contrib.staticfiles.urls import staticfiles_urlpatterns

urlpatterns = [
    path('', views.inicio, name='inicio'),
    path('nosotros/', views.nosotros, name='nosotros'),
    path('ustedes/', views.ustedes, name='ustedes'),
    path('libros/', views.libros, name='libros'),
    path('libros/crear/', views.crear, name='crear'),
    path('libros/editar/<int:id>/', views.editar, name='editar'),
    path('libros/eliminar/<int:id>/', views.eliminar, name='eliminar'),
    path('libros/detalle/<int:id>/', views.detalle_libro, name='detalle_libro'),
   
    path('cerrar_sesion/', views.cerrar_sesion, name='cerrar_sesion'),
    path('buscar/', views.search, name='search'),
    path('registrar-evaluador/', views.registrar_evaluador, name='registrar_evaluador'),
    path('registrar-empresa/', views.registrar_empresa, name='registrar_empresa'),
    path('libro/<int:libro_id>/comentar/', views.comentar_libro, name='comentar_libro'),
     
    path('subir-imagenes/', views.subir_imagenes, name='subir_imagenes'),
    path('mostrar-imagenes/', views.mostrar_imagenes, name='mostrar_imagenes'),

    path('perfil/', views.perfil, name='perfil'),
    path('editar-perfil/', views.editar_perfil, name='editar_perfil'),

    path('comentarios/responder/<int:comentario_id>/', views.responder_comentario, name='responder_comentario'),

    path('comentarios/responder/<int:comentario_id>/', views.responder_comentario, name='responder_comentario'),

] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)

urlpatterns += staticfiles_urlpatterns()
