from django.shortcuts import render

# Create your views here.
#Aqui na pagina de views é possivel adicionar variaveis para o arquivo html

def index(request):
    context = {
        'texto':  'testando'
    }
    return render(request, 'index.html', context)

def contato(request):
    return render(request, 'contato.html')