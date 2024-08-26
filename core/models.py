from django.db import models
from stdimage.models import StdImageField

#SIGNALS (Aparentemente é para pré processamento dos formulários)
from django.db.models import signals
from django.template.defaultfilters import slugify


# Create your models here.
class Corretor(models.Model):

    nome = models.CharField('Nome', max_length = 50)
    creci = models.CharField('Creci', max_length= 7, primary_key=True, unique=True)
    slug = models.SlugField(name='Slug', max_length=50, blank=True, editable=False)

    def __str__(self):
        return f'{self.nome} {self.creci}'
    
    def get_creci(self):
        return self.creci
    
def corretor_pre_save(signal, instance, sender, **kwargs):
    instance.slug = slugify(instance.nome)

signals.pre_save.connect(corretor_pre_save, sender=Corretor)

class Cliente(models.Model):
    
    cod = models.AutoField(name='CodCliente', primary_key=True, db_index=True)
    nome = models.CharField('Nome', max_length=50)
    telefone = models.CharField('Telefone', max_length=15)
    corretor = models.ForeignKey(Corretor, on_delete=models.CASCADE)

    def __str__(self):
        return f'{self.nome}, {self.telefone}' #mostra o nome do cliente produto na lista, Lembrar de usar os nomes dados as colunas
    
    def get_name(self):
        return self.nome
    
    def get_tel(self):
        return self.telefone
    
    def get_cod(self):
        return self.CodCliente

class Proprietario(models.Model):

    cod = models.AutoField(name='CodProprietario', primary_key=True, db_index=True)
    nome = models.CharField(name='Nome', max_length=50)
    telefone = models.CharField(name='Telefone', max_length=15)

    def __str__(self):
        return f'{self.Nome} {self.Telefone}'


class Endereco(models.Model):

    cod = models.AutoField(name='CodEndereco', primary_key=True, db_index=True)
    cep = models.CharField(name='Cep', max_length=8, null=False)
    num = models.IntegerField(name='Numero')
    comp = models.CharField(name = 'Complemento', max_length=8)

    def __str__(self):
        return f'{self.Cep}, {self.Numero}, {self.Complemento}' #usar os nomes dados as colunas


class Imovel (models.Model):

    cod = models.AutoField(name='CodImovel', primary_key=True, db_index=True)
    tipo = models.CharField(name='TipoImovel', max_length=15)
    endereco = models.OneToOneField(Endereco, on_delete=models.CASCADE)
    proprietario = models.ForeignKey(Proprietario, on_delete=models.CASCADE)
    valor = models.DecimalField(name='ValorImovel', max_digits=9, decimal_places=2)
    corretor = models.ForeignKey(Corretor, on_delete=models.CASCADE)
    disponivel = models.BooleanField('Disponível?', default=True)

    def __str__(self):
        return f'{self.CodImovel}, {self.TipoImovel}, {self.proprietario}'
    
    def get_cod(self):
        return self.CodImovel

class Visita (models.Model):

    cod = models.AutoField(name='CodVisita', primary_key=True, db_index=True)
    cliente = models.ForeignKey(Cliente, on_delete=models.CASCADE)
    imovel = models.ForeignKey(Imovel, on_delete=models.CASCADE)
    data = models.DateField(name='DataVisita')

    def __str__(self):
        return f'{self.codVisita}, {self.cliente}, {self.imovel}, {self.DataVisita}'

class Acompanhamento (models.Model):

    visita = models.ForeignKey(Visita, on_delete=models.CASCADE)
    corretor = models.ForeignKey(Corretor, on_delete=models.CASCADE)

    def __str__(self):
        return f'{self.corretor}, {self.visita}'

class Venda (models.Model):

    cod = models.AutoField(name='CodVenda', primary_key=True, db_index=True)
    data = models.DateField(name='Data da venda')
    imovel = models.OneToOneField(Imovel, on_delete=models.CASCADE)
    cliente = models.ForeignKey(Cliente, on_delete=models.CASCADE)
    fPagamento = models.CharField(name='Forma de pagamento', max_length=50)
    entrada = models.BooleanField(name='Entrada', default=True)
    valorF = models.DecimalField(name='Valor final', max_digits=9, decimal_places=2)
    fotos = StdImageField(name='Fotos', upload_to='imoveis', variations={'thumb': (300, 300)})

    def __str__(self):
        return f'{self.codVenda}, {self.cliente}, {self.imovel}'

class Intermedio (models.Model):

    corretor = models.ForeignKey(Corretor, on_delete=models.CASCADE)
    venda = models.ForeignKey(Venda, on_delete=models.CASCADE)

    def __str__(self):
        return f'{self.corretor}, {self.venda}'