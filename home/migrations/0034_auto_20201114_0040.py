# Generated by Django 3.0.8 on 2020-11-13 18:40

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('home', '0033_quizchapterlist'),
    ]

    operations = [
        migrations.AlterField(
            model_name='questionbank',
            name='options',
            field=models.CharField(max_length=3324530),
        ),
    ]
