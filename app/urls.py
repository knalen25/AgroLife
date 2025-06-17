from django.contrib import admin
from django.urls import path, include
from boi import views
from account import views as v2 
from django.contrib import admin
from app import views as v

urlpatterns = [
    
    path('', v.home, name='base'),
    path('admin/', admin.site.urls),
    path("curral/", include("curral.urls")),
    path("medicamento/", include("medicamento.urls")),
    path("lote/", include("lote.urls")),
    path("boi/", include("boi.urls")),
    path("account/", include("account.urls")),
    path('login/', v2.login_view, name='login'),
    path('logout/', v2.logout_view, name='logout'),
    path('protocolo/', include("protocolo.urls")),
    path('movimentacao/', include("movimentacao.urls")),
    path('manejo/', include('manejo.urls')),
]