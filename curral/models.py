from django.db import models


class TipoCurral(models.Model):
    idTipo_curral = models.AutoField(
        primary_key=True,
        help_text="Identificador único do tipo de curral."
    )
    nome_tipo_curral = models.CharField(
        max_length=45,
        help_text="Descrição do tipo de curral (por exemplo: 'Confinamento', 'Pasto')."
    )

    class Meta:
        db_table = 'Tipo_curral'

    def __str__(self):
        return self.nome_tipo_curral

class Curral(models.Model):
    idCurral = models.AutoField(
        primary_key=True,
        help_text="Identificador único do curral."
    )
    nome_curral = models.CharField(
        max_length=70,
        help_text="Nome ou código do curral."
    )
    peso_min = models.DecimalField(
        max_digits=6,
        decimal_places=2,
        help_text="Peso mínimo suportado no curral (em kg)."
    )
    peso_max = models.DecimalField(
        max_digits=6,
        decimal_places=2,
        help_text="Peso máximo suportado no curral (em kg)."
    )
    area_m2 = models.DecimalField(
        max_digits=6,
        decimal_places=2,
        help_text="Área total do curral em metros quadrados."
    )
    area_coche = models.DecimalField(
        max_digits=6,
        decimal_places=2,
        help_text="Área destinada à cocheira (descanso) dentro do curral, em metros quadrados."
    )
    ativo = models.BooleanField(
        default=True,
        help_text="Indica se o curral está ativo (True) ou inativo (False)."
    )
    tipo_curral = models.ForeignKey(
        TipoCurral,
        on_delete=models.PROTECT,
        related_name='currais',
        help_text="Referência ao tipo de curral."
    )

    class Meta:
        db_table = 'Curral'
    
    def __str__(self):
            return self.nome_curral