from django.shortcuts import render, redirect
from django.contrib.auth.models import User
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm
from django.contrib.auth import login, logout
from django.contrib.auth.models import Group
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from .forms import CustomRegisterForm
from .models import Profile
from django.http import HttpResponse

# Головна сторінка
def home(request):
    return render(request, 'home.html')

# Реєстрація
def register_view(request):
    if request.method == 'POST':
        form = CustomRegisterForm(request.POST)
        if form.is_valid():
            # Створюємо об’єкт користувача
            user = User.objects.create_user(
                username=form.cleaned_data['username'],
                password=form.cleaned_data['password'],
            )

            # Зберігаємо ім’я і прізвище
            user.first_name = form.cleaned_data['first_name']
            user.last_name = form.cleaned_data['last_name']
            user.save()

            # Створюємо запис профілю з групою
            Profile.objects.create(
                user=user,
                first_name=form.cleaned_data['first_name'],
                last_name=form.cleaned_data['last_name'],
                group=form.cleaned_data['group']
            )

            # Входимо автоматично
            login(request, user)
            return redirect('dashboard')
    else:
        form = CustomRegisterForm()

    return render(request, 'register.html', {'form': form})

# Вхід
def login_view(request):
    if request.method == 'POST':
        form = AuthenticationForm(data=request.POST)
        if form.is_valid():
            user = form.get_user()
            login(request, user)
            return redirect('dashboard')
    else:
        form = AuthenticationForm()
    return render(request, 'login.html', {'form': form})

# Вихід
def logout_view(request):
    logout(request)
    return redirect('home')

# Особистий кабінет — показує залежно від ролі
def dashboard_view(request):
    if not request.user.is_authenticated:
        return redirect('login')

    # Отримуємо всі групи користувача
    groups = request.user.groups.all()

    if groups:
        role = groups[0].name  # Припустимо, що лише одна роль
    else:
        role = 'без ролі'

    return render(request, 'dashboard.html', {'role': role})

@login_required
def edit_profile_view(request):
    if request.method == 'POST':
        user = request.user
        user.first_name = request.POST.get('first_name')
        user.last_name = request.POST.get('last_name')
        user.email = request.POST.get('email')
        user.save()
        messages.success(request, 'Профіль оновлено успішно!')
        return redirect('edit_profile')
    
    return render(request, 'edit_profile.html')