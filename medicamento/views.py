from django.urls import reverse_lazy
from django.views.generic import CreateView, ListView, DeleteView, UpdateView, DetailView
from django.forms import inlineformset_factory
from django.shortcuts import render, redirect
from medicamento.models import Medicamento, AplicacaoEvento
from medicamento.forms import MedicamentoAplicadoFormSet, MedicamentoForm, AplicacaoEventoForm

class MedicamentoCreateView(CreateView):
    model = Medicamento
    form_class = MedicamentoForm
    template_name = 'medicamento/criarmedicamento.html'
    success_url = reverse_lazy('listamedicamento')

class MedicamentoListView(ListView):
    model = Medicamento
    template_name = 'medicamento/listamedicamento.html'
    context_object_name = 'medicamentos'

class MedicamentoDeleteView(DeleteView):
    model = Medicamento
    template_name = 'medicamento/deletarmedicamento.html'
    success_url = reverse_lazy('listamedicamento')
    
class MedicamentoUpdateView(UpdateView):
    model = Medicamento
    form_class = MedicamentoForm
    template_name = 'medicamento/editarmedicamento.html'
    success_url = reverse_lazy('listamedicamento')

class MedicamentoDetailView(DetailView):
    model = Medicamento
    template_name = 'medicamento/detalhemedicamento.html'
    context_object_name = 'medicamento'    
    

class AplicacaoEventoCreateView(CreateView):
    model = AplicacaoEvento
    form_class = AplicacaoEventoForm
    template_name = 'aplicarmedicamento/criaraplicacao.html'
    success_url = reverse_lazy('listaaplicacao')

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        if self.request.POST:
            context['formset'] = MedicamentoAplicadoFormSet(self.request.POST)
        else:
            context['formset'] = MedicamentoAplicadoFormSet()
        return context

    def form_valid(self, form):
        context = self.get_context_data()
        formset = context['formset']
        if formset.is_valid():
            self.object = form.save()
            formset.instance = self.object
            formset.save()
            return redirect(self.get_success_url())
        else:
            return self.render_to_response(self.get_context_data(form=form))

class AplicacaoEventoListView(ListView):
    model = AplicacaoEvento
    template_name = 'aplicarmedicamento/listaaplicacao.html'
    context_object_name = 'aplicacoes'

class AplicacaoEventoDeleteView(DeleteView):
    model = AplicacaoEvento
    template_name = 'aplicarmedicamento/deletaraplicacao.html'
    success_url = reverse_lazy('listaaplicacao')
    
    
class AplicacaoEventoUpdateView(UpdateView):
    model = AplicacaoEvento
    form_class = AplicacaoEventoForm
    template_name = 'aplicarmedicamento/editaraplicacao.html'
    success_url = reverse_lazy('listaaplicacao')

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        if self.request.POST:
            context['formset'] = MedicamentoAplicadoFormSet(self.request.POST, instance=self.object)
        else:
            context['formset'] = MedicamentoAplicadoFormSet(instance=self.object)
        return context

    def form_valid(self, form):
        context = self.get_context_data()
        formset = context['formset']
        if formset.is_valid():
            self.object = form.save()
            formset.instance = self.object
            formset.save()
            return redirect(self.get_success_url())
        else:
            return self.render_to_response(self.get_context_data(form=form))

# ----------- DETALHE DA APLICAÇÃO DE MEDICAMENTO -----------
class AplicacaoEventoDetailView(DetailView):
    model = AplicacaoEvento
    template_name = 'aplicarmedicamento/detalheaplicacao.html'
    context_object_name = 'aplicacao'