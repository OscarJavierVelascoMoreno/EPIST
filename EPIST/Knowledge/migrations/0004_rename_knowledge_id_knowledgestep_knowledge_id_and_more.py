# Generated by Django 4.2.4 on 2023-08-13 01:30

import datetime
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('Knowledge', '0003_knowledge_project_id'),
    ]

    operations = [
        migrations.RenameField(
            model_name='knowledgestep',
            old_name='Knowledge_id',
            new_name='knowledge_id',
        ),
        migrations.AddField(
            model_name='knowledgestep',
            name='creation_date',
            field=models.DateField(default=datetime.date(2023, 8, 12)),
        ),
    ]
