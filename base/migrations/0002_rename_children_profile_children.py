# Generated by Django 5.0.1 on 2024-01-25 06:16

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('base', '0001_initial'),
    ]

    operations = [
        migrations.RenameField(
            model_name='profile',
            old_name='Children',
            new_name='children',
        ),
    ]
