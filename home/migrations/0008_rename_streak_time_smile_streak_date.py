# Generated by Django 5.0.1 on 2024-01-27 17:18

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('home', '0007_level_points'),
    ]

    operations = [
        migrations.RenameField(
            model_name='smile',
            old_name='streak_time',
            new_name='streak_date',
        ),
    ]
