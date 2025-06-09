from django.db import models

class StatusMovimentacao(models.Model):
    idstatus_movimentacao = models.AutoField(
        primary_key=True,
        help_text="Identificador único do status de movimentação."
    )
    nome_status = models.CharField(
        max_length=45,
        help_text="Descrição do status da movimentação (por exemplo: 'Em trânsito', 'Concluída')."
    )

    class Meta:
        db_table = 'status_movimentacao'


class Movimentacao(models.Model):
    idmovimentacao = models.AutoField(
        primary_key=True,
        help_text="Identificador único da movimentação."
    )
    data_movimentacao = models.DateField(
        help_text="Data em que a movimentação ocorreu."
    )
    status = models.ForeignKey(
        StatusMovimentacao,
        on_delete=models.PROTECT,
        related_name='movimentacoes',
        help_text="Status atual da movimentação."
    )

    class Meta:
        db_table = 'movimentacao'


class MovimentacaoLoteOrigem(models.Model):
    idmovimentacao_lote_origem = models.AutoField(
        primary_key=True,
        help_text="Identificador único do registro de origem de lote em movimentação."
    )
    curral = models.ForeignKey(
        'curral.Curral',
        on_delete=models.PROTECT,
        related_name='movorigem_curral',
        help_text="Curral de origem da movimentação."
    )
    lote = models.ForeignKey(
        'lote.Lote',
        on_delete=models.PROTECT,
        related_name='movorigem_lote',
        help_text="Lote de origem da movimentação."
    )
    movimentacao = models.ForeignKey(
        Movimentacao,
        on_delete=models.PROTECT,
        related_name='movorigem_mov',
        help_text="Movimentação associada à origem."
    )

    class Meta:
        db_table = 'movimentacao_lote_origem'


class MovimentacaoLoteDestino(models.Model):
    idmovimentacao_lote_destino = models.AutoField(
        primary_key=True,
        help_text="Identificador único do registro de destino de lote em movimentação."
    )
    lote = models.ForeignKey(
        'lote.Lote',
        on_delete=models.PROTECT,
        related_name='movdestino_lote',
        help_text="Lote de destino da movimentação."
    )
    curral = models.ForeignKey(
        'curral.Curral',
        on_delete=models.PROTECT,
        related_name='movdestino_curral',
        help_text="Curral de destino da movimentação."
    )
    movimentacao = models.ForeignKey(
        Movimentacao,
        on_delete=models.PROTECT,
        related_name='movdestino_mov',
        help_text="Movimentação associada ao destino."
    )

    class Meta:
        db_table = 'movimentacao_lote_destino'


