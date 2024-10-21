from django.shortcuts import render, get_object_or_404
from django.template import loader
from django.http import HttpResponse
from django.contrib import messages
from django.shortcuts import redirect
from django.http import HttpResponseRedirect
#from django.db import connection

#Usando class based view
from django.views.generic import TemplateView

from .models import Corretor, Cliente, Imovel, Endereco, Visita, Acompanhamento, Venda, Intermedio
from .forms import CorretorModelForm, ImovelModelForm, ClienteModelForm, BuscaCorretorNomeForm
from .forms import DelCorretorForm, EdtCorretorForm, EnderecoModelForm, ProprietarioModelForm
from .forms import BuscaImovelCod, BuscaImovelEnd, EdtImovelForm, VisitaModelForm, AcompanhamentoModelForm
from .forms import VendaModelForm, BuscaVendaCod, BuscaVendaCorretor

class IndexView(TemplateView):
    template_name = 'index.html'

def imoveis(request):

    form = BuscaImovelCod(request.POST)
    form2 = BuscaImovelEnd(request.POST)
    if form.is_valid() and form.has_changed():

        cod = form.cleaned_data['cod']
        form = BuscaImovelCod()
        try: #o método get do orm retorna exception caso não encontre o objeto, por isso a necessidade do try
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
        form = BuscaImovelCod()
        form2 = BuscaImovelEnd()
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
        return HttpResponseRedirect("/cadastroproprietario")
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
        return HttpResponseRedirect("/cadastroimovel")
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

    form = CorretorModelForm(request.POST)
    if form.has_changed():
        if form.is_valid():
            form.save()
            messages.success(request, 'Corretor cadastrado com sucesso!') #Mensagem de sucesso ao cadastrar corretor
            form = CorretorModelForm() #limpar os dados do formulários preenchido
            return HttpResponseRedirect("/corretores")
        else:
            form = CorretorModelForm()
            messages.error(request, 'Erro ao cadastrar corretor')
    else:
        form = CorretorModelForm()
    
    context = {
        'form': form
        }
    return render(request, 'cadastrocorretor.html', context)

def atualizarcorretor(request):

    form = EdtCorretorForm(request.POST)
    if form.has_changed():
        if form.is_valid():
            creci = form.cleaned_data['creci']
            novonome = form.cleaned_data['novonome']
            status = form.cleaned_data['status']
            form = EdtCorretorForm()
            try:
                corretor = get_object_or_404(Corretor, Creci = creci)
                corretor.Nome = novonome
                corretor.Ativo = status
                corretor.save()
                #with connection.cursor() as cursor:
                #cursor.execute("UPDATE core_corretor SET nome = %s WHERE creci = %s", [novonome, creci])
            except:
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

    form = DelCorretorForm(request.POST)
    if form.has_changed():
        if form.is_valid():
            nome = form.cleaned_data['nome']
            creci = form.cleaned_data['creci']
            
            form = DelCorretorForm()
            try:
                delCorret = get_object_or_404(Corretor, Creci = creci)
                delCorret.delete()
                #with connection.cursor() as cursor:
                #cursor.execute('DELETE FROM core_corretor WHERE "Creci" = %s AND "Nome" = %s', [creci, nome])
                messages.success(request, 'Corretor deletado com sucesso!') #Mensagem de sucesso ao cadastrar imóvel
                return HttpResponseRedirect("/corretores")
            except:
                messages.error(request, 'Corretor não encontrado!') #Mensagem de sucesso ao cadastrar imóvel
                return HttpResponseRedirect("/corretores")
        else:
            form = DelCorretorForm()             
    else:
        form = DelCorretorForm() #é necessário um valor inicial para o formulário 
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
    
    cliente = get_object_or_404(Cliente, CodCliente = codCliente)
    
    context = {
        'cliente': cliente
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

def cadastrovisita(request, codCliente):
    
    form = VisitaModelForm(request.POST)
    form2 = AcompanhamentoModelForm(request.POST)
    cliente = get_object_or_404(Cliente, CodCliente = codCliente)
    if form.has_changed() and form2.has_changed():

        if form.is_valid() and form2.is_valid():
            
            data = form.cleaned_data['DataVisita']
            imv = form.cleaned_data['imovel']
            corretor = form2.cleaned_data['corretor']

            nv = Visita(DataVisita = data, imovel= imv, cliente=cliente)
            nv.save()

            na = Acompanhamento(corretor = corretor, visita = nv)
            na.save()
            
            form = VisitaModelForm()
            form2 = AcompanhamentoModelForm()

            messages.success(request, 'Visita registrada')
    else:
        form = VisitaModelForm()
        form2 = AcompanhamentoModelForm()
    context = {
        'form': form,
        'form2': form2,
        'cliente': cliente
    }
    return render(request, 'cadastrovisita.html', context)

def vendas(request):
    form = BuscaVendaCod(request.POST)
    form2 = BuscaVendaCorretor(request.POST)
    if form.is_valid() and form.has_changed():

        cod = form.cleaned_data['cod']
        form = BuscaVendaCod()
        try: #o método get do orm retorna exception caso não encontre o objeto, por isso a necessidade do try
            vendas = [Venda.objects.get(CodVenda = cod)]
            messages.success(request, 'Dados encontrados')

        except:
            vendas = Venda.objects.all()
            messages.error(request, 'Código inválido')

    elif form2.is_valid() and form2.has_changed():

        nmcorretor = form2.cleaned_data['corretor']
        form2 = BuscaVendaCorretor()

        vendas = Venda.objects.raw('SELECT * FROM core_venda WHERE "CodVenda" IN (SELECT venda_id FROM core_intermedio WHERE corretor_id = (SELECT "Creci" FROM core_corretor WHERE "Nome" = %s))', [nmcorretor])
        
        if vendas.__len__() > 0:
            messages.success(request, 'Vendas encontrados')
        else:
            vendas = Venda.objects.all()
            messages.error(request, 'Vendas não encontradas')

    else:
        vendas = Venda.objects.all()
        form = BuscaVendaCod()
        form2 = BuscaVendaCorretor()
    context = {
        'form': form,
        'form2': form2,
        'vendas': vendas
    }
    return render(request, 'vendas.html', context)

def venda(request):
    pass

def cadastrovenda(request):

    form = VendaModelForm(request.POST)

    if form.is_valid() and form.has_changed():
        form.save()
        form = VendaModelForm() #limpar os dados do formulários preenchido
        messages.success(request, 'Venda registrada!') #Mensagem de sucesso ao cadastrar imóvel
        return HttpResponseRedirect("/vendas")
    else:
        form = VendaModelForm()
        messages.error(request, 'Erro ao registrar venda')

    context = {
        'form': form
    }
    return render(request, 'cadastrovenda.html', context)

def error404(request, exception):

    template = loader.get_template('404.html')
    return HttpResponse(content=template.render(), content_type='text/html; charset=utf8', status=404)

def error500(request):

    template = loader.get_template('500.html')
    return HttpResponse(content=template.render(), content_type='text/html; charset=utf8', status='500')