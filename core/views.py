from django.shortcuts import render, get_object_or_404
from django.template import loader
from django.http import HttpResponse
from django.contrib import messages
from django.shortcuts import redirect
from django.http import HttpResponseRedirect
from django.db import connection
from django.urls import reverse


from .models import Corretor, Cliente, Imovel
from .forms import CorretorModelForm, ImovelModelForm, ClienteModelForm, BuscaCorretorNomeForm, DelCorretorForm, EdtCorretorForm
#Aqui na pagina de views é possivel adicionar variaveis para o arquivo html
#Lembrar de importar os modelos caso queira algum objeto

def index(request):

    context = { #isso aqui é um dicionário pra passar tudo para o template
        'texto':  'Só testando'
    }
    return render(request, 'index.html', context)


def imoveis(request):

    if Imovel.objects.exists:
        context = {
            'imoveis':Imovel.objects.all()
        }
        return render(request, 'imoveis.html', context)
    else:
        return redirect('cadastroimovel.html')


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
        form = BuscaCorretorNomeForm(request.POST or None)
        if form.is_valid():
            nome = form.cleaned_data['nome']
            corretores = Corretor.objects.raw('SELECT * FROM core_corretor WHERE nome = %s', [nome])
            form = BuscaCorretorNomeForm()
            if not corretores:
                messages.error(request, 'Corretor não encontrado')
    else:
        corretores = Corretor.objects.all()
        form = BuscaCorretorNomeForm(initial={'corretores': corretores}) #é necessário um valor inicial para o formulário
    context = {
        'form': form,
        'corretores': corretores
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


            messages.success(request, 'Corretor cadastrado com sucesso!') #Mensagem de sucesso ao cadastrar corretor
            form = CorretorModelForm() #limpar os dados do formulários preenchido
        else:
            messages.error(request, 'Erro ao cadastrar corretor')
    else:
        form = CorretorModelForm()
    
    context = {
        'form': form
        }
    return render(request, 'cadastrocorretor.html', context)

def atualizarcorretor(request):

    if str(request.method) == 'POST':
        form = EdtCorretorForm(request.POST)
        if form.is_valid():
            creci = form.cleaned_data['creci']
            novonome = form.cleaned_data['novonome']
            form = EdtCorretorForm()
            if get_object_or_404(Corretor, creci = creci):
                with connection.cursor() as cursor:
                    cursor.execute("UPDATE core_corretor SET nome = %s WHERE creci = %s", [novonome, creci])
                    messages.success(request, 'Corretor atualizado com sucesso!') #Mensagem de sucesso ao cadastrar imóvel
                return HttpResponseRedirect("/corretores")
            
        else:
            form = EdtCorretorForm(initial={'nome': ''}) #é necessário um valor inicial para o formulário 
            
    else:
        form = EdtCorretorForm(initial={'nome': ''}) #é necessário um valor inicial para o formulário 
    context = {
        'form': form,
    }
    return render(request, 'atualizarcorretor.html', context)

def deletarcorretor(request):

    if str(request.method) == 'POST':
        form = DelCorretorForm(request.POST)
        if form.is_valid():

            nome = form.cleaned_data['nome']
            creci = form.cleaned_data['creci']
            
            form = DelCorretorForm()
            if get_object_or_404(Corretor, creci = creci):
                with connection.cursor() as cursor:
                    with connection.cursor() as cursor:
                        cursor.execute('DELETE FROM core_corretor WHERE creci = %s AND nome= %s', [creci, nome])
                    messages.success(request, 'Corretor deletado com sucesso!') #Mensagem de sucesso ao cadastrar imóvel
                return HttpResponseRedirect("/corretores")             

        else:
            form = DelCorretorForm(initial={'nome': ''}) #é necessário um valor inicial para o formulário 
            
    else:
        form = DelCorretorForm(initial={'nome': ''}) #é necessário um valor inicial para o formulário 
    context = {
        'form': form,
    }
    return render(request, 'deletarcorretor.html', context)


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