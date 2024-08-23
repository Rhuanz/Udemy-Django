from django.contrib import admin
from .models import Cliente, Imovel, Corretor
# Register your models here.

class ClienteAdmin(admin.ModelAdmin):
    list_display = ('CodigoCliente','nome', 'telefone') #mostrando mais de um item na consulta de clientes

class ImovelAdmin(admin.ModelAdmin):
    list_display = ('CodigoImovel', 'Proprietario')

class CorretorAdmin(admin.ModelAdmin):
    list_display = ('nome', 'creci') #Lembrar de usar o nome definido no parâmetro e não o nome da variável

admin.site.register(Cliente, ClienteAdmin)
admin.site.register(Imovel,)
admin.site.register(Corretor, CorretorAdmin)