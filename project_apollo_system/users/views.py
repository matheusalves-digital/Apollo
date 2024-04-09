from rest_framework.generics import GenericAPIView
from .serializers import UserRegisterSerializer, LogoutUserSerializer
from rest_framework.response import Response
from rest_framework import status
from .utils import send_code_to_user
from .models import OneTimePassword
from .serializers import LoginSerializer
from rest_framework.permissions import AllowAny
from rest_framework.permissions import IsAuthenticated

class RegisterUserView(GenericAPIView):
    serializer_class = UserRegisterSerializer

    def post(self, request):
        user_data = request.data
        serializer = self.serializer_class(data=user_data)

        if serializer.is_valid(raise_exception=True):
            serializer.save()
            user = serializer.data

            send_code_to_user(user['email'])
            
            print(user)

            return Response({
                'data': user,
                'message': f'Oi. Acesso com um passcode.'
            }, status=status.HTTP_201_CREATED)
        
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    
class VerifyUserEmail(GenericAPIView):
    permission_classes = [AllowAny]
    
    def post(self, request, *args, **kwargs):
        optcode = request.data.get('otp')

        try:
            user_code_obj = OneTimePassword.objects.get(code=optcode)
            user = user_code_obj.user

            if not user.is_verified:
                user.is_verified = True
                user.save()

                return Response({
                    'message':'Conta de e-mail verificada com sucesso'
                }, status=status.HTTP_200_OK)
            
            return Response({
                'message':'O código é inválido, o usuário já foi verificado'
            }, status=status.HTTP_204_NO_CONTENT)
        except OneTimePassword.DoesNotExist:
            return Response({
                'message':'Passcode não existe'
            }, status=status.HTTP_404_NOT_FOUND)
        
class LoginUserView(GenericAPIView):
    serializer_class = LoginSerializer

    def post(self, request):
        serializer = self.serializer_class(data=request.data, context={'request':request})
        serializer.is_valid(raise_exception=True)

        return Response(serializer.data, status=status.HTTP_200_OK)

class TestAuthenticationView(GenericAPIView):
    permission_classes = [IsAuthenticated]

    def get(self, request):
        data={
            'msg':'funcionando'
        }

        return Response(data, status=status.HTTP_200_OK)

class LogoutUserView(GenericAPIView):
    serializer_class = LogoutUserSerializer
    permission_classes = [IsAuthenticated]

    def post(self, request):
        serializer = self.serializer_class(data=request.data)
        serializer.is_valid(raise_exception=True)
        serializer.save()

        return Response(status=status.HTTP_204_NO_CONTENT)
