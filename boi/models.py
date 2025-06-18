from django.db import models

class Fornecedor(models.Model):
    idfornecedor = models.AutoField(
        primary_key=True,
        help_text="Identificador único do fornecedor."
    )
    nome_fornecedor = models.CharField(
        max_length=80,
        help_text="Nome do fornecedor."
    )

    class Meta:
        db_table = 'Fornecedor'

    def __str__(self):
        return self.nome_fornecedor

class Sexo(models.Model):
    idsexo = models.AutoField(
        primary_key=True,
        help_text="Identificador único do sexo."
    )
    tipo_sexo = models.CharField(
        max_length=10,
        help_text="Descrição do sexo (por exemplo: 'Macho', 'Fêmea')."
    )

    class Meta:
        db_table = 'Sexo'

    def __str__(self):
        return self.tipo_sexo

class Raca(models.Model):
    idraca = models.AutoField(
        primary_key=True,
        help_text="Identificador único da raça."
    )
    nome_raca = models.CharField(
        max_length=30,
        help_text="Nome da raça do boi (por exemplo: 'Nelore', 'Angus')."
    )

    class Meta:
        db_table = 'Raca'

    def __str__(self):
        return self.nome_raca

class StatusBoi(models.Model):
    idstatus_boi = models.AutoField(primary_key=True)
    STATUS_CHOICES = [
        ('Ativo', 'Ativo'),
        ('Morto', 'Morto'),
        ('Vendido', 'Vendido'),
    ]

    nome_status = models.CharField(
        max_length=10,
        choices=STATUS_CHOICES,
    )

    class Meta:
        db_table = 'status_boi'

    def __str__(self):
        return self.nome_status
    
class Boi(models.Model):
    idboi = models.AutoField(
        primary_key=True,
    )
    brinco = models.CharField(
        max_length=15,
    )
    chip = models.CharField(
        max_length=15,
        blank=True,
        null=True,
    )
    peso_entrada = models.DecimalField(
        max_digits=6,
        decimal_places=2,
        blank=True,
        null=True,
    )
    peso_saida = models.DecimalField(
        max_digits=6,
        decimal_places=2,
        blank=True,
        null=True,
    )

    data_nascimento = models.DateField(
        blank=True,
        null=True,
    )
    data_entrada = models.DateField()
    data_saida = models.DateField(
        blank=True,
        null=True,
    )
    data_morte = models.DateField(
        blank=True,
        null=True,
    )

    motivo_morte = models.CharField(
        max_length=200,
        blank=True,
        null=True,
    )
    necropsia = models.BooleanField(
        null=True,
        blank=True,
        default=False,
    )
    sexo = models.ForeignKey(
        Sexo,
        on_delete=models.PROTECT,
        related_name='bois_por_sexo',
    )
    fornecedor = models.ForeignKey(
        Fornecedor,
        on_delete=models.PROTECT,
        related_name='bois_por_fornecedor',
        blank=True,
        null=True,
    )
    raca = models.ForeignKey(
        Raca,
        on_delete=models.PROTECT,
        related_name='bois_por_raca',
    )
    lote = models.ForeignKey(
        'lote.Lote',
        on_delete=models.PROTECT,
        related_name='bois_por_lote',
        blank=True,
        null=True,
    )
    status_boi = models.ForeignKey( 
        StatusBoi, 
        on_delete=models.PROTECT, 
        related_name='bois_por_status'
    )

    class Meta:
        db_table = 'Boi'

    def __str__(self):
        return self.brinco

class PesoMovimentacao(models.Model):
    id_peso_movimentacao = models.AutoField(primary_key=True)
    peso_movimentacao = models.DecimalField( max_digits=6, decimal_places=2)
    data_movimentacao = models.DateField()
    boi = models.ForeignKey(
        Boi,
        on_delete=models.PROTECT,
        related_name='pesagens'
    )

    class Meta:
        db_table = 'peso_movimentacao'

    def __str__(self):
        return self.peso_movimentacao

class PesoProjetado(models.Model):
    id_peso_projetado = models.AutoField(
        primary_key=True,
        help_text="Identificador único do registro de projeção de peso."
    )
    peso_projetado = models.DecimalField(max_digits=6, decimal_places=2)
    data_projetado = models.DateField()
    boi = models.ForeignKey(
        Boi,
        on_delete=models.PROTECT,
        related_name='projecoes_peso')

    class Meta:
        db_table = 'peso_projetado'

    def __str__(self):
        return self.peso_projetado