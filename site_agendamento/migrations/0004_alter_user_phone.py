# Generated by Django 5.1.5 on 2025-02-04 22:23

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('site_agendamento', '0003_service_image'),
    ]

    operations = [
        migrations.AlterField(
            model_name='user',
            name='phone',
            field=models.CharField(max_length=15, unique=True),
        ),
    ]
