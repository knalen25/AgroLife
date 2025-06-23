from django.shortcuts import render, redirect
from django.db import transaction
from django.contrib import messages
from decimal import Decimal
from manejo.forms import ManejoForm, ParametroManejoFormSet, BoiEntradaFormSet, BuscaBoiForm,VendaBoiForm, ParametroMovimentacaoFormSet, MovimentacaoDataForm, ManejoUpdateForm
from manejo.models import Manejo, TipoManejo, StatusManejo, BoiManejo
from boi.models import StatusBoi
from boi.models import Boi, PesoMovimentacao
from django.views.generic import ListView, DetailView, UpdateView, DeleteView
from django.urls import reverse_lazy
import datetime

def criar_manejo_entrada(request):
    template_name = 'manejo/manejoentrada.html'
    
    if request.method == 'POST':

        form_manejo = ManejoForm(request.POST)
        formset_parametros = ParametroManejoFormSet(request.POST, prefix='parametros')
        formset_bois = BoiEntradaFormSet(request.POST, prefix='bois')

        if form_manejo.is_valid() and formset_parametros.is_valid() and formset_bois.is_valid():
            
            manejo = form_manejo.save(commit=False)
            status_concluido = StatusManejo.objects.get(nome_status_manejo='Concluido')
            manejo.status_manejo = status_concluido
            manejo.save()

            formset_parametros.instance = manejo
            formset_parametros.save()
            
            regras_deste_manejo = manejo.parametros_manejo.all()

            status_ativo_boi = StatusBoi.objects.get(nome_status='Ativo')
            bois_cadastrados = 0
            for boi_form in formset_bois:
                if boi_form.cleaned_data and not boi_form.cleaned_data.get('DELETE', False):
                    peso_entrada = boi_form.cleaned_data['peso_entrada']
                    raca_boi = boi_form.cleaned_data['raca']

                    lote_encontrado = None
                    for regra in regras_deste_manejo:
                        if regra.raca == raca_boi and regra.peso_inicial <= peso_entrada <= regra.peso_final:
                            lote_encontrado = regra.lote
                            break
                    
                    if not lote_encontrado:
                        messages.error(request, f"Nenhuma regra definida NESTE manejo para um boi da raça '{raca_boi}' com peso {peso_entrada}kg. A operação foi cancelada.")
                        return redirect('criar_manejo_entrada')
                    
                    boi = boi_form.save(commit=False)
                    boi.lote = lote_encontrado
                    boi.status_boi = status_ativo_boi
                    boi.save()

                    BoiManejo.objects.create(boi=boi, manejo=manejo)
                    bois_cadastrados += 1
            
            if bois_cadastrados == 0:
                 messages.warning(request, "Nenhum boi foi adicionado ao manejo.")
                 return redirect('')

            messages.success(request, f"Manejo de entrada #{manejo.idManejo} criado com sucesso! {bois_cadastrados} boi(s) registrados.")
            return redirect('pagina_de_sucesso_ou_listagem_de_manejos') # Altere para sua URL

    else:
        form_manejo = ManejoForm(initial={'tipo_manejo': TipoManejo.objects.get(nome_tipo_manejo='Entrada')})
        formset_parametros = ParametroManejoFormSet(prefix='parametros')
        formset_bois = BoiEntradaFormSet(prefix='bois')

    context = {
        'form_manejo': form_manejo,
        'formset_parametros': formset_parametros,
        'formset_bois': formset_bois,
    }
    return render(request, template_name, context)

