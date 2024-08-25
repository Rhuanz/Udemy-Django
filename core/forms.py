from django import forms
from .models import Corretor, Cliente, Imovel


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