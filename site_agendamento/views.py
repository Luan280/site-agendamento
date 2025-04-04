from django.shortcuts import get_object_or_404, render, redirect
from .models import User, Calendar, Appointment, Service
from sqlite3 import IntegrityError
from datetime import datetime, date
from django.http import JsonResponse
from django.contrib import messages
import calendar


def salvar_pessoa(request):
    context = {"mensagem": None, "color": None, "title": "Login"}

    if request.method == "POST":
        telefone = request.POST.get("phone")

        if not telefone:
            context["mensagem"] = "Por favor, insira um número de telefone."
            context["color"] = "red"
            return render(request, "site_agendamento/login.html", context)

        # Salva o telefone na sessão
        request.session["telephone"] = telefone

        # Verifica se o usuário já existe
        if not User.objects.filter(phone=telefone).exists():
            try:
                User.objects.create(phone=telefone)
            except IntegrityError:
                context["mensagem"] = "Erro: Número de telefone já cadastrado."
                context["color"] = "red"
                return render(request, "site_agendamento/login.html", context)

        return redirect("services")

    return render(request, "site_agendamento/login.html", context)


def services_view(request):
    services = Service.objects.all()
    categories = dict(Service.CATEGORY_CHOICES)

    user = request.user  # O context processor já fornece o usuário

    category_filter = request.GET.get("category")
    if category_filter and category_filter in categories:
        services = services.filter(category=category_filter)

    context = {
        "services": services,
        "categories": categories,
        "category_filter": category_filter,
        "title": "Serviços",
    }

    return render(request, "site_agendamento/services.html", context)


def calendar_view(request, service_id):
    hoje = datetime.today()
    ano, mes = hoje.year, hoje.month
    meses = [
        "Janeiro", "Fevereiro", "Março", "Abril", "Maio", "Junho",
        "Julho", "Agosto", "Setembro", "Outubro", "Novembro", "Dezembro",
    ]
    mes_atual = meses[mes - 1]
    total_dias_mes = calendar.monthrange(ano, mes)[1]
    primeiro_dia_semana = date(ano, mes, 1).weekday()
    empty_slots = (primeiro_dia_semana + 1) % 7
    dias_mes = [date(ano, mes, dia) for dia in range(1, total_dias_mes + 1)]

    calendario = [
        {"dia": dia, "horarios": Calendar.objects.filter(
            date=dia, is_available=True).values_list("time", flat=True)}
        for dia in dias_mes
    ]

    service = get_object_or_404(Service, id=service_id)
    service_type = request.GET.get("service_type", None)
    mensagem = "Por favor, selecione entre Aplicação ou Manutenção antes de continuar." if not service_type else None

    context = {
        "mensagem": mensagem,
        "service": service,
        "calendario": calendario,
        "mes": mes_atual,
        "ano": ano,
        "empty_slots": list(range(empty_slots)),
        "service_type": service_type,
        "title": "Agendamento",
    }

    return render(request, "site_agendamento/calendar.html", context)


def payment(request, service_type, service_id, date, time):
    data_obj = datetime.strptime(date, "%Y-%m-%d").date()
    horario_obj = datetime.strptime(time, "%H:%M").time()
    data_formatada = data_obj.strftime("%d/%m/%Y")

    user = request.user
    service = get_object_or_404(Service, id=service_id)
    horario_disponivel = Calendar.objects.filter(
        date=data_obj, time=horario_obj, is_available=True).first()

    payment_type = request.GET.get("payment_type")
    mensagem = "Por favor, selecione entre Sinal ou Valor Total antes de continuar." if not payment_type else None

    if request.method == "POST" and horario_disponivel:
        nome = request.POST.get("name")

        if user.name != nome:
            user.name = nome
            user.save()

        Appointment.objects.create(
            user=user, service=service, calendar=horario_disponivel, status="confirmado")
        horario_disponivel.is_available = False
        horario_disponivel.save()

        return redirect("calendario")

    context = {
        "service": service,
        "service_type": service_type,
        "date": data_formatada,
        "time": time,
        "title": "Pagamento",
        "mensagem": mensagem,
        "payment_type": payment_type,
    }
    return render(request, "site_agendamento/payment.html", context)


def get_client_data(request):
    return JsonResponse({"name": request.user.name if request.user else ""})


def about(request):
    context = {
        "title": "Sobre"
    }
    return render(request, "site_agendamento/about.html", context=context)


def appoinments(request):
    
    return render(request, "site_agendamento/appoinments.html")
