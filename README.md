## Установка

- Скачать код
```bash
git clone https://github.com/Alex-Men-VL/self_storage.git
cd self_storage
```
- Создать виртуальное окружение
```bash
python3 -m venv env
source env/bin/activate
```
- Установить зависимости
```bash
pip install -r requirements.txt
```
- Создать файл .env и вставить в него следующие строки:
```bash
DJANGO_DEBUG=True
DATABASE_URL=sqlite:///db.sqlite3
TELEGRAM_TOKEN=<Токен вашего бота>
```
- Запустите миграцию для настройки базы данных SQLite:
``` bash
python3 manage.py migrate
```
- Создайте суперпользователя, чтобы получить доступ к панели администратора:
``` bash
python3 manage.py createsuperuser
```

- Инициализация основных справочников:
``` bash
python3 manage.py shell
>>> from dbinit import init
>>> init()
```

## Запуск бота

```bash
python3 run_pooling.py 
```
## Запуск панели администратора:

``` bash
python3 manage.py runserver
```

Затем перейдите по [ссылке](http://127.0.0.1:8000/admin/).