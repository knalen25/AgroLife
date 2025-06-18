from django.urls import reverse_lazy
from django.shortcuts import render
from boi.forms import BoiModelForm, BoiMorteForm
from boi.models import Boi, StatusBoi
from django.views.generic import DetailView, DeleteView, UpdateView, CreateView, ListView
from django.db.models import Q

class ListaBoiView(ListView):
    model = Boi
    template_name = 'boi/listaboi.html'
    context_object_name = 'bois'

    def get_queryset(self):
        queryset = super().get_queryset().filter(
            status_boi__nome_status__in=['Ativo', 'Vendido']
        ).order_by('brinco')

        search = self.request.GET.get('search')
        if search:
            queryset = queryset.filter(
                Q(brinco__icontains=search) |
                Q(fornecedor__nome_fornecedor__icontains=search) |
                Q(status_boi__nome_status__icontains=search) |
                Q(lote__nome_lote__icontains=search) |
                Q(data_entrada__icontains=search)
            ).order_by('brinco')

        return queryset
    
class BoiCreateView(CreateView):
    model = Boi
    form_class = BoiModelForm
    template_name = 'boi/nascimentoboi.html'
    success_url = reverse_lazy('listaboi')

class BoiDetailView(DetailView):
    model = Boi
    template_name = 'boi/detalheboi.html'
        
class BoiUpdateView(UpdateView):
    model = Boi
    form_class = BoiModelForm
    template_name = 'boi/atualizarboi.html'
    success_url = reverse_lazy('listaboi')

class BoiDeleteView(DeleteView):
    model = Boi
    template_name = 'boi/deletarboi.html'
    success_url = reverse_lazy('listaboi')

class BoiMorteView(UpdateView):
    model = Boi
    form_class = BoiMorteForm
    template_name = "boi/registrarmorte.html"
    success_url = reverse_lazy('lista_morte')

class ListaBoiMorteView(ListView):
    model = Boi
    template_name = 'boi/listamorte.html'
    context_object_name = 'bois'

    def get_queryset(self):
        status_ids = StatusBoi.objects.filter(nome_status__in=['Ativo', 'Morto']).values_list('idstatus_boi', flat=True)

        queryset = super().get_queryset().filter(status_boi__in=status_ids).order_by('brinco')

        search = self.request.GET.get('search')
        if search:
            queryset = queryset.filter(
                Q(brinco__icontains=search) |
                Q(fornecedor__nome_fornecedor__icontains=search) |
                Q(status_boi__nome_status__icontains=search) |
                Q(lote__nome_lote__icontains=search) |
                Q(data_entrada__icontains=search)
            ).order_by('brinco')

        return queryset