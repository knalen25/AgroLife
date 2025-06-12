from django.views.generic import ListView, CreateView, UpdateView, DeleteView, DetailView, View
from django.shortcuts import render, redirect, get_object_or_404
from django.urls import reverse_lazy
from .models import Medicamento, AplicacaoEvento
from .forms import (MedicamentoForm, AplicacaoEventoForm, MedicamentoAplicadoFormSet)

class MedicamentoListView(ListView):
    model = Medicamento
    template_name = 'medicamento/listamedicamento.html'
    context_object_name = 'medicamentos'

class MedicamentoCreateView(CreateView):
    model = Medicamento
    form_class = MedicamentoForm
    template_name = 'medicamento/criarmedicamento.html'
    success_url = reverse_lazy('listamedicamento')

class MedicamentoUpdateView(UpdateView):
    model = Medicamento
    form_class = MedicamentoForm
    template_name = 'medicamento/atualizarmedicamento.html'
    success_url = reverse_lazy('listamedicamento')

class MedicamentoDeleteView(DeleteView):
    model = Medicamento
    template_name = 'medicamento/deletarmedicamento.html'
    success_url = reverse_lazy('listamedicamento')

class AplicacaoEventoCreateView(View):
    template_name = 'aplicacao/criaraplicacao.html'

    def get(self, request):
        evento_form = AplicacaoEventoForm()
        formset = MedicamentoAplicadoFormSet(prefix='form')
        return render(request, self.template_name, {
            'evento_form': evento_form,
            'formset': formset,
            'medicamentos': [],
        })

    def post(self, request):
        evento_form = AplicacaoEventoForm(request.POST)
        formset = MedicamentoAplicadoFormSet(request.POST, prefix='form')

        if evento_form.is_valid() and formset.is_valid():
            evento = evento_form.save()
            formset.instance = evento
            formset.save()

            medicamentos = evento.medicamentoaplicado_set.select_related('medicamento')
            return render(request, self.template_name, {
                'evento_form': AplicacaoEventoForm(instance=evento),
                'formset': MedicamentoAplicadoFormSet(instance=evento, prefix='form'),
                'medicamentos': medicamentos
            })

        return render(request, self.template_name, {
            'evento_form': evento_form,
            'formset': formset,
            'medicamentos': []
        })

class AplicacaoEventoUpdateView(View):
    template_name = 'aplicacao/atualizaraplicacao.html'

    def get(self, request, pk):
        evento = get_object_or_404(AplicacaoEvento, pk=pk)
        evento_form = AplicacaoEventoForm(instance=evento)
        formset = MedicamentoAplicadoFormSet(instance=evento, prefix='form')
        return render(request, self.template_name, {
            'evento_form': evento_form,
            'formset': formset,
            'evento': evento
        })

    def post(self, request, pk):
        evento = get_object_or_404(AplicacaoEvento, pk=pk)
        evento_form = AplicacaoEventoForm(request.POST, instance=evento)
        formset = MedicamentoAplicadoFormSet(request.POST, instance=evento, prefix='form')

        if evento_form.is_valid() and formset.is_valid():
            evento_form.save()
            formset.save()
            return redirect('lista_aplicacoes')

        return render(request, self.template_name, {
            'evento_form': evento_form,
            'formset': formset,
            'evento': evento
        })

class AplicacaoEventoListView(ListView):
    model = AplicacaoEvento
    template_name = 'aplicacao/listaaplicacao.html'
    context_object_name = 'aplicacoes'

class AplicacaoEventoDeleteView(DeleteView):
    model = AplicacaoEvento
    template_name = 'aplicacao/deletaraplicacao.html'
    context_object_name = 'evento'
    success_url = reverse_lazy('lista_aplicacoes')
    
class AplicacaoEventoDetailView(DetailView):
    model = AplicacaoEvento
    template_name = 'aplicacao/detalheaplicacao.html'
    context_object_name = 'evento'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['medicamentos_aplicados'] = self.object.medicamentoaplicado_set.select_related('medicamento')
        return context
