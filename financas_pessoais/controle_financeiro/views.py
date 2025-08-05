from django.shortcuts import render, redirect
from .forms import ControleForm
from .models import ControleModel
import pandas as pd
import matplotlib.pyplot as plt
import io
import base64

def controle_view(request):
    # Formulário
    if request.method == 'POST':
        formulario = ControleForm(request.POST)
        if formulario.is_valid():
            formulario.save()
            return redirect('controle_financeiro:home')
    else:
        formulario = ControleForm()

    # Dados
    dados = ControleModel.objects.all().values('Categoria', 'Preço')
    df = pd.DataFrame(dados)

    if df.empty:
        tabela = None
        grafico_base64 = None
    else:
        # Agrupando por categoria
        df_group = df.groupby('Categoria').sum().reset_index()
        df_group.rename(columns={'Preço': 'Total'}, inplace=True)
        df_group['Total'] = pd.to_numeric(df_group['Total'], errors='coerce')
        total_geral = float(df_group['Total'].sum())
        df_group['Porcentagem'] = (df_group['Total'] / total_geral * 100).round(2)

        # Mapeamento de categorias
        CATEGORIA_MAP = {
            '1': 'Educação',
            '2': 'Água',
            '3': 'Luz',
            '4': 'Aluguel',
            '5': 'Comida',
            '6': 'Lazer',
            '7': 'Internet',
            '8': 'Outros'
        }
        df_group['Categoria'] = df_group['Categoria'].map(CATEGORIA_MAP)

        # Criação do gráfico de pizza
        fig, ax = plt.subplots()
        ax.pie(df_group['Porcentagem'], labels=df_group['Categoria'], autopct='%1.1f%%', startangle=90)
        ax.axis('equal')  # Gráfico redondo

        # Conversão para base64
        buf = io.BytesIO()
        plt.savefig(buf, format='png')
        buf.seek(0)
        grafico_base64 = base64.b64encode(buf.read()).decode('utf-8')
        buf.close()
        plt.close(fig)

        tabela = df_group.to_dict(orient='records')

    # Contexto
    contexto = {
        'form': formulario,
        'tabela': tabela,
        'grafico_base64': grafico_base64,
        'total_geral': total_geral if not df.empty else 0,
    }

    return render(request, 'controle_financeiro/controle.html', contexto)
