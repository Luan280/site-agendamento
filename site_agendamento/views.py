from django.shortcuts import render, redirect
from .models import User, Calendar, Appointment, Service
from sqlite3 import IntegrityError
from django.urls import reverse
from datetime import datetime
import calendar

# Create your views here.
def services_view(request):
    services = Service.objects.all()
    return render(request, 'site_agendamento/services.html', {'services': services})

def calendar_view(request):
    """
    Exibe um calendário com todos os dias do mês atual.
    Ao clicar em um dia, mostra os horários disponíveis.
    """
    hoje = datetime.today()
    ano, mes = hoje.year, hoje.month
    meses= ["Janeiro", "Fevereiro", "Março", "Abril", "Maio", "Junho", "Julho", "Agosto", "Setembro", "Outubro", "Novembro", "Dezembro"]
    # Pega o "nome" do mes, de acordo com o número do mes.['0': 'Janeiro', '1': 'Fevereiro']
    mes_atual = meses[mes -1]
    # Quantidade de dias do mês.
    total_dias_mes = calendar.monthrange(ano, mes)[1]
    dias_mes = [datetime(ano, mes, dia).date() for dia in range(1, total_dias_mes + 1)]
    calendario = []
    # Obter os horários disponíveis para cada dia do mês
    for dia in dias_mes:
        horarios_disponiveis = Calendar.objects.filter(date=dia, is_available=True).values_list("time", flat=True)
        calendario.append({"dia": dia, "horarios": horarios_disponiveis})
    

    return render(request, 'site_agendamento/index.html', {"calendario": calendario, "mes": mes_atual, "ano": ano})


def agendar_horario(request, data, horario):
    """
    Permite que um cliente selecione um horário disponível e agende um serviço.
    """
    data_obj = datetime.strptime(data, "%Y-%m-%d").date()
    horario_obj = datetime.strptime(horario, "%H:%M").time()

    # Verifica se o horário ainda está disponível
    horario_disponivel = Calendar.objects.filter(date=data_obj, time=horario_obj, is_available=True).first()

    if horario_disponivel:
        if request.method == "POST":
            user = User.objects.first()  # Troque por autenticação real
            service = Service.objects.first()  # Exemplo: pegar o primeiro serviço disponível

            # Criar agendamento
            agendamento = Appointment.objects.create(
                user=user, service=service, calendar=horario_disponivel, status="confirmado"
            )

            # Atualizar horário como indisponível
            horario_disponivel.is_available = False
            horario_disponivel.save()

            return redirect("calendario")

    return render(request, "erro.html", {"mensagem": "Horário indisponível."})


def salvar_pessoa(request):
    mensagem = None
    color = None
    if request.method == "POST":
        phone = request.POST.get("phone")
        user = User.objects.filter(phone=phone)
        if user:
            return redirect(reverse('services') + f'?phone={phone}')
        try:
            # Salvar no banco de dados
            User.objects.create(phone=phone)
            mensagem = 'Cadastro realizado com sucesso'
            color = 'green'
            return redirect(reverse('service') + f'?phone={phone}')
        except IntegrityError as Error_IntegrityError:
            mensagem = f'Error: {Error_IntegrityError}'
            color = 'red'
        except Exception as Error:
            mensagem = f'Error inesperado: {Error}'
            color = 'red'
    return render(request, 'site_agendamento/login.html', context={'mensagem': mensagem, 'color': color})

