# Generated by Django 3.0.8 on 2020-11-20 11:46

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('accounts', '0021_auto_20201120_1202'),
    ]

    operations = [
        migrations.AddField(
            model_name='teachersapplied',
            name='classLink',
            field=models.CharField(default='', max_length=5000),
        ),
    ]