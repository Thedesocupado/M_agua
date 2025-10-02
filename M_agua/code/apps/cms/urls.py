from django.urls import path
from . import views

app_name = 'cms'

urlpatterns = [
    path('', views.visor_360, name='visor_360'),
]