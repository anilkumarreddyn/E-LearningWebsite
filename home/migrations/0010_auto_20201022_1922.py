# Generated by Django 3.0.8 on 2020-10-22 13:22

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('home', '0009_auto_20201022_1842'),
    ]

    operations = [
        migrations.AlterField(
            model_name='allcontent',
            name='desc',
            field=models.CharField(max_length=300),
        ),
    ]