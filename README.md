# EN
## Necessary tools and running

### django project root
The project folder (where README.md is located) is distinct from the django project root folder (where manage.py is located), and before you enter the commands related to venv and others, you must go to the django project root folder.

```shell
cd digest
```

### venv
You must create *venv* folder.

```shell
python -m venv venv
```

For example to activate *venv* in Bash you should write the command.

```shell
source venv/bin/activate
```

To activate *venv* in PowerShell you should write.

```shell
venv\Scripts\Activate.ps1
```

### dotenv
You must install *dotenv*.

```Bash
pip install dotenv
```

### .env
You must create *.env* file in main project folder and write the following.

```Python
CLOUD_FOLDER = 'your_cloud_folder'
CLOUD_API_KEY = 'your_api_key'
CLOUD_MODEL = 'your_model,optional_fallback_model,...'
SERVER_ADMIN_KEY = 'your_custom_secret_key'
SALT = 'your_custom_secret_salt'
```

### Django
This project is using Django 6.0.5.

```shell
pip install Django==6.0.5 requests bs4 lxml openai
```

You must create *personal_info.py* alongside *digest/settings.py* and write the following.

```Python
MY_EMAIL_HOST_USER = 'your-email@example.com'
MY_EMAIL_HOST_PASSWORD = 'password-generated-for-SMTP'
```

You should apply migrations.

```shell
py manage.py migrate
```

Next you should run the server.

```shell
py manage.py runserver
```

To send the digest to the subscribers every sunday at noon in system local time, use an external scheduler. The following is an example for Alpine Linux.

Run `crontab -e` and add the following line.

```
# min   hour    day     month   weekday command
0       12      *       *       0       /path/to/this/project/send_emails.sh
```

Make sure the cron scheduler is running.

```shell
sudo rc-update add crond
sudo rc-service crond start
```

Before running in production, disable *DEBUG* in *digest/settings.py* as follows.

```python
DEBUG = False
```

And replace *SECRET_KEY* right above with a newly generated secret key. Generate it as follows. Do not use the key from this manual, generate your own.

```
$ python manage.py shell
15 objects imported automatically (use -v 2 for details).

Python 3.12.13 (main, Apr 10 2026, 13:58:11) [GCC 15.2.0] on linux
Type "help", "copyright", "credits" or "license" for more information.
(InteractiveConsole)
>>> from django.core.management.utils import get_random_secret_key
>>> print(get_random_secret_key())
e2&6dg+t8w0%4*9b167+jv^vvf7fuo)0+1oszm)*w0#&4ix0n2
>>> exit()
```

# RU
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

Перед запуском на боевом сервере, выключите *DEBUG* в *digest/settings.py* следующим образом.

```python
DEBUG = False
```

И замените *SECRET_KEY* чуть выше на вновь сгенерированный секретный ключ. Сгенерируйте его следующим образом. Не берите ключ из этой инструкции, сгенерируйте свой.

```
$ python manage.py shell
15 objects imported automatically (use -v 2 for details).

Python 3.12.13 (main, Apr 10 2026, 13:58:11) [GCC 15.2.0] on linux
Type "help", "copyright", "credits" or "license" for more information.
(InteractiveConsole)
>>> from django.core.management.utils import get_random_secret_key
>>> print(get_random_secret_key())
e2&6dg+t8w0%4*9b167+jv^vvf7fuo)0+1oszm)*w0#&4ix0n2
>>> exit()
```
