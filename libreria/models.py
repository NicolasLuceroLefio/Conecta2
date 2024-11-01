from django.db import models
from django.contrib.auth.models import AbstractBaseUser, BaseUserManager

from django.db import models
from django.conf import settings

class Libro(models.Model):
    id = models.AutoField(primary_key=True)
    empresa = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, null=True, blank=True)
    id_evaluadoresEmpresa = models.ForeignKey('Evaluadores', on_delete=models.SET_NULL, null=True, blank=True, related_name='libros')
    id_galeriaEmpresa = models.ForeignKey('GaleriaEmpresa', on_delete=models.SET_NULL, null=True, blank=True, related_name='libros')
    id_serviciosEmpresa = models.ForeignKey('ServiciosEmpresa', on_delete=models.SET_NULL, null=True, blank=True, related_name='libros')
    nombre = models.CharField(max_length=100, verbose_name='Nombre')
    imagen = models.ImageField(upload_to='imagenes/', verbose_name="Imagen", null=True)
    descripcion = models.TextField(verbose_name="Descripción", null=True)
    direccion = models.CharField(max_length=100, verbose_name="Dirección", null=True)
    telefono = models.CharField(max_length=100, verbose_name="Teléfono", null=True)
    promedioCalificaciones = models.FloatField(default=0, null=True, blank=True)
    contadorComentarios = models.FloatField(default=0, null=True, blank=True)
    contadorVisitaInvitado = models.FloatField(default=0, null=True, blank=True)
    contadorVisitaEvaluador = models.FloatField(default=0, null=True, blank=True)

    def __str__(self):
        fila = f"Nombre: {self.nombre} - Descripción: {self.descripcion}"
        return fila

    def delete(self, using=None, keep_parents=False):
        if self.imagen:
            self.imagen.storage.delete(self.imagen.name)
        super().delete()

class EvaluadorManager(BaseUserManager):
    def create_user(self, nombreUsuario, claveUsuario, nombrePersona, apellidoPersona, **extra_fields):
        if not nombreUsuario:
            raise ValueError('El nombre de usuario debe ser establecido')
        user = self.model(nombreUsuario=nombreUsuario, nombrePersona=nombrePersona, apellidoPersona=apellidoPersona, **extra_fields)
        user.set_password(claveUsuario)  # Encriptar la contraseña
        user.save(using=self._db)
        return user

    def create_superuser(self, nombreUsuario, claveUsuario, nombrePersona, apellidoPersona, **extra_fields):
        extra_fields.setdefault('is_staff', True)
        extra_fields.setdefault('is_superuser', True)
        return self.create_user(nombreUsuario, claveUsuario, nombrePersona, apellidoPersona, **extra_fields)

class EmpresaManager(BaseUserManager):
    def create_user(self, nombreUsuario, claveUsuario, nombrePersona, apellidoPersona, **extra_fields):
        if not nombreUsuario:
            raise ValueError('El nombre de usuario debe ser establecido')
        user = self.model(nombreUsuario=nombreUsuario, nombrePersona=nombrePersona, apellidoPersona=apellidoPersona, **extra_fields)
        user.set_password(claveUsuario)  # Encriptar la contraseña
        user.save(using=self._db)
        return user

    def create_superuser(self, nombreUsuario, claveUsuario, nombrePersona, apellidoPersona, **extra_fields):
        extra_fields.setdefault('is_staff', True)
        extra_fields.setdefault('is_superuser', True)
        return self.create_user(nombreUsuario, claveUsuario, nombrePersona, apellidoPersona, **extra_fields)

class Evaluadores(AbstractBaseUser):
    nombreUsuario = models.CharField(max_length=100, unique=True)
    nombrePersona = models.CharField(max_length=100)
    apellidoPersona = models.CharField(max_length=100)
    perfilCreado = models.DateTimeField(auto_now_add=True)
    is_active = models.BooleanField(default=True)
    is_staff = models.BooleanField(default=False)  # Permite acceso al panel de administración

    objects = EvaluadorManager()

    USERNAME_FIELD = 'nombreUsuario'
    REQUIRED_FIELDS = ['nombrePersona', 'apellidoPersona']

    def __str__(self):
        return self.nombreUsuario



