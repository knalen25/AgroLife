from django.urls import path
from .views import MovimentacaoView

urlpatterns = [
    path('criar/', MovimentacaoView.as_view(), name='criarmovimentacao'),
    # path('lista/', MovimentacaoView.as_view(), name='listamovimentacao'),
    # path('criar/', MovimentacaoView.as_view(), name='criarmovimentacao'),
    # path('criar/', MovimentacaoView.as_view(), name='criarmovimentacao'),
    # path('criar/', MovimentacaoView.as_view(), name='criarmovimentacao'),
]
