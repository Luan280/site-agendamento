from .models import User
from django.conf import settings


def mercado_pago_keys(request):
    return {
        'MERCADO_PAGO_PUBLIC_KEY': settings.MERCADO_PAGO_PUBLIC_KEY
    }


def global_variables(request):
    telephone = request.GET.get(
        "telephone") or request.session.get("telephone")

    user = None
    if telephone:
        user = User.objects.filter(phone=telephone).first()
        request.session["telephone"] = telephone  # Salva na sessão

    return {
        "telephone": telephone,
        "user": user,
    }
