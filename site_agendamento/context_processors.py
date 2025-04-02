from .models import User

def global_variables(request):
    telephone = request.GET.get("telephone") or request.session.get("telephone")
    
    user = None
    if telephone:
        user = User.objects.filter(phone=telephone).first()
        request.session["telephone"] = telephone  # Salva na sessão

    return {
        "telephone": telephone,
        "user": user,
    }
