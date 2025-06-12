# manejo/views.py

from django.shortcuts import render, redirect, get_object_or_404
from django.db import transaction
from django.contrib import messages
from django.urls import reverse_lazy

from .models import Manejo, BoiManejo
from .forms import (
    ManejoForm,
    ParametroManejoFormSet,
    BoiManejoFormSet,
    BoiEntradaFormSet,
)
from boi.models import Boi

def manejo_unificado(request, pk=None):
    if pk:
        manejo = get_object_or_404(Manejo, pk=pk)
        success_url = reverse_lazy('') # Adapte
    else:
        manejo = None
        success_url = reverse_lazy('') # Adapte

    if request.method == 'POST':
        form = ManejoForm(request.POST, instance=manejo)
        param_formset = ParametroManejoFormSet(request.POST, instance=manejo, prefix='parametros')
        
        tipo_manejo = request.POST.get('tipo_manejo')

        if tipo_manejo == 'Entrada':
            boi_formset_entrada = BoiEntradaFormSet(request.POST, prefix='bois_entrada')
            
            if form.is_valid() and param_formset.is_valid() and boi_formset_entrada.is_valid():
                try:
                    with transaction.atomic():
                        # PASSO A: Salva o Manejo principal e os Parâmetros (regras)
                        saved_manejo = form.save()
                        param_formset.instance = saved_manejo
                        param_formset.save()
                        
                        # PASSO B: Salva os formulários de bois novos.
                        # O .save() aqui cria os registros de Boi no banco de dados.
                        # `novos_bois` será uma lista com as instâncias de Boi recém-criadas.
                        novos_bois = boi_formset_entrada.save(commit=False)

                        # Carrega os parâmetros em memória para evitar hits no banco dentro do loop
                        regras_de_lote = list(saved_manejo.parametros_manejo.all())

                        # PASSO C: Itera sobre cada boi recém-criado
                        for boi_criado in novos_bois:
                            boi_criado.save() # Salva o boi individualmente para ter um ID

                            # PASSO D: LÓGICA DE ATRIBUIÇÃO DE LOTE
                            # Para este boi, procuramos uma regra correspondente nos parâmetros
                            lote_atribuido = False
                            for regra in regras_de_lote:
                                # Verifica se a raça e o peso do boi batem com a regra
                                if (regra.raca == boi_criado.raca and
                                        regra.peso_inicial <= boi_criado.peso_entrada <= regra.peso_final):
                                    
                                    # ENCONTROU! Atribui o lote da regra ao boi
                                    boi_criado.lote = regra.lote
                                    boi_criado.save(update_fields=['lote'])
                                    lote_atribuido = True
                                    break # Para de procurar regras para este boi

                            if not lote_atribuido:
                                messages.warning(request, f"Atenção: O boi com brinco {boi_criado.brinco} não se encaixou em nenhum parâmetro e ficou sem lote.")

                            # PASSO E: Cria o registro na tabela de junção BoiManejo
                            BoiManejo.objects.create(
                                manejo=saved_manejo,
                                boi=boi_criado,
                                protocolo_sanitario=saved_manejo.protocolo_sanitario
                            )

                    messages.success(request, "Manejo de Entrada criado e bois alocados com sucesso!")
                    return redirect(success_url)
                
                except Exception as e:
                    messages.error(request, f"Ocorreu um erro inesperado: {e}")

            else: # Se os formulários não forem válidos
                messages.error(request, "Por favor, corrija os erros abaixo.")
                # Precisamos reinicializar o formset de seleção para o template
                boi_formset_selecao = BoiManejoFormSet(queryset=BoiManejo.objects.none(), prefix='bois_selecao')

        else: # Movimentação ou Venda
            boi_formset_selecao = BoiManejoFormSet(request.POST, instance=manejo, prefix='bois_selecao')
            if form.is_valid() and param_formset.is_valid() and boi_formset_selecao.is_valid():
                # Lógica para salvar movimentação/venda... (já implementada antes)
                messages.success(request, f"Manejo de {tipo_manejo} salvo com sucesso!")
                return redirect(success_url)
            else:
                 messages.error(request, "Por favor, corrija os erros abaixo.")
                 boi_formset_entrada = BoiEntradaFormSet(queryset=Boi.objects.none(), prefix='bois_entrada')
    
    else: # GET request
        form = ManejoForm(instance=manejo)
        param_formset = ParametroManejoFormSet(instance=manejo, prefix='parametros')
        boi_formset_entrada = BoiEntradaFormSet(queryset=Boi.objects.none(), prefix='bois_entrada')
        boi_formset_selecao = BoiManejoFormSet(instance=manejo, prefix='bois_selecao')

    context = {
        'form': form,
        'param_formset': param_formset,
        'boi_formset_entrada': locals().get('boi_formset_entrada'),
        'boi_formset_selecao': locals().get('boi_formset_selecao'),
    }
    return render(request, 'manejo/criarmanejo.html', context)