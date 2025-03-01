from django.db import models
from django.utils import timezone


class User(models.Model):
    name = models.CharField(max_length=50, blank=True)
    phone = models.CharField(max_length=15, unique=True)
    created_at = models.DateTimeField(default=timezone.now)

    def __str__(self):
        return self.phone


class Service(models.Model):
    CATEGORY_CHOICES = [
        ('cilios', 'Cílios'),
        ('unha', 'Unha'),
        ('limpeza_pele', 'Limpeza de Pele'),
        ('sobrancelha', 'Sobrancelha'),
    ]
    name = models.CharField(max_length=255)
    image = models.ImageField(upload_to='services/', blank=True)
    description = models.TextField(blank=True, null=True)
    application = models.DecimalField(max_digits=10, decimal_places=2)
    maintenance = models.DecimalField(max_digits=10, decimal_places=2, blank=True, null=True)
    duration = models.IntegerField(help_text="Duração em minutos")
    category = models.CharField(max_length=20, choices=CATEGORY_CHOICES)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.name


class Calendar(models.Model):
    """
    Modelo de calendário que armazena todos os dias e horários de um ano, 
    permitindo filtragem por mês e dia.
    """
    date = models.DateField()  # Guarda o dia do calendário (ex: 2025-02-01)
    time = models.TimeField()  # Guarda o horário disponível (ex: 10:00, 11:00)
    # Define se o horário está disponível
    is_available = models.BooleanField(default=True)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        # Garante que não haja horários duplicados para o mesmo dia
        unique_together = ('date', 'time')

    def __str__(self):
        return f"{self.date.strftime('%d/%m/%Y')} - {self.time.strftime('%H:%M')}"


class Appointment(models.Model):
    STATUS_CHOICES = [
        ('pendente', 'Pendente'),
        ('confirmado', 'Confirmado'),
        ('cancelado', 'Cancelado'),
    ]
    TYPE_CHOICES = [
        ('aplicação', 'Aplicação'),
        ('manutenção', 'Manutenção'),
    ]

    user = models.ForeignKey(User, on_delete=models.CASCADE)
    service = models.ForeignKey(Service, on_delete=models.CASCADE)
    calendar = models.OneToOneField(Calendar, on_delete=models.CASCADE)
    status = models.CharField(max_length=10, choices=STATUS_CHOICES, default='pendente')
    type_service = models.CharField(max_length=10, choices=TYPE_CHOICES, default='aplicação')
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def save(self, *args, **kwargs):
        """ Atualiza a disponibilidade do horário no calendário ao confirmar um agendamento."""
        if self.status == 'confirmado':
            self.calendar.is_available = False
            self.calendar.save()
        elif self.status == 'cancelado':
            self.calendar.is_available = True
            self.calendar.save()
        super().save(*args, **kwargs)

    def __str__(self):
        return f"Agendamento de {self.user} para {self.service} em {self.calendar}"


class Payment(models.Model):
    PAYMENT_METHODS = [
        ('cartao', 'Cartão de Crédito/Débito'),
        ('pix', 'Pix'),
    ]

    STATUS_CHOICES = [
        ('pendente', 'Pendente'),
        ('aprovado', 'Aprovado'),
        ('cancelado', 'Cancelado'),
    ]

    appointment = models.OneToOneField(Appointment, on_delete=models.CASCADE)
    amount = models.DecimalField(max_digits=10, decimal_places=2)
    payment_method = models.CharField(max_length=10, choices=PAYMENT_METHODS)
    status = models.CharField(
        max_length=10, choices=STATUS_CHOICES, default='pendente')
    transaction_id = models.CharField(max_length=255, blank=True, null=True)
    paid_at = models.DateTimeField(blank=True, null=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def save(self, *args, **kwargs):
        """ Define a data de pagamento ao aprovar o pagamento. """
        if self.status == 'aprovado' and not self.paid_at:
            self.paid_at = timezone.now()
        super().save(*args, **kwargs)

    def __str__(self):
        return f"Pagamento de {self.amount} para {self.appointment}"
