# Generated by Django 3.0.8 on 2020-10-23 08:41

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('accounts', '0002_auto_20201023_1439'),
    ]

    operations = [
        migrations.RenameField(
            model_name='teachers',
            old_name='reasonToAppointAsTeacher',
            new_name='appointment',
        ),
        migrations.RenameField(
            model_name='teachers',
            old_name='department',
            new_name='dept',
        ),
        migrations.RenameField(
            model_name='teachers',
            old_name='hscPassingYear',
            new_name='hscPass',
        ),
        migrations.RenameField(
            model_name='teachers',
            old_name='version1',
            new_name='vers1',
        ),
        migrations.RenameField(
            model_name='teachers',
            old_name='version2',
            new_name='vers2',
        ),
    ]
