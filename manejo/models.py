from django.db import models

class TipoManejo(models.Model):
    idtipo_manejo = models.AutoField(primary_key=True)
    nome_tipo_manejo = models.CharField(
        max_length=20,
        help_text="Descrição do tipo de manejo (por exemplo: 'Pesagem', 'Vacinação')."
    )

    class Meta:
        db_table = 'tipo_manejo'

    def __str__(self):
        return self.nome_tipo_manejo

class StatusManejo(models.Model):
    idstatus_manejo = models.AutoField(primary_key=True)
    nome_status_manejo = models.CharField(
        max_length=45,
        help_text="Descrição do status do manejo (por exemplo: 'Programado', 'Concluído')."
    )

    class Meta:
        db_table = 'status_manejo'

    def __str__(self):
        return self.nome_status_manejo

class Manejo(models.Model):
    idManejo = models.AutoField(primary_key=True)
    
    tipo_manejo = models.ForeignKey(
        TipoManejo,
        on_delete=models.PROTECT,
        related_name='manejos_por_tipo',
        help_text="Tipo de manejo aplicado."
    )
    status_manejo = models.ForeignKey(
        StatusManejo,
        on_delete=models.PROTECT,
        related_name='manejos_por_status',
        help_text="Status atual do manejo."
    )
    data_manejo = models.DateField(
        help_text="Data em que o manejo foi realizado."
    )
    protocolo_sanitario = models.ForeignKey(
        'protocolo.ProtocoloSanitario',
        on_delete=models.PROTECT,
        related_name='manejos_protocolo',
        help_text="Protocolo sanitário utilizado no manejo."
    )

    class Meta:
        db_table = 'manejo'

    def __str__(self):
        return f"Manejo #{self.idManejo} - {self.data_manejo}"

class BoiManejo(models.Model):
    idboi_manejo = models.AutoField(primary_key=True)

    boi = models.ForeignKey(
        'boi.Boi',
        on_delete=models.PROTECT,
        related_name='manejos',
        help_text="Boi que participou do manejo."
    )
    manejo = models.ForeignKey(
        Manejo,
        on_delete=models.PROTECT,
        related_name='bois_em_manejo',
        help_text="Manejo ao qual o boi está vinculado."
    )
    protocolo_sanitario = models.ForeignKey(
        'protocolo.ProtocoloSanitario',
        on_delete=models.PROTECT,
        related_name='bois_protocolo',
        blank=True,
        null=True,
        help_text="Protocolo sanitário utilizado no manejo."
    )

    class Meta:
        db_table = 'boi_manejo'
        
    def __str__(self):
        return self.idboi_manejo

class ParametroManejo(models.Model):
    idparametro_manejo = models.AutoField(primary_key=True)

    manejo = models.ForeignKey(
        Manejo,
        on_delete=models.CASCADE,
        related_name='parametros_manejo',
        help_text="Manejo ao qual este parâmetro pertence."
    )
    lote = models.ForeignKey(
        'lote.Lote',
        on_delete=models.PROTECT,
        help_text="Lote envolvido no manejo."
    )
    raca = models.ForeignKey(
        'boi.Raca',
        on_delete=models.PROTECT,
        help_text="Raça dos animais no lote."
    )
    peso_inicial = models.DecimalField(
        max_digits=5,
        decimal_places=2,
        help_text="Peso inicial dos animais do lote."
    )
    peso_final = models.DecimalField(
        max_digits=5,
        decimal_places=2,
        help_text="Peso final dos animais do lote."
    )

    class Meta:
        db_table = 'parametro_manejo'

    def __str__(self):
        return f"{self.lote} - {self.raca} ({self.peso_inicial}kg → {self.peso_final}kg)"