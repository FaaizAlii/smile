# Generated by Django 5.0.1 on 2024-01-26 06:55

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('base', '0003_alter_profile_children_and_more'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='profile_step3',
            options={'verbose_name_plural': 'profile3'},
        ),
        migrations.AddField(
            model_name='profile',
            name='image',
            field=models.ImageField(blank=True, null=True, upload_to='images/'),
        ),
    ]
