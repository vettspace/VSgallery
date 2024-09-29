from django.contrib.auth import authenticate, login, logout
from django.shortcuts import redirect, render

from .forms import CustomAuthenticationForm, CustomUserCreationForm


def register(request):
    """Регистрация пользователя."""
    if request.method == 'POST':
        form = CustomUserCreationForm(request.POST)
        if form.is_valid():
            user = form.save()
            login(request, user)
            return redirect('homepage')
    else:
        form = CustomUserCreationForm()
    return render(request, 'accounts/register.html', {'form': form})


def user_login(request):
    """Авторизация пользователя."""
    if request.method == 'POST':
        form = CustomAuthenticationForm(request, data=request.POST)
        if form.is_valid():
            user = form.get_user()
            login(request, user)
            return redirect('homepage')
    else:
        form = CustomAuthenticationForm()
    return render(request, 'accounts/login.html', {'form': form})


def user_logout(request):
    """Выход пользователя."""
    logout(request)
    return redirect('homepage')
