# Чтобы запустить проект локально, выполните следующие шаги:

## Откройте выбранную вами среду разработки и склонируйте репозиторий проекта:

### git clone https://github.com/savon01/Fast-API

## В терминале из директории проекта создайте виртуальное окружение с помощью следующей команды:
## python3 -m venv .venv
### Активируйте виртуальное окружение с помощью следующей команды:
## Для macOS/Linux:
### source .venv/bin/activate

## Для Windows:
### .venv\Scripts\activate

## Установите зависимости проекта с помощью следующей команды:
### pip install -r requirements.txt

## Перейдите в деректорию core, затем в файл db.py и заполните свои данные для подключение к бд в следующие переменные:
### POSTGRES_DB = "your_postgres_db_name"
### POSTGRES_USER = "your_postgres_username"
### POSTGRES_PASSWORD = "your_postgres_password"
### POSTGRES_HOST = "your_postgres_host"
### POSTGRES_PORT = "your_postgres_port"

## После этого запустите приложение с помощью следующей команды:
## uvicorn main:app --reload

# Теперь приложение запущено. Документация Swagger доступна по адресу:
### http://127.0.0.1:8000/
