from django import template
from site_agendamento.utils.helpers import format_duration, get_values

register = template.Library()


@register.filter
def duration_format(minutes):
    return format_duration(minutes)


@register.filter
def get_total_value(value):
    return f"R$ {value:.2f}"


@register.filter
def get_half_value(value):
    half_value = value // 2
    return f"R$ {half_value:.2f}"