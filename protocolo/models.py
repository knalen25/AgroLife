from django.db import models

class ProtocoloSanitario(models.Model):
    idprotocolo_sanitario = models.AutoField(
        primary_key=True,
        help_text="Identificador único do protocolo sanitário."
    )
    nome_protocolo = models.CharField(
        max_length=45,
        help_text="Nome do protocolo sanitário."
    )
    motivo_protocolo = models.CharField( 
        max_length=110,
        help_text="Motivo ou objetivo do protocolo sanitário."
    )
    
    responsavel_tecnico = models.ForeignKey(
        'medicamento.ResponsavelTecnico',
        on_delete=models.PROTECT,
        related_name='protocolos_por_tecnico',
        help_text="Técnico responsável pela formulação ou execução do protocolo."
    )
    
    medicamentos = models.ManyToManyField(
        'medicamento.Medicamento',
        through='ProtocoloMedicamento',
        related_name='protocolos'
    )

    class Meta:
        db_table = 'protocolo_sanitario'
        
class ProtocoloMedicamento(models.Model):
    idprotocolo_medicamento = models.AutoField(
        primary_key=True,
        help_text="Identificador único da relação entre protocolo sanitário e medicamento."
    )
    medicamento = models.ForeignKey(
        'medicamento.Medicamento',
        on_delete=models.PROTECT,
        related_name='protocolos_medicamento',
        help_text="Medicamento associado ao protocolo."
    )
    dose_protocolo = models.IntegerField( 
        help_text="Quantidade de ml."
    )
    protocolo_sanitario = models.ForeignKey(
        ProtocoloSanitario,
        on_delete=models.CASCADE,
        related_name='protocolos_por_sanitario',
        help_text="Protocolo sanitário ao qual o medicamento pertence."
    )

    class Meta:
        db_table = 'protocolo_medicamento'