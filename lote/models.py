from django.db import models


class Lote(models.Model):
    idlote = models.AutoField(
        primary_key=True,
        help_text="Identificador único do lote."
    )
    nome_lote = models.CharField(
        max_length=30,
        help_text="Nome ou código do lote."
    )
    data_inicio_lote = models.DateField(
        help_text="Data de início de utilização do lote."
    )
    ativo = models.BooleanField(
        default=True,
        help_text="Indica se o lote está ativo (True) ou inativo (False)."
    )
    curral = models.ForeignKey(
        'curral.Curral',
        on_delete=models.PROTECT,
        related_name='lotes',
        help_text="Curral ao qual o lote está vinculado."
    )

    class Meta:
        db_table = 'Lote'

    def __str__(self):
        return self.nome_lote