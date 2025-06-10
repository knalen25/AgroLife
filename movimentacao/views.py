from django.views import View
from django.shortcuts import render, redirect
from django.utils import timezone

from .forms import TrocaCurralForm
from movimentacao.models import Movimentacao
from boi.models import Boi

class TrocaCurralView(View):
    template_name = "movimentacao/troca_curral.html"

    def get(self, request):
        form = TrocaCurralForm()
        return render(request, self.template_name, {'form': form})

    def post(self, request):
        form = TrocaCurralForm(request.POST)
        if form.is_valid():
            movimentacao = form.save()

            # Atualizar curral do lote destino
            lote_destino = movimentacao.lote_destino
            lote_destino.curral = movimentacao.curral_destino
            lote_destino.save()

            # Atualizar bois para o novo lote
            Boi.objects.filter(lote=movimentacao.lote_origem).update(lote=movimentacao.lote_destino)

            return redirect('lista_boas_movimentacoes')  # redirecione conforme sua URL
        return render(request, self.template_name, {'form': form})
