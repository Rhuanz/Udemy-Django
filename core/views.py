from django.shortcuts import render, get_object_or_404
from django.template import loader
from django.http import HttpResponse
from django.contrib import messages

from .models import Corretor, Cliente, Imovel
from .forms import CorretorModelForm, ImovelModelForm, ClienteModelForm
#Aqui na pagina de views é possivel adicionar variaveis para o arquivo html
#Lembrar de importar os modelos caso queira algum objeto

def index(request):

    context = { #isso aqui é um dicionário pra passar tudo para o template
        'texto':  'Só testando'
    }
    return render(request, 'index.html', context)


def imoveis(request):

    context = {
        'imoveis':Imovel.objects.all()
    }
    return render(request, 'imoveis.html', context)


def imovel(request, codImovel):

    context = {
        'imovel' : get_object_or_404(Imovel, CodImovel = codImovel)
    }
    return render(request, 'imovel.html', context)


def cadastroimovel(request):

    if str(request.method) == 'POST':
        form = ImovelModelForm(request.POST, request.FILES)
        if form.is_valid():
            imov = form.save(commit=False)

            print(f'tipo: {imov.ValorImovel}')

            messages.success(request, 'Imovel cadastrado com sucesso!') #Mensagem de sucesso ao cadastrar imóvel
            form = ImovelModelForm() #limpar os dados do formulários preenchido
        else:
            messages.error(request, 'Erro ao cadastrar imóvel')
    else:
        form = ImovelModelForm()

    context = {
        'form': form
        }
    return render(request, 'cadastroimovel.html', context)


def corretores(request):

    if str(request.method) == 'POST':
        form = CorretorModelForm(request.POST)

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

def cadastrocorretor(request):

    if str(request.method) == 'POST':
        form = CorretorModelForm(request.POST)
        if form.is_valid():
            form.save()


            messages.success(request, 'Corretor cadastrado com sucesso!') #Mensagem de sucesso ao cadastrar imóvel
            form = CorretorModelForm() #limpar os dados do formulários preenchido
        else:
            messages.error(request, 'Erro ao cadastrar corretor')
    else:
        form = CorretorModelForm()
    
    context = {
        'form': form
        }
    return render(request, 'cadastrocorretor.html', context)


def clientes(request):

    context = {
        'clientes': Cliente.objects.all()
    }
    return render(request, 'clientes.html', context)

def cliente(request, codCliente):

    context = {
        'cliente': get_object_or_404(Cliente, CodCliente = codCliente)
    }
    return render(request, 'cliente.html', context)

def cadastrocliente(request):

    if str(request.method) == 'POST':
        form = ClienteModelForm(request.POST)
        if form.is_valid():
            form.save()


            messages.success(request, 'Cliente cadastrado com sucesso!') #Mensagem de sucesso ao cadastrar imóvel
            form = ClienteModelForm() #limpar os dados do formulários preenchido
        else:
            messages.error(request, 'Erro ao cadastrar cliente')
    else:
        form = ClienteModelForm()
    
    context = {
        'form': form
        }
    return render(request, 'cadastrocliente.html', context)


def error404(request, exception):

    template = loader.get_template('404.html')
    return HttpResponse(content=template.render(), content_type='text/html; charset=utf8', status=404)

def error500(request):

    template = loader.get_template('500.html')
    return HttpResponse(content=template.render(), content_type='text/html; charset=utf8', status='500')