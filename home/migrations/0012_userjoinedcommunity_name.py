# Generated by Django 5.0.1 on 2024-01-29 04:17

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('home', '0011_userimages'),
    ]

    operations = [
        migrations.AddField(
            model_name='userjoinedcommunity',
            name='name',
            field=models.CharField(default='defaul Com. Name', max_length=50),
        ),
    ]
