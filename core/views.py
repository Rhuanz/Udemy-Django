from django.shortcuts import render, get_object_or_404
from django.template import loader
from django.http import HttpResponse

from .models import Corretor
#Aqui na pagina de views é possivel adicionar variaveis para o arquivo html
#Lembrar de importar os modelos caso queira algum objeto

def index(request):

    context = { #isso aqui é um dicionário
        'texto':  'Só testando'
    }
    return render(request, 'index.html', context)

def contato(request):
    return render(request, 'contato.html')

def corretores(request):
    context = {
        'corretores': Corretor.objects.all()
    }
    return render(request, 'corretores.html', context)

def corretor(request, nCreci):

    context = {
        #'corretor': Corretor.objects.get(creci = nCreci)
        'corretor': get_object_or_404(Corretor, creci = nCreci)
    }
    return render(request, 'corretor.html', context)

def error404(request, exception):

    template = loader.get_template('404.html')
    return HttpResponse(content=template.render(), content_type='text/html; charset=utf8', status=404)

def error500(request):

    template = loader.get_template('500.html')
    return HttpResponse(content=template.render(), content_type='text/html; charset=utf8', status='500')