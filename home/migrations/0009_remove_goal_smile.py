# Generated by Django 5.0.1 on 2024-01-28 18:26

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('home', '0008_rename_streak_time_smile_streak_date'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='goal',
            name='smile',
        ),
    ]
