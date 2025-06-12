from django.urls import path
from lote.views import LoteCreateView, LoteDeleteView, LoteDetailView, LoteUpdateView, ListaLoteView

urlpatterns = [
    path('lista/', ListaLoteView.as_view(), name='listalote'),
    path('criar/', LoteCreateView.as_view(), name='criarlote'),
    path('<int:pk>/', LoteDetailView.as_view(), name='detalhelote'),
    path('<int:pk>/update/', LoteUpdateView.as_view(), name='atualizalote'),
    path('<int:pk>/delete/', LoteDeleteView.as_view(), name='deletalote'),
]