from django.shortcuts import render
from .models import CategoriaEscena, Escena360

def visor_360(request):
    """Vista principal con imagen 360 de fondo y menú jerárquico"""
    # Obtener todas las categorías activas con sus escenas
    categorias = CategoriaEscena.objects.filter(activa=True).prefetch_related(
        'escenas'
    ).order_by('orden')
    
    # Obtener la primera escena de la primera categoría como escena inicial
    escena_inicial = None
    imagen_inicial = None
    
    if categorias.exists():
        primera_categoria = categorias.first()
        escena_inicial = primera_categoria.escenas.filter(activa=True).order_by('orden').first()
        
        # Usar la imagen de fondo de la categoría o la primera escena como fallback
        imagen_inicial = primera_categoria.get_imagen_fondo()
    
    context = {
        'categorias': categorias,
        'escena_inicial': escena_inicial,
        'imagen_inicial': imagen_inicial,
        'titulo': escena_inicial.titulo if escena_inicial else 'Visor 360'
    }
    
    return render(request, 'cms/visor360.html', context)