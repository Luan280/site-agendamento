from django.urls import path, include
from site_agendamento import views

urlpatterns = [
    path('', views.login, name='login'),
    path('index/', views.home, name='home'),
]