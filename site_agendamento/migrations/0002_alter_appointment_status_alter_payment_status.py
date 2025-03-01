# Generated by Django 5.1.5 on 2025-02-01 17:44

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('site_agendamento', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='appointment',
            name='status',
            field=models.CharField(choices=[('pendente', 'Pendente'), ('confirmado', 'Confirmado'), ('cancelado', 'Cancelado')], default='pendente', max_length=10),
        ),
        migrations.AlterField(
            model_name='payment',
            name='status',
            field=models.CharField(choices=[('pendente', 'Pendente'), ('aprovado', 'Aprovado'), ('cancelado', 'Cancelado')], default='pendente', max_length=10),
        ),
    ]
