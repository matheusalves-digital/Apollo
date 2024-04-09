from django.db import models
from django.contrib.auth.models import AbstractBaseUser, PermissionsMixin
import uuid
from django.conf import settings
from rest_framework_simplejwt.tokens import RefreshToken
from .manager import UserManager
from django.core.validators import RegexValidator

class User(AbstractBaseUser, PermissionsMixin):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, null=False, blank=True)
    cpf = models.CharField(unique=True, max_length=11, null=False)
    first_name = models.CharField(max_length=100, null=False)
    last_name = models.CharField(max_length=100, null=False)
    
    email_regex = RegexValidator(
        regex=r'^[\w\.-]+@meirelesefreitas(?:\.adv\.br)+$',
        message="O e-mail deve estar no formato nomesobrenome@meirelesefreitas.adv.br",
    )

    email = models.EmailField(unique=True, max_length=255, null=False, validators=[email_regex])

    is_active = models.BooleanField(default=True)

    is_staff = models.BooleanField(default=False)
    is_superuser = models.BooleanField(default=False)
    is_verified = models.BooleanField(default=False)

    date_joined = models.DateTimeField(auto_now_add=True)
    last_login = models.DateTimeField(auto_now=True)

    triage_type = models.CharField(max_length=20, null=True, blank=True)

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = ['first_name', 'last_name']

    objects = UserManager()

    def __str__(self):
        return self.email

    @property
    def get_full_name(self):
        return f'{self.first_name} {self.last_name}'
    
    def tokens(self):
        refresh = RefreshToken.for_user(self)

        return {
            'refresh':str(refresh),
            'access':str(refresh.access_token)
        }

class OneTimePassword(models.Model):
    user = models.OneToOneField(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    code = models.CharField(max_length=6, unique=True)

    def __str__(self):
        return f'{self.user.get_full_name()} - passcode'
