from django.db import models

class StatusMovimentacao(models.Model):
    idstatus_movimentacao = models.AutoField(primary_key=True)
    nome_status = models.CharField(max_length=45)

    def __str__(self):
        return self.nome_status

    class Meta:
        db_table = 'status_movimentacao'

    def __str__(self):
        return self.nome_status

class Movimentacao(models.Model):
    idmovimentacao = models.AutoField(primary_key=True)
    data_movimentacao = models.DateField()
    status = models.ForeignKey(
        StatusMovimentacao,
        on_delete=models.PROTECT,
        related_name='movimentacoes'
    )
    lote_origem = models.ForeignKey(
        'lote.Lote',
        on_delete=models.PROTECT,
        related_name='movimentacoes_origem'
    )
    lote_destino = models.ForeignKey(
        'lote.Lote',
        on_delete=models.PROTECT,
        related_name='movimentacoes_destino'
    )
    curral_destino = models.ForeignKey(
        'curral.Curral',
        on_delete=models.PROTECT,
        related_name='movimentacoes_curral_destino'
    )

    class Meta:
        db_table = 'movimentacao'

    def __str__(self):
        return f"{self.data_movimentacao} | {self.lote_origem} → {self.lote_destino}"