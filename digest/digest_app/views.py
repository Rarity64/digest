from django.shortcuts import render, redirect, get_object_or_404
from .parsings.common_interface import get_news
from django.contrib.auth import login, logout, authenticate, update_session_auth_hash
from django.http import JsonResponse, HttpResponse
from django.core.mail import send_mail
from django.contrib.auth.models import User
from .models import UserProfile, EmailDigest, EmailCode
from django.core.exceptions import ValidationError, ObjectDoesNotExist
import random
import threading

def index(request):
    #news = get_news()
    #print(news)
    try:
        if request.user.is_authenticated:
            context = { 'username' : request.user.username }
            return render(request, 'index.html', context)
        else:
            return render(request, 'index.html')
    except AttributeError:
        return render(request, 'index.html')

def auth(request):
    if request.method == 'POST':
        username = request.POST.get('email')
        password = request.POST.get('password')

        user = authenticate(request, username=username, password=password)
        if user is not None:
            print('Нашелся пользователь ', user.username)
            login(request, user)
            return JsonResponse({'status' : 'success', 'message' : 'Пользователь авторизован'})
        else:
            return JsonResponse({'status' : 'error', 'message' : 'Неправильный адрес электронной почты или пароль'}, status=400)

    if request.user.is_authenticated:
        return redirect('index')
    else:
        return render(request, 'auth.html')
    
def send_email_code_async(email, code):
    send_mail(
        'Дайджест новостей: код подтверждения',
        f'Ваш код подтверждения: {code}',
        'edsuyargulov@yandex.ru',
        [email],
        fail_silently=False,
    )

def reg(request):
    if request.method == 'POST':
        email = request.POST.get('email')
        password = request.POST.get('password')
        first_name = request.POST.get('firstName')
        last_name = request.POST.get('lastName')
        birthdate = request.POST.get('birthdate')

        user = User.objects.create_user(
            username = email, 
            email = email, 
            password = password, 
            first_name = first_name, 
            last_name = last_name,
            is_active = False
        )

        UserProfile.objects.create(
            user = user, 
            birthdate = birthdate
        )

        code = str(random.randint(100000, 999999))

        EmailCode.objects.create(
            user = user,
            code = code
        )

        threading.Thread(
            target=send_email_code_async,
            args=(email, code)
        ).start()        

        request.session['pending_user_id'] = user.id
        return JsonResponse({
            'status': 'success',
            'redirect': '/confirm/'
        })

    if request.user.is_authenticated:
        return redirect('index')
    else:
        return render(request, 'reg.html')
    
def confirm(request):
    if request.method == 'POST':
        code = request.POST.get('email-code')
        user_id = request.session.get('pending_user_id')

        if user_id:
            try:
                user = User.objects.get(id = user_id)
                email_code = EmailCode.objects.get(user = user, code = code)

                if email_code.code == code:
                    if not email_code.is_expired():
                        user.is_active = True
                        user.save()
                        email_code.delete()
                        login(request, user)
                        return JsonResponse({'status' : 'success', 'redirect' : '/account/'})
                    else:
                        return JsonResponse({'status': 'error', 'message': 'Срок действия кода истек'}, status=400)
            except ObjectDoesNotExist:
                return JsonResponse({'status': 'error', 'message': 'Неверный код'}, status=400)

    return render(request, 'confirm.html')

def logout_view(request):
    if request.user.is_authenticated:
        logout(request)
    return redirect('index')

def account(request):
    user = request.user
    user_profile, created = UserProfile.objects.get_or_create(user=user)

    if request.method == 'POST':
        email = request.POST.get('email')
        password = request.POST.get('password')
        first_name = request.POST.get('firstName')
        last_name = request.POST.get('lastName')

        user.username = email
        user.email = email
        user.first_name = first_name
        user.last_name = last_name

        if password:
            user.set_password(password)
            update_session_auth_hash(request, user)

        user.save()

        return JsonResponse({
            'status': 'success', 
            'message' : 'Данные успешно изменены'
        })

    try:
        if request.user.is_authenticated:
            context = {
                'username' : request.user.username,
                'first_name' : request.user.first_name,
                'birthdate' : request.user.userprofile.birthdate,
                'last_name' : request.user.last_name,
                'email' : request.user.email,
            }
            return render(request, 'account.html', context)
    except AttributeError:
        return HttpResponse('<h1>401 Unauthorized</h1>', status=401)