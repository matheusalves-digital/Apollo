from django.urls import path
from .views import RegisterUserView, VerifyUserEmail, LoginUserView, TestAuthenticationView, LogoutUserView

urlpatterns = [
    path('register/', RegisterUserView.as_view(), name='register'),
    path('verify-email/', VerifyUserEmail.as_view(), name='verify'),
    path('login/', LoginUserView.as_view(), name='login'),
    path('profile/', TestAuthenticationView.as_view(), name='granted'),
    path('logout/', LogoutUserView.as_view(), name='logout'),
]
