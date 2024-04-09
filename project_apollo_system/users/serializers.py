from rest_framework import serializers
from .models import User
from django.contrib.auth import authenticate
from rest_framework.exceptions import AuthenticationFailed
import uuid
from rest_framework_simplejwt.tokens import RefreshToken, TokenError


class UserRegisterSerializer(serializers.ModelSerializer):
    password = serializers.CharField(max_length=68, min_length=6, write_only=True)
    password2 = serializers.CharField(max_length=68, min_length=6, write_only=True)

    class Meta:
        model = User
        fields = ['cpf', 'first_name', 'last_name', 'email', 'triage_type', 'password', 'password2']

    def validate(self, attrs):
        password = attrs.get('password', '')
        password2 = attrs.get('password2', '')

        if password != password2:
            raise serializers.ValidationError('As senhas não correspondem')

        return attrs
    
    def create(self, validated_data):
        user = User.objects.create_user(
            cpf=validated_data.get('cpf'),
            first_name=validated_data.get('first_name'),
            last_name=validated_data.get('last_name'),
            email=validated_data['email'],
            triage_type=validated_data.get('triage_type'),
            password=validated_data.get('password')
        )

        return user
    
class LoginSerializer(serializers.ModelSerializer):
    id = serializers.UUIDField(default=uuid.uuid4)
    email = serializers.EmailField(max_length=255)
    password = serializers.CharField(max_length=68, write_only=True)
    full_name = serializers.CharField(max_length=255, read_only=True)
    triage_type = serializers.CharField(max_length=255, read_only=True)
    access_token = serializers.CharField(max_length=255, read_only=True)
    refresh_token = serializers.CharField(max_length=255, read_only=True)
    
    class Meta:
        model = User
        fields = ['id', 'email', 'password', 'full_name', 'triage_type', 'access_token', 'refresh_token']

    def validate(self, attrs):
        email = attrs.get('email')
        password = attrs.get('password')
        request = self.context.get('request')

        user = authenticate(request, email=email, password=password)

        if not user:
            raise AuthenticationFailed('credenciais inválidas, tente novamente')
        
        if not user.is_verified:
            raise AuthenticationFailed('O e-mail não é verificado')
        
        user_tokens = user.tokens()

        return {
            'id':user.id,
            'email':user.email,
            'full_name':user.get_full_name,
            'triage_type':user.triage_type,
            'access_token':str(user_tokens.get('access')),
            'refresh_token':str(user_tokens.get('refresh'))
        }

class LogoutUserSerializer(serializers.Serializer):
    refresh_token = serializers.CharField()

    default_error_messages = {
        'bad_token':('O token é inválido ou já expirou')
    }

    def validate(self, attrs):
        self.token = attrs.get('refresh_token')

        return attrs
    
    def save(self, **kwargs):
        try:
            token = RefreshToken(self.token)
            token.blacklist()

        except TokenError:
            return self.fail('bad_token')