def manejo_saida_venda(request):
    template_name = 'manejo/manejosaida.html'
    context = {}

    if 'venda_atual' not in request.session:
        request.session['venda_atual'] = []

    if request.method == 'POST' and 'finalizar_venda' in request.POST:
        venda_atual = request.session.get('venda_atual', [])
        if not venda_atual:
            messages.error(request, "Não há animais na lista para vender.")
            return redirect('manejo_saida_venda')

        data_manejo_geral = datetime.datetime.strptime(venda_atual[0]['data_saida'], '%Y-%m-%d').date()
        manejo = Manejo.objects.create(
            tipo_manejo=TipoManejo.objects.get(nome_tipo_manejo='saida'),
            status_manejo=StatusManejo.objects.get(nome_status_manejo='Concluido'),
            data_manejo=data_manejo_geral
        )
        status_vendido = StatusBoi.objects.get(nome_status='Vendido')

        for boi_data in venda_atual:
            boi = Boi.objects.get(pk=boi_data['boi_id'])
            boi.peso_saida = boi_data['peso_saida']
            boi.data_saida = datetime.datetime.strptime(boi_data['data_saida'], '%Y-%m-%d').date()
            boi.status_boi = status_vendido
            boi.save()
            BoiManejo.objects.create(boi=boi, manejo=manejo)

        del request.session['venda_atual']
        messages.success(request, f"Venda de {len(venda_atual)} animais concluída com sucesso!")
        return redirect('pagina_de_sucesso_ou_listagem_de_manejos')

    elif request.method == 'POST' and 'adicionar_a_venda' in request.POST:
        venda_form = VendaBoiForm(request.POST)
        if venda_form.is_valid():
            boi_id = venda_form.cleaned_data['boi_id']
            venda_atual = request.session.get('venda_atual', [])
            if any(b['boi_id'] == boi_id for b in venda_atual):
                messages.warning(request, "Este animal já está na lista de venda.")
            else:
                nova_venda = {
                    'boi_id': boi_id,
                    'brinco': Boi.objects.get(pk=boi_id).brinco,
                    'peso_saida': str(venda_form.cleaned_data['peso_saida']),
                    'data_saida': venda_form.cleaned_data['data_saida'].strftime('%Y-%m-%d'),
                }
                venda_atual.append(nova_venda)
                request.session['venda_atual'] = venda_atual
                messages.success(request, f"Boi {nova_venda['brinco']} adicionado à venda.")
            
            return redirect('manejo_saida_venda')
        else:
            context['venda_form'] = venda_form
            context['boi_encontrado'] = Boi.objects.get(pk=request.POST.get('boi_id'))

    elif request.method == 'POST' and 'buscar_boi' in request.POST:
        busca_form = BuscaBoiForm(request.POST)
        if busca_form.is_valid():
            brinco = busca_form.cleaned_data['brinco']
            try:
                boi_encontrado = Boi.objects.get(brinco__iexact=brinco, status_boi__nome_status='Ativo')
                venda_form = VendaBoiForm(initial={'boi_id': boi_encontrado.idboi, 'data_saida': datetime.date.today()})
                context['boi_encontrado'] = boi_encontrado
                context['venda_form'] = venda_form
            except Boi.DoesNotExist:
                messages.error(request, f"Nenhum boi ATIVO encontrado com o brinco '{brinco}'.")
    
    if 'busca_form' not in context:
        context['busca_form'] = BuscaBoiForm()
    
    venda_atual_data = request.session.get('venda_atual', [])
    context['venda_atual'] = venda_atual_data

    return render(request, template_name, context)

