from django.urls import path
from .views import (
    MedicamentoListView, MedicamentoCreateView, MedicamentoUpdateView, MedicamentoDeleteView,
    AplicacaoEventoCreateView, AplicacaoEventoListView,AplicacaoEventoUpdateView, AplicacaoEventoDeleteView, AplicacaoEventoDetailView
)

urlpatterns = [
    # Urls Medicamento
    path('lista', MedicamentoListView.as_view(), name='listamedicamento'),
    path('criar', MedicamentoCreateView.as_view(), name='criarmedicamento'),
    path('<int:pk>/atualizar/', MedicamentoUpdateView.as_view(), name='atualizarmedicamento'),
    path('<int:pk>/deletar/', MedicamentoDeleteView.as_view(), name='deletarmedicamento'),
    # Urls aplicacao Medicamento
    path('aplicacoes/lista', AplicacaoEventoListView.as_view(), name='listaaplicacoes'),
    path('aplicacoes/criar', AplicacaoEventoCreateView.as_view(), name='criaraplicacao'),
    path('aplicacoes/<int:pk>/atualizar/', AplicacaoEventoUpdateView.as_view(), name='atualizaaplicacao'),
    path('aplicacoes/<int:pk>/deletar/', AplicacaoEventoDeleteView.as_view(), name='deletaraplicacao'),
    path('aplicacoes/<int:pk>/', AplicacaoEventoDetailView.as_view(), name='detalheaplicacao'),

]
