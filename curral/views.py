from django.shortcuts import render
from curral.forms import CurralModelForm
from curral.models import Curral
from django.views.generic import DetailView, DeleteView, UpdateView, CreateView, ListView
from django.db.models import Q


class ListaCurralView(ListView):
    model = Curral
    template_name = 'curral/listacurral.html'
    context_object_name = 'currais'

    def get_queryset(self):
        queryset = super().get_queryset().order_by('nome')
        search = self.request.GET.get('search')

        if search:
            queryset = queryset.filter(
                Q(nome_curral__icontains=search) |
                Q(tipo_curral__nome_tipo_curral__icontains=search)
            ).order_by('nome')
        return queryset        
        
class CurralCreateView(CreateView):
    model = Curral
    form_class = CurralModelForm
    template_name = 'curral/criarcurral.html'
    success_url = '/listacurral/'

class CurralDetailView(DetailView):
    model = Curral
    template_name = 'curral/detalhecurral.html'
    
class CurralUpdateView(UpdateView):
    model = Curral
    form_class = CurralModelForm
    template_name = 'curral/atualizarcurral.html'
    success_url = '/listacurral/'

class CurralDeleteView(DeleteView):
    model = Curral
    template_name = 'curral/deletarcurral.html'
    success_url = '/listacurral/'