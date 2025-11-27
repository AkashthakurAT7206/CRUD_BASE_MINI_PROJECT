from django.shortcuts import render
from django.contrib.auth.mixins import LoginRequiredMixin
# Create your views here.
from django.views import View
from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth import get_user_model
from django.contrib import messages
from django.utils import timezone
from django.core.mail import send_mail
from django.utils.http import url_has_allowed_host_and_scheme
import random
from products.models import Category

from .models import PasswordResetOTP, FeedBack, UserAddress
from .forms import (
    RegisterForm,
    LoginForm,
    ForgotPasswordForm,
    OTPForm,
    ResetPasswordForm,
    FeedbackForm,
    UserAddressForm,
)

User = get_user_model()


def home(request):
    # Show home page with categories for all users
    categories = Category.objects.filter(is_active=True)[:4]
    return render(request, 'Accounts/home.html', {'categories': categories})

class RegisterView(View):
    template_name = 'Accounts/register.html'

    def get(self, request):
        return render(request, self.template_name)

    def post(self, request):
        username = request.POST.get('username')
        email = request.POST.get('email')
        password1 = request.POST.get('password1')
        password2 = request.POST.get('password2')

        # 🔹 1. Validate passwords
        if password1 != password2:
            messages.error(request, "Passwords do not match.")
            return redirect('register')

        # 🔹 2. Check username/email existence
        if User.objects.filter(username=username).exists():
            messages.error(request, "Username already exists.")
            return redirect('register')

        if User.objects.filter(email=email).exists():
            messages.error(request, "Email already registered.")
            return redirect('register')

        # 🔹 3. Create user
        user = User.objects.create_user(username=username, email=email, password=password1)
        user.save()

        messages.success(request, "Account created successfully! Please log in.")
        return redirect('login')
# class RegisterView(View):
#     template_name = 'Accounts/register.html'

#     def get(self, request):
#         return render(request, self.template_name, {'form': RegisterForm()})

#     def post(self, request):
#         form = RegisterForm(request.POST)
#         if form.is_valid():
#             form.save()
#             messages.success(request, 'Account created successfully!')
#             return redirect('login')
#         messages.error(request, 'Please correct the errors below.')
#         return render(request, self.template_name, {'form': form})


# class LoginView(View):
#     template_name = 'Accounts/login.html'

#     def get(self, request):
#         return render(request, self.template_name, {'form': LoginForm()})

#     def post(self, request):
#         form = LoginForm(request.POST)
#         if form.is_valid():
#             username = form.cleaned_data['username']
#             password = form.cleaned_data['password']
#             user = authenticate(request, username=username, password=password)
#             if user:
#                 login(request, user)
#                 return redirect('home')
#             else:
#                 messages.error(request, 'Invalid username or password.')
#         return render(request, self.template_name, {'form': form})


class LoginView(View):
    template_name = 'Accounts/login.html'

    def get(self, request):
        return render(request, self.template_name, {'form': LoginForm()})

    def post(self, request):
        form = LoginForm(request.POST)
        if form.is_valid():
            username = form.cleaned_data['username']
            password = form.cleaned_data['password']

            # Ensure we have a session and remember the pre-login anonymous session key
            if not request.session.session_key:
                request.session.create()
            # Store pre-login session key so signal can merge that cart after login (session rotates)
            request.session['anon_cart_session_key'] = request.session.session_key

            user = authenticate(request, username=username, password=password)
            if user:
                login(request, user)
                return redirect('home')
            else:
                messages.error(request, 'Invalid username or password.')
        return render(request, self.template_name, {'form': form})



class LogoutView(View):
    def get(self, request):
        logout(request)
        return redirect('login')


class ForgotPasswordView(View):
    template_name = 'Accounts/forgot_password.html'

    def get(self, request):
        return render(request, self.template_name, {'form': ForgotPasswordForm()})

    def post(self, request):
        form = ForgotPasswordForm(request.POST)
        if form.is_valid():
            email = form.cleaned_data['email']
            try:
                user = User.objects.get(email=email)
                otp = str(random.randint(100000, 999999))
                PasswordResetOTP.objects.create(user=user, otp=otp)

                send_mail(
                    'Your OTP for Password Reset',
                    f'Your OTP is {otp}',
                    None,
                    [email],
                    fail_silently=False,
                )

                request.session['email'] = email
                messages.success(request, 'OTP sent to your email.')
                return redirect('verify_otp')
            except User.DoesNotExist:
                messages.error(request, 'Email not found.')
        return render(request, self.template_name, {'form': form})


