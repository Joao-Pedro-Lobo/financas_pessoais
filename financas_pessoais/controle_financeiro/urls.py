from django.urls import path
from . import views

app_name= 'controle_financeiro'

urlpatterns = [
    path('', views.controle_view, name='home'),
]