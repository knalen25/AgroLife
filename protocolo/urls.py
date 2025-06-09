from django.urls import path
from protocolo.views import ProtocoloCreateView, ProtocoloListView, ProtocoloDeleteView, ProtocoloUpdateView, ProtocoloDetailView

urlpatterns = [
    path('criarprotocolo/', ProtocoloCreateView.as_view(), name='criarprotocolo'),
    path('listaprotocolo/', ProtocoloListView.as_view(), name='listaprotocolo'),
    path('protocolo/<int:pk>/', ProtocoloDetailView.as_view(), name='detalheprotocolo'),
    path('protocolo/<int:pk>/update', ProtocoloUpdateView.as_view(), name='atualizarprotocolo'),
    path('protocolo/<int:pk>/delete', ProtocoloDeleteView.as_view(), name='deletarprotocolo'),
]
