from django.contrib import admin
from .models import Cliente, Imovel, Corretor
# Register your models here.

class ClienteAdmin(admin.ModelAdmin):
    list_display = ('nome', 'telefone', 'situacao') #mostrando mais de um item na consulta de clientes

class ImovelAdmin(admin.ModelAdmin):
    list_display = ('residencial', )
class CorretorAdmin(admin.ModelAdmin):
    list_display = ('nome', 'creci')

admin.site.register(Cliente, ClienteAdmin)
admin.site.register(Imovel)
admin.site.register(Corretor, CorretorAdmin)