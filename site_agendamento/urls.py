from django.urls import path
from site_agendamento import views

urlpatterns = [
    path('', views.salvar_pessoa, name='form'),
    path('index/', views.calendar_view, name='home'),
    path("horarios_disponiveis/<str:data>/", views.horarios_disponiveis, name="horarios_disponiveis"),
    path("dias_disponiveis/<int:ano>/<int:mes>/", views.filtrar_por_mes, name="filtrar_por_mes"),
]