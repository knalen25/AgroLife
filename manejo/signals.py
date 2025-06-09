# Em manejo/signals.py
from django.db.models.signals import pre_save
from django.dispatch import receiver
from .models import BoiManejo

# O decorator @receiver conecta esta função ao sinal pre_save do modelo BoiManejo
@receiver(pre_save, sender=BoiManejo)
def definir_protocolo_padrao(sender, instance, **kwargs):
    """
    Antes de salvar um BoiManejo, esta função é executada.
    """
    # A lógica é a mesma, mas vive aqui fora.
    if not instance.protocolo_sanitario:
        instance.protocolo_sanitario = instance.manejo.protocolo_sanitario