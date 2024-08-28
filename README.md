# Fruits CRUD
Это Telegram бот с backend-ом на REST API реализующее CRUD (create, read, update, delete) операции над фруктами.
## Требования
- Docker
## Инструкция по запуску (Через Docker):
1. `git clone https://github.com/filin121666/fruits_crud.git`
2. `cd fruits_crud`
3. Создайте файлы .env в директориях backend, bot и текущей директории, заполните их по примеру из файлов .env.example соответствующих директорий (для backend - backend/.env.example, для bot - bot/.env.example, для ./ - ./.env.example)
4. `docker compose up -d`
## Документация
Документация REST API находиться по адресу http://<хост приложения>:<порт приложения>/docs (например http://localhost:8000/docs, документация работает только, если сервер находится в рабочем состоянии!)
## История версий
- 1.0 (1.0.0) - Первая начальная версия которая содержала базовые операции (по id);
- 1.1.0 - Появление бота на aiogram 3 и добавление новых операций для backend-а (по названию).
- 1.1.1 - Добавление запуска через docker. В этой версии я уверен.