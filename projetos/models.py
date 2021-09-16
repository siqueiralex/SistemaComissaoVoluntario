from django.db import models
from django.db import models
from django.contrib.auth.models import User
from django.utils.timezone import now
from datetime import timedelta, time
from django.utils.formats import date_format


class Unidade(models.Model):
    sigla = models.CharField(max_length=20, unique=True)
    nome = models.CharField(max_length=100, null=True, blank=True)
    
    def __str__(self):
        return f"{self.sigla}"

    class Meta:
        db_table = "unidade"


class Cronograma(models.Model):
    inicio_servicos = models.DateField()
    fim_servicos = models.DateField()

    def __str__(self):
        return f"Voluntário de {date_format(self.inicio_servicos, format='d')} a {date_format(self.fim_servicos)}"

    @property
    def nome_curto(self):
        return f"{self.inicio_servicos.strftime(f'%d/%m')} a {self.fim_servicos.strftime(f'%d/%m')}"

    @property
    def quantidade_de_dias(self):
        inicio = self.inicio_servicos   
        fim = self.fim_servicos   
        delta = fim - inicio  
        return delta.days + 1

    @property
    def lista_de_datas(self):
        return [self.inicio_servicos + timedelta(days=i) for i in range(self.quantidade_de_dias)]

    class Meta:
        ordering = ["-inicio_servicos"]


class Atividade(models.Model):
    TIPO_ATIVIDADE = (

        ( "Profissionalização" , "Profissionalização" ),
        ( "Escolarização" , "Escolarização" ),
        ( "Ocupacional" , "Ocupacional" ),
        ( "Esportivo" , "Esportivo" ),
        ( "Cultural" , "Cultural" ),
        ( "Crença/Religião" , "Crença/Religião" ),
        ( "Lazer" , "Lazer" ),
        ( "Outros" , "Outros" ),
 
    )
    unidade = models.ForeignKey(Unidade, on_delete=models.SET_NULL, null=True)
    cronograma = models.ForeignKey(Cronograma, on_delete=models.SET_NULL, null=True)
    nome = models.CharField(max_length=35)
    tipo_atividade = models.CharField(max_length=45, choices=TIPO_ATIVIDADE, default="Outros")
    responsavel = models.CharField(max_length=35, null=True, blank=True)
    carga_horaria = models.IntegerField(default=12, null=True, blank=True)
    horario_inicio = models.TimeField(default=time(7, 00), null=True, blank=True)
    horario_fim = models.TimeField(default = time(19, 00), null=True, blank=True)
    
    def __str__(self):
        return f"{self.nome} - {self.cronograma}"

    @property
    def lista_efetivos(self):
        return list(self.efetivodiario_set.order_by('dia').values_list('efetivo',flat=True))

    @property
    def horario(self):
        return f"{self.horario_inicio.strftime(f'%Hh')} às {self.horario_fim.strftime(f'%Hh')}"

    @property
    def quantidade_de_dias(self):
        return len([i for i in self.lista_efetivos if i>0])
    @property
    def total_voluntarios(self):
        return sum(self.lista_efetivos)
    @property
    def total_cotas(self):
        return (self.total_voluntarios * self.carga_horaria)/12
    @property
    def voluntarios_dia(self):
        if self.quantidade_de_dias <= 0:
            return 0
        return sum(self.lista_efetivos)/self.quantidade_de_dias
    class Meta:
        ordering = ["id"]


#Nao permitir criação ou deleção, são basicamente parte do model Atividade
#edicao verifica cronograma
class EfetivoDiario(models.Model):
    atividade = models.ForeignKey(Atividade, on_delete=models.CASCADE)
    dia = models.DateField(blank=False)
    efetivo = models.IntegerField(default=0)

    def __str__(self):
        return f"{self.atividade.unidade.sigla}-{self.atividade.nome}-{self.dia.strftime(f'%d/%m/%Y')} {self.efetivo} vagas"

    class Meta:
        verbose_name_plural = "Efetivos Diários"
        ordering = ["dia"]


class Vaga(models.Model):
    generator = models.ForeignKey(EfetivoDiario, null=True, blank=True, on_delete=models.CASCADE)    
    unidade = models.ForeignKey(Unidade, on_delete=models.CASCADE)
    dia = models.DateField()
    horario = models.CharField(max_length=100, null=True, blank=True)
    atividade = models.CharField(max_length=255, null=True, blank=True)
    tipo_atividade = models.CharField(max_length=45, choices=Atividade.TIPO_ATIVIDADE, default="Outros")
    responsavel = models.CharField(max_length=100, null=True, blank=True)
    carga_horaria = models.IntegerField(default=12)


    class Meta:
        ordering = ["dia", 'unidade', 'atividade']
