# Generated by Django 4.2.4 on 2023-09-02 23:19

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('Users', '0002_alter_user_ident_number'),
    ]

    operations = [
        migrations.AlterField(
            model_name='user',
            name='ident_number',
            field=models.CharField(max_length=50, unique=True, verbose_name='Número de Identificación'),
        ),
    ]
