# Generated by Django 4.2.8 on 2023-12-20 20:58

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('core', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='Imovel',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('residencial', models.CharField(max_length=50, verbose_name='Residencial')),
                ('endereco', models.CharField(max_length=200, verbose_name='Endereço')),
                ('proprietario', models.CharField(max_length=100, verbose_name='Proprietário')),
                ('telefone', models.CharField(max_length=15, verbose_name='Telefone')),
                ('midia', models.ImageField(upload_to='', verbose_name='Fotos')),
            ],
        ),
        migrations.AlterField(
            model_name='cliente',
            name='contatoInicial',
            field=models.BooleanField(verbose_name='Contato bem sucedido'),
        ),
        migrations.AlterField(
            model_name='cliente',
            name='situacao',
            field=models.BooleanField(verbose_name='Conversando'),
        ),
    ]