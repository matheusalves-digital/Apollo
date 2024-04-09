from rest_framework import generics
from rest_framework.permissions import IsAuthenticated
from .models import Triage, RioDeJaneiro, Ceara, SaoPaulo
from .serializers import TriageSerializer, RioDeJaneiroSerializer, CearaSerializer, SaoPauloSerializer
from django.http import Http404
from rest_framework.response import Response

USER_TRIAGE_TYPE = {
    'RioDeJaneiro': {
        'serializer': RioDeJaneiroSerializer,
        'model': RioDeJaneiro
    }, 
    'Ceara': {
        'serializer': CearaSerializer,
        'model': Ceara
    },
    'SaoPaulo': {
        'serializer': SaoPauloSerializer,
        'model': SaoPaulo
    }
}

FIELDS_NOT_UPDATE = [
    'arrival_date',
    'arrival_time',
    'type_of_justice',
    'receive_by',
    'author',
    'cpf_cnpj'
]


class TriageCreateView(generics.CreateAPIView):
    permission_classes = [IsAuthenticated]

    def get_serializer_class(self):
        user_triage_type = self.request.user.triage_type
        serializer_class = USER_TRIAGE_TYPE.get(user_triage_type, {}).get('serializer', TriageSerializer)

        return serializer_class

    def perform_create(self, serializer):
        user = self.request.user
        return serializer.save(user=user)

class TriageListView(generics.ListAPIView):
    permission_classes = [IsAuthenticated]

    def get_serializer_class(self):
        user_triage_type = self.request.user.triage_type
        return USER_TRIAGE_TYPE[user_triage_type]['serializer']

    def get_queryset(self):
        user_triage_type = self.request.user.triage_type
        model = USER_TRIAGE_TYPE[user_triage_type]['model']
        return model.objects.filter(user=self.request.user)

class TriageDetailView(generics.RetrieveAPIView):
    queryset = Triage.objects.all()
    serializer_class = TriageSerializer
    permission_classes = [IsAuthenticated]

    def get_object(self):
        process_number = self.kwargs.get('pk')
        try:
            triage = Triage.objects.get(number_of_process=process_number)

            return triage
        except Triage.DoesNotExist:
            raise Http404('Triage not found')

class TriageUpdateView(generics.UpdateAPIView):
    permission_classes = [IsAuthenticated]

    def get_object(self):
        process_number = self.kwargs.get('pk')

        try:
            triage = Triage.objects.get(number_of_process=process_number)
    
            if triage.user != self.request.user:
                raise Http404()
            
            return triage
        
        except Triage.DoesNotExist:
            raise Http404('Triage not found')

    def get_serializer_class(self):
        user_triage_type = self.request.user.triage_type
        return USER_TRIAGE_TYPE[user_triage_type]['serializer']

    def update(self, request, *args, **kwargs):
        instance = self.get_object()
        serializer = self.get_serializer(instance, data=request.data, partial=True)
        serializer.is_valid(raise_exception=True)

        data = {key: value for key, value in serializer.validated_data.items() if key not in FIELDS_NOT_UPDATE}
        
        for key, value in data.items():
            setattr(instance, key, value)

        instance.save()

        return Response(serializer.data)
