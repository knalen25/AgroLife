from django.urls import path
from manejo.views import criar_manejo_entrada, manejo_saida_venda, manejo_movimentacao, ManejoListView, ManejoDetailView, ManejoUpdateView, ManejoDeleteView


urlpatterns = [
    path('entrada/', criar_manejo_entrada, name='criar_manejo_entrada'),
    path('venda/', manejo_saida_venda, name='manejo_saida_venda'),
    path('movimentacao/', manejo_movimentacao, name='manejo_movimentacao'),
    path('lista/', ManejoListView.as_view(), name='listamanejo'),
    path('lista/<str:tipo>/', ManejoListView.as_view(), name='listamanejo_filtrada'),
    path('<int:pk>/',ManejoDetailView.as_view(),name='detalhemanejo'),
    path('<int:pk>/editar/', ManejoUpdateView.as_view(), name='editarmanejo'),
    path('<int:pk>/deletar/', ManejoDeleteView.as_view(), name='deletarmanejo'),
]
