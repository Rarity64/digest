from django.shortcuts import render, redirect, get_object_or_404
from .parsings.common_interface import get_news
from django.contrib.auth import login, logout, authenticate, update_session_auth_hash
from django.http import JsonResponse, HttpResponse
from django.core.mail import send_mail, EmailMultiAlternatives
from django.contrib.auth.models import User
from .models import UserProfile, EmailDigest, EmailCode
from django.core.exceptions import ValidationError, ObjectDoesNotExist, PermissionDenied
import random
import threading
from .parsings.common_interface import get_news
from .parsings.news_digest import get_important_news
from .parsings.server_admin_key import check, get_salt
from .parsings.cache_manager import clear_cache
import hashlib
from urllib.parse import urlencode
from django.conf import settings
import os
from dotenv import load_dotenv
load_dotenv()

def index(request):
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
        settings.EMAIL_HOST_USER,
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
                        return JsonResponse({'status' : 'success', 'redirect' : '/digest_desktop/'})
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
        subscribed = request.POST.get('subscribed')

        user.username = email
        user.email = email
        user.first_name = first_name
        user.last_name = last_name

        if subscribed == 'true':
            try:
                user.emaildigest.email = email
                user.emaildigest.save()
            except EmailDigest.DoesNotExist:
                EmailDigest.objects.create(
                    email = email,
                    user = user
                )
        else:
            try:
                user.emaildigest.delete()
            except EmailDigest.DoesNotExist:
                pass

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
            try:
                subscribed_email = request.user.emaildigest.email
                subscribed = True
            except EmailDigest.DoesNotExist:
                subscribed = False
            context = {
                'username' : request.user.username,
                'first_name' : request.user.first_name,
                'birthdate' : request.user.userprofile.birthdate,
                'last_name' : request.user.last_name,
                'email' : request.user.email,
                'subscribed' : subscribed,
            }
            return render(request, 'account.html', context)
    except AttributeError:
        return HttpResponse('<h1>401 Unauthorized</h1>', status=401)

def digest_desktop(request):
    if request.user.is_authenticated:
        CLOUD_MODEL = os.getenv("CLOUD_MODEL")
        print('Current model:', CLOUD_MODEL)
        context = { 'username' : request.user.username }
        return render(request, 'digest_desktop.html', context)
    else:
        raise PermissionDenied

django_to_parsings = {
    'habr.com': 'habr',
    'gazeta.ru': 'gazetaru',
    'lenta.ru': 'lentaru',
    'kommersant.ru': 'kommersant',
    'vedomosti.ru': 'vedomosti',
    'bashinform.ru': 'bashinform',
}

def all_news(request):
    if not request.user.is_authenticated:
        raise PermissionDenied
    source = request.GET.get('source')
    parsings_source = django_to_parsings[source]
    result = get_news(parsings_source)
    return JsonResponse({'status': 'success', 'news': result})

def important_news(request):
    if not request.user.is_authenticated:
        raise PermissionDenied
    source = request.GET.get('source')
    parsings_source = django_to_parsings[source]
    print(f'parsings_source: {parsings_source}')
    result = get_important_news(parsings_source)
    return JsonResponse({'status': 'success', 'news': result})

human_to_parsings = {
    'Хабр': 'habr',
    'Газета.ру': 'gazetaru',
    'Лента.ру': 'lentaru',
    'Коммерсантъ': 'kommersant',
    'Ведомости': 'vedomosti',
    'Башинформ': 'bashinform',
}

def build_important_news():
    news = []
    for i, j in human_to_parsings.items():
        news.append({
            'source': i,
            'items': get_important_news(j),
        })
    return news

def build_unsubscribe_token(obj):
    value = f'{obj.id}:{obj.email}'
    return hashlib.blake2b(
        value.encode('utf-8'),
        key=get_salt().encode('utf-8'),
        digest_size=8,
    ).hexdigest()

