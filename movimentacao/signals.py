from django.db.models.signals import post_save
from django.dispatch import receiver
from .models import Movimentacao
from boi.models import Boi

@receiver(post_save, sender=Movimentacao)
def atualizar_animais_e_curral(sender, instance, created, **kwargs):
    if created:

        lote_destino = instance.lote_destino
        lote_destino.curral = instance.curral_destino
        lote_destino.save()

        Boi.objects.filter(lote=instance.lote_origem).update(lote=instance.lote_destino)
