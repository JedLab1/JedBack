# Generated by Django 5.1.3 on 2024-11-18 10:26

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('activities', '0003_alter_student_name'),
    ]

    operations = [
        migrations.AlterField(
            model_name='student',
            name='name',
            field=models.CharField(max_length=100),
        ),
    ]
