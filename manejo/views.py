# manejo/views.py

from django.shortcuts import render, redirect
from django.db import transaction
from django.contrib import messages
from manejo.forms import ManejoForm, ParametroManejoFormSet, BoiEntradaFormSet, SelecaoLoteForm, BoiSaidaFormSet, VendaBoiForm, BuscaBoiForm
from manejo.models import Manejo, TipoManejo, StatusManejo, BoiManejo
from boi.models import StatusBoi
from lote.models import Lote
from boi.models import Boi
import datetime

# @transaction.atomic
def criar_manejo_entrada(request):
    template_name = 'manejo/manejoentrada.html'
    
    if request.method == 'POST':
        # Instancia o formulário principal do Manejo e os dois formsets com os dados da requisição
        form_manejo = ManejoForm(request.POST)
        formset_parametros = ParametroManejoFormSet(request.POST, prefix='parametros')
        formset_bois = BoiEntradaFormSet(request.POST, prefix='bois')

        # Valida todos os formulários
        if form_manejo.is_valid() and formset_parametros.is_valid() and formset_bois.is_valid():
            
            # 1. Salva o Manejo principal
            manejo = form_manejo.save(commit=False)
            status_concluido = StatusManejo.objects.get(nome_status_manejo='Concluido')
            manejo.status_manejo = status_concluido
            manejo.save()

            # 2. Salva os Parâmetros (regras) associados a este Manejo
            formset_parametros.instance = manejo
            formset_parametros.save()
            
            # Pega as regras que acabamos de salvar para consulta
            regras_deste_manejo = manejo.parametros_manejo.all()

            # 3. Processa e salva cada Boi
            status_ativo_boi = StatusBoi.objects.get(nome_status='Ativo')
            bois_cadastrados = 0
            for boi_form in formset_bois:
                if boi_form.cleaned_data and not boi_form.cleaned_data.get('DELETE', False):
                    peso_entrada = boi_form.cleaned_data['peso_entrada']
                    raca_boi = boi_form.cleaned_data['raca']

                    # Busca o lote usando as regras específicas deste manejo
                    lote_encontrado = None
                    for regra in regras_deste_manejo:
                        if regra.raca == raca_boi and regra.peso_inicial <= peso_entrada <= regra.peso_final:
                            lote_encontrado = regra.lote
                            break
                    
                    if not lote_encontrado:
                        messages.error(request, f"Nenhuma regra definida NESTE manejo para um boi da raça '{raca_boi}' com peso {peso_entrada}kg. A operação foi cancelada.")
                        # A anotação @transaction.atomic cuidará do rollback
                        return redirect('criar_manejo_entrada')
                    
                    # Salva o Boi
                    boi = boi_form.save(commit=False)
                    boi.lote = lote_encontrado
                    boi.status_boi = status_ativo_boi
                    boi.save()

                    # Cria o vínculo Boi-Manejo
                    BoiManejo.objects.create(boi=boi, manejo=manejo)
                    bois_cadastrados += 1
            
            if bois_cadastrados == 0:
                 messages.warning(request, "Nenhum boi foi adicionado ao manejo.")
                 return redirect('')

            messages.success(request, f"Manejo de entrada #{manejo.idManejo} criado com sucesso! {bois_cadastrados} boi(s) registrados.")
            return redirect('pagina_de_sucesso_ou_listagem_de_manejos') # Altere para sua URL

    else:
        # Se for um GET, cria os formulários vazios
        form_manejo = ManejoForm(initial={'tipo_manejo': TipoManejo.objects.get(nome_tipo_manejo='Entrada')})
        formset_parametros = ParametroManejoFormSet(prefix='parametros')
        formset_bois = BoiEntradaFormSet(prefix='bois')

    context = {
        'form_manejo': form_manejo,
        'formset_parametros': formset_parametros,
        'formset_bois': formset_bois,
    }
    return render(request, template_name, context)





