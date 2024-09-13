from django.db import models
from stdimage.models import StdImageField

import uuid

#SIGNALS (Aparentemente é para pré processamento dos formulários)
from django.db.models import signals
from django.template.defaultfilters import slugify

#função para criar um nome aleatório para o arquivo
def get_file_path(_instance, filename):
    ext = filename.split('.')[-1] #Tirando a extenção do arquivo do nome
    filename = f'{uuid.uuid4()}.{ext}' #Criando o nome e juntando a extenção
    return filename

#Classe base com metadados de criação e modificação
class Base(models.Model):

    criado = models.DateField(name='Criação', auto_now_add=True) #O auto_now_add adiciona a data de criação automaticamente
    modificado = models.DateField(name='Modificado', auto_now=True) #Auto_now altera a data de modificação sempre que o objeto for modificado

    class Meta:
        abstract = True

#Classe modelo para corretor
class Corretor(Base):

    nome = models.CharField(name='Nome', max_length = 50)
    creci = models.CharField(name='Creci', max_length= 7, primary_key=True, unique=True)
    ativo = models.BooleanField(name='Ativo', default=True)

    def __str__(self):
        return f'{self.Nome} {self.Creci}'
    
    def get_creci(self):
        return self.Creci


#Classe modelo para clientes
class Cliente(Base):
    
    cod = models.AutoField(name='CodCliente', primary_key=True, db_index=True)
    nome = models.CharField(name= 'Nome', max_length=50)
    telefone = models.CharField(name= 'Telefone', max_length=15)
    corretor = models.ForeignKey(Corretor, on_delete=models.CASCADE)
    ativo = models.BooleanField(name='Ativo', default=True)
    compra = models.BooleanField(name='Comprou', default=False)

    def __str__(self): #A função str serve para exibição dos objetos na página de administrador
        return f'{self.Nome}, {self.Telefone}' 
    
    def get_name(self):
        return self.Nome
    
    def get_tel(self):
        return self.Telefone
    
    def get_cod(self):
        return self.CodCliente


#Classe modelo para proprietário
class Proprietario(Base):

    cod = models.AutoField(name='CodProprietario', primary_key=True, db_index=True)
    nome = models.CharField(name='Nome', max_length=50)
    telefone = models.CharField(name='Telefone', max_length=15)

    def __str__(self):
        return f'{self.Nome} {self.Telefone}'


#Classe modelo para o endereço
class Endereco(Base):

    cod = models.AutoField(name='CodEndereco', primary_key=True, db_index=True)
    rua = models.CharField(name='Rua', max_length=40)
    bairro = models.CharField(name='Bairro', max_length=25)
    num = models.IntegerField(name='Numero')
    cidade = models.CharField(name='Cidade', max_length=30)
    comp = models.CharField(name = 'Complemento', max_length=8)

    def __str__(self):
        return f'{self.Cep}, {self.Numero}, {self.Complemento}' #usar os nomes dados as colunas


#Classe modelo para imóveis
class Imovel (Base):

    cod = models.AutoField(name='CodImovel', primary_key=True, db_index=True)
    tipo = models.CharField(name='TipoImovel', max_length=15)
    endereco = models.OneToOneField(Endereco, on_delete=models.CASCADE, unique=True)
    proprietario = models.ForeignKey(Proprietario, on_delete=models.CASCADE)
    valor = models.DecimalField(name='ValorImovel', max_digits=9, decimal_places=2)
    corretor = models.ForeignKey(Corretor, on_delete=models.CASCADE)
    disponivel = models.BooleanField(name='Disponivel', default=True)
    fotos = StdImageField(name='Fotos', upload_to=get_file_path, variations={'thumb': (300, 300)})

    def __str__(self):
        return f'{self.CodImovel}, {self.TipoImovel}, {self.proprietario}'
    
    def get_cod(self):
        return self.CodImovel

#Classe modelo para visitas
class Visita (Base):

    cod = models.AutoField(name='CodVisita', primary_key=True, db_index=True)
    cliente = models.ForeignKey(Cliente, on_delete=models.CASCADE)
    imovel = models.ForeignKey(Imovel, on_delete=models.CASCADE)
    data = models.DateField(name='DataVisita')

    def __str__(self):
        return f'{self.CodVisita}, {self.cliente}, {self.imovel}, {self.DataVisita}'

#Classe modelo para acompanhamentos
class Acompanhamento (Base):

    visita = models.ForeignKey(Visita, on_delete=models.CASCADE)
    corretor = models.ForeignKey(Corretor, on_delete=models.CASCADE)

    def __str__(self):
        return f'{self.corretor}, {self.visita}'

#Classe modelo para vendas
class Venda (Base):

    cod = models.AutoField(name='CodVenda', primary_key=True, db_index=True)
    data = models.DateField(name='Data da venda')
    imovel = models.OneToOneField(Imovel, on_delete=models.CASCADE)
    cliente = models.ForeignKey(Cliente, on_delete=models.CASCADE)
    fPagamento = models.CharField(name='Forma de pagamento', max_length=50)
    entrada = models.BooleanField(name='Entrada', default=True)
    valorF = models.DecimalField(name='Valor final', max_digits=9, decimal_places=2)

    def __str__(self):
        return f'{self.CodVenda}, {self.cliente}, {self.imovel}'

#Classe modelo para intermédios(Corretores envolvidos na venda)
class Intermedio (Base):

    corretor = models.ForeignKey(Corretor, on_delete=models.CASCADE)
    venda = models.ForeignKey(Venda, on_delete=models.CASCADE)

    def __str__(self):
        return f'{self.corretor}, {self.venda}'