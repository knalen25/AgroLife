from django.urls import path
from curral.views import CurralCreateView, CurralDeleteView, CurralDetailView, CurralUpdateView, ListaCurralView

urlpatterns = [
    path('criar/', CurralCreateView.as_view(), name='criarcurral'),
    path('lista/', ListaCurralView.as_view(), name='listacurral'),
    path('<int:pk>/', CurralDetailView.as_view(), name='detalhecurral'),
    path('<int:pk>/update/', CurralUpdateView.as_view(), name='atualizacurral'),
    path('<int:pk>/delete/', CurralDeleteView.as_view(), name='deletacurral'),
]