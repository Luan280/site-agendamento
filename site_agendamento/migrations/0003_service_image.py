# Generated by Django 5.1.5 on 2025-02-03 21:00

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('site_agendamento', '0002_alter_appointment_status_alter_payment_status'),
    ]

    operations = [
        migrations.AddField(
            model_name='service',
            name='image',
            field=models.ImageField(blank=True, upload_to='services/'),
        ),
    ]