def build_unsubscribe_url(obj, host='http://localhost:8000'):
    token = build_unsubscribe_token(obj)
    return f'{host}/unsubscribe/?{urlencode({"email": obj.email, "token": build_unsubscribe_token(obj)})}'

def get_base_url():
    if hasattr(settings, 'SITE_URL'):
        return settings.SITE_URL.rstrip('/')
    allowed_hosts = getattr(settings, 'ALLOWED_HOSTS', [])
    if allowed_hosts:
        host = allowed_hosts[0]
        if host.startswith('http://') or host.startswith('https://'):
            return host.rstrip('/')
        return f'https://{host}'.rstrip('/')
    return 'http://localhost:8000'

def build_digest_html(news, obj):
    html = """
    <!DOCTYPE html>
    <html lang="ru">
    <head>
        <meta charset="UTF-8">
    </head>
    <body style="
        margin: 0;
        padding: 0;
        font-family: sans-serif;
    ">

    <div style="
        max-width: 700px;
        margin: 0 auto;
        padding: 30px 20px;
    ">

        <h1 style="
            text-align: center;
            margin-bottom: 40px;
            font-size: 32px;
        ">
            Важные новости
        </h1>
    """
    for source_data in news:
        source = source_data['source']
        items = source_data['items']
        html += f"""
        <div style="margin-bottom: 40px;">
        """
        for item in items:
            html += f"""
            <a href="{item['url']}" style="
                text-decoration: none;
                font-size: 16px;
                font-weight: bold;
                line-height: 1.4;
            ">
                {source}: {item['title']}
            </a>
            <br>
            """
        html += "</div>"
    base_url = get_base_url()
    unsubscribe_url = build_unsubscribe_url(obj, base_url)
    html += f"""
        <div style="
            margin-top: 50px;
            text-align: center;
            color: #777777;
            font-size: 13px;
        ">
            Вы получили это письмо потому, что подписаны на digest-рассылку.
            <br><br>

            <a href="{unsubscribe_url}" style="
                text-decoration: underline;
            ">
                Отписаться от рассылки
            </a>
        </div>

    </div>
    </body>
    </html>
    """
    return html

def build_digest_text(news, obj):
    text = """Важные новости
"""
    for source_data in news:
        source = source_data['source']
        items = source_data['items']
        text += f"""
{source}
"""
        for item in items:
            text += """
{item['title']}
{item['url']}
"""
    base_url = get_base_url()
    unsubscribe_url = build_unsubscribe_url(obj, base_url)
    text += f"""
Отписаться от рассылки: {unsubscribe_url}
"""
    return text

def unsubscribe(request):
    email = request.GET.get('email')
    token = request.GET.get('token')
    if EmailDigest.objects.filter(email=email).exists():
        if build_unsubscribe_token(EmailDigest.objects.filter(email=email).first()) == token:
            EmailDigest.objects.filter(email=email).delete()
            return render(request, 'unsubscribe_success.html')
    return render(request, 'unsubscribe_failure.html', status=400)

def send_digest(news, obj):
    html_content = build_digest_html(news, obj)
    text_content = build_digest_text(news, obj)
    email_message = EmailMultiAlternatives(
        subject='Важные новости',
        body=text_content,
        from_email=settings.EMAIL_HOST_USER,
        to=[obj.email],
    )
    email_message.attach_alternative(html_content, "text/html")
    email_message.send(fail_silently=False)

def email_everything_to_everyone():
    news = build_important_news()
    for obj in EmailDigest.objects.all():
        send_digest(news, obj)
    return JsonResponse({'status': 'success'})

def do(request):
    key = request.GET.get('key')
    if not check(key):
        raise PermissionDenied
    action = request.GET.get('action')
    if action == 'email_everything_to_everyone':
        return email_everything_to_everyone()
    if action == 'clear_cache':
        source = request.GET.get('source')
        kind = request.GET.get('kind')
        clear_cache(source, kind)
        return JsonResponse({'status': 'success'})
    return JsonResponse({'status': 'failure', 'error': 'unknown action'}, status=404)
