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
CLOUD_MODEL = 'your_model'
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
CLOUD_MODEL = 'your_model'
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
