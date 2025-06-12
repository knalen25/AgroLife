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
    # Definimos uma tupla de choices – cada item é (valor_guardado, rótulo_para_exibir)
    STATUS_CHOICES = [
        ('Ativo', 'Ativo'),
        ('Morto', 'Morto'),
        ('Vendido', 'Vendido'),
    ]

    nome_status = models.CharField(
        max_length=10,          # basta tamanho para conter os valores
        choices=STATUS_CHOICES,
        help_text="Escolha o status do boi."
    )

    class Meta:
        db_table = 'status_boi'

    def __str__(self):
        return self.nome_status

class Boi(models.Model):
    idboi = models.AutoField(
        primary_key=True,
        help_text="Identificador único do boi."
    )
    brinco = models.CharField(
        max_length=15,
        help_text="Número do brinco do boi (identificação individual)."
    )
    chip = models.CharField(
        max_length=15,
        blank=True,
        null=True,
        help_text="Código do chip do boi (opcional)."
    )

    peso_entrada = models.DecimalField(
        max_digits=6,
        decimal_places=2,
        blank=True,
        null=True,
        help_text="Peso do boi no momento de entrada (em kg)."
    )
    peso_saida = models.DecimalField(
        max_digits=6,
        decimal_places=2,
        blank=True,
        null=True,
        help_text="Peso do boi no momento de saída (em kg)."
    )

    data_nascimento = models.DateField(
        blank=True,
        null=True,
        help_text="Data de nascimento do boi."
    )
    data_entrada = models.DateField(
        help_text="data de entrada do boi"
    )
    data_saida = models.DateField(
        blank=True,
        null=True,
        help_text="Data de saída do boi (venda ou transferência)."
    )
    data_morte = models.DateField(
        blank=True,
        null=True,
        help_text="Data de morte do boi (se aplicável)."
    )

    motivo_morte = models.CharField(
        max_length=200,
        blank=True,
        null=True,
        help_text="Descrição do motivo da morte do boi (se falecido)."
    )
    necropsia = models.BooleanField(
        null=True,
        blank=True,
        default=False,
        help_text="Indica se foi realizada necropsia (True), não foi (False) ou desconhecido (NULL)."
    )

    sexo = models.ForeignKey(
        Sexo,
        on_delete=models.PROTECT,
        related_name='bois_por_sexo',
        help_text="Sexo do boi."
    )
    fornecedor = models.ForeignKey(
        Fornecedor,
        on_delete=models.PROTECT,
        related_name='bois_por_fornecedor',
        blank=True,
        null=True,
        help_text="Fornecedor de origem do boi."
    )
    raca = models.ForeignKey(
        Raca,
        on_delete=models.PROTECT,
        related_name='bois_por_raca',
        help_text="Raça do boi."
    )
    lote = models.ForeignKey(
        'lote.Lote',
        on_delete=models.PROTECT,
        related_name='bois_por_lote',
        blank=True,
        null=True,
        help_text="Lote atual ao qual o boi pertence."
    )
    status_boi = models.ForeignKey(
        StatusBoi,
        on_delete=models.PROTECT,
        related_name='bois_por_status',
        help_text="Status atual do boi."
    )

    class Meta:
        db_table = 'Boi'

    def __str__(self):
        return self.brinco


class PesoMovimentacao(models.Model):
    id_peso_movimentacao = models.AutoField(
        primary_key=True,
        help_text="Identificador único do registro de pesagem."
    )
    peso_movimentacao = models.DecimalField(
        max_digits=6,
        decimal_places=2,
        help_text="Valor do peso medido na data de movimentação (em kg)."
    )
    data_movimentacao = models.DateField(
        help_text="Data em que a pesagem foi realizada."
    )
    boi = models.ForeignKey(
        Boi,
        on_delete=models.PROTECT,
        related_name='pesagens',
        help_text="Boi cuja pesagem está sendo registrada."
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
    peso_projetado = models.DecimalField(
        max_digits=6,
        decimal_places=2,
        help_text="Valor do peso projetado para a data específica (em kg)."
    )
    data_projetado = models.DateField(
        help_text="Data para a qual a projeção de peso foi calculada."
    )
    boi = models.ForeignKey(
        Boi,
        on_delete=models.PROTECT,
        related_name='projecoes_peso',
        help_text="Boi ao qual esta projeção de peso se refere."
    )

    class Meta:
        db_table = 'peso_projetado'

    def __str__(self):
        return self.peso_projetado
