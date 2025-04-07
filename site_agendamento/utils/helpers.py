from datetime import datetime, date
import calendar
from django.shortcuts import get_object_or_404
from site_agendamento.models import Service


def format_weekday(data_obj):
    week = [
        "segunda-feira", "terça-feira", "quarta-feira",
        "quinta-feira", "sexta-feira", "sábado", "domingo"
    ]
    return week[data_obj.weekday()]


def get_formatted_date_and_time(date_str, time_str):
    data_obj = datetime.strptime(date_str, "%Y-%m-%d").date()
    horario_obj = datetime.strptime(time_str, "%H:%M").time()
    data_formatada = data_obj.strftime("%d/%m/%Y")
    return data_obj, horario_obj, data_formatada


def get_mes_info():
    dia_atual = datetime.today()
    ano, mes = dia_atual.year, dia_atual.month
    meses = [
        "Janeiro", "Fevereiro", "Março", "Abril", "Maio", "Junho",
        "Julho", "Agosto", "Setembro", "Outubro", "Novembro", "Dezembro",
    ]
    mes_atual = meses[mes - 1]
    total_dias_mes = calendar.monthrange(ano, mes)[1]
    primeiro_dia_semana = date(ano, mes, 1).weekday()
    empty_slots = (primeiro_dia_semana + 1) % 7
    dias_mes = [date(ano, mes, dia) for dia in range(1, total_dias_mes + 1)]
    return dia_atual, ano, mes_atual, dias_mes, empty_slots


def get_service_by_id(service_id):
    return get_object_or_404(Service, id=service_id)

def format_duration(minutos):
    time = minutos // 60
    rest = minutos % 60
    _time = time // 2
    if time and rest:
        return f"{time} H {rest} min"
    elif time:
        return f"{_time} | {time} hrs"
    else:
        return f"{rest} min"
    
def get_values(value):
    total_value = value
    half_value = value // 2
    return total_value, half_value