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

Next you should run the server.

```shell
py manage.py runserver
```

# RU
## Необходимые инструменты и запуск

### venv 
Вы должны создать папку *venv*.

```shell
python -m venv venv
```

Например, чтобы активировать *venv* в Bash вы должны написать команду.

```shell
source venv/bin/activate
```

Чтобы активировать *venv* в PowerShell вы должны написать.

```shell
venv\Scripts\Activate.ps1
```

### dotenv
Вы должны установить *dotenv*.

```Bash
pip install dotenv
```

### .env
Вы должны создать файл *.env* файл в главной папке проекта и написать следующий код.

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

Далее вы должны запустить сервер.

```shell
py manage.py runserver
```