from django.contrib import admin
from .models import Cliente, Imovel, Corretor, Proprietario, Venda, Acompanhamento, Visita, Endereco, Intermedio
# Register your models here.

class ClienteAdmin(admin.ModelAdmin):
    list_display = ('CodCliente','Nome', 'Telefone') #mostrando mais de um item na consulta de clientes da página admin

class ImovelAdmin(admin.ModelAdmin):
    list_display = ('CodImovel', 'TipoImovel', 'ValorImovel') #Lembrar de usar o nome definido no parâmetro e não o nome da variável

@admin.register(Corretor)
class CorretorAdmin(admin.ModelAdmin):
    list_display = ('Nome', 'Creci', 'Ativo') 

class ProprietarioAdmin(admin.ModelAdmin):
    list_display = ('Nome', 'Telefone')

class EnderecoAdmin(admin.ModelAdmin):
    list_display = ('CodEndereco', 'Bairro', 'Cidade', 'Rua', 'Numero')

class VisitaAdmin(admin.ModelAdmin):
    list_display = ('CodVisita', 'Cliente', 'Imovel', 'DataVisita')

class AcompanhamentoAdmin(admin.ModelAdmin):
    list_display = ('Visita', 'Corretor')


admin.site.register(Cliente, ClienteAdmin)
admin.site.register(Imovel, ImovelAdmin)
#admin.site.register(Corretor, CorretorAdmin)
admin.site.register(Proprietario, ProprietarioAdmin)
admin.site.register(Venda)
admin.site.register(Acompanhamento)
admin.site.register(Visita)
admin.site.register(Endereco, EnderecoAdmin)
admin.site.register(Intermedio)