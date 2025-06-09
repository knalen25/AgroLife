from django.urls import path
from curral.views import CurralCreateView, CurralDeleteView, CurralDetailView, CurralUpdateView, ListaCurralView

urlpatterns = [

    path('criarcurral/', CurralCreateView.as_view(), name='criarcurral'),
    path('listacurral/', ListaCurralView.as_view(), name='listacurral'),
    path('curral/<int:pk>/', CurralDetailView.as_view(), name='detalhecurral'),
    path('curral/<int:pk>/update/', CurralUpdateView.as_view(), name='atualizacurral'),
    path('curral/<int:pk>/delete/', CurralDeleteView.as_view(), name='deletacurral'),

]