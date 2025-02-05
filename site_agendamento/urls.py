from django.urls import path
from site_agendamento import views

urlpatterns = [
    path('index/<str:telephone>/<int:service_id>', views.calendar_view, name='home'),
    path('', views.salvar_pessoa, name='form'),
    path('servicos/<str:telephone>/', views.services_view, name='services'),
    path('servicos/detail/<int:service_id>/', views.service_detail, name='service_detail'),
    path("agendar/<str:telephone>/<int:service_id>/<str:data>/<str:horario>/", views.agendar_horario, name="agendar_horario"),
    path('sobre/', views.about_view, name='about'),

]