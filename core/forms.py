from django import forms
from .models import Corretor, Cliente, Imovel, Endereco, Proprietario
from .models import Visita, Acompanhamento, Venda

#formulários modelo pra classes do banco de dados
class CorretorModelForm(forms.ModelForm):

    class Meta:
        model = Corretor
        fields = ['Nome', 'Creci', 'Ativo']

class ClienteModelForm(forms.ModelForm):

    class Meta:
        model = Cliente
        fields = ['CodCliente', 'Nome', 'Telefone', 'corretor']

class EnderecoModelForm(forms.ModelForm):

    class Meta:
        model = Endereco
        fields = ['CodEndereco', 'Rua', 'Bairro', 'Numero', 'Cidade', 'Complemento']

class ProprietarioModelForm(forms.ModelForm):
    
    class Meta:
        model = Proprietario
        fields = ['CodProprietario', 'Nome', 'Telefone']

        
class ImovelModelForm(forms.ModelForm):

    class Meta:
        model = Imovel
        fields = ['CodImovel', 'TipoImovel', 'endereco', 'proprietario', 'ValorImovel', 'corretor', 'Disponivel', 'Fotos']

class VisitaModelForm(forms.ModelForm):

    class Meta:
        model = Visita
        fields = ['CodVisita', 'imovel', 'DataVisita']

class AcompanhamentoModelForm(forms.ModelForm):

    class Meta:
        model = Acompanhamento
        fields = ['corretor']

class VendaModelForm(forms.ModelForm):

    class Meta:
        model = Venda
        fields = ['CodVenda', 'DataVenda', 'imovel', 'cliente', 'FormaPagamento', 'Entrada', 'ValorFinal']

#Demais formulários
class BuscaCorretorNomeForm(forms.Form):

    nome = forms.CharField(label='Nome do corretor', max_length= 30, widget=forms.TextInput())

class EdtCorretorForm(forms.Form):

    creci = forms.CharField(label='Creci do corretor', max_length=7)
    novonome = forms.CharField(label='Novo nome', max_length=30)
    status = forms.BooleanField(label='Ativo', required=False)

class DelCorretorForm(forms.Form):

    nome = forms.CharField(label='Nome do corretor', max_length= 30, widget=forms.TextInput())
    creci = forms.CharField(label='Creci do corretor', max_length=7)

class BuscaImovelCod(forms.Form):

    cod = forms.IntegerField(label='Codigo do imóvel', required=False)

class BuscaImovelEnd(forms.Form):

    bairro = forms.CharField(label='Bairro:', max_length=30, required=False)
    cidade = forms.CharField(label='Cidade:', max_length=30, required=False)

class EdtImovelForm(forms.Form):

    cod = forms.IntegerField(label= 'Código do imóvel a ser alterado:')
    tipo = forms.CharField(label='Tipo do imóvel:', required = False)
    valor = forms.DecimalField(label='Novo valor:', required = False)
    disponivel = forms.BooleanField(label = 'Continua disponível?', required = False)
    fotos = forms.ImageField(label='Fotos do imóvel:',required = False)

class BuscaVendaCod(forms.Form):
    cod = forms.IntegerField(label='Codigo da venda:', required=False)

class BuscaVendaCorretor(forms.Form):
    corretor = forms.CharField(label='Nome do corretor:', required=False)