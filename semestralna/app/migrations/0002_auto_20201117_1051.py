# Generated by Django 3.1.2 on 2020-11-17 09:51

import datetime
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('app', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='discussion',
            name='date',
            field=models.DateTimeField(default=datetime.datetime(2020, 11, 17, 10, 51, 44, 838034)),
        ),
    ]
