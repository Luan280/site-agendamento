from django.urls import path
from site_agendamento import views

urlpatterns = [
    path('', views.salvar_pessoa, name='form'),

    path('servicos/<str:telephone>/', views.services_view, name='services'),

    path('calendar/<str:telephone>/<int:service_id>',
         views.calendar_view, name='home'),

    path("agendar/<str:telephone>/<str:service_type>/<int:service_id>/<str:date>/<str:time>/",
         views.payment, name="agendar_horario"),

    path("get_client_data/", views.get_client_data, name="get_client_data"),
]
