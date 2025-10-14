from django.db import models
from django.core.validators import MinValueValidator, MaxValueValidator

class CategoriaEscena(models.Model):
    """Botón principal del menú que agrupa escenas"""
    titulo = models.CharField(
        max_length=200, 
        verbose_name="Título",
        help_text="Nombre de la categoría (ej: 'Planta Baja', 'Primer Piso', 'Exteriores')"
    )
    icono = models.ImageField(
        upload_to='categorias/',
        verbose_name="Icono del botón principal",
        help_text="Imagen circular para el botón principal (recomendado: 200x200px)"
    )
    imagen_fondo = models.ImageField(
        upload_to='fondos_categorias/',
        verbose_name="Imagen 360 de fondo",
        help_text="Imagen 360 que se mostrará como fondo al seleccionar esta categoría",
        blank=True,
        null=True
    )
    descripcion = models.TextField(
        blank=True, 
        verbose_name="Descripción"
    )
    orden = models.IntegerField(
        default=0,
        verbose_name="Orden",
        help_text="Orden de aparición en el menú (menor número = más a la izquierda)"
    )
    activa = models.BooleanField(
        default=True,
        verbose_name="Activa",
        help_text="Si está desactivada, no aparecerá en el menú"
    )
    color_fondo = models.CharField(
        max_length=7,
        default="#667eea",
        verbose_name="Color de fondo",
        help_text="Color hexadecimal para el botón (ej: #667eea)"
    )
    fecha_creacion = models.DateTimeField(auto_now_add=True)
    fecha_modificacion = models.DateTimeField(auto_now=True)
    
    class Meta:
        verbose_name = "Categoría de Escenas"
        verbose_name_plural = "Categorías de Escenas"
        ordering = ['orden', 'titulo']
    
    def __str__(self):
        return self.titulo
    
    def get_imagen_fondo(self):
        """Retorna la imagen de fondo o la primera escena como fallback"""
        if self.imagen_fondo:
            return self.imagen_fondo.url
        primera_escena = self.escenas.filter(activa=True).order_by('orden').first()
        if primera_escena:
            return primera_escena.imagen.url
        return None


class Escena360(models.Model):
    """Botón secundario - cada vista/escena 360"""
    categoria = models.ForeignKey(
        CategoriaEscena,
        on_delete=models.CASCADE,
        related_name='escenas',
        verbose_name="Categoría",
        help_text="Botón principal al que pertenece esta escena"
    )
    titulo = models.CharField(
        max_length=200, 
        verbose_name="Título",
        help_text="Nombre de la escena (ej: 'Sala Principal', 'Jardín')"
    )
    imagen = models.ImageField(
        upload_to='imagenes_360/',
        verbose_name="Imagen 360",
        help_text="Imagen equirectangular para esta escena. Ratio recomendado 2:1"
    )
    icono = models.ImageField(
        upload_to='iconos_360/',
        verbose_name="Icono del botón",
        help_text="Imagen circular para el botón secundario (recomendado: 200x200px)"
    )
    descripcion = models.TextField(
        blank=True, 
        verbose_name="Descripción",
        help_text="Descripción que se mostrará en la parte izquierda de la pantalla"
    )
    orden = models.IntegerField(
        default=0,
        verbose_name="Orden",
        help_text="Orden dentro de su categoría"
    )
    activa = models.BooleanField(
        default=True,
        verbose_name="Activa",
        help_text="Si está desactivada, no aparecerá en el menú"
    )
    fecha_creacion = models.DateTimeField(auto_now_add=True)
    fecha_modificacion = models.DateTimeField(auto_now=True)
    
    class Meta:
        verbose_name = "Escena 360"
        verbose_name_plural = "Escenas 360"
        ordering = ['categoria__orden', 'orden', 'titulo']
    
    def __str__(self):
        return f"{self.categoria.titulo} - {self.titulo}"


