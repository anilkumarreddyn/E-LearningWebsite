# Generated by Django 3.0.8 on 2020-11-07 16:09

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('home', '0022_auto_20201103_2356'),
    ]

    operations = [
        migrations.CreateModel(
            name='CV',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('email', models.CharField(max_length=30)),
                ('img', models.ImageField(upload_to='static/images')),
            ],
        ),
    ]
