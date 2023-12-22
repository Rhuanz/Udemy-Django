from django.db import models

# Create your models here.

#Estudar herança para melhorar as classes cliente, corretor e proprietário
class Cliente(models.Model):
    nome = models.CharField('Nome', max_length=50)
    telefone = models.CharField('Telefone', max_length=15)
    dataEntrada = models.DateField('Data de Entrada')
    dataUltimAtualiza = models.DateField('Ultima atualização')
    contatoInicial = models.BooleanField('Contato bem sucedido')
    situacao = models.BooleanField('Conversando')
    andamento = models.CharField('Andamento', max_length=200)

    def __str__(self):
        return self.nome #mostra o nome do produto na lista

class Imovel (models.Model):
    residencial = models.CharField('Residencial', max_length=50)
    endereco = models.CharField('Endereço', max_length=200)
    proprietario = models.CharField('Proprietário', max_length=100)
    telefone = models.CharField('Telefone', max_length=15)
    midia = models.ImageField('Fotos', default= '') #verificar como deixar vazio
    corretor = models.CharField('Corretor', max_length=50) #Verificar como colcoar uma objeto aqui

    def __str__(self):
        return f'{self.residencial} {self.proprietario}'
    
class Corretor(models.Model):
    nome = models.CharField('Nome', max_length = 50)
    creci = models.IntegerField('Creci')

    def __str__(self):
        return f'{self.nome} {self.creci}'