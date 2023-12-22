from django.urls import path
from .views import index, contato, corretores

urlpatterns = [
    path('', index, name = 'index'),
    path('contato', contato, name = 'contato'),
    path('Corretores/<int:creci>', corretores, name = 'corretores'),
]