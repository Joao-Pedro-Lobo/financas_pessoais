from django.core.management.base import BaseCommand
from controle_financeiro import Contro
from app2.models import ResumoMensal
from datetime import datetime
from django.db.models import Sum
from django.db import transaction


class Command(BaseCommand):
    help = 'Gera resumo mensal agregado de transações'

    def handle(self, *args, **kwargs):
        hoje = datetime.now()
        mes = hoje.month
        ano = hoje.year
        mes_ref = datetime(ano, mes, 1)

        if ResumoMensal.objects.filter(mes_referencia=mes_ref).exists():
            self.stdout.write(self.style.WARNING('Resumo já existe para este mês.'))
            return

        receitas = Transacao.objects.filter(tipo='receita', data__month=mes, data__year=ano).aggregate(total=Sum('valor'))['total'] or 0
        despesas = Transacao.objects.filter(tipo='despesa', data__month=mes, data__year=ano).aggregate(total=Sum('valor'))['total'] or 0
        saldo = receitas - despesas

        with transaction.atomic():
            ResumoMensal.objects.create(
                mes_referencia=mes_ref,
                total_receitas=receitas,
                total_despesas=despesas,
                saldo_final=saldo
            )

        self.stdout.write(self.style.SUCCESS('Resumo mensal criado com sucesso.'))
