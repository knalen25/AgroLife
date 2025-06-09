from django.db import models

class Doenca(models.Model):
    iddoenca = models.AutoField(
        primary_key=True,
        help_text="Identificador único da doença."
    )
    nome_doenca = models.CharField(
        max_length=50,
        help_text="Nome da doença (por exemplo: 'Mastite', 'Pneumonia')."
    )

    class Meta:
        db_table = 'doenca'
        
class ResponsavelTecnico(models.Model):
    idresponsavel_tecnico = models.AutoField(
        primary_key=True,
        help_text="Identificador único do responsável técnico."
    )
    nome_responsavel = models.CharField(
        max_length=50,
        help_text="Nome do responsável técnico pela aplicação."
    )

    class Meta:
        db_table = 'responsavel_tecnico'
        
class TipoMedicamento(models.Model):
    idtipo_medicamento = models.AutoField(
        primary_key=True,
        help_text="Identificador único do tipo de medicamento."
    )
    nome_medicamento = models.CharField(
        max_length=50,
        help_text="Nome do tipo de medicamento (por exemplo: 'Antibiótico', 'Vacina')."
    )

    class Meta:
        db_table = 'tipo_medicamento'


class PrincipioAtivo(models.Model):
    idprincipio_ativo = models.AutoField(
        primary_key=True,
        help_text="Identificador único do princípio ativo."
    )
    nome_principio_ativo = models.CharField(
        max_length=45,
        help_text="Nome do princípio ativo (por exemplo: 'Penicilina', 'Ivermectina')."
    )

    class Meta:
        db_table = 'principio_ativo'


class Laboratorio(models.Model):
    idlaboratorio = models.AutoField(
        primary_key=True,
        help_text="Identificador único do laboratório."
    )
    nome_laboratorio = models.CharField(
        max_length=50,
        help_text="Nome do laboratório fabricante."
    )

    class Meta:
        db_table = 'laboratorio'


class Medicamento(models.Model):
    idmedicamento = models.AutoField(
        primary_key=True,
        help_text="Identificador único do medicamento."
    )
    nome_medicamento = models.CharField(
        max_length=50,
        help_text="Nome comercial do medicamento."
    )
    dias_de_carencia = models.IntegerField(
        help_text="Período de carência (em dias) após aplicação do medicamento."
    )
    preco_ml = models.DecimalField(
        max_digits=4,
        decimal_places=2,
        help_text="Preço do medicamento por ml."
    )
    tipo_medicamento = models.ForeignKey(
        TipoMedicamento,
        on_delete=models.PROTECT,
        related_name='medicamentos_por_tipo',
        help_text="Tipo do medicamento."
    )
    principio_ativo = models.ForeignKey(
        PrincipioAtivo,
        on_delete=models.PROTECT,
        related_name='medicamentos_por_principio',
        help_text="Princípio ativo presente no medicamento."
    )
    laboratorio = models.ForeignKey(
        Laboratorio,
        on_delete=models.PROTECT,
        related_name='medicamentos_por_laboratorio',
        help_text="Laboratório responsável pela fabricação do medicamento."
    )

    class Meta:
        db_table = 'medicamento'
    
    
class AplicacaoEvento(models.Model):
    idaplicacao_evento = models.AutoField(
        primary_key=True,
        help_text="Identificador único da aplicação de medicamento."
    )
    data_aplicacao_medicamento = models.DateField(
        help_text="Data em que o medicamento foi aplicado."
    )

    boi = models.ForeignKey(
        'boi.Boi',
        on_delete=models.PROTECT,
        related_name='aplicacoes',
        help_text="Boi que recebeu a aplicação do medicamento."
    )
    
    medicamento = models.ManyToManyField(
        Medicamento,
        through='MedicamentoAplicado',
        related_name='eventos_associados'
    )
    doenca = models.ForeignKey(
        Doenca,
        on_delete=models.PROTECT,
        related_name='aplicacoes_doenca',
        blank=True,
        null=True,
        help_text="Doença que motivou a aplicação (opcional)."
    )
    responsavel_tecnico = models.ForeignKey(
        ResponsavelTecnico,
        on_delete=models.PROTECT,
        related_name='aplicacoes_por_tecnico',
        blank=True,
        null=True,
        help_text="Pessoa responsável pela aplicação do medicamento."
    )

    class Meta:
        db_table = 'aplicacao_medicamento'


class MedicamentoAplicado(models.Model):

    idmedicamento_aplicado = models.AutoField(primary_key=True)
    evento = models.ForeignKey(AplicacaoEvento, on_delete=models.CASCADE)
    medicamento = models.ForeignKey(Medicamento, on_delete=models.PROTECT)
    
    dose_aplicada = models.DecimalField(
        max_digits=5,
        decimal_places=2,
        help_text="Dose específica deste medicamento (em ml, mg, etc.)"
    )

    class Meta:
        db_table = 'medicamento_aplicado'
        verbose_name = "Medicamento Aplicado"
        verbose_name_plural = "Medicamentos Aplicados"
        unique_together = ('evento', 'medicamento')