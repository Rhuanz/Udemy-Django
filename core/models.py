from django.db import models

from core.views import corretores

# Create your models here.

#Estudar herança para melhorar as classes cliente, corretor e proprietário
class Corretor(models.Model):
    nome = models.CharField('Nome', max_length = 50)
    creci = models.CharField('Creci', max_length= 7, primary_key=True, unique=True)

    def __str__(self):
        return f'{self.nome} {self.creci}'
    
    def get_creci(self):
        return self.creci

class Cliente(models.Model):
    
    cod = models.AutoField(name='CodigoCliente', primary_key=True, default=0)
    nome = models.CharField('Nome', max_length=50)
    telefone = models.CharField('Telefone', max_length=15)
    corretor = models.ForeignKey(Corretor, on_delete=models.CASCADE)

    def __str__(self):
        return self.nome #mostra o nome do produto na lista

class Imovel (models.Model):

    cod = models.AutoField(name='CodigoImovel', primary_key=True, default=0)
    endereco = models.CharField('Endereço', max_length=200)
    proprietario = models.CharField('Proprietario', max_length=100)
    telefone = models.CharField('Telefone', max_length=15)
    corretor = models.ForeignKey(Corretor, on_delete=models.CASCADE) #Verificar como colcoar uma objeto aqui

    def __str__(self):
        return f'{self.cod} {self.proprietario}'
    
