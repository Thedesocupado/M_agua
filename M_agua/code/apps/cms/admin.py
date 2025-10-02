from django.contrib import admin
from .models import Imagen360

@admin.register(Imagen360)
class Imagen360Admin(admin.ModelAdmin):
    list_display = ['titulo', 'activa', 'fecha_creacion', 'fecha_modificacion']
    list_filter = ['activa', 'fecha_creacion']
    search_fields = ['titulo', 'descripcion']
    readonly_fields = ['fecha_creacion', 'fecha_modificacion']
    
    fieldsets = (
        ('Información Principal', {
            'fields': ('titulo', 'imagen', 'descripcion')
        }),
        ('Estado', {
            'fields': ('activa',),
            'description': 'Solo una imagen puede estar activa a la vez. Al activar esta, las demás se desactivarán automáticamente.'
        }),
        ('Información del Sistema', {
            'fields': ('fecha_creacion', 'fecha_modificacion'),
            'classes': ('collapse',)
        }),
    )
    
    def get_queryset(self, request):
        qs = super().get_queryset(request)
        return qs
    
    class Media:
        css = {
            'all': ('admin/css/custom_admin.css',)
        }