from django.shortcuts import render, redirect
from .models import User, Calendar, Appointment, Service
from sqlite3 import IntegrityError
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
import json
import requests
from django.conf import settings
from site_agendamento.utils.helpers import (
    format_weekday, get_formatted_date_and_time,
    get_mes_info, get_service_by_id, format_duration
)


def login_view(request):
    context = {"mensagem": None, "color": None, "title": "Login"}

    if request.method == "POST":
        telefone = request.POST.get("phone")

        if not telefone:
            context["mensagem"] = "Por favor, insira um número de telefone."
            context["color"] = "red"
            return render(request, "site_agendamento/login.html", context)

        request.session["telephone"] = telefone

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
    dia_atual, ano, mes_atual, dias_mes, empty_slots = get_mes_info()

    calendario = [
        {
            "dia": dia,
            "horarios": Calendar.objects.filter(
                date=dia, is_available=True
            ).values_list("time", flat=True),
        }
        for dia in dias_mes
    ]

    service = get_service_by_id(service_id)
    service_type = request.GET.get("service_type", None)
    mensagem = (
        "Por favor, selecione entre Aplicação ou Manutenção antes de continuar."
        if not service_type else None
    )

    context = {
        "dia_atual": dia_atual,
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


def payment_view(request, service_type, service_id, date, time):
    data_obj, horario_obj, data_formatada = get_formatted_date_and_time(
        date, time)
    user = request.user
    service = get_service_by_id(service_id)
    horario_disponivel = Calendar.objects.filter(
        date=data_obj, time=horario_obj, is_available=True
    ).first()
    formatted_duration = format_duration(service.duration)
    payment_type = request.GET.get("payment_type")
    mensagem = (
        "Por favor, selecione entre Sinal ou Valor Total antes de continuar."
        if not payment_type else None
    )

    if request.method == "POST" and horario_disponivel:
        nome = request.POST.get("name")
        if user.name != nome:
            user.name = nome
            user.save()

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
        "title": "Pagamento",
        "mensagem": mensagem,
        "payment_type": payment_type,
        "name_week": format_weekday(data_obj),
        "formatted_duration": formatted_duration,
    }
    return render(request, "site_agendamento/payment.html", context)


@csrf_exempt
def process_payment(request):
    if request.method == "POST":
        data = json.loads(request.body)

        headers = {
            "Authorization": f"Bearer {settings.MERCADO_PAGO_ACCESS_TOKEN}",
            "Content-Type": "application/json"
        }

        response = requests.post(
            "https://api.mercadopago.com/v1/payments",
            headers=headers,
            json=data
        )

        return JsonResponse(response.json())


def get_client_data(request):
    return JsonResponse({"name": request.user.name if request.user else ""})


def about_view(request):
    context = {"title": "Sobre"}
    return render(request, "site_agendamento/about.html", context=context)


def appoinments_view(request):
    return render(request, "site_agendamento/appoinments.html")
