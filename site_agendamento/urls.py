from django.urls import path
from site_agendamento import views

urlpatterns = [
    path('', views.salvar_pessoa, name='form'),
    path('servicos/', views.services_view, name='services'),
    path('index/', views.calendar_view, name='home'),
    path("agendar/<str:data>/<str:horario>/", views.agendar_horario, name="agendar_horario"),
]