# Generated by Django 3.0.8 on 2020-11-03 17:56

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('home', '0021_courses'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='allsubjects',
            name='teacher',
        ),
        migrations.RemoveField(
            model_name='allsubjects',
            name='totStudents',
        ),
    ]