class VerifyOTPView(View):
    template_name = 'Accounts/verify_otp.html'

    def get(self, request):
        return render(request, self.template_name, {'form': OTPForm()})

    def post(self, request):
        form = OTPForm(request.POST)
        email = request.session.get('email')
        if not email:
            messages.error(request, 'Session expired. Please try again.')
            return redirect('forgot_password')

        if form.is_valid():
            otp = form.cleaned_data['otp']
            try:
                user = User.objects.get(email=email)
                record = PasswordResetOTP.objects.filter(user=user, otp=otp).last()
                if record and timezone.now() - record.created_at < timezone.timedelta(minutes=5):
                    record.delete()
                    request.session['verified_email'] = email
                    messages.success(request, 'OTP verified. Reset your password.')
                    return redirect('reset_password')
                else:
                    messages.error(request, 'Invalid or expired OTP.')
            except User.DoesNotExist:
                messages.error(request, 'Email not found.')
        return render(request, self.template_name, {'form': form})


class ResetPasswordView(View):
    template_name = 'Accounts/reset_password.html'

    def get(self, request):
        return render(request, self.template_name, {'form': ResetPasswordForm()})

    def post(self, request):
        form = ResetPasswordForm(request.POST)
        email = request.session.get('verified_email')
        if not email:
            messages.error(request, 'Session expired. Please start again.')
            return redirect('forgot_password')

        if form.is_valid():
            password1 = form.cleaned_data['password1']
            password2 = form.cleaned_data['password2']
            if password1 != password2:
                messages.error(request, 'Passwords do not match.')
                return redirect('reset_password')

            try:
                user = User.objects.get(email=email)
                user.set_password(password1)
                user.save()
                messages.success(request, 'Password reset successful! You can now login.')
                del request.session['verified_email']
                return redirect('login')
            except User.DoesNotExist:
                messages.error(request, 'User not found.')
        return render(request, self.template_name, {'form': form})


class ProfileView(LoginRequiredMixin, View):
    template_name = 'Accounts/profile.html'

    def get(self, request):
        from cart.models import Cart, CartItem
        
        # Get user's cart information
        try:
            cart = Cart.objects.get(user=request.user)
            cart_items = CartItem.objects.filter(cart=cart)
            cart_item_count = cart_items.count()
            cart_total = cart.get_total_price()
        except Cart.DoesNotExist:
            cart = None
            cart_item_count = 0
            cart_total = 0
        
        address = getattr(request.user, 'address', None)

        context = {
            'user': request.user,
            'cart': cart,
            'cart_item_count': cart_item_count,
            'cart_total': cart_total,
            'address': address,
        }
        return render(request, self.template_name, context)
    
    
class FeedbackView(LoginRequiredMixin, View):
    template_name = 'accounts/feedback.html'

    def get(self, request):
        return render(request, self.template_name, {'form': FeedbackForm()})

    def post(self, request):
        form = FeedbackForm(request.POST)
        if form.is_valid():
            feedback = form.save(commit=False)
            feedback.user = request.user   # attach logged-in user
            feedback.save()
            messages.success(request, 'Thank you for your feedback!')
            return redirect('profile')

        return render(request, self.template_name, {'form': form})


class AddressUpdateView(LoginRequiredMixin, View):
    template_name = 'Accounts/address_form.html'

    def get_next_url(self, request):
        next_url = request.POST.get('next') or request.GET.get('next')
        if next_url and url_has_allowed_host_and_scheme(next_url, allowed_hosts={request.get_host()}):
            return next_url
        return None

    def get(self, request):
        address = getattr(request.user, 'address', None)
        form = UserAddressForm(instance=address)
        context = {
            'form': form,
            'next': self.get_next_url(request),
        }
        return render(request, self.template_name, context)

    def post(self, request):
        address = getattr(request.user, 'address', None)
        form = UserAddressForm(request.POST, instance=address)

        if form.is_valid():
            user_address = form.save(commit=False)
            user_address.user = request.user
            user_address.save()
            messages.success(request, 'Address saved successfully.')
            next_url = self.get_next_url(request)
            if next_url:
                return redirect(next_url)
            return redirect('profile')

        context = {
            'form': form,
            'next': self.get_next_url(request),
        }
        return render(request, self.template_name, context)


