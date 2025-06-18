from django.urls import path
from boi.views import BoiCreateView, BoiDeleteView, BoiDetailView, BoiMorteView, BoiUpdateView,ListaBoiView, ListaBoiMorteView

urlpatterns = [
    path('criar/', BoiCreateView.as_view(), name='criarboi'),
    path('lista/', ListaBoiView.as_view(), name='listaboi'),
    path('<int:pk>/', BoiDetailView.as_view(), name='detalheboi'),
    path('<int:pk>/update/', BoiUpdateView.as_view(), name='atualizaboi'),
    path('<int:pk>/delete/', BoiDeleteView.as_view(), name='deletaboi'),
    path('<int:pk>/morte/', BoiMorteView.as_view(), name='boimorte'),
    path('listamorte/', ListaBoiMorteView.as_view(), name='listamorte'),
]