from django.shortcuts import get_object_or_404, render, redirect
from .models import User, Calendar, Appointment, Service
from sqlite3 import IntegrityError
from datetime import datetime, date
from django.http import HttpResponse, JsonResponse
from django.contrib import messages
import calendar

# Create your views here.


from django.shortcuts import render, redirect
from django.db import IntegrityError
from .models import User

def salvar_pessoa(request):
    context = {
        'mensagem': None,
        'color': None,
        'title': 'Login'
    }
    
    if request.method == "POST":
        telefone = request.POST.get("phone")
        
        if not telefone:
            context['mensagem'] = 'Por favor, insira um número de telefone.'
            context['color'] = 'red'
            return render(request, 'site_agendamento/login.html', context)
        
        # Verifica se o usuário já existe
        if User.objects.filter(phone=telefone).exists():
            return redirect('services', telefone)
        
        try:
            # Cria um novo usuário
            User.objects.create(phone=telefone)
            return redirect('services', telefone)
        except IntegrityError:
            context['mensagem'] = 'Erro: Número de telefone já cadastrado.'
            context['color'] = 'red'
        except Exception as e:
            context['mensagem'] = f'Erro inesperado: {str(e)}'
            context['color'] = 'red'
    
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
        "title" : "Serviços",
    }

    return render(request, 'site_agendamento/services.html', context)


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
    # 0 = Segunda, 6 = Domingo
    primeiro_dia_semana = date(ano, mes, 1).weekday()

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
        # Passa os espaços vazios para o template
        "empty_slots": list(range(empty_slots)),
        "service_type": service_type,
        "title" : "Agendamento",
    }

    return render(request, "site_agendamento/calendar.html", context)


from django.shortcuts import render, redirect, get_object_or_404
from django.contrib import messages
from datetime import datetime
from .models import User, Service, Calendar, Appointment

def payment(request, telephone, service_type, service_id, date, time):
    # Formata data e horário
    data_obj = datetime.strptime(date, "%Y-%m-%d").date()
    horario_obj = datetime.strptime(time, "%H:%M").time()
    data_formatada = data_obj.strftime("%d/%m/%Y")

    user = get_object_or_404(User, phone=telephone)
    service = Service.objects.filter(id=service_id).first()
    horario_disponivel = Calendar.objects.filter(
        date=data_obj, time=horario_obj, is_available=True
    ).first()

    # Captura a forma de pagamento
    payment_type = request.GET.get("payment_type")
    mensagem = "Por favor, selecione entre Sinal ou Valor Total antes de continuar." if not payment_type else None

    if request.method == "POST" and horario_disponivel:
        nome = request.POST.get("name")
        telefone = request.POST.get("telephone")

        user, created = User.objects.get_or_create(
            phone=telefone, defaults={"name": nome}
        )

        if not created and user.name != nome:
            user.name = nome
            user.save()

        if not service:
            messages.error(request, "Serviço não encontrado.")
            return redirect("calendario")

        # Criar agendamento e marcar horário como indisponível
        Appointment.objects.create(
            user=user, service=service, calendar=horario_disponivel, status="confirmado"
        )
        horario_disponivel.is_available = False
        horario_disponivel.save()

        return redirect("calendario")

    context = {
        "service": service,
        "service_type": service_type,
        "date": data_formatada,
        "time": time,
        "user": user,
        "title": "Pagamento",
        "mensagem": mensagem,
        "payment_type": payment_type,
    }
    return render(request, "site_agendamento/payment.html", context)

def get_client_data(request):
    telephone = request.GET.get("telephone")
    user = User.objects.filter(phone=telephone).first()

    if user:
        return JsonResponse({"name": user.name})

    return JsonResponse({"name": ""})
