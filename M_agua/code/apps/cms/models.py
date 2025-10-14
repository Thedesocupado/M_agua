from django.db import models

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
        blank=True,  # ← Agregar
        null=True    # ← Agregar
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
        # Fallback: usar la imagen de la primera escena
        primera_escena = self.escenas.filter(activa=True).order_by('orden').first()
        if primera_escena:
            return primera_escena.imagen.url
        return None


# ... resto del código sin cambios ...
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
        verbose_name="Descripción"
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