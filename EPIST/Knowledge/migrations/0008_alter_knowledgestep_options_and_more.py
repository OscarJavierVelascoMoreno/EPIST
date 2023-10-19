# Generated by Django 4.2.4 on 2023-10-19 19:24

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('Knowledge', '0007_alter_knowledge_options_alter_knowledgetype_options_and_more'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='knowledgestep',
            options={'verbose_name': 'Pasos de Conocimiento'},
        ),
        migrations.AlterField(
            model_name='knowledgestep',
            name='image',
            field=models.ImageField(null=True, upload_to='Users/static/uploads/KnowledgeSteps/', verbose_name='Imagen'),
        ),
        migrations.AlterField(
            model_name='knowledgetype',
            name='description',
            field=models.TextField(verbose_name='Descripción'),
        ),
        migrations.AlterField(
            model_name='knowledgetype',
            name='title',
            field=models.CharField(max_length=100, unique=True, verbose_name='Título'),
        ),
    ]
