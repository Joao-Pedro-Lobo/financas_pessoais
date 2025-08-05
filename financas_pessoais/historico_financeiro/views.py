from django.shortcuts import render
from django.http import HttpResponse

def historico_view(request):
    return render (request, 'historico_financeiro/historico.html')