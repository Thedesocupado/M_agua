from django.shortcuts import render
from .models import Imagen360

def visor_360(request):
    """Vista principal con imagen 360 de fondo desde base de datos"""
    # Obtener la imagen activa más reciente
    imagen = Imagen360.objects.filter(activa=True).first()
    
    context = {
        'imagen': imagen,
        'titulo': imagen.titulo if imagen else 'Visor 360'
    }
    
    return render(request, 'cms/visor360.html', context)