# Generated by Django 3.0.8 on 2020-11-12 12:20

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('home', '0030_auto_20201112_1820'),
    ]

    operations = [
        migrations.AlterField(
            model_name='questions',
            name='quesID',
            field=models.AutoField(primary_key=True, serialize=False),
        ),
    ]