class LogoCreador(models.Model):
    """Logos de los creadores que aparecen en la parte superior"""
    nombre = models.CharField(
        max_length=200,
        verbose_name="Nombre",
        help_text="Nombre del creador o institución"
    )
    logo = models.ImageField(
        upload_to='logos/',
        verbose_name="Logo",
        help_text="Logo del creador (recomendado: fondo transparente, max 150px de alto)"
    )
    url = models.URLField(
        blank=True,
        verbose_name="URL",
        help_text="Enlace opcional al sitio web del creador"
    )
    orden = models.IntegerField(
        default=0,
        verbose_name="Orden",
        help_text="Orden de aparición (menor número = más a la izquierda)"
    )
    activo = models.BooleanField(
        default=True,
        verbose_name="Activo"
    )
    fecha_creacion = models.DateTimeField(auto_now_add=True)
    
    class Meta:
        verbose_name = "Logo Creador"
        verbose_name_plural = "Logos Creadores"
        ordering = ['orden', 'nombre']
    
    def __str__(self):
        return self.nombre

class ConfiguracionInterfaz(models.Model):
    """Configuración de colores y fondos de la interfaz"""
    
    # Configuración de descripción lateral
    usar_imagen_descripcion = models.BooleanField(
        default=False,
        verbose_name="Usar imagen de fondo en descripción",
        help_text="Si está activado, se usará la imagen en lugar del color"
    )
    imagen_fondo_descripcion = models.ImageField(
        upload_to='config/',
        blank=True,
        null=True,
        verbose_name="Imagen de fondo para descripción",
        help_text="Imagen de fondo para el panel de descripción lateral"
    )
    color_descripcion = models.CharField(
        max_length=7,
        default="#ffffff",
        verbose_name="Color de fondo descripción",
        help_text="Color hexadecimal (ej: #ffffff para blanco)"
    )
    transparencia_descripcion = models.IntegerField(
        default=95,
        validators=[MinValueValidator(0), MaxValueValidator(100)],
        verbose_name="Transparencia descripción (%)",
        help_text="0 = transparente, 100 = opaco"
    )
    
    # Configuración de logos superiores
    mostrar_fondo_logos = models.BooleanField(
        default=True,
        verbose_name="Mostrar fondo en logos",
        help_text="Si está desactivado, los logos no tendrán ningún fondo"
    )
    color_logos = models.CharField(
        max_length=7,
        default="#ffffff",
        verbose_name="Color de fondo logos",
        help_text="Color hexadecimal (ej: #ffffff para blanco)"
    )
    transparencia_logos = models.IntegerField(
        default=90,
        validators=[MinValueValidator(0), MaxValueValidator(100)],
        verbose_name="Transparencia logos (%)",
        help_text="0 = transparente, 100 = opaco"
    )
    
    fecha_modificacion = models.DateTimeField(auto_now=True)
    
    class Meta:
        verbose_name = "Configuración de Interfaz"
        verbose_name_plural = "Configuración de Interfaz"
    
    def __str__(self):
        return "Configuración de Interfaz"
    
    def save(self, *args, **kwargs):
        # Solo permitir una configuración
        if not self.pk and ConfiguracionInterfaz.objects.exists():
            raise ValueError("Solo puede existir una configuración de interfaz")
        super().save(*args, **kwargs)
    
    def get_rgba_descripcion(self):
        """Convierte el color hex y transparencia a rgba"""
        hex_color = self.color_descripcion.lstrip('#')
        r, g, b = tuple(int(hex_color[i:i+2], 16) for i in (0, 2, 4))
        alpha = self.transparencia_descripcion / 100
        return f"rgba({r}, {g}, {b}, {alpha})"
    
    def get_rgba_logos(self):
        """Convierte el color hex y transparencia a rgba"""
        hex_color = self.color_logos.lstrip('#')
        r, g, b = tuple(int(hex_color[i:i+2], 16) for i in (0, 2, 4))
        alpha = self.transparencia_logos / 100
        return f"rgba({r}, {g}, {b}, {alpha})"