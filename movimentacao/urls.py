from django.urls import path
from .views import TrocaCurralView

urlpatterns = [
    path('criar/', TrocaCurralView.as_view(), name='troca_curral'),
]
