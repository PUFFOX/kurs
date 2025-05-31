from django.shortcuts import render, redirect
# render() — показує HTML-шаблон і передає туди змінні
# redirect() — перекидає користувача на іншу сторінку

from django.contrib.auth.models import User
# Імпортуємо стандартну модель користувача Django (auth_user у базі)

from django.contrib.auth.forms import UserCreationForm, AuthenticationForm
# UserCreationForm — готова форма для реєстрації
# AuthenticationForm — готова форма для входу

from django.contrib.auth import login, logout
# login() — вхід користувача (створює сесію)
# logout() — вихід (видаляє сесію)


from django.contrib.auth.models import Group
# Імпортуємо групи ролей, які ми створювали (курсант, журналіст…)

from django.contrib.auth.decorators import login_required
# Декоратор, який захищає сторінку — якщо користувач не залогінений, його перекине на логін

from django.contrib import messages
# Щоб виводити повідомлення успіху або помилки після змін

from .forms import CustomRegisterForm
# Наша власна форма реєстрації (логін, пароль, ім’я, прізвище, група)

from .models import Profile
# Наша модель профілю — розширення користувача

from django.http import HttpResponse
# Простий спосіб повернути текст (ми його тут не використовуємо — можна прибрати)

from django.shortcuts import render, get_object_or_404
# get_object_or_404() — отримує об’єкт або повертає 404, якщо не знайдено
# Це зручно, щоб не писати окремий код для перевірки наявності об’єкта
# Імпортуємо наші моделі та форми, які ми створили в accounts/models.py і accounts/forms.py

from utils.roles import user_can
# Імпортуємо функцію user_can, яка перевіряє права користувача
# Цей файл містить всі наші в'юхи (views) — функції, які обробляють запити користувачів
# Імпортуємо наші моделі та форми, які ми створили в accounts/models.py і accounts/forms.py

from django.contrib.auth.decorators import login_required
# Імпортуємо декоратор login_required, щоб захистити деякі сторінки від незалогінених користувачів
# Цей файл містить всі наші в'юхи (views) — функції, які обробляють запити користувачів





# Головна сторінка
def home(request):
    return render(request, 'home.html')
# home.html — головна сторінка, де можна розмістити привітання або інформацію про сайт
# Якщо користувач не залогінений, він побачить цю сторінку
# Коли користувач заходить на / → віддаємо йому шаблон home.html


# Реєстрація
def register_view(request):
    if request.method == 'POST':
        form = CustomRegisterForm(request.POST)
        # Якщо користувач натиснув "Зареєструватися", приходить POST
        # Отримуємо дані з форми
        # Якщо форма валідна, створюємо користувача
        # і профіль, а потім автоматично входимо
        # Якщо форма не валідна, повертаємо назад з помилками
        # Створюємо форму й передаємо в неї дані, які ввів користувач


        if form.is_valid(): #Перевіряємо, чи всі поля форми заповнені коректно
            # Створюємо об’єкт користувача
            # Використовуємо UserCreationForm для створення користувача
            # Використовуємо метод create_user, щоб зберегти пароль у хешованому вигляді
            # Створюємо користувача з логіном і паролем
            # Використовуємо дані з форми
            user = User.objects.create_user(
                username=form.cleaned_data['username'],
                password=form.cleaned_data['password'],
            )
            # Створюємо нового користувача (User — стандартна таблиця Django)

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
    else: # Якщо це не POST, а звичайний вхід на сторінку — просто показуємо пусту форму
        form = CustomRegisterForm()

    # Повертаємо шаблон реєстрації з формою
    return render(request, 'register.html', {'form': form})

# Вхід
def login_view(request):
    if request.method == 'POST':
        form = AuthenticationForm(data=request.POST)
        # Якщо користувач натиснув "Увійти", приходить POST
        # Отримуємо дані з форми входу
        # Використовуємо AuthenticationForm для перевірки логіна і пароля
        # Якщо форма валідна, виконуємо вхід
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
# Виходить із сайту (видаляється сесія)
# Перекидає на головну сторінку після виходу


# Особистий кабінет — показує залежно від ролі
def dashboard_view(request):
    if not request.user.is_authenticated:
        return redirect('login')

    groups = request.user.groups.all()
    role = groups[0].name if groups else None

    if role == "Курсант":
        return redirect('kursant_dashboard')
    elif role == "Журналіст":
        return redirect('journalist_dashboard')
    elif role == "Командир":
        return redirect('commander_dashboard')
    elif role == "Начальник курсу":
        return redirect('chief_dashboard')
    else:
        return HttpResponse("⛔ Роль не визначена або немає доступу.")




# Редагування профілю
@login_required
def edit_profile_view(request):# Ця сторінка доступна лише залогіненим користувачам
    if request.method == 'POST':
        user = request.user
        user.first_name = request.POST.get('first_name')
        user.last_name = request.POST.get('last_name')
        user.email = request.POST.get('email')
        user.save()
        # Зберігаємо зміни в користувача
        messages.success(request, 'Профіль оновлено успішно!')
        return redirect('edit_profile')
    # Якщо це POST-запит, оновлюємо дані користувача
    
    return render(request, 'edit_profile.html')
# Якщо це GET-запит, показуємо форму редагування профілю


def my_group_view(request):
    if not user_can(request.user, 'view_group'):
        return HttpResponse("⛔ Вам не дозволено переглядати групу.")

    group = request.user.profile.group
    kursants = Profile.objects.filter(group=group)
    return render(request, 'my_group.html', {'kursants': kursants})



def kursant_detail_view(request, user_id):
    # Шукаємо користувача з таким ID або повертаємо помилку 404
    user = get_object_or_404(User, id=user_id)

    # Дістаємо профіль цього користувача (там є ім'я, прізвище, група)
    profile = get_object_or_404(Profile, user=user)

    # Передаємо дані в шаблон
    return render(request, 'kursant_detail.html', {
        'user_obj': user,
        'profile': profile
    })


@login_required
def kursant_dashboard(request):
    # Отримай оцінки, рейтинг тощо для курсанта
    context = {
        'role': 'Курсант',
        'grades': [],  # TODO: отримай реальні оцінки з моделі
    }
    return render(request, 'dashboards/kursant.html', context)


@login_required
def journalist_dashboard(request):
    # Отримай групу журналіста і доступні функції (редагування оцінок)
    context = {
        'role': 'Журналіст',
    }
    return render(request, 'dashboards/journalist.html', context)


@login_required
def commander_dashboard(request):
    # Доступ до нарядів, звільнень, рейтингу групи
    context = {
        'role': 'Командир',
    }
    return render(request, 'dashboards/commander.html', context)


@login_required
def chief_dashboard(request):
    # Начальник бачить все, але тільки для перегляду
    context = {
        'role': 'Начальник курсу',
    }
    return render(request, 'dashboards/chief.html', context)

