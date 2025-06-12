from django.urls import path
from manejo.views import criar_manejo_entrada, manejo_saida_venda


urlpatterns = [
    path('entrada/', criar_manejo_entrada, name='criar_manejo_entrada'),
    path('venda/', manejo_saida_venda, name='manejo_saida_venda'),
]