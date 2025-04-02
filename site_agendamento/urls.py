from django.urls import path
from site_agendamento import views

urlpatterns = [
    path('', views.salvar_pessoa, name='form'),

    path('servicos/', views.services_view, name='services'),

    path('calendar/<int:service_id>',
         views.calendar_view, name='calendario'),

    path("agendar/<str:service_type>/<int:service_id>/<str:date>/<str:time>/",
         views.payment, name="agendar_horario"),

    path("get_client_data/", views.get_client_data, name="get_client_data"),

    path('sobre/', views.about, name='about'),
    
    path('contact/', views.contact, name='contact'),
]
