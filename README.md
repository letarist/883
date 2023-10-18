## Проект "Xabr"
## Сайт для обучения

### Базовая документация к проекту

Основные системные требования:

* Ubuntu 20.04 LTS
* Python 3.10
* PostgreSQL 12
* Django 4.0.3
* Зависимости (Python) из requirements.txt

### Установка необходимого ПО
#### обновляем информацию о репозиториях
```
apt update
```
#### Установка nginx, СУБД PostgreSQL, Git, virtualenv, gunicorn
nginx
```
apt install nginx
```
СУБД PostgreSQL
```
apt install postgresql postgresql-contrib
После установки проверяем статус СУБД, командой: service postgresql status
```
Git
```
apt install git-core
```
virtualenv
```
apt install python3-venv
```
gunicorn
```
apt install gunicorn
```
#### Настраиваем виртуальное окружение
При необходимости, для установки менеджера пакетов pip выполняем команду:
```
apt install python3-pip
```
Создаем и активируем виртуальное окружение:
```
python3 -m venv env
source env/bin/activate
```
Устанавливаем права:
```
chown -R hh env
```
Клонируем репозиторий:
```
git clone git@github.com:letarist/883.git /opt/venv/group_883
cd group_883/group_883
```
Ставим зависимости:
```
pip3 install -r requirements.txt
```
#### «PostgreSQL» Запускаем интерпретатор команд сервера:
```
sudo -u postgres psql
```
Создаем BD
```
CREATE DATABASE group_883;
```
Для проверки наличия бд «\l»
Для выхода пишем «\q».
#### Суперпользователь
```
python3 manage.py createsuperuser
```
к примеру (логин/пароль): admin:admin
#### Выполнение миграций и сбор статических файлов проекта
Выполняем миграции:
```
python3 manage.py migrate
```
Собираем статику:
```
python3 manage.py collectstatic
```
#### Заполнить базу данных тестовыми данными (не обязательно)
```
python3 manage.py fill
```
#### Тест запуска
```
python3 manage.py runserver
```
#### Назначение прав доступа
```
chown -R admin /home/admin/group_883
chmod -R 755 /home/admin/group_883
```
Настроим параметры службы «gunicorn»
```
sudo nano /etc/systemd/system/gunicorn.service


[Unit]
Description=gunicorn daemon
After=network.target

[Service]
User=USER_NAME
Group=www-data
WorkingDirectory=/home/xabr_env/xabr
ExecStart=/home/xabr_env/xabr/bin/gunicorn --access-logfile - --workers 3 --bind unix:/home/admin/group_883/group_883/group_883.sock group_883.wsgi

[Install]
WantedBy=multi-user.target

```
Активирование и запуск сервиса
```
sudo systemctl enable gunicorn
sudo systemctl start gunicorn
sudo systemctl status gunicorn
```
Настройки параметров для nginx
```
sudo nano /etc/nginx/sites-available/.conf

server {
    listen 80;
    server_name 89.108.88.136; ### server_name необхоимо написать ip-адрес сервера

    location = /favicon.ico { access_log off; log_not_found off; }
    location /static/ {
        root /home/admin/group_883/group_883/static;
    }

    location /media/ {
        root /home/admin/group_883/group_883/media;
    }
}
```
Перезапускаем службу «nginx»
```
sudo systemctl restart nginx
```
#### Активировируем сайт
```
sudo ln -s /etc/nginx/sites-available/xabr /etc/nginx/sites-enabled
```

### После этого в браузере можно ввести ip-адрес сервера и откроется проект.
#### Выкат изменений из Git:
```
source /home/admin/group_883/group_883/env/bin/activate
cd /home/admin/group_883
git pull origin master
pip3 install -r requirements.txt
python3 manage.py migrate
python3 manage.py collectstatic
