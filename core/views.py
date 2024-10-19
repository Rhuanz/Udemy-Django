from django.shortcuts import render, get_object_or_404
from django.template import loader
from django.http import HttpResponse
from django.contrib import messages
from django.shortcuts import redirect
from django.http import HttpResponseRedirect
#from django.db import connection

#Usando class based view
from django.views.generic import TemplateView

from .models import Corretor, Cliente, Imovel
from .forms import CorretorModelForm, ImovelModelForm, ClienteModelForm, BuscaCorretorNomeForm
from .forms import DelCorretorForm, EdtCorretorForm, EnderecoModelForm, ProprietarioModelForm

class IndexView(TemplateView):
    template_name = 'index.html'

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

    form = ImovelModelForm(request.POST, request.FILES)
    if form.is_valid():
        form.save() #Salvando no banco de dados
        form = ImovelModelForm()#limpar os dados do formulários preenchido
        messages.success(request, 'Imovel cadastrado com sucesso!') #Mensagem de sucesso ao cadastrar imóvel
    else:
        form = ImovelModelForm()

    context = {
        'form': form
    }
    return render(request, 'cadastroimovel.html', context)

def cadastroendereco(request):

    form = EnderecoModelForm(request.POST)
    if form.is_valid():
        form.save()
        form = EnderecoModelForm()
        messages.success(request, 'Endereço cadastrado com sucesso!')
    else:
        form = EnderecoModelForm()
    context = {'form': form}
    return render(request, 'cadastroendereco.html', context)
    
def cadastroproprietario(request):
    form = ProprietarioModelForm(request.POST)
    if form.is_valid():
        form.save()
        form = ProprietarioModelForm()
        messages.success(request, 'Proprietario cadastrado com sucesso!')
    else:
        form = ProprietarioModelForm()
    context = {'form': form}
    return render(request, 'cadastroproprietario.html', context)

def corretores(request):

    form = BuscaCorretorNomeForm(request.POST)
    if form.is_valid():
        nome = form.cleaned_data['nome']
        corretores = Corretor.objects.raw('SELECT * FROM core_corretor WHERE "Nome" = %s', [nome]) #lembrar de colocar aspas no nome da coluna para que diferencie maiuscula e minúscula
        form = BuscaCorretorNomeForm()

        if corretores.__len__() > 0:
            messages.success(request, 'Corretor encontrado')
        else:
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
        'corretor': get_object_or_404(Corretor, Creci = nCreci)
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
            status = form.cleaned_data['status']
            form = EdtCorretorForm()
            if get_object_or_404(Corretor, Creci = creci):

                corretor = Corretor.objects.get(Creci = creci)
                corretor.Nome = novonome
                corretor.Ativo = status
                corretor.save()
                #with connection.cursor() as cursor:
                    #cursor.execute("UPDATE core_corretor SET nome = %s WHERE creci = %s", [novonome, creci])
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
            if get_object_or_404(Corretor, Creci = creci):
                Corretor.objects.get(Creci = creci, Nome=nome).delete()
                #with connection.cursor() as cursor:
                    #cursor.execute('DELETE FROM core_corretor WHERE "Creci" = %s AND "Nome" = %s', [creci, nome])
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