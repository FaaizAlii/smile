# Generated by Django 5.0.1 on 2024-01-28 19:40

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('home', '0009_remove_goal_smile'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='activity',
            name='completed',
        ),
        migrations.RemoveField(
            model_name='activity',
            name='user',
        ),
    ]