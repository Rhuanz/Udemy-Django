from django.urls import path
from .views import IndexView, imoveis, corretores, corretor, cliente, clientes, imovel, cadastroimovel, cadastrocorretor, cadastrocliente, atualizarcorretor, deletarcorretor
from .views import cadastroendereco, cadastroproprietario, atualizarimovel, cadastrovisita
urlpatterns = [
    path('', IndexView.as_view(), name = 'index'),
    path('imoveis/', imoveis, name = 'imoveis'),
    path('imoveis/cadastro', cadastroimovel, name='cadastroimovel'),
    path('imoveis/cadastro/endereco', cadastroendereco, name='cadastroendereco'),
    path('imoveis/cadastro/proprietario', cadastroproprietario, name='cadastroproprietario'),
    path('imovel/<int:codImovel>', imovel, name='imovel'), #não pode usar o mesmo nome da coluna referente ao parâmetro (Case sensitive)
    path('imovel/atualizarimovel', atualizarimovel, name='atualizarimovel'),
    path('corretores/', corretores, name = 'corretores'),
    path('corretor/<int:nCreci>', corretor, name = 'corretor'),
    path('corretor/cadastro', cadastrocorretor, name='cadastrocorretor'),
    path('corretor/atualizarcorretor', atualizarcorretor, name='atualizarcorretor'),
    path('corretor/deletarcorretor', deletarcorretor, name='deletarcorretor'),
    path('clientes/', clientes, name='clientes'),
    path('cliente/<int:codCliente>', cliente, name='cliente'),
    path('cliente/Cadastro', cadastrocliente, name='cadastrocliente'),
    path('cliente/<int:codCliente>/cadastrovisita', cadastrovisita, name='cadastrovisita'),
]