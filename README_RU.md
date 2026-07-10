# Digest — свободная программа для локального развёртывания, в котором пользователи могут читать новый контент из определённых сайтов

Читать на [английском](./README.md)

## Необходимые инструменты и запуск

### корневая папка проекта django
Папка проекта (где находится README.md) отличается от корневой папки проекта django (где находится manage.py), и перед вводом команд, относящихся к venv и другому, необходимо перейти в корневую папку проекта django.

```
cd django
```

### venv 
Создайте папку *venv*.

```shell
python -m venv venv
```

Например, чтобы активировать *venv* в Bash напишите команду.

```shell
source venv/bin/activate
```

Чтобы активировать *venv* в PowerShell напишите.

```shell
venv\Scripts\Activate.ps1
```

### dotenv
Установите *dotenv*.

```Bash
pip install dotenv
```

### .env
Создайте файл *.env* файл в главной папке проекта и напишите следующий код.

```Python
CLOUD_FOLDER = 'your_cloud_folder'
CLOUD_API_KEY = 'your_api_key'
CLOUD_MODEL = 'your_model,optional_fallback_model,...'
SERVER_ADMIN_KEY = 'your_custom_secret_key'
SALT = 'your_custom_secret_salt'
```

### Django
Данный проект использует Django 6.0.5.

```shell
pip install Django==6.0.5 requests bs4 lxml openai
```

Создайте *personal_info.py* возле *digest/settings.py* и напишите следующее.

```Python
MY_EMAIL_HOST_USER = 'your-email@example.com'
MY_EMAIL_HOST_PASSWORD = 'password-generated-for-SMTP'
```

Подтвердите миграции.

```shell
py manage.py migrate
```

Далее запустите сервер.

```shell
py manage.py runserver
```

Чтобы посылать дайджест подписчикам каждое воскресенье в полдень по локальному времени системы, используйте внешний планировщик. Далее пример для Alpine Linux.

Выполните `crontab -e` и добавьте следующую строчку.

```
# минута  час     день    месяц   день недели  команда
0         12      *       *       0            /path/to/this/project/send_emails.sh
```

Убедитесь, что планировщик cron запущен.

```shell
sudo rc-update add crond
sudo rc-service crond start
```
