from django.urls import path
from medicamento.views import (MedicamentoCreateView, MedicamentoDeleteView, MedicamentoListView, AplicacaoEventoCreateView, AplicacaoEventoDeleteView, AplicacaoEventoListView)

urlpatterns = [
    path('criar/', MedicamentoCreateView.as_view(), name='criarmedicamento'),
    path('listar/', MedicamentoListView.as_view(), name='listamedicamento'),
    path('deletar/<int:pk>/', MedicamentoDeleteView.as_view(), name='deletarmedicamento'),

    path('aplicacao/criar/', AplicacaoEventoCreateView.as_view(), name='criaraplicacao'),
    path('aplicacao/listar/', AplicacaoEventoListView.as_view(), name='listaaplicacao'),
    path('aplicacao/deletar/<int:pk>/', AplicacaoEventoDeleteView.as_view(), name='deletaraplicacao'),
]
