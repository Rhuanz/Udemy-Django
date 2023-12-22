from django.shortcuts import render
from .models import Corretor
# Create your views here.

#Aqui na pagina de views é possivel adicionar variaveis para o arquivo html
#Lembrar de importar os modelos caso queira algum objeto
def index(request):

    corretores = Corretor.objects.all()
    context = { #isso aqui é um dicionário
        'texto':  'Só testando',
        'corretores': corretores
    }
    return render(request, 'index.html', context)

def contato(request):
    return render(request, 'contato.html')

def corretores(request, creci):
    return render(request, 'corretores.html')