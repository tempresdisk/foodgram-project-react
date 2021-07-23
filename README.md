# Проект Foodgram
Проект Foodgram сделан для публикации рецептов. Авторизованные пользователи
могут подписываться на понравившихся авторов, добавлять рецепты в избранное,
в покупки, скачать список покупок ингредиентов для добавленных в покупки
рецептов.

# Установка
Склонируйте репозиторий.
В корневой директории создайте файл `.env` со следующим содержанием:
```
SECRET_KEY= # секретный ключ django проекта
DB_ENGINE=django.db.backends.postgresql
DB_NAME=postgres
POSTGRES_USER=  # ваш вариант
POSTGRES_PASSWORD=  # ваш вариант
DB_HOST=db
DB_PORT=5432
```

Для запуска сервера на локальной машине выполните команды:
```
Первый запуск
docker-compose up -d
после запуска контейнеров
docker-compose exec web python manage.py migrate
docker-compose exec web python manage.py createsuperuser
docker-compose exec web python manage.py collectstatic --no-input

Последующие запуски
docker-compose up -d

```
Документацию к проекту можно посмотреть на странице `api/docs`.
Администрирование доступно на странице `/admin`.
Проект будет запущен и доступен по адресу [localhost](http://localhost).

Ознакомиться с уже развёрнутым проектом можно по адресу [Foodgram](http://178.154.252.191).

![Foodgram workflow](https://github.com/tempresdisk/foodgram-project-react/actions/workflows/foodgram_workflow.yaml/badge.svg)