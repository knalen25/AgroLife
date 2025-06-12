from django.views import View
from django.shortcuts import render, redirect
from movimentacao.forms import TrocaCurralForm
from boi.models import Boi

class MovimentacaoView(View):
    template_name = "movimentacao/criarmovimentacao.html"

    def get(self, request):
        form = TrocaCurralForm()
        return render(request, self.template_name, {'form': form})

    def post(self, request):
        form = TrocaCurralForm(request.POST)
        if form.is_valid():
            movimentacao = form.save()

            lote_destino = movimentacao.lote_destino
            lote_destino.curral = movimentacao.curral_destino
            lote_destino.save()

            Boi.objects.filter(lote=movimentacao.lote_origem).update(lote=movimentacao.lote_destino)

            return redirect('listamovimentacao')
        return render(request, self.template_name, {'form': form})