# @transaction.atomic
def manejo_saida_venda(request):
    template_name = 'manejo/manejosaida.html'
    context = {}

    # Inicializa a lista de venda na sessão se não existir
    if 'venda_atual' not in request.session:
        request.session['venda_atual'] = []

    # Ação 1: Finalizar a Venda
    if request.method == 'POST' and 'finalizar_venda' in request.POST:
        venda_atual = request.session.get('venda_atual', [])
        if not venda_atual:
            messages.error(request, "Não há animais na lista para vender.")
            return redirect('manejo_saida_venda')

        # Cria um único Manejo para toda esta operação de venda
        data_manejo_geral = datetime.datetime.strptime(venda_atual[0]['data_saida'], '%Y-%m-%d').date()
        manejo = Manejo.objects.create(
            tipo_manejo=TipoManejo.objects.get(nome_tipo_manejo='saida'),
            status_manejo=StatusManejo.objects.get(nome_status_manejo='Concluído'),
            data_manejo=data_manejo_geral
        )
        status_vendido = StatusBoi.objects.get(nome_status='Vendido')

        # Atualiza cada boi da lista
        for boi_data in venda_atual:
            boi = Boi.objects.get(pk=boi_data['boi_id'])
            boi.peso_saida = boi_data['peso_saida']
            boi.data_saida = datetime.datetime.strptime(boi_data['data_saida'], '%Y-%m-%d').date()
            boi.status_boi = status_vendido
            boi.save()
            BoiManejo.objects.create(boi=boi, manejo=manejo)

        # Limpa a sessão e redireciona para o sucesso
        del request.session['venda_atual']
        messages.success(request, f"Venda de {len(venda_atual)} animais concluída com sucesso!")
        return redirect('pagina_de_sucesso_ou_listagem_de_manejos')

    # Ação 2: Adicionar um boi à lista de venda
    elif request.method == 'POST' and 'adicionar_a_venda' in request.POST:
        venda_form = VendaBoiForm(request.POST)
        if venda_form.is_valid():
            boi_id = venda_form.cleaned_data['boi_id']
            # Garante que o mesmo boi não seja adicionado duas vezes
            venda_atual = request.session.get('venda_atual', [])
            if any(b['boi_id'] == boi_id for b in venda_atual):
                messages.warning(request, "Este animal já está na lista de venda.")
            else:
                # Adiciona os dados do boi à sessão
                nova_venda = {
                    'boi_id': boi_id,
                    'brinco': Boi.objects.get(pk=boi_id).brinco, # Pega o brinco para exibição
                    'peso_saida': str(venda_form.cleaned_data['peso_saida']),
                    'data_saida': venda_form.cleaned_data['data_saida'].strftime('%Y-%m-%d'),
                }
                venda_atual.append(nova_venda)
                request.session['venda_atual'] = venda_atual
                messages.success(request, f"Boi {nova_venda['brinco']} adicionado à venda.")
            
            return redirect('manejo_saida_venda')
        else:
            # Se o formulário de venda for inválido, re-exibe a página com o boi encontrado e os erros
            context['venda_form'] = venda_form
            context['boi_encontrado'] = Boi.objects.get(pk=request.POST.get('boi_id'))


    # Ação 3: Buscar um boi
    elif request.method == 'POST' and 'buscar_boi' in request.POST:
        busca_form = BuscaBoiForm(request.POST)
        if busca_form.is_valid():
            brinco = busca_form.cleaned_data['brinco']
            try:
                # Busca por boi ativo com o brinco exato
                boi_encontrado = Boi.objects.get(brinco__iexact=brinco, status_boi__nome_status='Ativo')
                # Prepara o formulário de venda para este boi
                venda_form = VendaBoiForm(initial={'boi_id': boi_encontrado.idboi, 'data_saida': datetime.date.today()})
                context['boi_encontrado'] = boi_encontrado
                context['venda_form'] = venda_form
            except Boi.DoesNotExist:
                messages.error(request, f"Nenhum boi ATIVO encontrado com o brinco '{brinco}'.")
    
    # Se a página for carregada (GET) ou após uma ação, exibe o estado atual
    if 'busca_form' not in context:
        context['busca_form'] = BuscaBoiForm()
    
    # Carrega a lista da sessão para exibir no template
    venda_atual_data = request.session.get('venda_atual', [])
    context['venda_atual'] = venda_atual_data

    return render(request, template_name, context)
