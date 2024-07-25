# Fruits CRUD
Это REST API реализующее CRUD (create, read, update, delete) операции над фруктами.
## Инструкция по запуску (на windows)
1. Клонирование репозитория
```shell
git clone https://github.com/filin121666/fruits_crud.git
```
2. Переход в папку репозитория
```shell
cd fruits_crud
```
3. Нужно создать .env файл и заполнить его по примеру из файла .env.example
4. Установка poetry (по необходимости)
```shell
pip install poetry
```
5. Установка виртуального окружения
```shell
poetry shell
```
6. Установка зависимостей
```shell
poetry install
```
7. Подключение к PostrgreSQL, для создания базы данных, нужно ввести данные, запрашиваемые после выполнения этой команды
```shell
psql -U <ваше имя пользователя PostgreSQL>
```
8. Создание базы данных и выход из psql
```shell
CREATE DATABASE fruits;
\q
```
9.  Проведение миграции в базу данных
```shell
alembic upgrade head
```
10.  Запуск приложения
```shell
python main.py
```