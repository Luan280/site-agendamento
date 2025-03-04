from django.shortcuts import get_object_or_404, render, redirect
from .models import User, Calendar, Appointment, Service
from sqlite3 import IntegrityError
from datetime import datetime
from django.http import HttpResponse
import calendar

# Create your views here.


def salvar_pessoa(request):
    mensagem = None
    color = None
    if request.method == "POST":
        telephone = request.POST.get("phone")
        user = User.objects.filter(phone=telephone)
        if user:
            return redirect('services', telephone)
        try:
            # Salvar no banco de dados
            User.objects.create(phone=telephone)
            mensagem = 'Cadastro realizado com sucesso'
            color = 'green'
            return redirect('services', telephone)
        except IntegrityError as Error_IntegrityError:
            mensagem = f'Error: {Error_IntegrityError}'
            color = 'red'
        except Exception as Error:
            mensagem = f'Error inesperado: {Error}'
            color = 'red'
    context = {'mensagem': mensagem, 'color': color}
    return render(request, 'site_agendamento/login.html', context)


def services_view(request, telephone):
    services = Service.objects.all()
    categories = Service.CATEGORY_CHOICES  # Pegando as categorias do modelo
    user = User.objects.get(phone=telephone)
    
    category_filter = request.GET.get('category')  # Obtendo o filtro da URL
    if category_filter:
        services = services.filter(category=category_filter)

    context = {
        'telephone': telephone,
        'services': services,
        'categories': categories,
        'user': user.__dict__,
        'category_filter': category_filter,
    }
    
    return render(request, 'site_agendamento/services.html', context)


import calendar
from datetime import datetime, date
from django.shortcuts import render
from .models import Calendar, Service

def calendar_view(request, telephone, service_id):
    """
    Exibe um calendário com todos os dias do mês atual.
    Ao clicar em um dia, mostra os horários disponíveis.
    """
    hoje = datetime.today()
    ano, mes = hoje.year, hoje.month

    # Nome dos meses
    meses = [
        "Janeiro", "Fevereiro", "Março", "Abril", "Maio", "Junho",
        "Julho", "Agosto", "Setembro", "Outubro", "Novembro", "Dezembro"
    ]
    mes_atual = meses[mes - 1]  # Obtém o nome do mês atual

    # Quantidade de dias do mês e dia da semana do primeiro dia
    total_dias_mes = calendar.monthrange(ano, mes)[1]
    primeiro_dia_semana = date(ano, mes, 1).weekday()  # 0 = Segunda, 6 = Domingo

    # Ajustando para que Domingo seja 0 e Segunda seja 1
    empty_slots = (primeiro_dia_semana + 1) % 7  

    # Criando lista de dias do mês
    dias_mes = [date(ano, mes, dia) for dia in range(1, total_dias_mes + 1)]
    calendario = []

    # Obtendo horários disponíveis para cada dia do mês
    for dia in dias_mes:
        horarios_disponiveis = Calendar.objects.filter(
            date=dia, is_available=True
        ).values_list("time", flat=True)

        calendario.append({"dia": dia, "horarios": horarios_disponiveis})

    service = Service.objects.get(id=service_id)

    # Captura o tipo de serviço escolhido pelo cliente
    service_type = request.GET.get("service_type", None)

    # Exibe mensagem se o cliente ainda não escolheu o tipo de serviço
    mensagem = None
    if not service_type:
        mensagem = "Por favor, selecione entre Aplicação ou Manutenção antes de continuar."

    context = {
        "mensagem": mensagem,
        "telephone": telephone,
        "service": service,
        "calendario": calendario,
        "mes": mes_atual,
        "ano": ano,
        "empty_slots": list(range(empty_slots)),  # Passa os espaços vazios para o template
        "service_type": service_type,
    }

    return render(request, "site_agendamento/index.html", context)



def agendar_horario(request, telephone, service_id):
    service = get_object_or_404(Service, id=service_id)

    if request.method == 'POST':
        service_type = request.POST.get('service_type')
        date = request.POST.get('date')
        time = request.POST.get('time')

        if service_type and date and time:
            # Cria o agendamento
            Appointment.objects.create(
                service=service,
                client=telephone,
                date=date,
                time=time,
                service_type=service_type,
            )
            return HttpResponse("Agendamento realizado com sucesso!")
        else:
            return HttpResponse("Preencha todos os campos corretamente!")

    # Renderiza a página
    return render(request, 'site_agendamento/payment.html', {'service': service})


def about_view(request):
    return render(request, "site_agendamento/about.html")