class Empresa(AbstractBaseUser):  ########## E M P R E S A ####
    TIPO_USUARIO_CHOICES = [
        ('empresa', 'Empresa'),
        ('evaluador', 'Evaluador'),
    ]

    nombreUsuario = models.CharField(max_length=100, unique=True)
    nombrePersona = models.CharField(max_length=100)
    apellidoPersona = models.CharField(max_length=100)
    perfilCreado = models.DateTimeField(auto_now_add=True)
    password = models.CharField(max_length=128, default='temporarypassword')  # Valor por defecto temporal
    tipo_empresa = models.CharField(max_length=10, choices=TIPO_USUARIO_CHOICES, default='empresa')
    is_active = models.BooleanField(default=True)
    is_staff = models.BooleanField(default=False)  # Permite acceso al panel de administración

    objects = EmpresaManager()

    USERNAME_FIELD = 'nombreUsuario'
    REQUIRED_FIELDS = ['nombrePersona', 'apellidoPersona']

    def __str__(self):
        return self.nombreUsuario


class GaleriaEmpresa(models.Model):
    id = models.AutoField(primary_key=True)
    perfilEmpresa = models.ForeignKey(Libro, on_delete=models.CASCADE)
    imagenGaleria1 = models.ImageField(upload_to='galeria/', null=True, blank=True)
    imagenGaleria2 = models.ImageField(upload_to='galeria/', null=True, blank=True)
    imagenGaleria3 = models.ImageField(upload_to='galeria/', null=True, blank=True)
    imagenGaleria4 = models.ImageField(upload_to='galeria/', null=True, blank=True)

    def __str__(self):
        return f"Galeria de {self.perfilEmpresa.nombre}"

class ServiciosEmpresa(models.Model):
    id = models.AutoField(primary_key=True)
    perfilEmpresa = models.ForeignKey(Libro, on_delete=models.CASCADE)
    serviciosEmpresa = models.TextField()

    def __str__(self):
        return f"Servicios de {self.perfilEmpresa.nombre}"

class RedesSocialesEmpresa(models.Model):
    id = models.AutoField(primary_key=True)
    perfilEmpresa = models.ForeignKey(Libro, on_delete=models.CASCADE)
    correoEmpresa = models.EmailField()
    paginaWebEmpresa = models.URLField(null=True, blank=True)
    InstagramEmpresa = models.URLField(null=True, blank=True)
    FacebookEmpresa = models.URLField(null=True, blank=True)
    WhatsappEmpresa = models.CharField(max_length=15, null=True, blank=True)

    def __str__(self):
        return f"Redes Sociales de {self.perfilEmpresa.nombre}"

class HorariosEmpresa(models.Model):
    id = models.AutoField(primary_key=True)
    perfilEmpresa = models.ForeignKey(Libro, on_delete=models.CASCADE)
    descripcionHorario = models.TextField()
    horarioApertura = models.TimeField()
    horarioCierre = models.TimeField()

    def __str__(self):
        return f"Horario de {self.perfilEmpresa.nombre}"

class Evaluaciones(models.Model):
    id = models.AutoField(primary_key=True)
    perfilEmpresa = models.ForeignKey(Libro, on_delete=models.CASCADE)
    comentarioEvaluador = models.TextField()
    puntuacionServicio = models.IntegerField()
   
    usuarioEvaluador = models.TextField()
    
    # Nuevo campo para respuesta
    respuesta = models.TextField(null=True, blank=True)

    def __str__(self):
        return f"Evaluación de {self.usuarioEvaluador} para {self.perfilEmpresa.nombre}"
class ProductoEmpresa(models.Model):
    id = models.AutoField(primary_key=True)
    perfilEmpresa = models.ForeignKey(Libro, on_delete=models.CASCADE)
    productosEmpresa = models.TextField()

    def __str__(self):
        return f"Productos de {self.perfilEmpresa.nombre}"