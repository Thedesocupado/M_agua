from django.db import models
from django.core.validators import MinValueValidator, MaxValueValidator

class CategoriaEscena(models.Model):
    """Categoría para agrupar escenas 360"""
    titulo = models.CharField(max_length=200, verbose_name="Título de la categoría")
    icono = models.ImageField(upload_to='categorias/', verbose_name="Icono de la categoría")
    color_fondo = models.CharField(
        max_length=7,
        default="#ffffff",
        verbose_name="Color de fondo",
        help_text="Color hexadecimal (ej: #ffffff para blanco)"
    )
    imagen_fondo = models.ImageField(
        upload_to='categorias/',
        blank=True,
        null=True,
        verbose_name="Imagen de fondo",
        help_text="Imagen que se mostrará al seleccionar esta categoría (opcional)"
    )
    orden = models.IntegerField(default=0, verbose_name="Orden de visualización")
    activa = models.BooleanField(default=True, verbose_name="Categoría activa")
    fecha_creacion = models.DateTimeField(auto_now_add=True)
    fecha_modificacion = models.DateTimeField(auto_now=True)
    
    class Meta:
        verbose_name = "Categoría de Escena"
        verbose_name_plural = "Categorías de Escenas"
        ordering = ['orden', 'titulo']
    
    def __str__(self):
        return self.titulo


class Escena360(models.Model):
    """Escena 360 individual"""
    categoria = models.ForeignKey(
        CategoriaEscena,
        on_delete=models.CASCADE,
        related_name='escenas',
        verbose_name="Categoría"
    )
    titulo = models.CharField(max_length=200, verbose_name="Título de la escena")
    descripcion = models.TextField(blank=True, verbose_name="Descripción")
    imagen = models.ImageField(upload_to='escenas/', verbose_name="Imagen 360")
    icono = models.ImageField(upload_to='iconos/', verbose_name="Icono de la escena")
    video_youtube = models.URLField(
        blank=True,
        verbose_name="Video de YouTube (opcional)",
        help_text="URL del video de YouTube (ej: https://www.youtube.com/watch?v=VIDEO_ID)"
    )
    orden = models.IntegerField(default=0, verbose_name="Orden de visualización")
    activa = models.BooleanField(default=True, verbose_name="Escena activa")
    fecha_creacion = models.DateTimeField(auto_now_add=True)
    fecha_modificacion = models.DateTimeField(auto_now=True)
    
    class Meta:
        verbose_name = "Escena 360"
        verbose_name_plural = "Escenas 360"
        ordering = ['categoria', 'orden', 'titulo']
    
    def __str__(self):
        return f"{self.categoria.titulo} - {self.titulo}"
    
    def get_youtube_embed_url(self):
        """Convierte URL de YouTube a formato embed"""
        if not self.video_youtube:
            return None
        
        video_id = None
        if 'youtube.com/watch?v=' in self.video_youtube:
            video_id = self.video_youtube.split('watch?v=')[1].split('&')[0]
        elif 'youtu.be/' in self.video_youtube:
            video_id = self.video_youtube.split('youtu.be/')[1].split('?')[0]
        elif 'youtube.com/embed/' in self.video_youtube:
            video_id = self.video_youtube.split('embed/')[1].split('?')[0]
        
        if video_id:
            return f"https://www.youtube.com/embed/{video_id}"
        return None
    
    def get_youtube_watch_url(self):
        """Obtiene la URL directa de YouTube para abrir en nueva pestaña"""
        if not self.video_youtube:
            return None
        
        video_id = None
        if 'youtube.com/watch?v=' in self.video_youtube:
            return self.video_youtube
        elif 'youtu.be/' in self.video_youtube:
            video_id = self.video_youtube.split('youtu.be/')[1].split('?')[0]
        elif 'youtube.com/embed/' in self.video_youtube:
            video_id = self.video_youtube.split('embed/')[1].split('?')[0]
        
        if video_id:
            return f"https://www.youtube.com/watch?v={video_id}"
        return self.video_youtube