def manejo_movimentacao(request):
    template_name = 'manejo/manejomovimentacao.html'
    context = {}

    if 'movimentacao_atual' not in request.session:
        request.session['movimentacao_atual'] = []

    if request.method == 'POST':
        manejo_form = ManejoForm(request.POST, prefix='manejo')
        formset_parametros = ParametroMovimentacaoFormSet(request.POST, prefix='parametros')
        
        if 'finalizar_movimentacao' in request.POST:
            animais_na_sessao = request.session.get('movimentacao_atual', [])

            if not animais_na_sessao:
                messages.error(request, "A lista de movimentação está vazia. Adicione animais antes de finalizar.")
                context['manejo_form'] = manejo_form
                context['formset_parametros'] = formset_parametros
            elif manejo_form.is_valid() and formset_parametros.is_valid():
                manejo = manejo_form.save(commit=False)
                manejo.tipo_manejo = TipoManejo.objects.get(nome_tipo_manejo='movimentacao')
                manejo.status_manejo = StatusManejo.objects.get(nome_status_manejo='Concluido')
                manejo.save()

                formset_parametros.instance = manejo
                formset_parametros.save()
                regras_deste_manejo = manejo.parametros_manejo.all()

                for dados_boi in animais_na_sessao:
                    boi = Boi.objects.get(pk=dados_boi['boi_id'])
                    novo_peso = Decimal(dados_boi['peso_movimentacao'])

                    PesoMovimentacao.objects.create(
                        boi=boi, peso_movimentacao=novo_peso, data_movimentacao=manejo.data_manejo
                    )

                    novo_lote = None
                    for regra in regras_deste_manejo:
                        if regra.raca == boi.raca and regra.peso_inicial <= novo_peso <= regra.peso_final:
                            novo_lote = regra.lote
                            break
                    
                    if novo_lote and boi.lote != novo_lote:
                        boi.lote = novo_lote
                        boi.save()

                    BoiManejo.objects.create(boi=boi, manejo=manejo)
                del request.session['movimentacao_atual']
                messages.success(request, "Manejo de movimentação salvo com sucesso!")
                return redirect('pagina_de_sucesso_ou_listagem_de_manejos')
            else:
                messages.error(request, "Não foi possível salvar. Verifique os erros no formulário de manejo ou nos parâmetros.")
                context['manejo_form'] = manejo_form
                context['formset_parametros'] = formset_parametros
        elif 'adicionar_boi' in request.POST:
            mov_data_form = MovimentacaoDataForm(request.POST)
            if mov_data_form.is_valid():
                boi_id = mov_data_form.cleaned_data['boi_id']
                if not any(b['boi_id'] == boi_id for b in request.session['movimentacao_atual']):
                    boi_instance = Boi.objects.get(pk=boi_id)
                    request.session['movimentacao_atual'].append({
                        'boi_id': boi_id,
                        'brinco': boi_instance.brinco,
                        'lote_atual': boi_instance.lote.nome_lote if boi_instance.lote else 'Sem Lote',
                        'peso_movimentacao': str(mov_data_form.cleaned_data['peso_movimentacao'])
                    })
                    request.session.modified = True
                    messages.success(request, f"Boi {boi_instance.brinco} adicionado à lista.")
                else:
                    messages.warning(request, "Este animal já está na lista.")
                context['busca_form'] = BuscaBoiForm()
            else:
                 context['boi_encontrado'] = Boi.objects.get(pk=request.POST.get('boi_id'))
                 context['mov_data_form'] = mov_data_form
            
            context['manejo_form'] = manejo_form
            context['formset_parametros'] = formset_parametros
            
        elif 'buscar_boi' in request.POST:
            busca_form = BuscaBoiForm(request.POST)
            if busca_form.is_valid():
                brinco = busca_form.cleaned_data['brinco']
                try:
                    boi_encontrado = Boi.objects.get(brinco__iexact=brinco, status_boi__nome_status='Ativo')
                    context['boi_encontrado'] = boi_encontrado
                    context['mov_data_form'] = MovimentacaoDataForm(initial={'boi_id': boi_encontrado.idboi})
                except Boi.DoesNotExist:
                    messages.error(request, f"Nenhum boi ATIVO encontrado com o brinco '{brinco}'.")
            
            context['manejo_form'] = manejo_form
            context['formset_parametros'] = formset_parametros
            context['busca_form'] = busca_form

    if 'manejo_form' not in context:
        context['manejo_form'] = ManejoForm(prefix='manejo', initial={'data_manejo': datetime.date.today()})
    if 'formset_parametros' not in context:
        context['formset_parametros'] = ParametroMovimentacaoFormSet(prefix='parametros')
    if 'busca_form' not in context:
        context['busca_form'] = BuscaBoiForm()

    context['animais_na_movimentacao'] = request.session.get('movimentacao_atual', [])

    return render(request, template_name, context)

class ManejoListView(ListView):
    model = Manejo
    template_name = 'manejo/listamanejo.html'
    context_object_name = 'manejos'
    paginate_by = 10

    def get_queryset(self):
    
        tipo_manejo_str = self.kwargs.get('tipo')
        queryset = super().get_queryset().order_by('-data_manejo', '-idManejo')

        if tipo_manejo_str:
            return queryset.filter(tipo_manejo__nome_tipo_manejo__iexact=tipo_manejo_str)
        return queryset

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['tipo_filtro'] = self.kwargs.get('tipo', 'Todos')
        return context
    
class ManejoDetailView(DetailView):
    model = Manejo
    template_name = 'manejo/detalhemanejo.html'
    context_object_name = 'manejo'

class ManejoUpdateView(UpdateView):
    model = Manejo
    form_class = ManejoUpdateForm
    template_name = 'manejo/atualizarmanejo.html'
    context_object_name = 'manejo'
    success_url = reverse_lazy('listamanejo')

class ManejoDeleteView(DeleteView):
    model = Manejo
    template_name = 'manejo/deletarmanejo.html'
    context_object_name = 'manejo'
    success_url = reverse_lazy('listamanejo')