from django.urls import path
from .views import MovimentacaoView, MovimentacaoDeleteView, MovimentacaoDetailView, MovimentacaoListView, MovimentacaoUpdateView

urlpatterns = [
    path('criar/', MovimentacaoView.as_view(), name='criarmovimentacao'),
    path('lista/', MovimentacaoListView.as_view(), name='listamovimentacao'),
    path('<int:pk>/', MovimentacaoDetailView.as_view(), name='detalhemovimentacao'),
    path('<int:pk>/editar/', MovimentacaoUpdateView.as_view(), name='editarmovimentacao'),
    path('<int:pk>/deletar/', MovimentacaoDeleteView.as_view(), name='deletarmovimentacao'),
]