class LogoCreador(models.Model):
    """Logos de los creadores que aparecen en la parte superior"""
    nombre = models.CharField(max_length=200, verbose_name="Nombre del creador")
    logo = models.ImageField(upload_to='logos/', verbose_name="Logo")
    url = models.URLField(blank=True, verbose_name="URL (opcional)", help_text="Enlace al hacer clic en el logo")
    orden = models.IntegerField(default=0, verbose_name="Orden de visualización")
    activo = models.BooleanField(default=True, verbose_name="Logo activo")
    fecha_creacion = models.DateTimeField(auto_now_add=True)
    
    class Meta:
        verbose_name = "Logo de Creador"
        verbose_name_plural = "Logos de Creadores"
        ordering = ['orden', 'nombre']
    
    def __str__(self):
        return self.nombre


class ConfiguracionInterfaz(models.Model):
    """Configuración de colores y fondos de la interfaz"""
    
    FUENTES_CHOICES = [
        ('Arial, sans-serif', 'Arial'),
        ('Helvetica, sans-serif', 'Helvetica'),
        ('Georgia, serif', 'Georgia'),
        ('Times New Roman, serif', 'Times New Roman'),
        ('Courier New, monospace', 'Courier New'),
        ('Verdana, sans-serif', 'Verdana'),
        ('Trebuchet MS, sans-serif', 'Trebuchet MS'),
        ('Impact, sans-serif', 'Impact'),
        ('Comic Sans MS, cursive', 'Comic Sans MS'),
        ('Palatino, serif', 'Palatino'),
        ('-apple-system, BlinkMacSystemFont, "Segoe UI", Roboto, sans-serif', 'Sistema (Recomendado)'),
    ]
    
    titulo_principal = models.CharField(
        max_length=200,
        default="Visor 360",
        verbose_name="Título Principal",
        help_text="Título fijo que aparece en la parte superior de todas las páginas"
    )
    mostrar_fondo_titulos = models.BooleanField(
        default=True,
        verbose_name="Mostrar fondo en títulos",
        help_text="Si está desactivado, los títulos no tendrán ningún fondo"
    )
    tamano_titulo_principal = models.IntegerField(
        default=32,
        validators=[MinValueValidator(16), MaxValueValidator(72)],
        verbose_name="Tamaño del título principal (px)",
        help_text="Tamaño de letra del título principal en píxeles"
    )
    tamano_titulo_secundario = models.IntegerField(
        default=22,
        validators=[MinValueValidator(12), MaxValueValidator(48)],
        verbose_name="Tamaño del título secundario (px)",
        help_text="Tamaño de letra del título de la escena actual en píxeles"
    )
    
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
    
    fuente_titulo_descripcion = models.CharField(
        max_length=100,
        choices=FUENTES_CHOICES,
        default='-apple-system, BlinkMacSystemFont, "Segoe UI", Roboto, sans-serif',
        verbose_name="Fuente del título",
        help_text="Tipografía para el título de la descripción"
    )
    tamano_titulo_descripcion = models.IntegerField(
        default=24,
        validators=[MinValueValidator(12), MaxValueValidator(72)],
        verbose_name="Tamaño del título (px)",
        help_text="Tamaño de letra del título en píxeles"
    )
    fuente_texto_descripcion = models.CharField(
        max_length=100,
        choices=FUENTES_CHOICES,
        default='-apple-system, BlinkMacSystemFont, "Segoe UI", Roboto, sans-serif',
        verbose_name="Fuente del texto",
        help_text="Tipografía para el texto de la descripción"
    )
    tamano_texto_descripcion = models.IntegerField(
        default=16,
        validators=[MinValueValidator(10), MaxValueValidator(48)],
        verbose_name="Tamaño del texto (px)",
        help_text="Tamaño de letra del texto en píxeles"
    )
    
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