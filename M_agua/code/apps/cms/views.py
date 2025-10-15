from django.shortcuts import render
from .models import CategoriaEscena, Escena360, LogoCreador, ConfiguracionInterfaz


def visor_360(request):
    """Vista principal del visor 360"""
    
    # Obtener todas las categorías activas con sus escenas
    categorias = CategoriaEscena.objects.filter(activa=True).prefetch_related('escenas')
    
    # Obtener la configuración de interfaz (solo debe haber una)
    config = ConfiguracionInterfaz.objects.first()
    if not config:
        # Crear configuración por defecto si no existe
        config = ConfiguracionInterfaz.objects.create()
    
    # Obtener logos activos
    logos = LogoCreador.objects.filter(activo=True)
    
    # Determinar la escena inicial
    escena_inicial = None
    imagen_inicial = None
    
    if categorias.exists():
        primera_categoria = categorias.first()
        escenas_primera_categoria = primera_categoria.escenas.filter(activa=True)
        
        if escenas_primera_categoria.exists():
            escena_inicial = escenas_primera_categoria.first()
            imagen_inicial = escena_inicial.imagen.url
        elif primera_categoria.imagen_fondo:
            # Si la categoría tiene imagen de fondo pero no escenas, usar esa imagen
            imagen_inicial = primera_categoria.imagen_fondo.url
    
    context = {
        'categorias': categorias,
        'escena_inicial': escena_inicial,
        'imagen_inicial': imagen_inicial,
        'titulo': config.titulo_principal if config else 'Visor 360',
        'logos': logos,
        'config': config,
    }
    
    return render(request, 'cms/visor360.html', context)