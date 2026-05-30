from config import settings
from django.contrib.auth.decorators import login_required
from django.shortcuts import render, redirect
from django.contrib.auth import login, authenticate, logout
from django.views import View
from accounts.forms import RegisterForm, LoginForm, User_profileForm, ResetPasswordForm, CodeForm, TotpForm
from accounts.models import VerificationCode, User
from common.service import thread_send_mail
import requests

def register(request):
    if request.method == 'POST':
        form = RegisterForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('login')
        return render(request, 'accounts/register.html', {'form': form})
    else:
        form = RegisterForm()
        return render(request, 'accounts/register.html', {'form': form})


def login_view(request):
    if request.method == 'POST':
        form = LoginForm(request.POST)
        if form.is_valid():
            user = form.cleaned_data.get('user')
            login(request, user)
            return redirect('games:game_list')
        return render(request, 'accounts/login.html', {'form': form})
    form = LoginForm()
    return render(request, 'accounts/login.html', {'form': form})

def logout_view(request):
    logout(request)
    return redirect('login')
@login_required
def profile(request):
    if request.method == 'GET':
        form = User_profileForm(instance=request.user)
        return render(request, 'accounts/profile.html', {'form': form})
    else:
        form = User_profileForm(request.POST, instance=request.user)
        if form.is_valid():
            form.save()
            return redirect('games:game_list')
        return render(request, 'accounts/profile.html', {'form': form})


class ForgotPassword(View):
    def get(self, request):
        form = ResetPasswordForm()
        return render(request, 'accounts/password_reset_form.html', {'form': form})

    def post(self, request):
        form = ResetPasswordForm(request.POST)
        if form.is_valid():
            email = form.cleaned_data.get('email')
            user = User.objects.filter(email=email).first()
            if user:
                code =  VerificationCode.objects.create(user=user, email=email)
                thread_send_mail(user, 'parolnitiklash ushun emailga xat', f'your code is {code.code}')
            return redirect('password_reset_done')
        return render(request, 'accounts/password_reset_form.html', {'form': form})


class ResetPasswordDone(View):
    def get(self, request):
        form = CodeForm()
        return render(request, 'accounts/password_code_verification.html', {'form': form})

    def post(self, request):
        form = CodeForm(request.POST)
        if form.is_valid():
            code = form.cleaned_data.get('code')
            password = form.cleaned_data.get('password')

            user = VerificationCode.objects.filter(code=code).first().user
            if user:
                VerificationCode.objects.filter(user=user).delete()
                user.set_password(password)
                user.save()
                return redirect('login')
            return render(request, 'accounts/password_code_verification.html', {'form': form})
        return render(request, 'accounts/password_code_verification.html', {'form': form})


def google_login_page(request):
    url = (f'{settings.GOOGLE_AUTH_URL}'
           f'?client_id={settings.GOOGLE_CLIENT_ID}'
           f'&redirect_uri={settings.GOOGLE_REDIRECT_URI}'
           f'&response_type=code'
           f'&scope=openid email profile')
    return redirect(url)


def google_login_callback(request):
    code = request.GET.get('code')
    token_data = {"code": code,
                  "client_id": settings.GOOGLE_CLIENT_ID,
                  "client_secret": settings.GOOGLE_CLIENT_SECRET,
                  "redirect_uri": settings.GOOGLE_REDIRECT_URI,
                  "grant_type": "authorization_code", }
    token = requests.post(
        settings.GOOGLE_TOKEN_URL, data=token_data
    ).json()
    print(token)
    access_token = token.get('access_token')

    # user_info = requests.get(
    #     settings.GOOGLE_USER_INFO_URL, headers={"Authorization": f"Bearer {access_token}"}
    # ).json()
    # print(user_info)
    return redirect('google_login_page')
    username = user_info.get('id') or user_info.get('email')  # Или другой fallback
    email = user_info.get('email')
    print('user id',user_info.get('id'))
    print(f"user information: {user_info}")
    user, created = User.objects.get_or_create(
        email=email,
        defaults={
            'first_name': user_info.get('given_name', ''),
            'last_name': user_info.get('family_name', ''),
            'username': username,
        }
    )
    if user.is_2fa_enabled:
        user.generate_totp_secret()
        thread_send_mail(user.email, 'totp', f'code : {user.totp_secret}')
        return redirect('verify_totp')
    login(request, user)
    return redirect('game:game_list')


def verify_totp(request):
    if request.method == 'POST':
        form = TotpForm(request.POST)
        if form.is_valid():
            code = form.cleaned_data.get('code')
            user = User.objects.get(totp_secret=code)
            login(request, user)
            return redirect('book_list')
        return render(request, 'accounts/totp.html', {'form': form})
    form = TotpForm()
    return render(request, 'accounts/totp.html', {'form': form})