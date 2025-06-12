from django.db.models.signals import post_save
from django.dispatch import receiver
from .models import Manejo, BoiManejo, ParametroManejo
from manejo.models import StatusManejo

@receiver(post_save, sender=Manejo)
def aplicar_lote_quando_encerrar(sender, instance: Manejo, created, **kwargs):
    # 1) só queremos rodar na atualização, não na criação
    if created:
        return

    # 2) busca o objeto StatusManejo cujo nome é "Encerrado"
    encerrado = StatusManejo.objects.filter(
        nome_status_manejo__iexact='Encerrado'
    ).first()
    if not encerrado:
        return

    # 3) verifica se o Manejo foi atualizado para esse status
    if instance.status_manejo_id != encerrado.idstatus_manejo:
        return

    # 4) para cada BoiManejo vinculado, busca o parâmetro correspondente
    for bm in BoiManejo.objects.filter(manejo=instance):
        for p in ParametroManejo.objects.filter(manejo=instance):
            boi = bm.boi
            # usa peso de entrada do próprio Boi
            peso = boi.peso_entrada
            if p.raca_id == boi.raca_id and p.peso_inicial <= peso <= p.peso_final:
                # 5) atualiza lote no registro de BoiManejo
                bm.lote_destino = p.lote
                bm.save(update_fields=['lote_destino'])

                # 6) opcional: também atualiza o lote no próprio Boi
                boi.lote = p.lote
                boi.save(update_fields=['lote'])
                break
