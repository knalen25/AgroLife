from django.urls import path
from lote.views import LoteCreateView, LoteDeleteView, LoteDetailView, LoteUpdateView, ListaLoteView

urlpatterns = [

path('criarlote/', LoteCreateView.as_view(), name='criarlote'),
path('listalote/', ListaLoteView.as_view(), name='listalote'),
path('lote/<int:pk>/', LoteDetailView.as_view(), name='detalhelote'),
path('lote/<int:pk>/update/', LoteUpdateView.as_view(), name='atualizalote'),
path('lote/<int:pk>/delete/', LoteDeleteView.as_view(), name='deletalote'),

]