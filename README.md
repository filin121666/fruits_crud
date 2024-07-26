# Fruits CRUD
Это REST API реализующее CRUD (create, read, update, delete) операции над фруктами.
## Требования
- Python 3
- Pip 3 (если вы на Linux)
- PostgreSQL (psql)
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
9. Проведение миграции в базу данных
    ```shell
    alembic upgrade head
    ```
    Запуск приложения
    ```shell
    python main.py
    ```
## Инструкция по запуску (на Linux)
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
    pip3 install poetry
    ```
5. Установка виртуального окружения
    ```shell
    python3 -m poetry shell
    ```
6. Установка poetry в виртуальное окружение
    ```shell
    pip3 install poetry
    ```
7. Установка зависимостей
    ```shell
    python3 -m poetry install
    ```
8. Подключение к PostrgreSQL, для создания базы данных, нужно ввести данные (если они требуются)
    ```shell
    sudo -u  postgres -i psql
    ```
9. Создание базы данных и выход из psql
    ```shell
    CREATE DATABASE fruits;
    \q
    ```
10. Проведение миграции в базу данных
    ```shell
    python3 -m alembic upgrade head
    ```
11. Запуск приложения
    ```shell
    python3 main.py
    ```
## Документация
Документация REST API находиться по адресу http://<хост приложения>:<порт приложения>/docs (например http://127.0.0.1:8000/docs), документация работает только, если сервер находится в рабочем состоянии!
