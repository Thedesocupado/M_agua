from django.contrib import admin
from .models import CategoriaEscena, Escena360

@admin.register(CategoriaEscena)
class CategoriaEscenaAdmin(admin.ModelAdmin):
    list_display = ['titulo', 'orden', 'activa', 'color_fondo', 'fecha_creacion']
    list_filter = ['activa', 'fecha_creacion']
    search_fields = ['titulo', 'descripcion']
    readonly_fields = ['fecha_creacion', 'fecha_modificacion']
    list_editable = ['orden', 'activa']
    
    fieldsets = (
        ('Información Principal', {
            'fields': ('titulo', 'icono', 'descripcion')
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


# Agregar inline a CategoriaEscena
CategoriaEscenaAdmin.inlines = [Escena360Inline]