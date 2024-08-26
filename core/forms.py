from django import forms
from .models import Corretor, Cliente, Imovel

class BuscaCorretorNomeForm(forms.Form):

    nome = forms.CharField(label='Nome do corretor', max_length= 30, widget=forms.TextInput())

class EdtCorretorForm(forms.Form):

    creci = forms.CharField(label='Creci do corretor', max_length=5)
    novonome = forms.CharField(label='Novo nome', max_length=30)

class DelCorretorForm(forms.Form):

    nome = forms.CharField(label='Nome do corretor', max_length= 30, widget=forms.TextInput())
    creci = forms.CharField(label='Creci do corretor', max_length=5)


class CorretorModelForm(forms.ModelForm):

    class Meta:
        model = Corretor
        fields = ['nome', 'creci']

class ClienteModelForm(forms.ModelForm):

    class Meta:
        model = Cliente
        fields = ['CodCliente', 'nome', 'telefone', 'corretor']

class ImovelModelForm(forms.ModelForm):

    class Meta:
        model = Imovel
        fields = ['CodImovel', 'TipoImovel', 'endereco', 'proprietario', 'ValorImovel', 'corretor', 'disponivel']
