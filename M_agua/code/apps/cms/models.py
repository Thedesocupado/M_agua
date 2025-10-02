from django.db import models

class Imagen360(models.Model):
    titulo = models.CharField(
        max_length=200, 
        verbose_name="Título",
        help_text="Nombre descriptivo de la imagen 360"
    )
    imagen = models.ImageField(
        upload_to='imagenes_360/',
        verbose_name="Imagen 360",
        help_text="Sube una imagen equirectangular (panorámica 360). Ratio recomendado 2:1"
    )
    descripcion = models.TextField(
        blank=True, 
        verbose_name="Descripción",
        help_text="Descripción opcional de la imagen"
    )
    activa = models.BooleanField(
        default=True,
        verbose_name="Activa",
        help_text="Solo se mostrará la imagen marcada como activa en la página principal"
    )
    fecha_creacion = models.DateTimeField(auto_now_add=True, verbose_name="Fecha de creación")
    fecha_modificacion = models.DateTimeField(auto_now=True, verbose_name="Última modificación")
    
    class Meta:
        verbose_name = "Imagen 360"
        verbose_name_plural = "Imágenes 360"
        ordering = ['-fecha_creacion']
    
    def __str__(self):
        return self.titulo
    
    def save(self, *args, **kwargs):
        # Si esta imagen se marca como activa, desactivar todas las demás
        if self.activa:
            Imagen360.objects.exclude(pk=self.pk).update(activa=False)
        super().save(*args, **kwargs)