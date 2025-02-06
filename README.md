# Django Project
https://www.tytrip.ru/

## Описание

Этот проект представляет собой веб-приложение, созданное с использованием Django. Он включает в себя основные функции, такие как аутентификация пользователей, управление контентом и API.

## Технологии

- Python 3.x
- Django
- Django REST Framework
- Redis
- SQLite/PostgreSQL (или другая СУБД по вашему выбору)
- OAuth 2.0

## Установка

1. Клонируйте репозиторий:

   ```sh
   git clone https://github.com/DTigi/mysite.git
   cd repository
   ```

2. Создайте и активируйте виртуальное окружение:

   ```sh
   python -m venv venv
   source venv/bin/activate  # Для macOS/Linux
   venv\Scripts\activate  # Для Windows
   ```

3. Установите зависимости:

   ```sh
   pip install -r requirements.txt
   ```

4. Примените миграции базы данных:

   ```sh
   python manage.py migrate
   ```

5. Создайте суперпользователя (при необходимости):

   ```sh
   python manage.py createsuperuser
   ```

6. Запустите сервер разработки:

   ```sh
   python manage.py runserver
   ```

## Использование

После запуска сервера приложение будет доступно по адресу [http://127.0.0.1:8000](http://127.0.0.1:8000).

## Конфигурация окружения

Создайте файл `.env` в корневой директории и добавьте в него необходимые переменные окружения:

```
SECRET_KEY=your_secret_key
DEBUG=True
DATABASE_URL=postgres://user:password@localhost:5432/dbname
```

## API эндпоинты

Приложение предоставляет RESTful API.

Примеры эндпоинтов:
- `GET /api/posts/` — Получить список постов
- `POST /api/feedback/` — Обратная связь
- `GET /api/posts/{slug}/` — Получить информацию о конкретном посте
- `GET /api/posts/?q=` — Поиск по сайту
- `POST /api/comments/` — Добавить комментарий
  
## Развертывание

Для развертывания на продакшн выполните следующие шаги:

1. Настройте файл `settings.py` (отключите `DEBUG`, настройте базу данных и `ALLOWED_HOSTS`).
2. Настройте статические файлы (`collectstatic`).
3. Настройте сервер (Gunicorn, Nginx, Docker и т. д.).


## Дополнительная информация
- [Django](https://www.djangoproject.com/)
- [Django REST Framework](https://www.django-rest-framework.org/)

### Автор
**DTigi** - [GitHub Profile](https://github.com/DTigi)


