# Generated by Django 5.1.3 on 2024-11-18 11:04

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('activities', '0006_alter_level_name'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='studentdifficulty',
            name='method',
        ),
    ]