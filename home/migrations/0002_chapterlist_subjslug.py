# Generated by Django 3.0.8 on 2020-10-21 19:34

import datetime
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('home', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='chapterlist',
            name='subjSlug',
            field=models.CharField(default=datetime.datetime(2020, 10, 22, 1, 34, 35, 418370), max_length=30),
            preserve_default=False,
        ),
    ]
