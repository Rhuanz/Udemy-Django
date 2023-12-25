from django.urls import path
from .views import index, contato, corretores, corretor

urlpatterns = [
    path('', index, name = 'index'),
    path('contato', contato, name = 'contato'),
    path('corretores', corretores, name = 'corretores'),
    path('corretor/<int:nCreci>', corretor, name = 'corretor'),
]