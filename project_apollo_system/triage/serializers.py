from rest_framework import serializers
from .models import Triage, RioDeJaneiro, Ceara, SaoPaulo
from rest_framework.exceptions import ValidationError


FIELDS_RIODEJANEIRO_CEARA = [
    'id',
    'number_of_process',
    'arrival_date',
    'arrival_time',
    'type_of_justice',
    'receive_by',
    'author',
    'cpf_cnpj',
    'hearing_date',
    'hearing_time',
    'preliminary_situation',
    'procedural_stage',
    'fatal_deadline',
    'traffic_ticket',
    'value_of_the_fine',
    'type_of_fine',
    'judicial_determination',
    'obligation_to_do',
    'user'
]

FIELDS_SAOPAULO = [
    'id',
    'number_of_process',
    'arrival_date',
    'arrival_time',
    'type_of_justice',
    'receive_by',
    'author',
    'hearing_date',
    'hearing_time',
    'preliminary_situation',
    'procedural_stage',
    'fatal_deadline',
    'traffic_ticket',
    'value_of_the_fine',
    'type_of_fine',
    'judicial_determination',
    'obligation_to_do',
    'quantity',
    'stamp_date',
    'internal_code',
    'value_of_the_claim',
    'user'
]


class TriageSerializer(serializers.ModelSerializer):
    class Meta:
        model = Triage
        fields = '__all__'

    def validate_number_of_process(self, value):
        print("Validating number of process:", value)
        existing_triage = Triage.objects.filter(number_of_process=value).first()
        
        if existing_triage:
            print("Process number exists, raised by:", existing_triage.user.get_full_name())
            
            raise ValidationError(f'Este processo já foi cadastrado por {existing_triage.user.get_full_name()}.')
        
        return value

class RioDeJaneiroSerializer(serializers.ModelSerializer):
    class Meta:
        model = RioDeJaneiro
        fields = FIELDS_RIODEJANEIRO_CEARA

class CearaSerializer(serializers.ModelSerializer):
    class Meta:
        model = Ceara
        fields = FIELDS_RIODEJANEIRO_CEARA

class SaoPauloSerializer(serializers.ModelSerializer):
    class Meta:
        model = SaoPaulo
        fields = FIELDS_SAOPAULO
