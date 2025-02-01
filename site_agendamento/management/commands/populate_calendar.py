from django.utils.timezone import make_aware
from datetime import datetime, timedelta
import pytz
from site_agendamento.models import Calendar  # Substitua 'myapp' pelo nome do seu app

# Definir o fuso horário do Brasil
br_tz = pytz.timezone("America/Sao_Paulo")

# Criar registros para todos os dias do ano atual
ano_atual = datetime.now().year
data_inicio = datetime(ano_atual, 1, 1, tzinfo=br_tz)
data_fim = datetime(ano_atual, 12, 31, tzinfo=br_tz)

# Criar horários das 10h às 23h
horarios = [make_aware(datetime(ano_atual, 1, 1, hora, 0), br_tz).time() for hora in range(10, 24)]

# Loop por cada dia do ano
data_atual = data_inicio
while data_atual <= data_fim:
    for horario in horarios:
        Calendar.objects.get_or_create(date=data_atual.date(), time=horario)
    data_atual += timedelta(days=1)

print("Calendário criado com sucesso!")
