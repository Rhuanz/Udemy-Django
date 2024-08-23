from django.urls import path
from .views import index, imoveis, corretores, corretor

urlpatterns = [
    path('', index, name = 'index'),
    path('imoveis/', imoveis, name = 'imoveis'),
    path('corretores/', corretores, name = 'corretores'),
    path('corretor/<int:nCreci>', corretor, name = 'corretor'),
]