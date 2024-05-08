from django.db import models
from django.utils import timezone
from django.core.validators import RegexValidator
import uuid
from django.conf import settings

class Triage(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    number_of_process = models.CharField(max_length=25,
                                         unique=True,
                                         validators=[
                                            RegexValidator(
                                                regex=r'^\d{7}-\d{2}\.\d{4}\.\d\.\d{2}\.\d{4}$',
                                                message=r'O número do processo deve estar no formato ^\d{7}-\d{2}\.\d{4}\.\d\.\d{2}\.\d{4}$',
                                                code='invalid_number_of_process'
                                            )
                                         ])
    
    class TypeOfJustice(models.TextChoices):
        JEC = 'JEC'
        COMMON_CIVIL = 'CIVEL COMUM'
        LABOR = 'TRABALHISTA'
        FEDERAL = 'FEDERAL'
        CRIMINAL = 'CRIMINAL'
        TAX_ENFORCEMENT = 'EXECUÇÃO FISCAL'
        ACPS = 'ACPs'

    class TypeOfFine(models.TextChoices):
        DAILY = 'DIÁRIA'
        ONLY = 'ÚNICA'
        HOURS = 'POR HORA'
        BY_ACTS = 'POR ATOS'
    
    class ReceiveBy(models.TextChoices):
        EMAIL = 'E-MAIL'
        ESAJ = 'ESAJ'
        PJE = 'PJE'
        PJE_RJ = 'PJE-RJ'
        SALESFORCE = 'SALESFORCE'
        RDS = 'RDs'
        DISTRIBUTED = 'DISTRIBUÍDOS'
        ROBO = 'ROBÔ'
        OTHERS = 'OUTROS'

    class PreliminarySituation(models.TextChoices):
        GRANTED = 'DEFERIDO'
        REJECTED = 'INDEFERIDO'
        UNAPPRECIATED = 'NÃO APRECIADA'
        QUOTE = 'CITAÇÃO / INTIMAÇÃO'
        ENFORCEMENT_OF_SENTENCE = 'CUMPRIMENTO DE SENTEÇA'

    class ProceduralStage(models.TextChoices):
        JOINED = 'INGRESSADOS'
        LOOSE = 'AVULSO'

    arrival_date = models.DateField(blank=True, null=True)
    arrival_time = models.TimeField(blank=True, null=True)
    type_of_justice = models.CharField(choices=TypeOfJustice.choices, null=False)
    receive_by = models.CharField(choices=ReceiveBy.choices, null=False)
    date_time_of_treaty = models.DateTimeField(default=timezone.now, null=False)
    author = models.CharField(max_length=255, null=False)
    hearing_date = models.DateField(blank=True, null=True)
    hearing_time = models.TimeField(blank=True, null=True)
    preliminary_situation = models.CharField(choices=PreliminarySituation.choices, null=False)
    procedural_stage = models.CharField(choices=ProceduralStage.choices, null=False)
    fatal_deadline = models.DateTimeField(blank=True, null=True)
    obligation_to_do = models.TextField(max_length=400, null=True, blank=True)
    traffic_ticket = models.BooleanField(null=False)
    value_of_the_fine = models.DecimalField(max_digits=10, decimal_places=2, blank=True, null=True)
    type_of_fine = models.CharField(choices=TypeOfFine.choices, max_length=255, null=True, blank=True)
    judicial_determination = models.CharField(max_length=255, null=True, blank=True)

    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name='triages')

    def __str__(self):
        return self.number_of_process

    def remaining_time(self):
        now = timezone.now()

        if self.fatal_deadline:
            delta = self.fatal_deadline - now

            if delta.total_seconds() < 0:
                return 'Prazo fatal já passou'
            else:
                days = delta.days
                hours, remainder = divmod(delta.seconds, 3600)
                minutes, _ = divmod(remainder, 60)
                
                return f'{days} dia(s) :{hours} hora(s) :{minutes} minuto(s)'
        else:
            return None

    def save(self, *args, **kwargs):
        self.judicial_determination = self.remaining_time()
        super().save(*args, **kwargs)

class RioDeJaneiro(Triage):
    cpf_cnpj = models.CharField(
        max_length=20,
        null=False,
        validators=[
            RegexValidator(
                regex=r'^\d{3}\.\d{3}\.\d{3}-\d{2}$|^\d{2}\.\d{3}\.\d{3}/\d{4}-\d{2}$',
                message='O CPF ou CNPJ deve estar no formato correto.',
                code='invalid_cpf_cnpj'
            )
        ])

class Ceara(Triage):
    cpf_cnpj = models.CharField(
        max_length=20,
        null=False,
        validators=[
            RegexValidator(
                regex=r'^\d{3}\.\d{3}\.\d{3}-\d{2}$|^\d{2}\.\d{3}\.\d{3}/\d{4}-\d{2}$',
                message='O CPF ou CNPJ deve estar no formato correto.',
                code='invalid_cpf_cnpj'
            )
        ])

class SaoPaulo(Triage):
    quantity = models.IntegerField(null=True, blank=True)
    stamp_date = models.DateField(null=True, blank=True)
    internal_code = models.IntegerField(null=False)
    value_of_the_claim = models.DecimalField(max_digits=10, decimal_places=2, null=True, blank=True)
