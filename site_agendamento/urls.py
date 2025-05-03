from django.urls import path
from site_agendamento import views

urlpatterns = [
    path('', views.login_view, name='form'),

    path('servicos/', views.services_view, name='services'),

    path('calendar/<int:service_id>',
         views.calendar_view, name='calendario'),

    path("agendar/<str:service_type>/<int:service_id>/<str:date>/<str:time>/",
         views.payment_view, name="agendar_horario"),

    path("get_client_data/", views.get_client_data, name="get_client_data"),

    path('sobre/', views.about_view, name='about'),

    path('agendamentos/', views.appoinments_view, name='appoinments'),

    path("process_payment/", views.process_payment, name="process_payment"),  # type: ignore

]
