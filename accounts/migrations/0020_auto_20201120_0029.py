# Generated by Django 3.0.8 on 2020-11-19 18:29

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('accounts', '0019_auto_20201118_1346'),
    ]

    operations = [
        migrations.AlterField(
            model_name='student',
            name='points',
            field=models.CharField(default=0, max_length=30),
        ),
        migrations.AlterField(
            model_name='student',
            name='quizAttended',
            field=models.CharField(default=0, max_length=300),
        ),
        migrations.AlterField(
            model_name='student',
            name='successRate',
            field=models.CharField(default=0, max_length=10),
        ),
    ]
