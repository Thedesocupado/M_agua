from django.shortcuts import render

def visor_360(request):
    """Vista principal con imagen 360 de fondo"""
    return render(request, 'cms/visor360.html')