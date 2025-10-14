from django.shortcuts import render
from .models import CategoriaEscena, Escena360, LogoCreador, ConfiguracionInterfaz

def visor_360(request):
    """Vista principal con imagen 360 de fondo y menú jerárquico"""
    # Obtener todas las categorías activas con sus escenas
    categorias = CategoriaEscena.objects.filter(activa=True).prefetch_related(
        'escenas'
    ).order_by('orden')
    
    # Obtener logos activos
    logos = LogoCreador.objects.filter(activo=True).order_by('orden')[:3]
    
    # Obtener configuración de interfaz
    config = ConfiguracionInterfaz.objects.first()
    if not config:
        # Crear configuración por defecto si no existe
        config = ConfiguracionInterfaz.objects.create()
    
    # Obtener la primera escena de la primera categoría como escena inicial
    escena_inicial = None
    imagen_inicial = None
    
    if categorias.exists():
        primera_categoria = categorias.first()
        escena_inicial = primera_categoria.escenas.filter(activa=True).order_by('orden').first()
        imagen_inicial = primera_categoria.get_imagen_fondo()
    
    context = {
        'categorias': categorias,
        'escena_inicial': escena_inicial,
        'imagen_inicial': imagen_inicial,
        'logos': logos,
        'config': config,
        'titulo': escena_inicial.titulo if escena_inicial else 'Visor 360'
    }
    
    return render(request, 'cms/visor360.html', context)