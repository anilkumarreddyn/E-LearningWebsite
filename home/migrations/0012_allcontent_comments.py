# Generated by Django 3.0.8 on 2020-10-24 10:34

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('home', '0011_noticeboard'),
    ]

    operations = [
        migrations.AddField(
            model_name='allcontent',
            name='comments',
            field=models.CharField(default='', max_length=99999999999999),
        ),
    ]
