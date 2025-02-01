from django.shortcuts import render, redirect
from .models import User, Calendar
from sqlite3 import IntegrityError
from django.urls import reverse
from django.utils import timezone
from django.http import JsonResponse
import calendar
from django.utils.timezone import datetime


# Create your views here.
def calendar_view(request):
    # Obtém o mês e ano atuais
    now = timezone.now()
    ano = now.year
    mes = now.month
    meses= ["Janeiro", "Fevereiro", "Março", "Abril", "Maio", "Junho", "Julho", "Agosto", "Setembro", "Outubro", "Novembro", "Dezembro"]
    mes_atual = meses[mes -1]
    # Obtém o primeiro e último dia do mês
    _, ultimo_dia = calendar.monthrange(ano, mes)
    
    # Cria uma lista com todos os dias do mês
    dias_do_mes = [
        {
            "dia": dia,
            "data": f"{ano}-{mes:02d}-{dia:02d}",
        }
        for dia in range(1, ultimo_dia + 1)
    ]
    return render(request, 'site_agendamento/index.html', {"dias_do_mes": dias_do_mes, 'mes':mes_atual})


def salvar_pessoa(request):
    mensagem = None
    color = None
    if request.method == "POST":
        phone = request.POST.get("phone")
        user = User.objects.filter(phone=phone)
        if user:
            return redirect(reverse('home') + f'?phone={phone}')
        try:
            # Salvar no banco de dados
            User.objects.create(phone=phone)
            mensagem = 'Cadastro realizado com sucesso'
            color = 'green'
            return redirect(reverse('home') + f'?phone={phone}')
        except IntegrityError as Error_IntegrityError:
            mensagem = f'Error: {Error_IntegrityError}'
            color = 'red'
        except Exception as Error:
            mensagem = f'Error inesperado: {Error}'
            color = 'red'
    return render(request, 'site_agendamento/login.html', context={'mensagem': mensagem, 'color': color})



def horarios_disponiveis(request, data):
    """
    Retorna os horários disponíveis para uma determinada data.
    """
    try:
        # Converte a string da URL para um formato de data válido
        data_formatada = datetime.strptime(data, "%Y-%m-%d").date()

        # Filtrar horários disponíveis para essa data
        horarios = Calendar.objects.filter(date=data_formatada, is_available=True).values_list("time", flat=True)

        return JsonResponse({"horarios": list(horarios)})
    
    except ValueError:
        return JsonResponse({"error": "Formato de data inválido. Use YYYY-MM-DD."}, status=400)

def filtrar_por_mes(request, ano, mes):
    """
    Filtra e retorna os dias disponíveis de um determinado mês.
    """
    try:
        # Filtrar todos os dias disponíveis no mês
        dias_disponiveis = Calendar.objects.filter(date__year=ano, date__month=mes).values_list("date", flat=True).distinct()

        return JsonResponse({"dias_disponiveis": list(dias_disponiveis)})
    
    except ValueError:
        return JsonResponse({"error": "Formato inválido de ano/mês."}, status=400)
