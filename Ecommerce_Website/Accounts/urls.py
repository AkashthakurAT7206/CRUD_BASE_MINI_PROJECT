from django.urls import path
from .views import *

urlpatterns = [
    path('', home, name='home'),
    path('register/', RegisterView.as_view(), name='register'),
    path('login/', LoginView.as_view(), name='login'),
    path('logout/', LogoutView.as_view(), name='logout'),
    path('forgot-password/', ForgotPasswordView.as_view(), name='forgot_password'),
    path('verify-otp/', VerifyOTPView.as_view(), name='verify_otp'),
    path('reset-password/', ResetPasswordView.as_view(), name='reset_password'),
    path('profile/', ProfileView.as_view(), name='profile'),
    path('feedback/', FeedbackView.as_view(), name='feedback'),
    path('address/', AddressUpdateView.as_view(), name='address_update'),
]
