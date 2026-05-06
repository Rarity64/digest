# EN
## Necessary tools and running

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
pip install Django==6.0.5
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
pip install Django==6.0.5
```

Подтвердите миграции.

```shell
py manage.py migrate
```

Далее запустите сервер.

```shell
py manage.py runserver
```