# Digest — a free self-hosted program where users can read new content from selected sites

Read in [Russian](./README_RU.md)

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
