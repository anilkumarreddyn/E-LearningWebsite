# Generated by Django 3.0.8 on 2020-10-26 10:23

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('accounts', '0005_auto_20201024_0024'),
    ]

    operations = [
        migrations.AlterField(
            model_name='student',
            name='enrolled',
            field=models.CharField(default=0, max_length=5000),
        ),
    ]
