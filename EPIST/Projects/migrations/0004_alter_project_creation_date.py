# Generated by Django 4.2.4 on 2023-08-13 00:27

import datetime
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('Projects', '0003_alter_project_state'),
    ]

    operations = [
        migrations.AlterField(
            model_name='project',
            name='creation_date',
            field=models.DateField(default=datetime.date(2023, 8, 12)),
        ),
    ]