from django.shortcuts import render, get_object_or_404
from django.template import loader
from django.http import HttpResponse
from django.contrib import messages
from django.shortcuts import redirect
from django.http import HttpResponseRedirect
#from django.db import connection

#Usando class based view
from django.views.generic import TemplateView

from .models import Corretor, Cliente, Imovel, Endereco
from .forms import CorretorModelForm, ImovelModelForm, ClienteModelForm, BuscaCorretorNomeForm
from .forms import DelCorretorForm, EdtCorretorForm, EnderecoModelForm, ProprietarioModelForm
from .forms import BuscaImovelCod, BuscaImovelEnd, EdtImovelForm


class IndexView(TemplateView):
    template_name = 'index.html'

def imoveis(request):

    form = BuscaImovelCod(request.POST)
    form2 = BuscaImovelEnd(request.POST)
    if form.is_valid() and form.has_changed():

        cod = form.cleaned_data['cod']
        form = BuscaImovelCod()
        try: #o método get do orm retorna exception, por isso a necessidade do try
            imoveis = [Imovel.objects.get(CodImovel = cod)]
            messages.success(request, 'Imovel encontrado')

        except:
            imoveis = Imovel.objects.raw('SELECT * FROM core_imovel WHERE "Disponivel" = True')
            messages.error(request, 'Código inválido')

    elif form2.is_valid() and form2.has_changed():

        bairro = form2.cleaned_data['bairro']
        cidade = form2.cleaned_data['cidade']

        form2 = BuscaImovelEnd()

        imoveis = Imovel.objects.raw('SELECT * FROM core_imovel WHERE endereco_id IN (SELECT "CodEndereco" FROM core_endereco WHERE "Bairro" = %s AND "Cidade" = %s)', [bairro, cidade])
        
        if imoveis.__len__() > 0:
            messages.success(request, 'Imoveis encontrados')
        else:
            imoveis = Imovel.objects.raw('SELECT * FROM core_imovel WHERE "Disponivel" = True')
            messages.error(request, 'Bairro ou cidade não encontrados')

    else:
        imoveis = Imovel.objects.raw('SELECT * FROM core_imovel WHERE "Disponivel" = True')
        form = BuscaImovelCod(initial={'imoveis': imoveis})
    context = {
        'form': form,
        'form2': form2,
        'imoveis': imoveis
    }
    return render(request, 'imoveis.html', context)

def imovel(request, codImovel):

    context = {
        'imovel' : get_object_or_404(Imovel, CodImovel = codImovel)
    }
    return render(request, 'imovel.html', context)

def atualizarimovel(request):

    form = EdtImovelForm(request.POST, request.FILES)
    if form.is_valid():
        cod = form.cleaned_data['cod']
        novotipo = form.cleaned_data['tipo']
        novovalor = form.cleaned_data['valor']
        dispon = form.cleaned_data['disponivel']
        fotos = form.cleaned_data['fotos']

        form = EdtImovelForm()

        try:
            
            imovel = get_object_or_404(Imovel, CodImovel = cod)
            
            if len(novotipo) > 0:
                imovel.TipoImovel = novotipo
            if novovalor is not None:
                imovel.ValorImovel = novovalor
            if fotos is not None:
                imovel.Fotos = fotos

            imovel.Disponivel = dispon
            imovel.save()

            messages.success(request, 'Imovel atualizado com sucesso!') #Mensagem de sucesso ao cadastrar imóvel
            return HttpResponseRedirect("/imoveis")
        
        except:
            messages.error(request, 'Imovel não existe na base de dados!') #Mensagem de erro
            return HttpResponseRedirect("/imoveis")
    else:
        form = EdtImovelForm(initial={'CodImovel': ''}) #é necessário um valor inicial para o formulário 
        
    context = {
        'form': form,
    }
    return render(request, 'atualizarimovel.html', context)

def cadastroimovel(request):

    form = ImovelModelForm(request.POST, request.FILES)
    if form.is_valid():
        form.save() #Salvando no banco de dados
        form = ImovelModelForm()#limpar os dados do formulários preenchido
        messages.success(request, 'Imovel cadastrado com sucesso!') #Mensagem de sucesso ao cadastrar imóvel
        return HttpResponseRedirect("/imoveis")
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

    form = ClienteModelForm(request.POST)
    if form.has_changed():
        if form.is_valid():
            form.save()
            form = ClienteModelForm() #limpar os dados do formulários preenchido
            messages.success(request, 'Cliente cadastrado com sucesso!') #Mensagem de sucesso ao cadastrar imóvel
            return HttpResponseRedirect("/clientes")
        
        else:
            messages.error(request, 'Erro ao cadastrar cliente')
    else:
        form = ClienteModelForm() #Formulário inicial limpo
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