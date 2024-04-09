from django.contrib.auth.models import BaseUserManager
from django.core.exceptions import ValidationError
from django.core.validators import validate_email

class UserManager(BaseUserManager):
    def email_validator(self, email):
        try:
            validate_email(email)
        except ValidationError:
            raise ValueError('Por favor, entre com um endereço de e-mail válido')
        
    def create_user(self, cpf, first_name, last_name, email, password, triage_type=None, **extra_fields):
        if email:
            email=self.normalize_email(email)
            self.email_validator(email)
        else:
            raise ValueError('É necessário um endereço de e-mail')
        
        if not cpf:
            raise ValueError('É necessário o CPF') 
        
        if not first_name:
            raise ValueError('É necessário o primeiro nome')
        
        if not last_name:
            raise ValueError('É necessário o último nome')
        
        user = self.model(cpf=cpf, first_name=first_name, last_name=last_name, email=email, triage_type=triage_type, **extra_fields)
        user.set_password(password)
        user.save(using=self._db)

        return user
    
    def create_superuser(self, cpf, first_name, last_name, email, password, triage_type=None, **extra_fields):
        extra_fields.setdefault('is_staff', True)
        extra_fields.setdefault('is_superuser', True)
        extra_fields.setdefault('is_verified', True)

        if extra_fields.get('is_staff') is not True:
            raise ValueError('este campo deve estar habilitado para o usuário coordenador')
        
        if extra_fields.get('is_superuser') is not True:
            raise ValueError('este campo deve estar habilitado para o usuário master')
        
        user = self.create_user(cpf, first_name, last_name, email, password, triage_type=triage_type, **extra_fields)

        return user
