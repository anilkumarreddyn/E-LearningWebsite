# Generated by Django 3.0.8 on 2020-10-26 19:44

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('home', '0015_replies'),
    ]

    operations = [
        migrations.CreateModel(
            name='Reports',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=50)),
                ('against', models.CharField(max_length=50)),
                ('topic', models.CharField(max_length=150)),
                ('desc', models.CharField(max_length=1000)),
            ],
        ),
    ]
