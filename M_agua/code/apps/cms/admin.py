from django.contrib import admin
from .models import CategoriaEscena, Escena360, LogoCreador, ConfiguracionInterfaz

@admin.register(CategoriaEscena)
class CategoriaEscenaAdmin(admin.ModelAdmin):
    list_display = ['titulo', 'orden', 'activa', 'color_fondo', 'fecha_creacion']
    list_filter = ['activa', 'fecha_creacion']
    search_fields = ['titulo', 'descripcion']
    readonly_fields = ['fecha_creacion', 'fecha_modificacion']
    list_editable = ['orden', 'activa']
    
    fieldsets = (
        ('Información Principal', {
            'fields': ('titulo', 'icono', 'imagen_fondo', 'descripcion')
        }),
        ('Configuración', {
            'fields': ('orden', 'activa', 'color_fondo'),
            'description': 'El orden determina la posición del botón principal en el menú.'
        }),
        ('Información del Sistema', {
            'fields': ('fecha_creacion', 'fecha_modificacion'),
            'classes': ('collapse',)
        }),
    )


class Escena360Inline(admin.TabularInline):
    model = Escena360
    extra = 1
    fields = ['titulo', 'imagen', 'icono', 'orden', 'activa']
    ordering = ['orden']


@admin.register(Escena360)
class Escena360Admin(admin.ModelAdmin):
    list_display = ['titulo', 'categoria', 'orden', 'activa', 'fecha_creacion']
    list_filter = ['activa', 'categoria', 'fecha_creacion']
    search_fields = ['titulo', 'descripcion', 'categoria__titulo']
    readonly_fields = ['fecha_creacion', 'fecha_modificacion']
    list_editable = ['orden', 'activa']
    
    fieldsets = (
        ('Información Principal', {
            'fields': ('categoria', 'titulo', 'imagen', 'icono', 'descripcion')
        }),
        ('Configuración', {
            'fields': ('orden', 'activa'),
            'description': 'El orden determina la posición dentro de su categoría.'
        }),
        ('Información del Sistema', {
            'fields': ('fecha_creacion', 'fecha_modificacion'),
            'classes': ('collapse',)
        }),
    )
    
    def get_queryset(self, request):
        return super().get_queryset(request).select_related('categoria')


@admin.register(LogoCreador)
class LogoCreadorAdmin(admin.ModelAdmin):
    list_display = ['nombre', 'orden', 'activo', 'fecha_creacion']
    list_filter = ['activo', 'fecha_creacion']
    search_fields = ['nombre']
    list_editable = ['orden', 'activo']
    
    fieldsets = (
        ('Información', {
            'fields': ('nombre', 'logo', 'url')
        }),
        ('Configuración', {
            'fields': ('orden', 'activo')
        }),
    )


@admin.register(ConfiguracionInterfaz)
class ConfiguracionInterfazAdmin(admin.ModelAdmin):
    fieldsets = (
        ('Configuración de Descripción Lateral', {
            'fields': (
                'usar_imagen_descripcion',
                'imagen_fondo_descripcion',
                'color_descripcion',
                'transparencia_descripcion'
            ),
            'description': 'Personaliza el fondo del panel de descripción en la parte izquierda'
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
        # Solo permitir crear si no existe ninguna configuración
        return not ConfiguracionInterfaz.objects.exists()
    
    def has_delete_permission(self, request, obj=None):
        # No permitir eliminar la configuración
        return False


CategoriaEscenaAdmin.inlines = [Escena360Inline]