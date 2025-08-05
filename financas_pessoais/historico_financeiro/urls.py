from django.urls import path
from . import views

app_name = 'historico_financeiro'

urlpatterns = [
    path('', views.historico_view, name='home'),
]