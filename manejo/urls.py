from django.urls import path
from manejo.views import manejo_unificado

urlpatterns = [
    path('/criar/', manejo_unificado, name='criarmanejo'),
    
]
