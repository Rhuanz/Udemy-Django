# Generated by Django 4.2.8 on 2023-12-22 01:34

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('core', '0005_alter_imovel_midia'),
    ]

    operations = [
        migrations.AlterField(
            model_name='imovel',
            name='midia',
            field=models.ImageField(default='', upload_to='', verbose_name='Fotos'),
        ),
    ]
