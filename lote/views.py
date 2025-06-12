from django.shortcuts import render
from django.urls import reverse_lazy
from lote.forms import LoteModelForm
from lote.models import Lote
from django.views.generic import DetailView, DeleteView, UpdateView, CreateView, ListView
from django.db.models import Q

class ListaLoteView(ListView):
    model = Lote
    template_name = 'lote/listalote.html'
    context_object_name = 'lotes'

    def get_queryset(self):
        # Ordena pelo campo nome_lote
        queryset = super().get_queryset().order_by('nome_lote')
        search = self.request.GET.get('search')
        if search:
            queryset = queryset.filter(
                Q(nome_lote__icontains=search) |
                Q(curral__nome__icontains=search)
            ).order_by('nome_lote')
        return queryset
                
class LoteCreateView(CreateView):
    model = Lote
    form_class = LoteModelForm
    template_name = 'lote/criarlote.html'
    success_url = reverse_lazy('listalote')

class LoteDetailView(DetailView):
    model = Lote
    template_name = 'lote/detalhelote.html'

class LoteUpdateView(UpdateView):
    model = Lote
    form_class = LoteModelForm
    template_name = 'lote/atualizarlote.html'
    success_url = reverse_lazy('listalote')
    
class LoteDeleteView(DeleteView):
    model = Lote
    template_name = 'lote/deletarlote.html'
    success_url = reverse_lazy('listalote')