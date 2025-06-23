from django.db.models.signals import pre_save
from django.dispatch import receiver
from .models import BoiManejo

@receiver(pre_save, sender=BoiManejo)
def definir_protocolo_padrao(sender, instance, **kwargs):
    if not instance.protocolo_sanitario:
        instance.protocolo_sanitario = instance.manejo.protocolo_sanitario