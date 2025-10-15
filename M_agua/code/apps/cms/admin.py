from django.contrib import admin
from .models import CategoriaEscena, Escena360, LogoCreador, ConfiguracionInterfaz


@admin.register(CategoriaEscena)
class CategoriaEscenaAdmin(admin.ModelAdmin):
    list_display = ('titulo', 'orden', 'activa', 'fecha_creacion')
    list_filter = ('activa', 'fecha_creacion')
    search_fields = ('titulo',)
    list_editable = ('orden', 'activa')
    ordering = ('orden', 'titulo')


@admin.register(Escena360)
class Escena360Admin(admin.ModelAdmin):
    list_display = ('titulo', 'categoria', 'orden', 'activa', 'fecha_creacion')
    list_filter = ('categoria', 'activa', 'fecha_creacion')
    search_fields = ('titulo', 'descripcion')
    list_editable = ('orden', 'activa')
    ordering = ('categoria', 'orden', 'titulo')


@admin.register(LogoCreador)
class LogoCreadorAdmin(admin.ModelAdmin):
    list_display = ('nombre', 'orden', 'activo', 'url', 'fecha_creacion')
    list_filter = ('activo', 'fecha_creacion')
    search_fields = ('nombre',)
    list_editable = ('orden', 'activo')
    ordering = ('orden', 'nombre')


@admin.register(ConfiguracionInterfaz)
class ConfiguracionInterfazAdmin(admin.ModelAdmin):
    fieldsets = (
        ('Títulos Superiores', {
            'fields': (
                'titulo_principal',
                'mostrar_fondo_titulos',
                'tamano_titulo_principal',
                'tamano_titulo_secundario'
            ),
            'description': 'Configura los títulos que aparecen en la parte superior. El título principal es fijo, el secundario cambia según la escena.'
        }),
        ('Configuración de Descripción Lateral - Fondo', {
            'fields': (
                'usar_imagen_descripcion',
                'imagen_fondo_descripcion',
                'color_descripcion',
                'transparencia_descripcion'
            ),
            'description': 'Personaliza el fondo del panel de descripción en la parte izquierda'
        }),
        ('Configuración de Descripción Lateral - Tipografía', {
            'fields': (
                'fuente_titulo_descripcion',
                'tamano_titulo_descripcion',
                'fuente_texto_descripcion',
                'tamano_texto_descripcion'
            ),
            'description': 'Personaliza la tipografía y tamaño de letra de la descripción'
        }),
        ('Configuración de Logos Superiores', {
            'fields': (
                'mostrar_fondo_logos',
                'color_logos',
                'transparencia_logos'
            ),
            'description': 'Personaliza el fondo del contenedor de logos en la parte superior. Si "Mostrar fondo" está desactivado, los logos no tendrán ningún fondo.'
        }),
    )
    
    def has_add_permission(self, request):
        return not ConfiguracionInterfaz.objects.exists()
    
    def has_delete_permission(self, request, obj=None):
        return False